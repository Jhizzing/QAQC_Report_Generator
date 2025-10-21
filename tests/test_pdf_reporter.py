"""
Tests for PDF reporter functionality.
"""
import pytest
import tempfile
import os
from src.reporting import PDFReporter


class TestPDFReporter:
    """Test PDFReporter functionality."""

    def test_init_default_config(self):
        """Test initialization with default config."""
        reporter = PDFReporter()
        assert reporter.include_plots == True
        assert reporter.include_raw_data == True
        assert reporter.page_size == 'A4'
        assert reporter.margins == {'top': 1, 'bottom': 1, 'left': 1, 'right': 1}

    def test_init_custom_config(self):
        """Test initialization with custom config."""
        config = {
            'include_plots': False,
            'include_raw_data': False,
            'page_size': 'Letter',
            'margins': {'top': 2, 'bottom': 2, 'left': 2, 'right': 2}
        }
        reporter = PDFReporter(config)
        assert reporter.include_plots == False
        assert reporter.include_raw_data == False
        assert reporter.page_size == 'Letter'
        assert reporter.margins == {'top': 2, 'bottom': 2, 'left': 2, 'right': 2}

    def test_create_executive_summary(self):
        """Test executive summary creation."""
        reporter = PDFReporter()
        analysis_results = {
            'standards': {
                'overall_acceptable': True,
                'bias': {'bias_detected': False},
                'recovery': {'mean_recovery': 98.5},
                'precision': {'rsd': 3.2}
            },
            'blanks': {
                'overall_acceptable': True,
                'contamination': {'contamination_rate': 0.05},
                'mdl': 0.01,
                'carryover': {'carryover_detected': False}
            },
            'duplicates': {
                'overall_acceptable': True,
                'precision': {'mean_rpd': 8.5},
                'systematic_errors': {'systematic_error': False},
                'nugget_ratio': 0.25
            },
            'total_samples': 10,
            'analysis_date': '2024-01-15'
        }

        summary = reporter.create_executive_summary(analysis_results)

        assert 'EXECUTIVE SUMMARY' in summary
        assert 'Overall QAQC Status: PASS' in summary
        assert 'STANDARDS ANALYSIS: PASS' in summary
        assert 'BLANKS ANALYSIS: PASS' in summary
        assert 'DUPLICATES ANALYSIS: PASS' in summary
        assert 'Total Samples: 10' in summary

    def test_create_executive_summary_fail(self):
        """Test executive summary with failed analysis."""
        reporter = PDFReporter()
        analysis_results = {
            'standards': {
                'overall_acceptable': False,
                'bias': {'bias_detected': True},
                'recovery': {'mean_recovery': 85.0},
                'precision': {'rsd': 8.5}
            },
            'blanks': {
                'overall_acceptable': True,
                'contamination': {'contamination_rate': 0.05},
                'mdl': 0.01,
                'carryover': {'carryover_detected': False}
            },
            'duplicates': {
                'overall_acceptable': True,
                'precision': {'mean_rpd': 8.5},
                'systematic_errors': {'systematic_error': False},
                'nugget_ratio': 0.25
            },
            'total_samples': 10
        }

        summary = reporter.create_executive_summary(analysis_results)

        assert 'Overall QAQC Status: FAIL' in summary
        assert 'STANDARDS ANALYSIS: FAIL' in summary
        assert 'Bias Detection: YES' in summary

    def test_generate_recommendations(self):
        """Test recommendation generation."""
        reporter = PDFReporter()

        # Test with issues
        analysis_results = {
            'standards': {
                'bias': {'bias_detected': True},
                'recovery': {'acceptable': False},
                'precision': {'acceptable': False}
            },
            'blanks': {
                'contamination': {'acceptable': False},
                'carryover': {'carryover_detected': True},
                'background': {'acceptable': False}
            },
            'duplicates': {
                'precision': {'acceptable': False},
                'systematic_errors': {'systematic_error': True},
                'nugget_ratio': 0.5
            }
        }

        recommendations = reporter._generate_recommendations(analysis_results)

        assert 'Investigate and correct systematic bias' in recommendations
        assert 'Review recovery procedures' in recommendations
        assert 'Improve precision' in recommendations
        assert 'Investigate contamination sources' in recommendations
        assert 'Implement additional rinsing' in recommendations
        assert 'Review background levels' in recommendations
        assert 'Improve duplicate precision' in recommendations
        assert 'Investigate systematic errors' in recommendations
        assert 'Consider spatial sampling strategy' in recommendations

    def test_generate_recommendations_no_issues(self):
        """Test recommendation generation with no issues."""
        reporter = PDFReporter()

        analysis_results = {
            'standards': {
                'bias': {'bias_detected': False},
                'recovery': {'acceptable': True},
                'precision': {'acceptable': True}
            },
            'blanks': {
                'contamination': {'acceptable': True},
                'carryover': {'carryover_detected': False},
                'background': {'acceptable': True}
            },
            'duplicates': {
                'precision': {'acceptable': True},
                'systematic_errors': {'systematic_error': False},
                'nugget_ratio': 0.2
            }
        }

        recommendations = reporter._generate_recommendations(analysis_results)

        assert 'All QAQC parameters are within acceptable limits' in recommendations

    def test_create_detailed_section_standards(self):
        """Test detailed standards section creation."""
        reporter = PDFReporter()
        results = {
            'bias': {
                'bias_detected': False,
                'systematic_bias': False,
                'max_z_score': 1.5,
                'mean_z_score': 0.2
            },
            'recovery': {
                'acceptable': True,
                'mean_recovery': 98.5,
                'limits': (90, 110)
            },
            'precision': {
                'acceptable': True,
                'rsd': 3.2,
                'cv': 0.032,
                'std_dev': 0.32
            }
        }

        section = reporter.create_detailed_section('Standards', results)

        assert 'STANDARDS' in section
        assert 'BIAS ANALYSIS:' in section
        assert 'RECOVERY ANALYSIS:' in section
        assert 'PRECISION ANALYSIS:' in section
        assert 'Bias Detected: NO' in section
        assert 'Recovery Acceptable: YES' in section
        assert 'Precision Acceptable: YES' in section

    def test_create_detailed_section_blanks(self):
        """Test detailed blanks section creation."""
        reporter = PDFReporter()
        results = {
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

        section = reporter.create_detailed_section('Blanks', results)

        assert 'BLANKS' in section
        assert 'CONTAMINATION ANALYSIS:' in section
        assert 'CARRY-OVER ANALYSIS:' in section
        assert 'BACKGROUND ANALYSIS:' in section
        assert 'Contamination Acceptable: YES' in section
        assert 'Carry-over Detected: NO' in section
        assert 'Background Acceptable: YES' in section

    def test_create_detailed_section_duplicates(self):
        """Test detailed duplicates section creation."""
        reporter = PDFReporter()
        results = {
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

        section = reporter.create_detailed_section('Duplicates', results)

        assert 'DUPLICATES' in section
        assert 'PRECISION ANALYSIS:' in section
        assert 'SYSTEMATIC ERROR ANALYSIS:' in section
        assert 'SPATIAL ANALYSIS:' in section
        assert 'Precision Acceptable: YES' in section
        assert 'Systematic Error: NO' in section
        assert 'Nugget Ratio: 0.250' in section

    def test_generate_pdf_report(self):
        """Test PDF report generation."""
        reporter = PDFReporter()
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
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            filename = tmp.name

        try:
            result = reporter.generate_pdf_report(analysis_results, filename=filename)
            assert result == filename
            assert os.path.exists(filename)
            assert os.path.getsize(filename) > 0

            # Check content
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'QAQC ANALYSIS REPORT' in content
                assert 'EXECUTIVE SUMMARY' in content
                assert 'STANDARDS' in content
                assert 'BLANKS' in content
                assert 'DUPLICATES' in content

        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)
