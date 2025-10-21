#!/usr/bin/env python3
"""
GUI Launcher for QAQC Analysis Application

This script launches the graphical user interface for the QAQC Analysis Application,
designed specifically for geologists working with assay data.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        return True
    except ImportError as e:
        print(f"Error: Missing required dependency: {e}")
        print("Please install PyQt6: pip install PyQt6")
        print("Make sure you're in the virtual environment:")
        print("   source venv/bin/activate")
        return False

def main():
    """Main entry point for GUI application."""
    print("QAQC Analysis Application - GUI Launcher")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    try:
        from PyQt6.QtWidgets import QApplication
        from src.gui.main_window import QAQCApplication

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("QAQC Analysis Application")
        app.setApplicationVersion("2.0.0")
        app.setOrganizationName("QAQC Analysis")

        # Create and show main window
        window = QAQCApplication()
        window.show()

        print("GUI launched successfully!")
        print("Application ready for geological data analysis.")

        # Run application
        return app.exec()

    except Exception as e:
        print(f"Error launching GUI: {e}")
        print("Please check your installation and try again.")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
