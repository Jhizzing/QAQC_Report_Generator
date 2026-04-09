"""
Service layer for LogiQore Reporter.

Provides clean interfaces between entry points (API, CLI) and the core engine.
All business logic flows through these services — entry points should never
import analyzers or reporters directly.
"""

from .data_service import DataService
from .analysis_service import AnalysisService
from .crm_service import CRMService
from .report_service import ReportService
from .settings_service import SettingsService

__all__ = [
    "DataService",
    "AnalysisService",
    "CRMService",
    "ReportService",
    "SettingsService",
]
