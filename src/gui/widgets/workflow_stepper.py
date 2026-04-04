"""
Workflow Stepper Widget

Horizontal step indicator showing progression through the QAQC workflow:
Import -> Configure -> Analyse -> Review -> Export.
"""

from typing import List, Optional

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QFont


class StepIndicator(QWidget):
    """Single step circle + label."""

    clicked = pyqtSignal()

    def __init__(self, label: str, index: int, parent=None):
        super().__init__(parent)
        self.label = label
        self.index = index
        self.state = "pending"  # pending | active | completed
        self.setFixedSize(100, 56)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_state(self, state: str):
        self.state = state
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx = self.width() // 2
        radius = 14

        colours = {
            "completed": ("#059669", "#ECFDF5"),
            "active":    ("#F59E0B", "#0F172A"),
            "pending":   ("#334155", "#94A3B8"),
        }
        bg_hex, fg_hex = colours.get(self.state, colours["pending"])

        # Circle
        p.setBrush(QColor(bg_hex))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(cx - radius, 4, radius * 2, radius * 2)

        # Number or tick
        p.setPen(QColor(fg_hex))
        font = QFont()
        font.setBold(True)
        font.setPixelSize(12)
        p.setFont(font)

        if self.state == "completed":
            p.drawText(cx - radius, 4, radius * 2, radius * 2,
                       Qt.AlignmentFlag.AlignCenter, "\u2713")
        else:
            p.drawText(cx - radius, 4, radius * 2, radius * 2,
                       Qt.AlignmentFlag.AlignCenter, str(self.index + 1))

        # Label below circle
        label_colour = "#F59E0B" if self.state == "active" else (
            "#10B981" if self.state == "completed" else "#94A3B8")
        p.setPen(QColor(label_colour))
        font.setPixelSize(10)
        font.setBold(self.state == "active")
        p.setFont(font)
        p.drawText(0, 36, self.width(), 18,
                   Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                   self.label)

    def mousePressEvent(self, event):
        self.clicked.emit()


class _ConnectorLine(QWidget):
    """Thin horizontal connector between step indicators."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(32, 56)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor("#475569"), 2))
        p.drawLine(0, 18, self.width(), 18)


class WorkflowStepper(QWidget):
    """
    Horizontal stepper showing the QAQC workflow progression.

    Emits ``step_clicked(index)`` when a step is clicked so the parent
    can navigate to that panel.
    """

    step_clicked = pyqtSignal(int)

    DEFAULT_STEPS = ["Import", "Configure", "Analyse", "Review", "Export"]

    def __init__(self, steps: Optional[List[str]] = None, parent=None):
        super().__init__(parent)
        self.steps = steps or self.DEFAULT_STEPS
        self._current = 0
        self._indicators: List[StepIndicator] = []

        self.setFixedHeight(64)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(0)

        layout.addStretch()

        for i, name in enumerate(self.steps):
            indicator = StepIndicator(name, i)
            indicator.clicked.connect(lambda idx=i: self._on_step_clicked(idx))
            self._indicators.append(indicator)
            layout.addWidget(indicator)

            if i < len(self.steps) - 1:
                layout.addWidget(_ConnectorLine())

        layout.addStretch()
        self._refresh_states()

    @property
    def current_step(self) -> int:
        return self._current

    def set_step(self, index: int):
        """Set the active step (0-based). Steps before it become completed."""
        if 0 <= index < len(self.steps):
            self._current = index
            self._refresh_states()

    def complete_step(self, index: int):
        """Mark a specific step as completed without changing active step."""
        if 0 <= index < len(self._indicators):
            self._indicators[index].set_state("completed")

    def reset(self):
        """Reset to the first step."""
        self._current = 0
        self._refresh_states()

    def _on_step_clicked(self, index: int):
        self.step_clicked.emit(index)

    def _refresh_states(self):
        for i, ind in enumerate(self._indicators):
            if i < self._current:
                ind.set_state("completed")
            elif i == self._current:
                ind.set_state("active")
            else:
                ind.set_state("pending")
