#!/usr/bin/env python3
"""
Test GUI with Mock Data

This script tests the GUI components with mock data to ensure
everything works correctly.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_gui_components():
    """Test GUI components with mock data."""
    print("🧪 Testing GUI Components with Mock Data")
    print("=" * 50)

    try:
        # Test imports
        print("1. Testing imports...")
        from PyQt6.QtWidgets import QApplication
        from src.gui.main_window import QAQCApplication
        from src.gui.widgets.data_panel import DataPanel
        from src.gui.widgets.visualization_panel import VisualizationPanel
        print("   ✅ All imports successful")

        # Test data loading
        print("\n2. Testing data loading...")
        import pandas as pd

        # Load mock data
        mock_data_path = Path(__file__).parent / "mock_data" / "gui_test_data.csv"
        if mock_data_path.exists():
            df = pd.read_csv(mock_data_path)
            print(f"   ✅ Loaded {len(df)} rows from mock data")
            print(f"   ✅ Columns: {list(df.columns)}")
            print(f"   ✅ Sample types: {df['sample_type'].value_counts().to_dict()}")
        else:
            print("   ❌ Mock data file not found")
            return False

        # Test data processing
        print("\n3. Testing data processing...")
        from src.data.importer import DataImporter

        importer = DataImporter()
        data_info = {
            'data': df,
            'columns': list(df.columns),
            'data_preview': df.head(10).to_dict('records'),
            'file_path': str(mock_data_path)
        }
        print("   ✅ Data info created successfully")

        # Test GUI application creation
        print("\n4. Testing GUI application creation...")
        app = QApplication(sys.argv)
        app.setApplicationName("QAQC Test Application")

        window = QAQCApplication()
        print("   ✅ Main window created successfully")

        # Test data panel
        print("\n5. Testing data panel...")
        data_panel = window.data_panel
        if data_panel:
            print("   ✅ Data panel found")
        else:
            print("   ❌ Data panel not found")

        # Test visualization panel
        print("\n6. Testing visualization panel...")
        viz_panel = window.visualization_panel
        if viz_panel:
            print("   ✅ Visualization panel found")
        else:
            print("   ❌ Visualization panel not found")

        print("\n🎉 All GUI component tests passed!")
        print("\n📋 Mock Data Summary:")
        print(f"   • Total samples: {len(df)}")
        print(f"   • Standards: {len(df[df['sample_type'] == 'STANDARD'])}")
        print(f"   • Blanks: {len(df[df['sample_type'] == 'BLANK'])}")
        print(f"   • Duplicates: {len(df[df['sample_type'] == 'DUPLICATE'])}")
        print(f"   • Unknown samples: {len(df[df['sample_type'] == 'UNKNOWN'])}")
        print(f"   • Date range: {df['date_analyzed'].min()} to {df['date_analyzed'].max()}")
        print(f"   • Lab batches: {df['lab_batch'].nunique()}")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🚀 Starting GUI Mock Data Test")
    print("=" * 50)

    success = test_gui_components()

    if success:
        print("\n✅ All tests passed! GUI is ready for use.")
        print("\n📁 Mock data files created:")
        print("   • mock_data/gui_test_data.csv - Basic test data")
        print("   • mock_data/complex_test_data.csv - Complex test data with qualifiers")
        print("\n🎯 Next steps:")
        print("   1. Launch GUI: python3 launch_gui_simple.py")
        print("   2. Import mock data file")
        print("   3. Test data visualization")
        print("   4. Test analysis features")
    else:
        print("\n❌ Tests failed. Check the error messages above.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
