"""
JORC Report Configuration Dialog

Configure report metadata, formatting, and export options before
generating JORC-compliant QAQC reports. Provides parity with the
React UI's ReportConfig component.
"""

from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QGroupBox, QTextEdit, QCheckBox,
    QFormLayout, QTabWidget, QWidget, QDialogButtonBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class ReportConfigDialog(QDialog):
    """
    JORC report configuration dialog.

    Allows users to set report metadata (competent person, company, etc.),
    formatting options (color scheme, font size, layout), and export format
    before generating a report.
    """

    config_accepted = pyqtSignal(dict)

    def __init__(self, parent=None, current_config: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.config = current_config or {}

        self.setWindowTitle("Report Configuration")
        self.setMinimumSize(650, 550)
        self.resize(700, 600)

        self.setup_ui()
        self.apply_theme()
        self.load_config()

    def setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header = QLabel("JORC Report Configuration")
        header.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #F59E0B; "
            "padding-bottom: 4px;"
        )
        layout.addWidget(header)

        subtitle = QLabel("Configure report metadata and formatting options")
        subtitle.setStyleSheet("color: #94A3B8; font-size: 11px;")
        layout.addWidget(subtitle)

        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #334155;
                border-radius: 6px;
                background-color: #0F172A;
            }
            QTabBar::tab {
                background-color: #1E293B;
                color: #94A3B8;
                padding: 8px 16px;
                border: 1px solid #334155;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0F172A;
                color: #F59E0B;
                border-bottom: 2px solid #F59E0B;
            }
            QTabBar::tab:hover:!selected {
                color: #F1F5F9;
            }
        """)

        # Tab 1: Report Metadata
        metadata_tab = QWidget()
        metadata_layout = QFormLayout(metadata_tab)
        metadata_layout.setContentsMargins(16, 16, 16, 16)
        metadata_layout.setSpacing(10)

        self.report_title_input = QLineEdit()
        self.report_title_input.setPlaceholderText("e.g. QAQC Report — Project Name")
        metadata_layout.addRow("Report Title:", self.report_title_input)

        self.competent_person_input = QLineEdit()
        self.competent_person_input.setPlaceholderText("Name of Competent Person")
        metadata_layout.addRow("Competent Person:", self.competent_person_input)

        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Company Name")
        metadata_layout.addRow("Company:", self.company_input)

        self.laboratory_input = QLineEdit()
        self.laboratory_input.setPlaceholderText("e.g. ALS Geochemistry, SGS")
        metadata_layout.addRow("Laboratory:", self.laboratory_input)

        self.drilling_company_input = QLineEdit()
        self.drilling_company_input.setPlaceholderText("e.g. Boart Longyear")
        metadata_layout.addRow("Drilling Company:", self.drilling_company_input)

        self.sample_type_input = QLineEdit()
        self.sample_type_input.setPlaceholderText("e.g. RC chips, Diamond core, Soil")
        metadata_layout.addRow("Sample Type:", self.sample_type_input)

        self.comments_input = QTextEdit()
        self.comments_input.setMaximumHeight(80)
        self.comments_input.setPlaceholderText("Additional comments or notes for the report...")
        metadata_layout.addRow("Comments:", self.comments_input)

        tabs.addTab(metadata_tab, "Metadata")

        # Tab 2: Formatting
        format_tab = QWidget()
        format_layout = QFormLayout(format_tab)
        format_layout.setContentsMargins(16, 16, 16, 16)
        format_layout.setSpacing(10)

        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems(["Default (LogiQore)", "Corporate", "Minimal"])
        format_layout.addRow("Color Scheme:", self.color_scheme_combo)

        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Small (9pt)", "Medium (10pt)", "Large (11pt)"])
        self.font_size_combo.setCurrentIndex(1)
        format_layout.addRow("Font Size:", self.font_size_combo)

        self.page_layout_combo = QComboBox()
        self.page_layout_combo.addItems(["Portrait", "Landscape"])
        format_layout.addRow("Page Layout:", self.page_layout_combo)

        self.logo_url_input = QLineEdit()
        self.logo_url_input.setPlaceholderText("URL or path to company logo (optional)")
        format_layout.addRow("Logo:", self.logo_url_input)

        self.dpi_combo = QComboBox()
        self.dpi_combo.addItems(["150 DPI (Draft)", "300 DPI (Standard)", "600 DPI (High Quality)"])
        self.dpi_combo.setCurrentIndex(1)
        format_layout.addRow("Figure Resolution:", self.dpi_combo)

        tabs.addTab(format_tab, "Formatting")

        # Tab 3: Content
        content_tab = QWidget()
        content_layout = QVBoxLayout(content_tab)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(10)

        include_group = QGroupBox("Include in Report")
        include_group.setStyleSheet("""
            QGroupBox {
                color: #CBD5E1;
                font-weight: bold;
                border: 1px solid #334155;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
        """)
        include_layout = QVBoxLayout(include_group)

        self.include_cover = QCheckBox("Cover Page")
        self.include_cover.setChecked(True)
        include_layout.addWidget(self.include_cover)

        self.include_jorc_table = QCheckBox("JORC Compliance Table")
        self.include_jorc_table.setChecked(True)
        include_layout.addWidget(self.include_jorc_table)

        self.include_control_charts = QCheckBox("Control Charts (Standards)")
        self.include_control_charts.setChecked(True)
        include_layout.addWidget(self.include_control_charts)

        self.include_scatter_plots = QCheckBox("Scatter Plots (Duplicates)")
        self.include_scatter_plots.setChecked(True)
        include_layout.addWidget(self.include_scatter_plots)

        self.include_histograms = QCheckBox("Histograms (Blanks)")
        self.include_histograms.setChecked(True)
        include_layout.addWidget(self.include_histograms)

        self.include_tables = QCheckBox("Summary Data Tables")
        self.include_tables.setChecked(True)
        include_layout.addWidget(self.include_tables)

        content_layout.addWidget(include_group)
        content_layout.addStretch()

        tabs.addTab(content_tab, "Content")

        # Tab 4: Export
        export_tab = QWidget()
        export_layout = QFormLayout(export_tab)
        export_layout.setContentsMargins(16, 16, 16, 16)
        export_layout.setSpacing(10)

        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems([
            "Excel + PDF (Both)",
            "PDF Only (.pdf)",
            "Word Document (.docx)",
            "Excel Only (.xlsx)"
        ])
        export_layout.addRow("Export Format:", self.export_format_combo)

        self.plot_format_combo = QComboBox()
        self.plot_format_combo.addItems(["PNG", "SVG", "PDF"])
        export_layout.addRow("Plot Format:", self.plot_format_combo)

        tabs.addTab(export_tab, "Export")

        layout.addWidget(tabs, stretch=1)

        # Bottom buttons
        button_layout = QHBoxLayout()

        reset_button = QPushButton("Reset Defaults")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #334155;
                color: #F1F5F9;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #475569; }
        """)
        reset_button.clicked.connect(self.reset_defaults)
        button_layout.addWidget(reset_button)

        button_layout.addStretch()

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #334155;
                color: #F1F5F9;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #475569; }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        self.generate_button = QPushButton("Generate Report")
        self.generate_button.setMinimumHeight(36)
        self.generate_button.clicked.connect(self.accept_config)
        button_layout.addWidget(self.generate_button)

        layout.addLayout(button_layout)

    def apply_theme(self):
        """Apply the dark slate + amber gold theme."""
        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
                color: #F1F5F9;
            }
            QLabel {
                color: #CBD5E1;
                font-size: 12px;
            }
            QLineEdit, QTextEdit {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #F59E0B;
            }
            QComboBox {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QComboBox:hover { border-color: #F59E0B; }
            QComboBox::drop-down { border: none; width: 24px; }
            QComboBox QAbstractItemView {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                selection-background-color: #422006;
            }
            QCheckBox {
                color: #F1F5F9;
                spacing: 8px;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 18px; height: 18px;
                border: 2px solid #475569;
                border-radius: 4px;
                background-color: #1E293B;
            }
            QCheckBox::indicator:checked {
                background-color: #F59E0B;
                border-color: #F59E0B;
            }
            QPushButton {
                background-color: #F59E0B;
                color: #0F172A;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #FBBF24; }
        """)

    def load_config(self):
        """Load existing config into form fields."""
        if not self.config:
            return

        self.report_title_input.setText(self.config.get('report_title', ''))
        self.competent_person_input.setText(self.config.get('competent_person', ''))
        self.company_input.setText(self.config.get('company', ''))
        self.laboratory_input.setText(self.config.get('laboratory', ''))
        self.drilling_company_input.setText(self.config.get('drilling_company', ''))
        self.sample_type_input.setText(self.config.get('sample_type', ''))
        self.comments_input.setPlainText(self.config.get('comments', ''))

    def get_config(self) -> Dict[str, Any]:
        """Collect all config values from form."""
        dpi_map = {"150 DPI (Draft)": 150, "300 DPI (Standard)": 300, "600 DPI (High Quality)": 600}
        font_map = {"Small (9pt)": 9, "Medium (10pt)": 10, "Large (11pt)": 11}
        format_map = {
            "Excel + PDF (Both)": "both",
            "PDF Only (.pdf)": "pdf",
            "Word Document (.docx)": "docx",
            "Excel Only (.xlsx)": "excel"
        }
        scheme_map = {
            "Default (LogiQore)": "default",
            "Corporate": "corporate",
            "Minimal": "minimal"
        }

        return {
            'report_title': self.report_title_input.text().strip(),
            'competent_person': self.competent_person_input.text().strip(),
            'company': self.company_input.text().strip(),
            'laboratory': self.laboratory_input.text().strip(),
            'drilling_company': self.drilling_company_input.text().strip(),
            'sample_type': self.sample_type_input.text().strip(),
            'comments': self.comments_input.toPlainText().strip(),
            'color_scheme': scheme_map.get(self.color_scheme_combo.currentText(), 'default'),
            'font_size': font_map.get(self.font_size_combo.currentText(), 10),
            'page_layout': self.page_layout_combo.currentText().lower(),
            'logo_url': self.logo_url_input.text().strip(),
            'dpi': dpi_map.get(self.dpi_combo.currentText(), 300),
            'export_format': format_map.get(self.export_format_combo.currentText(), 'both'),
            'plot_format': self.plot_format_combo.currentText().lower(),
            'include_cover': self.include_cover.isChecked(),
            'include_jorc_table': self.include_jorc_table.isChecked(),
            'include_control_charts': self.include_control_charts.isChecked(),
            'include_scatter_plots': self.include_scatter_plots.isChecked(),
            'include_histograms': self.include_histograms.isChecked(),
            'include_tables': self.include_tables.isChecked(),
        }

    def reset_defaults(self):
        """Reset all fields to defaults."""
        self.report_title_input.clear()
        self.competent_person_input.clear()
        self.company_input.clear()
        self.laboratory_input.clear()
        self.drilling_company_input.clear()
        self.sample_type_input.clear()
        self.comments_input.clear()
        self.color_scheme_combo.setCurrentIndex(0)
        self.font_size_combo.setCurrentIndex(1)
        self.page_layout_combo.setCurrentIndex(0)
        self.logo_url_input.clear()
        self.dpi_combo.setCurrentIndex(1)
        self.export_format_combo.setCurrentIndex(0)
        self.plot_format_combo.setCurrentIndex(0)
        self.include_cover.setChecked(True)
        self.include_jorc_table.setChecked(True)
        self.include_control_charts.setChecked(True)
        self.include_scatter_plots.setChecked(True)
        self.include_histograms.setChecked(True)
        self.include_tables.setChecked(True)

    def accept_config(self):
        """Accept configuration and emit signal."""
        config = self.get_config()
        self.config_accepted.emit(config)
        self.accept()
