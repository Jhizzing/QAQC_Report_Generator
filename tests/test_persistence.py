import sys
import os
import pandas as pd
from pathlib import Path
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.project_manager import ProjectManager

def test_project_persistence():
    print("Testing Project Persistence...")
    
    # Setup test data
    test_dir = Path("test_output")
    test_dir.mkdir(exist_ok=True)
    project_file = test_dir / "test_project.qaqc"
    
    # Create dummy data
    df = pd.DataFrame({
        'sample_id': ['S1', 'S2', 'S3'],
        'result': [1.1, 2.2, 3.3],
        'sample_type': ['Standard', 'Blank', 'Duplicate']
    })
    
    state = {
        "config": {"test_setting": True, "column_mapping": {"id": "sample_id"}},
        "results": {"standards": {"status": "PASS"}},
        "data": {
            "dataframe": df,
            "file_name": "test_data.csv"
        }
    }
    
    # Test Save
    print(f"Saving project to {project_file}...")
    pm = ProjectManager()
    pm.save_project(state, str(project_file))
    
    if not project_file.exists():
        print("FAIL: Project file not created")
        return False
        
    # Test Load
    print("Loading project...")
    loaded_state = pm.load_project(str(project_file))
    
    # Verify Data
    print("Verifying loaded state...")
    
    # Check config
    if loaded_state["config"] != state["config"]:
        print(f"FAIL: Config mismatch. Expected {state['config']}, got {loaded_state['config']}")
        return False
        
    # Check results
    if loaded_state["results"] != state["results"]:
        print(f"FAIL: Results mismatch. Expected {state['results']}, got {loaded_state['results']}")
        return False
        
    # Check dataframe
    loaded_df = loaded_state["data"]["dataframe"]
    pd.testing.assert_frame_equal(loaded_df, df)
    
    print("SUCCESS: Project persistence verified!")
    
    # Cleanup
    shutil.rmtree(test_dir)
    return True

if __name__ == "__main__":
    try:
        success = test_project_persistence()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
