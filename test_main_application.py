#!/usr/bin/env python3
"""
Test script for the main QAQC application.

This script demonstrates the full capabilities of the integrated application
including data import, analysis, CRM integration, and reporting.
"""

import os
import sys
import tempfile
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def create_test_data():
    """Create comprehensive test data for QAQC analysis."""
    # Create test data with standards, blanks, and duplicates
    data = {
        'sample_id': [
            'S001', 'S002', 'S003', 'S004', 'S005',  # Standards
            'B001', 'B002', 'B003', 'B004',           # Blanks
            'D001', 'D001', 'D002', 'D002', 'D003', 'D003',  # Duplicates
            'R001', 'R002', 'R003', 'R004', 'R005'    # Regular samples
        ],
        'sample_type': [
            'STANDARD', 'STANDARD', 'STANDARD', 'STANDARD', 'STANDARD',
            'BLANK', 'BLANK', 'BLANK', 'BLANK',
            'DUPLICATE', 'DUPLICATE', 'DUPLICATE', 'DUPLICATE', 'DUPLICATE', 'DUPLICATE',
            'SAMPLE', 'SAMPLE', 'SAMPLE', 'SAMPLE', 'SAMPLE'
        ],
        'result': [
            # Standards (around 0.85 g/t - matches NIST SRM 2709a)
            0.82, 0.87, 0.84, 0.86, 0.83,
            # Blanks (low values)
            0.01, 0.02, 0.015, 0.018,
            # Duplicates (pairs with slight differences)
            1.25, 1.28, 2.15, 2.18, 0.95, 0.97,
            # Regular samples
            1.5, 2.1, 0.8, 3.2, 1.8
        ],
        'qualifier': [
            '', '', '', '', '',  # Standards
            '', '', '', '',      # Blanks
            '', '', '', '', '', '',  # Duplicates
            '', '', '', '', ''   # Regular samples
        ],
        'detection_limit': [
            0.01, 0.01, 0.01, 0.01, 0.01,  # Standards
            0.01, 0.01, 0.01, 0.01,         # Blanks
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01,  # Duplicates
            0.01, 0.01, 0.01, 0.01, 0.01   # Regular samples
        ]
    }

    return pd.DataFrame(data)


def test_basic_analysis():
    """Test basic QAQC analysis with auto-mapping and CRM selection."""
    print("=" * 60)
    print("Testing Basic QAQC Analysis")
    print("=" * 60)

    # Create test data
    test_data = create_test_data()

    # Create temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "test_assays.csv"
        output_dir = Path(temp_dir) / "output"

        # Save test data
        test_data.to_csv(input_file, index=False)

        # Run analysis
        cmd = f"""python main.py --input {input_file} --output {output_dir} --infer-mapping --normalize-results --yes --auto-crm --include-plots --verbose"""

        print(f"Running: {cmd}")
        result = os.system(cmd)

        if result == 0:
            print("✅ Basic analysis completed successfully!")

            # Check output files
            output_files = list(output_dir.glob("*"))
            print(f"Generated {len(output_files)} output files:")
            for file in output_files:
                print(f"  - {file.name}")
        else:
            print("❌ Basic analysis failed!")
            return False

    return True


def test_specific_crm():
    """Test analysis with specific CRM selection."""
    print("\n" + "=" * 60)
    print("Testing Specific CRM Selection")
    print("=" * 60)

    # Create test data
    test_data = create_test_data()

    # Create temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "test_assays.csv"
        output_dir = Path(temp_dir) / "output"

        # Save test data
        test_data.to_csv(input_file, index=False)

        # Run analysis with specific CRM
        cmd = f"""python main.py --input {input_file} --output {output_dir} --infer-mapping --normalize-results --yes --crm-name "NIST SRM 2709a" --include-plots --output-format both --verbose"""

        print(f"Running: {cmd}")
        result = os.system(cmd)

        if result == 0:
            print("✅ Specific CRM analysis completed successfully!")

            # Check output files
            output_files = list(output_dir.glob("*"))
            print(f"Generated {len(output_files)} output files:")
            for file in output_files:
                print(f"  - {file.name}")
        else:
            print("❌ Specific CRM analysis failed!")
            return False

    return True


def test_skip_analyses():
    """Test analysis with some analyses skipped."""
    print("\n" + "=" * 60)
    print("Testing Skip Analyses")
    print("=" * 60)

    # Create test data
    test_data = create_test_data()

    # Create temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "test_assays.csv"
        output_dir = Path(temp_dir) / "output"

        # Save test data
        test_data.to_csv(input_file, index=False)

        # Run analysis skipping standards and duplicates
        cmd = f"""python main.py --input {input_file} --output {output_dir} --infer-mapping --normalize-results --yes --skip-standards --skip-duplicates --output-format excel --verbose"""

        print(f"Running: {cmd}")
        result = os.system(cmd)

        if result == 0:
            print("✅ Skip analyses completed successfully!")

            # Check output files
            output_files = list(output_dir.glob("*"))
            print(f"Generated {len(output_files)} output files:")
            for file in output_files:
                print(f"  - {file.name}")
        else:
            print("❌ Skip analyses failed!")
            return False

    return True


def test_dry_run():
    """Test dry run mode."""
    print("\n" + "=" * 60)
    print("Testing Dry Run Mode")
    print("=" * 60)

    # Create test data
    test_data = create_test_data()

    # Create temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = Path(temp_dir) / "test_assays.csv"
        output_dir = Path(temp_dir) / "output"

        # Save test data
        test_data.to_csv(input_file, index=False)

        # Run dry run
        cmd = f"""python main.py --input {input_file} --output {output_dir} --infer-mapping --normalize-results --yes --auto-crm --dry-run --verbose"""

        print(f"Running: {cmd}")
        result = os.system(cmd)

        if result == 0:
            print("✅ Dry run completed successfully!")
        else:
            print("❌ Dry run failed!")
            return False

    return True


def main():
    """Run all tests."""
    print("QAQC Application Integration Tests")
    print("=" * 60)

    tests = [
        test_basic_analysis,
        test_specific_crm,
        test_skip_analyses,
        test_dry_run
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")

    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("🎉 All tests passed! The main application is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
