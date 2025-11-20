"""
Settings Dialog

Provides a comprehensive settings/preferences dialog for the QAQC Analysis Application.
"""

from typing import Optional
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QComboBox, QCheckBox, QSpinBox, QPushButton,
    QGroupBox, QFormLayout, QFileDialog, QDialogButtonBox,
    QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ...core.settings_manager import SettingsManager


class SettingsDialog(QDialog):
    """
    Settings dialog for configuring application preferences.
    
    Provides tabbed interface for different setting categories.
    """
    
    settings_changed = pyqtSignal()
    theme_changed = pyqtSignal(str)  # Emits theme name
    
    def __init__(self, settings_manager: SettingsManager, parent=None):
        super().__init__(parent)
        self.settings = settings_manager
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 500)
        self.setModal(True)
        
        self.setup_ui()
        self.load_current_settings()
        
    def setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Add tabs
        self.tabs.addTab(self.create_appearance_tab(), "Appearance")
        self.tabs.addTab(self.create_data_tab(), "Data & Files")
        self.tabs.addTab(self.create_analysis_tab(), "Analysis")
        self.tabs.addTab(self.create_visualization_tab(), "Visualization")
        self.tabs.addTab(self.create_performance_tab(), "Performance")
        self.tabs.addTab(self.create_advanced_tab(), "Advanced")
        
        layout.addWidget(self.tabs)
        
        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Apply |
            QDialogButtonBox.StandardButton.RestoreDefaults
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_settings)
        button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(self.restore_defaults)
        
        layout.addWidget(button_box)
    
    def create_appearance_tab(self) -> QWidget:
        """Create appearance settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Theme group
        theme_group = QGroupBox("Theme")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto (Follow System)"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_preview)
        theme_layout.addRow("Color Theme:", self.theme_combo)
        
        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems(["Geological", "Professional", "High Contrast"])
        theme_layout.addRow("Color Scheme:", self.color_scheme_combo)
        
        layout.addWidget(theme_group)
        
        # UI group
        ui_group = QGroupBox("User Interface")
        ui_layout = QFormLayout(ui_group)
        
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Small", "Medium", "Large", "Extra Large"])
        ui_layout.addRow("Font Size:", self.font_size_combo)
        
        self.compact_mode_check = QCheckBox("Enable compact mode")
        ui_layout.addRow("", self.compact_mode_check)
        
        layout.addWidget(ui_group)
        layout.addStretch()
        
        return tab
    
    def create_data_tab(self) -> QWidget:
        """Create data & files settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Directories group
        dirs_group = QGroupBox("Default Directories")
        dirs_layout = QFormLayout(dirs_group)
        
        # Input directory
        input_layout = QHBoxLayout()
        self.input_dir_edit = QLineEdit()
        input_browse_btn = QPushButton("Browse...")
        input_browse_btn.clicked.connect(lambda: self.browse_directory(self.input_dir_edit))
        input_layout.addWidget(self.input_dir_edit)
        input_layout.addWidget(input_browse_btn)
        dirs_layout.addRow("Input:", input_layout)
        
        # Output directory
        output_layout = QHBoxLayout()
        self.output_dir_edit = QLineEdit()
        output_browse_btn = QPushButton("Browse...")
        output_browse_btn.clicked.connect(lambda: self.browse_directory(self.output_dir_edit))
        output_layout.addWidget(self.output_dir_edit)
        output_layout.addWidget(output_browse_btn)
        dirs_layout.addRow("Output:", output_layout)
        
        layout.addWidget(dirs_group)
        
        # Auto-save group
        autosave_group = QGroupBox("Auto-Save")
        autosave_layout = QFormLayout(autosave_group)
        
        self.autosave_check = QCheckBox("Enable auto-save")
        autosave_layout.addRow("", self.autosave_check)
        
        self.autosave_interval_spin = QSpinBox()
        self.autosave_interval_spin.setRange(1, 60)
        self.autosave_interval_spin.setSuffix(" minutes")
        autosave_layout.addRow("Interval:", self.autosave_interval_spin)
        
        layout.addWidget(autosave_group)
        
        # Files group
        files_group = QGroupBox("File Settings")
        files_layout = QFormLayout(files_group)
        
        self.recent_files_spin = QSpinBox()
        self.recent_files_spin.setRange(5, 20)
        files_layout.addRow("Recent Files:", self.recent_files_spin)
        
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["UTF-8", "ASCII", "Latin-1", "Windows-1252"])
        files_layout.addRow("Encoding:", self.encoding_combo)
        
        layout.addWidget(files_group)
        layout.addStretch()
        
        return tab
    
    def create_analysis_tab(self) -> QWidget:
        """Create analysis settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Analysis defaults group
        defaults_group = QGroupBox("Analysis Defaults")
        defaults_layout = QFormLayout(defaults_group)
        
        self.auto_run_check = QCheckBox("Auto-run analysis when data loads")
        defaults_layout.addRow("", self.auto_run_check)
        
        # CRM database
        crm_layout = QHBoxLayout()
        self.crm_db_edit = QLineEdit()
        crm_browse_btn = QPushButton("Browse...")
        crm_browse_btn.clicked.connect(lambda: self.browse_file(self.crm_db_edit, "YAML Files (*.yaml *.yml)"))
        crm_layout.addWidget(self.crm_db_edit)
        crm_layout.addWidget(crm_browse_btn)
        defaults_layout.addRow("CRM Database:", crm_layout)
        
        self.confidence_combo = QComboBox()
        self.confidence_combo.addItems(["90%", "95%", "99%"])
        defaults_layout.addRow("Confidence Level:", self.confidence_combo)
        
        self.decimal_spin = QSpinBox()
        self.decimal_spin.setRange(1, 5)
        defaults_layout.addRow("Decimal Places:", self.decimal_spin)
        
        self.missing_data_combo = QComboBox()
        self.missing_data_combo.addItems(["Skip", "Replace with 0", "Flag"])
        defaults_layout.addRow("Missing Data:", self.missing_data_combo)
        
        layout.addWidget(defaults_group)
        layout.addStretch()
        
        return tab
    
    def create_visualization_tab(self) -> QWidget:
        """Create visualization settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Plot defaults group
        plot_group = QGroupBox("Plot Defaults")
        plot_layout = QFormLayout(plot_group)
        
        self.dpi_combo = QComboBox()
        self.dpi_combo.addItems(["150", "200", "300", "600"])
        plot_layout.addRow("DPI:", self.dpi_combo)
        
        self.plot_style_combo = QComboBox()
        self.plot_style_combo.addItems(["seaborn-v0_8", "ggplot", "classic", "bmh"])
        plot_layout.addRow("Style:", self.plot_style_combo)
        
        self.colorblind_check = QCheckBox("Use colorblind-friendly palettes")
        plot_layout.addRow("", self.colorblind_check)
        
        self.gridlines_check = QCheckBox("Show gridlines by default")
        plot_layout.addRow("", self.gridlines_check)
        
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["PNG", "SVG", "PDF"])
        plot_layout.addRow("Export Format:", self.export_format_combo)
        
        layout.addWidget(plot_group)
        layout.addStretch()
        
        return tab
    
    def create_performance_tab(self) -> QWidget:
        """Create performance settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Performance group
        perf_group = QGroupBox("Performance")
        perf_layout = QFormLayout(perf_group)
        
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 16)
        perf_layout.addRow("Thread Count:", self.thread_spin)
        
        self.memory_spin = QSpinBox()
        self.memory_spin.setRange(512, 8192)
        self.memory_spin.setSuffix(" MB")
        self.memory_spin.setSingleStep(256)
        perf_layout.addRow("Memory Limit:", self.memory_spin)
        
        self.cache_spin = QSpinBox()
        self.cache_spin.setRange(64, 1024)
        self.cache_spin.setSuffix(" MB")
        self.cache_spin.setSingleStep(64)
        perf_layout.addRow("Cache Size:", self.cache_spin)
        
        self.logging_combo = QComboBox()
        self.logging_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        perf_layout.addRow("Logging Level:", self.logging_combo)
        
        layout.addWidget(perf_group)
        layout.addStretch()
        
        return tab
    
    def create_advanced_tab(self) -> QWidget:
        """Create advanced settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Advanced group
        adv_group = QGroupBox("Advanced")
        adv_layout = QVBoxLayout(adv_group)
        
        self.developer_check = QCheckBox("Enable developer mode")
        adv_layout.addWidget(self.developer_check)
        
        self.updates_check = QCheckBox("Check for updates on startup")
        adv_layout.addWidget(self.updates_check)
        
        self.analytics_check = QCheckBox("Send anonymous usage statistics")
        adv_layout.addWidget(self.analytics_check)
        
        layout.addWidget(adv_group)
        layout.addStretch()
        
        return tab
    
    def load_current_settings(self):
        """Load current settings into UI controls."""
        # Appearance
        theme_map = {"light": 0, "dark": 1, "auto": 2}
        self.theme_combo.setCurrentIndex(theme_map.get(self.settings.get("appearance/theme"), 0))
        
        scheme_map = {"geological": 0, "professional": 1, "high_contrast": 2}
        self.color_scheme_combo.setCurrentIndex(scheme_map.get(self.settings.get("appearance/color_scheme"), 0))
        
        font_map = {"small": 0, "medium": 1, "large": 2, "xlarge": 3}
        self.font_size_combo.setCurrentIndex(font_map.get(self.settings.get("appearance/font_size"), 1))
        
        self.compact_mode_check.setChecked(self.settings.get("appearance/compact_mode"))
        
        # Data & Files
        self.input_dir_edit.setText(self.settings.get("data/input_dir"))
        self.output_dir_edit.setText(self.settings.get("data/output_dir"))
        self.autosave_check.setChecked(self.settings.get("data/autosave_enabled"))
        self.autosave_interval_spin.setValue(self.settings.get("data/autosave_interval"))
        self.recent_files_spin.setValue(self.settings.get("data/recent_files_limit"))
        
        encoding_map = {"utf-8": 0, "ascii": 1, "latin-1": 2, "windows-1252": 3}
        self.encoding_combo.setCurrentIndex(encoding_map.get(self.settings.get("data/file_encoding").lower(), 0))
        
        # Analysis
        self.auto_run_check.setChecked(self.settings.get("analysis/auto_run"))
        self.crm_db_edit.setText(self.settings.get("analysis/crm_database"))
        
        conf_map = {0.90: 0, 0.95: 1, 0.99: 2}
        self.confidence_combo.setCurrentIndex(conf_map.get(self.settings.get("analysis/confidence_level"), 1))
        
        self.decimal_spin.setValue(self.settings.get("analysis/decimal_places"))
        
        missing_map = {"skip": 0, "replace_zero": 1, "flag": 2}
        self.missing_data_combo.setCurrentIndex(missing_map.get(self.settings.get("analysis/missing_data"), 0))
        
        # Visualization
        dpi_map = {150: 0, 200: 1, 300: 2, 600: 3}
        self.dpi_combo.setCurrentIndex(dpi_map.get(self.settings.get("visualization/default_dpi"), 2))
        
        self.plot_style_combo.setCurrentText(self.settings.get("visualization/plot_style"))
        self.colorblind_check.setChecked(self.settings.get("visualization/colorblind_friendly"))
        self.gridlines_check.setChecked(self.settings.get("visualization/show_gridlines"))
        
        format_map = {"png": 0, "svg": 1, "pdf": 2}
        self.export_format_combo.setCurrentIndex(format_map.get(self.settings.get("visualization/export_format").lower(), 0))
        
        # Performance
        self.thread_spin.setValue(self.settings.get("performance/thread_count"))
        self.memory_spin.setValue(self.settings.get("performance/memory_limit_mb"))
        self.cache_spin.setValue(self.settings.get("performance/cache_size_mb"))
        self.logging_combo.setCurrentText(self.settings.get("performance/logging_level"))
        
        # Advanced
        self.developer_check.setChecked(self.settings.get("advanced/developer_mode"))
        self.updates_check.setChecked(self.settings.get("advanced/check_updates"))
        self.analytics_check.setChecked(self.settings.get("advanced/send_analytics"))
    
    def save_settings(self):
        """Save all settings from UI controls."""
        # Appearance
        theme_map = {0: "light", 1: "dark", 2: "auto"}
        self.settings.set("appearance/theme", theme_map.get(self.theme_combo.currentIndex(), "light"))
        
        scheme_map = {0: "geological", 1: "professional", 2: "high_contrast"}
        self.settings.set("appearance/color_scheme", scheme_map.get(self.color_scheme_combo.currentIndex(), "geological"))
        
        font_map = {0: "small", 1: "medium", 2: "large", 3: "xlarge"}
        self.settings.set("appearance/font_size", font_map.get(self.font_size_combo.currentIndex(), "medium"))
        
        self.settings.set("appearance/compact_mode", self.compact_mode_check.isChecked())
        
        # Data & Files
        self.settings.set("data/input_dir", self.input_dir_edit.text())
        self.settings.set("data/output_dir", self.output_dir_edit.text())
        self.settings.set("data/autosave_enabled", self.autosave_check.isChecked())
        self.settings.set("data/autosave_interval", self.autosave_interval_spin.value())
        self.settings.set("data/recent_files_limit", self.recent_files_spin.value())
        
        encoding_map = {0: "utf-8", 1: "ascii", 2: "latin-1", 3: "windows-1252"}
        self.settings.set("data/file_encoding", encoding_map.get(self.encoding_combo.currentIndex(), "utf-8"))
        
        # Analysis
        self.settings.set("analysis/auto_run", self.auto_run_check.isChecked())
        self.settings.set("analysis/crm_database", self.crm_db_edit.text())
        
        conf_map = {0: 0.90, 1: 0.95, 2: 0.99}
        self.settings.set("analysis/confidence_level", conf_map.get(self.confidence_combo.currentIndex(), 0.95))
        
        self.settings.set("analysis/decimal_places", self.decimal_spin.value())
        
        missing_map = {0: "skip", 1: "replace_zero", 2: "flag"}
        self.settings.set("analysis/missing_data", missing_map.get(self.missing_data_combo.currentIndex(), "skip"))
        
        # Visualization
        dpi_map = {0: 150, 1: 200, 2: 300, 3: 600}
        self.settings.set("visualization/default_dpi", dpi_map.get(self.dpi_combo.currentIndex(), 300))
        
        self.settings.set("visualization/plot_style", self.plot_style_combo.currentText())
        self.settings.set("visualization/colorblind_friendly", self.colorblind_check.isChecked())
        self.settings.set("visualization/show_gridlines", self.gridlines_check.isChecked())
        
        format_map = {0: "png", 1: "svg", 2: "pdf"}
        self.settings.set("visualization/export_format", format_map.get(self.export_format_combo.currentIndex(), "png"))
        
        # Performance
        self.settings.set("performance/thread_count", self.thread_spin.value())
        self.settings.set("performance/memory_limit_mb", self.memory_spin.value())
        self.settings.set("performance/cache_size_mb", self.cache_spin.value())
        self.settings.set("performance/logging_level", self.logging_combo.currentText())
        
        # Advanced
        self.settings.set("advanced/developer_mode", self.developer_check.isChecked())
        self.settings.set("advanced/check_updates", self.updates_check.isChecked())
        self.settings.set("advanced/send_analytics", self.analytics_check.isChecked())
        
        self.settings_changed.emit()
    
    def apply_settings(self):
        """Apply settings without closing dialog."""
        self.save_settings()
        
        # Emit theme changed signal if theme was changed
        theme = self.settings.get("appearance/theme")
        self.theme_changed.emit(theme)
    
    def accept(self):
        """Handle OK button."""
        self.save_settings()
        theme = self.settings.get("appearance/theme")
        self.theme_changed.emit(theme)
        super().accept()
    
    def restore_defaults(self):
        """Restore all settings to defaults."""
        reply = QMessageBox.question(
            self,
            "Restore Defaults",
            "Are you sure you want to restore all settings to their default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.settings.reset_to_defaults()
            self.load_current_settings()
            QMessageBox.information(self, "Success", "Settings restored to defaults.")
    
    def browse_directory(self, line_edit: QLineEdit):
        """Browse for directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", line_edit.text())
        if directory:
            line_edit.setText(directory)
    
    def browse_file(self, line_edit: QLineEdit, filter_str: str = "All Files (*)"):
        """Browse for file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", line_edit.text(), filter_str)
        if file_path:
            line_edit.setText(file_path)
    
    def on_theme_preview(self, theme_text: str):
        """Handle theme preview (for future implementation)."""
        # Could add live preview here
        pass
