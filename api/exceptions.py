"""
Custom exceptions for QAQC API
"""
from fastapi import HTTPException, status


class QAQCException(HTTPException):
    """Base exception for QAQC API errors"""
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or f"QAQC_{status_code}"


class FileProcessingError(QAQCException):
    """Error during file processing"""
    def __init__(self, detail: str, error_code: str = "FILE_PROCESSING_ERROR"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )


class FileNotFoundError(QAQCException):
    """File not found error"""
    def __init__(self, file_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with ID '{file_id}' not found",
            error_code="FILE_NOT_FOUND"
        )


class AnalysisNotFoundError(QAQCException):
    """Analysis not found error"""
    def __init__(self, analysis_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis with ID '{analysis_id}' not found",
            error_code="ANALYSIS_NOT_FOUND"
        )


class AnalysisExecutionError(QAQCException):
    """Error during analysis execution"""
    def __init__(self, detail: str, error_code: str = "ANALYSIS_EXECUTION_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code
        )


class ReportGenerationError(QAQCException):
    """Error during report generation"""
    def __init__(self, detail: str, error_code: str = "REPORT_GENERATION_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code
        )


class ValidationError(QAQCException):
    """Input validation error"""
    def __init__(self, detail: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )
