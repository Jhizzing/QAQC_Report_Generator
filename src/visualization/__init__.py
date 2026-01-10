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

    def create_rpd_scatter(self, original: list, duplicate: list, 
                            rpd_limit: float = 20.0, absolute_precision: float = 0.01,
                            title: str = "RPD vs Grade") -> dict:
        """
        Create an RPD scatter plot with hyperbolic precision envelope.
        
        Industry-standard plot for duplicate precision assessment. Shows that
        acceptable RPD varies with grade - lower grades naturally have higher
        RPD tolerance due to the relationship between absolute and relative error.
        
        The hyperbolic envelope is calculated as:
        RPD_limit = 100 * sqrt(2) * (absolute_precision / grade)
        
        Where absolute_precision is the detection limit or analytical precision.

        Args:
            original: List of original measurement values
            duplicate: List of duplicate measurement values
            rpd_limit: Fixed RPD limit (%) for higher grades (default 20%)
            absolute_precision: Absolute precision/detection limit (default 0.01)
            title: Chart title

        Returns:
            Dictionary with plot data and metadata including pass/fail counts
        """
        import matplotlib.pyplot as plt
        import numpy as np

        if len(original) != len(duplicate):
            raise ValueError("Original and duplicate lists must have same length")

        original = np.array(original)
        duplicate = np.array(duplicate)

        # Calculate grade (mean of pair) and RPD
        grades = (original + duplicate) / 2
        
        # Avoid division by zero
        rpd_values = np.zeros_like(grades)
        nonzero_mask = grades > 0
        rpd_values[nonzero_mask] = (
            np.abs(original[nonzero_mask] - duplicate[nonzero_mask]) / 
            grades[nonzero_mask] * 100
        )

        # Calculate hyperbolic envelope
        # At low grades, RPD tolerance is higher due to detection limit effects
        grade_range = np.linspace(max(0.001, grades.min() * 0.5), grades.max() * 1.2, 200)
        
        # Hyperbolic component: RPD = sqrt(2) * 100 * (precision / grade)
        hyperbolic_limit = 100 * np.sqrt(2) * (absolute_precision / grade_range)
        
        # Combined limit: max of hyperbolic (low grade) and fixed limit (high grade)
        combined_limit = np.maximum(hyperbolic_limit, rpd_limit)

        # Determine pass/fail for each point
        point_limits = np.maximum(
            100 * np.sqrt(2) * (absolute_precision / np.maximum(grades, 0.001)),
            rpd_limit
        )
        passed = rpd_values <= point_limits
        failed = ~passed

        # Set up the plot
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Plot passing points
        if np.any(passed):
            ax.scatter(grades[passed], rpd_values[passed], 
                      alpha=0.7, s=50, color='#27AE60', edgecolors='white', 
                      linewidth=0.5, label=f'Pass ({np.sum(passed)})')

        # Plot failing points
        if np.any(failed):
            ax.scatter(grades[failed], rpd_values[failed], 
                      alpha=0.7, s=50, color='#E74C3C', edgecolors='white', 
                      linewidth=0.5, label=f'Fail ({np.sum(failed)})')

        # Plot hyperbolic envelope
        ax.plot(grade_range, combined_limit, 'k-', linewidth=2, 
                label=f'Precision Envelope')
        
        # Add fixed RPD limit line
        ax.axhline(y=rpd_limit, color='gray', linestyle=':', linewidth=1.5, 
                   label=f'Fixed Limit ({rpd_limit}%)')

        # Fill under the envelope
        ax.fill_between(grade_range, 0, combined_limit, alpha=0.1, color='green')

        # Formatting
        ax.set_xlabel('Grade (Mean of Pair)')
        ax.set_ylabel('Relative Percent Difference (%)')
        ax.set_title(title)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(bottom=0)

        # Set x-axis to log scale if range is large
        if grades.max() / max(grades.min(), 0.001) > 100:
            ax.set_xscale('log')

        # Add statistics text box
        pass_rate = np.sum(passed) / len(passed) * 100 if len(passed) > 0 else 0
        mean_rpd = np.mean(rpd_values)
        stats_text = (f'n = {len(original)}\n'
                      f'Pass Rate = {pass_rate:.1f}%\n'
                      f'Mean RPD = {mean_rpd:.1f}%')
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8), fontsize=9)

        return {
            'figure': fig,
            'axes': ax,
            'grades': grades.tolist(),
            'rpd_values': rpd_values.tolist(),
            'passed': passed.tolist(),
            'failed': failed.tolist(),
            'pass_rate': pass_rate,
            'mean_rpd': mean_rpd,
            'rpd_limit': rpd_limit,
            'absolute_precision': absolute_precision,
            'n': len(original)
        }

    def create_cusum_chart(self, values: list, target: float, 
                            title: str = "CUSUM Chart") -> dict:
        """
        Create a CUSUM (Cumulative Sum) chart for detecting drift in standards.
        
        Plots the cumulative sum of deviations from the target value.
        - Horizontal trend = process is stable
        - Upward slope = values consistently above target (positive drift)
        - Downward slope = values consistently below target (negative drift)
        - Sudden step change = abrupt shift in process

        Args:
            values: List of measured values (e.g., CRM results)
            target: Target/certified value
            title: Chart title

        Returns:
            Dictionary with plot data and metadata including drift detection
        """
        import matplotlib.pyplot as plt
        import numpy as np

        values = np.array(values)
        n = len(values)

        # Calculate deviations and cumulative sum
        deviations = values - target
        cusum = np.cumsum(deviations)

        # Calculate control limits (V-mask parameters)
        std_dev = np.std(deviations, ddof=1) if n > 1 else 0
        
        # Decision interval (h) and reference value (k) for V-mask
        # Using typical values: h = 4*sigma, k = 0.5*sigma
        h = 4 * std_dev
        k = 0.5 * std_dev
        
        # Upper and lower CUSUM (for two-sided detection)
        cusum_upper = np.zeros(n)
        cusum_lower = np.zeros(n)
        
        for i in range(n):
            if i == 0:
                cusum_upper[i] = max(0, deviations[i] - k)
                cusum_lower[i] = max(0, -deviations[i] - k)
            else:
                cusum_upper[i] = max(0, cusum_upper[i-1] + deviations[i] - k)
                cusum_lower[i] = max(0, cusum_lower[i-1] - deviations[i] - k)

        # Detect out-of-control points
        upper_violations = np.where(cusum_upper > h)[0]
        lower_violations = np.where(cusum_lower > h)[0]

        # Set up the plot with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figure_size[0], self.figure_size[1] * 1.2), 
                                        dpi=self.dpi, sharex=True)

        # Top plot: Raw CUSUM
        x_values = list(range(1, n + 1))
        ax1.plot(x_values, cusum, 'b-', linewidth=2, marker='o', markersize=4, label='Cumulative Sum')
        ax1.axhline(y=0, color='green', linestyle='-', linewidth=2, label='Target (0)')
        ax1.fill_between(x_values, cusum, 0, alpha=0.2, color='blue')
        
        ax1.set_ylabel('Cumulative Sum of Deviations')
        ax1.set_title(title)
        ax1.legend(loc='upper left', fontsize=9)
        ax1.grid(True, alpha=0.3)

        # Add trend indicator
        if n > 1:
            slope = np.polyfit(range(n), cusum, 1)[0]
            if abs(slope) < 0.1 * std_dev:
                trend = "Stable"
                trend_color = 'green'
            elif slope > 0:
                trend = "Positive Drift"
                trend_color = 'orange'
            else:
                trend = "Negative Drift"
                trend_color = 'orange'
            ax1.text(0.98, 0.98, f'Trend: {trend}', transform=ax1.transAxes, 
                     verticalalignment='top', horizontalalignment='right',
                     bbox=dict(boxstyle='round', facecolor=trend_color, alpha=0.3), fontsize=10)

        # Bottom plot: Two-sided CUSUM with decision limits
        ax2.plot(x_values, cusum_upper, 'r-', linewidth=2, marker='^', markersize=4, label='Upper CUSUM')
        ax2.plot(x_values, -cusum_lower, 'b-', linewidth=2, marker='v', markersize=4, label='Lower CUSUM')
        ax2.axhline(y=h, color='red', linestyle='--', linewidth=2, label=f'UCL (+{h:.3f})')
        ax2.axhline(y=-h, color='blue', linestyle='--', linewidth=2, label=f'LCL (-{h:.3f})')
        ax2.axhline(y=0, color='gray', linestyle=':', linewidth=1)

        # Highlight violations
        if len(upper_violations) > 0:
            ax2.scatter([v+1 for v in upper_violations], [cusum_upper[v] for v in upper_violations],
                       color='red', s=100, zorder=5, marker='X', label='Upper Violation')
        if len(lower_violations) > 0:
            ax2.scatter([v+1 for v in lower_violations], [-cusum_lower[v] for v in lower_violations],
                       color='blue', s=100, zorder=5, marker='X', label='Lower Violation')

        ax2.set_xlabel('Sample Number')
        ax2.set_ylabel('Two-Sided CUSUM')
        ax2.legend(loc='upper left', fontsize=8, ncol=2)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        return {
            'figure': fig,
            'axes': (ax1, ax2),
            'values': values.tolist(),
            'target': target,
            'cusum': cusum.tolist(),
            'cusum_upper': cusum_upper.tolist(),
            'cusum_lower': cusum_lower.tolist(),
            'decision_interval': h,
            'upper_violations': upper_violations.tolist(),
            'lower_violations': lower_violations.tolist(),
            'n': n
        }

    def create_bland_altman(self, original: list, duplicate: list, 
                             title: str = "Bland-Altman Plot") -> dict:
        """
        Create a Bland-Altman plot for duplicate bias analysis.
        
        Shows agreement between original and duplicate measurements by plotting
        the mean of each pair against their difference. Reveals systematic bias
        that simple scatter plots may miss.

        Args:
            original: List of original measurement values
            duplicate: List of duplicate measurement values
            title: Chart title

        Returns:
            Dictionary with plot data and metadata including bias and limits
        """
        import matplotlib.pyplot as plt
        import numpy as np

        if len(original) != len(duplicate):
            raise ValueError("Original and duplicate lists must have same length")

        original = np.array(original)
        duplicate = np.array(duplicate)

        # Calculate mean and difference for each pair
        means = (original + duplicate) / 2
        differences = original - duplicate

        # Calculate statistics
        mean_diff = np.mean(differences)  # Bias
        std_diff = np.std(differences, ddof=1)
        
        # Limits of agreement (95% confidence)
        loa_upper = mean_diff + 1.96 * std_diff
        loa_lower = mean_diff - 1.96 * std_diff

        # Set up the plot
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        # Scatter plot of means vs differences
        ax.scatter(means, differences, alpha=0.7, s=50, color='#2E86AB', edgecolors='white', linewidth=0.5)

        # Mean difference line (bias)
        ax.axhline(y=mean_diff, color='#E94F37', linestyle='-', linewidth=2, 
                   label=f'Mean Difference (Bias): {mean_diff:.4f}')

        # Limits of agreement
        ax.axhline(y=loa_upper, color='#F39C12', linestyle='--', linewidth=2,
                   label=f'+1.96 SD: {loa_upper:.4f}')
        ax.axhline(y=loa_lower, color='#F39C12', linestyle='--', linewidth=2,
                   label=f'-1.96 SD: {loa_lower:.4f}')

        # Zero line for reference
        ax.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)

        # Fill between limits of agreement
        ax.fill_between(ax.get_xlim(), loa_lower, loa_upper, alpha=0.1, color='#F39C12')

        # Formatting
        ax.set_xlabel('Mean of Original and Duplicate')
        ax.set_ylabel('Difference (Original - Duplicate)')
        ax.set_title(title)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)

        # Add statistics text box
        stats_text = (f'n = {len(original)}\n'
                      f'Bias = {mean_diff:.4f}\n'
                      f'SD = {std_diff:.4f}')
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8), fontsize=9)

        return {
            'figure': fig,
            'axes': ax,
            'means': means.tolist(),
            'differences': differences.tolist(),
            'bias': mean_diff,
            'std': std_diff,
            'loa_upper': loa_upper,
            'loa_lower': loa_lower,
            'n': len(original)
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
