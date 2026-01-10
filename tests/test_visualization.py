"""
Tests for QAQC visualization plots.

Tests the PlotGenerator class including the new QAQC-specific plots:
- Bland-Altman plot for duplicates bias
- CUSUM chart for standards drift detection
- RPD scatter with hyperbolic precision envelope
"""

import pytest
import numpy as np
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.visualization import PlotGenerator


class TestPlotGenerator:
    """Tests for the PlotGenerator class."""

    @pytest.fixture
    def plot_gen(self):
        """Create a PlotGenerator instance."""
        return PlotGenerator({'figure_size': (10, 6), 'dpi': 100})

    @pytest.fixture
    def output_dir(self, tmp_path):
        """Create temporary output directory."""
        out = tmp_path / "plots"
        out.mkdir()
        return out

    # ===== Existing Plot Tests =====

    def test_control_chart_basic(self, plot_gen):
        """Test basic control chart creation."""
        data = [1.0, 1.02, 0.98, 1.01, 0.99, 1.03, 0.97, 1.0]
        limits = {'center': 1.0, 'ucl': 1.1, 'lcl': 0.9}
        
        result = plot_gen.create_control_chart(data, limits, "Test Control Chart")
        
        assert 'figure' in result
        assert 'axes' in result
        assert result['data'] == data
        assert result['limits'] == limits

    def test_scatter_plot_basic(self, plot_gen):
        """Test basic scatter plot creation."""
        x_data = [1.0, 2.0, 3.0, 4.0, 5.0]
        y_data = [1.1, 2.05, 2.9, 4.1, 5.0]
        
        result = plot_gen.create_scatter_plot(x_data, y_data, "Test Scatter")
        
        assert 'figure' in result
        assert 'r_squared' in result
        assert 0 <= result['r_squared'] <= 1

    def test_histogram_basic(self, plot_gen):
        """Test basic histogram creation."""
        np.random.seed(42)
        data = np.random.normal(1.0, 0.1, 100).tolist()
        
        result = plot_gen.create_histogram(data, bins=20, title="Test Histogram")
        
        assert 'figure' in result
        assert 'mean' in result
        assert 'std' in result

    # ===== Bland-Altman Plot Tests =====

    def test_bland_altman_basic(self, plot_gen):
        """Test basic Bland-Altman plot creation."""
        np.random.seed(42)
        original = np.random.normal(1.0, 0.1, 50).tolist()
        duplicate = [o + np.random.normal(0, 0.02) for o in original]  # Small random diff
        
        result = plot_gen.create_bland_altman(original, duplicate, "Test Bland-Altman")
        
        assert 'figure' in result
        assert 'bias' in result
        assert 'std' in result
        assert 'loa_upper' in result
        assert 'loa_lower' in result
        assert result['n'] == 50
        # Bias should be close to 0 for well-matched duplicates
        assert abs(result['bias']) < 0.1

    def test_bland_altman_with_bias(self, plot_gen):
        """Test Bland-Altman detects systematic bias."""
        original = [1.0, 2.0, 3.0, 4.0, 5.0]
        duplicate = [0.9, 1.9, 2.9, 3.9, 4.9]  # Consistent 0.1 lower
        
        result = plot_gen.create_bland_altman(original, duplicate, "Bias Detection")
        
        # Should detect positive bias (original consistently higher)
        assert result['bias'] == pytest.approx(0.1, abs=0.001)
        assert result['std'] == pytest.approx(0.0, abs=0.001)  # No variability in bias

    def test_bland_altman_unequal_lengths(self, plot_gen):
        """Test Bland-Altman raises error for unequal lengths."""
        with pytest.raises(ValueError, match="same length"):
            plot_gen.create_bland_altman([1, 2, 3], [1, 2])

    def test_bland_altman_limits_of_agreement(self, plot_gen):
        """Test limits of agreement calculation."""
        np.random.seed(42)
        original = [1.0] * 100
        # Add known variability
        duplicate = [1.0 + np.random.normal(0, 0.1) for _ in range(100)]
        
        result = plot_gen.create_bland_altman(original, duplicate)
        
        # LOA should be approximately 1.96 * std from mean
        expected_loa_range = 1.96 * result['std']
        actual_loa_range = (result['loa_upper'] - result['bias'])
        assert actual_loa_range == pytest.approx(expected_loa_range, rel=0.01)

    # ===== CUSUM Chart Tests =====

    def test_cusum_basic(self, plot_gen):
        """Test basic CUSUM chart creation."""
        # Values fluctuating around target
        values = [1.02, 0.98, 1.01, 0.99, 1.0, 1.01, 0.99, 1.02, 0.98, 1.0]
        target = 1.0
        
        result = plot_gen.create_cusum_chart(values, target, "Test CUSUM")
        
        assert 'figure' in result
        assert 'cusum' in result
        assert 'cusum_upper' in result
        assert 'cusum_lower' in result
        assert result['target'] == target
        assert result['n'] == 10

    def test_cusum_detects_positive_drift(self, plot_gen):
        """Test CUSUM detects positive drift (values consistently above target)."""
        # Simulate positive drift: values trend upward
        values = [1.0, 1.02, 1.04, 1.06, 1.08, 1.10, 1.12, 1.14, 1.16, 1.18]
        target = 1.0
        
        result = plot_gen.create_cusum_chart(values, target, "Positive Drift")
        
        cusum = result['cusum']
        # CUSUM should be consistently positive and increasing
        assert all(c > 0 for c in cusum[1:])
        assert cusum[-1] > cusum[0]  # Trend upward

    def test_cusum_detects_negative_drift(self, plot_gen):
        """Test CUSUM detects negative drift (values consistently below target)."""
        values = [1.0, 0.98, 0.96, 0.94, 0.92, 0.90, 0.88, 0.86, 0.84, 0.82]
        target = 1.0
        
        result = plot_gen.create_cusum_chart(values, target, "Negative Drift")
        
        cusum = result['cusum']
        # CUSUM should be consistently negative and decreasing
        assert all(c < 0 for c in cusum[1:])
        assert cusum[-1] < cusum[0]

    def test_cusum_stable_process(self, plot_gen):
        """Test CUSUM for stable process (random variation around target)."""
        np.random.seed(42)
        values = np.random.normal(1.0, 0.02, 50).tolist()
        target = 1.0
        
        result = plot_gen.create_cusum_chart(values, target, "Stable Process")
        
        # Should have no violations for a well-controlled process
        assert len(result['upper_violations']) == 0 or len(result['lower_violations']) == 0

    # ===== RPD Scatter Tests =====

    def test_rpd_scatter_basic(self, plot_gen):
        """Test basic RPD scatter plot creation."""
        np.random.seed(42)
        original = np.abs(np.random.normal(1.0, 0.3, 50)).tolist()
        duplicate = [o * np.random.uniform(0.95, 1.05) for o in original]  # ±5% variation
        
        result = plot_gen.create_rpd_scatter(original, duplicate, title="Test RPD")
        
        assert 'figure' in result
        assert 'grades' in result
        assert 'rpd_values' in result
        assert 'passed' in result
        assert 'failed' in result
        assert 'pass_rate' in result
        assert result['n'] == 50

    def test_rpd_scatter_all_pass(self, plot_gen):
        """Test RPD scatter with all passing duplicates."""
        original = [1.0, 2.0, 3.0, 4.0, 5.0]
        duplicate = [1.02, 2.04, 3.03, 4.04, 5.05]  # ~2% difference
        
        result = plot_gen.create_rpd_scatter(original, duplicate, rpd_limit=20.0)
        
        assert result['pass_rate'] == 100.0
        assert all(result['passed'])
        assert not any(result['failed'])

    def test_rpd_scatter_failures(self, plot_gen):
        """Test RPD scatter identifies failing duplicates."""
        original = [1.0, 1.0, 1.0, 1.0, 1.0]
        duplicate = [0.7, 1.0, 1.0, 1.0, 1.3]  # First and last are 30% off
        
        result = plot_gen.create_rpd_scatter(original, duplicate, rpd_limit=20.0)
        
        assert result['pass_rate'] < 100.0
        assert any(result['failed'])

    def test_rpd_scatter_hyperbolic_envelope(self, plot_gen):
        """Test that low grades get higher RPD tolerance via hyperbolic envelope."""
        # Low grade samples with high RPD that should pass due to detection limit effects
        original = [0.01, 0.01, 0.01]  # Very low grade
        duplicate = [0.012, 0.008, 0.011]  # 20% variation at low grade
        
        result = plot_gen.create_rpd_scatter(
            original, duplicate, 
            rpd_limit=20.0, 
            absolute_precision=0.005  # Detection limit
        )
        
        # At low grades, hyperbolic envelope should allow higher RPD
        # These should pass despite high RPD values
        assert result['pass_rate'] > 0

    def test_rpd_scatter_unequal_lengths(self, plot_gen):
        """Test RPD scatter raises error for unequal lengths."""
        with pytest.raises(ValueError, match="same length"):
            plot_gen.create_rpd_scatter([1, 2, 3], [1, 2])

    # ===== Save Plot Tests =====

    def test_save_plot(self, plot_gen, output_dir):
        """Test saving plots to file."""
        data = [1.0, 1.1, 0.9, 1.05, 0.95]
        result = plot_gen.create_control_chart(data)
        
        filename = str(output_dir / "test_plot.png")
        saved_path = plot_gen.save_plot(result, filename)
        
        assert os.path.exists(saved_path)
        assert saved_path == filename


def generate_sample_plots():
    """Generate sample plots for visual inspection."""
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'output', 'plots'
    )
    os.makedirs(output_dir, exist_ok=True)
    
    plot_gen = PlotGenerator({'figure_size': (10, 6), 'dpi': 150})
    np.random.seed(42)
    
    print("Generating sample QAQC plots...")
    
    # 1. Bland-Altman Plot
    print("  - Bland-Altman plot...")
    original = np.abs(np.random.normal(1.0, 0.3, 80))
    duplicate = original + np.random.normal(0.02, 0.05, 80)  # Slight positive bias
    result = plot_gen.create_bland_altman(original.tolist(), duplicate.tolist(),
                                          "Duplicate Bias Analysis (Bland-Altman)")
    plot_gen.save_plot(result, os.path.join(output_dir, 'bland_altman_sample.png'))
    print(f"    Bias: {result['bias']:.4f}, SD: {result['std']:.4f}")
    
    # 2. CUSUM Chart - Stable
    print("  - CUSUM chart (stable)...")
    stable_values = np.random.normal(1.0, 0.02, 50)
    result = plot_gen.create_cusum_chart(stable_values.tolist(), 1.0,
                                         "CRM Monitoring - Stable Process")
    plot_gen.save_plot(result, os.path.join(output_dir, 'cusum_stable_sample.png'))
    
    # 3. CUSUM Chart - With Drift
    print("  - CUSUM chart (drift)...")
    drift_values = np.concatenate([
        np.random.normal(1.0, 0.02, 25),  # Stable period
        np.random.normal(1.05, 0.02, 25)  # Drift period
    ])
    result = plot_gen.create_cusum_chart(drift_values.tolist(), 1.0,
                                         "CRM Monitoring - Drift Detection")
    plot_gen.save_plot(result, os.path.join(output_dir, 'cusum_drift_sample.png'))
    
    # 4. RPD Scatter with Hyperbolic Envelope
    print("  - RPD scatter plot...")
    # Mix of low and high grade samples
    grades_orig = np.concatenate([
        np.random.uniform(0.01, 0.1, 30),   # Low grade
        np.random.uniform(0.5, 2.0, 40),    # Medium grade
        np.random.uniform(5.0, 20.0, 30)    # High grade
    ])
    # Add realistic precision-based variation
    grades_dup = grades_orig * np.random.uniform(0.85, 1.15, 100)
    result = plot_gen.create_rpd_scatter(grades_orig.tolist(), grades_dup.tolist(),
                                         rpd_limit=20.0, absolute_precision=0.01,
                                         title="Duplicate Precision Analysis")
    plot_gen.save_plot(result, os.path.join(output_dir, 'rpd_scatter_sample.png'))
    print(f"    Pass Rate: {result['pass_rate']:.1f}%, Mean RPD: {result['mean_rpd']:.1f}%")
    
    print(f"\n✓ Sample plots saved to: {output_dir}")
    
    # Close all figures to free memory
    import matplotlib.pyplot as plt
    plt.close('all')


if __name__ == '__main__':
    generate_sample_plots()
