"""
Results Dashboard Widget

Provides a summary dashboard showing key QAQC metrics at a glance:
pass/fail cards, JORC compliance gauge, and a quick-stats grid.
Designed for geologists to rapidly assess data quality.
"""

from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QGridLayout, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor


class MetricCard(QFrame):
    """Single metric card with title, value, and status colour."""

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumSize(160, 100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            "color: #94A3B8; font-size: 10px; font-weight: bold; "
            "text-transform: uppercase; letter-spacing: 1px;"
        )
        layout.addWidget(self.title_label)

        self.value_label = QLabel("—")
        self.value_label.setStyleSheet(
            "color: #F1F5F9; font-size: 22px; font-weight: bold;"
        )
        layout.addWidget(self.value_label)

        self.detail_label = QLabel("")
        self.detail_label.setStyleSheet("color: #64748B; font-size: 10px;")
        layout.addWidget(self.detail_label)

        self._apply_base_style()

    def _apply_base_style(self):
        self.setStyleSheet(
            "MetricCard { background-color: #1E293B; "
            "border: 1px solid #334155; border-radius: 8px; }"
        )

    def set_value(self, value: str, detail: str = "", status: str = "neutral"):
        """Update the card value and optional detail text."""
        self.value_label.setText(value)
        self.detail_label.setText(detail)

        colour_map = {
            "pass": "#10B981", "fail": "#EF4444",
            "warning": "#F59E0B", "neutral": "#F1F5F9",
        }
        colour = colour_map.get(status, "#F1F5F9")
        self.value_label.setStyleSheet(
            f"color: {colour}; font-size: 22px; font-weight: bold;"
        )

        border_map = {
            "pass": "#059669", "fail": "#DC2626",
            "warning": "#D97706", "neutral": "#334155",
        }
        border = border_map.get(status, "#334155")
        self.setStyleSheet(
            f"MetricCard {{ background-color: #1E293B; "
            f"border: 1px solid {border}; border-radius: 8px; }}"
        )


class StatusBadge(QLabel):
    """Small PASS / FAIL badge."""

    def __init__(self, text: str = "", passed: bool = True, parent=None):
        super().__init__(text, parent)
        self.set_status(text, passed)

    def set_status(self, text: str, passed: bool):
        self.setText(text)
        if passed:
            self.setStyleSheet(
                "background-color: #059669; color: #ECFDF5; "
                "font-weight: bold; font-size: 11px; "
                "padding: 4px 12px; border-radius: 4px;"
            )
        else:
            self.setStyleSheet(
                "background-color: #DC2626; color: #FEF2F2; "
                "font-weight: bold; font-size: 11px; "
                "padding: 4px 12px; border-radius: 4px;"
            )


class ResultsDashboard(QWidget):
    """
    Summary dashboard for QAQC analysis results.

    Shows metric cards for each analysis type, overall JORC compliance,
    and a quick-stats grid.
    """

    navigate_to_detail = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.results: Optional[Dict[str, Any]] = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        header = QLabel("Results Dashboard")
        header.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #F59E0B;"
        )
        layout.addWidget(header)

        self.overall_badge = StatusBadge("NO DATA", passed=True)
        layout.addWidget(self.overall_badge, alignment=Qt.AlignmentFlag.AlignLeft)

        # Metric cards row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(10)

        self.standards_card = MetricCard("Standards")
        self.blanks_card = MetricCard("Blanks")
        self.duplicates_card = MetricCard("Duplicates")
        self.jorc_card = MetricCard("JORC Compliance")

        for card in (self.standards_card, self.blanks_card,
                     self.duplicates_card, self.jorc_card):
            cards_layout.addWidget(card)

        layout.addLayout(cards_layout)

        # Stats grid
        self.stats_group = QGroupBox("Quick Stats")
        self.stats_group.setStyleSheet(
            "QGroupBox { color: #CBD5E1; font-weight: bold; "
            "border: 1px solid #334155; border-radius: 6px; "
            "margin-top: 8px; padding-top: 20px; } "
            "QGroupBox::title { subcontrol-origin: margin; "
            "left: 12px; padding: 0 6px; }"
        )
        self.stats_grid = QGridLayout(self.stats_group)
        self.stats_grid.setSpacing(8)

        self._stat_labels: Dict[str, QLabel] = {}
        stat_keys = [
            ("Total Samples", "total_samples"),
            ("Analysis Date", "analysis_date"),
            ("Standards Count", "standards_count"),
            ("Blanks Count", "blanks_count"),
            ("Duplicates Count", "duplicates_count"),
            ("Overall Pass Rate", "pass_rate"),
        ]
        for i, (display, key) in enumerate(stat_keys):
            row, col = divmod(i, 3)
            name_lbl = QLabel(display)
            name_lbl.setStyleSheet("color: #94A3B8; font-size: 10px;")
            val_lbl = QLabel("—")
            val_lbl.setStyleSheet(
                "color: #F1F5F9; font-size: 13px; font-weight: bold;"
            )
            self.stats_grid.addWidget(name_lbl, row * 2, col)
            self.stats_grid.addWidget(val_lbl, row * 2 + 1, col)
            self._stat_labels[key] = val_lbl

        layout.addWidget(self.stats_group)
        layout.addStretch()

    def set_results(self, results: Dict[str, Any]):
        """Update the dashboard with new analysis results."""
        self.results = results
        self._update_cards(results)
        self._update_stats(results)

    def reset(self):
        """Clear the dashboard."""
        self.results = None
        for card in (self.standards_card, self.blanks_card,
                     self.duplicates_card, self.jorc_card):
            card.set_value("—")
        for lbl in self._stat_labels.values():
            lbl.setText("—")
        self.overall_badge.set_status("NO DATA", True)

    def _status_for(self, result: dict) -> str:
        if 'error' in result:
            return "warning"
        return "pass" if result.get('overall_acceptable', False) else "fail"

    def _update_cards(self, results: Dict[str, Any]):
        std = results.get('standards')
        if isinstance(std, dict) and 'error' not in std:
            recovery = std.get('recovery', {}).get('mean_recovery', 0)
            self.standards_card.set_value(
                f"{recovery:.1f}%",
                f"Mean recovery | {std.get('summary', {}).get('n_measurements', '?')} measurements",
                self._status_for(std))
        else:
            self.standards_card.set_value("N/A", "Not run or no data", "neutral")

        blk = results.get('blanks')
        if isinstance(blk, dict) and 'error' not in blk:
            rate = blk.get('contamination', {}).get('contamination_rate', 0) * 100
            self.blanks_card.set_value(
                f"{rate:.1f}%",
                f"Contamination rate | {blk.get('summary', {}).get('n_blanks', '?')} blanks",
                self._status_for(blk))
        else:
            self.blanks_card.set_value("N/A", "Not run or no data", "neutral")

        dup = results.get('duplicates')
        if isinstance(dup, dict) and 'error' not in dup:
            mean_rpd = dup.get('precision', {}).get('mean_rpd', 0)
            self.duplicates_card.set_value(
                f"{mean_rpd:.1f}%",
                f"Mean RPD | {dup.get('summary', {}).get('n_duplicates', '?')} pairs",
                self._status_for(dup))
        else:
            self.duplicates_card.set_value("N/A", "Not run or no data", "neutral")

        pass_count = 0
        total_count = 0
        for key in ('standards', 'blanks', 'duplicates'):
            r = results.get(key)
            if isinstance(r, dict) and 'error' not in r:
                total_count += 1
                if r.get('overall_acceptable', False):
                    pass_count += 1

        if total_count > 0:
            jorc_pct = pass_count / total_count * 100
            jorc_status = "pass" if jorc_pct == 100 else ("warning" if jorc_pct >= 50 else "fail")
            self.jorc_card.set_value(
                f"{pass_count}/{total_count}",
                f"{jorc_pct:.0f}% analyses passed",
                jorc_status)
            overall_pass = pass_count == total_count
            self.overall_badge.set_status(
                "ALL PASS" if overall_pass else "ACTION REQUIRED",
                overall_pass)
        else:
            self.jorc_card.set_value("—", "No analyses completed", "neutral")
            self.overall_badge.set_status("NO DATA", True)

    def _update_stats(self, results: Dict[str, Any]):
        self._stat_labels['total_samples'].setText(str(results.get('total_samples', '—')))
        self._stat_labels['analysis_date'].setText(str(results.get('analysis_date', '—')))

        std = results.get('standards', {})
        self._stat_labels['standards_count'].setText(
            str(std.get('summary', {}).get('n_measurements', '—'))
            if isinstance(std, dict) and 'error' not in std else '—')

        blk = results.get('blanks', {})
        self._stat_labels['blanks_count'].setText(
            str(blk.get('summary', {}).get('n_blanks', '—'))
            if isinstance(blk, dict) and 'error' not in blk else '—')

        dup = results.get('duplicates', {})
        self._stat_labels['duplicates_count'].setText(
            str(dup.get('summary', {}).get('n_duplicates', '—'))
            if isinstance(dup, dict) and 'error' not in dup else '—')

        pass_count = 0
        total = 0
        for key in ('standards', 'blanks', 'duplicates'):
            r = results.get(key)
            if isinstance(r, dict) and 'error' not in r:
                total += 1
                if r.get('overall_acceptable', False):
                    pass_count += 1
        self._stat_labels['pass_rate'].setText(f"{pass_count}/{total}" if total else "—")
