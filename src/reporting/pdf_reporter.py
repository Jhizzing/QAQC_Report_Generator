"""
Professional PDF Report Generator using ReportLab

Generates JORC-compliant QAQC analysis reports with:
- Cover page with branding
- Executive summary with pass/fail badges
- Detailed analysis sections with tables
- Embedded Matplotlib plots
- JORC Table 1 helper text
"""

import os
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Any

# ReportLab imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie


class QAQCPDFReporter:
    """
    Professional PDF report generator for QAQC analysis results.
    
    Uses ReportLab to create properly formatted PDF documents with
    embedded charts, tables, and professional styling.
    """
    
    # Color scheme
    COLORS = {
        'primary': colors.HexColor('#F59E0B'),      # Amber/Gold
        'primary_dark': colors.HexColor('#D97706'),
        'success': colors.HexColor('#10B981'),       # Green
        'error': colors.HexColor('#EF4444'),         # Red
        'warning': colors.HexColor('#F59E0B'),       # Amber
        'text_dark': colors.HexColor('#1E293B'),     # Slate 800
        'text_light': colors.HexColor('#64748B'),    # Slate 500
        'bg_light': colors.HexColor('#F8FAFC'),      # Slate 50
        'border': colors.HexColor('#E2E8F0'),        # Slate 200
    }
    
    def __init__(self, config: Dict = None) -> None:
        """
        Initialize PDF reporter with configuration.
        
        Args:
            config: Dictionary with report settings
        """
        self.config = config or {}
        self.page_size = self._normalize_page_size(self.config.get('page_size', A4))
        default_margins = {
            'top': 0.75 * inch,
            'bottom': 0.75 * inch,
            'left': 0.75 * inch,
            'right': 0.75 * inch
        }
        self.margins = self._normalize_margins(self.config.get('margins', default_margins), default_margins)
        self.include_plots = self.config.get('include_plots', True)
        
        # Initialize styles
        self._init_styles()

    @staticmethod
    def _normalize_page_size(page_size: Any):
        """Normalize page size from config string or tuple."""
        if isinstance(page_size, str):
            normalized = page_size.strip().upper()
            if normalized == "A4":
                return A4
            if normalized in {"LETTER", "US_LETTER", "US-LETTER"}:
                return letter
            return A4

        if isinstance(page_size, (list, tuple)) and len(page_size) == 2:
            return tuple(page_size)

        return page_size

    @staticmethod
    def _margin_to_points(value: Any) -> float:
        """
        Convert margin value to PDF points.

        Backward compatibility:
        - small numeric values (<= 10) are treated as inches
        - larger numeric values are treated as points
        """
        if isinstance(value, (int, float)):
            return float(value) * inch if value <= 10 else float(value)
        return float(value)

    def _normalize_margins(self, margins: Any, default_margins: Dict[str, float]) -> Dict[str, float]:
        """Accept either dict margins or legacy [top, bottom, left, right] lists."""
        if isinstance(margins, dict):
            return {
                key: self._margin_to_points(margins.get(key, default_margins[key]))
                for key in ('top', 'bottom', 'left', 'right')
            }

        if isinstance(margins, (list, tuple)) and len(margins) == 4:
            top, bottom, left, right = margins
            return {
                'top': self._margin_to_points(top),
                'bottom': self._margin_to_points(bottom),
                'left': self._margin_to_points(left),
                'right': self._margin_to_points(right),
            }

        return default_margins
    
    def _init_styles(self) -> None:
        """Initialize custom paragraph styles."""
        self.styles = getSampleStyleSheet()
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            spaceAfter=6,
            textColor=self.COLORS['text_dark'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=30,
            textColor=self.COLORS['text_light'],
            alignment=TA_CENTER
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=self.COLORS['primary_dark'],
            fontName='Helvetica-Bold',
            borderPadding=(0, 0, 5, 0)
        ))
        
        # Subsection heading
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=8,
            textColor=self.COLORS['text_dark'],
            fontName='Helvetica-Bold'
        ))
        
        # Body text (use unique name to avoid conflict)
        self.styles.add(ParagraphStyle(
            name='QAQCBodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=self.COLORS['text_dark'],
            alignment=TA_JUSTIFY,
            leading=14
        ))
        
        # Status pass
        self.styles.add(ParagraphStyle(
            name='StatusPass',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.white,
            backColor=self.COLORS['success'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Status fail
        self.styles.add(ParagraphStyle(
            name='StatusFail',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.white,
            backColor=self.COLORS['error'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Metric label
        self.styles.add(ParagraphStyle(
            name='MetricLabel',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.COLORS['text_light'],
            alignment=TA_LEFT
        ))
        
        # Metric value
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.COLORS['text_dark'],
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        # JORC text
        self.styles.add(ParagraphStyle(
            name='JORCText',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.COLORS['text_dark'],
            alignment=TA_JUSTIFY,
            leading=12,
            leftIndent=20,
            rightIndent=20
        ))
        
        # Footer
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=self.COLORS['text_light'],
            alignment=TA_CENTER
        ))
    
    def _create_status_badge(self, status: bool) -> Table:
        """Create a colored status badge."""
        text = "PASS" if status else "FAIL"
        color = self.COLORS['success'] if status else self.COLORS['error']
        
        data = [[text]]
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ])
        
        table = Table(data, colWidths=[80])
        table.setStyle(style)
        return table
    
    def _create_metric_table(self, metrics: List[Dict]) -> Table:
        """
        Create a styled metrics table.
        
        Args:
            metrics: List of dicts with 'label', 'value', and optional 'status'
        """
        data = []
        for metric in metrics:
            label = Paragraph(metric['label'], self.styles['MetricLabel'])
            
            # Color value based on status if provided
            value_text = str(metric['value'])
            if metric.get('status') == 'pass':
                value_text = f'<font color="#{self.COLORS["success"].hexval()[2:]}">{value_text}</font>'
            elif metric.get('status') == 'fail':
                value_text = f'<font color="#{self.COLORS["error"].hexval()[2:]}">{value_text}</font>'
            
            value = Paragraph(value_text, self.styles['MetricValue'])
            data.append([label, value])
        
        table = Table(data, colWidths=[2.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, self.COLORS['border']),
        ]))
        
        return table
    
    def _create_statistics_table(self, headers: List[str], rows: List[List]) -> Table:
        """Create a styled statistics table with headers."""
        # Header row
        header_row = [Paragraph(f'<b>{h}</b>', self.styles['Normal']) for h in headers]
        data = [header_row] + rows
        
        # Calculate column widths
        col_count = len(headers)
        col_width = (self.page_size[0] - 2 * inch) / col_count
        
        table = Table(data, colWidths=[col_width] * col_count)
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Body styling
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Borders and padding
            ('GRID', (0, 0), (-1, -1), 0.5, self.COLORS['border']),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.COLORS['bg_light']]),
        ]))
        
        return table
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to each page."""
        canvas.saveState()
        
        # Footer
        footer_text = f"QAQC Analysis Report | Generated {datetime.now().strftime('%Y-%m-%d')} | Page {doc.page}"
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(self.COLORS['text_light'])
        canvas.drawCentredString(
            self.page_size[0] / 2,
            0.5 * inch,
            footer_text
        )
        
        # Header line
        canvas.setStrokeColor(self.COLORS['primary'])
        canvas.setLineWidth(2)
        canvas.line(
            0.75 * inch,
            self.page_size[1] - 0.5 * inch,
            self.page_size[0] - 0.75 * inch,
            self.page_size[1] - 0.5 * inch
        )
        
        canvas.restoreState()
    
    def build_cover_page(self, project_info: Dict) -> List:
        """
        Build cover page elements.
        
        Args:
            project_info: Dictionary with project metadata
        """
        elements = []
        
        # Add vertical space
        elements.append(Spacer(1, 2 * inch))
        
        # Title
        elements.append(Paragraph("QAQC ANALYSIS REPORT", self.styles['ReportTitle']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Subtitle with project info
        project_name = project_info.get('name', 'Untitled Project')
        deposit = project_info.get('deposit', '')
        subtitle = f"{project_name}"
        if deposit:
            subtitle += f" | {deposit}"
        elements.append(Paragraph(subtitle, self.styles['ReportSubtitle']))
        
        # Horizontal rule
        elements.append(HRFlowable(
            width="60%",
            thickness=2,
            color=self.COLORS['primary'],
            spaceBefore=20,
            spaceAfter=30
        ))
        
        # Project details table
        details = [
            ['Commodity:', project_info.get('commodity', 'N/A')],
            ['Analysis Date:', datetime.now().strftime('%B %d, %Y')],
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M')],
        ]
        
        if project_info.get('laboratory'):
            details.append(['Laboratory:', project_info['laboratory']])
        if project_info.get('competent_person'):
            details.append(['Competent Person:', project_info['competent_person']])
        
        details_table = Table(details, colWidths=[1.5 * inch, 3 * inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.COLORS['text_dark']),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(details_table)
        
        # Page break after cover
        elements.append(PageBreak())
        
        return elements
    
    def build_executive_summary(self, analysis_results: Dict) -> List:
        """Build executive summary section."""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeading']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.COLORS['border']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Get overall status
        standards = analysis_results.get('standards', {})
        blanks = analysis_results.get('blanks', {})
        duplicates = analysis_results.get('duplicates', {})
        
        overall_pass = all([
            standards.get('overall_acceptable', True),
            blanks.get('overall_acceptable', True),
            duplicates.get('overall_acceptable', True)
        ])
        
        # Overall status badge
        status_text = "OVERALL QAQC STATUS"
        elements.append(Paragraph(status_text, self.styles['SubsectionHeading']))
        elements.append(self._create_status_badge(overall_pass))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Summary metrics in a table
        summary_data = [
            ['Analysis Component', 'Status', 'Key Metric', 'Value'],
            [
                'Standards (CRMs)',
                'PASS' if standards.get('overall_acceptable', True) else 'FAIL',
                'Pass Rate',
                f"{standards.get('precision', {}).get('rsd', 0):.1f}%"
            ],
            [
                'Blanks',
                'PASS' if blanks.get('overall_acceptable', True) else 'FAIL',
                'Contamination Rate',
                f"{blanks.get('contamination', {}).get('contamination_rate', 0) * 100:.1f}%"
            ],
            [
                'Duplicates',
                'PASS' if duplicates.get('overall_acceptable', True) else 'FAIL',
                'Mean RPD',
                f"{duplicates.get('precision', {}).get('mean_rpd', 0):.1f}%"
            ],
        ]
        
        summary_table = Table(summary_data, colWidths=[2 * inch, 1 * inch, 1.5 * inch, 1 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, self.COLORS['border']),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.COLORS['bg_light']]),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Recommendations
        elements.append(Paragraph("RECOMMENDATIONS", self.styles['SubsectionHeading']))
        recommendations = self._generate_recommendations(analysis_results)
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", self.styles['QAQCBodyText']))
        
        elements.append(PageBreak())
        return elements
    
    def _generate_recommendations(self, analysis_results: Dict) -> List[str]:
        """Generate recommendations based on analysis results."""
        recommendations = []
        
        standards = analysis_results.get('standards', {})
        blanks = analysis_results.get('blanks', {})
        duplicates = analysis_results.get('duplicates', {})
        
        if standards.get('bias', {}).get('bias_detected', False):
            recommendations.append("Investigate and correct systematic bias in standards analysis")
        
        if not blanks.get('contamination', {}).get('acceptable', True):
            recommendations.append("Investigate contamination sources in blank samples")
        
        if blanks.get('carryover', {}).get('carryover_detected', False):
            recommendations.append("Implement additional rinsing between samples to reduce carry-over")
        
        if not duplicates.get('precision', {}).get('acceptable', True):
            recommendations.append("Improve duplicate precision through better homogenization")
        
        if duplicates.get('nugget_ratio', 0) > 0.3:
            recommendations.append("Consider spatial sampling strategy improvements due to high nugget ratio")
        
        if not recommendations:
            recommendations.append("All QAQC parameters are within acceptable limits. Continue current protocols.")
        
        return recommendations
    
    def build_standards_section(self, standards_results: Dict, plot_path: str = None) -> List:
        """Build standards analysis section."""
        elements = []
        
        elements.append(Paragraph("STANDARDS ANALYSIS", self.styles['SectionHeading']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.COLORS['border']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Description
        elements.append(Paragraph(
            "Certified Reference Materials (CRMs) are used to assess analytical accuracy and detect bias. "
            "The following results show the performance of standards against certified values.",
            self.styles['QAQCBodyText']
        ))
        elements.append(Spacer(1, 0.15 * inch))
        
        # Status badge
        elements.append(self._create_status_badge(standards_results.get('overall_acceptable', True)))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Metrics
        bias = standards_results.get('bias', {})
        recovery = standards_results.get('recovery', {})
        precision = standards_results.get('precision', {})
        
        metrics = [
            {'label': 'Bias Detected', 'value': 'Yes' if bias.get('bias_detected', False) else 'No',
             'status': 'fail' if bias.get('bias_detected', False) else 'pass'},
            {'label': 'Max Z-Score', 'value': f"{bias.get('max_z_score', 0):.2f}"},
            {'label': 'Mean Recovery', 'value': f"{recovery.get('mean_recovery', 100):.1f}%",
             'status': 'pass' if recovery.get('acceptable', True) else 'fail'},
            {'label': 'Precision (RSD)', 'value': f"{precision.get('rsd', 0):.2f}%",
             'status': 'pass' if precision.get('acceptable', True) else 'fail'},
        ]
        elements.append(self._create_metric_table(metrics))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Embedded plot if provided
        if plot_path and os.path.exists(plot_path):
            elements.append(Paragraph("Control Chart", self.styles['SubsectionHeading']))
            img = Image(plot_path, width=5.5 * inch, height=3.5 * inch)
            elements.append(img)
        
        elements.append(PageBreak())
        return elements
    
    def build_blanks_section(self, blanks_results: Dict, plot_path: str = None) -> List:
        """Build blanks analysis section."""
        elements = []
        
        elements.append(Paragraph("BLANKS ANALYSIS", self.styles['SectionHeading']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.COLORS['border']))
        elements.append(Spacer(1, 0.2 * inch))
        
        elements.append(Paragraph(
            "Blank samples are analyzed to detect contamination and assess background levels. "
            "Contamination is flagged when blank values exceed the detection limit multiplied by a threshold factor.",
            self.styles['QAQCBodyText']
        ))
        elements.append(Spacer(1, 0.15 * inch))
        
        # Status badge
        elements.append(self._create_status_badge(blanks_results.get('overall_acceptable', True)))
        elements.append(Spacer(1, 0.2 * inch))
        
        contamination = blanks_results.get('contamination', {})
        carryover = blanks_results.get('carryover', {})
        background = blanks_results.get('background', {})
        
        metrics = [
            {'label': 'Contamination Rate', 'value': f"{contamination.get('contamination_rate', 0) * 100:.1f}%",
             'status': 'pass' if contamination.get('acceptable', True) else 'fail'},
            {'label': 'Method Detection Limit', 'value': f"{blanks_results.get('mdl', 0):.4f}"},
            {'label': 'Carry-over Detected', 'value': 'Yes' if carryover.get('carryover_detected', False) else 'No',
             'status': 'fail' if carryover.get('carryover_detected', False) else 'pass'},
            {'label': 'Background Mean', 'value': f"{background.get('mean', 0):.4f}"},
        ]
        elements.append(self._create_metric_table(metrics))
        elements.append(Spacer(1, 0.3 * inch))
        
        if plot_path and os.path.exists(plot_path):
            elements.append(Paragraph("Blanks Distribution", self.styles['SubsectionHeading']))
            img = Image(plot_path, width=5.5 * inch, height=3.5 * inch)
            elements.append(img)
        
        elements.append(PageBreak())
        return elements
    
    def build_duplicates_section(self, duplicates_results: Dict, plot_path: str = None) -> List:
        """Build duplicates analysis section."""
        elements = []
        
        elements.append(Paragraph("DUPLICATES ANALYSIS", self.styles['SectionHeading']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.COLORS['border']))
        elements.append(Spacer(1, 0.2 * inch))
        
        elements.append(Paragraph(
            "Duplicate samples assess analytical and sampling precision. Results are evaluated using "
            "Relative Percent Difference (RPD) and Half Absolute Relative Difference (HARD) metrics.",
            self.styles['QAQCBodyText']
        ))
        elements.append(Spacer(1, 0.15 * inch))
        
        # Status badge
        elements.append(self._create_status_badge(duplicates_results.get('overall_acceptable', True)))
        elements.append(Spacer(1, 0.2 * inch))
        
        precision = duplicates_results.get('precision', {})
        systematic = duplicates_results.get('systematic_errors', {})
        
        metrics = [
            {'label': 'Mean RPD', 'value': f"{precision.get('mean_rpd', 0):.1f}%",
             'status': 'pass' if precision.get('acceptable', True) else 'fail'},
            {'label': 'Max RPD', 'value': f"{precision.get('max_rpd', 0):.1f}%"},
            {'label': 'Within Target', 'value': f"{precision.get('mean_rpd', 0) <= precision.get('threshold', 20)}"},
            {'label': 'Systematic Error', 'value': 'Yes' if systematic.get('systematic_error', False) else 'No',
             'status': 'fail' if systematic.get('systematic_error', False) else 'pass'},
            {'label': 'Nugget Ratio', 'value': f"{duplicates_results.get('nugget_ratio', 0):.3f}"},
        ]
        elements.append(self._create_metric_table(metrics))
        elements.append(Spacer(1, 0.3 * inch))
        
        if plot_path and os.path.exists(plot_path):
            elements.append(Paragraph("Duplicates Scatter Plot", self.styles['SubsectionHeading']))
            img = Image(plot_path, width=5.5 * inch, height=3.5 * inch)
            elements.append(img)
        
        elements.append(PageBreak())
        return elements
    
    def build_jorc_section(self, analysis_results: Dict) -> List:
        """Build JORC Table 1 helper section."""
        elements = []
        
        elements.append(Paragraph("JORC TABLE 1 HELPER", self.styles['SectionHeading']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.COLORS['border']))
        elements.append(Spacer(1, 0.2 * inch))
        
        elements.append(Paragraph(
            "<i>The following text is provided to assist the Competent Person in completing JORC Table 1, "
            "Section 1 (Sampling Techniques and Data). Please review and modify as appropriate.</i>",
            self.styles['QAQCBodyText']
        ))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Criteria: Quality of assay data
        elements.append(Paragraph(
            "<b>Criteria: Quality of assay data and laboratory tests</b>",
            self.styles['SubsectionHeading']
        ))
        elements.append(Paragraph(
            '"Nature of quality control procedures adopted (e.g. standards, blanks, duplicates, '
            'external laboratory checks) and whether acceptable levels of accuracy (i.e. lack of bias) '
            'and precision have been established."',
            self.styles['JORCText']
        ))
        elements.append(Spacer(1, 0.15 * inch))
        
        # Generate JORC text based on results
        standards = analysis_results.get('standards', {})
        blanks = analysis_results.get('blanks', {})
        duplicates = analysis_results.get('duplicates', {})
        
        jorc_text = self._generate_jorc_text(standards, blanks, duplicates)
        elements.append(Paragraph("<b>SUGGESTED TEXT:</b>", self.styles['QAQCBodyText']))
        elements.append(Paragraph(jorc_text, self.styles['JORCText']))
        
        return elements
    
    def _generate_jorc_text(self, standards: Dict, blanks: Dict, duplicates: Dict) -> str:
        """Generate JORC-compliant text based on analysis results."""
        standards_pass = standards.get('overall_acceptable', True)
        blanks_pass = blanks.get('overall_acceptable', True)
        duplicates_pass = duplicates.get('overall_acceptable', True)
        
        text = f"""
        A comprehensive QAQC program was implemented including certified reference materials (standards), 
        blank samples, and field duplicates. 
        
        <b>Standards:</b> Analysis of CRMs indicates that analytical accuracy is 
        {'acceptable with no significant bias detected' if standards_pass else 'outside acceptable limits, with bias detected'}. 
        Mean recovery is {standards.get('recovery', {}).get('mean_recovery', 100):.1f}%.
        
        <b>Blanks:</b> Blank sample analysis indicates that contamination is 
        {'minimal and within acceptable limits' if blanks_pass else 'present and requires investigation'}. 
        Contamination rate is {blanks.get('contamination', {}).get('contamination_rate', 0) * 100:.1f}%.
        
        <b>Duplicates:</b> Duplicate analysis indicates that sampling and analytical precision is 
        {'acceptable' if duplicates_pass else 'outside acceptable limits'}. 
        Mean RPD is {duplicates.get('precision', {}).get('mean_rpd', 0):.1f}%.
        
        {'Overall, acceptable levels of accuracy and precision have been established.' if all([standards_pass, blanks_pass, duplicates_pass]) else 'Further investigation is recommended to address identified issues.'}
        """
        return text.strip()
    
    def generate_pdf_report(
        self,
        analysis_results: Dict,
        project_info: Dict = None,
        plots: Dict = None,
        filename: str = None
    ) -> str:
        """
        Generate complete PDF report.
        
        Args:
            analysis_results: Dictionary with all analysis results
            project_info: Dictionary with project metadata
            plots: Dictionary with plot file paths
            filename: Output filename (optional)
            
        Returns:
            Path to generated PDF file
        """
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"qaqc_report_{timestamp}.pdf"
        
        # Ensure output directory exists
        output_dir = os.path.dirname(filename)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Create document
        doc = SimpleDocTemplate(
            filename,
            pagesize=self.page_size,
            topMargin=self.margins['top'],
            bottomMargin=self.margins['bottom'],
            leftMargin=self.margins['left'],
            rightMargin=self.margins['right']
        )
        
        # Build content
        elements = []
        
        # Cover page
        project_info = project_info or {}
        elements.extend(self.build_cover_page(project_info))
        
        # Executive summary
        elements.extend(self.build_executive_summary(analysis_results))
        
        # Detailed sections
        plots = plots or {}
        
        if 'standards' in analysis_results:
            elements.extend(self.build_standards_section(
                analysis_results['standards'],
                plots.get('standards')
            ))
        
        if 'blanks' in analysis_results:
            elements.extend(self.build_blanks_section(
                analysis_results['blanks'],
                plots.get('blanks')
            ))
        
        if 'duplicates' in analysis_results:
            elements.extend(self.build_duplicates_section(
                analysis_results['duplicates'],
                plots.get('duplicates')
            ))
        
        # JORC section
        elements.extend(self.build_jorc_section(analysis_results))
        
        # Build PDF
        doc.build(elements, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        return filename


# Backwards compatibility alias
PDFReporter = QAQCPDFReporter
