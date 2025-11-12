"""
CRM (Certified Reference Material) Manager for QAQC Analysis.

This module handles loading, querying, and managing CRM data from the YAML database.
It provides functionality to look up certified values, uncertainties, and other
CRM metadata for use in standards analysis.
"""

import yaml
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple

from src.utils.runtime_paths import resolve_runtime_path


class CRMManager:
    """
    Manages Certified Reference Material data for QAQC analysis.

    Key functionality:
    - Load CRM database from YAML
    - Query CRMs by name, matrix, or concentration range
    - Check CRM expiry dates
    - Get certified values and uncertainties
    - Validate CRM selection for analysis
    """

    def __init__(self, database_path: str = None) -> None:
        """
        Initialize CRM manager.

        Args:
            database_path: Path to CRM database YAML file
        """
        if database_path is None:
            resolved = resolve_runtime_path('crm_database.yaml')
        else:
            resolved = resolve_runtime_path(database_path)

        if resolved is None:
            raise FileNotFoundError(f"CRM database not found at {database_path or 'crm_database.yaml'}")

        self.database_path = str(resolved)
        self.database = self._load_database()

    def _load_database(self) -> Dict:
        """
        Load CRM database from YAML file.

        Returns:
            Dictionary containing CRM database
        """
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                database = yaml.safe_load(f)
            return database
        except FileNotFoundError:
            raise FileNotFoundError(f"CRM database not found at {self.database_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing CRM database: {e}")

    def get_all_crms(self) -> List[Dict]:
        """
        Get all CRMs from database.

        Returns:
            List of CRM dictionaries
        """
        return self.database.get('crms', [])

    def get_crm_by_name(self, name: str) -> Optional[Dict]:
        """
        Get CRM by exact name match.

        Args:
            name: CRM name to search for

        Returns:
            CRM dictionary if found, None otherwise
        """
        crms = self.get_all_crms()
        for crm in crms:
            if crm.get('name', '').lower() == name.lower():
                return crm
        return None

    def get_crms_by_matrix(self, matrix: str) -> List[Dict]:
        """
        Get CRMs by matrix type.

        Args:
            matrix: Matrix type to search for

        Returns:
            List of matching CRMs
        """
        crms = self.get_all_crms()
        matching = []
        for crm in crms:
            if matrix.lower() in crm.get('matrix', '').lower():
                matching.append(crm)
        return matching

    def get_crms_by_concentration_range(self, min_conc: float, max_conc: float) -> List[Dict]:
        """
        Get CRMs within a concentration range.

        Args:
            min_conc: Minimum concentration
            max_conc: Maximum concentration

        Returns:
            List of CRMs within the range
        """
        crms = self.get_all_crms()
        matching = []
        for crm in crms:
            conc = crm.get('certified_value', 0)
            if min_conc <= conc <= max_conc:
                matching.append(crm)
        return matching

    def get_crms_by_supplier(self, supplier: str) -> List[Dict]:
        """
        Get CRMs by supplier.

        Args:
            supplier: Supplier name to search for

        Returns:
            List of CRMs from the supplier
        """
        crms = self.get_all_crms()
        matching = []
        for crm in crms:
            if supplier.lower() in crm.get('supplier', '').lower():
                matching.append(crm)
        return matching

    def check_crm_expiry(self, crm_name: str) -> Tuple[bool, str]:
        """
        Check if CRM is expired.

        Args:
            crm_name: Name of CRM to check

        Returns:
            Tuple of (is_expired, message)
        """
        crm = self.get_crm_by_name(crm_name)
        if not crm:
            return True, f"CRM '{crm_name}' not found in database"

        expiry_date_str = crm.get('expiry_date')
        if not expiry_date_str:
            return False, "No expiry date specified"

        try:
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            today = date.today()

            if today > expiry_date:
                return True, f"CRM expired on {expiry_date_str}"
            else:
                days_remaining = (expiry_date - today).days
                return False, f"CRM valid until {expiry_date_str} ({days_remaining} days remaining)"

        except ValueError:
            return True, f"Invalid expiry date format: {expiry_date_str}"

    def get_certified_value(self, crm_name: str) -> Optional[float]:
        """
        Get certified value for a CRM.

        Args:
            crm_name: Name of CRM

        Returns:
            Certified value or None if not found
        """
        crm = self.get_crm_by_name(crm_name)
        return crm.get('certified_value') if crm else None

    def get_uncertainty(self, crm_name: str) -> Optional[float]:
        """
        Get uncertainty for a CRM.

        Args:
            crm_name: Name of CRM

        Returns:
            Uncertainty value or None if not found
        """
        crm = self.get_crm_by_name(crm_name)
        return crm.get('uncertainty') if crm else None

    def get_crm_info(self, crm_name: str) -> Optional[Dict]:
        """
        Get complete CRM information.

        Args:
            crm_name: Name of CRM

        Returns:
            Complete CRM dictionary or None if not found
        """
        return self.get_crm_by_name(crm_name)

    def validate_crm_selection(self, crm_name: str, sample_concentration: float) -> Tuple[bool, str]:
        """
        Validate CRM selection for a given sample concentration.

        Args:
            crm_name: Name of CRM to validate
            sample_concentration: Expected sample concentration

        Returns:
            Tuple of (is_valid, message)
        """
        crm = self.get_crm_by_name(crm_name)
        if not crm:
            return False, f"CRM '{crm_name}' not found in database"

        # Check expiry
        is_expired, expiry_msg = self.check_crm_expiry(crm_name)
        if is_expired:
            return False, f"CRM expired: {expiry_msg}"

        # Check concentration match (within 50% of certified value)
        certified_value = crm.get('certified_value', 0)
        if certified_value == 0:
            return False, "CRM has no certified value"

        concentration_ratio = sample_concentration / certified_value
        if not (0.5 <= concentration_ratio <= 2.0):
            return False, f"Sample concentration ({sample_concentration:.2f}) not suitable for CRM ({certified_value:.2f})"

        return True, f"CRM '{crm_name}' is valid for analysis"

    def get_analysis_thresholds(self) -> Dict:
        """
        Get analysis thresholds from database.

        Returns:
            Dictionary of analysis thresholds
        """
        return self.database.get('analysis_thresholds', {})

    def get_methods(self) -> Dict:
        """
        Get analysis methods from database.

        Returns:
            Dictionary of analysis methods
        """
        return self.database.get('methods', {})

    def search_crms(self, query: str) -> List[Dict]:
        """
        Search CRMs by query string.

        Args:
            query: Search query

        Returns:
            List of matching CRMs
        """
        crms = self.get_all_crms()
        matching = []
        query_lower = query.lower()

        for crm in crms:
            # Search in name, matrix, supplier, and notes
            searchable_text = ' '.join([
                crm.get('name', ''),
                crm.get('matrix', ''),
                crm.get('supplier', ''),
                crm.get('notes', '')
            ]).lower()

            if query_lower in searchable_text:
                matching.append(crm)

        return matching

    def get_database_info(self) -> Dict:
        """
        Get database information.

        Returns:
            Dictionary with database metadata
        """
        return self.database.get('database_info', {})

    def reload_database(self) -> None:
        """Reload CRM database from file."""
        self.database = self._load_database()

    def get_crm_summary(self) -> Dict:
        """
        Get summary statistics of CRM database.

        Returns:
            Dictionary with summary statistics
        """
        crms = self.get_all_crms()
        if not crms:
            return {'total_crms': 0}

        # Count by supplier
        suppliers = {}
        for crm in crms:
            supplier = crm.get('supplier', 'Unknown')
            suppliers[supplier] = suppliers.get(supplier, 0) + 1

        # Count by matrix
        matrices = {}
        for crm in crms:
            matrix = crm.get('matrix', 'Unknown')
            matrices[matrix] = matrices.get(matrix, 0) + 1

        # Concentration range
        concentrations = [crm.get('certified_value', 0) for crm in crms if crm.get('certified_value')]
        min_conc = min(concentrations) if concentrations else 0
        max_conc = max(concentrations) if concentrations else 0

        return {
            'total_crms': len(crms),
            'suppliers': suppliers,
            'matrices': matrices,
            'concentration_range': {
                'min': min_conc,
                'max': max_conc
            }
        }
