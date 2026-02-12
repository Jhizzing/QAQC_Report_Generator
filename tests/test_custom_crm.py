
import pytest
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "react_ui" / "api"))

from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def custom_std_csv():
    """Create a CSV with a custom standard."""
    csv_content = """Sample_ID,Sample_Type,Au_ppm
MY-STD-01,STD,2.55
MY-STD-01,STD,2.48
MY-STD-01,STD,2.52
MY-STD-02,STD,5.01
UNK-01,UNK,0.5
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_path = f.name
    
    yield Path(temp_path)
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)

def test_custom_crm_analysis(client, custom_std_csv):
    """Test that custom CRMs passed in request are used."""
    
    # 1. Upload
    with open(custom_std_csv, "rb") as f:
        upload_resp = client.post(
            "/api/upload",
            files={"file": (custom_std_csv.name, f, "text/csv")}
        )
    assert upload_resp.status_code == 200
    file_id = upload_resp.json()["file_id"]
    
    # 2. Analyze with Custom CRM definitions
    request_data = {
        "file_id": file_id,
        "column_mapping": {
            "sample_id": "Sample_ID",
            "sample_type": "Sample_Type",
            "result": "Au_ppm"
        },
        "methodology": {
            "assay_method": "fire_assay",
            "category": "gold"
        },
        "qaqc_rules": {
            "standards_tolerance": 2.0,
            "blanks_threshold": 0.01,
            "duplicates_rpd_limit": 10.0,
            "duplicates_hard_limit": 15.0
        },
        "crms": [
            {
                "name": "MY-STD-01",
                "certified_value": 2.50,
                "uncertainty": 0.05,
                "unit": "ppm"
            },
            {
                "name": "MY-STD-02",
                "certified_value": 5.00,
                "uncertainty": 0.1,
                "unit": "ppm"
            }
        ]
    }
    
    resp = client.post("/api/analyze", json=request_data)
    assert resp.status_code == 200
    result = resp.json()
    
    standards_stats = result["standards"]["statistics"]
    
    # Check if we have results for both standards
    assert len(standards_stats) >= 2
    
    # Check MY-STD-01
    std1 = next((s for s in standards_stats if s["crm"] == "MY-STD-01"), None)
    assert std1 is not None
    # Mean of 2.55, 2.48, 2.52 -> 2.5166
    assert 2.4 < std1["mean"] < 2.6
    assert std1["found_in_db"] is True
    
    # Check MY-STD-02
    std2 = next((s for s in standards_stats if s["crm"] == "MY-STD-02"), None)
    assert std2 is not None
    assert 4.9 < std2["mean"] < 5.1
    assert std2["found_in_db"] is True

def test_missing_custom_crm(client, custom_std_csv):
    """Test behavior when custom CRM is NOT provided."""
    # 1. Upload
    with open(custom_std_csv, "rb") as f:
        upload_resp = client.post(
            "/api/upload",
            files={"file": (custom_std_csv.name, f, "text/csv")}
        )
    file_id = upload_resp.json()["file_id"]
    
    # 2. Analyze WITHOUT Custom CRM definitions
    request_data = {
        "file_id": file_id,
        "column_mapping": {
            "sample_id": "Sample_ID",
            "sample_type": "Sample_Type",
            "result": "Au_ppm"
        },
        "methodology": {
            "assay_method": "fire_assay",
            "category": "gold"
        },
        "qaqc_rules": {
             "standards_tolerance": 2.0,
             "blanks_threshold": 0.01,
             "duplicates_rpd_limit": 10.0,
             "duplicates_hard_limit": 15.0
        },
        "crms": [] # Empty
    }
    
    resp = client.post("/api/analyze", json=request_data)
    assert resp.status_code == 200
    result = resp.json()
    
    standards_stats = result["standards"]["statistics"]
    std1 = next((s for s in standards_stats if s["crm"] == "MY-STD-01"), None)
    
    assert std1 is not None
    # Should use default fallback (1.0 or whatever crm_manager returns)
    # Since "MY-STD-01" is likely not in the yaml DB, it might use fallback
    # In my logic: certified_val = 1.0 if not found
    
    # Measured ~2.5, Certified 1.0 -> FAIL
    assert std1["found_in_db"] is False
    # Check data points for failure
    points = result["standards"]["data_points"]
    p1 = next((p for p in points if p["crm_id"] == "MY-STD-01"), None)
    if p1:
        assert p1["certified_value"] == 1.0
