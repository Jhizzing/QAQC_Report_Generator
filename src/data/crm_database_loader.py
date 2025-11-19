import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional

class CRMDatabaseLoader:
    """
    Loads and queries the Industry CRM Database.
    """

    def __init__(self, csv_path: str = "data/industry_crms.csv"):
        """
        Initialize the loader.

        Args:
            csv_path: Path to the CRM database CSV file.
        """
        self.csv_path = csv_path
        self.data = None
        self._load_database()

    def _load_database(self):
        """Load the CSV database into a pandas DataFrame."""
        try:
            # Try to find the file relative to the project root if not found directly
            path = Path(self.csv_path)
            if not path.exists():
                # Assume we might be running from src/ or similar, try to find project root
                # This is a simple heuristic, can be improved
                project_root = Path(__file__).parent.parent.parent
                path = project_root / self.csv_path
            
            if path.exists():
                self.data = pd.read_csv(path)
            else:
                print(f"Warning: CRM database not found at {self.csv_path}")
                self.data = pd.DataFrame(columns=[
                    "CRM_ID", "Element", "CertifiedValue", "SD", "Unit", "Method", "Matrix", "Supplier"
                ])
        except Exception as e:
            print(f"Error loading CRM database: {e}")
            self.data = pd.DataFrame(columns=[
                "CRM_ID", "Element", "CertifiedValue", "SD", "Unit", "Method", "Matrix", "Supplier"
            ])

    def get_crm_details(self, crm_id: str, element: str = None) -> List[Dict]:
        """
        Get details for a specific CRM.

        Args:
            crm_id: The ID of the CRM (e.g., "OREAS 22e").
            element: Optional element to filter by (e.g., "Au").

        Returns:
            List of dictionaries containing CRM details.
        """
        if self.data is None or self.data.empty:
            return []

        query = self.data[self.data["CRM_ID"].astype(str).str.lower() == str(crm_id).lower()]
        
        if element:
            query = query[query["Element"].astype(str).str.lower() == str(element).lower()]

        return query.to_dict("records")

    def search_crms(self, 
                   element: str = None, 
                   min_grade: float = None, 
                   max_grade: float = None, 
                   matrix: str = None) -> List[Dict]:
        """
        Search for CRMs matching criteria.

        Args:
            element: Element to search for (e.g., "Au").
            min_grade: Minimum certified value.
            max_grade: Maximum certified value.
            matrix: Matrix type (substring match).

        Returns:
            List of matching CRMs.
        """
        if self.data is None or self.data.empty:
            return []

        result = self.data.copy()

        if element:
            result = result[result["Element"].astype(str).str.lower() == str(element).lower()]

        if min_grade is not None:
            result = result[result["CertifiedValue"] >= min_grade]

        if max_grade is not None:
            result = result[result["CertifiedValue"] <= max_grade]

        if matrix:
            result = result[result["Matrix"].astype(str).str.lower().str.contains(str(matrix).lower())]

        return result.to_dict("records")

    def get_all_crms(self) -> List[str]:
        """Get a list of all unique CRM IDs in the database."""
        if self.data is None or self.data.empty:
            return []
        return sorted(self.data["CRM_ID"].unique().tolist())

if __name__ == "__main__":
    # Simple test
    loader = CRMDatabaseLoader()
    print(f"Loaded {len(loader.data)} records.")
    
    au_crms = loader.search_crms(element="Au", min_grade=0.5, max_grade=2.0)
    print(f"Found {len(au_crms)} Au CRMs between 0.5 and 2.0 ppm:")
    for crm in au_crms:
        print(f" - {crm['CRM_ID']}: {crm['CertifiedValue']} {crm['Unit']} ({crm['Matrix']})")
