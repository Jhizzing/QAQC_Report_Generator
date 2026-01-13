"""
QAQC Analysis Automation Application

A comprehensive system for automated Quality Assurance/Quality Control analysis
of drilling assay data, including standards, blanks, and duplicates evaluation.
"""

__version__ = "1.0.0"
__author__ = "LogiQore"
__email__ = "info@logiqore.com"

# Import main modules
from .data import DataProcessor, DataImporter
from .analysis import QAQCAnalyzer, StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer
from .visualization import PlotGenerator, ReportVisualizer
from .reporting import ReportGenerator, ExcelReporter, PDFReporter

__all__ = [
    "DataProcessor",
    "DataImporter",
    "QAQCAnalyzer",
    "StandardsAnalyzer",
    "BlanksAnalyzer",
    "DuplicatesAnalyzer",
    "PlotGenerator",
    "ReportVisualizer",
    "ReportGenerator",
    "ExcelReporter",
    "PDFReporter"
]
