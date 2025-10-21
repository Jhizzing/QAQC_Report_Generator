#!/usr/bin/env python3
"""
Demonstration script for CRM (Certified Reference Material) usage in QAQC analysis.

This script shows how to:
1. Load and query CRM database
2. Validate CRM selection for samples
3. Use CRM data in standards analysis
4. Generate reports with CRM information
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data.crm_manager import CRMManager
from analysis import StandardsAnalyzer
from reporting import ExcelReporter


def main():
    """Demonstrate CRM usage in QAQC analysis."""
    print("=" * 60)
    print("CRM (Certified Reference Material) Usage Demonstration")
    print("=" * 60)

    # Initialize CRM manager
    print("\n1. Loading CRM Database...")
    crm_manager = CRMManager()

    # Show database summary
    summary = crm_manager.get_crm_summary()
    print(f"   Total CRMs: {summary['total_crms']}")
    print(f"   Suppliers: {list(summary['suppliers'].keys())}")
    print(f"   Matrices: {list(summary['matrices'].keys())}")
    print(f"   Concentration Range: {summary['concentration_range']['min']:.2f} - {summary['concentration_range']['max']:.2f} g/t")

    # Demonstrate CRM search by concentration
    print("\n2. Finding CRMs for Different Sample Types...")

    # Low-grade samples (0.1 - 1.0 g/t)
    low_crms = crm_manager.get_crms_by_concentration_range(0.1, 1.0)
    print(f"   Low-grade samples (0.1-1.0 g/t): {len(low_crms)} CRMs available")
    for crm in low_crms[:3]:  # Show first 3
        print(f"     - {crm['name']}: {crm['certified_value']} ± {crm['uncertainty']} g/t")

    # High-grade samples (10.0 - 50.0 g/t)
    high_crms = crm_manager.get_crms_by_concentration_range(10.0, 50.0)
    print(f"   High-grade samples (10.0-50.0 g/t): {len(high_crms)} CRMs available")
    for crm in high_crms[:3]:  # Show first 3
        print(f"     - {crm['name']}: {crm['certified_value']} ± {crm['uncertainty']} g/t")

    # Demonstrate CRM validation
    print("\n3. Validating CRM Selection...")

    # Test with appropriate CRM
    crm_name = 'NIST SRM 2709a'
    sample_conc = 0.8
    is_valid, message = crm_manager.validate_crm_selection(crm_name, sample_conc)
    print(f"   Sample: {sample_conc} g/t")
    print(f"   CRM: {crm_name}")
    print(f"   Valid: {is_valid}")
    print(f"   Message: {message}")

    # Test with mismatched CRM
    crm_name = 'NIST SRM 2709a'
    sample_conc = 20.0
    is_valid, message = crm_manager.validate_crm_selection(crm_name, sample_conc)
    print(f"\n   Sample: {sample_conc} g/t")
    print(f"   CRM: {crm_name}")
    print(f"   Valid: {is_valid}")
    print(f"   Message: {message}")

    # Demonstrate standards analysis with CRM data
    print("\n4. Standards Analysis with CRM Data...")

    # Get CRM information
    crm_info = crm_manager.get_crm_info('NIST SRM 2709a')
    print(f"   Using CRM: {crm_info['name']}")
    print(f"   Certified Value: {crm_info['certified_value']} g/t")
    print(f"   Uncertainty: ±{crm_info['uncertainty']} g/t")
    print(f"   Matrix: {crm_info['matrix']}")
    print(f"   Supplier: {crm_info['supplier']}")

    # Simulate measured values (slightly different from certified)
    measured_values = [0.82, 0.87, 0.84, 0.86, 0.83, 0.85, 0.88, 0.81]
    print(f"   Measured Values: {measured_values} g/t")

    # Run standards analysis
    standards_analyzer = StandardsAnalyzer()
    analysis_data = {
        'measured': measured_values,
        'certified': crm_info['certified_value'],
        'uncertainty': crm_info['uncertainty']
    }

    results = standards_analyzer.analyze_standards(analysis_data)

    # Display results
    print(f"\n   Analysis Results:")
    print(f"     Overall Acceptable: {results['overall_acceptable']}")
    print(f"     Bias Detected: {results['bias']['bias_detected']}")
    print(f"     Max Z-Score: {results['bias']['max_z_score']:.3f}")
    print(f"     Mean Recovery: {results['recovery']['mean_recovery']:.1f}%")
    print(f"     Precision (RSD): {results['precision']['rsd']:.1f}%")

    # Demonstrate CRM expiry checking
    print("\n5. Checking CRM Expiry Dates...")

    # Check a few CRMs
    test_crms = ['NIST SRM 2709a', 'NIST SRM 2710a', 'CANMET OREAS 101']
    for crm_name in test_crms:
        is_expired, message = crm_manager.check_crm_expiry(crm_name)
        print(f"   {crm_name}: {message}")

    # Demonstrate analysis thresholds
    print("\n6. Analysis Thresholds from CRM Database...")
    thresholds = crm_manager.get_analysis_thresholds()
    print(f"   Z-Score Threshold: {thresholds['z_score_threshold']}")
    print(f"   Recovery Limits: {thresholds['recovery_limits']['min']}-{thresholds['recovery_limits']['max']}%")
    print(f"   Precision Threshold: {thresholds['precision_threshold']}% RSD")
    print(f"   RPD Threshold: {thresholds['rpd_threshold']}%")

    # Demonstrate analysis methods
    print("\n7. Available Analysis Methods...")
    methods = crm_manager.get_methods()
    for method_name, method_info in methods.items():
        print(f"   {method_name.upper()}:")
        print(f"     Name: {method_info['name']}")
        print(f"     Detection Limit: {method_info['detection_limit']} g/t")
        print(f"     Working Range: {method_info['working_range']}")
        print(f"     Notes: {method_info['notes']}")
        print()

    print("=" * 60)
    print("CRM Demonstration Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
