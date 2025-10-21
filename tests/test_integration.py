"""
Integration tests for the complete QAQC pipeline.
"""
import pytest
import tempfile
import os
from src.analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer
from src.visualization import PlotGenerator
from src.reporting import ExcelReporter


class TestQAQCPipeline:
    """Test complete QAQC analysis pipeline."""

    def test_full_pipeline(self):
        """Test complete QAQC pipeline from data to report."""
        # Sample data
        standards_data = {
            'measured': [10.0, 10.2, 9.8, 10.1, 9.9],
            'certified': 10.0,
            'uncertainty': 0.5
        }

        blanks_data = {
            'blanks': [0.01, 0.02, 0.015, 0.018, 0.012],
            'previous_samples': [1.0, 2.0, 1.5]
        }

        duplicates_data = {
            'duplicates': [[10.0, 12.0], [15.0, 17.0], [20.0, 22.0]]
        }

        # Initialize analyzers
        standards_analyzer = StandardsAnalyzer()
        blanks_analyzer = BlanksAnalyzer()
        duplicates_analyzer = DuplicatesAnalyzer()

        # Run analyses
        standards_results = standards_analyzer.analyze_standards(standards_data)
        blanks_results = blanks_analyzer.analyze_blanks(blanks_data)
        duplicates_results = duplicates_analyzer.analyze_duplicates(duplicates_data)

        # Verify results structure
        assert 'overall_acceptable' in standards_results
        assert 'bias' in standards_results
        assert 'recovery' in standards_results
        assert 'precision' in standards_results

        assert 'overall_acceptable' in blanks_results
        assert 'contamination' in blanks_results
        assert 'carryover' in blanks_results
        assert 'background' in blanks_results

        assert 'overall_acceptable' in duplicates_results
        assert 'precision' in duplicates_results
        assert 'systematic_errors' in duplicates_results
        assert 'nugget_ratio' in duplicates_results

    def test_visualization_pipeline(self):
        """Test visualization generation."""
        # Sample data
        control_data = [10.0, 10.2, 9.8, 10.1, 9.9, 10.3, 9.7, 10.0]
        scatter_x = [10.0, 12.0, 15.0, 18.0, 20.0]
        scatter_y = [10.5, 12.2, 14.8, 17.9, 20.1]
        histogram_data = [10.0, 10.2, 9.8, 10.1, 9.9, 10.3, 9.7, 10.0, 10.1, 9.8]

        # Initialize plot generator
        plot_generator = PlotGenerator()

        # Create plots
        control_plot = plot_generator.create_control_chart(
            control_data,
            {'center': 10.0, 'ucl': 10.5, 'lcl': 9.5},
            "Standards Control Chart"
        )

        scatter_plot = plot_generator.create_scatter_plot(
            scatter_x, scatter_y, "Duplicates Scatter Plot"
        )

        histogram_plot = plot_generator.create_histogram(
            histogram_data, bins=5, title="Distribution Histogram"
        )

        # Verify plot structures
        assert 'figure' in control_plot
        assert 'axes' in control_plot
        assert 'data' in control_plot

        assert 'figure' in scatter_plot
        assert 'r_squared' in scatter_plot
        assert 0 <= scatter_plot['r_squared'] <= 1

        assert 'figure' in histogram_plot
        assert 'mean' in histogram_plot
        assert 'std' in histogram_plot

    def test_reporting_pipeline(self):
        """Test Excel report generation."""
        # Sample analysis results
        analysis_results = {
            'standards': {
                'overall_acceptable': True,
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
                },
                'summary': {'n_measurements': 5}
            },
            'blanks': {
                'overall_acceptable': True,
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
                },
                'summary': {'n_blanks': 3}
            },
            'duplicates': {
                'overall_acceptable': True,
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
                'nugget_ratio': 0.25,
                'summary': {'n_duplicates': 2}
            },
            'total_samples': 10
        }

        # Sample raw data
        raw_data = {
            'data': [
                {'sample_id': 'S001', 'value': 10.5, 'type': 'STANDARD'},
                {'sample_id': 'S002', 'value': 9.8, 'type': 'BLANK'},
                {'sample_id': 'S003', 'value': 15.2, 'type': 'DUPLICATE'}
            ],
            'flags': {
                'bias': [False, False, False],
                'contamination': [False, True, False]
            }
        }

        # Initialize reporter
        reporter = ExcelReporter()

        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            filename = tmp.name

        try:
            # Generate report
            result = reporter.generate_excel_report(analysis_results, raw_data, filename)

            # Verify file was created
            assert result == filename
            assert os.path.exists(filename)
            assert os.path.getsize(filename) > 0

        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        # This test demonstrates the complete workflow
        # that would be used in the main application

        # 1. Sample data (would come from importer)
        standards_data = {
            'measured': [10.0, 10.2, 9.8, 10.1, 9.9],
            'certified': 10.0,
            'uncertainty': 0.5
        }

        blanks_data = {
            'blanks': [0.01, 0.02, 0.015, 0.018, 0.012],
            'previous_samples': [1.0, 2.0, 1.5]
        }

        duplicates_data = {
            'duplicates': [[10.0, 12.0], [15.0, 17.0], [20.0, 22.0]]
        }

        # 2. Initialize components
        standards_analyzer = StandardsAnalyzer()
        blanks_analyzer = BlanksAnalyzer()
        duplicates_analyzer = DuplicatesAnalyzer()
        plot_generator = PlotGenerator()
        reporter = ExcelReporter()

        # 3. Run analyses
        standards_results = standards_analyzer.analyze_standards(standards_data)
        blanks_results = blanks_analyzer.analyze_blanks(blanks_data)
        duplicates_results = duplicates_analyzer.analyze_duplicates(duplicates_data)

        # 4. Create visualizations
        control_plot = plot_generator.create_control_chart(
            standards_data['measured'],
            {'center': 10.0, 'ucl': 10.5, 'lcl': 9.5},
            "Standards Control Chart"
        )

        # 5. Compile results
        analysis_results = {
            'standards': standards_results,
            'blanks': blanks_results,
            'duplicates': duplicates_results,
            'total_samples': 10
        }

        # 6. Generate report
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            filename = tmp.name

        try:
            report_path = reporter.generate_excel_report(analysis_results, filename=filename)

            # Verify complete workflow
            assert os.path.exists(report_path)
            assert os.path.getsize(report_path) > 0

            # Verify analysis results are reasonable
            assert isinstance(standards_results['overall_acceptable'], bool)
            assert isinstance(blanks_results['overall_acceptable'], bool)
            assert isinstance(duplicates_results['overall_acceptable'], bool)

        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)
