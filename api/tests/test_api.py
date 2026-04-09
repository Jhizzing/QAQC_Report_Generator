"""
Tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import json
import sys

# Ensure we can import the app
try:
    from conftest import client, sample_csv_file, sample_excel_file, invalid_file
except ImportError:
    # If running tests directly, we need to set up the path
    import os
    api_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(api_dir))
    from tests.conftest import client, sample_csv_file, sample_excel_file, invalid_file


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_upload_csv(client: TestClient, sample_csv_file: Path):
    """Test CSV file upload. Returns file_id for use in other tests."""
    with open(sample_csv_file, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": ("test_data.csv", f, "text/csv")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert "filename" in data
    assert data["filename"] == "test_data.csv"
    # Return file_id for use in other tests (pytest allows this)
    return data["file_id"]  # type: ignore


def test_upload_excel(client: TestClient, sample_excel_file: Path):
    """Test Excel file upload. Returns file_id for use in other tests."""
    with open(sample_excel_file, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": ("test_data.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    # Return file_id for use in other tests (pytest allows this)
    return data["file_id"]  # type: ignore


def test_upload_invalid_file(client: TestClient, invalid_file: Path):
    """Test upload of invalid file format."""
    with open(invalid_file, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": ("invalid.txt", f, "text/plain")}
        )
    
    # Should return error for invalid file
    assert response.status_code in [400, 422]


def test_preview_data(client: TestClient, sample_csv_file: Path):
    """Test data preview endpoint."""
    # First upload a file
    file_id = test_upload_csv(client, sample_csv_file)
    
    # Then preview it
    response = client.get(f"/api/preview/{file_id}")
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data
    assert "data" in data
    assert len(data["data"]) > 0


def test_preview_invalid_file_id(client: TestClient):
    """Test preview with invalid file ID."""
    response = client.get("/api/preview/invalid-id")
    assert response.status_code == 404


def test_analyze_endpoint(client: TestClient, sample_csv_file: Path):
    """Test analysis execution endpoint."""
    # Upload file first
    file_id = test_upload_csv(client, sample_csv_file)
    
    # Prepare analysis request
    analysis_request = {
        "file_id": file_id,
        "column_mapping": {
            "sample_id": "SampleID",
            "sample_type": "Type",
            "result": "Result",
            "elements": {"Au": "Result"}
        },
        "methodology": {
            "assay_method": "fire_assay",
            "duplicate_strategy": "field_duplicate",
            "insertion_rate": 5.0
        },
        "qaqc_rules": {
            "standards_tolerance": 2.0,
            "blanks_threshold": 0.01,
            "duplicates_rpd_limit": 10.0,
            "duplicates_hard_limit": 15.0
        }
    }
    
    response = client.post("/api/analyze", json=analysis_request)
    assert response.status_code == 200
    data = response.json()
    assert "analysis_id" in data
    # Response has separate sections: standards, blanks, duplicates, summary
    assert "standards" in data or "summary" in data
    # Return analysis_id for use in other tests (pytest allows this)
    return data["analysis_id"]  # type: ignore


def test_analyze_invalid_file_id(client: TestClient):
    """Test analysis with invalid file ID."""
    analysis_request = {
        "file_id": "invalid-id",
        "column_mapping": {
            "sample_id": "SampleID",
            "sample_type": "Type",
            "result": "Result"
        },
        "methodology": {
            "assay_method": "fire_assay",
            "duplicate_strategy": "field_duplicate",
            "insertion_rate": 5.0
        },
        "qaqc_rules": {
            "standards_tolerance": 2.0,
            "blanks_threshold": 0.01,
            "duplicates_rpd_limit": 10.0,
            "duplicates_hard_limit": 15.0
        }
    }
    
    response = client.post("/api/analyze", json=analysis_request)
    assert response.status_code == 404


def test_export_excel(client: TestClient, sample_csv_file: Path):
    """Test Excel export endpoint."""
    # Run analysis first
    analysis_id = test_analyze_endpoint(client, sample_csv_file)
    
    # Export to Excel (uses POST, not GET)
    response = client.post(f"/api/export/excel?analysis_id={analysis_id}")
    assert response.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in response.headers.get("content-type", "")


def test_export_pdf(client: TestClient, sample_csv_file: Path):
    """Test PDF export endpoint."""
    # Run analysis first
    analysis_id = test_analyze_endpoint(client, sample_csv_file)
    
    # Export to PDF (uses POST, not GET)
    response = client.post(f"/api/export/pdf?analysis_id={analysis_id}")
    assert response.status_code == 200
    assert "application/pdf" in response.headers.get("content-type", "")


def test_export_invalid_analysis_id(client: TestClient):
    """Test export with invalid analysis ID."""
    # Export uses POST, not GET
    response = client.post("/api/export/excel?analysis_id=invalid-id")
    assert response.status_code == 404


def test_crms_list(client: TestClient):
    """Test CRM listing endpoint."""
    response = client.get("/api/crms")
    assert response.status_code == 200
    data = response.json()
    # Response is an object with "crms" and "total" keys
    assert "crms" in data
    assert "total" in data
    assert isinstance(data["crms"], list)
    if len(data["crms"]) > 0:
        # Check structure of CRM objects
        assert "batch_number" in data["crms"][0] or "name" in data["crms"][0]


def test_crms_search(client: TestClient):
    """Test CRM search endpoint."""
    response = client.get("/api/crms?search=OREAS")
    assert response.status_code == 200
    data = response.json()
    # Response is an object with "crms" and "total" keys
    assert "crms" in data
    assert "total" in data
    assert isinstance(data["crms"], list)
    assert len(data["crms"]) > 0


def test_crms_category_filter(client: TestClient):
    """Test CRM category filtering."""
    # Note: API uses "element" parameter, not "category"
    response = client.get("/api/crms?element=Au")
    assert response.status_code == 200
    data = response.json()
    # Response is an object with "crms" and "total" keys
    assert "crms" in data
    assert "total" in data
    assert isinstance(data["crms"], list)
