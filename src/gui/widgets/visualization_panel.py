"""
Visualization Panel Widget

This widget handles plot generation and visualization for the
QAQC Analysis Application. Designed for geologists working with assay data.
"""

from typing import Optional, Dict, Any, List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QGroupBox, QComboBox, QCheckBox, QSpinBox,
    QFileDialog, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..styles.geological_theme import GeologicalTheme


class PlotCanvas(FigureCanvas):
    """Custom matplotlib canvas for interactive plots."""

    def __init__(self, parent=None, width=8, height=6, dpi=100):
        # Set matplotlib backend before creating figure
        import matplotlib
        matplotlib.use('QtAgg')

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

        # Apply geological theme to matplotlib
        self.apply_geological_theme()

    def apply_geological_theme(self):
        """Apply geological theme to matplotlib plots."""
        # Set color scheme
        plt.style.use('default')

        # Custom colors for geological theme
        self.colors = {
            'primary': '#2E5266',
            'secondary': '#4A7C59',
            'accent': '#8B4513',
            'success': '#27AE60',
            'warning': '#F39C12',
            'error': '#E74C3C',
            'info': '#3498DB'
        }

        # Set default colors
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=[
            self.colors['primary'],
            self.colors['secondary'],
            self.colors['accent'],
            self.colors['success'],
            self.colors['warning'],
            self.colors['error'],
            self.colors['info']
        ])

        # Set other style parameters
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 16


class VisualizationPanel(QWidget):
    """
    Visualization panel widget for generating and displaying plots.

    Provides functionality for:
    - Interactive plot generation
    - Multiple plot types (control charts, scatter plots, histograms)
    - Plot customization and export
    - Real-time visualization updates
    """

    # Signals
    plot_requested = pyqtSignal(str)
    export_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Visualization state
        self.current_plots: Dict[str, Any] = {}
        self.plot_data: Optional[Dict[str, Any]] = None

        # Initialize UI
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()

    def setup_ui(self):
        """Set up the visualization panel user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Plot controls group
        self.controls_group = QGroupBox("Plot Controls")
        controls_layout = QHBoxLayout(self.controls_group)

        # Plot type selection
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems([
            "Standards Control Chart",
            "Blanks Histogram",
            "Duplicates Scatter Plot",
            "Results Distribution",
            "All Plots"
        ])
        controls_layout.addWidget(QLabel("Plot Type:"))
        controls_layout.addWidget(self.plot_type_combo)

        # Generate plot button
        self.generate_button = QPushButton("Generate Plot")
        self.generate_button.setMinimumHeight(35)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #2E5266;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4A7C59;
            }
        """)
        controls_layout.addWidget(self.generate_button)

        # Export button
        self.export_button = QPushButton("Export Plot")
        self.export_button.setMinimumHeight(35)
        self.export_button.setEnabled(False)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
            QPushButton:disabled {
                background-color: #ADB5BD;
            }
        """)
        controls_layout.addWidget(self.export_button)

        layout.addWidget(self.controls_group)

        # Plot display area
        self.plot_widget = QTabWidget()

        # Standards plot tab
        self.standards_tab = QWidget()
        standards_layout = QVBoxLayout(self.standards_tab)
        self.standards_canvas = PlotCanvas(self.standards_tab, width=8, height=6)
        standards_layout.addWidget(self.standards_canvas)
        self.plot_widget.addTab(self.standards_tab, "Standards")

        # Blanks plot tab
        self.blanks_tab = QWidget()
        blanks_layout = QVBoxLayout(self.blanks_tab)
        self.blanks_canvas = PlotCanvas(self.blanks_tab, width=8, height=6)
        blanks_layout.addWidget(self.blanks_canvas)
        self.plot_widget.addTab(self.blanks_tab, "Blanks")

        # Duplicates plot tab
        self.duplicates_tab = QWidget()
        duplicates_layout = QVBoxLayout(self.duplicates_tab)
        self.duplicates_canvas = PlotCanvas(self.duplicates_tab, width=8, height=6)
        duplicates_layout.addWidget(self.duplicates_canvas)
        self.plot_widget.addTab(self.duplicates_tab, "Duplicates")

        # Results plot tab
        self.results_tab = QWidget()
        results_layout = QVBoxLayout(self.results_tab)
        self.results_canvas = PlotCanvas(self.results_tab, width=8, height=6)
        results_layout.addWidget(self.results_canvas)
        self.plot_widget.addTab(self.results_tab, "Results")

        layout.addWidget(self.plot_widget)

        # Plot information group
        self.info_group = QGroupBox("Plot Information")
        info_layout = QVBoxLayout(self.info_group)

        self.plot_info_label = QLabel("No plot generated")
        self.plot_info_label.setWordWrap(True)
        self.plot_info_label.setStyleSheet("""
            QLabel {
                color: #6C757D;
                font-style: italic;
                padding: 8px;
                background-color: #F8F9FA;
                border: 1px solid #DEE2E6;
                border-radius: 4px;
            }
        """)
        info_layout.addWidget(self.plot_info_label)

        layout.addWidget(self.info_group)

    def setup_connections(self):
        """Set up signal connections."""
        self.generate_button.clicked.connect(self.generate_plot)
        self.export_button.clicked.connect(self.export_plot)

    def apply_theme(self):
        """Apply the geological theme."""
        theme = GeologicalTheme()
        self.setStyleSheet(theme.get_widget_style('visualization_panel'))

    def show_styled_warning(self, title, message):
        """Show a styled warning message."""
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
                color: #1A1A1A;
            }
            QMessageBox QPushButton {
                background-color: #2E5266;
                color: #FFFFFF;
                border: 2px solid #2E5266;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
                min-width: 100px;
                min-height: 30px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4A7C59;
                border-color: #4A7C59;
                color: #FFFFFF;
            }
            QMessageBox QPushButton:pressed {
                background-color: #1A3A4A;
                border-color: #1A3A4A;
                color: #FFFFFF;
            }
        """)
        return msg.exec()

    def generate_plot(self):
        """Generate the selected plot type."""
        plot_type = self.plot_type_combo.currentText()

        # Check if data is loaded and valid
        if not self.plot_data or not isinstance(self.plot_data, dict) or 'data' not in self.plot_data or self.plot_data['data'].empty:
            self.show_styled_warning("No Data", "Please load data before generating plots.")
            return

        print(f"Generating plot: {plot_type} with data: {list(self.plot_data.keys()) if self.plot_data else 'None'}")

        try:
            if plot_type == "Standards Control Chart":
                self.create_standards_plot()
            elif plot_type == "Blanks Histogram":
                self.create_blanks_plot()
            elif plot_type == "Duplicates Scatter Plot":
                self.create_duplicates_plot()
            elif plot_type == "Results Distribution":
                self.create_results_plot()
            elif plot_type == "All Plots":
                self.create_all_plots()

            self.export_button.setEnabled(True)
            self.plot_info_label.setText(f"Generated: {plot_type}")
            self.plot_info_label.setStyleSheet("""
                QLabel {
                    color: #27AE60;
                    font-weight: bold;
                    padding: 8px;
                    background-color: #F8F9FA;
                    border: 1px solid #DEE2E6;
                    border-radius: 4px;
                }
            """)

        except Exception as e:
            QMessageBox.critical(self, "Plot Error", f"Failed to generate plot: {str(e)}")
            self.plot_info_label.setText(f"Error: {str(e)}")
            self.plot_info_label.setStyleSheet("""
                QLabel {
                    color: #E74C3C;
                    font-weight: bold;
                    padding: 8px;
                    background-color: #F8F9FA;
                    border: 1px solid #DEE2E6;
                    border-radius: 4px;
                }
            """)

    def create_standards_plot(self):
        """Create standards control chart."""
        try:
            canvas = self.standards_canvas
            canvas.fig.clear()

            # Simulate standards data
            standards_data = np.random.normal(0.85, 0.05, 20)
            certified_value = 0.85
            uncertainty = 0.05

            ax = canvas.fig.add_subplot(111)

            # Plot data points
            ax.plot(range(1, len(standards_data) + 1), standards_data, 'o-',
                    color=canvas.colors['primary'], markersize=6, linewidth=2)

            # Add control limits
            ax.axhline(y=certified_value, color=canvas.colors['success'],
                      linestyle='-', linewidth=2, label='Certified Value')
            ax.axhline(y=certified_value + 2*uncertainty, color=canvas.colors['warning'],
                      linestyle='--', linewidth=1, label='±2σ')
            ax.axhline(y=certified_value - 2*uncertainty, color=canvas.colors['warning'],
                      linestyle='--', linewidth=1)
            ax.axhline(y=certified_value + 3*uncertainty, color=canvas.colors['error'],
                      linestyle=':', linewidth=1, label='±3σ')
            ax.axhline(y=certified_value - 3*uncertainty, color=canvas.colors['error'],
                      linestyle=':', linewidth=1)

            ax.set_xlabel('Sample Number')
            ax.set_ylabel('Concentration (g/t)')
            ax.set_title('Standards Control Chart')
            ax.legend()
            ax.grid(True, alpha=0.3)

            canvas.draw()

        except Exception as e:
            print(f"Error creating standards plot: {e}")
            # Create a simple error plot
            canvas = self.standards_canvas
            canvas.fig.clear()
            ax = canvas.fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error creating plot:\n{str(e)}",
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Standards Control Chart - Error')
            canvas.draw()

    def create_blanks_plot(self):
        """Create blanks histogram."""
        try:
            canvas = self.blanks_canvas
            canvas.fig.clear()

            # Simulate blanks data
            blanks_data = np.random.normal(0.01, 0.005, 15)

            ax = canvas.fig.add_subplot(111)

            # Create histogram
            n, bins, patches = ax.hist(blanks_data, bins=10, alpha=0.7,
                                     color=canvas.colors['secondary'], edgecolor='black')

            # Add detection limit line
            dl = 0.01
            ax.axvline(x=dl, color=canvas.colors['warning'],
                      linestyle='--', linewidth=2, label='Detection Limit')

            # Add contamination threshold
            threshold = 3 * dl
            ax.axvline(x=threshold, color=canvas.colors['error'],
                      linestyle=':', linewidth=2, label='Contamination Threshold')

            ax.set_xlabel('Concentration (g/t)')
            ax.set_ylabel('Frequency')
            ax.set_title('Blanks Distribution')
            ax.legend()
            ax.grid(True, alpha=0.3)

            canvas.draw()

        except Exception as e:
            print(f"Error creating blanks plot: {e}")
            # Create a simple error plot
            canvas = self.blanks_canvas
            canvas.fig.clear()
            ax = canvas.fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error creating plot:\n{str(e)}",
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Blanks Distribution - Error')
            canvas.draw()

    def create_duplicates_plot(self):
        """Create duplicates scatter plot."""
        canvas = self.duplicates_canvas
        canvas.fig.clear()

        # Simulate duplicates data
        n_pairs = 8
        x_data = np.random.uniform(0.5, 3.0, n_pairs)
        y_data = x_data + np.random.normal(0, 0.1, n_pairs)

        ax = canvas.fig.add_subplot(111)

        # Plot duplicate pairs
        ax.scatter(x_data, y_data, color=canvas.colors['accent'],
                  s=100, alpha=0.7, edgecolors='black')

        # Add 1:1 line
        min_val = min(min(x_data), min(y_data))
        max_val = max(max(x_data), max(y_data))
        ax.plot([min_val, max_val], [min_val, max_val],
               color=canvas.colors['success'], linestyle='-', linewidth=2,
               label='1:1 Line')

        # Add RPD lines
        rpd_20 = 0.20  # 20% RPD
        ax.plot([min_val, max_val], [min_val * (1 + rpd_20), max_val * (1 + rpd_20)],
               color=canvas.colors['warning'], linestyle='--', linewidth=1,
               label='±20% RPD')
        ax.plot([min_val, max_val], [min_val * (1 - rpd_20), max_val * (1 - rpd_20)],
               color=canvas.colors['warning'], linestyle='--', linewidth=1)

        ax.set_xlabel('First Analysis (g/t)')
        ax.set_ylabel('Duplicate Analysis (g/t)')
        ax.set_title('Duplicates Scatter Plot')
        ax.legend()
        ax.grid(True, alpha=0.3)

        canvas.draw()

    def create_results_plot(self):
        """Create results distribution histogram."""
        canvas = self.results_canvas
        canvas.fig.clear()

        # Simulate results data
        results_data = np.random.lognormal(0, 0.5, 100)

        ax = canvas.fig.add_subplot(111)

        # Create histogram
        n, bins, patches = ax.hist(results_data, bins=20, alpha=0.7,
                                 color=canvas.colors['info'], edgecolor='black')

        # Add statistics
        mean_val = np.mean(results_data)
        median_val = np.median(results_data)

        ax.axvline(x=mean_val, color=canvas.colors['success'],
                  linestyle='-', linewidth=2, label=f'Mean: {mean_val:.3f}')
        ax.axvline(x=median_val, color=canvas.colors['warning'],
                  linestyle='--', linewidth=2, label=f'Median: {median_val:.3f}')

        ax.set_xlabel('Concentration (g/t)')
        ax.set_ylabel('Frequency')
        ax.set_title('Results Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)

        canvas.draw()

    def create_all_plots(self):
        """Create all plot types."""
        self.create_standards_plot()
        self.create_blanks_plot()
        self.create_duplicates_plot()
        self.create_results_plot()

    def export_plot(self):
        """Export the current plot."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Plot",
            "",
            "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg);;All Files (*)"
        )

        if file_path:
            try:
                # Get current tab
                current_tab = self.plot_widget.currentIndex()

                if current_tab == 0:  # Standards
                    canvas = self.standards_canvas
                elif current_tab == 1:  # Blanks
                    canvas = self.blanks_canvas
                elif current_tab == 2:  # Duplicates
                    canvas = self.duplicates_canvas
                elif current_tab == 3:  # Results
                    canvas = self.results_canvas
                else:
                    QMessageBox.warning(self, "No Plot", "No plot to export.")
                    return

                # Save plot
                canvas.fig.savefig(file_path, dpi=300, bbox_inches='tight')

                QMessageBox.information(self, "Export Successful",
                                      f"Plot saved to: {file_path}")

            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export plot: {str(e)}")

    def set_plot_data(self, data: Dict[str, Any]):
        """Set plot data for visualization."""
        # Only set data if it's valid and contains actual data
        if data and isinstance(data, dict) and 'data' in data and not data['data'].empty:
            self.plot_data = data
            print(f"Plot data set: {list(data.keys()) if data else 'None'}")
        else:
            self.plot_data = None
            print("No valid data provided - plot data cleared")

    def reset(self):
        """Reset the visualization panel to initial state."""
        self.current_plots = {}
        self.plot_data = None

        # Clear all canvases
        self.standards_canvas.fig.clear()
        self.blanks_canvas.fig.clear()
        self.duplicates_canvas.fig.clear()
        self.results_canvas.fig.clear()

        # Update displays
        self.plot_info_label.setText("No plot generated")
        self.plot_info_label.setStyleSheet("""
            QLabel {
                color: #6C757D;
                font-style: italic;
                padding: 8px;
                background-color: #F8F9FA;
                border: 1px solid #DEE2E6;
                border-radius: 4px;
            }
        """)

        self.export_button.setEnabled(False)
