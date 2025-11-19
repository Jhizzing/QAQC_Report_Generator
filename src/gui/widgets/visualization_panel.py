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
import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QGroupBox, QComboBox, QCheckBox, QSpinBox,
    QFileDialog, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..styles.geological_theme import GeologicalTheme
from ...visualization import PlotGenerator


class PlotCanvas(FigureCanvas):
    """Custom matplotlib canvas for interactive plots."""

    def __init__(self, parent=None, width=8, height=6, dpi=100):
        # Set matplotlib backend before creating figure (must be done before Figure)
        import matplotlib
        try:
            matplotlib.use('QtAgg', force=True)
        except Exception:
            pass  # Backend already set

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
        self.analysis_results: Optional[Dict[str, Any]] = None
        self.plot_generator = PlotGenerator()

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
        if not self.plot_data or not isinstance(self.plot_data, dict):
            self.show_styled_warning("No Data", "Please load data before generating plots.")
            return

        # Check for dataframe (either 'dataframe' or 'data' key)
        # Can't use 'or' with DataFrames - need explicit None check
        df = self.plot_data.get('dataframe')
        if df is None:
            df = self.plot_data.get('data')

        if df is None or (hasattr(df, 'empty') and df.empty):
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
            summary = self._build_plot_summary(plot_type)
            if summary:
                self.plot_info_label.setText(summary)
                self.plot_info_label.setStyleSheet("""
                    QLabel {
                        color: #1A1A1A;
                        font-weight: bold;
                        padding: 8px;
                        background-color: #E7F5EE;
                        border: 1px solid #B6E0C2;
                        border-radius: 4px;
                    }
                """)
            else:
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
            print(f"Error generating plot: {e}")
            import traceback
            traceback.print_exc()
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
        """Create standards control chart from real data."""
        try:
            canvas = self.standards_canvas
            canvas.fig.clear()

            # Get data from plot_data
            if not self.plot_data or 'dataframe' not in self.plot_data:
                raise ValueError("No data available for plotting")

            df = self.plot_data['dataframe']

            # Extract standards data
            # Try to find sample_type column (case-insensitive)
            type_col = None
            result_col = None
            for col in df.columns:
                col_lower = col.lower()
                if 'type' in col_lower or 'sample_type' in col_lower:
                    type_col = col
                if 'result' in col_lower or 'value' in col_lower or 'assay' in col_lower:
                    result_col = col

            if not type_col or not result_col:
                raise ValueError("Could not find required columns (sample_type, result)")

            # Filter for standards
            standards_df = df[df[type_col].str.upper().str.contains('STANDARD|STD|CRM', na=False, regex=True)].copy()

            if standards_df.empty:
                raise ValueError("No standards data found in dataset")

            # Convert result to numeric
            standards_df[result_col] = pd.to_numeric(standards_df[result_col], errors='coerce')
            standards_data = standards_df[result_col].dropna().tolist()

            if not standards_data:
                raise ValueError("No valid numeric standards data found")

            # Calculate statistics
            mean_value = np.mean(standards_data)
            std_value = np.std(standards_data)
            certified_value = mean_value  # Default if no CRM info available
            uncertainty = std_value

            # Incorporate analysis results if available
            analysis_result = None
            if hasattr(self, 'analysis_results') and self.analysis_results:
                analysis_result = self.analysis_results.get('standards')

            if isinstance(analysis_result, dict):
                summary = analysis_result.get('summary', {})
                precision = analysis_result.get('precision', {})

                certified_value = summary.get('certified_value', certified_value)
                uncertainty = summary.get('uncertainty', uncertainty)
                std_value = precision.get('std_dev', std_value) or std_value

            ax = canvas.fig.add_subplot(111)

            # Plot data points
            x_values = list(range(1, len(standards_data) + 1))
            ax.plot(x_values, standards_data, 'o-',
                    color=canvas.colors['primary'], markersize=6, linewidth=2, label='Standards')

            # Add control limits
            ax.axhline(y=certified_value, color=canvas.colors['success'],
                      linestyle='-', linewidth=2, label=f'Mean: {certified_value:.3f}')
            ax.axhline(y=certified_value + 2*std_value, color=canvas.colors['warning'],
                      linestyle='--', linewidth=1, label='±2σ')
            ax.axhline(y=certified_value - 2*std_value, color=canvas.colors['warning'],
                      linestyle='--', linewidth=1)
            ax.axhline(y=certified_value + 3*std_value, color=canvas.colors['error'],
                      linestyle=':', linewidth=1, label='±3σ')
            ax.axhline(y=certified_value - 3*std_value, color=canvas.colors['error'],
                      linestyle=':', linewidth=1)

            ax.set_xlabel('Sample Number')
            ax.set_ylabel('Concentration (g/t)')
            title = f'Standards Control Chart (n={len(standards_data)})'
            if isinstance(analysis_result, dict):
                status = "PASS" if analysis_result.get('overall_acceptable', False) else "FAIL"
                title += f' • {status}'
            ax.set_title(title)
            ax.legend()
            ax.grid(True, alpha=0.3)

            # Safely draw the canvas
            try:
                canvas.draw_idle()  # Use draw_idle instead of draw for better thread safety
            except Exception as draw_error:
                print(f"Warning: Could not draw canvas: {draw_error}")
                # Try regular draw as fallback
                try:
                    canvas.draw()
                except Exception:
                    pass  # If both fail, at least the plot is created

        except Exception as e:
            print(f"Error creating standards plot: {e}")
            import traceback
            traceback.print_exc()
            # Create a simple error plot
            try:
                canvas = self.standards_canvas
                canvas.fig.clear()
                ax = canvas.fig.add_subplot(111)
                ax.text(0.5, 0.5, f"Error creating plot:\n{str(e)}",
                       ha='center', va='center', transform=ax.transAxes, fontsize=10)
                ax.set_title('Standards Control Chart - Error')
                canvas.draw_idle()
            except Exception as draw_err:
                print(f"Could not display error plot: {draw_err}")

    def create_blanks_plot(self):
        """Create blanks histogram from real data."""
        try:
            canvas = self.blanks_canvas
            canvas.fig.clear()

            # Get data from plot_data
            if not self.plot_data or 'dataframe' not in self.plot_data:
                raise ValueError("No data available for plotting")

            df = self.plot_data['dataframe']

            # Extract blanks data
            type_col = None
            result_col = None
            dl_col = None
            for col in df.columns:
                col_lower = col.lower()
                if 'type' in col_lower or 'sample_type' in col_lower:
                    type_col = col
                if 'result' in col_lower or 'value' in col_lower or 'assay' in col_lower:
                    result_col = col
                if 'detection' in col_lower or 'dl' in col_lower or 'lod' in col_lower:
                    dl_col = col

            if not type_col or not result_col:
                raise ValueError("Could not find required columns (sample_type, result)")

            # Filter for blanks
            blanks_df = df[df[type_col].str.upper().str.contains('BLANK|BLK', na=False, regex=True)].copy()

            if blanks_df.empty:
                raise ValueError("No blanks data found in dataset")

            # Convert result to numeric
            blanks_df[result_col] = pd.to_numeric(blanks_df[result_col], errors='coerce')
            blanks_data = blanks_df[result_col].dropna().tolist()

            if not blanks_data:
                raise ValueError("No valid numeric blanks data found")

            # Get detection limit
            if dl_col and dl_col in blanks_df.columns:
                dl_values = pd.to_numeric(blanks_df[dl_col], errors='coerce').dropna()
                dl = dl_values.median() if not dl_values.empty else np.percentile(blanks_data, 50)
            else:
                dl = np.percentile(blanks_data, 50)  # Use median as estimate

            contamination_threshold = 3 * dl
            analysis_result = None
            if hasattr(self, 'analysis_results') and self.analysis_results:
                analysis_result = self.analysis_results.get('blanks')
                if isinstance(analysis_result, dict):
                    contamination_info = analysis_result.get('contamination', {})
                    mdl_value = analysis_result.get('mdl') or analysis_result.get('summary', {}).get('mdl')
                    if mdl_value:
                        dl = mdl_value
                    contamination_threshold = contamination_info.get('threshold', contamination_threshold)

            ax = canvas.fig.add_subplot(111)

            # Create histogram
            bins = min(15, max(5, len(blanks_data) // 2))
            n, bins_edges, patches = ax.hist(blanks_data, bins=bins, alpha=0.7,
                                     color=canvas.colors['secondary'], edgecolor='black')

            # Add detection limit line
            ax.axvline(x=dl, color=canvas.colors['warning'],
                      linestyle='--', linewidth=2, label=f'Detection Limit: {dl:.3f}')

            # Add contamination threshold
            ax.axvline(x=contamination_threshold, color=canvas.colors['error'],
                      linestyle=':', linewidth=2, label=f'Contamination Threshold: {contamination_threshold:.3f}')

            # Highlight contaminated samples
            contaminated = [x for x in blanks_data if x > contamination_threshold]
            if isinstance(analysis_result, dict):
                contaminated_from_results = analysis_result.get('contamination', {}).get('contaminated_samples')
                if contaminated_from_results:
                    contaminated = contaminated_from_results
            if contaminated:
                ax.scatter(contaminated, [0.1] * len(contaminated),
                          color=canvas.colors['error'], s=100, zorder=5,
                          label=f'Contaminated (n={len(contaminated)})')

            ax.set_xlabel('Concentration (g/t)')
            ax.set_ylabel('Frequency')
            title = f'Blanks Distribution (n={len(blanks_data)})'
            if isinstance(analysis_result, dict):
                status = "PASS" if analysis_result.get('overall_acceptable', False) else "FAIL"
                title += f' • {status}'
            ax.set_title(title)
            ax.legend()
            ax.grid(True, alpha=0.3)

            # Safely draw the canvas
            try:
                canvas.draw_idle()  # Use draw_idle for better thread safety
            except Exception:
                try:
                    canvas.draw()
                except Exception:
                    pass

        except Exception as e:
            print(f"Error creating blanks plot: {e}")
            import traceback
            traceback.print_exc()
            # Create a simple error plot
            canvas = self.blanks_canvas
            canvas.fig.clear()
            ax = canvas.fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error creating plot:\n{str(e)}",
                   ha='center', va='center', transform=ax.transAxes, fontsize=10)
            ax.set_title('Blanks Distribution - Error')
            # Safely draw the canvas
            try:
                canvas.draw_idle()  # Use draw_idle for better thread safety
            except Exception:
                try:
                    canvas.draw()
                except Exception:
                    pass

    def create_duplicates_plot(self):
        """Create duplicates scatter plot from real data."""
        try:
            canvas = self.duplicates_canvas
            canvas.fig.clear()

            # Get data from plot_data
            if not self.plot_data or 'dataframe' not in self.plot_data:
                raise ValueError("No data available for plotting")

            df = self.plot_data['dataframe']

            # Extract duplicates data
            type_col = None
            result_col = None
            sample_id_col = None
            for col in df.columns:
                col_lower = col.lower()
                if 'type' in col_lower or 'sample_type' in col_lower:
                    type_col = col
                if 'result' in col_lower or 'value' in col_lower or 'assay' in col_lower:
                    result_col = col
                if 'id' in col_lower or 'sample_id' in col_lower:
                    sample_id_col = col

            if not type_col or not result_col:
                raise ValueError("Could not find required columns (sample_type, result)")

            # Filter for duplicates
            duplicates_df = df[df[type_col].str.upper().str.contains('DUPLICATE|DUP|CHECK|CK', na=False, regex=True)].copy()

            if duplicates_df.empty:
                raise ValueError("No duplicates data found in dataset")

            # Convert result to numeric
            duplicates_df[result_col] = pd.to_numeric(duplicates_df[result_col], errors='coerce')
            duplicates_df = duplicates_df.dropna(subset=[result_col])

            if duplicates_df.empty:
                raise ValueError("No valid numeric duplicates data found")

            # For now, use all duplicates as pairs (in real scenario, would pair by ID)
            # Take first half as x, second half as y
            n = len(duplicates_df)
            if n < 2:
                raise ValueError("Need at least 2 duplicate samples for scatter plot")

            # Simple pairing: split in half
            mid = n // 2
            x_data = duplicates_df[result_col].iloc[:mid].tolist()
            y_data = duplicates_df[result_col].iloc[mid:mid+len(x_data)].tolist()

            if len(x_data) != len(y_data):
                # Adjust to same length
                min_len = min(len(x_data), len(y_data))
                x_data = x_data[:min_len]
                y_data = y_data[:min_len]

            if not x_data or not y_data:
                raise ValueError("Could not create duplicate pairs")

            ax = canvas.fig.add_subplot(111)

            # Plot duplicate pairs
            ax.scatter(x_data, y_data, color=canvas.colors['accent'],
                      s=100, alpha=0.7, edgecolors='black', label=f'Duplicates (n={len(x_data)})')

            # Add 1:1 line
            min_val = min(min(x_data), min(y_data))
            max_val = max(max(x_data), max(y_data))
            ax.plot([min_val, max_val], [min_val, max_val],
                   color=canvas.colors['success'], linestyle='-', linewidth=2,
                   label='1:1 Line')

            # Calculate and display R²
            if len(x_data) > 1:
                correlation = np.corrcoef(x_data, y_data)[0, 1]
                r_squared = correlation ** 2
                ax.text(0.05, 0.95, f'R² = {r_squared:.3f}', transform=ax.transAxes,
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

            # Determine RPD threshold from analysis results or fallback to 20%
            rpd_threshold = 0.20
            analysis_result = None
            if hasattr(self, 'analysis_results') and self.analysis_results:
                analysis_result = self.analysis_results.get('duplicates')
                if isinstance(analysis_result, dict):
                    precision_info = analysis_result.get('precision', {})
                    threshold_value = precision_info.get('threshold')
                    if threshold_value is not None:
                        rpd_threshold = (threshold_value / 100.0) if threshold_value > 1 else threshold_value

            ax.plot([min_val, max_val], [min_val * (1 + rpd_threshold), max_val * (1 + rpd_threshold)],
                   color=canvas.colors['warning'], linestyle='--', linewidth=1,
                   label=f'±{rpd_threshold*100:.0f}% RPD')
            ax.plot([min_val, max_val], [min_val * (1 - rpd_threshold), max_val * (1 - rpd_threshold)],
                   color=canvas.colors['warning'], linestyle='--', linewidth=1)

            ax.set_xlabel('First Analysis (g/t)')
            ax.set_ylabel('Duplicate Analysis (g/t)')
            title = f'Duplicates Scatter Plot (n={len(x_data)} pairs)'
            if isinstance(analysis_result, dict):
                status = "PASS" if analysis_result.get('overall_acceptable', False) else "FAIL"
                title += f' • {status}'
            ax.set_title(title)
            ax.legend()
            ax.grid(True, alpha=0.3)

            # Safely draw the canvas
            try:
                canvas.draw_idle()  # Use draw_idle for better thread safety
            except Exception:
                try:
                    canvas.draw()
                except Exception:
                    pass

        except Exception as e:
            print(f"Error creating duplicates plot: {e}")
            import traceback
            traceback.print_exc()
            # Create a simple error plot
            canvas = self.duplicates_canvas
            canvas.fig.clear()
            ax = canvas.fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error creating plot:\n{str(e)}",
                   ha='center', va='center', transform=ax.transAxes, fontsize=10)
            ax.set_title('Duplicates Scatter Plot - Error')
            # Safely draw the canvas
            try:
                canvas.draw_idle()  # Use draw_idle for better thread safety
            except Exception:
                try:
                    canvas.draw()
                except Exception:
                    pass

    def create_results_plot(self):
        """Create results distribution histogram from real data."""
        try:
            canvas = self.results_canvas
            canvas.fig.clear()

            # Get data from plot_data
            if not self.plot_data or 'dataframe' not in self.plot_data:
                raise ValueError("No data available for plotting")

            df = self.plot_data['dataframe']

            # Find result column
            result_col = None
            for col in df.columns:
                col_lower = col.lower()
                if 'result' in col_lower or 'value' in col_lower or 'assay' in col_lower:
                    result_col = col
                    break

            if not result_col:
                raise ValueError("Could not find result column")

            # Convert result to numeric
            df[result_col] = pd.to_numeric(df[result_col], errors='coerce')
            results_data = df[result_col].dropna().tolist()

            if not results_data:
                raise ValueError("No valid numeric results data found")

            ax = canvas.fig.add_subplot(111)

            # Create histogram
            bins = min(30, max(10, len(results_data) // 5))
            n, bins_edges, patches = ax.hist(results_data, bins=bins, alpha=0.7,
                                 color=canvas.colors['info'], edgecolor='black')

            # Add statistics
            mean_val = np.mean(results_data)
            median_val = np.median(results_data)
            std_val = np.std(results_data)

            ax.axvline(x=mean_val, color=canvas.colors['success'],
                      linestyle='-', linewidth=2, label=f'Mean: {mean_val:.3f}')
            ax.axvline(x=median_val, color=canvas.colors['warning'],
                      linestyle='--', linewidth=2, label=f'Median: {median_val:.3f}')
            ax.axvline(x=mean_val + std_val, color=canvas.colors['accent'],
                      linestyle=':', linewidth=1, label=f'±1σ: {std_val:.3f}')
            ax.axvline(x=mean_val - std_val, color=canvas.colors['accent'],
                      linestyle=':', linewidth=1)

            ax.set_xlabel('Concentration (g/t)')
            ax.set_ylabel('Frequency')
            ax.set_title(f'Results Distribution (n={len(results_data)})')
            ax.legend()
            ax.grid(True, alpha=0.3)

            # Safely draw the canvas
            try:
                canvas.draw_idle()  # Use draw_idle for better thread safety
            except Exception:
                try:
                    canvas.draw()
                except Exception:
                    pass

        except Exception as e:
            print(f"Error creating results plot: {e}")
            import traceback
            traceback.print_exc()
            # Create a simple error plot
            canvas = self.results_canvas
            canvas.fig.clear()
            ax = canvas.fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error creating plot:\n{str(e)}",
                   ha='center', va='center', transform=ax.transAxes, fontsize=10)
            ax.set_title('Results Distribution - Error')
            # Safely draw the canvas
            try:
                canvas.draw_idle()  # Use draw_idle for better thread safety
            except Exception:
                try:
                    canvas.draw()
                except Exception:
                    pass

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
        if data and isinstance(data, dict):
            # Check for dataframe key first, then fall back to 'data' key
            # Can't use 'or' with DataFrames - need explicit None check
            df = data.get('dataframe')
            if df is None:
                df = data.get('data')

            if df is not None and hasattr(df, 'empty') and not df.empty:
                self.plot_data = data
                print(f"Plot data set: {list(data.keys()) if data else 'None'}, shape: {df.shape}")
            else:
                self.plot_data = None
                print("No valid dataframe in data - plot data cleared")
        else:
            self.plot_data = None
            print("No valid data provided - plot data cleared")

    def set_analysis_results(self, results: Dict[str, Any]):
        """Store analysis results for use in visualization summaries."""
        self.analysis_results = results
        if results:
            summary = self._build_plot_summary(self.plot_type_combo.currentText())
            if summary:
                self.plot_info_label.setText(summary)
                self.plot_info_label.setStyleSheet("""
                    QLabel {
                        color: #1A1A1A;
                        font-weight: bold;
                        padding: 8px;
                        background-color: #E7F5EE;
                        border: 1px solid #B6E0C2;
                        border-radius: 4px;
                    }
                """)

    def reset(self):
        """Reset the visualization panel to initial state."""
        self.current_plots = {}
        self.plot_data = None
        self.analysis_results = None

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

    def _build_plot_summary(self, plot_type: str) -> Optional[str]:
        """Build a summary message for the plot based on analysis results."""
        if not self.analysis_results or not isinstance(self.analysis_results, dict):
            return None

        summary_lines: List[str] = []

        mapping = {
            "Standards Control Chart": "standards",
            "Blanks Histogram": "blanks",
            "Duplicates Scatter Plot": "duplicates",
            "Results Distribution": None,
            "All Plots": None,
        }

        key = mapping.get(plot_type)
        if key and key in self.analysis_results:
            result = self.analysis_results[key]
            if isinstance(result, dict):
                if 'error' in result:
                    summary_lines.append(f"{plot_type}: ERROR - {result['error']}")
                else:
                    status = "PASS" if result.get('overall_acceptable', False) else "FAIL"
                    summary_lines.append(f"{plot_type}: {status}")

                    if key == 'standards':
                        bias = result.get('bias', {})
                        recovery = result.get('recovery', {})
                        precision = result.get('precision', {})
                        summary_lines.append(
                            f"Max Z: {bias.get('max_z_score', 0):.2f} | Mean Recovery: {recovery.get('mean_recovery', 0):.1f}% | RSD: {precision.get('rsd', 0):.1f}%"
                        )
                    elif key == 'blanks':
                        contamination = result.get('contamination', {})
                        summary_lines.append(
                            f"Contaminated: {len(contamination.get('contaminated_samples', []))} | Rate: {contamination.get('contamination_rate', 0)*100:.1f}%"
                        )
                    elif key == 'duplicates':
                        precision = result.get('precision', {})
                        summary_lines.append(
                            f"Mean RPD: {precision.get('mean_rpd', 0):.1f}% | Max RPD: {precision.get('max_rpd', 0):.1f}%"
                        )

        if 'total_samples' in self.analysis_results and plot_type == 'Results Distribution':
            summary_lines.append(
                f"Total Samples: {self.analysis_results.get('total_samples', 0)}"
            )

        if plot_type == 'All Plots':
            statuses: List[str] = []
            for key in ('standards', 'blanks', 'duplicates'):
                result = self.analysis_results.get(key)
                if isinstance(result, dict):
                    if 'error' in result:
                        statuses.append(f"{key.title()}: ERROR")
                    else:
                        status = "PASS" if result.get('overall_acceptable', False) else "FAIL"
                        statuses.append(f"{key.title()}: {status}")
            if statuses:
                summary_lines.extend(statuses)

        return "\n".join(summary_lines) if summary_lines else None
