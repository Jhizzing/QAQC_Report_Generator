"""
Reporting utilities for QAQC application.
"""

class ReportGenerator:
    def __init__(self) -> None:
        pass

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

class PDFReporter:
    """
    Generates PDF reports with formatted text and embedded plots.

    Report sections:
    - Executive Summary
    - Standards Analysis
    - Blanks Analysis
    - Duplicates Analysis
    - Recommendations
    - Appendices (plots, raw data)
    """

    def __init__(self, config: dict = None) -> None:
        """
        Initialize with PDF reporting configuration.

        Args:
            config: Dictionary with report settings
        """
        self.config = config or {}
        self.include_plots = self.config.get('include_plots', True)
        self.include_raw_data = self.config.get('include_raw_data', True)
        self.page_size = self.config.get('page_size', 'A4')
        self.margins = self.config.get('margins', {'top': 1, 'bottom': 1, 'left': 1, 'right': 1})

    def create_executive_summary(self, analysis_results: dict) -> str:
        """
        Create executive summary section.

        Args:
            analysis_results: Dictionary with all analysis results

        Returns:
            Formatted summary text
        """
        standards = analysis_results.get('standards', {})
        blanks = analysis_results.get('blanks', {})
        duplicates = analysis_results.get('duplicates', {})

        # Determine overall status
        overall_pass = all([
            standards.get('overall_acceptable', False),
            blanks.get('overall_acceptable', False),
            duplicates.get('overall_acceptable', False)
        ])

        status = "PASS" if overall_pass else "FAIL"

        summary = f"""
EXECUTIVE SUMMARY
================

Overall QAQC Status: {status}
Analysis Date: {analysis_results.get('analysis_date', 'N/A')}
Total Samples: {analysis_results.get('total_samples', 0)}

JORC COMPLIANCE SUMMARY:
{analysis_results.get('compliance', {}).get('jorc_statement', 'Compliance analysis not available.')}

STANDARDS ANALYSIS: {'PASS' if standards.get('overall_acceptable', False) else 'FAIL'}
- Bias Detection: {'YES' if standards.get('bias', {}).get('bias_detected', False) else 'NO'}
- Recovery: {standards.get('recovery', {}).get('mean_recovery', 0):.1f}%
- Precision (RSD): {standards.get('precision', {}).get('rsd', 0):.1f}%

BLANKS ANALYSIS: {'PASS' if blanks.get('overall_acceptable', False) else 'FAIL'}
- Contamination Rate: {blanks.get('contamination', {}).get('contamination_rate', 0) * 100:.1f}%
- MDL: {blanks.get('mdl', 0):.3f}
- Carry-over: {'DETECTED' if blanks.get('carryover', {}).get('carryover_detected', False) else 'NONE'}

DUPLICATES ANALYSIS: {'PASS' if duplicates.get('overall_acceptable', False) else 'FAIL'}
- Mean RPD: {duplicates.get('precision', {}).get('mean_rpd', 0):.1f}%
- Systematic Error: {'YES' if duplicates.get('systematic_errors', {}).get('systematic_error', False) else 'NO'}
- Nugget Ratio: {duplicates.get('nugget_ratio', 0):.3f}

RECOMMENDATIONS:
{self._generate_recommendations(analysis_results)}
"""
        return summary.strip()

    def _generate_recommendations(self, analysis_results: dict) -> str:
        """Generate recommendations based on analysis results."""
        recommendations = []

        standards = analysis_results.get('standards', {})
        blanks = analysis_results.get('blanks', {})
        duplicates = analysis_results.get('duplicates', {})

        # Standards recommendations
        if standards.get('bias', {}).get('bias_detected', False):
            recommendations.append("- Investigate and correct systematic bias in standards analysis")

        if not standards.get('recovery', {}).get('acceptable', True):
            recommendations.append("- Review recovery procedures and calibration")

        if not standards.get('precision', {}).get('acceptable', True):
            recommendations.append("- Improve precision through better sample preparation and analysis")

        # Blanks recommendations
        if not blanks.get('contamination', {}).get('acceptable', True):
            recommendations.append("- Investigate contamination sources in blank samples")

        if blanks.get('carryover', {}).get('carryover_detected', False):
            recommendations.append("- Implement additional rinsing between samples")

        if not blanks.get('background', {}).get('acceptable', True):
            recommendations.append("- Review background levels and method detection limits")

        # Duplicates recommendations
        if not duplicates.get('precision', {}).get('acceptable', True):
            recommendations.append("- Improve duplicate precision through better homogenization")

        if duplicates.get('systematic_errors', {}).get('systematic_error', False):
            recommendations.append("- Investigate systematic errors in duplicate analysis")

        if duplicates.get('nugget_ratio', 0) > 0.3:
            recommendations.append("- Consider spatial sampling strategy improvements")

        if not recommendations:
            recommendations.append("- All QAQC parameters are within acceptable limits")

        return "\n".join(recommendations)

    def create_detailed_section(self, section_name: str, results: dict) -> str:
        """
        Create detailed analysis section.

        Args:
            section_name: Name of the section
            results: Analysis results dictionary

        Returns:
            Formatted section text
        """
        section = f"""
{section_name.upper()}
{'=' * len(section_name)}

"""

        if section_name.lower() == 'standards':
            bias = results.get('bias', {})
            recovery = results.get('recovery', {})
            precision = results.get('precision', {})

            section += f"""BIAS ANALYSIS:
- Bias Detected: {'YES' if bias.get('bias_detected', False) else 'NO'}
- Systematic Bias: {'YES' if bias.get('systematic_bias', False) else 'NO'}
- Max Z-Score: {bias.get('max_z_score', 0):.3f}
- Mean Z-Score: {bias.get('mean_z_score', 0):.3f}

RECOVERY ANALYSIS:
- Recovery Acceptable: {'YES' if recovery.get('acceptable', False) else 'NO'}
- Mean Recovery: {recovery.get('mean_recovery', 0):.2f}%
- Recovery Limits: {recovery.get('limits', (0, 0))}

PRECISION ANALYSIS:
- Precision Acceptable: {'YES' if precision.get('acceptable', False) else 'NO'}
- RSD: {precision.get('rsd', 0):.2f}%
- CV: {precision.get('cv', 0):.3f}
- Standard Deviation: {precision.get('std_dev', 0):.3f}
"""

        elif section_name.lower() == 'blanks':
            contamination = results.get('contamination', {})
            carryover = results.get('carryover', {})
            background = results.get('background', {})

            section += f"""CONTAMINATION ANALYSIS:
- Contamination Acceptable: {'YES' if contamination.get('acceptable', False) else 'NO'}
- Contamination Rate: {contamination.get('contamination_rate', 0) * 100:.2f}%
- MDL: {contamination.get('mdl', 0):.3f}
- Threshold: {contamination.get('threshold', 0):.3f}

CARRY-OVER ANALYSIS:
- Carry-over Detected: {'YES' if carryover.get('carryover_detected', False) else 'NO'}
- Trend: {carryover.get('trend', 0):.3f}

BACKGROUND ANALYSIS:
- Background Acceptable: {'YES' if background.get('acceptable', False) else 'NO'}
- Mean: {background.get('mean', 0):.3f}
- Standard Deviation: {background.get('std_dev', 0):.3f}
- CV: {background.get('cv', 0):.2f}%
"""

        elif section_name.lower() == 'duplicates':
            precision = results.get('precision', {})
            systematic = results.get('systematic_errors', {})

            section += f"""PRECISION ANALYSIS:
- Precision Acceptable: {'YES' if precision.get('acceptable', False) else 'NO'}
- Mean RPD: {precision.get('mean_rpd', 0):.2f}%
- Max RPD: {precision.get('max_rpd', 0):.2f}%
- Threshold: {precision.get('threshold', 0):.2f}%

SYSTEMATIC ERROR ANALYSIS:
- Systematic Error: {'YES' if systematic.get('systematic_error', False) else 'NO'}
- Mean Bias: {systematic.get('bias', 0):.3f}

SPATIAL ANALYSIS:
- Nugget Ratio: {results.get('nugget_ratio', 0):.3f}
"""

        return section.strip()

    def create_jorc_table1_section(self, analysis_results: dict) -> str:
        """
        Create JORC Table 1 helper section.

        Args:
            analysis_results: Dictionary with all analysis results

        Returns:
            Formatted JORC Table 1 text
        """
        compliance = analysis_results.get('compliance', {})
        jorc_statement = compliance.get('jorc_statement', 'N/A')
        
        standards = analysis_results.get('standards', {})
        blanks = analysis_results.get('blanks', {})
        duplicates = analysis_results.get('duplicates', {})

        section = f"""
JORC TABLE 1 - SECTION 1 (SAMPLING TECHNIQUES AND DATA)
=======================================================

The following text is generated to assist the Competent Person in completing JORC Table 1.
Please review and edit as necessary to ensure it accurately reflects the project's specific procedures.

Criteria: Quality of assay data and laboratory tests
----------------------------------------------------
"Nature of quality control procedures adopted (e.g. standards, blanks, duplicates, external laboratory checks) and whether acceptable levels of accuracy (i.e. lack of bias) and precision have been established."

SUGGESTED TEXT:
{jorc_statement}

Standards Analysis:
Analysis of Certified Reference Materials (CRMs) indicates that accuracy is {'acceptable' if standards.get('overall_acceptable') else 'outside of tolerance'}.
- Bias: {'No significant bias detected' if not standards.get('bias', {}).get('bias_detected') else 'Bias detected in some standards'}.
- Precision: {'Acceptable' if standards.get('precision', {}).get('acceptable') else 'Low precision observed'}.

Blanks Analysis:
Analysis of blank samples indicates that contamination is {'minimal' if blanks.get('overall_acceptable') else 'present'}.
- Contamination Rate: {blanks.get('contamination', {}).get('contamination_rate', 0) * 100:.1f}% of blanks returned values > 3x MDL.

Duplicates Analysis:
Analysis of duplicate samples indicates that precision is {'acceptable' if duplicates.get('overall_acceptable') else 'poor'}.
- Sampling/Analytical Precision: Mean RPD of {duplicates.get('precision', {}).get('mean_rpd', 0):.1f}%.

Criteria: Verification of sampling and assaying
-----------------------------------------------
"The verification of significant intersections by either independent or alternative personnel."

SUGGESTED TEXT:
Significant intersections have been verified by internal QAQC procedures.
No independent verification has been performed at this stage (modify if incorrect).
"""
        return section.strip()

    def generate_pdf_report(self, analysis_results: dict, plots: dict = None, filename: str = None) -> str:
        """
        Generate complete PDF report.

        Args:
            analysis_results: Dictionary with all analysis results
            plots: Dictionary with plot data (optional)
            filename: Output filename (optional)

        Returns:
            Path to generated PDF file
        """
        from datetime import datetime
        import os

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"qaqc_report_{timestamp}.pdf"

        # Ensure output directory exists
        output_dir = os.path.dirname(filename) or "."
        os.makedirs(output_dir, exist_ok=True)

        # Create report content
        report_content = self._build_report_content(analysis_results, plots)

        # Write to file (simplified - in production would use reportlab)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return filename

    def _build_report_content(self, analysis_results: dict, plots: dict = None) -> str:
        """Build complete report content."""
        from datetime import datetime
        content = []

        # Title page
        content.append("QAQC ANALYSIS REPORT")
        content.append("=" * 50)
        content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")

        # Executive summary
        content.append(self.create_executive_summary(analysis_results))
        content.append("")
        content.append("")

        # Detailed sections
        if 'standards' in analysis_results:
            content.append(self.create_detailed_section('Standards', analysis_results['standards']))
            content.append("")
            content.append("")

        if 'blanks' in analysis_results:
            content.append(self.create_detailed_section('Blanks', analysis_results['blanks']))
            content.append("")
            content.append("")

        if 'duplicates' in analysis_results:
            content.append(self.create_detailed_section('Duplicates', analysis_results['duplicates']))
            content.append("")
            content.append("")

            content.append("")
            content.append("")

        # JORC Table 1 Helper
        content.append(self.create_jorc_table1_section(analysis_results))
        content.append("")
        content.append("")

        # Appendices
        content.append("APPENDICES")
        content.append("=" * 20)
        content.append("")

        if plots:
            content.append("PLOTS:")
            for plot_name, plot_data in plots.items():
                content.append(f"- {plot_name}: {plot_data.get('description', 'N/A')}")
            content.append("")

        # Raw data summary
        if 'total_samples' in analysis_results:
            content.append("DATA SUMMARY:")
            content.append(f"- Total Samples: {analysis_results['total_samples']}")
            content.append(f"- Standards: {analysis_results.get('standards', {}).get('summary', {}).get('n_measurements', 0)}")
            content.append(f"- Blanks: {analysis_results.get('blanks', {}).get('summary', {}).get('n_blanks', 0)}")
            content.append(f"- Duplicates: {analysis_results.get('duplicates', {}).get('summary', {}).get('n_duplicates', 0)}")

        return "\n".join(content)
