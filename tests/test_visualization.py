"""
Tests for visualization modules.
"""
import pytest
import tempfile
import os
from src.visualization import PlotGenerator


class TestPlotGenerator:
    """Test PlotGenerator functionality."""

    def test_init_default_config(self):
        """Test initialization with default config."""
        generator = PlotGenerator()
        assert generator.figure_size == (10, 6)
        assert generator.dpi == 100
        assert generator.style == 'seaborn-v0_8'

    def test_init_custom_config(self):
        """Test initialization with custom config."""
        config = {
            'figure_size': (12, 8),
            'dpi': 150,
            'style': 'ggplot'
        }
        generator = PlotGenerator(config)
        assert generator.figure_size == (12, 8)
        assert generator.dpi == 150
        assert generator.style == 'ggplot'

    def test_create_control_chart(self):
        """Test control chart creation."""
        generator = PlotGenerator()
        data = [10.0, 10.2, 9.8, 10.1, 9.9, 10.3, 9.7, 10.0]
        limits = {
            'center': 10.0,
            'ucl': 10.5,
            'lcl': 9.5
        }

        result = generator.create_control_chart(data, limits, "Test Control Chart")

        assert 'figure' in result
        assert 'axes' in result
        assert 'data' in result
        assert 'limits' in result
        assert result['data'] == data
        assert result['limits'] == limits

    def test_create_scatter_plot(self):
        """Test scatter plot creation."""
        generator = PlotGenerator()
        x_data = [10.0, 12.0, 15.0, 18.0, 20.0]
        y_data = [10.5, 12.2, 14.8, 17.9, 20.1]

        result = generator.create_scatter_plot(x_data, y_data, "Test Scatter Plot")

        assert 'figure' in result
        assert 'axes' in result
        assert 'x_data' in result
        assert 'y_data' in result
        assert 'r_squared' in result
        assert result['x_data'] == x_data
        assert result['y_data'] == y_data
        assert 0 <= result['r_squared'] <= 1

    def test_create_histogram(self):
        """Test histogram creation."""
        generator = PlotGenerator()
        data = [10.0, 10.2, 9.8, 10.1, 9.9, 10.3, 9.7, 10.0, 10.1, 9.8]

        result = generator.create_histogram(data, bins=5, title="Test Histogram")

        assert 'figure' in result
        assert 'axes' in result
        assert 'data' in result
        assert 'mean' in result
        assert 'std' in result
        assert 'bins' in result
        assert result['data'] == data
        assert result['mean'] > 0
        assert result['std'] > 0

    def test_create_time_series(self):
        """Test time series creation."""
        generator = PlotGenerator()
        data = [10.0, 10.2, 9.8, 10.1, 9.9]

        result = generator.create_time_series(data, title="Test Time Series")

        assert 'figure' in result
        assert 'axes' in result
        assert 'data' in result
        assert 'timestamps' in result
        assert result['data'] == data
        assert len(result['timestamps']) == len(data)

    def test_save_plot(self):
        """Test plot saving."""
        generator = PlotGenerator()
        data = [10.0, 10.2, 9.8, 10.1, 9.9]

        # Create a plot
        plot_data = generator.create_histogram(data, title="Test Histogram")

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            filename = tmp.name

        try:
            result = generator.save_plot(plot_data, filename, 'png')
            assert result == filename
            assert os.path.exists(filename)
        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)
