"""
GUI Helper Functions

This module provides utility functions for the QAQC Analysis Application GUI.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
import os

from PyQt6.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap


class GuiHelpers:
    """Helper functions for GUI operations."""

    @staticmethod
    def show_info_message(parent: QWidget, title: str, message: str):
        """Show an information message box."""
        QMessageBox.information(parent, title, message)

    @staticmethod
    def show_warning_message(parent: QWidget, title: str, message: str):
        """Show a warning message box."""
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def show_error_message(parent: QWidget, title: str, message: str):
        """Show an error message box."""
        QMessageBox.critical(parent, title, message)

    @staticmethod
    def show_question_message(parent: QWidget, title: str, message: str) -> bool:
        """Show a question message box and return user response."""
        reply = QMessageBox.question(parent, title, message,
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return reply == QMessageBox.StandardButton.Yes

    @staticmethod
    def get_open_file_path(parent: QWidget, title: str, file_filter: str = "All Files (*)") -> Optional[str]:
        """Get file path from open file dialog."""
        file_path, _ = QFileDialog.getOpenFileName(parent, title, "", file_filter)
        return file_path if file_path else None

    @staticmethod
    def get_save_file_path(parent: QWidget, title: str, file_filter: str = "All Files (*)") -> Optional[str]:
        """Get file path from save file dialog."""
        file_path, _ = QFileDialog.getSaveFileName(parent, title, "", file_filter)
        return file_path if file_path else None

    @staticmethod
    def get_directory_path(parent: QWidget, title: str) -> Optional[str]:
        """Get directory path from directory dialog."""
        dir_path = QFileDialog.getExistingDirectory(parent, title)
        return dir_path if dir_path else None

    @staticmethod
    def create_icon(icon_path: str, size: QSize = QSize(24, 24)) -> QIcon:
        """Create an icon from file path."""
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            return QIcon(pixmap.scaled(size))
        return QIcon()

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.1f} {size_names[i]}"

    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
        """Format number with specified decimal places."""
        return f"{value:.{decimals}f}"

    @staticmethod
    def format_percentage(value: float, decimals: int = 1) -> str:
        """Format percentage with specified decimal places."""
        return f"{value:.{decimals}f}%"

    @staticmethod
    def validate_file_extension(file_path: str, allowed_extensions: List[str]) -> bool:
        """Validate file extension."""
        if not file_path:
            return False

        file_ext = Path(file_path).suffix.lower()
        return file_ext in [ext.lower() for ext in allowed_extensions]

    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get file information."""
        if not os.path.exists(file_path):
            return {}

        stat = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'path': file_path,
            'size': stat.st_size,
            'size_formatted': GuiHelpers.format_file_size(stat.st_size),
            'modified': stat.st_mtime,
            'extension': Path(file_path).suffix.lower()
        }
