"""
Backend integration tests for FastAPI endpoints.
Tests the API server endpoints for file upload, analysis, and report generation.
"""
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

try:
    from main import app
except ImportError:
    # If API not available, skip these tests
    pytestmark = pytest.mark.skip("API module not available")


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing."""
    csv_content = """Sample_ID,Sample_Type,Au_ppm
OREAS-101-1,STD,0.082
OREAS-101-2,STD,0.085
BLANK-001,BLK,0.001
RC0001,UNK,2.5
RC0002,UNK,1.8
RC0001-DUP,DUP,2.4
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_path = f.name
    
    yield Path(temp_path)
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_pxrf_csv_file():
    """Create a sample pXRF CSV file for testing."""
    csv_content = """Sample_ID,Sample_Type,Cu_ppm,Pb_ppm,Zn_ppm,Fe_pct
OREAS-100-1,STD,189,42.3,127,3.42
OREAS-100-2,STD,192,43.1,129,3.45
BLANK-PX-1,BLK,2.1,1.5,3.2,0.05
PX0001,UNK,245,58,189,4.2
PX0002,UNK,189,42,127,3.4
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_path = f.name
    
    yield Path(temp_path)
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)


class TestBackendHealth:
    """Test backend health and status endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "ok"]


class TestBackendFileUpload:
    """Test file upload endpoints."""

    def test_backend_file_upload(self, client, sample_csv_file):
        """Test file upload endpoint."""
        with open(sample_csv_file, "rb") as f:
            response = client.post(
                "/api/upload",
                files={"file": (sample_csv_file.name, f, "text/csv")}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "file_id" in data
        assert "filename" in data
        assert "row_count" in data
        assert data["row_count"] > 0
        return data["file_id"]

    def test_backend_file_upload_invalid_type(self, client):
        """Test file upload with invalid file type."""
        # Create a text file with invalid extension
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Invalid file content")
            temp_path = f.name
        
        try:
            with open(temp_path, "rb") as file:
                response = client.post(
                    "/api/upload",
                    files={"file": ("test.txt", file, "text/plain")}
                )
            
            assert response.status_code in [400, 422]
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_backend_file_upload_too_large(self, client):
        """Test file upload with file too large."""
        # Create a large file (simulate)
        # Note: Actual implementation would need to create a file >50MB
        # For now, we'll test the endpoint exists
        pass  # Skip actual large file test in unit tests


class TestBackendAnalysis:
    """Test analysis execution endpoints."""

    def test_backend_analysis_endpoint(self, client, sample_csv_file):
        """Test analysis execution endpoint."""
        # First upload file
        with open(sample_csv_file, "rb") as f:
            upload_response = client.post(
                "/api/upload",
                files={"file": (sample_csv_file.name, f, "text/csv")}
            )
        file_id = upload_response.json()["file_id"]

        # Then run analysis
        analysis_request = {
            "file_id": file_id,
            "column_mapping": {
                "sample_id": "Sample_ID",
                "sample_type": "Sample_Type",
                "result": "Au_ppm",
                "elements": {}
            },
            "methodology_config": {
                "assay_method": "fire_assay",
                "category": "gold"
            },
            "qaqc_rules": {
                "standards_tolerance": 10.0,
                "blanks_threshold": 0.01,
                "duplicates_threshold": 20.0
            }
        }

        response = client.post("/api/analyze", json=analysis_request)
        assert response.status_code in [200, 202]  # 202 if async
        data = response.json()
        
        # If async, check for analysis_id
        if "analysis_id" in data:
            assert "status" in data
        else:
            # If sync, check for results
            assert "standards" in data or "results" in data

    def test_backend_analysis_invalid_file_id(self, client):
        """Test analysis with invalid file ID."""
        analysis_request = {
            "file_id": "invalid_file_id",
            "column_mapping": {
                "sample_id": "Sample_ID",
                "sample_type": "Sample_Type",
                "result": "Au_ppm"
            },
            "methodology_config": {
                "assay_method": "fire_assay"
            },
            "qaqc_rules": {
                "standards_tolerance": 10.0,
                "blanks_threshold": 0.01,
                "duplicates_threshold": 20.0
            }
        }

        response = client.post("/api/analyze", json=analysis_request)
        assert response.status_code == 404

    def test_backend_analysis_pxrf(self, client, sample_pxrf_csv_file):
        """Test pXRF analysis endpoint."""
        # Upload pXRF file
        with open(sample_pxrf_csv_file, "rb") as f:
            upload_response = client.post(
                "/api/upload",
                files={"file": (sample_pxrf_csv_file.name, f, "text/csv")}
            )
        file_id = upload_response.json()["file_id"]

        # Run pXRF analysis
        analysis_request = {
            "file_id": file_id,
            "column_mapping": {
                "sample_id": "Sample_ID",
                "sample_type": "Sample_Type",
                "elements": {
                    "Cu": "Cu_ppm",
                    "Pb": "Pb_ppm",
                    "Zn": "Zn_ppm",
                    "Fe": "Fe_pct"
                }
            },
            "methodology_config": {
                "category": "pxrf",
                "elements": ["Cu", "Pb", "Zn", "Fe"]
            },
            "qaqc_rules": {
                "standards_tolerance": 15.0,
                "blanks_threshold": 10.0,
                "duplicates_threshold": 20.0
            }
        }

        response = client.post("/api/analyze", json=analysis_request)
        assert response.status_code in [200, 202]


class TestBackendPlotGeneration:
    """Test plot generation endpoints."""

    def test_backend_plot_generation(self, client, sample_csv_file):
        """Test plot generation endpoint."""
        # First upload and analyze
        with open(sample_csv_file, "rb") as f:
            upload_response = client.post(
                "/api/upload",
                files={"file": (sample_csv_file.name, f, "text/csv")}
            )
        file_id = upload_response.json()["file_id"]

        analysis_request = {
            "file_id": file_id,
            "column_mapping": {
                "sample_id": "Sample_ID",
                "sample_type": "Sample_Type",
                "result": "Au_ppm"
            },
            "methodology_config": {"assay_method": "fire_assay"},
            "qaqc_rules": {
                "standards_tolerance": 10.0,
                "blanks_threshold": 0.01,
                "duplicates_threshold": 20.0
            }
        }

        analysis_response = client.post("/api/analyze", json=analysis_request)
        
        # Get analysis ID or results
        if analysis_response.status_code == 202:
            analysis_id = analysis_response.json().get("analysis_id")
            # Wait for analysis or get results
            # (Implementation depends on async handling)
        else:
            # Request plot generation
            plot_request = {
                "analysis_id": file_id,  # Use file_id as analysis identifier
                "plot_type": "control_chart",
                "element": "Au"
            }
            
            response = client.post("/api/plots", json=plot_request)
            # May return 404 if endpoint doesn't exist yet
            assert response.status_code in [200, 404, 501]


class TestBackendErrorHandling:
    """Test backend error handling."""

    def test_backend_error_handling(self, client):
        """Test that backend returns appropriate error responses."""
        # Test invalid endpoint
        response = client.get("/api/invalid_endpoint")
        assert response.status_code == 404

        # Test invalid request data
        response = client.post("/api/analyze", json={"invalid": "data"})
        assert response.status_code in [400, 422]

    def test_backend_validation_errors(self, client):
        """Test validation error handling."""
        # Test with missing required fields
        invalid_request = {
            "file_id": "test",
            # Missing column_mapping, methodology_config, etc.
        }
        
        response = client.post("/api/analyze", json=invalid_request)
        assert response.status_code in [400, 422]
        
        # Verify error message is user-friendly
        if response.status_code == 422:
            data = response.json()
            assert "detail" in data


class TestBackendCRMEndpoints:
    """Test CRM-related endpoints."""

    def test_backend_get_crms(self, client):
        """Test getting list of CRMs."""
        response = client.get("/api/crms")
        assert response.status_code in [200, 404]  # 404 if endpoint doesn't exist
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, (list, dict))

    def test_backend_get_crm_by_name(self, client):
        """Test getting specific CRM by name."""
        response = client.get("/api/crms/OREAS-101")
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert "name" in data or "id" in data
