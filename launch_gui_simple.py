#!/usr/bin/env python3
"""
Simple GUI Launcher - Guaranteed to Work

This script launches the GUI with minimal complexity and maximum reliability.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Launch the GUI application."""
    print("QAQC Analysis Application - Simple GUI Launcher")
    print("=" * 50)

    try:
        # Import and setup
        from PyQt6.QtWidgets import QApplication
        from src.gui.main_window import QAQCApplication

        print("✓ Dependencies loaded")

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("QAQC Analysis Application")
        app.setApplicationVersion("2.0.0")

        print("✓ Application created")

        # Create main window
        window = QAQCApplication()
        print("✓ Main window created")

        # Show window
        window.show()
        print("✓ Window displayed")

        print("\n🎉 GUI launched successfully!")
        print("\n📋 How to use:")
        print("   1. Click 'Import Data File' in the left panel")
        print("   2. Select your CSV or Excel file")
        print("   3. Configure analysis in the right panel")
        print("   4. Click 'Generate Plot' in the bottom panel")
        print("   5. View your geological analysis plots!")

        # Run application
        return app.exec()

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTry the CLI version instead:")
        print("   python3 main.py --help")
        return 1

if __name__ == "__main__":
    sys.exit(main())
