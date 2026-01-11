"""
Pytest configuration and fixtures for API tests
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator
from fastapi.testclient import TestClient
from fastapi import FastAPI
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Import the app after path setup
# Note: Import path may need adjustment based on how the API is run
try:
    from api.main import app
except ImportError:
    # Try alternative import path
    import sys
    api_path = Path(__file__).parent.parent
    sys.path.insert(0, str(api_path))
    from main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_csv_file(temp_dir: Path) -> Path:
    """Create a sample CSV file for testing."""
    csv_path = temp_dir / "test_data.csv"
    csv_content = """SampleID,Type,Result,Element
STD-001,STD,10.5,Au
BLK-001,BLK,0.01,Au
DUP-001-OR,UNK,15.2,Au
DUP-001-CK,UNK,15.8,Au"""
    csv_path.write_text(csv_content)
    return csv_path


@pytest.fixture
def sample_excel_file(temp_dir: Path) -> Path:
    """Create a sample Excel file for testing."""
    import pandas as pd
    
    excel_path = temp_dir / "test_data.xlsx"
    data = {
        'SampleID': ['STD-001', 'BLK-001', 'DUP-001-OR', 'DUP-001-CK'],
        'Type': ['STD', 'BLK', 'UNK', 'UNK'],
        'Result': [10.5, 0.01, 15.2, 15.8],
        'Element': ['Au', 'Au', 'Au', 'Au']
    }
    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)
    return excel_path


@pytest.fixture
def invalid_file(temp_dir: Path) -> Path:
    """Create an invalid file for testing error handling."""
    invalid_path = temp_dir / "invalid.txt"
    invalid_path.write_text("This is not a valid CSV or Excel file")
    return invalid_path
