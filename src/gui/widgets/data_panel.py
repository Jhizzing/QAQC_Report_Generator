"""
Data Panel Widget

This widget handles data import, preview, and column mapping for the
QAQC Analysis Application. Designed for geologists working with assay data.
"""

from typing import Optional, Dict, Any, List
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
    QFileDialog, QMessageBox, QProgressBar, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from ..styles.geological_theme import GeologicalTheme


class DataImportThread(QThread):
    """Thread for data import operations."""

    data_loaded = pyqtSignal(dict)
    progress_updated = pyqtSignal(int)
    error_occurred = pyqtSignal(str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def run(self):
        """Run data import in separate thread."""
        try:
            # Check if file path is valid
            if not self.file_path or not Path(self.file_path).exists():
                self.error_occurred.emit("No valid file selected")
                return

            # TODO: Implement actual data import using DataImporter
            # This is a placeholder for now

            # Simulate progress
            for i in range(101):
                self.progress_updated.emit(i)
                self.msleep(20)  # Simulate processing time

            # Simulate data structure
            data_info = {
                'file_path': self.file_path,
                'file_name': Path(self.file_path).name,
                'sample_count': 1250,
                'columns': ['sample_id', 'sample_type', 'result', 'qualifier', 'detection_limit'],
                'data_preview': [
                    ['STD-001', 'STANDARD', '0.85', '', '0.01'],
                    ['STD-002', 'STANDARD', '0.87', '', '0.01'],
                    ['BLK-001', 'BLANK', '0.01', '', '0.01'],
                    ['DUP-001', 'DUPLICATE', '1.25', '', '0.01'],
                    ['SMP-001', 'SAMPLE', '1.5', '', '0.01']
                ]
            }

            self.data_loaded.emit(data_info)

        except Exception as e:
            self.error_occurred.emit(str(e))


class DataPanel(QWidget):
    """
    Data panel widget for importing and managing assay data.

    Provides functionality for:
    - File import and validation
    - Data preview and statistics
    - Column mapping and configuration
    - CRM selection and validation
    """

    # Signals
    data_loaded = pyqtSignal(dict)
    data_changed = pyqtSignal(dict)
    column_mapping_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        # Data state
        self.current_data: Optional[Dict[str, Any]] = None
        self.column_mapping: Dict[str, str] = {}

        # Initialize UI
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()

    def setup_ui(self):
        """Set up the data panel user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # File information group
        self.file_group = QGroupBox("File Information")
        file_layout = QVBoxLayout(self.file_group)

        # File path display
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setWordWrap(True)
        self.file_path_label.setStyleSheet("color: #6C757D; font-style: italic;")
        file_layout.addWidget(self.file_path_label)

        # File statistics
        self.file_stats_label = QLabel("")
        self.file_stats_label.setStyleSheet("color: #2C3E50; font-weight: bold;")
        file_layout.addWidget(self.file_stats_label)

        # Import button
        self.import_button = QPushButton("Import Data File")
        self.import_button.setMinimumHeight(35)
        file_layout.addWidget(self.import_button)

        layout.addWidget(self.file_group)

        # Data preview group
        self.preview_group = QGroupBox("Data Preview")
        preview_layout = QVBoxLayout(self.preview_group)

        # Data table
        self.data_table = QTableWidget()
        self.data_table.setMaximumHeight(200)
        self.data_table.setAlternatingRowColors(True)
        preview_layout.addWidget(self.data_table)

        layout.addWidget(self.preview_group)

        # Column mapping group
        self.mapping_group = QGroupBox("Column Mapping")
        mapping_layout = QVBoxLayout(self.mapping_group)

        # Column mapping table
        self.mapping_table = QTableWidget()
        self.mapping_table.setColumnCount(2)
        self.mapping_table.setHorizontalHeaderLabels(["Required Field", "Mapped Column"])
        self.mapping_table.setMaximumHeight(150)
        mapping_layout.addWidget(self.mapping_table)

        # Auto-map button
        self.auto_map_button = QPushButton("Auto-Detect Mapping")
        self.auto_map_button.setEnabled(False)
        mapping_layout.addWidget(self.auto_map_button)

        layout.addWidget(self.mapping_group)

        # CRM selection group
        self.crm_group = QGroupBox("CRM Selection")
        crm_layout = QVBoxLayout(self.crm_group)

        # CRM dropdown
        self.crm_combo = QComboBox()
        self.crm_combo.addItems([
            "Auto-Select CRM",
            "NIST SRM 2709a (0.85 g/t)",
            "NIST SRM 2704 (15.2 g/t)",
            "CANMET OREAS 101 (0.12 g/t)"
        ])
        crm_layout.addWidget(self.crm_combo)

        # CRM info display
        self.crm_info_label = QLabel("")
        self.crm_info_label.setWordWrap(True)
        self.crm_info_label.setStyleSheet("color: #6C757D; font-size: 10px;")
        crm_layout.addWidget(self.crm_info_label)

        layout.addWidget(self.crm_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready to import data")
        self.status_label.setStyleSheet("color: #27AE60; font-weight: bold;")
        layout.addWidget(self.status_label)

    def setup_connections(self):
        """Set up signal connections."""
        self.import_button.clicked.connect(self.import_data)
        self.auto_map_button.clicked.connect(self.auto_detect_mapping)
        self.crm_combo.currentTextChanged.connect(self.on_crm_changed)

    def apply_theme(self):
        """Apply the geological theme."""
        theme = GeologicalTheme()
        self.setStyleSheet(theme.get_widget_style('data_panel'))

    def import_data(self):
        """Import data file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Assay Data File",
            "",
            "CSV Files (*.csv);;Excel Files (*.xlsx *.xls);;All Files (*)"
        )

        if file_path:
            self.load_data_file(file_path)

    def load_data_file(self, file_path: str):
        """Load data from file."""
        self.status_label.setText("Loading data...")
        self.progress_bar.setVisible(True)
        self.import_button.setEnabled(False)

        # Start import thread
        self.import_thread = DataImportThread(file_path)
        self.import_thread.data_loaded.connect(self.on_data_loaded)
        self.import_thread.progress_updated.connect(self.progress_bar.setValue)
        self.import_thread.error_occurred.connect(self.on_import_error)
        self.import_thread.start()

    def on_data_loaded(self, data_info: Dict[str, Any]):
        """Handle data loaded signal."""
        self.current_data = data_info

        # Update file information
        self.file_path_label.setText(f"File: {data_info['file_name']}")
        self.file_stats_label.setText(
            f"Samples: {data_info['sample_count']} | "
            f"Columns: {len(data_info['columns'])}"
        )

        # Update data preview
        self.update_data_preview(data_info)

        # Update column mapping
        self.setup_column_mapping(data_info['columns'])

        # Enable controls
        self.auto_map_button.setEnabled(True)
        self.import_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Data loaded successfully")
        self.status_label.setStyleSheet("color: #27AE60; font-weight: bold;")

        # Emit signal to main window
        self.data_loaded.emit(data_info)

    def on_import_error(self, error_message: str):
        """Handle import error."""
        self.status_label.setText(f"Error: {error_message}")
        self.status_label.setStyleSheet("color: #E74C3C; font-weight: bold;")
        self.progress_bar.setVisible(False)
        self.import_button.setEnabled(True)

        QMessageBox.critical(self, "Import Error", f"Failed to load data:\n{error_message}")

    def update_data_preview(self, data_info: Dict[str, Any]):
        """Update the data preview table."""
        columns = data_info.get('columns', [])
        preview_data = data_info.get('data_preview', [])

        if not columns or not preview_data:
            # Clear table if no data
            self.data_table.setRowCount(0)
            self.data_table.setColumnCount(0)
            return

        self.data_table.setRowCount(len(preview_data))
        self.data_table.setColumnCount(len(columns))
        self.data_table.setHorizontalHeaderLabels(columns)

        for row, row_data in enumerate(preview_data):
            for col, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.data_table.setItem(row, col, item)

        # Resize columns to content
        self.data_table.resizeColumnsToContents()

    def setup_column_mapping(self, columns: List[str]):
        """Setup column mapping interface."""
        if not columns:
            # Clear mapping table if no columns
            self.mapping_table.setRowCount(0)
            return

        required_fields = [
            "sample_id",
            "sample_type",
            "result",
            "qualifier",
            "detection_limit"
        ]

        self.mapping_table.setRowCount(len(required_fields))

        for row, field in enumerate(required_fields):
            # Required field label
            field_item = QTableWidgetItem(field.replace('_', ' ').title())
            field_item.setFlags(field_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.mapping_table.setItem(row, 0, field_item)

            # Column mapping combo
            combo = QComboBox()
            combo.addItem("-- Select Column --")
            combo.addItems(columns)

            # Auto-detect if possible
            field_lower = field.lower()
            for i, col in enumerate(columns):
                if field_lower in col.lower() or col.lower() in field_lower:
                    combo.setCurrentIndex(i + 1)
                    break

            self.mapping_table.setCellWidget(row, 1, combo)
            combo.currentTextChanged.connect(self.on_mapping_changed)

        # Resize columns
        self.mapping_table.resizeColumnsToContents()

    def auto_detect_mapping(self):
        """Auto-detect column mapping."""
        # TODO: Implement intelligent column mapping
        # This would use the existing DataImporter functionality

        QMessageBox.information(
            self,
            "Auto-Mapping",
            "Auto-mapping functionality will be implemented with the DataImporter integration."
        )

    def on_mapping_changed(self):
        """Handle column mapping changes."""
        mapping = {}

        for row in range(self.mapping_table.rowCount()):
            field_item = self.mapping_table.item(row, 0)
            combo = self.mapping_table.cellWidget(row, 1)

            if field_item and combo:
                field = field_item.text().lower().replace(' ', '_')
                mapped_column = combo.currentText()

                if mapped_column != "-- Select Column --":
                    mapping[field] = mapped_column

        self.column_mapping = mapping
        self.column_mapping_changed.emit(mapping)

    def on_crm_changed(self, crm_name: str):
        """Handle CRM selection changes."""
        if crm_name == "Auto-Select CRM":
            self.crm_info_label.setText("CRM will be automatically selected based on concentration")
        elif "NIST SRM 2709a" in crm_name:
            self.crm_info_label.setText("Certified Value: 0.85 ± 0.05 g/t | Matrix: Gold Ore | Supplier: NIST")
        elif "NIST SRM 2704" in crm_name:
            self.crm_info_label.setText("Certified Value: 15.2 ± 0.8 g/t | Matrix: Gold Ore | Supplier: NIST")
        elif "CANMET OREAS 101" in crm_name:
            self.crm_info_label.setText("Certified Value: 0.12 ± 0.02 g/t | Matrix: Gold Ore | Supplier: CANMET")
        else:
            self.crm_info_label.setText("")

    def reset(self):
        """Reset the data panel to initial state."""
        self.current_data = None
        self.column_mapping = {}

        self.file_path_label.setText("No file selected")
        self.file_stats_label.setText("")
        self.data_table.setRowCount(0)
        self.mapping_table.setRowCount(0)
        self.crm_combo.setCurrentIndex(0)
        self.crm_info_label.setText("")

        self.status_label.setText("Ready to import data")
        self.status_label.setStyleSheet("color: #27AE60; font-weight: bold;")
        self.progress_bar.setVisible(False)
        self.import_button.setEnabled(True)
        self.auto_map_button.setEnabled(False)
