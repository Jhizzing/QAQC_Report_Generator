"""
Tests for CRM manager functionality.
"""
import pytest
import tempfile
import os
import yaml
from src.data.crm_manager import CRMManager


class TestCRMManager:
    """Test CRMManager functionality."""

    def test_init_default_path(self):
        """Test initialization with default path."""
        manager = CRMManager()
        assert manager.database_path is not None
        assert os.path.exists(manager.database_path)

    def test_init_custom_path(self):
        """Test initialization with custom path."""
        # Create temporary YAML file
        test_data = {
            'database_info': {'version': '1.0'},
            'crms': [
                {
                    'name': 'Test CRM',
                    'certified_value': 1.0,
                    'uncertainty': 0.1,
                    'units': 'g/t',
                    'matrix': 'Test Matrix',
                    'expiry_date': '2025-12-31',
                    'supplier': 'Test Supplier'
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            temp_path = f.name

        try:
            manager = CRMManager(temp_path)
            assert manager.database_path == temp_path
            assert manager.database['database_info']['version'] == '1.0'
        finally:
            os.unlink(temp_path)

    def test_load_database_file_not_found(self):
        """Test loading database when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            CRMManager('/nonexistent/path.yaml')

    def test_get_all_crms(self):
        """Test getting all CRMs."""
        manager = CRMManager()
        crms = manager.get_all_crms()

        assert isinstance(crms, list)
        assert len(crms) > 0
        assert all('name' in crm for crm in crms)
        assert all('certified_value' in crm for crm in crms)

    def test_get_crm_by_name(self):
        """Test getting CRM by name."""
        manager = CRMManager()

        # Test exact match
        crm = manager.get_crm_by_name('NIST SRM 2709a')
        assert crm is not None
        assert crm['name'] == 'NIST SRM 2709a'
        assert crm['certified_value'] == 0.85

        # Test case insensitive
        crm = manager.get_crm_by_name('nist srm 2709a')
        assert crm is not None
        assert crm['name'] == 'NIST SRM 2709a'

        # Test not found
        crm = manager.get_crm_by_name('Nonexistent CRM')
        assert crm is None

    def test_get_crms_by_matrix(self):
        """Test getting CRMs by matrix."""
        manager = CRMManager()

        # Test soil matrix
        soil_crms = manager.get_crms_by_matrix('soil')
        assert len(soil_crms) > 0
        assert all('soil' in crm.get('matrix', '').lower() for crm in soil_crms)

        # Test sediment matrix
        sediment_crms = manager.get_crms_by_matrix('sediment')
        assert len(sediment_crms) > 0
        assert all('sediment' in crm.get('matrix', '').lower() for crm in sediment_crms)

    def test_get_crms_by_concentration_range(self):
        """Test getting CRMs by concentration range."""
        manager = CRMManager()

        # Test low concentration range
        low_crms = manager.get_crms_by_concentration_range(0.0, 1.0)
        assert len(low_crms) > 0
        assert all(0.0 <= crm.get('certified_value', 0) <= 1.0 for crm in low_crms)

        # Test high concentration range
        high_crms = manager.get_crms_by_concentration_range(10.0, 50.0)
        assert len(high_crms) > 0
        assert all(10.0 <= crm.get('certified_value', 0) <= 50.0 for crm in high_crms)

    def test_get_crms_by_supplier(self):
        """Test getting CRMs by supplier."""
        manager = CRMManager()

        # Test NIST supplier
        nist_crms = manager.get_crms_by_supplier('NIST')
        assert len(nist_crms) > 0
        assert all('NIST' in crm.get('supplier', '') for crm in nist_crms)

        # Test CANMET supplier
        canmet_crms = manager.get_crms_by_supplier('CANMET')
        assert len(canmet_crms) > 0
        assert all('CANMET' in crm.get('supplier', '') for crm in canmet_crms)

    def test_check_crm_expiry(self):
        """Test checking CRM expiry."""
        manager = CRMManager()

        # Test valid CRM
        is_expired, message = manager.check_crm_expiry('NIST SRM 2709a')
        assert not is_expired
        assert 'valid until' in message or 'days remaining' in message

        # Test nonexistent CRM
        is_expired, message = manager.check_crm_expiry('Nonexistent CRM')
        assert is_expired
        assert 'not found' in message

    def test_get_certified_value(self):
        """Test getting certified value."""
        manager = CRMManager()

        # Test valid CRM
        value = manager.get_certified_value('NIST SRM 2709a')
        assert value == 0.85

        # Test nonexistent CRM
        value = manager.get_certified_value('Nonexistent CRM')
        assert value is None

    def test_get_uncertainty(self):
        """Test getting uncertainty."""
        manager = CRMManager()

        # Test valid CRM
        uncertainty = manager.get_uncertainty('NIST SRM 2709a')
        assert uncertainty == 0.05

        # Test nonexistent CRM
        uncertainty = manager.get_uncertainty('Nonexistent CRM')
        assert uncertainty is None

    def test_get_crm_info(self):
        """Test getting complete CRM info."""
        manager = CRMManager()

        # Test valid CRM
        info = manager.get_crm_info('NIST SRM 2709a')
        assert info is not None
        assert info['name'] == 'NIST SRM 2709a'
        assert info['certified_value'] == 0.85
        assert info['uncertainty'] == 0.05
        assert info['matrix'] == 'Freshwater Sediment'

        # Test nonexistent CRM
        info = manager.get_crm_info('Nonexistent CRM')
        assert info is None

    def test_validate_crm_selection(self):
        """Test validating CRM selection."""
        manager = CRMManager()

        # Test valid selection
        is_valid, message = manager.validate_crm_selection('NIST SRM 2709a', 0.8)
        assert is_valid
        assert 'valid for analysis' in message

        # Test concentration mismatch
        is_valid, message = manager.validate_crm_selection('NIST SRM 2709a', 10.0)
        assert not is_valid
        assert 'not suitable' in message

        # Test nonexistent CRM
        is_valid, message = manager.validate_crm_selection('Nonexistent CRM', 1.0)
        assert not is_valid
        assert 'not found' in message

    def test_get_analysis_thresholds(self):
        """Test getting analysis thresholds."""
        manager = CRMManager()
        thresholds = manager.get_analysis_thresholds()

        assert 'z_score_threshold' in thresholds
        assert 'recovery_limits' in thresholds
        assert 'precision_threshold' in thresholds
        assert thresholds['z_score_threshold'] == 2.0

    def test_get_methods(self):
        """Test getting analysis methods."""
        manager = CRMManager()
        methods = manager.get_methods()

        assert 'fire_assay' in methods
        assert 'icp_ms' in methods
        assert 'icp_aes' in methods

        fire_assay = methods['fire_assay']
        assert 'name' in fire_assay
        assert 'detection_limit' in fire_assay
        assert 'working_range' in fire_assay

    def test_search_crms(self):
        """Test searching CRMs."""
        manager = CRMManager()

        # Test search by name
        results = manager.search_crms('NIST')
        assert len(results) > 0
        assert all('NIST' in crm.get('name', '') for crm in results)

        # Test search by matrix
        results = manager.search_crms('soil')
        assert len(results) > 0
        assert any('soil' in crm.get('matrix', '').lower() for crm in results)

        # Test search by supplier
        results = manager.search_crms('CANMET')
        assert len(results) > 0
        assert all('CANMET' in crm.get('supplier', '') for crm in results)

    def test_get_database_info(self):
        """Test getting database info."""
        manager = CRMManager()
        info = manager.get_database_info()

        assert 'version' in info
        assert 'last_updated' in info
        assert 'description' in info

    def test_get_crm_summary(self):
        """Test getting CRM summary."""
        manager = CRMManager()
        summary = manager.get_crm_summary()

        assert 'total_crms' in summary
        assert 'suppliers' in summary
        assert 'matrices' in summary
        assert 'concentration_range' in summary

        assert summary['total_crms'] > 0
        assert len(summary['suppliers']) > 0
        assert len(summary['matrices']) > 0
        assert summary['concentration_range']['min'] >= 0
        assert summary['concentration_range']['max'] > 0

    def test_reload_database(self):
        """Test reloading database."""
        manager = CRMManager()
        original_crms = manager.get_all_crms()

        # Reload should work without errors
        manager.reload_database()
        reloaded_crms = manager.get_all_crms()

        assert len(reloaded_crms) == len(original_crms)
        assert reloaded_crms[0]['name'] == original_crms[0]['name']
