"""
Report Service — generates Word document reports from analysis results.

For v1.0, the primary output is a Word (.docx) template with plots, tables,
and placeholder sections for user commentary.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from reporting import QAQCDOCXReporter


class ReportService:
    """Generates QAQC reports from analysis results."""

    def __init__(self) -> None:
        self.docx_reporter = QAQCDOCXReporter()

    def generate_docx(
        self,
        analysis_results: Dict[str, Any],
        output_path: str,
        metadata: Optional[Dict[str, str]] = None,
        plot_images: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Generate a Word document report.

        Args:
            analysis_results: Full results dict from AnalysisService.
            output_path: Where to save the .docx file.
            metadata: Report metadata (project, author, date, lab).
            plot_images: Dict mapping plot name -> file path for embedded images.

        Returns:
            Path to the generated file.
        """
        meta = metadata or {}
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        self.docx_reporter.generate(
            results=analysis_results,
            output_path=str(path),
            metadata=meta,
            plot_images=plot_images or {},
        )

        return str(path)
