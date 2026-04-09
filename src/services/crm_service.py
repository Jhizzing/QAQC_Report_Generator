"""
CRM Service — manages the Certified Reference Material database.

Wraps CRMManager to provide CRUD operations and fuzzy matching for the
standard-to-CRM confirmation step in the wizard.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from data.crm_manager import CRMManager


class CRMService:
    """Interface for CRM database operations."""

    def __init__(self, database_path: Optional[str] = None) -> None:
        self.manager = CRMManager(database_path=database_path)

    def get_all_crms(self) -> List[Dict[str, Any]]:
        """Return all CRMs in the database."""
        return self.manager.get_all_crms()

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Full-text search across CRM names, suppliers, matrices."""
        return self.manager.search_crms(query)

    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Look up a single CRM by name (case-insensitive)."""
        return self.manager.get_crm_by_name(name)

    def get_by_supplier(self, supplier: str) -> List[Dict[str, Any]]:
        """Filter CRMs by supplier."""
        return self.manager.get_crms_by_supplier(supplier)

    def get_by_concentration_range(
        self, min_conc: float, max_conc: float
    ) -> List[Dict[str, Any]]:
        """Filter CRMs by certified value range."""
        return self.manager.get_crms_by_concentration_range(min_conc, max_conc)

    def match_standards_to_crms(
        self, standard_names: List[str]
    ) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        Attempt to auto-match detected standard sample names to CRM records.

        Returns:
            Dict mapping each standard name to its best CRM match (or None).
        """
        matches: Dict[str, Optional[Dict[str, Any]]] = {}
        all_crms = self.manager.get_all_crms()

        for name in standard_names:
            name_lower = name.lower().strip()
            best = None

            # Exact match first
            for crm in all_crms:
                if crm["name"].lower() == name_lower:
                    best = crm
                    break

            # Substring match fallback
            if best is None:
                for crm in all_crms:
                    crm_lower = crm["name"].lower()
                    if crm_lower in name_lower or name_lower in crm_lower:
                        best = crm
                        break

            matches[name] = best

        return matches

    def add_local_crm(self, crm_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a user-defined CRM to the local database.

        Required fields: name, certified_value, uncertainty.
        Optional: units, matrix, supplier, notes.
        """
        required = ["name", "certified_value", "uncertainty"]
        for field in required:
            if field not in crm_data:
                raise ValueError(f"Missing required field: {field}")

        crm = {
            "name": crm_data["name"],
            "certified_value": float(crm_data["certified_value"]),
            "uncertainty": float(crm_data["uncertainty"]),
            "units": crm_data.get("units", "g/t"),
            "matrix": crm_data.get("matrix", "Unknown"),
            "supplier": crm_data.get("supplier", "User-defined"),
            "notes": crm_data.get("notes", ""),
            "source": "local",
        }

        # Append to the in-memory database
        self.manager._crm_database.setdefault("standards", []).append(crm)
        return crm

    def get_thresholds(self) -> Dict[str, Any]:
        """Return analysis threshold configuration."""
        return self.manager.get_analysis_thresholds()
