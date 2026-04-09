"""
Analysis Service — orchestrates standards, blanks, and duplicates analysis.

Single entry point for running QAQC analysis. Consumes prepared data from
DataService and CRM info from CRMService, delegates to core analyzers.
"""

from typing import Any, Dict, List, Optional

import pandas as pd
import numpy as np

from analysis import StandardsAnalyzer


class AnalysisService:
    """Runs QAQC analysis and returns structured results."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.standards_analyzer = StandardsAnalyzer(self.config)
        self._last_results: Optional[Dict[str, Any]] = None

    def run_full_analysis(
        self,
        df: pd.DataFrame,
        column_mapping: Dict[str, str],
        crm_matches: Dict[str, Dict[str, Any]],
        thresholds: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run complete QAQC analysis on prepared data.

        Args:
            df: Prepared DataFrame with assay data.
            column_mapping: Map of role -> column name.
            crm_matches: Map of standard name -> CRM details.
            thresholds: Optional override thresholds (LDL, RPD limit, etc.)

        Returns:
            Dict with keys: standards, blanks, duplicates, summary.
        """
        thresh = {
            "ldl": 0.03,
            "rpd_limit": 20.0,
            "warning_sd": 2.0,
            "fail_sd": 3.0,
            **(thresholds or {}),
        }

        qc_col = column_mapping.get("qc_type", "qc_type")
        value_col = column_mapping.get("assay_value", "result")
        sample_col = column_mapping.get("sample_id", "sample_id")
        orig_col = column_mapping.get("original_sample_id")

        standards_result = self._analyse_standards(df, qc_col, value_col, sample_col, crm_matches, thresh)
        blanks_result = self._analyse_blanks(df, qc_col, value_col, sample_col, thresh)
        duplicates_result = self._analyse_duplicates(df, qc_col, value_col, sample_col, orig_col, thresh)

        summary = self._build_summary(df, qc_col, standards_result, blanks_result, duplicates_result)

        self._last_results = {
            "standards": standards_result,
            "blanks": blanks_result,
            "duplicates": duplicates_result,
            "summary": summary,
        }
        return self._last_results

    def _analyse_standards(
        self, df, qc_col, value_col, sample_col, crm_matches, thresh
    ) -> Dict[str, Any]:
        """Analyse CRM standards against certified values."""
        mask = df[qc_col].str.lower().str.strip().isin(["standard", "std"])
        standards_df = df[mask].copy()

        if standards_df.empty:
            return {"status": "no_data", "records": [], "pass_count": 0, "fail_count": 0, "warning_count": 0}

        records = []
        for _, row in standards_df.iterrows():
            sample_name = str(row[sample_col])
            measured = float(row[value_col]) if pd.notna(row[value_col]) else None
            crm = crm_matches.get(sample_name, {})
            certified = crm.get("certified_value")
            uncertainty = crm.get("uncertainty")

            if measured is None or certified is None or uncertainty is None or uncertainty == 0:
                records.append({"sample_id": sample_name, "measured": measured, "status": "unmapped"})
                continue

            z_score = (measured - certified) / uncertainty
            recovery = (measured / certified) * 100 if certified != 0 else None

            if abs(z_score) > thresh["fail_sd"]:
                status = "fail"
            elif abs(z_score) > thresh["warning_sd"]:
                status = "warning"
            else:
                status = "pass"

            records.append({
                "sample_id": sample_name,
                "measured": measured,
                "certified_value": certified,
                "uncertainty": uncertainty,
                "z_score": round(z_score, 3),
                "recovery_pct": round(recovery, 2) if recovery else None,
                "status": status,
            })

        pass_count = sum(1 for r in records if r.get("status") == "pass")
        fail_count = sum(1 for r in records if r.get("status") == "fail")
        warning_count = sum(1 for r in records if r.get("status") == "warning")

        return {
            "status": "complete",
            "records": records,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "warning_count": warning_count,
            "total": len(records),
        }

    def _analyse_blanks(self, df, qc_col, value_col, sample_col, thresh) -> Dict[str, Any]:
        """Analyse field blanks against lower detection limit."""
        mask = df[qc_col].str.lower().str.strip().isin(["blank", "blk"])
        blanks_df = df[mask].copy()

        if blanks_df.empty:
            return {"status": "no_data", "records": [], "pass_count": 0, "fail_count": 0}

        ldl = thresh["ldl"]
        records = []
        for _, row in blanks_df.iterrows():
            measured = float(row[value_col]) if pd.notna(row[value_col]) else 0.0
            status = "fail" if measured > ldl else "pass"
            records.append({
                "sample_id": str(row[sample_col]),
                "measured": measured,
                "ldl": ldl,
                "status": status,
            })

        pass_count = sum(1 for r in records if r["status"] == "pass")
        fail_count = sum(1 for r in records if r["status"] == "fail")

        return {
            "status": "complete",
            "records": records,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "total": len(records),
            "contamination_rate_pct": round(fail_count / len(records) * 100, 2) if records else 0,
        }

    def _analyse_duplicates(self, df, qc_col, value_col, sample_col, orig_col, thresh) -> Dict[str, Any]:
        """Analyse duplicate pairs — primary vs duplicate RPD."""
        mask = df[qc_col].str.lower().str.strip().isin(["duplicate", "dup"])
        dups_df = df[mask].copy()

        if dups_df.empty or orig_col is None:
            return {"status": "no_data", "records": [], "pass_count": 0, "fail_count": 0}

        rpd_limit = thresh["rpd_limit"]
        records = []

        for _, dup_row in dups_df.iterrows():
            orig_id = str(dup_row.get(orig_col, ""))
            orig_rows = df[df[sample_col].astype(str) == orig_id]
            if orig_rows.empty:
                continue

            orig_value = float(orig_rows.iloc[0][value_col]) if pd.notna(orig_rows.iloc[0][value_col]) else None
            dup_value = float(dup_row[value_col]) if pd.notna(dup_row[value_col]) else None

            if orig_value is None or dup_value is None:
                continue

            mean_val = (orig_value + dup_value) / 2
            rpd = abs(orig_value - dup_value) / mean_val * 100 if mean_val != 0 else 0
            status = "fail" if rpd > rpd_limit else "pass"

            records.append({
                "sample_id": str(dup_row[sample_col]),
                "original_id": orig_id,
                "original_value": orig_value,
                "duplicate_value": dup_value,
                "rpd": round(rpd, 2),
                "status": status,
            })

        pass_count = sum(1 for r in records if r["status"] == "pass")
        fail_count = sum(1 for r in records if r["status"] == "fail")
        rpd_values = [r["rpd"] for r in records]

        return {
            "status": "complete",
            "records": records,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "total": len(records),
            "mean_rpd": round(float(np.mean(rpd_values)), 2) if rpd_values else 0,
            "median_rpd": round(float(np.median(rpd_values)), 2) if rpd_values else 0,
        }

    def _build_summary(self, df, qc_col, standards, blanks, duplicates) -> Dict[str, Any]:
        """Build the summary statistics table."""
        total = len(df)
        n_std = standards.get("total", 0)
        n_blk = blanks.get("total", 0)
        n_dup = duplicates.get("total", 0)
        n_qaqc = n_std + n_blk + n_dup

        total_warnings = standards.get("warning_count", 0)
        total_fails = (
            standards.get("fail_count", 0)
            + blanks.get("fail_count", 0)
            + duplicates.get("fail_count", 0)
        )

        overall_status = "PASS" if total_fails == 0 else "FAIL"

        return {
            "total_samples": total,
            "total_qaqc": n_qaqc,
            "standards_count": n_std,
            "standards_pct": round(n_std / total * 100, 1) if total else 0,
            "blanks_count": n_blk,
            "blanks_pct": round(n_blk / total * 100, 1) if total else 0,
            "duplicates_count": n_dup,
            "duplicates_pct": round(n_dup / total * 100, 1) if total else 0,
            "total_warnings": total_warnings,
            "total_fails": total_fails,
            "overall_status": overall_status,
        }
