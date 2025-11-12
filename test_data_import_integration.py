#!/usr/bin/env python3
"""
Test script for data import integration in GUI.

Tests that the DataImporter is properly integrated and can load test data.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data.importer import DataImporter

def test_data_import():
    """Test data import with mock data files."""
    print("Testing Data Import Integration")
    print("=" * 50)

    importer = DataImporter()

    # Test with gui_test_data.csv
    test_file = Path("mock_data/gui_test_data.csv")

    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False

    try:
        print(f"\n📁 Loading: {test_file}")
        df = importer.read_table(test_file)

        print(f"✅ File loaded successfully!")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Column names: {list(df.columns)}")

        # Test column mapping suggestions
        print(f"\n🔍 Testing column mapping suggestions...")
        suggestions = importer.suggest_mapping(df.columns.tolist())

        print("   Suggested mappings:")
        for canonical, (header, confidence) in suggestions.items():
            if header:
                print(f"     {canonical} → {header} (confidence: {confidence:.2f})")

        # Test data preview
        print(f"\n📊 Data preview (first 5 rows):")
        print(df.head().to_string())

        print(f"\n✅ All tests passed!")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_data_import()
    sys.exit(0 if success else 1)
