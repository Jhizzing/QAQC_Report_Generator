"""
Custom Themed Checkbox Widget

A custom checkbox widget that displays an amber gold background with a dark checkmark
when checked, matching the LogiQore theme for the QAQC Analysis Application.
"""

from PyQt6.QtWidgets import QCheckBox, QStyleOptionButton, QStyle
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QPen, QColor

from ..styles.geological_theme import GeologicalTheme


class GreenCheckBox(QCheckBox):
    """
    Custom checkbox with green background and white checkmark.

    When checked, displays a green box with a white checkmark.
    When unchecked, displays a white box with gray border.
    """

    def __init__(self, text: str = "", parent=None):
        """Initialize the green checkbox."""
        super().__init__(text, parent)
        self.theme = GeologicalTheme()
        self.setMinimumHeight(24)  # Ensure enough space for the checkbox
        # Hide the default indicator so we can draw our own
        self.setStyleSheet("QCheckBox::indicator { width: 0px; height: 0px; }")

    def sizeHint(self):
        """Return the recommended size for the checkbox."""
        base_size = super().sizeHint()
        return QSize(base_size.width() + 18, max(base_size.height(), 24))

    def paintEvent(self, event):
        """Custom paint event to draw the checkbox with green background and white checkmark."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get checkbox indicator rectangle
        indicator_size = 18
        indicator_rect = QRect(0, (self.height() - indicator_size) // 2,
                              indicator_size, indicator_size)

        # Draw checkbox background
        if self.isChecked():
            # Amber gold background when checked (matches LogiQore theme)
            painter.setBrush(QColor(self.theme.get_color('primary')))
            painter.setPen(QColor(self.theme.get_color('primary')))
        else:
            # White background when unchecked
            painter.setBrush(QColor(self.theme.get_color('surface')))
            pen_color = QColor(self.theme.get_color('border_dark'))
            pen_color.setAlpha(200)  # Slightly transparent border
            painter.setPen(QPen(pen_color, 2))

        # Draw rounded rectangle for checkbox
        painter.drawRoundedRect(indicator_rect, 4, 4)

        # Draw checkmark if checked
        if self.isChecked():
            # Draw dark checkmark (✓) on amber background - bold and clearly visible
            pen = QPen(QColor("#0F172A"))  # Dark slate for contrast on gold
            pen.setWidth(3)  # Thicker line for better visibility
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)

            # Draw checkmark path - two lines forming a checkmark
            # Start from left-middle, down to center-bottom, then up-right
            # Adjusted coordinates for better visibility
            x1 = indicator_rect.left() + 5
            y1 = indicator_rect.center().y() + 1
            x2 = indicator_rect.center().x()
            y2 = indicator_rect.bottom() - 5
            x3 = indicator_rect.right() - 5
            y3 = indicator_rect.top() + 6

            # Draw the checkmark as two connected lines
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            painter.drawLine(int(x2), int(y2), int(x3), int(y3))

        # Draw text label
        text_rect = QRect(indicator_size + 8, 0,
                         self.width() - indicator_size - 8, self.height())
        text_color = QColor(self.theme.get_color('text_primary'))
        painter.setPen(text_color)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                        self.text())
