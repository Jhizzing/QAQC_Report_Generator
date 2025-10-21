#!/usr/bin/env python3
"""
Create comprehensive mock data for QAQC analysis testing.

This script generates realistic gold assay data including:
- Standards with various concentrations
- Blanks with contamination scenarios
- Duplicates with precision issues
- Regular samples with qualifiers
- Realistic CRM scenarios
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

def create_realistic_assay_data():
    """Create realistic gold assay data for comprehensive testing."""

    # Set random seed for reproducible results
    np.random.seed(42)
    random.seed(42)

    # Base data structure
    data = {
        'sample_id': [],
        'sample_type': [],
        'result': [],
        'qualifier': [],
        'detection_limit': [],
        'lab_batch': [],
        'analysis_date': [],
        'analyst': [],
        'method': []
    }

    # Generate standards (5 samples around NIST SRM 2709a - 0.85 g/t)
    standards_results = np.random.normal(0.85, 0.05, 5)  # Mean 0.85, std 0.05
    for i in range(5):
        data['sample_id'].append(f'STD-{i+1:03d}')
        data['sample_type'].append('STANDARD')
        data['result'].append(round(standards_results[i], 3))
        data['qualifier'].append('')
        data['detection_limit'].append(0.01)
        data['lab_batch'].append('BATCH-001')
        data['analysis_date'].append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst A')
        data['method'].append('Fire Assay')

    # Generate blanks (4 samples - some with contamination)
    blank_results = [0.01, 0.02, 0.15, 0.02]  # One contaminated blank
    for i, result in enumerate(blank_results):
        data['sample_id'].append(f'BLK-{i+1:03d}')
        data['sample_type'].append('BLANK')
        data['result'].append(result)
        data['qualifier'].append('' if result < 0.1 else '<DL')
        data['detection_limit'].append(0.01)
        data['lab_batch'].append('BATCH-001')
        data['analysis_date'].append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst A')
        data['method'].append('Fire Assay')

    # Generate duplicates (3 pairs with varying precision)
    duplicate_pairs = [
        (1.25, 1.28),  # Good precision
        (2.15, 2.35),  # Poor precision
        (0.95, 0.97)   # Good precision
    ]

    for i, (val1, val2) in enumerate(duplicate_pairs):
        for j, result in enumerate([val1, val2]):
            data['sample_id'].append(f'DUP-{i+1:03d}')
            data['sample_type'].append('DUPLICATE')
            data['result'].append(result)
            data['qualifier'].append('')
            data['detection_limit'].append(0.01)
            data['lab_batch'].append('BATCH-001')
            data['analysis_date'].append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
            data['analyst'].append('Analyst A')
            data['method'].append('Fire Assay')

    # Generate regular samples with various concentrations and qualifiers
    sample_results = [
        (1.5, ''),      # Normal result
        (0.005, '<DL'), # Below detection limit
        (2.1, ''),      # Normal result
        (0.008, '<DL'), # Below detection limit
        (3.2, ''),      # Normal result
        (1.8, ''),      # Normal result
        (0.012, ''),    # Low but detectable
        (4.5, ''),      # High result
        (0.009, '<DL'), # Below detection limit
        (2.8, '')       # Normal result
    ]

    for i, (result, qualifier) in enumerate(sample_results):
        data['sample_id'].append(f'SMP-{i+1:03d}')
        data['sample_type'].append('SAMPLE')
        data['result'].append(result)
        data['qualifier'].append(qualifier)
        data['detection_limit'].append(0.01)
        data['lab_batch'].append('BATCH-001')
        data['analysis_date'].append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst A')
        data['method'].append('Fire Assay')

    # Generate additional standards for different CRM testing
    # High-grade standards (around NIST SRM 2705 - 32.5 g/t)
    high_standards = np.random.normal(32.5, 1.5, 3)
    for i, result in enumerate(high_standards):
        data['sample_id'].append(f'HSTD-{i+1:03d}')
        data['sample_type'].append('STANDARD')
        data['result'].append(round(result, 2))
        data['qualifier'].append('')
        data['detection_limit'].append(0.1)
        data['lab_batch'].append('BATCH-002')
        data['analysis_date'].append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst B')
        data['method'].append('Fire Assay')

    # Generate more blanks for better statistics
    additional_blanks = np.random.normal(0.02, 0.005, 3)
    for i, result in enumerate(additional_blanks):
        data['sample_id'].append(f'BLK-{i+5:03d}')
        data['sample_type'].append('BLANK')
        data['result'].append(round(result, 3))
        data['qualifier'].append('')
        data['detection_limit'].append(0.01)
        data['lab_batch'].append('BATCH-002')
        data['analysis_date'].append((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst B')
        data['method'].append('Fire Assay')

    return pd.DataFrame(data)

def create_low_grade_data():
    """Create low-grade gold assay data for testing different CRM scenarios."""

    np.random.seed(123)
    random.seed(123)

    data = {
        'sample_id': [],
        'sample_type': [],
        'result': [],
        'qualifier': [],
        'detection_limit': [],
        'lab_batch': [],
        'analysis_date': [],
        'analyst': [],
        'method': []
    }

    # Low-grade standards (around CANMET OREAS 101 - 0.12 g/t)
    low_standards = np.random.normal(0.12, 0.02, 4)
    for i, result in enumerate(low_standards):
        data['sample_id'].append(f'LSTD-{i+1:03d}')
        data['sample_type'].append('STANDARD')
        data['result'].append(round(result, 3))
        data['qualifier'].append('')
        data['detection_limit'].append(0.005)
        data['lab_batch'].append('BATCH-003')
        data['analysis_date'].append((datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst C')
        data['method'].append('ICP-MS')

    # Low-grade blanks
    low_blanks = [0.001, 0.002, 0.0015, 0.0018]
    for i, result in enumerate(low_blanks):
        data['sample_id'].append(f'LBLK-{i+1:03d}')
        data['sample_type'].append('BLANK')
        data['result'].append(result)
        data['qualifier'].append('')
        data['detection_limit'].append(0.005)
        data['lab_batch'].append('BATCH-003')
        data['analysis_date'].append((datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst C')
        data['method'].append('ICP-MS')

    # Low-grade samples
    low_samples = [0.08, 0.15, 0.22, 0.18, 0.12, 0.25, 0.09, 0.31]
    for i, result in enumerate(low_samples):
        data['sample_id'].append(f'LSMP-{i+1:03d}')
        data['sample_type'].append('SAMPLE')
        data['result'].append(result)
        data['qualifier'].append('')
        data['detection_limit'].append(0.005)
        data['lab_batch'].append('BATCH-003')
        data['analysis_date'].append((datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst C')
        data['method'].append('ICP-MS')

    return pd.DataFrame(data)

def create_problematic_data():
    """Create data with various QAQC issues for testing error detection."""

    np.random.seed(456)
    random.seed(456)

    data = {
        'sample_id': [],
        'sample_type': [],
        'result': [],
        'qualifier': [],
        'detection_limit': [],
        'lab_batch': [],
        'analysis_date': [],
        'analyst': [],
        'method': []
    }

    # Standards with bias (systematically high)
    biased_standards = np.random.normal(0.95, 0.05, 4)  # Should be 0.85
    for i, result in enumerate(biased_standards):
        data['sample_id'].append(f'BSTD-{i+1:03d}')
        data['sample_type'].append('STANDARD')
        data['result'].append(round(result, 3))
        data['qualifier'].append('')
        data['detection_limit'].append(0.01)
        data['lab_batch'].append('BATCH-004')
        data['analysis_date'].append((datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst D')
        data['method'].append('Fire Assay')

    # Contaminated blanks
    contaminated_blanks = [0.05, 0.08, 0.12, 0.15]  # All contaminated
    for i, result in enumerate(contaminated_blanks):
        data['sample_id'].append(f'CBLK-{i+1:03d}')
        data['sample_type'].append('BLANK')
        data['result'].append(result)
        data['qualifier'].append('')
        data['detection_limit'].append(0.01)
        data['lab_batch'].append('BATCH-004')
        data['analysis_date'].append((datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'))
        data['analyst'].append('Analyst D')
        data['method'].append('Fire Assay')

    # Poor precision duplicates
    poor_duplicates = [(1.0, 1.5), (2.0, 3.0), (0.5, 1.2)]  # High RPD
    for i, (val1, val2) in enumerate(poor_duplicates):
        for j, result in enumerate([val1, val2]):
            data['sample_id'].append(f'PDUP-{i+1:03d}')
            data['sample_type'].append('DUPLICATE')
            data['result'].append(result)
            data['qualifier'].append('')
            data['detection_limit'].append(0.01)
            data['lab_batch'].append('BATCH-004')
            data['analysis_date'].append((datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'))
            data['analyst'].append('Analyst D')
            data['method'].append('Fire Assay')

    return pd.DataFrame(data)

def main():
    """Create and save mock datasets."""
    print("Creating comprehensive mock data for QAQC testing...")

    # Create output directory
    output_dir = Path("mock_data")
    output_dir.mkdir(exist_ok=True)

    # Generate datasets
    print("  Creating realistic assay data...")
    realistic_data = create_realistic_assay_data()
    realistic_data.to_csv(output_dir / "realistic_assays.csv", index=False)
    print(f"    Saved: {len(realistic_data)} samples")

    print("  Creating low-grade data...")
    low_grade_data = create_low_grade_data()
    low_grade_data.to_csv(output_dir / "low_grade_assays.csv", index=False)
    print(f"    Saved: {len(low_grade_data)} samples")

    print("  Creating problematic data...")
    problematic_data = create_problematic_data()
    problematic_data.to_csv(output_dir / "problematic_assays.csv", index=False)
    print(f"    Saved: {len(problematic_data)} samples")

    # Create combined dataset
    print("  Creating combined dataset...")
    combined_data = pd.concat([realistic_data, low_grade_data, problematic_data], ignore_index=True)
    combined_data.to_csv(output_dir / "combined_assays.csv", index=False)
    print(f"    Saved: {len(combined_data)} total samples")

    # Create data summary
    summary = {
        'dataset': ['realistic_assays.csv', 'low_grade_assays.csv', 'problematic_assays.csv', 'combined_assays.csv'],
        'samples': [len(realistic_data), len(low_grade_data), len(problematic_data), len(combined_data)],
        'description': [
            'Realistic gold assay data with good QAQC',
            'Low-grade samples for ICP-MS testing',
            'Data with various QAQC issues',
            'Combined dataset for comprehensive testing'
        ]
    }

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(output_dir / "data_summary.csv", index=False)

    print(f"\nMock data creation complete!")
    print(f"Files saved to: {output_dir}")
    print(f"Data summary:")
    print(summary_df.to_string(index=False))

    return output_dir

if __name__ == "__main__":
    main()
