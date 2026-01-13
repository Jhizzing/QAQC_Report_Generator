"""
Centralized error handling for QAQC application.
Provides custom exception classes and error handling utilities.
"""
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class QAQCError(Exception):
    """Base exception for all QAQC-related errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        logger.error(f"QAQCError: {message}", extra=self.details)


class DataImportError(QAQCError):
    """Raised when data import fails."""
    
    def __init__(self, message: str, file_path: Optional[Path] = None, 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.file_path = file_path
        self.details = details or {}
        if file_path:
            self.details['file_path'] = str(file_path)


class AnalysisError(QAQCError):
    """Raised when analysis execution fails."""
    
    def __init__(self, message: str, analysis_type: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.analysis_type = analysis_type
        self.details = details or {}
        if analysis_type:
            self.details['analysis_type'] = analysis_type


class ReportGenerationError(QAQCError):
    """Raised when report generation fails."""
    
    def __init__(self, message: str, report_type: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.report_type = report_type
        self.details = details or {}
        if report_type:
            self.details['report_type'] = report_type


class ConfigurationError(QAQCError):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str, config_key: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.config_key = config_key
        self.details = details or {}
        if config_key:
            self.details['config_key'] = config_key


class ValidationError(QAQCError):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None,
                 value: Optional[Any] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.field = field
        self.value = value
        self.details = details or {}
        if field:
            self.details['field'] = field
        if value is not None:
            self.details['value'] = str(value)


def get_user_friendly_error_message(error: Exception) -> str:
    """Convert exception to user-friendly error message."""
    if isinstance(error, QAQCError):
        return error.message
    elif isinstance(error, FileNotFoundError):
        return f"File not found: {error.filename if hasattr(error, 'filename') else 'unknown'}"
    elif isinstance(error, ValueError):
        return f"Invalid value: {str(error)}"
    elif isinstance(error, TypeError):
        return f"Type error: {str(error)}"
    elif isinstance(error, PermissionError):
        return "Permission denied. Please check file permissions."
    elif isinstance(error, MemoryError):
        return "Out of memory. Please try with a smaller dataset."
    else:
        return f"An unexpected error occurred: {str(error)}"


def get_error_recovery_suggestions(error: Exception) -> list[str]:
    """Get recovery suggestions for an error."""
    suggestions = []
    
    if isinstance(error, DataImportError):
        suggestions.append("Check that the file format is correct (CSV or Excel)")
        suggestions.append("Verify that required columns are present")
        suggestions.append("Ensure the file is not corrupted")
        if error.file_path:
            suggestions.append(f"Verify file exists: {error.file_path}")
    
    elif isinstance(error, AnalysisError):
        suggestions.append("Check that all required data is present")
        suggestions.append("Verify QAQC configuration settings")
        suggestions.append("Ensure CRM values are correctly specified")
    
    elif isinstance(error, ReportGenerationError):
        suggestions.append("Check that analysis results are available")
        suggestions.append("Verify output directory is writable")
        suggestions.append("Ensure sufficient disk space is available")
    
    elif isinstance(error, ConfigurationError):
        suggestions.append("Check configuration file format")
        suggestions.append("Verify all required settings are present")
        suggestions.append("Review configuration documentation")
    
    elif isinstance(error, ValidationError):
        suggestions.append("Check input data format")
        suggestions.append("Verify data types are correct")
        suggestions.append("Review validation error details")
    
    elif isinstance(error, FileNotFoundError):
        suggestions.append("Check that the file path is correct")
        suggestions.append("Verify the file exists")
        suggestions.append("Check file permissions")
    
    elif isinstance(error, MemoryError):
        suggestions.append("Try processing a smaller dataset")
        suggestions.append("Close other applications to free memory")
        suggestions.append("Consider processing data in batches")
    
    else:
        suggestions.append("Check the error message for details")
        suggestions.append("Review application logs")
        suggestions.append("Contact support if the problem persists")
    
    return suggestions


def log_error_with_context(error: Exception, context: Optional[Dict[str, Any]] = None):
    """Log error with additional context."""
    context = context or {}
    
    if isinstance(error, QAQCError):
        context.update(error.details)
    
    logger.error(
        f"Error: {get_user_friendly_error_message(error)}",
        exc_info=True,
        extra=context
    )


def handle_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle an error and return structured error information."""
    log_error_with_context(error, context)
    
    return {
        'error_type': type(error).__name__,
        'message': get_user_friendly_error_message(error),
        'suggestions': get_error_recovery_suggestions(error),
        'details': context or {}
    }
