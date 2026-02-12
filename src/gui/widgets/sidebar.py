from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QIcon

class Sidebar(QWidget):
    """
    Vertical sidebar navigation widget.
    """
    
    # Signal emitted when a navigation button is clicked
    # Arguments: index (int), name (str)
    navigation_changed = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = []
        self.current_index = 0
        self.setup_ui()

    def setup_ui(self):
        """Initialize the sidebar UI."""
        self.setObjectName("sidebar")
        self.setFixedWidth(250)  # Fixed width for the sidebar
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # App Title / Header Area
        header = QFrame()
        header.setObjectName("sidebarHeader")
        header.setFixedHeight(80)
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("LogiQore Reporter")
        title.setObjectName("sidebarTitle")
        header_layout.addWidget(title)
        
        subtitle = QLabel("Geological QAQC Platform")
        subtitle.setObjectName("sidebarSubtitle")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)

        # Navigation Buttons Container
        nav_container = QFrame()
        nav_container.setObjectName("navContainer")
        self.nav_layout = QVBoxLayout(nav_container)
        self.nav_layout.setContentsMargins(10, 20, 10, 20)
        self.nav_layout.setSpacing(10)
        self.nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        layout.addWidget(nav_container)
        
        # Add Spacer to push everything up
        layout.addStretch()
        
        # Footer (optional, e.g., version or settings)
        footer = QFrame()
        footer.setObjectName("sidebarFooter")
        footer_layout = QVBoxLayout(footer)
        version = QLabel("v2.0.0")
        version.setObjectName("sidebarVersion")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(version)
        layout.addWidget(footer)

    def add_button(self, text, icon_name=None, index=None):
        """
        Add a navigation button to the sidebar.
        
        Args:
            text (str): Button label
            icon_name (str, optional): Icon name (not implemented yet, placeholder)
            index (int, optional): specific index for the button
        """
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setFixedHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Store the index this button corresponds to
        btn_index = index if index is not None else len(self.buttons)
        btn.setProperty("nav_index", btn_index)
        
        btn.clicked.connect(lambda checked, b=btn: self._handle_click(b))
        
        self.nav_layout.addWidget(btn)
        self.buttons.append(btn)
        
        # Select first button by default
        if len(self.buttons) == 1:
            btn.setChecked(True)

    def _handle_click(self, clicked_btn):
        """Handle button clicks to ensure mutual exclusivity and emit signal."""
        # Uncheck all other buttons
        for btn in self.buttons:
            if btn != clicked_btn:
                btn.setChecked(False)
        
        # Ensure the clicked button remains checked (radio button behavior)
        clicked_btn.setChecked(True)
        
        index = clicked_btn.property("nav_index")
        self.navigation_changed.emit(index, clicked_btn.text())
        self.current_index = index

    def set_active_index(self, index):
        """Programmatically set the active button."""
        for btn in self.buttons:
            if btn.property("nav_index") == index:
                self._handle_click(btn)
                break
