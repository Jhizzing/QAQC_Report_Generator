import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication, QStackedWidget
from src.gui.main_window import QAQCApplication
from src.gui.widgets.sidebar import Sidebar

def verify_layout():
    app = QApplication(sys.argv)
    window = QAQCApplication()
    
    # Check if sidebar exists
    if not hasattr(window, 'sidebar'):
        print("FAIL: Sidebar not found in MainWindow")
        return False
    
    if not isinstance(window.sidebar, Sidebar):
        print("FAIL: window.sidebar is not an instance of Sidebar")
        return False
        
    # Check if content_area exists
    if not hasattr(window, 'content_area'):
        print("FAIL: Content area not found in MainWindow")
        return False
        
    if not isinstance(window.content_area, QStackedWidget):
        print("FAIL: window.content_area is not an instance of QStackedWidget")
        return False
        
    # Check if panels are added to content_area
    if window.content_area.count() != 3:
        print(f"FAIL: Expected 3 panels in content area, found {window.content_area.count()}")
        return False
        
    print("SUCCESS: GUI layout verification passed!")
    return True

if __name__ == "__main__":
    success = verify_layout()
    sys.exit(0 if success else 1)
