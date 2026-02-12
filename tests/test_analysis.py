"""
Tests for analysis modules.
"""
import pytest
from src.analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer


class TestStandardsAnalyzer:
    """Test StandardsAnalyzer functionality."""

    def test_init_default_config(self):
        """Test initialization with default config."""
        analyzer = StandardsAnalyzer()
        assert analyzer.z_score_threshold == 2.0
        assert analyzer.recovery_limits == (90, 110)
        assert analyzer.precision_threshold == 5.0

    def test_init_custom_config(self):
        """Test initialization with custom config."""
        config = {
            'z_score_threshold': 3.0,
            'recovery_limits': (85, 115),
            'precision_threshold': 10.0
        }
        analyzer = StandardsAnalyzer(config)
        assert analyzer.z_score_threshold == 3.0
        assert analyzer.recovery_limits == (85, 115)
        assert analyzer.precision_threshold == 10.0

    def test_calculate_z_scores(self):
        """Test Z-score calculation."""
        analyzer = StandardsAnalyzer()
        measured = [10.0, 10.5, 9.8]
        certified = 10.0
        uncertainty = 0.5

        z_scores = analyzer.calculate_z_scores(measured, certified, uncertainty)
        expected = [0.0, 1.0, -0.4]

        for i, (actual, expected_val) in enumerate(zip(z_scores, expected)):
            assert abs(actual - expected_val) < 0.001

    def test_calculate_z_scores_default_uncertainty(self):
        """Test Z-score calculation with default uncertainty."""
        analyzer = StandardsAnalyzer()
        measured = [10.0, 10.5, 9.8]
        certified = 10.0

        z_scores = analyzer.calculate_z_scores(measured, certified)
        # Default uncertainty is 5% of certified = 0.5
        expected = [0.0, 1.0, -0.4]

        for i, (actual, expected_val) in enumerate(zip(z_scores, expected)):
            assert abs(actual - expected_val) < 0.001

    def test_detect_bias(self):
        """Test bias detection."""
        analyzer = StandardsAnalyzer()
        z_scores = [0.5, 1.0, 2.5, -0.5]

        result = analyzer.detect_bias(z_scores)

        assert result['bias_detected'] == True  # max_z = 2.5 > 2.0
        assert result['systematic_bias'] == False  # mean_z = 0.875 < 2.0
        assert result['max_z_score'] == 2.5
        assert result['mean_z_score'] == 0.875

    def test_calculate_recovery(self):
        """Test recovery calculation."""
        analyzer = StandardsAnalyzer()
        measured = [9.5, 10.0, 10.5]
        certified = 10.0

        recoveries = analyzer.calculate_recovery(measured, certified)
        expected = [95.0, 100.0, 105.0]

        for actual, expected_val in zip(recoveries, expected):
            assert abs(actual - expected_val) < 0.001

    def test_assess_recovery(self):
        """Test recovery assessment."""
        analyzer = StandardsAnalyzer()
        recoveries = [95.0, 100.0, 105.0]

        result = analyzer.assess_recovery(recoveries)

        assert result['acceptable'] == True
        assert result['mean_recovery'] == 100.0
        assert result['recoveries'] == recoveries

    def test_assess_recovery_unacceptable(self):
        """Test recovery assessment with unacceptable values."""
        analyzer = StandardsAnalyzer()
        recoveries = [85.0, 100.0, 115.0]  # Outside 90-110 range

        result = analyzer.assess_recovery(recoveries)

        assert result['acceptable'] == False

    def test_calculate_precision(self):
        """Test precision calculation."""
        analyzer = StandardsAnalyzer()
        values = [10.0, 10.2, 9.8, 10.1, 9.9]

        result = analyzer.calculate_precision(values)

        assert result['acceptable'] == True  # RSD should be low
        assert result['mean'] == 10.0
        assert result['rsd'] > 0

    def test_calculate_precision_insufficient_data(self):
        """Test precision calculation with insufficient data."""
        analyzer = StandardsAnalyzer()
        values = [10.0]

        result = analyzer.calculate_precision(values)

        assert result['rsd'] == 0
        assert result['acceptable'] == True

    def test_analyze_standards(self):
        """Test complete standards analysis."""
        analyzer = StandardsAnalyzer()
        data = {
            'measured': [10.0, 10.2, 9.8],
            'certified': 10.0,
            'uncertainty': 0.5
        }

        result = analyzer.analyze_standards(data)

        assert 'overall_acceptable' in result
        assert 'bias' in result
        assert 'recovery' in result
        assert 'precision' in result
        assert 'summary' in result


class TestBlanksAnalyzer:
    """Test BlanksAnalyzer functionality."""

    def test_init_default_config(self):
        """Test initialization with default config."""
        analyzer = BlanksAnalyzer()
        assert analyzer.contamination_threshold == 3.0
        assert analyzer.carryover_threshold == 5.0
        assert analyzer.blank_limit == 0.1

    def test_calculate_mdl(self):
        """Test MDL calculation."""
        analyzer = BlanksAnalyzer()
        blanks = [0.01, 0.02, 0.015, 0.018, 0.012]

        mdl = analyzer.calculate_mdl(blanks)

        assert mdl > 0
        assert mdl < max(blanks)  # MDL should be reasonable

    def test_calculate_mdl_insufficient_data(self):
        """Test MDL calculation with insufficient data."""
        analyzer = BlanksAnalyzer()
        blanks = [0.01, 0.02]

        mdl = analyzer.calculate_mdl(blanks)

        assert mdl == 0.0

    def test_detect_contamination(self):
        """Test contamination detection."""
        analyzer = BlanksAnalyzer()
        blanks = [0.01, 0.02, 0.05, 0.01, 0.02]

        result = analyzer.detect_contamination(blanks)

        assert 'contaminated_samples' in result
        assert 'contamination_rate' in result
        assert 'mdl' in result
        assert 'acceptable' in result

    def test_detect_carryover(self):
        """Test carry-over detection."""
        analyzer = BlanksAnalyzer()
        blanks = [0.01, 0.02, 0.03, 0.04, 0.05]  # Increasing trend

        result = analyzer.detect_carryover(blanks)

        assert 'carryover_detected' in result
        assert 'trend' in result
        assert 'max_blank' in result
        assert 'min_blank' in result

    def test_detect_carryover_insufficient_data(self):
        """Test carry-over detection with insufficient data."""
        analyzer = BlanksAnalyzer()
        blanks = [0.01]

        result = analyzer.detect_carryover(blanks)

        assert result['carryover_detected'] == False
        assert result['carryover_rate'] == 0

    def test_assess_background(self):
        """Test background assessment."""
        analyzer = BlanksAnalyzer()
        blanks = [0.01, 0.02, 0.015, 0.018, 0.012]

        result = analyzer.assess_background(blanks)

        assert 'mean' in result
        assert 'std_dev' in result
        assert 'cv' in result
        assert 'acceptable' in result

    def test_assess_background_empty(self):
        """Test background assessment with empty data."""
        analyzer = BlanksAnalyzer()
        blanks = []

        result = analyzer.assess_background(blanks)

        assert result['mean'] == 0
        assert result['std_dev'] == 0
        assert result['acceptable'] == True

    def test_analyze_blanks(self):
        """Test complete blanks analysis."""
        analyzer = BlanksAnalyzer()
        data = {
            'blanks': [0.01, 0.02, 0.015, 0.018, 0.012],
            'previous_samples': [1.0, 2.0, 1.5]
        }

        result = analyzer.analyze_blanks(data)

        assert 'overall_acceptable' in result
        assert 'contamination' in result
        assert 'carryover' in result
        assert 'background' in result
        assert 'mdl' in result
        assert 'summary' in result


class TestDuplicatesAnalyzer:
    """Test DuplicatesAnalyzer functionality."""

    def test_init_default_config(self):
        """Test initialization with default config."""
        analyzer = DuplicatesAnalyzer()
        assert analyzer.rpd_threshold == 20.0
        assert analyzer.precision_limit == 15.0
        assert analyzer.nugget_threshold == 0.3

    def test_calculate_rpd(self):
        """Test RPD calculation."""
        analyzer = DuplicatesAnalyzer()

        # Test normal case
        rpd = analyzer.calculate_rpd(10.0, 12.0)
        expected = abs(10.0 - 12.0) / ((10.0 + 12.0) / 2) * 100
        assert abs(rpd - expected) < 0.001

        # Test zero values
        rpd_zero = analyzer.calculate_rpd(0.0, 0.0)
        assert rpd_zero == 0.0

        # Test one zero value
        rpd_inf = analyzer.calculate_rpd(0.0, 10.0)
        assert rpd_inf == 200.0  # RPD = |0-10| / ((0+10)/2) * 100 = 10/5 * 100 = 200%

    def test_assess_precision(self):
        """Test precision assessment."""
        analyzer = DuplicatesAnalyzer()
        duplicates = [[10.0, 12.0], [15.0, 16.0], [20.0, 22.0]]

        result = analyzer.assess_precision(duplicates)

        assert 'rpd_values' in result
        assert 'mean_rpd' in result
        assert 'max_rpd' in result
        assert 'acceptable' in result
        assert len(result['rpd_values']) == 3

    def test_assess_precision_empty(self):
        """Test precision assessment with empty data."""
        analyzer = DuplicatesAnalyzer()
        duplicates = []

        result = analyzer.assess_precision(duplicates)

        assert result['rpd_values'] == []
        assert result['mean_rpd'] == 0
        assert result['acceptable'] == True

    def test_detect_systematic_errors(self):
        """Test systematic error detection."""
        analyzer = DuplicatesAnalyzer()
        duplicates = [[10.0, 12.0], [15.0, 17.0], [20.0, 22.0]]  # Consistent bias

        result = analyzer.detect_systematic_errors(duplicates)

        assert 'systematic_error' in result
        assert 'bias' in result
        assert 'biases' in result

    def test_detect_systematic_errors_insufficient_data(self):
        """Test systematic error detection with insufficient data."""
        analyzer = DuplicatesAnalyzer()
        duplicates = [[10.0, 12.0]]

        result = analyzer.detect_systematic_errors(duplicates)

        assert result['systematic_error'] == False
        assert result['bias'] == 0

    def test_calculate_nugget_ratio(self):
        """Test nugget ratio calculation."""
        analyzer = DuplicatesAnalyzer()
        duplicates = [[10.0, 12.0], [15.0, 17.0], [20.0, 22.0]]

        result = analyzer.calculate_nugget_ratio(duplicates)

        assert isinstance(result, dict)
        assert 'ratio' in result
        assert 0 <= result['ratio'] <= 1
        assert 'nugget' in result
        assert 'sill' in result
        assert 'interpretation' in result

    def test_calculate_nugget_ratio_insufficient_data(self):
        """Test nugget ratio calculation with insufficient data."""
        analyzer = DuplicatesAnalyzer()
        duplicates = [[10.0, 12.0]]

        result = analyzer.calculate_nugget_ratio(duplicates)

        assert isinstance(result, dict)
        assert result['ratio'] == 0.0
        assert result['interpretation'] == 'insufficient_data'

    def test_analyze_duplicates(self):
        """Test complete duplicates analysis."""
        analyzer = DuplicatesAnalyzer()
        data = {
            'duplicates': [[10.0, 12.0], [15.0, 17.0], [20.0, 22.0]]
        }

        result = analyzer.analyze_duplicates(data)

        assert 'overall_acceptable' in result
        assert 'precision' in result
        assert 'systematic_errors' in result
        assert 'nugget_ratio' in result
        assert 'summary' in result
