"""
Reporting utilities for QAQC application.
"""

from .pdf_reporter import QAQCPDFReporter, PDFReporter
from .docx_reporter import QAQCDOCXReporter, DOCXReporter
from .excel_reporter import ExcelChartReporter, generate_excel_with_charts

class ReportGenerator:
    def __init__(self) -> None:
        pass

__all__ = [
    'ReportGenerator', 
    'ExcelReporter', 
    'PDFReporter', 
    'QAQCPDFReporter',
    'DOCXReporter',
    'QAQCDOCXReporter',
    'ExcelChartReporter',
    'generate_excel_with_charts',
]

class ExcelReporter:
    """
    Generates Excel reports with multiple sheets for QAQC analysis.

    Sheet structure:
    - Summary: Overall results and flags
    - Standards: Standards analysis results
    - Blanks: Blanks analysis results
    - Duplicates: Duplicates analysis results
    - Raw Data: Original data with flags
    """

    def __init__(self, config: dict = None) -> None:
        """
        Initialize with reporting configuration.

        Args:
            config: Dictionary with report settings
        """
        self.config = config or {}
        self.include_plots = self.config.get('include_plots', True)
        self.include_raw_data = self.config.get('include_raw_data', True)

    def create_summary_sheet(self, analysis_results: dict) -> dict:
        """
        Create summary sheet with overall results.

        Args:
            analysis_results: Dictionary with all analysis results

        Returns:
            Dictionary with sheet data
        """
        import pandas as pd
        from datetime import datetime

        # Extract key metrics
        standards = analysis_results.get('standards', {})
        blanks = analysis_results.get('blanks', {})
        duplicates = analysis_results.get('duplicates', {})

        # Create summary data
        summary_data = {
            'Metric': [
                'Overall QAQC Status',
                'Standards Analysis',
                'Blanks Analysis',
                'Duplicates Analysis',
                'Total Samples',
                'Standards Count',
                'Blanks Count',
                'Duplicates Count',
                'Analysis Date'
            ],
            'Value': [
                'PASS' if all([
                    standards.get('overall_acceptable', False),
                    blanks.get('overall_acceptable', False),
                    duplicates.get('overall_acceptable', False)
                ]) else 'FAIL',
                'PASS' if standards.get('overall_acceptable', False) else 'FAIL',
                'PASS' if blanks.get('overall_acceptable', False) else 'FAIL',
                'PASS' if duplicates.get('overall_acceptable', False) else 'FAIL',
                analysis_results.get('total_samples', 0),
                standards.get('summary', {}).get('n_measurements', 0),
                blanks.get('summary', {}).get('n_blanks', 0),
                duplicates.get('summary', {}).get('n_duplicates', 0),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
        }

        df = pd.DataFrame(summary_data)

        return {
            'name': 'Summary',
            'data': df,
            'description': 'Overall QAQC analysis summary'
        }

    def create_standards_sheet(self, standards_results: dict) -> dict:
        """
        Create standards analysis sheet.

        Args:
            standards_results: Standards analysis results

        Returns:
            Dictionary with sheet data
        """
        import pandas as pd

        # Extract detailed results
        bias = standards_results.get('bias', {})
        recovery = standards_results.get('recovery', {})
        precision = standards_results.get('precision', {})

        # Create detailed data
        standards_data = {
            'Metric': [
                'Bias Detected',
                'Systematic Bias',
                'Max Z-Score',
                'Mean Z-Score',
                'Recovery Acceptable',
                'Mean Recovery (%)',
                'Precision Acceptable',
                'RSD (%)',
                'CV',
                'Standard Deviation'
            ],
            'Value': [
                'YES' if bias.get('bias_detected', False) else 'NO',
                'YES' if bias.get('systematic_bias', False) else 'NO',
                f"{bias.get('max_z_score', 0):.3f}",
                f"{bias.get('mean_z_score', 0):.3f}",
                'YES' if recovery.get('acceptable', False) else 'NO',
                f"{recovery.get('mean_recovery', 0):.2f}",
                'YES' if precision.get('acceptable', False) else 'NO',
                f"{precision.get('rsd', 0):.2f}",
                f"{precision.get('cv', 0):.3f}",
                f"{precision.get('std_dev', 0):.3f}"
            ]
        }

        df = pd.DataFrame(standards_data)

        return {
            'name': 'Standards',
            'data': df,
            'description': 'Standards analysis detailed results'
        }

    def create_blanks_sheet(self, blanks_results: dict) -> dict:
        """
        Create blanks analysis sheet.

        Args:
            blanks_results: Blanks analysis results

        Returns:
            Dictionary with sheet data
        """
        import pandas as pd

        # Extract detailed results
        contamination = blanks_results.get('contamination', {})
        carryover = blanks_results.get('carryover', {})
        background = blanks_results.get('background', {})

        # Create detailed data
        blanks_data = {
            'Metric': [
                'Contamination Acceptable',
                'Contamination Rate (%)',
                'MDL',
                'Contamination Threshold',
                'Carry-over Detected',
                'Carry-over Trend',
                'Background Acceptable',
                'Background Mean',
                'Background Std Dev',
                'Background CV (%)'
            ],
            'Value': [
                'YES' if contamination.get('acceptable', False) else 'NO',
                f"{contamination.get('contamination_rate', 0) * 100:.2f}",
                f"{contamination.get('mdl', 0):.3f}",
                f"{contamination.get('threshold', 0):.3f}",
                'YES' if carryover.get('carryover_detected', False) else 'NO',
                f"{carryover.get('trend', 0):.3f}",
                'YES' if background.get('acceptable', False) else 'NO',
                f"{background.get('mean', 0):.3f}",
                f"{background.get('std_dev', 0):.3f}",
                f"{background.get('cv', 0):.2f}"
            ]
        }

        df = pd.DataFrame(blanks_data)

        return {
            'name': 'Blanks',
            'data': df,
            'description': 'Blanks analysis detailed results'
        }

    def create_duplicates_sheet(self, duplicates_results: dict) -> dict:
        """
        Create duplicates analysis sheet.

        Args:
            duplicates_results: Duplicates analysis results

        Returns:
            Dictionary with sheet data
        """
        import pandas as pd

        # Extract detailed results
        precision = duplicates_results.get('precision', {})
        systematic = duplicates_results.get('systematic_errors', {})

        # Create detailed data
        duplicates_data = {
            'Metric': [
                'Precision Acceptable',
                'Mean RPD (%)',
                'Max RPD (%)',
                'RPD Threshold (%)',
                'Systematic Error',
                'Mean Bias',
                'Nugget Ratio',
                'Nugget Threshold'
            ],
            'Value': [
                'YES' if precision.get('acceptable', False) else 'NO',
                f"{precision.get('mean_rpd', 0):.2f}",
                f"{precision.get('max_rpd', 0):.2f}",
                f"{precision.get('threshold', 0):.2f}",
                'YES' if systematic.get('systematic_error', False) else 'NO',
                f"{systematic.get('bias', 0):.3f}",
                f"{duplicates_results.get('nugget_ratio', 0):.3f}",
                f"{self.config.get('nugget_threshold', 0.3):.3f}"
            ]
        }

        df = pd.DataFrame(duplicates_data)

        return {
            'name': 'Duplicates',
            'data': df,
            'description': 'Duplicates analysis detailed results'
        }

    def create_raw_data_sheet(self, raw_data: dict) -> dict:
        """
        Create raw data sheet with QAQC flags.

        Args:
            raw_data: Dictionary with raw data and flags

        Returns:
            Dictionary with sheet data
        """
        import pandas as pd

        # Convert raw data to DataFrame
        df = pd.DataFrame(raw_data.get('data', []))

        # Add QAQC flags if available
        if 'flags' in raw_data:
            for flag_name, flag_values in raw_data['flags'].items():
                df[f'FLAG_{flag_name.upper()}'] = flag_values

        return {
            'name': 'Raw Data',
            'data': df,
            'description': 'Original data with QAQC flags'
        }

    def generate_excel_report(self, analysis_results: dict, raw_data: dict = None, filename: str = None) -> str:
        """
        Generate complete Excel report.

        Args:
            analysis_results: Dictionary with all analysis results
            raw_data: Dictionary with raw data (optional)
            filename: Output filename (optional)

        Returns:
            Path to generated Excel file
        """
        import pandas as pd
        from datetime import datetime
        import os

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"qaqc_report_{timestamp}.xlsx"

        # Ensure output directory exists
        output_dir = os.path.dirname(filename) or "."
        os.makedirs(output_dir, exist_ok=True)

        # Create Excel writer
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Summary sheet
            summary_sheet = self.create_summary_sheet(analysis_results)
            summary_sheet['data'].to_excel(writer, sheet_name=summary_sheet['name'], index=False)

            # Standards sheet
            if 'standards' in analysis_results:
                standards_sheet = self.create_standards_sheet(analysis_results['standards'])
                standards_sheet['data'].to_excel(writer, sheet_name=standards_sheet['name'], index=False)

            # Blanks sheet
            if 'blanks' in analysis_results:
                blanks_sheet = self.create_blanks_sheet(analysis_results['blanks'])
                blanks_sheet['data'].to_excel(writer, sheet_name=blanks_sheet['name'], index=False)

            # Duplicates sheet
            if 'duplicates' in analysis_results:
                duplicates_sheet = self.create_duplicates_sheet(analysis_results['duplicates'])
                duplicates_sheet['data'].to_excel(writer, sheet_name=duplicates_sheet['name'], index=False)

            # Raw data sheet
            if raw_data and self.include_raw_data:
                raw_sheet = self.create_raw_data_sheet(raw_data)
                raw_sheet['data'].to_excel(writer, sheet_name=raw_sheet['name'], index=False)

        return filename

# Legacy PDFReporter class has been moved to pdf_reporter.py
# The QAQCPDFReporter class provides full ReportLab-based PDF generation
