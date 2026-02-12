import sys
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.project_manager import ProjectManager


def test_project_persistence(tmp_path):
    # Setup test data
    project_file = tmp_path / "test_project.qaqc"

    # Create dummy data
    df = pd.DataFrame(
        {
            "sample_id": ["S1", "S2", "S3"],
            "result": [1.1, 2.2, 3.3],
            "sample_type": ["Standard", "Blank", "Duplicate"],
        }
    )

    state = {
        "config": {"test_setting": True, "column_mapping": {"id": "sample_id"}},
        "results": {"standards": {"status": "PASS"}},
        "data": {"dataframe": df, "file_name": "test_data.csv"},
    }

    # Test Save
    pm = ProjectManager()
    pm.save_project(state, str(project_file))

    assert project_file.exists(), "Project file was not created"

    # Test Load
    loaded_state = pm.load_project(str(project_file))

    # Verify Data
    # Check config
    assert loaded_state["config"] == state["config"]

    # Check results
    assert loaded_state["results"] == state["results"]

    # Check dataframe
    loaded_df = loaded_state["data"]["dataframe"]
    pd.testing.assert_frame_equal(loaded_df, df)
