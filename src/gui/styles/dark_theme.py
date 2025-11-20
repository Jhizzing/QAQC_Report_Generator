"""
Dark Theme for QAQC Analysis Application

Provides a professional dark mode theme with muted geological colors.
"""

from typing import Dict
from .geological_theme import GeologicalTheme


class DarkTheme(GeologicalTheme):
    """
    Dark theme variant of the Geological theme.
    
    Uses dark backgrounds with light text and muted earth tones
    for a professional, eye-friendly appearance.
    """
    
    def __init__(self):
        """Initialize dark theme with custom colors."""
        super().__init__()
        # Override colors with dark theme palette
        self.colors = self._define_dark_colors()
    
    def _define_dark_colors(self) -> Dict[str, str]:
        """Define the dark theme color palette."""
        return {
            # Primary colors (dark geological theme)
            'primary': '#4A7C59',      # Muted forest green
            'primary_light': '#5D9A6E', # Lighter green
            'primary_dark': '#3A6047',  # Darker green
            
            # Secondary colors
            'secondary': '#A0714F',     # Muted brown
            'secondary_light': '#B88A6E', # Lighter brown
            'secondary_dark': '#8A5F3E', # Darker brown
            
            # Accent colors
            'accent': '#D4976D',        # Muted copper
            'accent_light': '#E5B084',  # Light copper
            'accent_dark': '#B8805A',   # Dark copper
            
            # Background colors (dark grays)
            'background': '#1E1E1E',   # Very dark gray (main background)
            'surface': '#252526',      # Dark gray (panels)
            'surface_alt': '#2D2D30',  # Slightly lighter gray
            
            # Text colors (light)
            'text_primary': '#E0E0E0',  # Light gray (primary text)
            'text_secondary': '#CCCCCC', # Medium gray
            'text_light': '#B0B0B0',   # Dimmed gray
            
            # Status colors (slightly muted for dark mode)
            'success': '#4EC9B0',      # Teal
            'success_light': '#6FD9C3', # Light teal
            'success_dark': '#3FA88F', # Dark teal
            
            'warning': '#D4A34A',      # Muted orange
            'warning_light': '#E5B96E', # Light orange
            'warning_dark': '#B88A3E', # Dark orange
            
            'error': '#D16969',        # Muted red
            'error_light': '#E58787',  # Light red
            'error_dark': '#B85555',   # Dark red
            
            'info': '#569CD6',         # Muted blue
            'info_light': '#74B0E3',   # Light blue
            'info_dark': '#4682B4',    # Dark blue
            
            # Border colors (subtle)
            'border': '#3E3E42',       # Subtle border
            'border_dark': '#505055',  # Darker border
            
            # Hover colors
            'hover': '#333337',       # Subtle hover
            'hover_dark': '#3E3E42',  # Darker hover
            
            # Selection colors
            'selection': '#264F78',    # Dark blue selection
            'selection_light': '#37537A', # Light selection
        }
    
    def get_main_style(self) -> str:
        """Get the dark theme stylesheet."""
        # Get base stylesheet from parent
        base_style = super().get_main_style()
        
        # Add dark theme specific overrides
        dark_overrides = f"""
        /* Dark Theme Specific Overrides */
        
        /* Scrollbar styling for dark theme */
        QScrollBar:vertical {{
            background-color: {self.colors['background']};
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.colors['border_dark']};
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors['text_light']};
        }}
        
        QScrollBar:horizontal {{
            background-color: {self.colors['background']};
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {self.colors['border_dark']};
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {self.colors['text_light']};
        }}
        
        /* Combo box dropdown items - darker */
        QComboBox QAbstractItemView {{
            background-color: {self.colors['surface_alt']};
            border: 1px solid {self.colors['border']};
        }}
        
        QComboBox QAbstractItemView::item:selected {{
            background-color: {self.colors['selection']};
            color: {self.colors['text_primary']};
        }}
        
        QComboBox QAbstractItemView::item:hover {{
            background-color: {self.colors['selection_light']};
        }}
        
        /* Table styling for dark theme */
        QTableWidget::item:alternate {{
            background-color: {self.colors['surface']};
        }}
        
        QTableWidget::item:selected {{
            background-color: {self.colors['selection']};
            color: {self.colors['text_primary']};
        }}
        
        QTableWidget::item:selected:hover {{
            background-color: {self.colors['selection_light']};
        }}
        
        /* Input fields - darker backgrounds */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            background-color: {self.colors['surface_alt']};
        }}
        
        /* Sidebar for dark theme */
        QWidget#sidebar {{
            background-color: {self.colors['surface']};
            border-right: 1px solid {self.colors['border']};
        }}
        
        QFrame#sidebarHeader {{
            background-color: {self.colors['background']};
            border-bottom: 1px solid {self.colors['primary']};
        }}
        """
        
        return base_style + dark_overrides
