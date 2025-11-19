"""
Main Window for QAQC Analysis Application

This module contains the main application window designed for geologists
working with assay data. It provides an intuitive interface for data import,
analysis configuration, and result visualization.
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QMenuBar, QToolBar, QStatusBar,
    QMessageBox, QFileDialog, QProgressBar, QLabel
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QIcon, QKeySequence

from .widgets.data_panel import DataPanel
from .widgets.analysis_panel import AnalysisPanel
from .widgets.visualization_panel import VisualizationPanel
from .styles.geological_theme import GeologicalTheme
from .utils.gui_helpers import GuiHelpers
from src.reporting import ExcelReporter, PDFReporter


class QAQCApplication(QMainWindow):
    """
    Main application window for QAQC Analysis Application.

    Designed specifically for geologists and mining engineers working
    with assay data. Provides an intuitive interface for data import,
    analysis configuration, and result visualization.
    """

    def __init__(self):
        super().__init__()

        # Application state
        self.current_file: Optional[str] = None
        self.current_data = None
        self.analysis_results = None
        self.config = {}
        self.output_dir = Path.cwd() / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.excel_reporter = ExcelReporter({'include_raw_data': True})
        self.pdf_reporter = PDFReporter({'include_plots': True})

        # Initialize UI
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()

        # Set window properties
        self.setWindowTitle("QAQC Analysis Application - Geological Data Analysis")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Center window on screen
        self.center_window()

    def setup_ui(self):
        """Set up the main user interface."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Create main splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)

        # Create panels
        self.data_panel = DataPanel()
        self.analysis_panel = AnalysisPanel()
        self.visualization_panel = VisualizationPanel()

        # Add panels to splitter
        main_splitter.addWidget(self.data_panel)
        main_splitter.addWidget(self.analysis_panel)
        main_splitter.addWidget(self.visualization_panel)

        # Set splitter proportions (30%, 30%, 40%)
        main_splitter.setSizes([300, 300, 400])
        main_splitter.setStretchFactor(0, 0)  # Data panel fixed
        main_splitter.setStretchFactor(1, 0)  # Analysis panel fixed
        main_splitter.setStretchFactor(2, 1)  # Visualization panel flexible

        # Create menu bar
        self.create_menu_bar()

        # Create toolbar
        self.create_toolbar()

        # Create status bar
        self.create_status_bar()

    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('&File')

        # New project
        new_action = QAction('&New Project', self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip('Create a new project')
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)

        # Open file
        open_action = QAction('&Open Data File...', self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip('Open assay data file')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Recent files
        file_menu.addSeparator()
        self.recent_files_menu = file_menu.addMenu('Recent Files')

        # Save project
        save_action = QAction('&Save Project', self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip('Save current project')
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        # Export results
        file_menu.addSeparator()
        export_action = QAction('&Export Results...', self)
        export_action.setStatusTip('Export analysis results')
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)

        # Exit
        file_menu.addSeparator()
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu('&Edit')

        # Undo/Redo
        undo_action = QAction('&Undo', self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.setStatusTip('Undo last action')
        edit_menu.addAction(undo_action)

        redo_action = QAction('&Redo', self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.setStatusTip('Redo last action')
        edit_menu.addAction(redo_action)

        # View menu
        view_menu = menubar.addMenu('&View')

        # Panel visibility
        toggle_data_action = QAction('&Data Panel', self)
        toggle_data_action.setCheckable(True)
        toggle_data_action.setChecked(True)
        toggle_data_action.triggered.connect(self.toggle_data_panel)
        view_menu.addAction(toggle_data_action)

        toggle_analysis_action = QAction('&Analysis Panel', self)
        toggle_analysis_action.setCheckable(True)
        toggle_analysis_action.setChecked(True)
        toggle_analysis_action.triggered.connect(self.toggle_analysis_panel)
        view_menu.addAction(toggle_analysis_action)

        toggle_visualization_action = QAction('&Visualization Panel', self)
        toggle_visualization_action.setCheckable(True)
        toggle_visualization_action.setChecked(True)
        toggle_visualization_action.triggered.connect(self.toggle_visualization_panel)
        view_menu.addAction(toggle_visualization_action)

        # Analysis menu
        analysis_menu = menubar.addMenu('&Analysis')

        # Run analysis
        run_analysis_action = QAction('&Run Analysis', self)
        run_analysis_action.setShortcut('F5')
        run_analysis_action.setStatusTip('Run QAQC analysis')
        run_analysis_action.triggered.connect(self.run_analysis)
        analysis_menu.addAction(run_analysis_action)

        # Configure analysis
        config_analysis_action = QAction('&Configure Analysis...', self)
        config_analysis_action.setStatusTip('Configure analysis parameters')
        config_analysis_action.triggered.connect(self.configure_analysis)
        analysis_menu.addAction(config_analysis_action)

        # Tools menu
        tools_menu = menubar.addMenu('&Tools')

        # CRM Management
        crm_action = QAction('&CRM Management...', self)
        crm_action.setStatusTip('Manage Certified Reference Materials')
        crm_action.triggered.connect(self.manage_crms)
        tools_menu.addAction(crm_action)

        # Settings
        settings_action = QAction('&Settings...', self)
        settings_action.setStatusTip('Application settings')
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu('&Help')

        # User Guide
        guide_action = QAction('&User Guide', self)
        guide_action.setStatusTip('Open user guide')
        guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(guide_action)

        # About
        about_action = QAction('&About', self)
        about_action.setStatusTip('About QAQC Analysis Application')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Create the application toolbar."""
        toolbar = self.addToolBar('Main Toolbar')
        toolbar.setMovable(False)

        # Import data
        import_action = QAction('Import Data', self)
        import_action.setStatusTip('Import assay data file')
        import_action.triggered.connect(self.open_file)
        toolbar.addAction(import_action)

        toolbar.addSeparator()

        # Run analysis
        analyze_action = QAction('Run Analysis', self)
        analyze_action.setStatusTip('Run QAQC analysis')
        analyze_action.triggered.connect(self.run_analysis)
        toolbar.addAction(analyze_action)

        # Export results
        export_action = QAction('Export Results', self)
        export_action.setStatusTip('Export analysis results')
        export_action.triggered.connect(self.export_results)
        toolbar.addAction(export_action)

        toolbar.addSeparator()

        # Settings
        settings_action = QAction('Settings', self)
        settings_action.setStatusTip('Application settings')
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)

    def create_status_bar(self):
        """Create the application status bar."""
        self.status_bar = self.statusBar()

        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Data info label
        self.data_info_label = QLabel("No data loaded")
        self.status_bar.addPermanentWidget(self.data_info_label)

    def setup_connections(self):
        """Set up signal connections between components."""
        # Connect data panel signals
        self.data_panel.data_loaded.connect(self.on_data_loaded)
        self.data_panel.data_changed.connect(self.on_data_changed)
        self.data_panel.column_mapping_changed.connect(self.on_column_mapping_changed)
        self.data_panel.analysis_requested.connect(self.on_analysis_requested)
        self.data_panel.configuration_changed.connect(self.on_configuration_changed)

        self.analysis_panel.analysis_requested.connect(self.on_analysis_requested)
        self.analysis_panel.configuration_changed.connect(self.on_configuration_changed)
        self.analysis_panel.results_ready.connect(self.on_analysis_results)

        # Connect visualization panel signals
        self.visualization_panel.plot_requested.connect(self.on_plot_requested)
        self.visualization_panel.export_requested.connect(self.on_export_requested)

    def apply_theme(self):
        """Apply the geological theme to the application."""
        theme = GeologicalTheme()
        self.setStyleSheet(theme.get_main_style())

        # Apply theme to all child widgets
        self.apply_theme_to_children(self)

    def apply_theme_to_children(self, widget):
        """Apply theme to all child widgets recursively."""
        for child in widget.findChildren(QWidget):
            if hasattr(child, 'setStyleSheet'):
                # Apply specific styling for different widget types
                if isinstance(child, QMessageBox):
                    child.setStyleSheet(self.get_dialog_style())
                elif hasattr(child, 'setStyleSheet'):
                    child.setStyleSheet("")

    def get_dialog_style(self):
        """Get specific styling for dialogs."""
        return """
        QMessageBox {
            background-color: #FFFFFF;
            color: #1A1A1A;
        }
        QMessageBox QPushButton {
            background-color: #2E5266;
            color: #FFFFFF;
            border: 2px solid #2E5266;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 12px;
            min-width: 100px;
            min-height: 30px;
        }
        QMessageBox QPushButton:hover {
            background-color: #4A7C59;
            border-color: #4A7C59;
            color: #FFFFFF;
        }
        QMessageBox QPushButton:pressed {
            background-color: #1A3A4A;
            border-color: #1A3A4A;
            color: #FFFFFF;
        }
        """

    def show_styled_message(self, title, message, msg_type=QMessageBox.Icon.Information):
        """Show a message box with proper styling."""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(msg_type)
        msg.setStyleSheet(self.get_dialog_style())
        return msg.exec()

    def center_window(self):
        """Center the window on the screen."""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    # Menu action handlers
    def new_project(self):
        """Create a new project."""
        if self.ask_save_changes():
            self.reset_application()

    def open_file(self):
        """Open a data file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Assay Data File",
            "",
            "CSV Files (*.csv);;Excel Files (*.xlsx *.xls);;All Files (*)"
        )

        if file_path:
            self.load_data_file(file_path)

    def save_project(self):
        """Save the current project."""
        # TODO: Implement project saving
        QMessageBox.information(self, "Save Project", "Project saving not yet implemented.")

    def export_results(self):
        """Export analysis results."""
        if not self.analysis_results:
            QMessageBox.warning(self, "No Results", "No analysis results to export.")
            return
        if not self.current_data or 'dataframe' not in self.current_data:
            QMessageBox.warning(self, "No Data", "Raw data is unavailable for export.")
            return

        dialog = QMessageBox(self)
        dialog.setWindowTitle("Export QAQC Results")
        dialog.setText("Select the report format to export.")
        excel_button = dialog.addButton("Excel (.xlsx)", QMessageBox.ButtonRole.AcceptRole)
        pdf_button = dialog.addButton("PDF (.pdf)", QMessageBox.ButtonRole.AcceptRole)
        both_button = dialog.addButton("Excel + PDF", QMessageBox.ButtonRole.AcceptRole)
        cancel_button = dialog.addButton(QMessageBox.StandardButton.Cancel)
        dialog.exec()

        clicked = dialog.clickedButton()
        if clicked == cancel_button or clicked is None:
            return

        export_excel = clicked in (excel_button, both_button)
        export_pdf = clicked in (pdf_button, both_button)

        exported_paths = []

        if export_excel:
            path = self._export_excel_report()
            if path:
                exported_paths.append(path)

        if export_pdf:
            path = self._export_pdf_report()
            if path:
                exported_paths.append(path)

        if exported_paths:
            message = "Export completed successfully:\n\n" + "\n".join(exported_paths)
            QMessageBox.information(self, "Export Successful", message)

    def _export_excel_report(self) -> Optional[str]:
        """Export Excel report and return generated path."""
        default_filename = self.output_dir / "qaqc_report.xlsx"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Excel Report",
            str(default_filename),
            "Excel Report (*.xlsx)"
        )

        if not filename:
            return None

        filename_path = Path(filename)
        if filename_path.suffix.lower() != ".xlsx":
            filename_path = filename_path.with_suffix(".xlsx")

        raw_data = {'data': self.current_data['dataframe']}

        try:
            generated_path = self.excel_reporter.generate_excel_report(
                self.analysis_results,
                raw_data=raw_data,
                filename=str(filename_path)
            )
            return generated_path
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to generate Excel report:\n{exc}"
            )
            return None

    def _export_pdf_report(self) -> Optional[str]:
        """Export PDF report and return generated path."""
        default_filename = self.output_dir / "qaqc_report.pdf"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export PDF Report",
            str(default_filename),
            "PDF Report (*.pdf)"
        )

        if not filename:
            return None

        filename_path = Path(filename)
        if filename_path.suffix.lower() != ".pdf":
            filename_path = filename_path.with_suffix(".pdf")

        plots_summary = None
        if hasattr(self.visualization_panel, 'plot_info_label'):
            summary_text = self.visualization_panel.plot_info_label.text()
            if summary_text:
                plots_summary = {
                    'Plot Summary': {
                        'description': summary_text
                    }
                }

        try:
            generated_path = self.pdf_reporter.generate_pdf_report(
                self.analysis_results,
                plots=plots_summary,
                filename=str(filename_path)
            )
            return generated_path
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to generate PDF report:\n{exc}"
            )
            return None

    def run_analysis(self):
        """Run QAQC analysis."""
        if not self.current_data:
            QMessageBox.warning(self, "No Data", "Please load data before running analysis.")
            return

        # Trigger analysis via analysis panel
        self.analysis_panel.run_analysis()

    def configure_analysis(self):
        """Configure analysis parameters."""
        # TODO: Implement analysis configuration dialog
        QMessageBox.information(self, "Configure Analysis", "Analysis configuration not yet implemented.")

    def manage_crms(self):
        """Manage Certified Reference Materials."""
        # TODO: Implement CRM management dialog
        QMessageBox.information(self, "CRM Management", "CRM management not yet implemented.")

    def show_settings(self):
        """Show application settings."""
        # TODO: Implement settings dialog
        QMessageBox.information(self, "Settings", "Settings dialog not yet implemented.")

    def show_user_guide(self):
        """Show user guide."""
        # TODO: Implement user guide
        QMessageBox.information(self, "User Guide", "User guide not yet implemented.")

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About QAQC Analysis Application",
            """
            <h3>QAQC Analysis Application</h3>
            <p>Version 2.0.0</p>
            <p>Professional QAQC analysis tool for geologists and mining engineers.</p>
            <p>Designed for assay data analysis with comprehensive reporting capabilities.</p>
            """
        )

    # Panel visibility handlers
    def toggle_data_panel(self, visible):
        """Toggle data panel visibility."""
        self.data_panel.setVisible(visible)

    def toggle_analysis_panel(self, visible):
        """Toggle analysis panel visibility."""
        self.analysis_panel.setVisible(visible)

    def toggle_visualization_panel(self, visible):
        """Toggle visualization panel visibility."""
        self.visualization_panel.setVisible(visible)

    # Signal handlers
    def on_data_loaded(self, data_info):
        """Handle data loaded signal."""
        self.current_data = data_info
        self.update_data_info()
        self.status_label.setText("Data loaded successfully")

        # Pass data to analysis panel
        if hasattr(self, 'analysis_panel'):
            self.analysis_panel.set_data_info(data_info)

        # Pass data to visualization panel only if there's valid data
        if hasattr(self, 'visualization_panel'):
            # Check for dataframe in data_info
            if data_info and 'dataframe' in data_info and not data_info['dataframe'].empty:
                # Create plot data structure
                plot_data = {
                    'data': data_info['dataframe'],
                    'dataframe': data_info['dataframe'],
                    'file_name': data_info.get('file_name', 'Unknown'),
                    'sample_count': data_info.get('sample_count', 0)
                }
                self.visualization_panel.set_plot_data(plot_data)
            elif data_info and 'data' in data_info and not data_info['data'].empty:
                self.visualization_panel.set_plot_data(data_info)
            else:
                self.visualization_panel.set_plot_data(None)
                self.visualization_panel.reset()  # Reset the panel when no data

    def on_data_changed(self, data_info):
        """Handle data changed signal."""
        self.current_data = data_info
        self.update_data_info()

        if hasattr(self, 'analysis_panel'):
            self.analysis_panel.set_data_info(data_info)

    def on_analysis_requested(self, configuration):
        """Handle analysis requested signal."""
        self.run_analysis_with_config(configuration)

    def on_configuration_changed(self, configuration):
        """Handle configuration changed signal."""
        self.config = configuration

    def on_analysis_results(self, results):
        """Handle analysis results and update visualization panel."""
        self.analysis_results = results
        if hasattr(self, 'visualization_panel'):
            self.visualization_panel.set_analysis_results(results)
        self.status_label.setText("Analysis results available")

    def on_plot_requested(self, plot_type):
        """Handle plot requested signal."""
        # TODO: Implement plot generation
        pass

    def on_export_requested(self, export_type):
        """Handle export requested signal."""
        # TODO: Implement export functionality
        pass

    # Helper methods
    def load_data_file(self, file_path):
        """Load data from file."""
        try:
            self.status_label.setText("Loading data...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress

            # TODO: Implement actual data loading
            # This would integrate with the existing DataImporter

            self.current_file = file_path
            self.status_label.setText("Data loaded successfully")
            self.progress_bar.setVisible(False)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            self.status_label.setText("Error loading data")
            self.progress_bar.setVisible(False)

    def run_analysis_with_config(self, configuration):
        """Run analysis with given configuration."""
        # Store configuration and trigger analysis
        self.config = configuration
        if self.current_data:
            self.analysis_panel.run_analysis()

    def update_data_info(self):
        """Update data information in status bar."""
        if self.current_data:
            dataframe = self.current_data.get('dataframe')
            if dataframe is not None:
                self.data_info_label.setText(
                    f"Samples: {len(dataframe)} | Columns: {len(dataframe.columns)}"
                )
            else:
                self.data_info_label.setText("Data loaded")
        else:
            self.data_info_label.setText("No data loaded")

    def reset_application(self):
        """Reset application to initial state."""
        self.current_file = None
        self.current_data = None
        self.analysis_results = None
        self.config = {}

        # Reset panels
        self.data_panel.reset()
        self.analysis_panel.reset()
        self.visualization_panel.reset()

        # Update status
        self.status_label.setText("Ready")
        self.data_info_label.setText("No data loaded")

    def ask_save_changes(self):
        """Ask user if they want to save changes."""
        # TODO: Implement change detection and save prompt
        return True


def main():
    """Main entry point for GUI application."""
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setApplicationName("QAQC Analysis Application")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("QAQC Analysis")

    window = QAQCApplication()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
