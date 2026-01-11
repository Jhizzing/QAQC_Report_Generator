"""
Tests for error handling scenarios in FastAPI
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
from api.exceptions import (
    FileProcessingError,
    FileNotFoundError,
    AnalysisNotFoundError,
    ValidationError
)


def test_upload_file_too_large(client: TestClient):
    """Test upload of file exceeding size limit."""
    # Create a large file (simulate > 50MB)
    large_content = b'x' * (51 * 1024 * 1024)  # 51MB
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        tmp.write(large_content)
        tmp_path = Path(tmp.name)
    
    try:
        with open(tmp_path, 'rb') as f:
            response = client.post(
                "/api/upload",
                files={"file": ("large.csv", f, "text/csv")}
            )
        
        assert response.status_code == 400
        data = response.json()
        assert "error_code" in data or "detail" in data
    finally:
        tmp_path.unlink()


def test_upload_invalid_file_type(client: TestClient):
    """Test upload of invalid file type."""
    invalid_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
    invalid_file.write(b"Not a CSV or Excel file")
    invalid_file.close()
    
    try:
        with open(invalid_file.name, 'rb') as f:
            response = client.post(
                "/api/upload",
                files={"file": ("invalid.txt", f, "text/plain")}
            )
        
        assert response.status_code in [400, 422]
    finally:
        Path(invalid_file.name).unlink()


def test_preview_nonexistent_file(client: TestClient):
    """Test preview of non-existent file."""
    response = client.get("/api/preview/nonexistent-file-id")
    
    assert response.status_code == 404
    data = response.json()
    assert "error_code" in data or "detail" in data


def test_analyze_with_invalid_file_id(client: TestClient):
    """Test analysis with invalid file ID."""
    analysis_request = {
        "file_id": "invalid-file-id",
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
    data = response.json()
    assert "error_code" in data or "detail" in data


def test_analyze_with_invalid_parameters(client: TestClient, sample_csv_file: Path):
    """Test analysis with invalid parameters."""
    # First upload a file
    file_id = None
    with open(sample_csv_file, "rb") as f:
        upload_response = client.post(
            "/api/upload",
            files={"file": ("test.csv", f, "text/csv")}
        )
        if upload_response.status_code == 200:
            file_id = upload_response.json()["file_id"]
    
    if not file_id:
        pytest.skip("File upload failed, cannot test analysis")
    
    # Try analysis with invalid tolerance (negative)
    analysis_request = {
        "file_id": file_id,
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
            "standards_tolerance": -1.0,  # Invalid: negative
            "blanks_threshold": 0.01,
            "duplicates_rpd_limit": 10.0,
            "duplicates_hard_limit": 15.0
        }
    }
    
    response = client.post("/api/analyze", json=analysis_request)
    
    assert response.status_code in [400, 422]
    data = response.json()
    assert "error_code" in data or "detail" in data


def test_export_with_invalid_analysis_id(client: TestClient):
    """Test export with invalid analysis ID."""
    # Export uses POST, not GET
    response = client.post("/api/export/excel?analysis_id=invalid-id")
    
    assert response.status_code == 404
    data = response.json()
    assert "error_code" in data or "detail" in data


def test_preview_with_invalid_pagination(client: TestClient, sample_csv_file: Path):
    """Test preview with invalid pagination parameters."""
    # Upload file first
    file_id = None
    with open(sample_csv_file, "rb") as f:
        upload_response = client.post(
            "/api/upload",
            files={"file": ("test.csv", f, "text/csv")}
        )
        if upload_response.status_code == 200:
            file_id = upload_response.json()["file_id"]
    
    if not file_id:
        pytest.skip("File upload failed")
    
    # Try with negative offset
    response = client.get(f"/api/preview/{file_id}?offset=-1")
    
    assert response.status_code in [400, 422]
    
    # Try with invalid limit
    response = client.get(f"/api/preview/{file_id}?limit=0")
    
    assert response.status_code in [400, 422]
    
    # Try with limit too large
    response = client.get(f"/api/preview/{file_id}?limit=10000")
    
    assert response.status_code in [400, 422]
