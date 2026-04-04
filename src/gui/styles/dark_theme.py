"""
Dark Theme for QAQC Analysis Application

Deeper variant of the LogiQore theme — uses the same amber gold accent system
but with even darker backgrounds for OLED/true-dark displays.
"""

from typing import Dict
from .geological_theme import GeologicalTheme


class DarkTheme(GeologicalTheme):
    """
    Deep dark variant of the LogiQore theme.

    Uses near-black backgrounds with the same amber gold accent system
    for an even more immersive dark mode experience.
    """

    def __init__(self):
        """Initialize deep dark theme with custom colors."""
        super().__init__()
        # Override colors with deeper dark palette
        self.colors = self._define_dark_colors()

    def _define_dark_colors(self) -> Dict[str, str]:
        """Define the deep dark theme color palette."""
        return {
            # Primary colors (same amber gold system)
            'primary': '#F59E0B',        # Amber-500
            'primary_light': '#FBBF24',  # Amber-400
            'primary_dark': '#D97706',   # Amber-600

            # Secondary colors (deeper slate)
            'secondary': '#1E293B',      # Slate-800
            'secondary_light': '#334155', # Slate-700
            'secondary_dark': '#0F172A', # Slate-900

            # Accent colors (same sky blue)
            'accent': '#0EA5E9',         # Sky-500
            'accent_light': '#38BDF8',   # Sky-400
            'accent_dark': '#0284C7',    # Sky-600

            # Background colors (near-black)
            'background': '#020617',     # Slate-950 (deepest)
            'surface': '#0F172A',        # Slate-900 (panels)
            'surface_alt': '#1E293B',    # Slate-800 (alternate)

            # Text colors (same light text)
            'text_primary': '#F1F5F9',   # Slate-100
            'text_secondary': '#CBD5E1', # Slate-300
            'text_light': '#94A3B8',     # Slate-400

            # Status colors (same)
            'success': '#10B981',
            'success_light': '#34D399',
            'success_dark': '#059669',

            'warning': '#F59E0B',
            'warning_light': '#FBBF24',
            'warning_dark': '#D97706',

            'error': '#EF4444',
            'error_light': '#F87171',
            'error_dark': '#DC2626',

            'info': '#3B82F6',
            'info_light': '#60A5FA',
            'info_dark': '#2563EB',

            # Border colors (subtler)
            'border': '#1E293B',
            'border_dark': '#334155',

            # Hover colors
            'hover': '#1E293B',
            'hover_dark': '#334155',

            # Selection colors
            'selection': '#F59E0B',
            'selection_light': '#2A1F0A',
        }

    def get_main_style(self) -> str:
        """Get the deep dark theme stylesheet."""
        # Get base stylesheet from parent (uses the overridden colors)
        base_style = super().get_main_style()

        # Add deep dark specific overrides
        dark_overrides = f"""
        /* Deep Dark Theme Overrides */

        QWidget#sidebar {{
            background-color: #020617;
            border-right: 1px solid {self.colors['border']};
        }}

        QFrame#sidebarHeader {{
            background-color: #020617;
            border-bottom: 1px solid {self.colors['primary']};
        }}

        QFrame#sidebarFooter {{
            background-color: #020617;
            border-top: 1px solid {self.colors['border']};
        }}
        """

        return base_style + dark_overrides
