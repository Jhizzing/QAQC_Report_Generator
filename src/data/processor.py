"""
Data processing utilities for QAQC analysis.
"""
from __future__ import annotations

from typing import Any
import pandas as pd


class DataProcessor:
    """Minimal data processor stub."""

    def __init__(self) -> None:
        pass

    def categorize_samples(self, df: pd.DataFrame) -> pd.DataFrame:
        """Placeholder: return df unchanged."""
        return df

    def pair_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Placeholder: return df unchanged."""
        return df

    @staticmethod
    def _normalize_col_name(name: str) -> str:
        """Normalize header names for resilient matching."""
        return "".join(ch for ch in name.lower() if ch.isalnum())

    def _find_sample_type_column(self, df: pd.DataFrame) -> str | None:
        """Find sample type column across common naming conventions."""
        if 'sample_type' in df.columns:
            return 'sample_type'

        candidates = {
            "sampletype",
            "type",
            "qaqctype",
            "sampleclass",
            "samplecategory",
        }
        for col in df.columns:
            if self._normalize_col_name(str(col)) in candidates:
                return col
        return None

    def process_data(self, df: pd.DataFrame) -> dict[str, Any]:
        """Process data and return categorized samples.
        
        Args:
            df: Input DataFrame with sample data
            
        Returns:
            Dictionary with 'standards', 'blanks', 'duplicates' keys
        """
        # Categorize samples
        categorized = self.categorize_samples(df)

        sample_type_col = self._find_sample_type_column(categorized)
        if sample_type_col:
            sample_types = categorized[sample_type_col].fillna("").astype(str).str.upper()
        else:
            sample_types = pd.Series([""] * len(categorized), index=categorized.index)

        standards_mask = sample_types.isin(['STD', 'STANDARD', 'CRM'])
        blanks_mask = sample_types.isin(['BLK', 'BLANK'])
        duplicates_mask = sample_types.isin(['DUP', 'DUPLICATE', 'CK', 'CHECK'])
        known_mask = standards_mask | blanks_mask | duplicates_mask

        standards = categorized[standards_mask]
        blanks = categorized[blanks_mask]
        duplicates = categorized[duplicates_mask]
        unknowns = categorized[~known_mask]

        return {
            'standards': standards.to_dict('records') if not standards.empty else [],
            'blanks': blanks.to_dict('records') if not blanks.empty else [],
            'duplicates': duplicates.to_dict('records') if not duplicates.empty else [],
            'unknowns': unknowns
        }
