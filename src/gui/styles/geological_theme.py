"""
LogiQore Theme for QAQC Analysis Application

Provides a modern dark slate + amber gold theme matching the React web UI.
Professional appearance for geologists and mining engineers.
"""

from typing import Dict, Any


class GeologicalTheme:
    """
    LogiQore theme for the QAQC Analysis Application.

    Dark slate backgrounds with amber gold accents — matches the React web UI
    for visual parity across desktop and web interfaces.
    """

    def __init__(self):
        """Initialize the LogiQore theme."""
        self.colors = self._define_colors()
        self.fonts = self._define_fonts()
        self.sizes = self._define_sizes()

    def _define_colors(self) -> Dict[str, str]:
        """Define the LogiQore color palette (dark slate + amber gold)."""
        return {
            # Primary colors (amber gold — matches React #F59E0B)
            'primary': '#F59E0B',        # Amber-500 (vibrant gold)
            'primary_light': '#FBBF24',  # Amber-400
            'primary_dark': '#D97706',   # Amber-600

            # Secondary colors (slate)
            'secondary': '#334155',      # Slate-700
            'secondary_light': '#475569', # Slate-600
            'secondary_dark': '#1E293B', # Slate-800

            # Accent colors (sky blue)
            'accent': '#0EA5E9',         # Sky-500
            'accent_light': '#38BDF8',   # Sky-400
            'accent_dark': '#0284C7',    # Sky-600

            # Background colors (deep slate)
            'background': '#0F172A',     # Slate-900 (main background)
            'surface': '#1E293B',        # Slate-800 (panels/cards)
            'surface_alt': '#334155',    # Slate-700 (alternate)

            # Text colors (light on dark)
            'text_primary': '#F1F5F9',   # Slate-100 (high contrast)
            'text_secondary': '#CBD5E1', # Slate-300
            'text_light': '#94A3B8',     # Slate-400 (muted)

            # Status colors (matching React UI)
            'success': '#10B981',        # Emerald-500
            'success_light': '#34D399',  # Emerald-400
            'success_dark': '#059669',   # Emerald-600

            'warning': '#F59E0B',        # Amber-500
            'warning_light': '#FBBF24',  # Amber-400
            'warning_dark': '#D97706',   # Amber-600

            'error': '#EF4444',          # Red-500
            'error_light': '#F87171',    # Red-400
            'error_dark': '#DC2626',     # Red-600

            'info': '#3B82F6',           # Blue-500
            'info_light': '#60A5FA',     # Blue-400
            'info_dark': '#2563EB',      # Blue-600

            # Border colors
            'border': '#334155',         # Slate-700
            'border_dark': '#475569',    # Slate-600

            # Hover colors
            'hover': '#334155',          # Slate-700
            'hover_dark': '#475569',     # Slate-600

            # Selection colors
            'selection': '#F59E0B',      # Primary amber
            'selection_light': '#422006', # Amber tint on dark
        }

    def _define_fonts(self) -> Dict[str, str]:
        """Define the font family."""
        return {
            'primary': 'Inter, Segoe UI, Arial, sans-serif',
            'monospace': 'JetBrains Mono, Consolas, Monaco, monospace',
            'heading': 'Inter, Segoe UI, Arial, sans-serif',
        }

    def _define_sizes(self) -> Dict[str, str]:
        """Define size constants."""
        return {
            'border_radius': '6px',
            'border_radius_lg': '8px',
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
        # Convenience aliases
        c = self.colors
        f = self.fonts
        s = self.sizes
        # Button text on amber background
        btn_text = '#0F172A'  # Dark text for contrast on gold

        return f"""
        /* ═══════════════════════════════════════════════════════════
           LogiQore Theme — Dark Slate + Amber Gold
           Matches the React web UI for visual parity
           ═══════════════════════════════════════════════════════════ */

        /* Main Application */
        QMainWindow {{
            background-color: {c['background']};
            color: {c['text_primary']};
            font-family: {f['primary']};
        }}

        QMainWindow::title {{
            color: {c['text_primary']};
            font-weight: bold;
        }}

        /* ── Menu Bar ── */
        QMenuBar {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border-bottom: {s['border_width']} solid {c['border']};
            padding: {s['padding_small']};
            font-weight: bold;
        }}

        QMenuBar::item {{
            background-color: transparent;
            color: {c['text_secondary']};
            padding: {s['padding_small']} {s['padding_medium']};
            border-radius: {s['border_radius']};
            font-weight: bold;
        }}

        QMenuBar::item:selected {{
            background-color: {c['primary']};
            color: {btn_text};
        }}

        QMenuBar::item:pressed {{
            background-color: {c['primary_dark']};
            color: {btn_text};
        }}

        /* ── Menus ── */
        QMenu {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            padding: {s['padding_small']};
        }}

        QMenu::item {{
            background-color: transparent;
            color: {c['text_primary']};
            padding: 6px {s['padding_medium']};
            border-radius: {s['border_radius']};
        }}

        QMenu::item:selected {{
            background-color: {c['primary']};
            color: {btn_text};
        }}

        QMenu::separator {{
            height: {s['border_width']};
            background-color: {c['border']};
            margin: {s['margin_small']} 0;
        }}

        /* ── Toolbar ── */
        QToolBar {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border-bottom: {s['border_width']} solid {c['border']};
            padding: {s['padding_small']};
            spacing: {s['margin_small']};
        }}

        QToolBar QToolButton {{
            color: {c['text_primary']};
            font-weight: bold;
            background-color: transparent;
            border: none;
            border-radius: {s['border_radius']};
            padding: 4px 8px;
        }}

        QToolBar QToolButton:hover {{
            background-color: {c['hover']};
        }}

        QToolBar::separator {{
            background-color: {c['border']};
            width: {s['border_width']};
            margin: {s['margin_small']} {s['margin_medium']};
        }}

        /* ── Status Bar ── */
        QStatusBar {{
            background-color: {c['surface']};
            color: {c['text_secondary']};
            border-top: {s['border_width']} solid {c['border']};
            padding: {s['padding_small']};
        }}

        QStatusBar QLabel {{
            color: {c['text_secondary']};
            font-weight: bold;
        }}

        /* ══════════════ Buttons ══════════════ */
        QPushButton {{
            background-color: {c['primary']};
            color: {btn_text};
            border: {s['border_width']} solid {c['primary']};
            border-radius: {s['border_radius']};
            padding: 6px {s['padding_large']};
            font-weight: bold;
            font-size: 11px;
        }}

        QPushButton QLabel {{
            color: {btn_text};
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: {c['primary_light']};
            border-color: {c['primary_light']};
            color: {btn_text};
        }}

        QPushButton:pressed {{
            background-color: {c['primary_dark']};
            border-color: {c['primary_dark']};
            color: {btn_text};
        }}

        QPushButton:disabled {{
            background-color: {c['secondary']};
            color: {c['text_light']};
            border-color: {c['secondary']};
        }}

        /* Secondary Buttons */
        QPushButton[class="secondary"] {{
            background-color: {c['secondary']};
            border-color: {c['secondary_light']};
            color: {c['text_primary']};
        }}

        QPushButton[class="secondary"]:hover {{
            background-color: {c['secondary_light']};
            border-color: {c['secondary_light']};
            color: {c['text_primary']};
        }}

        /* Success Buttons */
        QPushButton[class="success"] {{
            background-color: {c['success']};
            border-color: {c['success']};
            color: #FFFFFF;
        }}

        QPushButton[class="success"]:hover {{
            background-color: {c['success_light']};
            border-color: {c['success_light']};
            color: #FFFFFF;
        }}

        /* Warning Buttons */
        QPushButton[class="warning"] {{
            background-color: {c['warning']};
            border-color: {c['warning']};
            color: {btn_text};
        }}

        QPushButton[class="warning"]:hover {{
            background-color: {c['warning_light']};
            border-color: {c['warning_light']};
            color: {btn_text};
        }}

        /* Error Buttons */
        QPushButton[class="error"] {{
            background-color: {c['error']};
            border-color: {c['error']};
            color: #FFFFFF;
        }}

        QPushButton[class="error"]:hover {{
            background-color: {c['error_light']};
            border-color: {c['error_light']};
            color: #FFFFFF;
        }}

        /* ══════════════ Inputs ══════════════ */
        QLineEdit {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            padding: 6px 8px;
            selection-background-color: {c['primary']};
            selection-color: {btn_text};
        }}

        QLineEdit:focus {{
            border-color: {c['primary']};
        }}

        QLineEdit:disabled {{
            background-color: {c['surface_alt']};
            color: {c['text_light']};
        }}

        /* ── Spin Boxes ── */
        QSpinBox, QDoubleSpinBox {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            padding: 6px 8px;
            min-height: 28px;
            selection-background-color: {c['primary']};
            selection-color: {btn_text};
        }}

        QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {c['primary']};
        }}

        QSpinBox:disabled, QDoubleSpinBox:disabled {{
            background-color: {c['surface_alt']};
            color: {c['text_light']};
        }}

        QSpinBox::up-button, QDoubleSpinBox::up-button {{
            background-color: {c['surface']};
            border: none;
            border-left: 1px solid {c['border']};
            border-top-right-radius: {s['border_radius']};
            width: 20px;
        }}

        QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
            background-color: {c['hover']};
        }}

        QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{
            background-color: {c['primary']};
        }}

        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            background-color: {c['surface']};
            border: none;
            border-left: 1px solid {c['border']};
            border-bottom-right-radius: {s['border_radius']};
            width: 20px;
        }}

        QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
            background-color: {c['hover']};
        }}

        QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
            background-color: {c['primary']};
        }}

        QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
            width: 8px;
            height: 8px;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-bottom: 4px solid {c['text_light']};
        }}

        QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
            width: 8px;
            height: 8px;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid {c['text_light']};
        }}

        /* ── Text Edits ── */
        QTextEdit {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            padding: {s['padding_small']};
            selection-background-color: {c['primary']};
            selection-color: {btn_text};
        }}

        QTextEdit:focus {{
            border-color: {c['primary']};
        }}

        QPlainTextEdit {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            padding: {s['padding_small']};
            selection-background-color: {c['primary']};
            selection-color: {btn_text};
        }}

        /* ── Combo Boxes ── */
        QComboBox {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            padding: 6px 10px;
            min-height: 30px;
            text-align: center;
        }}

        QComboBox:focus {{
            border-color: {c['primary']};
            background-color: {c['surface']};
        }}

        QComboBox:hover {{
            border-color: {c['border_dark']};
            background-color: {c['surface_alt']};
        }}

        QComboBox::drop-down {{
            width: 0px;
            border: none;
            background-color: transparent;
        }}

        QComboBox::down-arrow {{
            image: none;
            border: none;
            width: 0;
            height: 0;
        }}

        /* Combo Box Dropdown Items */
        QComboBox QAbstractItemView {{
            background-color: {c['surface']};
            border: 1px solid {c['border']};
            border-radius: {s['border_radius']};
            padding: 4px;
            selection-background-color: {c['secondary']};
            selection-color: {c['text_primary']};
            outline: none;
        }}

        QComboBox QAbstractItemView::item {{
            min-height: 30px;
            padding: 8px 12px;
            color: {c['text_primary']};
            background-color: transparent;
            border-radius: 4px;
        }}

        QComboBox QAbstractItemView::item:selected {{
            background-color: {c['selection_light']};
            color: {c['primary']};
        }}

        QComboBox QAbstractItemView::item:hover {{
            background-color: {c['hover']};
            color: {c['text_primary']};
        }}

        /* ══════════════ Controls ══════════════ */

        /* Check Boxes */
        QCheckBox {{
            color: {c['text_primary']};
            spacing: {s['padding_small']};
        }}

        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {c['border_dark']};
            border-radius: {s['border_radius']};
            background-color: {c['surface']};
        }}

        QCheckBox::indicator:checked {{
            background-color: {c['primary']};
            border-color: {c['primary']};
        }}

        QCheckBox::indicator:checked:hover {{
            background-color: {c['primary_light']};
            border-color: {c['primary_light']};
        }}

        QCheckBox::indicator:hover {{
            border-color: {c['primary']};
        }}

        /* Radio Buttons */
        QRadioButton {{
            color: {c['text_primary']};
            spacing: {s['padding_small']};
        }}

        QRadioButton::indicator {{
            width: 16px;
            height: 16px;
            border: {s['border_width']} solid {c['border']};
            border-radius: 8px;
            background-color: {c['surface']};
        }}

        QRadioButton::indicator:checked {{
            background-color: {c['primary']};
            border-color: {c['primary']};
        }}

        QRadioButton::indicator:hover {{
            border-color: {c['primary']};
        }}

        /* Progress Bars */
        QProgressBar {{
            background-color: {c['surface_alt']};
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            text-align: center;
            color: {c['text_primary']};
        }}

        QProgressBar::chunk {{
            background-color: {c['primary']};
            border-radius: {s['border_radius']};
        }}

        /* ══════════════ Dialogs ══════════════ */
        QDialog {{
            background-color: {c['surface']};
            color: {c['text_primary']};
        }}

        QMessageBox {{
            background-color: {c['surface']};
            color: {c['text_primary']};
        }}

        QMessageBox QPushButton {{
            background-color: {c['primary']};
            color: {btn_text};
            border: 2px solid {c['primary']};
            border-radius: {s['border_radius']};
            padding: 8px 16px;
            font-weight: bold;
            font-size: 12px;
            min-width: 100px;
            min-height: 30px;
        }}

        QMessageBox QPushButton:hover {{
            background-color: {c['primary_light']};
            border-color: {c['primary_light']};
            color: {btn_text};
        }}

        QMessageBox QPushButton:pressed {{
            background-color: {c['primary_dark']};
            border-color: {c['primary_dark']};
            color: {btn_text};
        }}

        QFileDialog {{
            background-color: {c['surface']};
            color: {c['text_primary']};
        }}

        QFileDialog QPushButton {{
            background-color: {c['primary']};
            color: {btn_text};
            border: {s['border_width']} solid {c['primary']};
            border-radius: {s['border_radius']};
            padding: {s['padding_small']} {s['padding_medium']};
            font-weight: bold;
        }}

        QFileDialog QPushButton:hover {{
            background-color: {c['primary_light']};
            border-color: {c['primary_light']};
            color: {btn_text};
        }}

        QFileDialog QPushButton:pressed {{
            background-color: {c['primary_dark']};
            border-color: {c['primary_dark']};
            color: {btn_text};
        }}

        /* ══════════════ Labels ══════════════ */
        QLabel {{
            color: {c['text_primary']};
            font-weight: bold;
        }}

        QLabel[class="placeholder"] {{
            color: {c['text_light']};
            font-weight: normal;
            font-style: italic;
        }}

        QLabel[class="status"] {{
            color: {c['text_secondary']};
            font-weight: bold;
        }}

        QLabel[class="heading"] {{
            font-weight: bold;
            font-size: 14px;
            color: {c['text_primary']};
        }}

        QLabel[class="subheading"] {{
            font-weight: bold;
            font-size: 12px;
            color: {c['text_secondary']};
        }}

        /* ══════════════ Group Boxes ══════════════ */
        QGroupBox {{
            color: {c['text_primary']};
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            margin-top: {s['margin_medium']};
            padding-top: {s['padding_medium']};
            background-color: {c['surface']};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {s['padding_medium']};
            padding: 0 {s['padding_small']} 0 {s['padding_small']};
            color: {c['primary']};
            font-weight: bold;
            font-size: 12px;
        }}

        /* ══════════════ Tabs ══════════════ */
        QTabWidget::pane {{
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            background-color: {c['surface']};
        }}

        QTabBar::tab {{
            background-color: {c['surface_alt']};
            color: {c['text_light']};
            border: {s['border_width']} solid {c['border']};
            border-bottom: none;
            border-radius: {s['border_radius']} {s['border_radius']} 0 0;
            padding: 6px {s['padding_large']};
            margin-right: {s['border_width']};
        }}

        QTabBar::tab:selected {{
            background-color: {c['surface']};
            color: {c['primary']};
            border-bottom: 2px solid {c['primary']};
        }}

        QTabBar::tab:hover {{
            background-color: {c['hover']};
            color: {c['text_primary']};
        }}

        /* ══════════════ Tables ══════════════ */
        QTableWidget {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: {s['border_width']} solid {c['border']};
            border-radius: {s['border_radius']};
            gridline-color: {c['border']};
            alternate-background-color: {c['surface_alt']};
        }}

        QTableWidget::item {{
            padding: 6px 8px;
            border: none;
            background-color: {c['surface']};
        }}

        QTableWidget::item:alternate {{
            background-color: #253347;
        }}

        QTableWidget::item:selected {{
            background-color: {c['selection_light']};
            color: {c['primary']};
        }}

        QTableWidget::item:hover {{
            background-color: {c['hover']};
        }}

        QTableWidget::item:selected:hover {{
            background-color: #3D2A08;
            color: {c['primary_light']};
        }}

        QTableWidget::item:empty {{
            background-color: transparent;
            border: none;
        }}

        /* Table Headers */
        QHeaderView {{
            background-color: {c['surface']};
        }}

        QHeaderView::section {{
            background-color: {c['surface']};
            color: {c['text_secondary']};
            border: none;
            border-bottom: 2px solid {c['primary']};
            border-right: 1px solid {c['border']};
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
            background-color: {c['hover']};
            color: {c['primary']};
        }}

        /* ══════════════ Splitter ══════════════ */
        QSplitter::handle {{
            background-color: {c['border']};
        }}

        QSplitter::handle:horizontal {{
            width: {s['border_width']};
        }}

        QSplitter::handle:vertical {{
            height: {s['border_width']};
        }}

        QSplitter::handle:hover {{
            background-color: {c['primary']};
        }}

        /* ══════════════ Scroll Bars ══════════════ */
        QScrollBar:vertical {{
            background-color: {c['background']};
            width: 10px;
            border-radius: 5px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {c['secondary']};
            border-radius: 5px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {c['primary']};
        }}

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {c['background']};
            height: 10px;
            border-radius: 5px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {c['secondary']};
            border-radius: 5px;
            min-width: 20px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {c['primary']};
        }}

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}

        /* ══════════════ Sidebar ══════════════ */
        QWidget#sidebar {{
            background-color: #0F172A;
            border-right: 1px solid {c['border']};
        }}

        QFrame#sidebarHeader {{
            background-color: #020617;
            border-bottom: 1px solid {c['primary']};
        }}

        QLabel#sidebarTitle {{
            color: {c['primary']};
            font-size: 18px;
            font-weight: bold;
        }}

        QLabel#sidebarSubtitle {{
            color: {c['text_light']};
            font-size: 12px;
            font-style: italic;
        }}

        QFrame#navContainer {{
            background-color: transparent;
            border: none;
        }}

        QWidget#sidebar QPushButton {{
            text-align: left;
            padding-left: 20px;
            border: none;
            border-radius: 0px;
            background-color: transparent;
            color: {c['text_secondary']};
            font-size: 14px;
            border-left: 4px solid transparent;
        }}

        QWidget#sidebar QPushButton:hover {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border-left: 4px solid {c['accent']};
        }}

        QWidget#sidebar QPushButton:checked {{
            background-color: {c['surface']};
            color: {c['primary']};
            border-left: 4px solid {c['primary']};
            font-weight: bold;
        }}

        QFrame#sidebarFooter {{
            background-color: #020617;
            border-top: 1px solid {c['border']};
        }}

        QLabel#sidebarVersion {{
            color: {c['text_light']};
            font-size: 10px;
        }}
        """

    def get_widget_style(self, widget_type: str) -> str:
        """Get specific widget styling."""
        c = self.colors
        s = self.sizes
        styles = {
            'data_panel': f"""
                QWidget {{
                    background-color: {c['surface']};
                    border: {s['border_width']} solid {c['border']};
                    border-radius: {s['border_radius']};
                }}
            """,
            'analysis_panel': f"""
                QWidget {{
                    background-color: {c['surface']};
                    border: {s['border_width']} solid {c['border']};
                    border-radius: {s['border_radius']};
                }}
            """,
            'visualization_panel': f"""
                QWidget {{
                    background-color: {c['surface']};
                    border: {s['border_width']} solid {c['border']};
                    border-radius: {s['border_radius']};
                }}
            """,
        }

        return styles.get(widget_type, "")

    def get_color(self, color_name: str) -> str:
        """Get a specific color from the theme."""
        return self.colors.get(color_name, "#F1F5F9")

    def get_colors(self) -> Dict[str, str]:
        """Get all theme colors."""
        return self.colors.copy()
