"""
Tests for reporting modules.
"""
import pytest
import tempfile
import os
from src.reporting import ExcelReporter


class TestExcelReporter:
    """Test ExcelReporter functionality."""

    def test_init_default_config(self):
        """Test initialization with default config."""
        reporter = ExcelReporter()
        assert reporter.include_plots == True
        assert reporter.include_raw_data == True

    def test_init_custom_config(self):
        """Test initialization with custom config."""
        config = {
            'include_plots': False,
            'include_raw_data': False
        }
        reporter = ExcelReporter(config)
        assert reporter.include_plots == False
        assert reporter.include_raw_data == False

    def test_create_summary_sheet(self):
        """Test summary sheet creation."""
        reporter = ExcelReporter()
        analysis_results = {
            'standards': {
                'overall_acceptable': True,
                'summary': {'n_measurements': 5}
            },
            'blanks': {
                'overall_acceptable': True,
                'summary': {'n_blanks': 3}
            },
            'duplicates': {
                'overall_acceptable': True,
                'summary': {'n_duplicates': 2}
            },
            'total_samples': 10
        }

        result = reporter.create_summary_sheet(analysis_results)

        assert 'name' in result
        assert 'data' in result
        assert 'description' in result
        assert result['name'] == 'Summary'
        assert 'Overall QAQC Status' in result['data']['Metric'].values

    def test_create_standards_sheet(self):
        """Test standards sheet creation."""
        reporter = ExcelReporter()
        standards_results = {
            'bias': {
                'bias_detected': False,
                'systematic_bias': False,
                'max_z_score': 1.5,
                'mean_z_score': 0.2
            },
            'recovery': {
                'acceptable': True,
                'mean_recovery': 98.5
            },
            'precision': {
                'acceptable': True,
                'rsd': 3.2,
                'cv': 0.032,
                'std_dev': 0.32
            }
        }

        result = reporter.create_standards_sheet(standards_results)

        assert 'name' in result
        assert 'data' in result
        assert 'description' in result
        assert result['name'] == 'Standards'
        assert 'Bias Detected' in result['data']['Metric'].values

    def test_create_blanks_sheet(self):
        """Test blanks sheet creation."""
        reporter = ExcelReporter()
        blanks_results = {
            'contamination': {
                'acceptable': True,
                'contamination_rate': 0.05,
                'mdl': 0.01,
                'threshold': 0.03
            },
            'carryover': {
                'carryover_detected': False,
                'trend': 0.001
            },
            'background': {
                'acceptable': True,
                'mean': 0.005,
                'std_dev': 0.002,
                'cv': 40.0
            }
        }

        result = reporter.create_blanks_sheet(blanks_results)

        assert 'name' in result
        assert 'data' in result
        assert 'description' in result
        assert result['name'] == 'Blanks'
        assert 'Contamination Acceptable' in result['data']['Metric'].values

    def test_create_duplicates_sheet(self):
        """Test duplicates sheet creation."""
        reporter = ExcelReporter()
        duplicates_results = {
            'precision': {
                'acceptable': True,
                'mean_rpd': 8.5,
                'max_rpd': 15.2,
                'threshold': 20.0
            },
            'systematic_errors': {
                'systematic_error': False,
                'bias': 0.02
            },
            'nugget_ratio': 0.25
        }

        result = reporter.create_duplicates_sheet(duplicates_results)

        assert 'name' in result
        assert 'data' in result
        assert 'description' in result
        assert result['name'] == 'Duplicates'
        assert 'Precision Acceptable' in result['data']['Metric'].values

    def test_create_raw_data_sheet(self):
        """Test raw data sheet creation."""
        reporter = ExcelReporter()
        raw_data = {
            'data': [
                {'sample_id': 'S001', 'value': 10.5, 'type': 'STANDARD'},
                {'sample_id': 'S002', 'value': 9.8, 'type': 'BLANK'}
            ],
            'flags': {
                'bias': [False, False],
                'contamination': [False, True]
            }
        }

        result = reporter.create_raw_data_sheet(raw_data)

        assert 'name' in result
        assert 'data' in result
        assert 'description' in result
        assert result['name'] == 'Raw Data'
        assert 'FLAG_BIAS' in result['data'].columns
        assert 'FLAG_CONTAMINATION' in result['data'].columns

    def test_generate_excel_report(self):
        """Test Excel report generation."""
        reporter = ExcelReporter()
        analysis_results = {
            'standards': {
                'overall_acceptable': True,
                'bias': {'bias_detected': False},
                'recovery': {'acceptable': True, 'mean_recovery': 98.5},
                'precision': {'acceptable': True, 'rsd': 3.2},
                'summary': {'n_measurements': 5}
            },
            'blanks': {
                'overall_acceptable': True,
                'contamination': {'acceptable': True},
                'carryover': {'carryover_detected': False},
                'background': {'acceptable': True},
                'summary': {'n_blanks': 3}
            },
            'duplicates': {
                'overall_acceptable': True,
                'precision': {'acceptable': True},
                'systematic_errors': {'systematic_error': False},
                'summary': {'n_duplicates': 2}
            },
            'total_samples': 10
        }

        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            filename = tmp.name

        try:
            result = reporter.generate_excel_report(analysis_results, filename=filename)
            assert result == filename
            assert os.path.exists(filename)
        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)
