"""
Toast Notification Widget

Non-intrusive slide-in notifications that auto-dismiss.
Supports info, success, warning, and error levels.
"""

from typing import Optional

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer


class ToastNotification(QWidget):
    """
    Lightweight toast notification that appears at the top-right
    of its parent and auto-dismisses after a configurable duration.

    Usage::

        toast = ToastNotification(parent_widget)
        toast.show_toast("Analysis complete", level="success")
    """

    _STYLES = {
        "info": {
            "bg": "#1E293B", "border": "#3B82F6",
            "icon": "i", "icon_bg": "#2563EB", "text": "#F1F5F9",
        },
        "success": {
            "bg": "#1E293B", "border": "#10B981",
            "icon": "\u2713", "icon_bg": "#059669", "text": "#F1F5F9",
        },
        "warning": {
            "bg": "#1E293B", "border": "#F59E0B",
            "icon": "!", "icon_bg": "#D97706", "text": "#F1F5F9",
        },
        "error": {
            "bg": "#1E293B", "border": "#EF4444",
            "icon": "\u2717", "icon_bg": "#DC2626", "text": "#F1F5F9",
        },
    }

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(48)
        self.setMinimumWidth(280)
        self.setMaximumWidth(420)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._container = QWidget(self)
        container_layout = QHBoxLayout(self._container)
        container_layout.setContentsMargins(10, 8, 10, 8)
        container_layout.setSpacing(8)

        self._icon_label = QLabel()
        self._icon_label.setFixedSize(24, 24)
        self._icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self._icon_label)

        self._message_label = QLabel()
        self._message_label.setWordWrap(True)
        container_layout.addWidget(self._message_label, stretch=1)

        self._close_btn = QPushButton("\u00d7")
        self._close_btn.setFixedSize(20, 20)
        self._close_btn.setFlat(True)
        self._close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._close_btn.clicked.connect(self._dismiss)
        container_layout.addWidget(self._close_btn)

        self._layout.addWidget(self._container)

        self._dismiss_timer = QTimer(self)
        self._dismiss_timer.setSingleShot(True)
        self._dismiss_timer.timeout.connect(self._dismiss)

        self.hide()

    def show_toast(self, message: str, level: str = "info",
                   duration_ms: int = 4000):
        """
        Show a toast notification.

        Args:
            message: Text to display.
            level: One of 'info', 'success', 'warning', 'error'.
            duration_ms: Auto-dismiss delay (0 = manual only).
        """
        style = self._STYLES.get(level, self._STYLES["info"])

        self._container.setStyleSheet(
            f"QWidget {{ background-color: {style['bg']}; "
            f"border: 1px solid {style['border']}; border-radius: 8px; }}"
        )
        self._icon_label.setText(style["icon"])
        self._icon_label.setStyleSheet(
            f"background-color: {style['icon_bg']}; "
            f"color: white; font-weight: bold; font-size: 13px; border-radius: 12px;"
        )
        self._message_label.setText(message)
        self._message_label.setStyleSheet(
            f"color: {style['text']}; font-size: 12px; background: transparent; border: none;"
        )
        self._close_btn.setStyleSheet(
            f"color: {style['text']}; font-size: 16px; background: transparent; border: none;"
        )

        self._position_toast()
        self.show()
        self.raise_()

        if duration_ms > 0:
            self._dismiss_timer.start(duration_ms)

    def _position_toast(self):
        parent = self.parentWidget()
        if parent:
            x = parent.width() - self.width() - 16
            self.move(x, 16)

    def _dismiss(self):
        self._dismiss_timer.stop()
        self.hide()
