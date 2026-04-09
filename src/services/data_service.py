"""
Data Service — handles file import, column mapping, and QC type detection.

This is the entry point for all data ingestion. It wraps DataImporter and
DataProcessor, providing a clean interface for the API layer.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from data import DataImporter, DataProcessor


class DataService:
    """Orchestrates data import, validation, and preparation."""

    def __init__(self) -> None:
        self.importer = DataImporter()
        self.processor = DataProcessor()
        self._current_df: Optional[pd.DataFrame] = None
        self._column_mapping: Dict[str, str] = {}

    def load_file(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Load a CSV or Excel file and return a preview.

        Returns:
            Dict with keys: columns, dtypes, row_count, preview (first 20 rows),
            suggested_mapping (auto-detected column roles).
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        df = self.importer.load_file(str(path), **kwargs)
        self._current_df = df

        return {
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "row_count": len(df),
            "preview": df.head(20).to_dict(orient="records"),
            "suggested_mapping": self._suggest_column_mapping(df),
        }

    def _suggest_column_mapping(self, df: pd.DataFrame) -> Dict[str, Optional[str]]:
        """Auto-detect which columns map to required fields."""
        mapping: Dict[str, Optional[str]] = {
            "sample_id": None,
            "assay_value": None,
            "qc_type": None,
            "original_sample_id": None,
        }

        col_lower = {col: col.lower().replace(" ", "_") for col in df.columns}

        sample_id_hints = ["sample_id", "sampleid", "sample", "sampno", "sample_no"]
        assay_hints = ["au_ppm", "au_gpt", "au", "result", "assay", "value", "grade"]
        qc_type_hints = ["qc_type", "qctype", "sample_type", "sampletype", "type"]
        orig_id_hints = ["original_sample", "orig_sample", "parent_id", "original_id"]

        for col, low in col_lower.items():
            if low in sample_id_hints and mapping["sample_id"] is None:
                mapping["sample_id"] = col
            if low in assay_hints and mapping["assay_value"] is None:
                mapping["assay_value"] = col
            if low in qc_type_hints and mapping["qc_type"] is None:
                mapping["qc_type"] = col
            if low in orig_id_hints and mapping["original_sample_id"] is None:
                mapping["original_sample_id"] = col

        return mapping

    def set_column_mapping(self, mapping: Dict[str, str]) -> None:
        """Set the user-confirmed column mapping."""
        self._column_mapping = mapping

    def detect_qc_types(self) -> Dict[str, int]:
        """
        Detect QC sample types in the loaded data.

        Returns:
            Dict with counts: {routine: N, standard: N, blank: N, duplicate: N}
        """
        if self._current_df is None:
            raise ValueError("No data loaded. Call load_file() first.")

        qc_col = self._column_mapping.get("qc_type")
        if not qc_col or qc_col not in self._current_df.columns:
            return {"routine": len(self._current_df), "standard": 0, "blank": 0, "duplicate": 0}

        type_col = self._current_df[qc_col].str.lower().str.strip()
        return {
            "routine": int((~type_col.isin(["standard", "std", "blank", "blk", "duplicate", "dup"])).sum()),
            "standard": int(type_col.isin(["standard", "std"]).sum()),
            "blank": int(type_col.isin(["blank", "blk"]).sum()),
            "duplicate": int(type_col.isin(["duplicate", "dup"]).sum()),
        }

    def get_prepared_data(self) -> pd.DataFrame:
        """Return the loaded DataFrame with column mapping applied."""
        if self._current_df is None:
            raise ValueError("No data loaded. Call load_file() first.")
        return self._current_df.copy()
