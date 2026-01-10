"""
Excel Reporter with Embedded Charts

Generates professional Excel reports with xlsxwriter charts embedded directly in worksheets.
Provides interactive visual QAQC analysis results with:
- Control charts on Standards sheet
- Scatter plots on Duplicates sheet  
- Summary dashboard with mini charts
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    import xlsxwriter
    from xlsxwriter.utility import xl_rowcol_to_cell
    XLSXWRITER_AVAILABLE = True
except ImportError:
    XLSXWRITER_AVAILABLE = False


class ExcelChartReporter:
    """
    Generates Excel reports with embedded xlsxwriter charts.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize with reporting configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        if not XLSXWRITER_AVAILABLE:
            raise ImportError("xlsxwriter is required for chart generation. Install with: pip install xlsxwriter")
        
        self.config = config or {}
        
    def generate_report(
        self,
        analysis_results: Dict[str, Any],
        project_info: Optional[Dict[str, str]] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Generate complete Excel report with charts.
        
        Args:
            analysis_results: QAQC analysis results
            project_info: Optional project metadata
            filename: Output filename
            
        Returns:
            Path to generated Excel file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"qaqc_report_{timestamp}.xlsx"
        
        # Ensure directory exists
        output_dir = os.path.dirname(filename)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Create workbook
        workbook = xlsxwriter.Workbook(filename)
        
        # Define formats
        formats = self._create_formats(workbook)
        
        # Create sheets
        self._create_dashboard_sheet(workbook, analysis_results, project_info, formats)
        self._create_standards_sheet(workbook, analysis_results.get('standards', {}), formats)
        self._create_blanks_sheet(workbook, analysis_results.get('blanks', {}), formats)
        self._create_duplicates_sheet(workbook, analysis_results.get('duplicates', {}), formats)
        
        workbook.close()
        
        return filename
    
    def _create_formats(self, workbook) -> Dict[str, Any]:
        """Create reusable cell formats."""
        return {
            'title': workbook.add_format({
                'bold': True, 'font_size': 16, 'font_color': '#1a1a2e',
                'bottom': 2, 'bottom_color': '#4a90d9'
            }),
            'header': workbook.add_format({
                'bold': True, 'bg_color': '#2c3e50', 'font_color': 'white',
                'border': 1, 'align': 'center', 'valign': 'vcenter'
            }),
            'data': workbook.add_format({
                'border': 1, 'align': 'center', 'valign': 'vcenter'
            }),
            'number': workbook.add_format({
                'border': 1, 'align': 'center', 'num_format': '0.000'
            }),
            'percent': workbook.add_format({
                'border': 1, 'align': 'center', 'num_format': '0.00%'
            }),
            'pass': workbook.add_format({
                'bold': True, 'bg_color': '#27ae60', 'font_color': 'white',
                'border': 1, 'align': 'center'
            }),
            'fail': workbook.add_format({
                'bold': True, 'bg_color': '#e74c3c', 'font_color': 'white',
                'border': 1, 'align': 'center'
            }),
            'warning': workbook.add_format({
                'bold': True, 'bg_color': '#f39c12', 'font_color': 'white',
                'border': 1, 'align': 'center'
            }),
            'section': workbook.add_format({
                'bold': True, 'font_size': 12, 'bg_color': '#ecf0f1',
                'border': 1
            }),
        }
    
    def _create_dashboard_sheet(
        self, 
        workbook, 
        results: Dict, 
        project_info: Optional[Dict],
        formats: Dict
    ):
        """Create summary dashboard with mini charts."""
        sheet = workbook.add_worksheet('Dashboard')
        sheet.set_column('A:A', 30)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:H', 12)
        
        # Title
        project_name = project_info.get('name', 'QAQC Analysis') if project_info else 'QAQC Analysis'
        sheet.write('A1', f'{project_name} - Summary Dashboard', formats['title'])
        sheet.write('A2', f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        
        # Summary statistics
        row = 4
        sheet.write(row, 0, 'Analysis Summary', formats['section'])
        sheet.write(row, 1, 'Value', formats['section'])
        sheet.write(row, 2, 'Status', formats['section'])
        
        summary = results.get('summary', {})
        stats = [
            ('Total Samples', summary.get('total_samples', 0), None),
            ('Standards', summary.get('total_standards', 0), None),
            ('Blanks', summary.get('total_blanks', 0), None),
            ('Duplicates', summary.get('total_duplicates', 0), None),
            ('Overall Pass Rate', f"{summary.get('overall_pass_rate', 0):.1f}%", 
             summary.get('overall_pass_rate', 0) >= 90),
        ]
        
        for i, (metric, value, is_pass) in enumerate(stats):
            row += 1
            sheet.write(row, 0, metric, formats['data'])
            sheet.write(row, 1, value, formats['data'])
            if is_pass is not None:
                status_fmt = formats['pass'] if is_pass else formats['fail']
                sheet.write(row, 2, 'PASS' if is_pass else 'FAIL', status_fmt)
        
        # Mini chart data for pass rates
        row += 3
        sheet.write(row, 0, 'Module Performance', formats['section'])
        row += 1
        
        # Write chart data
        modules = ['Standards', 'Blanks', 'Duplicates']
        standards_stats = results.get('standards', {}).get('statistics', [{}])[0] if results.get('standards', {}).get('statistics') else {}
        blanks_stats = results.get('blanks', {}).get('statistics', [{}])[0] if results.get('blanks', {}).get('statistics') else {}
        dup_stats = results.get('duplicates', {}).get('statistics', [{}])[0] if results.get('duplicates', {}).get('statistics') else {}
        
        pass_rates = [
            standards_stats.get('pass_rate', 0),
            100 - blanks_stats.get('contamination_rate', 0),
            dup_stats.get('within_target', 0),
        ]
        
        sheet.write(row, 0, 'Module', formats['header'])
        sheet.write(row, 1, 'Pass Rate (%)', formats['header'])
        
        data_start_row = row + 1
        for i, (module, rate) in enumerate(zip(modules, pass_rates)):
            sheet.write(row + 1 + i, 0, module, formats['data'])
            sheet.write(row + 1 + i, 1, rate, formats['number'])
        data_end_row = row + len(modules)
        
        # Create bar chart for pass rates
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': 'Pass Rate',
            'categories': f"='Dashboard'!$A${data_start_row + 1}:$A${data_end_row + 1}",
            'values': f"='Dashboard'!$B${data_start_row + 1}:$B${data_end_row + 1}",
            'fill': {'color': '#4a90d9'},
            'border': {'color': '#2c3e50'},
        })
        chart.set_title({'name': 'QAQC Module Performance'})
        chart.set_y_axis({'min': 0, 'max': 100, 'name': 'Pass Rate (%)'})
        chart.set_x_axis({'name': 'Module'})
        chart.set_legend({'none': True})
        chart.set_size({'width': 400, 'height': 300})
        
        sheet.insert_chart('D4', chart)
        
    def _create_standards_sheet(self, workbook, standards: Dict, formats: Dict):
        """Create Standards sheet with control chart."""
        sheet = workbook.add_worksheet('Standards')
        sheet.set_column('A:A', 15)
        sheet.set_column('B:D', 12)
        
        sheet.write('A1', 'Standards Analysis', formats['title'])
        
        # Statistics table
        row = 3
        headers = ['Element', 'Mean', 'SD', 'RSD (%)', 'Pass Rate (%)', 'Count']
        for col, header in enumerate(headers):
            sheet.write(row, col, header, formats['header'])
        
        statistics = standards.get('statistics', [])
        for i, stat in enumerate(statistics):
            row += 1
            sheet.write(row, 0, stat.get('element', 'Au'), formats['data'])
            sheet.write(row, 1, stat.get('mean', 0), formats['number'])
            sheet.write(row, 2, stat.get('sd', 0), formats['number'])
            sheet.write(row, 3, stat.get('rsd', 0), formats['number'])
            
            pass_rate = stat.get('pass_rate', 0)
            pass_fmt = formats['pass'] if pass_rate >= 90 else formats['warning'] if pass_rate >= 80 else formats['fail']
            sheet.write(row, 4, pass_rate, pass_fmt)
            sheet.write(row, 5, stat.get('count', 0), formats['data'])
        
        # Control chart data
        data_points = standards.get('data_points', [])
        if data_points:
            chart_start_row = row + 3
            sheet.write(chart_start_row, 0, 'Sequence', formats['header'])
            sheet.write(chart_start_row, 1, 'Value', formats['header'])
            sheet.write(chart_start_row, 2, 'Status', formats['header'])
            
            for i, dp in enumerate(data_points[:50]):  # Limit to 50 points
                sheet.write(chart_start_row + 1 + i, 0, dp.get('sequence', i), formats['data'])
                sheet.write(chart_start_row + 1 + i, 1, dp.get('value', 0), formats['number'])
                status = dp.get('status', 'PASS')
                status_fmt = formats['pass'] if status == 'PASS' else formats['fail']
                sheet.write(chart_start_row + 1 + i, 2, status, status_fmt)
            
            # Create control chart
            if len(data_points) >= 3:
                chart = workbook.add_chart({'type': 'line'})
                
                data_end_row = chart_start_row + min(len(data_points), 50)
                
                chart.add_series({
                    'name': 'Measured Value',
                    'categories': f"='Standards'!$A${chart_start_row + 2}:$A${data_end_row + 1}",
                    'values': f"='Standards'!$B${chart_start_row + 2}:$B${data_end_row + 1}",
                    'marker': {'type': 'circle', 'size': 6, 'fill': {'color': '#4a90d9'}},
                    'line': {'color': '#4a90d9', 'width': 1.5},
                })
                
                chart.set_title({'name': 'Standards Control Chart'})
                chart.set_x_axis({'name': 'Sequence Number'})
                chart.set_y_axis({'name': 'Measured Value'})
                chart.set_size({'width': 600, 'height': 350})
                chart.set_legend({'position': 'bottom'})
                
                sheet.insert_chart('E3', chart)
    
    def _create_blanks_sheet(self, workbook, blanks: Dict, formats: Dict):
        """Create Blanks sheet with contamination chart."""
        sheet = workbook.add_worksheet('Blanks')
        sheet.set_column('A:A', 15)
        sheet.set_column('B:E', 12)
        
        sheet.write('A1', 'Blanks Analysis', formats['title'])
        
        # Statistics table
        row = 3
        headers = ['Element', 'Max', 'Mean', 'Median', 'Contamination Rate (%)', 'Count']
        for col, header in enumerate(headers):
            sheet.write(row, col, header, formats['header'])
        
        statistics = blanks.get('statistics', [])
        for i, stat in enumerate(statistics):
            row += 1
            sheet.write(row, 0, stat.get('element', 'Au'), formats['data'])
            sheet.write(row, 1, stat.get('max', 0), formats['number'])
            sheet.write(row, 2, stat.get('mean', 0), formats['number'])
            sheet.write(row, 3, stat.get('median', 0), formats['number'])
            
            cont_rate = stat.get('contamination_rate', 0)
            cont_fmt = formats['pass'] if cont_rate <= 5 else formats['warning'] if cont_rate <= 10 else formats['fail']
            sheet.write(row, 4, cont_rate, cont_fmt)
            sheet.write(row, 5, stat.get('count', 0), formats['data'])
        
        # Flagged blanks table
        flagged = blanks.get('flagged_blanks', [])
        if flagged:
            row += 3
            sheet.write(row, 0, 'Flagged Blanks', formats['section'])
            row += 1
            
            headers = ['Sample ID', 'Value', 'Threshold', 'Issue']
            for col, header in enumerate(headers):
                sheet.write(row, col, header, formats['header'])
            
            for fb in flagged[:20]:  # Limit to 20
                row += 1
                sheet.write(row, 0, fb.get('sample_id', ''), formats['data'])
                sheet.write(row, 1, fb.get('value', 0), formats['number'])
                sheet.write(row, 2, fb.get('threshold', 0), formats['number'])
                sheet.write(row, 3, fb.get('issue', 'Contamination'), formats['fail'])
    
    def _create_duplicates_sheet(self, workbook, duplicates: Dict, formats: Dict):
        """Create Duplicates sheet with scatter chart."""
        sheet = workbook.add_worksheet('Duplicates')
        sheet.set_column('A:A', 15)
        sheet.set_column('B:E', 12)
        
        sheet.write('A1', 'Duplicates Analysis', formats['title'])
        
        # Statistics table
        row = 3
        headers = ['Element', 'Mean RPD (%)', 'Within Target (%)', 'Count']
        for col, header in enumerate(headers):
            sheet.write(row, col, header, formats['header'])
        
        statistics = duplicates.get('statistics', [])
        for i, stat in enumerate(statistics):
            row += 1
            sheet.write(row, 0, stat.get('element', 'Au'), formats['data'])
            sheet.write(row, 1, stat.get('mean_rpd', 0), formats['number'])
            
            within = stat.get('within_target', 0)
            within_fmt = formats['pass'] if within >= 90 else formats['warning'] if within >= 80 else formats['fail']
            sheet.write(row, 2, within, within_fmt)
            sheet.write(row, 3, stat.get('count', 0), formats['data'])
        
        # Pairs data
        pairs = duplicates.get('pairs', [])
        if pairs:
            chart_start_row = row + 3
            sheet.write(chart_start_row, 0, 'Sample ID', formats['header'])
            sheet.write(chart_start_row, 1, 'Original', formats['header'])
            sheet.write(chart_start_row, 2, 'Duplicate', formats['header'])
            sheet.write(chart_start_row, 3, 'RPD (%)', formats['header'])
            
            for i, pair in enumerate(pairs[:50]):  # Limit to 50 pairs
                r = chart_start_row + 1 + i
                sheet.write(r, 0, pair.get('sample_id', f'Sample_{i}'), formats['data'])
                sheet.write(r, 1, pair.get('original', 0), formats['number'])
                sheet.write(r, 2, pair.get('duplicate', 0), formats['number'])
                
                rpd = pair.get('rpd', 0)
                rpd_fmt = formats['pass'] if rpd <= 10 else formats['warning'] if rpd <= 20 else formats['fail']
                sheet.write(r, 3, rpd, rpd_fmt)
            
            # Create scatter chart
            if len(pairs) >= 3:
                chart = workbook.add_chart({'type': 'scatter'})
                
                data_end_row = chart_start_row + min(len(pairs), 50)
                
                chart.add_series({
                    'name': 'Duplicate Pairs',
                    'categories': f"='Duplicates'!$B${chart_start_row + 2}:$B${data_end_row + 1}",
                    'values': f"='Duplicates'!$C${chart_start_row + 2}:$C${data_end_row + 1}",
                    'marker': {'type': 'circle', 'size': 8, 'fill': {'color': '#3498db'}},
                })
                
                chart.set_title({'name': 'Original vs Duplicate Scatter Plot'})
                chart.set_x_axis({'name': 'Original Value'})
                chart.set_y_axis({'name': 'Duplicate Value'})
                chart.set_size({'width': 500, 'height': 400})
                chart.set_legend({'none': True})
                
                sheet.insert_chart('F3', chart)


# Convenience function
def generate_excel_with_charts(
    analysis_results: Dict[str, Any],
    project_info: Optional[Dict[str, str]] = None,
    filename: Optional[str] = None
) -> str:
    """
    Generate Excel report with embedded charts.
    
    Args:
        analysis_results: QAQC analysis results
        project_info: Optional project metadata
        filename: Output filename
        
    Returns:
        Path to generated file
    """
    reporter = ExcelChartReporter()
    return reporter.generate_report(analysis_results, project_info, filename)
