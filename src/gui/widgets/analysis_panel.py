"""
Analysis Panel Widget

This widget handles analysis configuration and execution for the
QAQC Analysis Application. Designed for geologists working with assay data.
"""

from typing import Optional, Dict, Any, List
from enum import Enum
from pathlib import Path
import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QGroupBox, QSpinBox, QDoubleSpinBox, QComboBox,
    QProgressBar, QTextEdit, QTabWidget, QFormLayout, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from ..styles.geological_theme import GeologicalTheme
from .green_checkbox import GreenCheckBox
from ...analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer
from ...data.crm_manager import CRMManager


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
        """Run analysis in separate thread using real analysis modules."""
        try:
            # Get dataframe from data_info
            df = self.data_info.get('dataframe')
            if df is None or df.empty:
                self.error_occurred.emit("No data available for analysis")
                return

            # Initialize analyzers with configuration
            config = self.configuration.get('analysis_config', {})
            standards_analyzer = StandardsAnalyzer(config.get('standards', {}))
            blanks_analyzer = BlanksAnalyzer(config.get('blanks', {}))
            duplicates_analyzer = DuplicatesAnalyzer(config.get('duplicates', {}))

            # Initialize CRM manager
            crm_db_path = self.configuration.get('crm_database', 'crm_database.yaml')
            crm_manager = None
            try:
                if crm_db_path:
                    crm_manager = CRMManager(crm_db_path)
            except FileNotFoundError:
                self.status_updated.emit(f"CRM database not found at {crm_db_path}")
                crm_manager = None
            except Exception as exc:
                self.status_updated.emit(f"CRM database error: {exc}")
                crm_manager = None

            self.status_updated.emit("Initializing analysis...")
            self.progress_updated.emit(10)

            results = {}
            df = df.copy()

            # Ensure result column is numeric
            if 'result' in df.columns:
                df['result'] = pd.to_numeric(df['result'], errors='coerce')

            # Find sample_type column (case-insensitive)
            type_col = None
            for col in df.columns:
                if col.lower() in ['sample_type', 'type', 'samp_type']:
                    type_col = col
                    break

            if not type_col:
                self.error_occurred.emit("Could not find sample_type column")
                return

            # Standards Analysis
            if self.configuration.get('standards_enabled', False):
                self.status_updated.emit("Running standards analysis...")
                self.progress_updated.emit(30)

                standards_data = self._prepare_standards_data(df, type_col, crm_manager)
                if standards_data:
                    standards_result = standards_analyzer.analyze_standards(standards_data)
                    results['standards'] = standards_result
                else:
                    results['standards'] = {'error': 'No standards data available or CRM not found'}

            # Blanks Analysis
            if self.configuration.get('blanks_enabled', False):
                self.status_updated.emit("Running blanks analysis...")
                self.progress_updated.emit(60)

                blanks_data = self._prepare_blanks_data(df, type_col)
                if blanks_data:
                    blanks_result = blanks_analyzer.analyze_blanks(blanks_data)
                    results['blanks'] = blanks_result
                else:
                    results['blanks'] = {'error': 'No blanks data available'}

            # Duplicates Analysis
            if self.configuration.get('duplicates_enabled', False):
                self.status_updated.emit("Running duplicates analysis...")
                self.progress_updated.emit(80)

                duplicates_data = self._prepare_duplicates_data(df, type_col)
                if duplicates_data:
                    duplicates_result = duplicates_analyzer.analyze_duplicates(duplicates_data)
                    results['duplicates'] = duplicates_result
                else:
                    results['duplicates'] = {'error': 'No duplicates data available'}

            # Add summary information
            results['total_samples'] = len(df)
            results['analysis_date'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

            self.progress_updated.emit(100)
            self.status_updated.emit("Analysis completed")
            self.analysis_completed.emit(results)

        except Exception as e:
            import traceback
            error_msg = f"Analysis error: {str(e)}\n{traceback.format_exc()}"
            self.error_occurred.emit(error_msg)

    def _prepare_standards_data(self, df, type_col, crm_manager):
        """Prepare data for standards analysis."""
        # Filter standards samples
        standards_df = df[df[type_col].str.upper().str.contains('STANDARD|STD|CRM', na=False, regex=True)].copy()
        if len(standards_df) == 0:
            return None

        # Get CRM information
        crm_name = self.configuration.get('crm_name')
        if not crm_name and crm_manager:
            # Auto-select CRM based on concentration
            mean_conc = standards_df['result'].mean()
            suitable_crms = crm_manager.get_crms_by_concentration_range(mean_conc * 0.5, mean_conc * 2.0)
            if suitable_crms:
                best_crm = min(suitable_crms, key=lambda x: abs(x['certified_value'] - mean_conc))
                crm_name = best_crm['name']

        if not crm_name or not crm_manager:
            return None

        # Get CRM data
        crm_info = crm_manager.get_crm_by_name(crm_name)
        if not crm_info:
            return None

        return {
            'measured': standards_df['result'].dropna().tolist(),
            'certified': crm_info.get('certified_value', 0),
            'uncertainty': crm_info.get('uncertainty', crm_info.get('certified_value', 0) * 0.05)
        }

    def _prepare_blanks_data(self, df, type_col):
        """Prepare data for blanks analysis."""
        blanks_df = df[df[type_col].str.upper().str.contains('BLANK|BLK', na=False, regex=True)].copy()
        if len(blanks_df) == 0:
            return None

        # Get previous samples for carry-over analysis (simplified)
        all_samples = df.sort_index()
        previous_samples = []
        if len(blanks_df) > 0:
            first_blank_idx = blanks_df.index.min()
            prev_samples = all_samples[all_samples.index < first_blank_idx]
            if 'result' in prev_samples.columns:
                previous_samples = prev_samples['result'].dropna().tolist()

        return {
            'blanks': blanks_df['result'].dropna().tolist(),
            'previous_samples': previous_samples
        }

    def _prepare_duplicates_data(self, df, type_col):
        """Prepare data for duplicates analysis."""
        # Find duplicate pairs
        duplicates_df = df[df[type_col].str.upper().str.contains('DUPLICATE|DUP|CHECK|CK', na=False, regex=True)].copy()
        if len(duplicates_df) < 2:
            return None

        # Simple pairing: split in half for now
        # In production, would pair by sample_id
        n = len(duplicates_df)
        mid = n // 2
        values = duplicates_df['result'].dropna().tolist()

        if len(values) < 2:
            return None

        # Create pairs from first and second half
        pairs = []
        for i in range(min(mid, len(values) - mid)):
            if i + mid < len(values):
                pairs.append([values[i], values[i + mid]])

        if not pairs:
            return None

        return {'duplicates': pairs}


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
        self.data_info: Optional[Dict[str, Any]] = None  # Store data info for analysis

        # Initialize UI
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()

    def set_data_info(self, data_info: Dict[str, Any]):
        """Set data info for analysis."""
        self.data_info = data_info

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

        # JORC Compliance tab
        self.jorc_tab = self.create_jorc_tab()
        self.params_tabs.addTab(self.jorc_tab, "JORC Compliance")

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

    def create_jorc_tab(self) -> QWidget:
        """Create JORC compliance parameters tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Insertion Rates Group - Use Grid Layout for compactness
        insertion_group = QGroupBox("JORC Insertion Rate Targets (%)")
        insertion_layout = QGridLayout(insertion_group)
        insertion_layout.setSpacing(10)

        # Standards
        insertion_layout.addWidget(QLabel("Standards:"), 0, 0)
        self.jorc_standards_spin = QDoubleSpinBox()
        self.jorc_standards_spin.setRange(0.0, 20.0)
        self.jorc_standards_spin.setValue(5.0)
        self.jorc_standards_spin.setDecimals(1)
        self.jorc_standards_spin.setSuffix("%")
        self.jorc_standards_spin.setToolTip("JORC recommended: ≥5%")
        insertion_layout.addWidget(self.jorc_standards_spin, 0, 1)

        # Blanks
        insertion_layout.addWidget(QLabel("Blanks:"), 0, 2)
        self.jorc_blanks_spin = QDoubleSpinBox()
        self.jorc_blanks_spin.setRange(0.0, 20.0)
        self.jorc_blanks_spin.setValue(5.0)
        self.jorc_blanks_spin.setDecimals(1)
        self.jorc_blanks_spin.setSuffix("%")
        self.jorc_blanks_spin.setToolTip("JORC recommended: ≥5%")
        insertion_layout.addWidget(self.jorc_blanks_spin, 0, 3)

        # Duplicates
        insertion_layout.addWidget(QLabel("Duplicates:"), 1, 0)
        self.jorc_duplicates_spin = QDoubleSpinBox()
        self.jorc_duplicates_spin.setRange(0.0, 20.0)
        self.jorc_duplicates_spin.setValue(5.0)
        self.jorc_duplicates_spin.setDecimals(1)
        self.jorc_duplicates_spin.setSuffix("%")
        self.jorc_duplicates_spin.setToolTip("JORC recommended: ≥5%")
        insertion_layout.addWidget(self.jorc_duplicates_spin, 1, 1)

        # Total QAQC
        insertion_layout.addWidget(QLabel("Total QAQC:"), 1, 2)
        self.jorc_total_spin = QDoubleSpinBox()
        self.jorc_total_spin.setRange(0.0, 50.0)
        self.jorc_total_spin.setValue(20.0)
        self.jorc_total_spin.setDecimals(1)
        self.jorc_total_spin.setSuffix("%")
        self.jorc_total_spin.setToolTip("JORC recommended: ≥20%")
        insertion_layout.addWidget(self.jorc_total_spin, 1, 3)

        # Use JORC Defaults button
        jorc_defaults_btn = QPushButton("Use JORC Defaults")
        jorc_defaults_btn.setToolTip("Set all rates to JORC recommended values (5%/5%/5%/20%)")
        jorc_defaults_btn.clicked.connect(self.set_jorc_defaults)
        insertion_layout.addWidget(jorc_defaults_btn, 2, 0, 1, 4)

        layout.addWidget(insertion_group)

        # Bottom section - Horizontal layout for Westgard and Precision
        bottom_layout = QHBoxLayout()
        
        # Westgard Rules Group
        westgard_group = QGroupBox("Westgard Rules")
        westgard_layout = QVBoxLayout(westgard_group)
        westgard_layout.setSpacing(8)

        self.westgard_enabled = GreenCheckBox("Enable Rules")
        self.westgard_enabled.setChecked(True)
        self.westgard_enabled.setToolTip("Enable process control rules for standards analysis")
        westgard_layout.addWidget(self.westgard_enabled)

        # Add info label
        info_label = QLabel("Rules: 1-3s, 2-2s,\nR-4s, 10-x")
        info_label.setStyleSheet("color: #607D8B; font-size: 10px; font-style: italic;")
        westgard_layout.addWidget(info_label)
        westgard_layout.addStretch()

        bottom_layout.addWidget(westgard_group)

        # Precision Method Group
        precision_group = QGroupBox("Precision Method")
        precision_layout = QFormLayout(precision_group)
        precision_layout.setSpacing(10)

        self.precision_method_combo = QComboBox()
        self.precision_method_combo.addItems(["Simple RPD", "Hyperbolic"])
        self.precision_method_combo.setCurrentIndex(1)  # Default to hyperbolic
        self.precision_method_combo.setToolTip("Hyperbolic method accounts for nugget effect")
        precision_layout.addRow("Method:", self.precision_method_combo)

        # Hyperbolic parameters
        self.hyperbolic_m_spin = QDoubleSpinBox()
        self.hyperbolic_m_spin.setRange(0.1, 5.0)
        self.hyperbolic_m_spin.setValue(1.0)
        self.hyperbolic_m_spin.setDecimals(2)
        self.hyperbolic_m_spin.setToolTip("Slope (m)")
        precision_layout.addRow("Slope (m):", self.hyperbolic_m_spin)

        self.hyperbolic_c_spin = QDoubleSpinBox()
        self.hyperbolic_c_spin.setRange(-2.0, 2.0)
        self.hyperbolic_c_spin.setValue(0.0)
        self.hyperbolic_c_spin.setDecimals(2)
        self.hyperbolic_c_spin.setToolTip("Intercept (c)")
        precision_layout.addRow("Intercept (c):", self.hyperbolic_c_spin)

        bottom_layout.addWidget(precision_group)
        
        layout.addLayout(bottom_layout)
        layout.addStretch()
        
        return tab
        self.hyperbolic_c_spin.setDecimals(2)
        self.hyperbolic_c_spin.setToolTip("Intercept parameter for hyperbolic curve")
        precision_layout.addRow("Hyperbolic C:", self.hyperbolic_c_spin)

        layout.addWidget(precision_group)

        layout.addStretch()
        return tab

    def set_jorc_defaults(self):
        """Set JORC default insertion rates."""
        self.jorc_standards_spin.setValue(5.0)
        self.jorc_blanks_spin.setValue(5.0)
        self.jorc_duplicates_spin.setValue(5.0)
        self.jorc_total_spin.setValue(20.0)

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

        # JORC parameter controls
        self.jorc_standards_spin.valueChanged.connect(self.on_configuration_changed)
        self.jorc_blanks_spin.valueChanged.connect(self.on_configuration_changed)
        self.jorc_duplicates_spin.valueChanged.connect(self.on_configuration_changed)
        self.jorc_total_spin.valueChanged.connect(self.on_configuration_changed)
        self.westgard_enabled.toggled.connect(self.on_configuration_changed)
        self.precision_method_combo.currentIndexChanged.connect(self.on_configuration_changed)
        self.hyperbolic_m_spin.valueChanged.connect(self.on_configuration_changed)
        self.hyperbolic_c_spin.valueChanged.connect(self.on_configuration_changed)

    def apply_theme(self):
        """Apply the geological theme."""
        theme = GeologicalTheme()
        self.setStyleSheet(theme.get_widget_style('analysis_panel'))

    def run_analysis(self):
        """Run QAQC analysis using real analysis modules."""
        if not self.standards_check.isChecked() and not self.blanks_check.isChecked() and not self.duplicates_check.isChecked():
            self.status_label.setText("Please select at least one analysis type")
            self.status_label.setStyleSheet("color: #E74C3C; font-weight: bold;")
            return

        # Check if data is available
        if not hasattr(self, 'data_info') or not self.data_info or 'dataframe' not in self.data_info:
            self.status_label.setText("Please load data before running analysis")
            self.status_label.setStyleSheet("color: #E74C3C; font-weight: bold;")
            return

        # Get current configuration
        configuration = self.get_current_configuration()

        # Emit analysis requested signal
        self.analysis_requested.emit(configuration)

        # Start analysis thread with real analysis
        self.status_label.setText("Starting analysis...")
        self.status_label.setStyleSheet("color: #F39C12; font-weight: bold;")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.run_button.setEnabled(False)

        # Create and start analysis thread
        self.analysis_thread = AnalysisThread(self.data_info, configuration)
        self.analysis_thread.analysis_completed.connect(self.on_analysis_completed)
        self.analysis_thread.progress_updated.connect(self.progress_bar.setValue)
        self.analysis_thread.status_updated.connect(self.status_label.setText)
        self.analysis_thread.error_occurred.connect(self.on_analysis_error)
        self.analysis_thread.start()

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
        """Update the results display with real analysis results."""
        display_text = "QAQC Analysis Results\n"
        display_text += "=" * 50 + "\n\n"

        # Skip metadata keys
        skip_keys = ['total_samples', 'analysis_date']

        for analysis_type, result in results.items():
            if analysis_type in skip_keys:
                continue

            if isinstance(result, dict) and 'error' in result:
                display_text += f"{analysis_type.upper()} ANALYSIS: ERROR\n"
                display_text += f"  • {result['error']}\n\n"
                continue

            # Get status from real analysis results
            if isinstance(result, dict):
                overall_acceptable = result.get('overall_acceptable', False)
                status = "PASS" if overall_acceptable else "FAIL"
                status_color = "✓" if status == "PASS" else "✗"

                display_text += f"{analysis_type.upper()} ANALYSIS: {status_color} {status}\n"

                if analysis_type == 'standards':
                    bias = result.get('bias', {})
                    recovery = result.get('recovery', {})
                    precision = result.get('precision', {})
                    summary = result.get('summary', {})

                    display_text += f"  • Measurements: {summary.get('n_measurements', 0)}\n"
                    display_text += f"  • Certified Value: {summary.get('certified_value', 0):.3f} g/t\n"
                    if bias.get('z_scores'):
                        z_scores = bias['z_scores']
                        display_text += f"  • Z-Scores: {[f'{z:.2f}' for z in z_scores[:5]]}{'...' if len(z_scores) > 5 else ''}\n"
                    display_text += f"  • Max Z-Score: {bias.get('max_z_score', 0):.2f}\n"
                    display_text += f"  • Mean Recovery: {recovery.get('mean_recovery', 0):.1f}%\n"
                    display_text += f"  • Precision (RSD): {precision.get('rsd', 0):.1f}%\n"

                elif analysis_type == 'blanks':
                    contamination = result.get('contamination', {})
                    carryover = result.get('carryover', {})
                    summary = result.get('summary', {})

                    display_text += f"  • Blanks Analyzed: {summary.get('n_blanks', 0)}\n"
                    display_text += f"  • MDL: {summary.get('mdl', 0):.4f} g/t\n"
                    contaminated = contamination.get('contaminated_samples', [])
                    display_text += f"  • Contaminated: {len(contaminated)} samples\n"
                    display_text += f"  • Contamination Rate: {contamination.get('contamination_rate', 0)*100:.1f}%\n"
                    display_text += f"  • Carry-over Detected: {'Yes' if carryover.get('carryover_detected', False) else 'No'}\n"

                elif analysis_type == 'duplicates':
                    precision = result.get('precision', {})
                    summary = result.get('summary', {})

                    display_text += f"  • Duplicate Pairs: {summary.get('n_duplicates', 0)}\n"
                    rpd_values = precision.get('rpd_values', [])
                    if rpd_values:
                        display_text += f"  • RPD Values: {[f'{r:.1f}%' for r in rpd_values[:5]]}{'...' if len(rpd_values) > 5 else ''}\n"
                    display_text += f"  • Mean RPD: {precision.get('mean_rpd', 0):.1f}%\n"
                    display_text += f"  • Max RPD: {precision.get('max_rpd', 0):.1f}%\n"
                    display_text += f"  • Nugget Ratio: {result.get('nugget_ratio', 0):.3f}\n"

                display_text += "\n"

        # Add summary
        if 'total_samples' in results:
            display_text += f"\nTotal Samples: {results['total_samples']}\n"
        if 'analysis_date' in results:
            display_text += f"Analysis Date: {results['analysis_date']}\n"

        self.results_display.setPlainText(display_text)

    def on_analysis_error(self, error_message: str):
        """Handle analysis error."""
        self.status_label.setText(f"Analysis error: {error_message[:50]}...")
        self.status_label.setStyleSheet("color: #E74C3C; font-weight: bold;")
        self.progress_bar.setVisible(False)
        self.run_button.setEnabled(True)

        # Show error in results display
        self.results_display.setPlainText(f"Analysis Error:\n{error_message}")

    def get_current_configuration(self) -> Dict[str, Any]:
        """Get current analysis configuration including analysis parameters."""
        return {
            'standards_enabled': self.standards_check.isChecked(),
            'blanks_enabled': self.blanks_check.isChecked(),
            'duplicates_enabled': self.duplicates_check.isChecked(),
            'crm_database': 'crm_database.yaml',  # Default CRM database path
            'crm_name': None,  # Can be set via UI later
            'analysis_config': {
                'standards': {
                    'z_score_threshold': self.z_score_spin.value(),
                    'recovery_limits': (self.recovery_min_spin.value(), self.recovery_max_spin.value()),
                    'precision_threshold': self.precision_spin.value(),
                    'westgard_enabled': self.westgard_enabled.isChecked() if hasattr(self, 'westgard_enabled') else True
                },
                'blanks': {
                    'contamination_threshold': self.contamination_spin.value(),
                    'carryover_threshold': self.carryover_spin.value(),
                    'blank_limit': self.blank_limit_spin.value()
                },
                'duplicates': {
                    'rpd_threshold': self.rpd_spin.value(),
                    'precision_limit': self.precision_limit_spin.value(),
                    'nugget_threshold': self.nugget_spin.value(),
                    'precision_method': 'hyperbolic' if hasattr(self, 'precision_method_combo') and self.precision_method_combo.currentIndex() == 1 else 'simple_rpd',
                    'hyperbolic_m': self.hyperbolic_m_spin.value() if hasattr(self, 'hyperbolic_m_spin') else 1.0,
                    'hyperbolic_c': self.hyperbolic_c_spin.value() if hasattr(self, 'hyperbolic_c_spin') else 0.0
                }
            },
            'jorc_settings': {
                'insertion_rates': {
                    'target_standards': self.jorc_standards_spin.value() if hasattr(self, 'jorc_standards_spin') else 5.0,
                    'target_blanks': self.jorc_blanks_spin.value() if hasattr(self, 'jorc_blanks_spin') else 5.0,
                    'target_duplicates': self.jorc_duplicates_spin.value() if hasattr(self, 'jorc_duplicates_spin') else 5.0,
                    'target_total': self.jorc_total_spin.value() if hasattr(self, 'jorc_total_spin') else 20.0
                },
                'westgard_enabled': self.westgard_enabled.isChecked() if hasattr(self, 'westgard_enabled') else True
            }
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
        self.data_info = None

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
