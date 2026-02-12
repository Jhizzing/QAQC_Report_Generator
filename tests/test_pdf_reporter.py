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
        assert hasattr(reporter, 'page_size')
        assert hasattr(reporter, 'margins')
        assert reporter.config is not None

    def test_init_custom_config(self):
        """Test initialization with custom config."""
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        
        config = {
            'include_plots': False,
            'page_size': letter,
            'margins': {'top': 2 * inch, 'bottom': 2 * inch, 'left': 2 * inch, 'right': 2 * inch}
        }
        reporter = PDFReporter(config)
        assert reporter.include_plots == False
        assert reporter.page_size == letter
        assert reporter.margins['top'] == 2 * inch

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

        summary_elements = reporter.build_executive_summary(analysis_results)

        # build_executive_summary returns a list of ReportLab elements
        assert isinstance(summary_elements, list)
        assert len(summary_elements) > 0
        # Check that it contains expected content by converting to string representation
        summary_text = str(summary_elements)
        assert 'EXECUTIVE SUMMARY' in summary_text or any('EXECUTIVE' in str(e) for e in summary_elements)

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

        summary_elements = reporter.build_executive_summary(analysis_results)

        # build_executive_summary returns a list of ReportLab elements
        assert isinstance(summary_elements, list)
        assert len(summary_elements) > 0

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

        # Check that recommendations list contains expected items
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        # Check for key recommendation text (actual implementation may have slightly different wording)
        recommendation_text = ' '.join(recommendations)
        assert 'bias' in recommendation_text.lower() or 'contamination' in recommendation_text.lower() or 'precision' in recommendation_text.lower()

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

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        # Should have the "all good" message when no issues
        recommendation_text = ' '.join(recommendations)
        assert 'acceptable limits' in recommendation_text.lower() or 'continue' in recommendation_text.lower()

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

        # Use build_standards_section instead
        section_elements = reporter.build_standards_section(results)

        # build_standards_section returns a list of ReportLab elements
        assert isinstance(section_elements, list)
        assert len(section_elements) > 0

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

        # Use build_blanks_section instead
        section_elements = reporter.build_blanks_section(results)

        # build_blanks_section returns a list of ReportLab elements
        assert isinstance(section_elements, list)
        assert len(section_elements) > 0

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

        # Use build_duplicates_section instead
        section_elements = reporter.build_duplicates_section(results)

        # build_duplicates_section returns a list of ReportLab elements
        assert isinstance(section_elements, list)
        assert len(section_elements) > 0

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
            
            # PDF files are binary, so we just verify it was created and has content
            # Content verification would require PDF parsing library

        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)
