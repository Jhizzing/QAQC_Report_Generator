"""
Analysis Panel Widget

This widget handles analysis configuration and execution for the
QAQC Analysis Application. Designed for geologists working with assay data.
"""

from typing import Optional, Dict, Any, List
from enum import Enum

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QGroupBox, QSpinBox, QDoubleSpinBox, QComboBox,
    QProgressBar, QTextEdit, QTabWidget, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from ..styles.geological_theme import GeologicalTheme
from .green_checkbox import GreenCheckBox


class AnalysisType(Enum):
    """Analysis types for QAQC."""
    STANDARDS = "standards"
    BLANKS = "blanks"
    DUPLICATES = "duplicates"


class AnalysisThread(QThread):
    """Thread for analysis execution."""

    analysis_completed = pyqtSignal(dict)
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, data_info: Dict[str, Any], configuration: Dict[str, Any]):
        super().__init__()
        self.data_info = data_info
        self.configuration = configuration

    def run(self):
        """Run analysis in separate thread."""
        try:
            # TODO: Implement actual analysis using existing analysis modules
            # This is a placeholder for now

            # Simulate analysis progress
            self.status_updated.emit("Initializing analysis...")
            self.progress_updated.emit(10)
            self.msleep(500)

            self.status_updated.emit("Running standards analysis...")
            self.progress_updated.emit(30)
            self.msleep(1000)

            self.status_updated.emit("Running blanks analysis...")
            self.progress_updated.emit(60)
            self.msleep(1000)

            self.status_updated.emit("Running duplicates analysis...")
            self.progress_updated.emit(80)
            self.msleep(1000)

            self.status_updated.emit("Generating results...")
            self.progress_updated.emit(90)
            self.msleep(500)

            # Simulate analysis results
            results = {
                'standards': {
                    'enabled': self.configuration.get('standards_enabled', True),
                    'status': 'PASS',
                    'z_scores': [0.5, -0.8, 1.2, -0.3, 0.7],
                    'bias': 0.02,
                    'recovery': 98.5,
                    'precision': 2.1
                },
                'blanks': {
                    'enabled': self.configuration.get('blanks_enabled', True),
                    'status': 'FAIL',
                    'contamination_count': 2,
                    'carryover_detected': True,
                    'mdl': 0.008
                },
                'duplicates': {
                    'enabled': self.configuration.get('duplicates_enabled', True),
                    'status': 'PASS',
                    'rpd_values': [5.2, 8.1, 3.7, 6.9],
                    'precision': 7.1,
                    'correlation': 0.95
                }
            }

            self.progress_updated.emit(100)
            self.status_updated.emit("Analysis completed")
            self.analysis_completed.emit(results)

        except Exception as e:
            self.error_occurred.emit(str(e))


class AnalysisPanel(QWidget):
    """
    Analysis panel widget for configuring and executing QAQC analysis.

    Provides functionality for:
    - Analysis type selection (standards, blanks, duplicates)
    - Parameter configuration
    - Analysis execution and progress monitoring
    - Results display and interpretation
    """

    # Signals
    analysis_requested = pyqtSignal(dict)
    configuration_changed = pyqtSignal(dict)
    results_ready = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        # Analysis state
        self.current_configuration: Dict[str, Any] = {}
        self.current_results: Optional[Dict[str, Any]] = None
        self.analysis_thread: Optional[AnalysisThread] = None

        # Initialize UI
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()

    def setup_ui(self):
        """Set up the analysis panel user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Analysis configuration group
        self.config_group = QGroupBox("Analysis Configuration")
        config_layout = QVBoxLayout(self.config_group)

        # Analysis type checkboxes (using custom green checkboxes with visible ticks)
        self.standards_check = GreenCheckBox("Standards Analysis")
        self.standards_check.setChecked(True)
        self.standards_check.setStyleSheet("font-weight: bold; color: #2E5266;")
        config_layout.addWidget(self.standards_check)

        self.blanks_check = GreenCheckBox("Blanks Analysis")
        self.blanks_check.setChecked(True)
        self.blanks_check.setStyleSheet("font-weight: bold; color: #2E5266;")
        config_layout.addWidget(self.blanks_check)

        self.duplicates_check = GreenCheckBox("Duplicates Analysis")
        self.duplicates_check.setChecked(True)
        self.duplicates_check.setStyleSheet("font-weight: bold; color: #2E5266;")
        config_layout.addWidget(self.duplicates_check)

        layout.addWidget(self.config_group)

        # Analysis parameters tab widget
        self.params_tabs = QTabWidget()

        # Standards parameters tab
        self.standards_tab = self.create_standards_tab()
        self.params_tabs.addTab(self.standards_tab, "Standards")

        # Blanks parameters tab
        self.blanks_tab = self.create_blanks_tab()
        self.params_tabs.addTab(self.blanks_tab, "Blanks")

        # Duplicates parameters tab
        self.duplicates_tab = self.create_duplicates_tab()
        self.params_tabs.addTab(self.duplicates_tab, "Duplicates")

        layout.addWidget(self.params_tabs)

        # Analysis execution group
        self.execution_group = QGroupBox("Analysis Execution")
        exec_layout = QVBoxLayout(self.execution_group)

        # Run analysis button
        self.run_button = QPushButton("Run QAQC Analysis")
        self.run_button.setMinimumHeight(40)
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #2E5266;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4A7C59;
            }
            QPushButton:disabled {
                background-color: #ADB5BD;
            }
        """)
        exec_layout.addWidget(self.run_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        exec_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready to run analysis")
        self.status_label.setStyleSheet("color: #27AE60; font-weight: bold;")
        exec_layout.addWidget(self.status_label)

        layout.addWidget(self.execution_group)

        # Results summary group
        self.results_group = QGroupBox("Analysis Results")
        results_layout = QVBoxLayout(self.results_group)

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setMaximumHeight(150)
        self.results_display.setReadOnly(True)
        self.results_display.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 1px solid #DEE2E6;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 10px;
            }
        """)
        results_layout.addWidget(self.results_display)

        layout.addWidget(self.results_group)

    def create_standards_tab(self) -> QWidget:
        """Create standards analysis parameters tab."""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)

        # Z-score threshold
        self.z_score_spin = QDoubleSpinBox()
        self.z_score_spin.setRange(1.0, 5.0)
        self.z_score_spin.setValue(2.0)
        self.z_score_spin.setDecimals(1)
        self.z_score_spin.setSuffix(" σ")
        layout.addRow("Z-Score Threshold:", self.z_score_spin)

        # Recovery limits
        self.recovery_min_spin = QDoubleSpinBox()
        self.recovery_min_spin.setRange(80.0, 100.0)
        self.recovery_min_spin.setValue(95.0)
        self.recovery_min_spin.setDecimals(1)
        self.recovery_min_spin.setSuffix("%")
        layout.addRow("Min Recovery:", self.recovery_min_spin)

        self.recovery_max_spin = QDoubleSpinBox()
        self.recovery_max_spin.setRange(100.0, 120.0)
        self.recovery_max_spin.setValue(105.0)
        self.recovery_max_spin.setDecimals(1)
        self.recovery_max_spin.setSuffix("%")
        layout.addRow("Max Recovery:", self.recovery_max_spin)

        # Precision threshold
        self.precision_spin = QDoubleSpinBox()
        self.precision_spin.setRange(1.0, 20.0)
        self.precision_spin.setValue(5.0)
        self.precision_spin.setDecimals(1)
        self.precision_spin.setSuffix("%")
        layout.addRow("Precision Threshold:", self.precision_spin)

        return tab

    def create_blanks_tab(self) -> QWidget:
        """Create blanks analysis parameters tab."""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)

        # Contamination threshold
        self.contamination_spin = QDoubleSpinBox()
        self.contamination_spin.setRange(1.0, 10.0)
        self.contamination_spin.setValue(3.0)
        self.contamination_spin.setDecimals(1)
        self.contamination_spin.setSuffix(" × DL")
        layout.addRow("Contamination Threshold:", self.contamination_spin)

        # Carry-over threshold
        self.carryover_spin = QDoubleSpinBox()
        self.carryover_spin.setRange(1.0, 5.0)
        self.carryover_spin.setValue(2.0)
        self.carryover_spin.setDecimals(1)
        self.carryover_spin.setSuffix(" × DL")
        layout.addRow("Carry-over Threshold:", self.carryover_spin)

        # Blank limit
        self.blank_limit_spin = QDoubleSpinBox()
        self.blank_limit_spin.setRange(0.001, 0.1)
        self.blank_limit_spin.setValue(0.01)
        self.blank_limit_spin.setDecimals(3)
        self.blank_limit_spin.setSuffix(" g/t")
        layout.addRow("Blank Limit:", self.blank_limit_spin)

        return tab

    def create_duplicates_tab(self) -> QWidget:
        """Create duplicates analysis parameters tab."""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)

        # RPD threshold
        self.rpd_spin = QDoubleSpinBox()
        self.rpd_spin.setRange(5.0, 50.0)
        self.rpd_spin.setValue(20.0)
        self.rpd_spin.setDecimals(1)
        self.rpd_spin.setSuffix("%")
        layout.addRow("RPD Threshold:", self.rpd_spin)

        # Precision limit
        self.precision_limit_spin = QDoubleSpinBox()
        self.precision_limit_spin.setRange(1.0, 20.0)
        self.precision_limit_spin.setValue(10.0)
        self.precision_limit_spin.setDecimals(1)
        self.precision_limit_spin.setSuffix("%")
        layout.addRow("Precision Limit:", self.precision_limit_spin)

        # Nugget threshold
        self.nugget_spin = QDoubleSpinBox()
        self.nugget_spin.setRange(0.1, 2.0)
        self.nugget_spin.setValue(0.5)
        self.nugget_spin.setDecimals(1)
        layout.addRow("Nugget Threshold:", self.nugget_spin)

        return tab

    def setup_connections(self):
        """Set up signal connections."""
        self.run_button.clicked.connect(self.run_analysis)

        # Analysis type checkboxes
        self.standards_check.toggled.connect(self.on_configuration_changed)
        self.blanks_check.toggled.connect(self.on_configuration_changed)
        self.duplicates_check.toggled.connect(self.on_configuration_changed)

        # Parameter controls
        self.z_score_spin.valueChanged.connect(self.on_configuration_changed)
        self.recovery_min_spin.valueChanged.connect(self.on_configuration_changed)
        self.recovery_max_spin.valueChanged.connect(self.on_configuration_changed)
        self.precision_spin.valueChanged.connect(self.on_configuration_changed)
        self.contamination_spin.valueChanged.connect(self.on_configuration_changed)
        self.carryover_spin.valueChanged.connect(self.on_configuration_changed)
        self.blank_limit_spin.valueChanged.connect(self.on_configuration_changed)
        self.rpd_spin.valueChanged.connect(self.on_configuration_changed)
        self.precision_limit_spin.valueChanged.connect(self.on_configuration_changed)
        self.nugget_spin.valueChanged.connect(self.on_configuration_changed)

    def apply_theme(self):
        """Apply the geological theme."""
        theme = GeologicalTheme()
        self.setStyleSheet(theme.get_widget_style('analysis_panel'))

    def run_analysis(self):
        """Run QAQC analysis."""
        if not self.standards_check.isChecked() and not self.blanks_check.isChecked() and not self.duplicates_check.isChecked():
            self.status_label.setText("Please select at least one analysis type")
            self.status_label.setStyleSheet("color: #E74C3C; font-weight: bold;")
            return

        # Get current configuration
        configuration = self.get_current_configuration()

        # Emit analysis requested signal
        self.analysis_requested.emit(configuration)

        # Start analysis thread (placeholder)
        self.status_label.setText("Starting analysis...")
        self.status_label.setStyleSheet("color: #F39C12; font-weight: bold;")
        self.progress_bar.setVisible(True)
        self.run_button.setEnabled(False)

        # TODO: Implement actual analysis execution
        # This would integrate with the existing analysis modules

        # Simulate analysis completion
        self.simulate_analysis_completion()

    def simulate_analysis_completion(self):
        """Simulate analysis completion for demonstration."""
        # This is a placeholder - in real implementation, this would be handled by the analysis thread

        # Simulate results
        results = {
            'standards': {
                'enabled': self.standards_check.isChecked(),
                'status': 'PASS',
                'z_scores': [0.5, -0.8, 1.2, -0.3, 0.7],
                'bias': 0.02,
                'recovery': 98.5,
                'precision': 2.1
            },
            'blanks': {
                'enabled': self.blanks_check.isChecked(),
                'status': 'FAIL',
                'contamination_count': 2,
                'carryover_detected': True,
                'mdl': 0.008
            },
            'duplicates': {
                'enabled': self.duplicates_check.isChecked(),
                'status': 'PASS',
                'rpd_values': [5.2, 8.1, 3.7, 6.9],
                'precision': 7.1,
                'correlation': 0.95
            }
        }

        self.on_analysis_completed(results)

    def on_analysis_completed(self, results: Dict[str, Any]):
        """Handle analysis completion."""
        self.current_results = results

        # Update results display
        self.update_results_display(results)

        # Update status
        self.status_label.setText("Analysis completed successfully")
        self.status_label.setStyleSheet("color: #27AE60; font-weight: bold;")
        self.progress_bar.setVisible(False)
        self.run_button.setEnabled(True)

        # Emit results ready signal
        self.results_ready.emit(results)

    def update_results_display(self, results: Dict[str, Any]):
        """Update the results display."""
        display_text = "QAQC Analysis Results\n"
        display_text += "=" * 50 + "\n\n"

        for analysis_type, result in results.items():
            if result.get('enabled', False):
                status = result.get('status', 'UNKNOWN')
                status_color = "✓" if status == "PASS" else "✗"

                display_text += f"{analysis_type.upper()} ANALYSIS: {status_color} {status}\n"

                if analysis_type == 'standards':
                    display_text += f"  • Z-Scores: {result.get('z_scores', [])}\n"
                    display_text += f"  • Bias: {result.get('bias', 0):.3f}\n"
                    display_text += f"  • Recovery: {result.get('recovery', 0):.1f}%\n"
                    display_text += f"  • Precision: {result.get('precision', 0):.1f}%\n"

                elif analysis_type == 'blanks':
                    display_text += f"  • Contamination: {result.get('contamination_count', 0)} samples\n"
                    display_text += f"  • Carry-over: {'Yes' if result.get('carryover_detected', False) else 'No'}\n"
                    display_text += f"  • MDL: {result.get('mdl', 0):.3f} g/t\n"

                elif analysis_type == 'duplicates':
                    display_text += f"  • RPD Values: {result.get('rpd_values', [])}\n"
                    display_text += f"  • Precision: {result.get('precision', 0):.1f}%\n"
                    display_text += f"  • Correlation: {result.get('correlation', 0):.2f}\n"

                display_text += "\n"

        self.results_display.setPlainText(display_text)

    def get_current_configuration(self) -> Dict[str, Any]:
        """Get current analysis configuration."""
        return {
            'standards_enabled': self.standards_check.isChecked(),
            'blanks_enabled': self.blanks_check.isChecked(),
            'duplicates_enabled': self.duplicates_check.isChecked(),
            'z_score_threshold': self.z_score_spin.value(),
            'recovery_limits': [self.recovery_min_spin.value(), self.recovery_max_spin.value()],
            'precision_threshold': self.precision_spin.value(),
            'contamination_threshold': self.contamination_spin.value(),
            'carryover_threshold': self.carryover_spin.value(),
            'blank_limit': self.blank_limit_spin.value(),
            'rpd_threshold': self.rpd_spin.value(),
            'precision_limit': self.precision_limit_spin.value(),
            'nugget_threshold': self.nugget_spin.value()
        }

    def on_configuration_changed(self):
        """Handle configuration changes."""
        configuration = self.get_current_configuration()
        self.current_configuration = configuration
        self.configuration_changed.emit(configuration)

    def reset(self):
        """Reset the analysis panel to initial state."""
        self.current_configuration = {}
        self.current_results = None

        # Reset checkboxes
        self.standards_check.setChecked(True)
        self.blanks_check.setChecked(True)
        self.duplicates_check.setChecked(True)

        # Reset parameters to defaults
        self.z_score_spin.setValue(2.0)
        self.recovery_min_spin.setValue(95.0)
        self.recovery_max_spin.setValue(105.0)
        self.precision_spin.setValue(5.0)
        self.contamination_spin.setValue(3.0)
        self.carryover_spin.setValue(2.0)
        self.blank_limit_spin.setValue(0.01)
        self.rpd_spin.setValue(20.0)
        self.precision_limit_spin.setValue(10.0)
        self.nugget_spin.setValue(0.5)

        # Reset display
        self.results_display.clear()
        self.status_label.setText("Ready to run analysis")
        self.status_label.setStyleSheet("color: #27AE60; font-weight: bold;")
        self.progress_bar.setVisible(False)
        self.run_button.setEnabled(True)
