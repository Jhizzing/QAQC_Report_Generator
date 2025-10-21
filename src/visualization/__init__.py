"""
Visualization utilities for QAQC application.
"""

class PlotGenerator:
    """
    Generates plots for QAQC analysis.

    Key plot types:
    - Control charts (Shewhart, CUSUM)
    - Scatter plots for duplicates
    - Histograms for distributions
    - Time series plots
    """

    def __init__(self, config: dict = None) -> None:
        """
        Initialize with plotting configuration.

        Args:
            config: Dictionary with plot settings
        """
        self.config = config or {}
        self.figure_size = self.config.get('figure_size', (10, 6))
        self.dpi = self.config.get('dpi', 100)
        self.style = self.config.get('style', 'seaborn-v0_8')

    def create_control_chart(self, data: list, limits: dict = None, title: str = "Control Chart") -> dict:
        """
        Create a Shewhart control chart.

        Args:
            data: List of measured values
            limits: Dictionary with 'ucl', 'lcl', 'center' keys
            title: Chart title

        Returns:
            Dictionary with plot data and metadata
        """
        import matplotlib.pyplot as plt
        import numpy as np

        # Set up the plot
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Plot data points
        x_values = list(range(1, len(data) + 1))
        ax.plot(x_values, data, 'bo-', markersize=6, linewidth=2, label='Measurements')

        # Add control limits if provided
        if limits:
            center = limits.get('center', np.mean(data))
            ucl = limits.get('ucl', center + 3 * np.std(data))
            lcl = limits.get('lcl', center - 3 * np.std(data))

            ax.axhline(y=center, color='g', linestyle='-', linewidth=2, label='Center Line')
            ax.axhline(y=ucl, color='r', linestyle='--', linewidth=2, label='Upper Control Limit')
            ax.axhline(y=lcl, color='r', linestyle='--', linewidth=2, label='Lower Control Limit')

            # Highlight out-of-control points
            out_of_control = [i for i, val in enumerate(data) if val > ucl or val < lcl]
            if out_of_control:
                ax.scatter([i+1 for i in out_of_control], [data[i] for i in out_of_control],
                          color='red', s=100, zorder=5, label='Out of Control')

        # Formatting
        ax.set_xlabel('Sample Number')
        ax.set_ylabel('Value')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)

        return {
            'figure': fig,
            'axes': ax,
            'data': data,
            'limits': limits
        }

    def create_scatter_plot(self, x_data: list, y_data: list, title: str = "Scatter Plot") -> dict:
        """
        Create a scatter plot for duplicate analysis.

        Args:
            x_data: X-axis data
            y_data: Y-axis data
            title: Chart title

        Returns:
            Dictionary with plot data and metadata
        """
        import matplotlib.pyplot as plt
        import numpy as np

        # Set up the plot
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Create scatter plot
        ax.scatter(x_data, y_data, alpha=0.7, s=50, color='blue')

        # Add 1:1 line
        min_val = min(min(x_data), min(y_data))
        max_val = max(max(x_data), max(y_data))
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='1:1 Line')

        # Calculate and display R²
        correlation = np.corrcoef(x_data, y_data)[0, 1]
        r_squared = correlation ** 2

        ax.text(0.05, 0.95, f'R² = {r_squared:.3f}', transform=ax.transAxes,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # Formatting
        ax.set_xlabel('First Measurement')
        ax.set_ylabel('Second Measurement')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)

        return {
            'figure': fig,
            'axes': ax,
            'x_data': x_data,
            'y_data': y_data,
            'r_squared': r_squared
        }

    def create_histogram(self, data: list, bins: int = 20, title: str = "Histogram") -> dict:
        """
        Create a histogram for distribution analysis.

        Args:
            data: List of values
            bins: Number of bins
            title: Chart title

        Returns:
            Dictionary with plot data and metadata
        """
        import matplotlib.pyplot as plt
        import numpy as np

        # Set up the plot
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Create histogram
        n, bins_edges, patches = ax.hist(data, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')

        # Add statistics
        mean_val = np.mean(data)
        std_val = np.std(data)

        ax.axvline(mean_val, color='red', linestyle='-', linewidth=2, label=f'Mean: {mean_val:.2f}')
        ax.axvline(mean_val + std_val, color='orange', linestyle='--', linewidth=2, label=f'+1σ: {mean_val + std_val:.2f}')
        ax.axvline(mean_val - std_val, color='orange', linestyle='--', linewidth=2, label=f'-1σ: {mean_val - std_val:.2f}')

        # Formatting
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)

        return {
            'figure': fig,
            'axes': ax,
            'data': data,
            'mean': mean_val,
            'std': std_val,
            'bins': bins_edges
        }

    def create_time_series(self, data: list, timestamps: list = None, title: str = "Time Series") -> dict:
        """
        Create a time series plot.

        Args:
            data: List of values
            timestamps: List of timestamps (optional)
            title: Chart title

        Returns:
            Dictionary with plot data and metadata
        """
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime, timedelta

        # Set up the plot
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Generate timestamps if not provided
        if timestamps is None:
            timestamps = [datetime.now() + timedelta(hours=i) for i in range(len(data))]

        # Create time series plot
        ax.plot(timestamps, data, 'bo-', markersize=6, linewidth=2)

        # Format x-axis for dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        # Formatting
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)

        return {
            'figure': fig,
            'axes': ax,
            'data': data,
            'timestamps': timestamps
        }

    def save_plot(self, plot_data: dict, filename: str, format: str = 'png') -> str:
        """
        Save a plot to file.

        Args:
            plot_data: Dictionary from plot creation methods
            filename: Output filename
            format: File format ('png', 'pdf', 'svg')

        Returns:
            Full path to saved file
        """
        import os

        # Ensure output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Save the plot
        plot_data['figure'].savefig(filename, format=format, dpi=self.dpi, bbox_inches='tight')

        return filename

class ReportVisualizer:
    """Stub report visualizer class."""
    def __init__(self) -> None:
        pass
