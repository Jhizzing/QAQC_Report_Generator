"""
Geological Theme for QAQC Analysis Application

This module provides a professional geological theme with earth tones
and colors that appeal to geologists and mining engineers.
"""

from typing import Dict, Any


class GeologicalTheme:
    """
    Geological theme for the QAQC Analysis Application.

    Provides a professional color scheme and styling that appeals to
    geologists and mining engineers working with assay data.
    """

    def __init__(self):
        """Initialize the geological theme."""
        self.colors = self._define_colors()
        self.fonts = self._define_fonts()
        self.sizes = self._define_sizes()

    def _define_colors(self) -> Dict[str, str]:
        """Define the geological color palette."""
        return {
            # Primary colors (geological theme)
            'primary': '#2E5266',      # Deep blue (geological)
            'primary_light': '#4A7C59', # Forest green
            'primary_dark': '#1A3A4A',  # Darker blue

            # Secondary colors
            'secondary': '#8B4513',     # Saddle brown
            'secondary_light': '#A0522D', # Sienna
            'secondary_dark': '#654321', # Dark brown

            # Accent colors
            'accent': '#D2691E',        # Chocolate
            'accent_light': '#F4A460',  # Sandy brown
            'accent_dark': '#B8860B',   # Dark goldenrod

            # Background colors
            'background': '#F5F5F5',   # Light gray
            'surface': '#FFFFFF',      # White
            'surface_alt': '#F8F9FA',  # Light gray alternative

            # Text colors (improved contrast)
            'text_primary': '#1A1A1A',  # Very dark gray for maximum readability
            'text_secondary': '#2C3E50', # Dark blue-gray (was too light)
            'text_light': '#495057',   # Medium gray (was too light)

            # Status colors
            'success': '#27AE60',      # Green
            'success_light': '#58D68D', # Light green
            'success_dark': '#1E8449', # Dark green

            'warning': '#F39C12',      # Orange
            'warning_light': '#F7DC6F', # Light orange
            'warning_dark': '#D68910', # Dark orange

            'error': '#E74C3C',        # Red
            'error_light': '#F1948A',  # Light red
            'error_dark': '#C0392B',   # Dark red

            'info': '#3498DB',         # Blue
            'info_light': '#85C1E9',   # Light blue
            'info_dark': '#2980B9',    # Dark blue

            # Border colors
            'border': '#DEE2E6',       # Light border
            'border_dark': '#ADB5BD',  # Dark border

            # Hover colors
            'hover': '#E9ECEF',       # Light hover
            'hover_dark': '#DEE2E6',  # Dark hover

            # Selection colors (more subtle for better text visibility)
            'selection': '#3498DB',    # Blue selection
            'selection_light': '#E3F2FD', # Very light blue selection (subtle)
        }

    def _define_fonts(self) -> Dict[str, str]:
        """Define the font family."""
        return {
            'primary': 'Segoe UI, Arial, sans-serif',
            'monospace': 'Consolas, Monaco, monospace',
            'heading': 'Segoe UI, Arial, sans-serif',
        }

    def _define_sizes(self) -> Dict[str, str]:
        """Define size constants."""
        return {
            'border_radius': '4px',
            'border_width': '1px',
            'padding_small': '4px',
            'padding_medium': '8px',
            'padding_large': '12px',
            'margin_small': '4px',
            'margin_medium': '8px',
            'margin_large': '12px',
        }

    def get_main_style(self) -> str:
        """Get the main application stylesheet."""
        return f"""
        /* Main Application Styles */
        QMainWindow {{
            background-color: {self.colors['background']};
            color: {self.colors['text_primary']};
            font-family: {self.fonts['primary']};
        }}

        /* Window Title */
        QMainWindow::title {{
            color: {self.colors['text_primary']};
            font-weight: bold;
        }}

        /* Menu Bar */
        QMenuBar {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border-bottom: {self.sizes['border_width']} solid {self.colors['border']};
            padding: {self.sizes['padding_small']};
            font-weight: bold;
        }}

        QMenuBar::item {{
            background-color: transparent;
            color: {self.colors['text_primary']};
            padding: {self.sizes['padding_small']} {self.sizes['padding_medium']};
            border-radius: {self.sizes['border_radius']};
            font-weight: bold;
        }}

        QMenuBar::item:selected {{
            background-color: {self.colors['primary']};
            color: {self.colors['surface']};
        }}

        QMenuBar::item:pressed {{
            background-color: {self.colors['primary_dark']};
            color: {self.colors['surface']};
        }}

        /* Menu */
        QMenu {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            padding: {self.sizes['padding_small']};
        }}

        QMenu::item {{
            background-color: transparent;
            color: {self.colors['text_primary']};
            padding: {self.sizes['padding_small']} {self.sizes['padding_medium']};
            border-radius: {self.sizes['border_radius']};
        }}

        QMenu::item:selected {{
            background-color: {self.colors['primary']};
            color: {self.colors['surface']};
        }}

        QMenu::separator {{
            height: {self.sizes['border_width']};
            background-color: {self.colors['border']};
            margin: {self.sizes['margin_small']} 0;
        }}

        /* Tool Bar */
        QToolBar {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border-bottom: {self.sizes['border_width']} solid {self.colors['border']};
            padding: {self.sizes['padding_small']};
            spacing: {self.sizes['margin_small']};
        }}

        QToolBar QToolButton {{
            color: {self.colors['text_primary']};
            font-weight: bold;
        }}

        QToolBar::separator {{
            background-color: {self.colors['border']};
            width: {self.sizes['border_width']};
            margin: {self.sizes['margin_small']} {self.sizes['margin_medium']};
        }}

        /* Status Bar */
        QStatusBar {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border-top: {self.sizes['border_width']} solid {self.colors['border']};
            padding: {self.sizes['padding_small']};
        }}

        QStatusBar QLabel {{
            color: {self.colors['text_primary']};
            font-weight: bold;
        }}

        /* Buttons */
        QPushButton {{
            background-color: {self.colors['primary']};
            color: {self.colors['surface']};
            border: {self.sizes['border_width']} solid {self.colors['primary']};
            border-radius: {self.sizes['border_radius']};
            padding: {self.sizes['padding_small']} {self.sizes['padding_medium']};
            font-weight: bold;
            font-size: 11px;
        }}

        QPushButton QLabel {{
            color: {self.colors['surface']};
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: {self.colors['primary_light']};
            border-color: {self.colors['primary_light']};
            color: {self.colors['surface']};
        }}

        QPushButton:pressed {{
            background-color: {self.colors['primary_dark']};
            border-color: {self.colors['primary_dark']};
            color: {self.colors['surface']};
        }}

        QPushButton:disabled {{
            background-color: {self.colors['border']};
            color: {self.colors['text_primary']};
            border-color: {self.colors['border']};
        }}

        /* Secondary Buttons */
        QPushButton[class="secondary"] {{
            background-color: {self.colors['secondary']};
            border-color: {self.colors['secondary']};
            color: {self.colors['surface']};
        }}

        QPushButton[class="secondary"]:hover {{
            background-color: {self.colors['secondary_light']};
            border-color: {self.colors['secondary_light']};
            color: {self.colors['surface']};
        }}

        /* Success Buttons */
        QPushButton[class="success"] {{
            background-color: {self.colors['success']};
            border-color: {self.colors['success']};
            color: {self.colors['surface']};
        }}

        QPushButton[class="success"]:hover {{
            background-color: {self.colors['success_light']};
            border-color: {self.colors['success_light']};
            color: {self.colors['surface']};
        }}

        /* Warning Buttons */
        QPushButton[class="warning"] {{
            background-color: {self.colors['warning']};
            border-color: {self.colors['warning']};
            color: {self.colors['surface']};
        }}

        QPushButton[class="warning"]:hover {{
            background-color: {self.colors['warning_light']};
            border-color: {self.colors['warning_light']};
            color: {self.colors['surface']};
        }}

        /* Error Buttons */
        QPushButton[class="error"] {{
            background-color: {self.colors['error']};
            border-color: {self.colors['error']};
            color: {self.colors['surface']};
        }}

        QPushButton[class="error"]:hover {{
            background-color: {self.colors['error_light']};
            border-color: {self.colors['error_light']};
            color: {self.colors['surface']};
        }}

        /* Line Edits */
        QLineEdit {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            padding: {self.sizes['padding_small']};
        }}

        QLineEdit:focus {{
            border-color: {self.colors['primary']};
        }}

        QLineEdit:disabled {{
            background-color: {self.colors['surface_alt']};
            color: {self.colors['text_secondary']};
        }}

        /* Spin Boxes (QSpinBox, QDoubleSpinBox) */
        QSpinBox, QDoubleSpinBox {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            padding: {self.sizes['padding_small']};
            min-height: 28px;
        }}

        QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {self.colors['primary']};
        }}

        QSpinBox:disabled, QDoubleSpinBox:disabled {{
            background-color: {self.colors['surface_alt']};
            color: {self.colors['text_secondary']};
        }}

        QSpinBox::up-button, QDoubleSpinBox::up-button {{
            background-color: {self.colors['surface']};
            border: none;
            border-left: 1px solid {self.colors['border']};
            border-top-right-radius: {self.sizes['border_radius']};
            width: 20px;
        }}

        QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
            background-color: {self.colors['hover']};
        }}

        QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{
            background-color: {self.colors['border']};
        }}

        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            background-color: {self.colors['surface']};
            border: none;
            border-left: 1px solid {self.colors['border']};
            border-bottom-right-radius: {self.sizes['border_radius']};
            width: 20px;
        }}

        QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
            background-color: {self.colors['hover']};
        }}

        QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
            background-color: {self.colors['border']};
        }}

        QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
            width: 8px;
            height: 8px;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-bottom: 4px solid {self.colors['text_primary']};
        }}

        QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
            width: 8px;
            height: 8px;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid {self.colors['text_primary']};
        }}

        /* Text Edits */
        QTextEdit {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            padding: {self.sizes['padding_small']};
        }}

        QTextEdit:focus {{
            border-color: {self.colors['primary']};
        }}

        /* Combo Boxes */
        QComboBox {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            padding: {self.sizes['padding_small']};
            min-height: 28px;
        }}

        QComboBox:focus {{
            border-color: {self.colors['primary']};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {self.colors['text_primary']};
            margin-right: 5px;
        }}

        /* Combo Box Dropdown Items - increased row height and very subtle selection */
        QComboBox QAbstractItemView {{
            background-color: {self.colors['surface']};
            border: 1px solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            selection-background-color: #F0F7FA;
            selection-color: {self.colors['text_primary']};
            outline: none;
        }}

        QComboBox QAbstractItemView::item {{
            min-height: 32px;
            padding: 6px 10px;
            color: {self.colors['text_primary']};
            background-color: {self.colors['surface']};
        }}

        QComboBox QAbstractItemView::item:selected {{
            background-color: #F0F7FA;
            color: {self.colors['text_primary']};
        }}

        QComboBox QAbstractItemView::item:hover {{
            background-color: #F5F8FA;
            color: {self.colors['text_primary']};
        }}

        /* Check Boxes */
        QCheckBox {{
            color: {self.colors['text_primary']};
            spacing: {self.sizes['padding_small']};
        }}

        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {self.colors['border_dark']};
            border-radius: {self.sizes['border_radius']};
            background-color: {self.colors['surface']};
        }}

        QCheckBox::indicator:checked {{
            background-color: {self.colors['success']};
            border-color: {self.colors['success']};
        }}

        QCheckBox::indicator:checked:hover {{
            background-color: {self.colors['success_light']};
            border-color: {self.colors['success_light']};
        }}

        QCheckBox::indicator:hover {{
            border-color: {self.colors['success']};
        }}

        /* Radio Buttons */
        QRadioButton {{
            color: {self.colors['text_primary']};
            spacing: {self.sizes['padding_small']};
        }}

        QRadioButton::indicator {{
            width: 16px;
            height: 16px;
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: 8px;
            background-color: {self.colors['surface']};
        }}

        QRadioButton::indicator:checked {{
            background-color: {self.colors['primary']};
            border-color: {self.colors['primary']};
        }}

        QRadioButton::indicator:hover {{
            border-color: {self.colors['primary']};
        }}

        /* Progress Bars */
        QProgressBar {{
            background-color: {self.colors['surface_alt']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            text-align: center;
        }}

        QProgressBar::chunk {{
            background-color: {self.colors['primary']};
            border-radius: {self.sizes['border_radius']};
        }}

        /* Dialog Boxes and Message Boxes */
        QDialog {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
        }}

        QMessageBox {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
        }}

        QMessageBox QPushButton {{
            background-color: {self.colors['primary']};
            color: {self.colors['surface']};
            border: 2px solid {self.colors['primary']};
            border-radius: {self.sizes['border_radius']};
            padding: 8px 16px;
            font-weight: bold;
            font-size: 12px;
            min-width: 100px;
            min-height: 30px;
        }}

        QMessageBox QPushButton:hover {{
            background-color: {self.colors['primary_light']};
            border-color: {self.colors['primary_light']};
            color: {self.colors['surface']};
        }}

        QMessageBox QPushButton:pressed {{
            background-color: {self.colors['primary_dark']};
            border-color: {self.colors['primary_dark']};
            color: {self.colors['surface']};
        }}

        /* File Dialog and Other Dialogs */
        QFileDialog {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
        }}

        QFileDialog QPushButton {{
            background-color: {self.colors['primary']};
            color: {self.colors['surface']};
            border: {self.sizes['border_width']} solid {self.colors['primary']};
            border-radius: {self.sizes['border_radius']};
            padding: {self.sizes['padding_small']} {self.sizes['padding_medium']};
            font-weight: bold;
        }}

        QFileDialog QPushButton:hover {{
            background-color: {self.colors['primary_light']};
            border-color: {self.colors['primary_light']};
            color: {self.colors['surface']};
        }}

        QFileDialog QPushButton:pressed {{
            background-color: {self.colors['primary_dark']};
            border-color: {self.colors['primary_dark']};
            color: {self.colors['surface']};
        }}

        /* Labels */
        QLabel {{
            color: {self.colors['text_primary']};
            font-weight: bold;
        }}

        /* Placeholder text styling */
        QLabel[class="placeholder"] {{
            color: {self.colors['text_secondary']};
            font-weight: normal;
            font-style: italic;
        }}

        /* Status text styling */
        QLabel[class="status"] {{
            color: {self.colors['text_secondary']};
            font-weight: bold;
        }}

        /* Text areas and status displays */
        QTextEdit {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            padding: {self.sizes['padding_small']};
        }}

        QPlainTextEdit {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            padding: {self.sizes['padding_small']};
        }}

        QLabel[class="heading"] {{
            font-weight: bold;
            font-size: 14px;
            color: {self.colors['text_primary']};
        }}

        QLabel[class="subheading"] {{
            font-weight: bold;
            font-size: 12px;
            color: {self.colors['text_primary']};
        }}

        /* Group Boxes */
        QGroupBox {{
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            margin-top: {self.sizes['margin_medium']};
            padding-top: {self.sizes['padding_medium']};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {self.sizes['padding_medium']};
            padding: 0 {self.sizes['padding_small']} 0 {self.sizes['padding_small']};
            color: {self.colors['text_primary']};
            font-weight: bold;
            font-size: 12px;
        }}

        /* Tabs */
        QTabWidget::pane {{
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            background-color: {self.colors['surface']};
        }}

        QTabBar::tab {{
            background-color: {self.colors['surface_alt']};
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-bottom: none;
            border-radius: {self.sizes['border_radius']} {self.sizes['border_radius']} 0 0;
            padding: {self.sizes['padding_small']} {self.sizes['padding_medium']};
            margin-right: {self.sizes['border_width']};
        }}

        QTabBar::tab:selected {{
            background-color: {self.colors['surface']};
            border-bottom: {self.sizes['border_width']} solid {self.colors['surface']};
        }}

        QTabBar::tab:hover {{
            background-color: {self.colors['hover']};
        }}

        /* Tables */
        QTableWidget {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border: {self.sizes['border_width']} solid {self.colors['border']};
            border-radius: {self.sizes['border_radius']};
            gridline-color: {self.colors['border']};
            alternate-background-color: {self.colors['surface_alt']};
        }}

        QTableWidget::item {{
            padding: 6px 8px;
            border: none;
            background-color: {self.colors['surface']};
        }}

        QTableWidget::item:alternate {{
            background-color: {self.colors['surface_alt']};
        }}

        QTableWidget::item:selected {{
            background-color: {self.colors['selection_light']};
            color: {self.colors['text_primary']};
        }}

        QTableWidget::item:hover {{
            background-color: {self.colors['hover']};
        }}

        QTableWidget::item:selected:hover {{
            background-color: #D1E7F0;
            color: {self.colors['text_primary']};
        }}

        /* Empty cells - make them invisible/transparent */
        QTableWidget::item:empty {{
            background-color: transparent;
            border: none;
        }}

        /* Header styling - cleaner and less clunky */
        QHeaderView {{
            background-color: {self.colors['surface']};
        }}

        QHeaderView::section {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            border: none;
            border-bottom: 2px solid {self.colors['border_dark']};
            border-right: 1px solid {self.colors['border']};
            padding: 8px 10px;
            font-weight: 600;
            font-size: 11px;
        }}

        QHeaderView::section:first {{
            border-left: none;
        }}

        QHeaderView::section:last {{
            border-right: none;
        }}

        QHeaderView::section:hover {{
            background-color: {self.colors['hover']};
        }}

        /* Splitter */
        QSplitter::handle {{
            background-color: {self.colors['border']};
        }}

        QSplitter::handle:horizontal {{
            width: {self.sizes['border_width']};
        }}

        QSplitter::handle:vertical {{
            height: {self.sizes['border_width']};
        }}

        QSplitter::handle:hover {{
            background-color: {self.colors['primary']};
        }}

        /* Scroll Bars */
        QScrollBar:vertical {{
            background-color: {self.colors['surface_alt']};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {self.colors['border_dark']};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors['primary']};
        }}

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {self.colors['surface_alt']};
            height: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {self.colors['border_dark']};
            border-radius: 6px;
            min-width: 20px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {self.colors['primary']};
        }}

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        """

    def get_widget_style(self, widget_type: str) -> str:
        """Get specific widget styling."""
        styles = {
            'data_panel': f"""
                QWidget {{
                    background-color: {self.colors['surface']};
                    border: {self.sizes['border_width']} solid {self.colors['border']};
                    border-radius: {self.sizes['border_radius']};
                }}
            """,
            'analysis_panel': f"""
                QWidget {{
                    background-color: {self.colors['surface']};
                    border: {self.sizes['border_width']} solid {self.colors['border']};
                    border-radius: {self.sizes['border_radius']};
                }}
            """,
            'visualization_panel': f"""
                QWidget {{
                    background-color: {self.colors['surface']};
                    border: {self.sizes['border_width']} solid {self.colors['border']};
                    border-radius: {self.sizes['border_radius']};
                }}
            """,
        }

        return styles.get(widget_type, "")

    def get_color(self, color_name: str) -> str:
        """Get a specific color from the theme."""
        return self.colors.get(color_name, "#000000")

    def get_colors(self) -> Dict[str, str]:
        """Get all theme colors."""
        return self.colors.copy()
