"""
CRM Database Browser Dialog

Browse, search, and manage Certified Reference Materials.
Provides parity with the React UI's CRMDatabase component.
"""

import yaml
from pathlib import Path
from typing import Optional, Dict, Any, List

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QLineEdit,
    QGroupBox, QTextEdit, QHeaderView, QAbstractItemView,
    QMessageBox, QFormLayout, QDoubleSpinBox, QDialogButtonBox,
    QWidget, QSplitter, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


# Default CRM database path
DEFAULT_CRM_DB_PATH = Path(__file__).parent.parent.parent.parent / "crm_database.yaml"


class CRMDatabaseDialog(QDialog):
    """
    CRM Database browser dialog.

    Allows users to browse, search, and view details
    of Certified Reference Materials from the YAML database.
    """

    crm_selected = pyqtSignal(dict)  # Emitted when user selects a CRM

    def __init__(self, parent=None, db_path: Optional[str] = None):
        super().__init__(parent)
        self.db_path = Path(db_path) if db_path else DEFAULT_CRM_DB_PATH
        self.crm_data: List[Dict[str, Any]] = []
        self.filtered_data: List[Dict[str, Any]] = []
        self.methods_info: Dict[str, Any] = {}
        self.thresholds: Dict[str, Any] = {}

        self.setWindowTitle("CRM Database Browser")
        self.setMinimumSize(900, 650)
        self.resize(1000, 700)

        self.load_database()
        self.setup_ui()
        self.apply_theme()
        self.filter_crms()  # Initial population

    def load_database(self):
        """Load CRM data from YAML database."""
        try:
            if self.db_path.exists():
                with open(self.db_path, 'r') as f:
                    data = yaml.safe_load(f)
                self.crm_data = data.get('crms', [])
                self.methods_info = data.get('methods', {})
                self.thresholds = data.get('analysis_thresholds', {})
            else:
                self.crm_data = []
        except Exception as e:
            self.crm_data = []
            print(f"Error loading CRM database: {e}")

    def setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header = QLabel("Certified Reference Materials")
        header.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #F59E0B; "
            "padding-bottom: 4px;"
        )
        layout.addWidget(header)

        subtitle = QLabel(
            f"{len(self.crm_data)} standards available  •  "
            f"Source: {self.db_path.name}"
        )
        subtitle.setStyleSheet("color: #94A3B8; font-size: 11px;")
        layout.addWidget(subtitle)

        # Search & filter row
        filter_row = QHBoxLayout()
        filter_row.setSpacing(8)

        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, supplier, or notes...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setMinimumHeight(32)
        self.search_input.textChanged.connect(self.filter_crms)
        filter_row.addWidget(self.search_input, stretch=3)

        # Supplier filter
        self.supplier_filter = QComboBox()
        self.supplier_filter.setMinimumHeight(32)
        self.supplier_filter.addItem("All Suppliers")
        suppliers = sorted(set(crm.get('supplier', '') for crm in self.crm_data if crm.get('supplier')))
        self.supplier_filter.addItems(suppliers)
        self.supplier_filter.currentTextChanged.connect(self.filter_crms)
        filter_row.addWidget(self.supplier_filter, stretch=1)

        # Matrix filter
        self.matrix_filter = QComboBox()
        self.matrix_filter.setMinimumHeight(32)
        self.matrix_filter.addItem("All Matrices")
        matrices = sorted(set(crm.get('matrix', '') for crm in self.crm_data if crm.get('matrix')))
        self.matrix_filter.addItems(matrices)
        self.matrix_filter.currentTextChanged.connect(self.filter_crms)
        filter_row.addWidget(self.matrix_filter, stretch=1)

        layout.addLayout(filter_row)

        # Splitter: table on left, detail on right
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # CRM Table
        self.crm_table = QTableWidget()
        self.crm_table.setColumnCount(5)
        self.crm_table.setHorizontalHeaderLabels([
            "Name", "Value (g/t)", "± Uncertainty", "Supplier", "Matrix"
        ])
        self.crm_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.crm_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.crm_table.setAlternatingRowColors(True)
        self.crm_table.verticalHeader().setVisible(False)
        self.crm_table.verticalHeader().setDefaultSectionSize(32)
        self.crm_table.setShowGrid(True)
        header_view = self.crm_table.horizontalHeader()
        header_view.setStretchLastSection(True)
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, 5):
            header_view.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        self.crm_table.currentCellChanged.connect(self.on_crm_selected)
        splitter.addWidget(self.crm_table)

        # Detail panel (right side)
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(12, 8, 8, 8)
        detail_layout.setSpacing(8)

        self.detail_title = QLabel("Select a CRM")
        self.detail_title.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #F59E0B;"
        )
        detail_layout.addWidget(self.detail_title)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E293B;
                color: #CBD5E1;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Inter', sans-serif;
                font-size: 12px;
            }
        """)
        detail_layout.addWidget(self.detail_text)

        splitter.addWidget(detail_widget)
        splitter.setSizes([550, 350])

        layout.addWidget(splitter, stretch=1)

        # Analysis thresholds info
        if self.thresholds:
            thresholds_group = QGroupBox("Default Analysis Thresholds")
            thresholds_group.setStyleSheet("""
                QGroupBox {
                    color: #CBD5E1;
                    font-weight: bold;
                    border: 1px solid #334155;
                    border-radius: 6px;
                    margin-top: 8px;
                    padding-top: 16px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 6px;
                }
            """)
            thresh_layout = QHBoxLayout(thresholds_group)
            thresh_layout.setSpacing(20)

            thresh_items = [
                ("Z-Score", f"± {self.thresholds.get('z_score_threshold', 'N/A')}σ"),
                ("Recovery", f"{self.thresholds.get('recovery_limits', {}).get('min', '?')}–{self.thresholds.get('recovery_limits', {}).get('max', '?')}%"),
                ("Precision", f"≤ {self.thresholds.get('precision_threshold', 'N/A')}% RSD"),
                ("RPD", f"≤ {self.thresholds.get('rpd_threshold', 'N/A')}%"),
                ("Blank Limit", f"≤ {self.thresholds.get('blank_limit', 'N/A')} g/t"),
            ]
            for label_text, value_text in thresh_items:
                item_layout = QVBoxLayout()
                lbl = QLabel(label_text)
                lbl.setStyleSheet("color: #94A3B8; font-size: 10px; font-weight: normal;")
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                val = QLabel(value_text)
                val.setStyleSheet("color: #F1F5F9; font-size: 12px; font-weight: bold;")
                val.setAlignment(Qt.AlignmentFlag.AlignCenter)
                item_layout.addWidget(lbl)
                item_layout.addWidget(val)
                thresh_layout.addLayout(item_layout)

            layout.addWidget(thresholds_group)

        # Bottom buttons
        button_layout = QHBoxLayout()

        self.select_button = QPushButton("Use Selected CRM")
        self.select_button.setEnabled(False)
        self.select_button.setMinimumHeight(36)
        self.select_button.clicked.connect(self.accept_selection)
        button_layout.addWidget(self.select_button)

        close_button = QPushButton("Close")
        close_button.setMinimumHeight(36)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #334155;
                color: #F1F5F9;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """)
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

    def apply_theme(self):
        """Apply the dark slate + amber gold theme."""
        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
                color: #F1F5F9;
            }
            QLineEdit {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QLineEdit:focus {
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
            QComboBox:hover {
                border-color: #F59E0B;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox QAbstractItemView {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                selection-background-color: #422006;
            }
            QTableWidget {
                background-color: #1E293B;
                gridline-color: #334155;
                border: 1px solid #334155;
                border-radius: 6px;
                color: #F1F5F9;
            }
            QTableWidget::item {
                padding: 6px 8px;
                background-color: #1E293B;
            }
            QTableWidget::item:alternate {
                background-color: #0F172A;
            }
            QTableWidget::item:selected {
                background-color: #422006;
                color: #F1F5F9;
            }
            QHeaderView::section {
                background-color: #0F172A;
                color: #F59E0B;
                font-weight: bold;
                padding: 6px 8px;
                border: 1px solid #334155;
            }
            QPushButton#select_button, QPushButton {
                background-color: #F59E0B;
                color: #0F172A;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #FBBF24;
            }
            QPushButton:disabled {
                background-color: #334155;
                color: #64748B;
            }
        """)

    def filter_crms(self):
        """Filter CRM list based on search and filter criteria."""
        search_text = self.search_input.text().lower().strip()
        supplier_filter = self.supplier_filter.currentText()
        matrix_filter = self.matrix_filter.currentText()

        self.filtered_data = []
        for crm in self.crm_data:
            # Search filter
            if search_text:
                searchable = (
                    crm.get('name', '').lower() +
                    crm.get('supplier', '').lower() +
                    crm.get('notes', '').lower() +
                    crm.get('matrix', '').lower()
                )
                if search_text not in searchable:
                    continue

            # Supplier filter
            if supplier_filter != "All Suppliers":
                if crm.get('supplier', '') != supplier_filter:
                    continue

            # Matrix filter
            if matrix_filter != "All Matrices":
                if crm.get('matrix', '') != matrix_filter:
                    continue

            self.filtered_data.append(crm)

        self.populate_table()

    def populate_table(self):
        """Populate the CRM table with filtered data."""
        self.crm_table.setRowCount(len(self.filtered_data))

        for row, crm in enumerate(self.filtered_data):
            name_item = QTableWidgetItem(crm.get('name', ''))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.crm_table.setItem(row, 0, name_item)

            value_item = QTableWidgetItem(f"{crm.get('certified_value', 'N/A')}")
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.crm_table.setItem(row, 1, value_item)

            uncert_item = QTableWidgetItem(f"± {crm.get('uncertainty', 'N/A')}")
            uncert_item.setFlags(uncert_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            uncert_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.crm_table.setItem(row, 2, uncert_item)

            supplier_item = QTableWidgetItem(crm.get('supplier', ''))
            supplier_item.setFlags(supplier_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.crm_table.setItem(row, 3, supplier_item)

            matrix_item = QTableWidgetItem(crm.get('matrix', ''))
            matrix_item.setFlags(matrix_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.crm_table.setItem(row, 4, matrix_item)

        # Clear detail when table changes
        if not self.filtered_data:
            self.detail_title.setText("No CRMs match filters")
            self.detail_text.setHtml(
                "<p style='color: #94A3B8;'>Try adjusting your search or filters.</p>"
            )
            self.select_button.setEnabled(False)

    def on_crm_selected(self, row, col, prev_row, prev_col):
        """Handle CRM row selection."""
        if 0 <= row < len(self.filtered_data):
            crm = self.filtered_data[row]
            self.show_crm_detail(crm)
            self.select_button.setEnabled(True)
        else:
            self.select_button.setEnabled(False)

    def show_crm_detail(self, crm: Dict[str, Any]):
        """Display detailed CRM information."""
        name = crm.get('name', 'Unknown')
        self.detail_title.setText(name)

        html = f"""
        <table style="width:100%; border-collapse: collapse;">
            <tr>
                <td style="color: #94A3B8; padding: 4px 8px;">Certified Value</td>
                <td style="color: #F59E0B; font-weight: bold; padding: 4px 8px;">
                    {crm.get('certified_value', 'N/A')} ± {crm.get('uncertainty', 'N/A')} {crm.get('units', 'g/t')}
                </td>
            </tr>
            <tr>
                <td style="color: #94A3B8; padding: 4px 8px;">Supplier</td>
                <td style="color: #F1F5F9; padding: 4px 8px;">{crm.get('supplier', 'N/A')}</td>
            </tr>
            <tr>
                <td style="color: #94A3B8; padding: 4px 8px;">Matrix</td>
                <td style="color: #F1F5F9; padding: 4px 8px;">{crm.get('matrix', 'N/A')}</td>
            </tr>
            <tr>
                <td style="color: #94A3B8; padding: 4px 8px;">Batch Number</td>
                <td style="color: #F1F5F9; padding: 4px 8px;">{crm.get('batch_number', 'N/A')}</td>
            </tr>
            <tr>
                <td style="color: #94A3B8; padding: 4px 8px;">Expiry Date</td>
                <td style="color: #F1F5F9; padding: 4px 8px;">{crm.get('expiry_date', 'N/A')}</td>
            </tr>
            <tr>
                <td style="color: #94A3B8; padding: 4px 8px;">Storage</td>
                <td style="color: #F1F5F9; padding: 4px 8px;">{crm.get('storage_conditions', 'N/A')}</td>
            </tr>
        </table>
        <br/>
        <p style="color: #94A3B8; font-style: italic; padding: 4px 8px;">
            {crm.get('notes', '')}
        </p>
        """
        self.detail_text.setHtml(html)

    def accept_selection(self):
        """Accept the currently selected CRM."""
        row = self.crm_table.currentRow()
        if 0 <= row < len(self.filtered_data):
            self.crm_selected.emit(self.filtered_data[row])
            self.accept()

    def get_selected_crm(self) -> Optional[Dict[str, Any]]:
        """Return the selected CRM data, or None."""
        row = self.crm_table.currentRow()
        if 0 <= row < len(self.filtered_data):
            return self.filtered_data[row]
        return None
