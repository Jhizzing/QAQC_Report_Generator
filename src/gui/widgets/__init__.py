"""
GUI Widgets Module

This module contains custom widgets for the QAQC Analysis Application GUI,
designed specifically for geologists working with assay data.
"""

from .data_panel import DataPanel
from .analysis_panel import AnalysisPanel
from .visualization_panel import VisualizationPanel

__all__ = ['DataPanel', 'AnalysisPanel', 'VisualizationPanel']
