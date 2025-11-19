"""
Data Panel Widget

This widget handles data import, preview, and column mapping for the
QAQC Analysis Application. Designed for geologists working with assay data.
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
    QFileDialog, QMessageBox, QProgressBar, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from ..styles.geological_theme import GeologicalTheme
from ...data.importer import DataImporter


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

            self.progress_updated.emit(10)
            self.msleep(50)

            # Initialize data importer
            importer = DataImporter()

            self.progress_updated.emit(30)
            self.msleep(50)

            # Read the file
            df = importer.read_table(self.file_path)

            self.progress_updated.emit(60)
            self.msleep(50)

            # Get column mapping suggestions
            suggestions = importer.suggest_mapping(df.columns.tolist())

            # Build mapping dictionary (use suggested mappings with confidence > 0.8)
            auto_mapping = {}
            for canonical, (header, confidence) in suggestions.items():
                if header and confidence >= 0.8:
                    auto_mapping[canonical] = header

            self.progress_updated.emit(80)
            self.msleep(50)

            # Prepare data preview (first 10 rows)
            preview_rows = min(10, len(df))
            data_preview = []
            for idx in range(preview_rows):
                row_data = []
                for col in df.columns:
                    value = df.iloc[idx][col]
                    # Convert to string, handle NaN
                    if pd.isna(value):
                        row_data.append("")
                    else:
                        row_data.append(str(value))
                data_preview.append(row_data)

            # Prepare data info structure (ONLY pass lightweight metadata through signal)
            # The DataFrame will be re-read in the main thread to avoid all threading issues
            data_info = {
                'file_path': self.file_path,
                'file_name': Path(self.file_path).name,
                'sample_count': len(df),
                'columns': df.columns.tolist(),
                'data_preview': data_preview,
                'suggested_mapping': auto_mapping,
                'all_suggestions': suggestions
                # NOTE: DataFrame is NOT passed through signal - will be re-read in main thread
            }

            self.progress_updated.emit(100)
            self.data_loaded.emit(data_info)

        except Exception as e:
            import traceback
            error_msg = f"Import error: {str(e)}\n{traceback.format_exc()}"
            self.error_occurred.emit(error_msg)


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
    analysis_requested = pyqtSignal(dict)
    configuration_changed = pyqtSignal(dict)

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
        self.data_table.setShowGrid(True)
        self.data_table.setGridStyle(Qt.PenStyle.SolidLine)
        self.data_table.verticalHeader().setVisible(False)  # Hide row numbers
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        # Increase row height for better readability
        self.data_table.verticalHeader().setDefaultSectionSize(32)
        # Initially set to 0 rows/columns to avoid dark squares
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        # Style empty cells to be invisible and clean appearance with subtle selection
        self.data_table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                gridline-color: #E9ECEF;
                border: 1px solid #DEE2E6;
            }
            QTableWidget::item:empty {
                background-color: transparent;
                border: none;
            }
            QTableWidget::item {
                padding: 6px 8px;
                background-color: #FFFFFF;
            }
            QTableWidget::item:alternate {
                background-color: #F8F9FA;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1A1A1A;
            }
            QTableWidget::item:hover {
                background-color: #E9ECEF;
            }
            QTableWidget::item:selected:hover {
                background-color: #D1E7F0;
                color: #1A1A1A;
            }
        """)
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
        self.mapping_table.setShowGrid(True)
        self.mapping_table.setGridStyle(Qt.PenStyle.SolidLine)
        self.mapping_table.verticalHeader().setVisible(False)  # Hide row numbers
        self.mapping_table.horizontalHeader().setStretchLastSection(True)
        self.mapping_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        # Increase row height for better readability (especially for dropdowns)
        self.mapping_table.verticalHeader().setDefaultSectionSize(36)
        # Initially set to 0 rows to avoid dark squares
        self.mapping_table.setRowCount(0)
        # Style empty cells to be invisible and clean appearance with subtle selection
        self.mapping_table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                gridline-color: #E9ECEF;
                border: 1px solid #DEE2E6;
            }
            QTableWidget::item:empty {
                background-color: transparent;
                border: none;
            }
            QTableWidget::item {
                padding: 6px 8px;
                background-color: #FFFFFF;
            }
            QTableWidget::item:alternate {
                background-color: #F8F9FA;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1A1A1A;
            }
            QTableWidget::item:hover {
                background-color: #E9ECEF;
            }
            QTableWidget::item:selected:hover {
                background-color: #D1E7F0;
                color: #1A1A1A;
            }
        """)
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
        self.progress_bar.setValue(0)
        self.import_button.setEnabled(False)

        # Process in main thread to avoid PyQt6 threading crashes
        # Use QApplication.processEvents() to keep UI responsive
        try:
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()

            # Validate file
            if not file_path or not Path(file_path).exists():
                self.on_import_error("No valid file selected")
                return

            app.processEvents()  # Keep UI responsive
            self.progress_bar.setValue(10)

            # Initialize data importer
            importer = DataImporter()
            app.processEvents()
            self.progress_bar.setValue(30)

            # Read the file
            df = importer.read_table(file_path)
            app.processEvents()
            self.progress_bar.setValue(60)

            # Get column mapping suggestions
            suggestions = importer.suggest_mapping(df.columns.tolist())

            # Build mapping dictionary
            auto_mapping = {}
            for canonical, (header, confidence) in suggestions.items():
                if header and confidence >= 0.8:
                    auto_mapping[canonical] = header

            app.processEvents()
            self.progress_bar.setValue(80)

            # Prepare data preview (first 10 rows)
            preview_rows = min(10, len(df))
            data_preview = []
            for idx in range(preview_rows):
                row_data = []
                for col in df.columns:
                    value = df.iloc[idx][col]
                    if pd.isna(value):
                        row_data.append("")
                    else:
                        row_data.append(str(value))
                data_preview.append(row_data)

            app.processEvents()
            self.progress_bar.setValue(100)

            # Prepare data info structure
            data_info = {
                'file_path': file_path,
                'file_name': Path(file_path).name,
                'sample_count': len(df),
                'columns': df.columns.tolist(),
                'data_preview': data_preview,
                'dataframe': df,  # Safe to include now - we're in main thread
                'suggested_mapping': auto_mapping,
                'all_suggestions': suggestions
            }

            # Call handler directly (no signal needed)
            self.on_data_loaded(data_info)

        except Exception as e:
            import traceback
            error_msg = f"Import error: {str(e)}\n{traceback.format_exc()}"
            self.on_import_error(error_msg)

    def on_data_loaded(self, data_info: Dict[str, Any]):
        """Handle data loaded signal."""
        # Re-read the file in the main thread (safest approach - avoids all threading issues)
        # This is slightly less efficient but completely thread-safe
        try:
            importer = DataImporter()
            df = importer.read_table(data_info['file_path'])
            data_info['dataframe'] = df
        except Exception as e:
            QMessageBox.critical(self, "Data Error",
                               f"Failed to load DataFrame in main thread:\n{str(e)}")
            return

        self.current_data = data_info

        # Update file information
        self.file_path_label.setText(f"File: {data_info['file_name']}")
        self.file_stats_label.setText(
            f"Samples: {data_info['sample_count']} | "
            f"Columns: {len(data_info['columns'])}"
        )

        # Update data preview
        self.update_data_preview(data_info)

        # Update column mapping with suggested mappings
        suggested_mapping = data_info.get('suggested_mapping', {})
        self.setup_column_mapping(data_info['columns'], suggested_mapping)

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
            for col in range(len(columns)):
                if col < len(row_data):
                    cell_data = row_data[col]
                    item = QTableWidgetItem(str(cell_data) if cell_data else "")
                else:
                    item = QTableWidgetItem("")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.data_table.setItem(row, col, item)

        # Resize columns to content with minimum width
        self.data_table.resizeColumnsToContents()
        # Set minimum column widths to prevent squishing
        for col in range(len(columns)):
            current_width = self.data_table.columnWidth(col)
            self.data_table.setColumnWidth(col, max(current_width, 80))

    def setup_column_mapping(self, columns: List[str], suggested_mapping: Optional[Dict[str, str]] = None):
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

            # Use suggested mapping if available
            if suggested_mapping and field in suggested_mapping:
                mapped_col = suggested_mapping[field]
                if mapped_col in columns:
                    idx = columns.index(mapped_col)
                    combo.setCurrentIndex(idx + 1)
            else:
                # Fallback: Auto-detect if possible
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
        """Auto-detect column mapping using DataImporter suggestions."""
        if not self.current_data or 'columns' not in self.current_data:
            QMessageBox.warning(self, "No Data", "Please import data first.")
            return

        columns = self.current_data['columns']
        importer = DataImporter()
        suggestions = importer.suggest_mapping(columns)

        # Apply high-confidence mappings automatically
        applied_count = 0
        for row in range(self.mapping_table.rowCount()):
            field_item = self.mapping_table.item(row, 0)
            if not field_item:
                continue

            field = field_item.text().lower().replace(' ', '_')
            combo = self.mapping_table.cellWidget(row, 1)
            if not combo:
                continue

            if field in suggestions:
                suggested_col, confidence = suggestions[field]
                if suggested_col and confidence >= 0.8:
                    if suggested_col in columns:
                        idx = columns.index(suggested_col)
                        combo.setCurrentIndex(idx + 1)
                        applied_count += 1

        QMessageBox.information(
            self,
            "Auto-Mapping Complete",
            f"Applied {applied_count} column mappings with high confidence (≥80%).\n"
            "Please review and adjust any remaining mappings manually."
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
        # Clear tables completely to avoid dark squares
        self.data_table.setRowCount(0)
        self.data_table.setColumnCount(0)
        self.mapping_table.setRowCount(0)
        self.crm_combo.setCurrentIndex(0)
        self.crm_info_label.setText("")

        self.status_label.setText("Ready to import data")
        self.status_label.setStyleSheet("color: #27AE60; font-weight: bold;")
        self.progress_bar.setVisible(False)
        self.import_button.setEnabled(True)
        self.auto_map_button.setEnabled(False)
