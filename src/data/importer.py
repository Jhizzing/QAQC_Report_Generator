"""
Data import utilities for QAQC analysis.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union
import difflib
import re

import pandas as pd

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # YAML is optional; only used if available


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

# Required canonical fields for downstream processing
REQUIRED_FIELDS: Tuple[str, ...] = (
    "sample_id",
    "sample_type",
    "result",
)

# Helpful optional fields commonly present in QAQC datasets
OPTIONAL_FIELDS: Tuple[str, ...] = (
    "hole_id",
    "from_depth",
    "to_depth",
    "lab",
    "method",
    "batch_id",
    "analyte",
    "units",
    "detection_limit",  # normalized DL column
)

# Canonical sample types
CANON_SAMPLE_TYPES = ("STANDARD", "BLANK", "DUPLICATE")
SAMPLE_TYPE_ALIASES: Dict[str, str] = {
    # Standards
    "std": "STANDARD",
    "crm": "STANDARD",
    "standard": "STANDARD",
    # Blanks
    "blank": "BLANK",
    "blk": "BLANK",
    "fieldblank": "BLANK",
    "labblank": "BLANK",
    # Duplicates / Checks
    "duplicate": "DUPLICATE",
    "dup": "DUPLICATE",
    "check": "DUPLICATE",
    "ck": "DUPLICATE",
}

# Synonyms for fuzzy matching (normalized)
SYNONYMS: Dict[str, Tuple[str, ...]] = {
    "sample_id": ("sampleid", "id", "sample", "sampno", "samp_id", "samp_id"),
    "sample_type": ("type", "samp_type", "qaqc_type", "class", "category"),
    "result": ("value", "assay", "grade", "analysis", "result_value"),
    "hole_id": ("holeid", "hole", "dhid", "drillhole", "collar"),
    "from_depth": ("from", "from_m", "from_depth_m", "depth_from"),
    "to_depth": ("to", "to_m", "to_depth_m", "depth_to"),
    "lab": ("laboratory", "lab_name"),
    "method": ("analysis_method", "method_code", "ana_method"),
    "batch_id": ("batch", "job", "job_id", "submission", "batchno"),
    "analyte": ("element", "commodity", "au", "cu", "zn"),
    "units": ("unit", "ppm", "ppb", "pct", "%"),
    "detection_limit": ("dl", "lod", "loq", "detectionlimit", "lowerdetectionlimit"),
}

# Patterns for qualifier parsing
LESS_THAN_PATTERN = re.compile(r"^\s*<\s*(\d+(?:\.\d+)?)\s*$")
GREATER_THAN_PATTERN = re.compile(r"^\s*>\s*(\d+(?:\.\d+)?)\s*$")
GENERIC_NUMBER_PATTERN = re.compile(r"^\s*([+-]?\d+(?:\.\d+)?)\s*$")

NEGATIVE_TOKENS = {"nd", "notdetected", "bdl", "<dl", "<lod"}
POSITIVE_TOKENS = {">dl", ">lod", ">loq"}


class ImportErrorUnsupportedFormat(Exception):
    """Raised when an unsupported file format is encountered."""


class ImportErrorReadFailed(Exception):
    """Raised when a file cannot be read with details."""


class ColumnMappingError(Exception):
    """Raised when required fields are missing in the mapping or headers."""


@dataclass
class ImportedFrame:
    """Container for an imported DataFrame with source metadata."""
    dataframe: pd.DataFrame
    source_path: Path


class DataImporter:
    """Data importer supporting CSV and Excel files, multi-file and directory input.

    Also provides hybrid column mapping: automatic suggestions with validation,
    and qualifier parsing + detection limit normalization.
    """

    def __init__(self) -> None:
        pass

    # --------------------------- Public API ---------------------------
    def import_csv(
        self,
        path: Union[str, Path],
        *,
        delimiter: Optional[str] = None,
        encoding: str = "utf-8",
        chunksize: Optional[int] = None,
        detect_encoding_fallback: bool = False,
    ) -> pd.DataFrame:
        """Backward-compatible CSV import wrapper around ``read_table``."""
        return self.read_table(
            path,
            csv_delimiter=delimiter,
            encoding=encoding,
            csv_chunksize=chunksize,
            detect_encoding_fallback=detect_encoding_fallback,
        )

    def read_table(
        self,
        path: Union[str, Path],
        *,
        csv_delimiter: Optional[str] = None,
        encoding: str = "utf-8",
        sheet_name: Optional[Union[str, int]] = 0,
        csv_chunksize: Optional[int] = None,
        detect_encoding_fallback: bool = False,
    ) -> pd.DataFrame:
        """Read a single CSV/XLSX/XLS file into a DataFrame.

        Args:
            csv_delimiter: Optional delimiter for CSV (e.g., "," or ";"). If None, pandas infers.
            encoding: Text encoding (default utf-8). For BOM CSVs, consider "utf-8-sig".
            sheet_name: Excel sheet name or index; default 0 (first sheet).
            csv_chunksize: If set, stream CSV in chunks and concatenate (memory-friendly).
            detect_encoding_fallback: If True and CSV read fails, try common encodings.
        """
        path = Path(path)
        ext = path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ImportErrorUnsupportedFormat(f"Unsupported file type: {ext}")

        try:
            if ext == ".csv":
                return self._read_csv(
                    path,
                    delimiter=csv_delimiter,
                    encoding=encoding,
                    chunksize=csv_chunksize,
                    detect_encoding_fallback=detect_encoding_fallback,
                )
            return self._read_excel(path, sheet_name=sheet_name)
        except Exception as exc:  # noqa: BLE001
            raise ImportErrorReadFailed(f"Failed to read '{path}': {exc}") from exc

    def read_many(
        self,
        paths: Sequence[Union[str, Path]],
        *,
        csv_delimiter: Optional[str] = None,
        encoding: str = "utf-8",
        sheet_name: Optional[Union[str, int]] = 0,
        csv_chunksize: Optional[int] = None,
        detect_encoding_fallback: bool = False,
    ) -> List[ImportedFrame]:
        """Read many files and return list of ImportedFrame."""
        results: List[ImportedFrame] = []
        for p in paths:
            df = self.read_table(
                p,
                csv_delimiter=csv_delimiter,
                encoding=encoding,
                sheet_name=sheet_name,
                csv_chunksize=csv_chunksize,
                detect_encoding_fallback=detect_encoding_fallback,
            )
            results.append(ImportedFrame(dataframe=df, source_path=Path(p)))
        return results

    def read_from_directory(
        self,
        directory: Union[str, Path],
        *,
        csv_delimiter: Optional[str] = None,
        encoding: str = "utf-8",
        sheet_name: Optional[Union[str, int]] = 0,
        csv_chunksize: Optional[int] = None,
        detect_encoding_fallback: bool = False,
    ) -> List[ImportedFrame]:
        """Scan a directory for supported files and read them all."""
        directory = Path(directory)
        files = sorted(
            f for f in directory.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
        )
        return self.read_many(
            files,
            csv_delimiter=csv_delimiter,
            encoding=encoding,
            sheet_name=sheet_name,
            csv_chunksize=csv_chunksize,
            detect_encoding_fallback=detect_encoding_fallback,
        )

    # ---------------------- Column mapping (hybrid) -------------------
    @staticmethod
    def normalize_header(name: str) -> str:
        """Normalize a header for matching: lowercase, strip, remove spaces/underscores.
        Also remove punctuation like '-' and '/'.
        """
        simplified = (
            name.strip().lower().replace(" ", "").replace("_", "").replace("-", "").replace("/", "")
        )
        return simplified

    def suggest_mapping(self, headers: Sequence[str], threshold: float = 0.85) -> Dict[str, Tuple[Optional[str], float]]:
        """Suggest a mapping from canonical fields to existing headers.

        Returns dict: {canonical_field: (matched_header_or_None, confidence_0_1)}
        """
        norm_headers = {self.normalize_header(h): h for h in headers}
        suggestions: Dict[str, Tuple[Optional[str], float]] = {}

        for canonical in list(REQUIRED_FIELDS) + list(OPTIONAL_FIELDS):
            targets = {canonical} | set(SYNONYMS.get(canonical, ()))
            targets_norm = [self.normalize_header(t) for t in targets]

            # Exact match first
            for t in targets_norm:
                if t in norm_headers:
                    suggestions[canonical] = (norm_headers[t], 1.0)
                    break
            else:
                # Fuzzy match
                best_match: Optional[str] = None
                best_score = 0.0
                for nh_norm, original in norm_headers.items():
                    score = max(difflib.SequenceMatcher(a=nh_norm, b=tg).ratio() for tg in targets_norm)
                    if score > best_score:
                        best_score, best_match = score, original
                if best_score >= threshold:
                    suggestions[canonical] = (best_match, best_score)
                else:
                    suggestions[canonical] = (None, best_score)

        return suggestions

    def validate_required(self, mapping: Dict[str, Optional[str]]) -> List[str]:
        """Return list of missing required canonical fields not present in mapping."""
        missing: List[str] = []
        for req in REQUIRED_FIELDS:
            if mapping.get(req) in (None, ""):
                missing.append(req)
        return missing

    def apply_mapping(self, df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """Apply a user-approved mapping and return a renamed DataFrame."""
        return df.rename(columns=mapping)

    def save_mapping_yaml(self, mapping: Dict[str, str], path: Union[str, Path]) -> None:
        if yaml is None:
            raise RuntimeError("PyYAML is not installed; cannot save mapping as YAML.")
        with open(Path(path), "w", encoding="utf-8") as f:
            yaml.safe_dump(mapping, f, sort_keys=True)

    def load_mapping_yaml(self, path: Union[str, Path]) -> Dict[str, str]:
        if yaml is None:
            raise RuntimeError("PyYAML is not installed; cannot load mapping from YAML.")
        with open(Path(path), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError("Invalid mapping YAML: expected a dict of {canonical: header}")
        # Coerce keys/values to str
        return {str(k): str(v) for k, v in data.items()}

    # --------------- Qualifier parsing & DL normalization --------------
    def parse_result_with_qualifier(
        self,
        text: Optional[str],
        default_dl: Optional[float] = None,
    ) -> Tuple[Optional[float], Optional[str], Optional[float]]:
        """Parse a raw result string into (numeric_value, qualifier, detection_limit).

        Supports patterns:
        - "<0.01" → (None, "<", 0.01)
        - ">10" → (None, ">", 10)
        - "ND" / "<DL" → (None, "<", default_dl)
        - plain number "1.23" → (1.23, None, None)
        - negative number "-0.02" → (None, "<", 0.02)
        """
        if text is None:
            return None, None, default_dl

        s = str(text).strip().lower()
        if s == "":
            return None, None, default_dl

        # Token patterns
        if s in NEGATIVE_TOKENS:
            return None, "<", default_dl
        if s in POSITIVE_TOKENS:
            return None, ">", default_dl

        # <number
        m = LESS_THAN_PATTERN.match(s)
        if m:
            return None, "<", float(m.group(1))

        # >number
        m = GREATER_THAN_PATTERN.match(s)
        if m:
            return None, ">", float(m.group(1))

        # plain/negative number
        m = GENERIC_NUMBER_PATTERN.match(s)
        if m:
            val = float(m.group(1))
            if val < 0:
                # Labs sometimes encode below-DL as negative numeric values
                return None, "<", abs(val)
            return val, None, None

        # Fallback: unrecognized string, return as missing value with no qualifier
        return None, None, default_dl

    def normalize_results(
        self,
        df: pd.DataFrame,
        result_col: str = "result",
        qualifier_col: str = "qualifier",
        dl_col: str = "detection_limit",
        default_dl: Optional[float] = None,
    ) -> pd.DataFrame:
        """Normalize result strings into numeric results and explicit qualifier/DL columns.

        - Parses qualifier tokens and numeric values
        - Writes qualifier to `qualifier_col`
        - Writes detection limit to `dl_col` (from parsed value, per-row DL, or default)
        - Leaves `result_col` numeric where possible (string inputs become parsed numeric)
        """
        results: List[Optional[float]] = []
        qualifiers: List[Optional[str]] = []
        dls: List[Optional[float]] = []

        raw_values = df[result_col] if result_col in df.columns else pd.Series([], dtype="object")
        # Pull existing per-row DLs if present
        existing_dls = None
        if dl_col in df.columns:
            try:
                existing_dls = pd.to_numeric(df[dl_col], errors="coerce").tolist()
            except Exception:
                existing_dls = [None] * len(df)
        else:
            existing_dls = [None] * len(raw_values)

        for idx, raw in enumerate(raw_values.astype("string", errors="ignore").tolist()):
            row_default_dl = existing_dls[idx] if idx < len(existing_dls) and existing_dls[idx] is not None else default_dl
            value, qual, dl = self.parse_result_with_qualifier(raw, default_dl=row_default_dl)
            results.append(value)
            qualifiers.append(qual)
            # Determine effective DL:
            if qual is not None:
                # For qualified values (<, >): prefer parsed dl; else row_default_dl
                effective_dl = dl if dl is not None else row_default_dl
            else:
                if value is None:
                    # Missing/blank result: use row_default_dl as the best available DL context
                    effective_dl = row_default_dl
                else:
                    # Plain numeric: keep existing per-row DL if any; otherwise None
                    effective_dl = existing_dls[idx] if idx < len(existing_dls) else None
            dls.append(effective_dl)

        out = df.copy()
        if len(results) == len(out):
            out[result_col] = results
        out[qualifier_col] = qualifiers
        out[dl_col] = dls
        return out

    def normalize_sample_type(self, df: pd.DataFrame, *, source_col: str = "sample_type", out_col: str = "sample_type") -> pd.DataFrame:
        """Normalize sample type labels to canonical values: STANDARD, BLANK, DUPLICATE.

        Unknown values are uppercased and left as-is.
        """
        if source_col not in df.columns:
            return df
        def _norm(v: object) -> object:
            if v is None:
                return v
            s = str(v).strip().lower().replace(" ", "")
            return SAMPLE_TYPE_ALIASES.get(s, str(v).strip().upper())
        out = df.copy()
        out[out_col] = out[source_col].map(_norm)
        return out

    # ------------------------- Internal helpers -----------------------
    def _read_csv(
        self,
        path: Path,
        *,
        delimiter: Optional[str] = None,
        encoding: str = "utf-8",
        chunksize: Optional[int] = None,
        detect_encoding_fallback: bool = False,
    ) -> pd.DataFrame:
        # First attempt with provided encoding
        try:
            common_kwargs = dict(
                dtype="unicode",
                na_values=["NA", "NaN", "#N/A", "", "null", "NULL"],
                keep_default_na=True,
                encoding=encoding,
                engine="python",
            )
            if delimiter is not None:
                common_kwargs["sep"] = delimiter
            if chunksize:
                chunks = pd.read_csv(
                    path,
                    **common_kwargs,
                    chunksize=chunksize,
                )
                return pd.concat(chunks, ignore_index=True)
            return pd.read_csv(
                path,
                **common_kwargs,
            )
        except Exception as first_exc:  # noqa: BLE001
            if not detect_encoding_fallback:
                raise
            # Try common encodings in order
            for enc in ("utf-8-sig", "cp1252", "latin1"):
                try:
                    common_kwargs = dict(
                        dtype="unicode",
                        na_values=["NA", "NaN", "#N/A", "", "null", "NULL"],
                        keep_default_na=True,
                        encoding=enc,
                        engine="python",
                    )
                    if delimiter is not None:
                        common_kwargs["sep"] = delimiter
                    if chunksize:
                        chunks = pd.read_csv(
                            path,
                            **common_kwargs,
                            chunksize=chunksize,
                        )
                        return pd.concat(chunks, ignore_index=True)
                    return pd.read_csv(
                        path,
                        **common_kwargs,
                    )
                except Exception:
                    continue
            # If all fail, re-raise original
            raise first_exc

    def _read_excel(self, path: Path, *, sheet_name: Optional[Union[str, int]] = 0) -> pd.DataFrame:
        # Read chosen sheet (default first). Users can pass name or index.
        return pd.read_excel(
            path,
            dtype="unicode",
            sheet_name=sheet_name,
            engine=None,  # let pandas choose installed engine (openpyxl/xlrd)
        )
