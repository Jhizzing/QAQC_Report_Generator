"""
Integration tests for CRM manager with standards analyzer.
"""
import pytest
from src.data.crm_manager import CRMManager
from src.analysis import StandardsAnalyzer


class TestCRMIntegration:
    """Test CRM integration with standards analysis."""

    def test_crm_standards_analysis(self):
        """Test standards analysis using CRM data."""
        # Initialize components
        crm_manager = CRMManager()
        standards_analyzer = StandardsAnalyzer()

        # Get CRM data
        crm_name = 'NIST SRM 2709a'
        crm_info = crm_manager.get_crm_info(crm_name)

        assert crm_info is not None
        assert crm_info['name'] == 'NIST SRM 2709a'
        assert crm_info['certified_value'] == 0.85
        assert crm_info['uncertainty'] == 0.05

        # Simulate measured values (slightly different from certified)
        measured_values = [0.82, 0.87, 0.84, 0.86, 0.83]

        # Prepare data for analysis
        analysis_data = {
            'measured': measured_values,
            'certified': crm_info['certified_value'],
            'uncertainty': crm_info['uncertainty']
        }

        # Run analysis
        results = standards_analyzer.analyze_standards(analysis_data)

        # Verify results
        assert 'overall_acceptable' in results
        assert 'bias' in results
        assert 'recovery' in results
        assert 'precision' in results

        # Check that analysis used CRM data correctly
        assert results['summary']['certified_value'] == 0.85
        assert results['summary']['uncertainty'] == 0.05

        # Verify Z-scores are calculated correctly
        z_scores = results['bias']['z_scores']
        assert len(z_scores) == len(measured_values)

        # Verify recovery calculations
        recoveries = results['recovery']['recoveries']
        assert len(recoveries) == len(measured_values)
        assert all(0 < r < 200 for r in recoveries)  # Reasonable recovery range

    def test_crm_validation(self):
        """Test CRM validation for different sample types."""
        crm_manager = CRMManager()

        # Test low-grade sample with appropriate CRM
        is_valid, message = crm_manager.validate_crm_selection('NIST SRM 2709a', 0.8)
        assert is_valid
        assert 'valid for analysis' in message

        # Test high-grade sample with appropriate CRM
        is_valid, message = crm_manager.validate_crm_selection('NIST SRM 2705', 30.0)
        assert is_valid
        assert 'valid for analysis' in message

        # Test mismatched concentration
        is_valid, message = crm_manager.validate_crm_selection('NIST SRM 2709a', 20.0)
        assert not is_valid
        assert 'not suitable' in message

    def test_crm_search_by_concentration(self):
        """Test finding appropriate CRMs for different concentration ranges."""
        crm_manager = CRMManager()

        # Test low concentration range
        low_crms = crm_manager.get_crms_by_concentration_range(0.1, 1.0)
        assert len(low_crms) > 0
        assert all(0.1 <= crm.get('certified_value', 0) <= 1.0 for crm in low_crms)

        # Test medium concentration range
        medium_crms = crm_manager.get_crms_by_concentration_range(1.0, 10.0)
        assert len(medium_crms) > 0
        assert all(1.0 <= crm.get('certified_value', 0) <= 10.0 for crm in medium_crms)

        # Test high concentration range
        high_crms = crm_manager.get_crms_by_concentration_range(10.0, 50.0)
        assert len(high_crms) > 0
        assert all(10.0 <= crm.get('certified_value', 0) <= 50.0 for crm in high_crms)

    def test_crm_matrix_matching(self):
        """Test finding CRMs by matrix type."""
        crm_manager = CRMManager()

        # Test soil matrix CRMs
        soil_crms = crm_manager.get_crms_by_matrix('soil')
        assert len(soil_crms) > 0
        assert all('soil' in crm.get('matrix', '').lower() for crm in soil_crms)

        # Test sediment matrix CRMs
        sediment_crms = crm_manager.get_crms_by_matrix('sediment')
        assert len(sediment_crms) > 0
        assert all('sediment' in crm.get('matrix', '').lower() for crm in sediment_crms)

        # Test ore matrix CRMs
        ore_crms = crm_manager.get_crms_by_matrix('ore')
        assert len(ore_crms) > 0
        assert all('ore' in crm.get('matrix', '').lower() for crm in ore_crms)

    def test_crm_supplier_analysis(self):
        """Test analyzing CRMs by supplier."""
        crm_manager = CRMManager()

        # Test NIST CRMs
        nist_crms = crm_manager.get_crms_by_supplier('NIST')
        assert len(nist_crms) > 0
        assert all('NIST' in crm.get('supplier', '') for crm in nist_crms)

        # Test CANMET CRMs
        canmet_crms = crm_manager.get_crms_by_supplier('CANMET')
        assert len(canmet_crms) > 0
        assert all('CANMET' in crm.get('supplier', '') for crm in canmet_crms)

        # Test CDN CRMs
        cdn_crms = crm_manager.get_crms_by_supplier('CDN')
        assert len(cdn_crms) > 0
        assert all('CDN' in crm.get('supplier', '') for crm in cdn_crms)

    def test_crm_expiry_checking(self):
        """Test CRM expiry date checking."""
        crm_manager = CRMManager()

        # Test valid CRM
        is_expired, message = crm_manager.check_crm_expiry('NIST SRM 2709a')
        assert not is_expired
        assert 'valid until' in message or 'days remaining' in message

        # Test CRM with no expiry date
        # (This would need a CRM without expiry date in the database)
        # For now, just test the method works
        assert isinstance(is_expired, bool)
        assert isinstance(message, str)

    def test_crm_analysis_thresholds(self):
        """Test getting analysis thresholds from CRM database."""
        crm_manager = CRMManager()
        thresholds = crm_manager.get_analysis_thresholds()

        # Verify threshold structure
        assert 'z_score_threshold' in thresholds
        assert 'recovery_limits' in thresholds
        assert 'precision_threshold' in thresholds
        assert 'contamination_threshold' in thresholds
        assert 'carryover_threshold' in thresholds
        assert 'blank_limit' in thresholds
        assert 'rpd_threshold' in thresholds
        assert 'nugget_threshold' in thresholds

        # Verify threshold values are reasonable
        assert thresholds['z_score_threshold'] == 2.0
        assert thresholds['recovery_limits']['min'] == 90.0
        assert thresholds['recovery_limits']['max'] == 110.0
        assert thresholds['precision_threshold'] == 5.0

    def test_crm_methods(self):
        """Test getting analysis methods from CRM database."""
        crm_manager = CRMManager()
        methods = crm_manager.get_methods()

        # Verify method structure
        assert 'fire_assay' in methods
        assert 'icp_ms' in methods
        assert 'icp_aes' in methods

        # Verify fire assay method
        fire_assay = methods['fire_assay']
        assert 'name' in fire_assay
        assert 'detection_limit' in fire_assay
        assert 'working_range' in fire_assay
        assert 'notes' in fire_assay

        # Verify ICP-MS method
        icp_ms = methods['icp_ms']
        assert 'name' in icp_ms
        assert 'detection_limit' in icp_ms
        assert 'working_range' in icp_ms
        assert 'notes' in icp_ms

    def test_crm_summary_statistics(self):
        """Test getting CRM database summary."""
        crm_manager = CRMManager()
        summary = crm_manager.get_crm_summary()

        # Verify summary structure
        assert 'total_crms' in summary
        assert 'suppliers' in summary
        assert 'matrices' in summary
        assert 'concentration_range' in summary

        # Verify summary values
        assert summary['total_crms'] > 0
        assert len(summary['suppliers']) > 0
        assert len(summary['matrices']) > 0
        assert summary['concentration_range']['min'] >= 0
        assert summary['concentration_range']['max'] > 0

        # Verify supplier distribution
        assert 'NIST' in summary['suppliers']
        assert 'CANMET' in summary['suppliers']
        assert 'CDN Resource Laboratories' in summary['suppliers']

        # Verify matrix distribution
        assert 'Montana Soil' in summary['matrices'] or 'soil' in str(summary['matrices'])
        assert 'Freshwater Sediment' in summary['matrices'] or 'sediment' in str(summary['matrices'])
        assert 'Gold Ore' in summary['matrices'] or 'ore' in str(summary['matrices'])
