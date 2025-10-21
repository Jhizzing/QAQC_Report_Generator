"""
Analysis engines for QAQC application.
"""

class QAQCAnalyzer:
    def __init__(self) -> None:
        pass

class StandardsAnalyzer:
    """
    Analyzes certified reference materials (standards) for bias and precision.

    Key metrics:
    - Z-scores for bias detection
    - Control charts (Shewhart, CUSUM)
    - Recovery percentages
    - Precision assessment
    """

    def __init__(self, config: dict = None) -> None:
        """
        Initialize with QAQC configuration.

        Args:
            config: Dictionary with thresholds and settings
        """
        self.config = config or {}
        self.z_score_threshold = self.config.get('z_score_threshold', 2.0)
        self.recovery_limits = self.config.get('recovery_limits', (90, 110))  # %
        self.precision_threshold = self.config.get('precision_threshold', 5.0)  # %RSD

    def calculate_z_scores(self, measured: list, certified: float, uncertainty: float = None) -> list:
        """
        Calculate Z-scores for bias detection.

        Z = (measured - certified) / uncertainty

        Args:
            measured: List of measured values
            certified: Certified reference value
            uncertainty: Certified uncertainty (default: 5% of certified)

        Returns:
            List of Z-scores
        """
        if uncertainty is None:
            uncertainty = certified * 0.05  # Default 5% uncertainty

        z_scores = [(m - certified) / uncertainty for m in measured]
        return z_scores

    def detect_bias(self, z_scores: list) -> dict:
        """
        Detect systematic bias using Z-scores.

        Args:
            z_scores: List of Z-scores

        Returns:
            Dictionary with bias assessment
        """
        abs_z_scores = [abs(z) for z in z_scores]
        max_z = max(abs_z_scores) if abs_z_scores else 0
        mean_z = sum(z_scores) / len(z_scores) if z_scores else 0

        bias_detected = max_z > self.z_score_threshold
        systematic_bias = abs(mean_z) > self.z_score_threshold

        return {
            'bias_detected': bias_detected,
            'systematic_bias': systematic_bias,
            'max_z_score': max_z,
            'mean_z_score': mean_z,
            'z_scores': z_scores
        }

    def calculate_recovery(self, measured: list, certified: float) -> list:
        """
        Calculate recovery percentages.

        Recovery % = (measured / certified) * 100

        Args:
            measured: List of measured values
            certified: Certified reference value

        Returns:
            List of recovery percentages
        """
        recoveries = [(m / certified) * 100 for m in measured]
        return recoveries

    def assess_recovery(self, recoveries: list) -> dict:
        """
        Assess recovery acceptability.

        Args:
            recoveries: List of recovery percentages

        Returns:
            Dictionary with recovery assessment
        """
        min_recovery, max_recovery = self.recovery_limits
        acceptable = all(min_recovery <= r <= max_recovery for r in recoveries)
        mean_recovery = sum(recoveries) / len(recoveries) if recoveries else 0

        return {
            'acceptable': acceptable,
            'mean_recovery': mean_recovery,
            'recoveries': recoveries,
            'limits': self.recovery_limits
        }

    def calculate_precision(self, values: list) -> dict:
        """
        Calculate precision metrics (RSD, CV).

        Args:
            values: List of measured values

        Returns:
            Dictionary with precision metrics
        """
        if len(values) < 2:
            return {'rsd': 0, 'cv': 0, 'acceptable': True}

        mean_val = sum(values) / len(values)
        variance = sum((v - mean_val) ** 2 for v in values) / (len(values) - 1)
        std_dev = variance ** 0.5

        rsd = (std_dev / mean_val) * 100 if mean_val != 0 else 0
        cv = std_dev / mean_val if mean_val != 0 else 0

        acceptable = rsd <= self.precision_threshold

        return {
            'rsd': rsd,
            'cv': cv,
            'std_dev': std_dev,
            'mean': mean_val,
            'acceptable': acceptable,
            'threshold': self.precision_threshold
        }

    def analyze_standards(self, data: dict) -> dict:
        """
        Complete standards analysis.

        Args:
            data: Dictionary with 'measured', 'certified', 'uncertainty' keys

        Returns:
            Comprehensive analysis results
        """
        measured = data.get('measured', [])
        certified = data.get('certified', 0)
        uncertainty = data.get('uncertainty')

        # Calculate metrics
        z_scores = self.calculate_z_scores(measured, certified, uncertainty)
        bias_assessment = self.detect_bias(z_scores)
        recoveries = self.calculate_recovery(measured, certified)
        recovery_assessment = self.assess_recovery(recoveries)
        precision_assessment = self.calculate_precision(measured)

        # Overall assessment
        overall_acceptable = (
            not bias_assessment['bias_detected'] and
            recovery_assessment['acceptable'] and
            precision_assessment['acceptable']
        )

        return {
            'overall_acceptable': overall_acceptable,
            'bias': bias_assessment,
            'recovery': recovery_assessment,
            'precision': precision_assessment,
            'summary': {
                'n_measurements': len(measured),
                'certified_value': certified,
                'uncertainty': uncertainty
            }
        }

class BlanksAnalyzer:
    """
    Analyzes blank samples for contamination and carry-over effects.

    Key metrics:
    - Contamination thresholds
    - Carry-over detection
    - Background levels
    - Method detection limits
    """

    def __init__(self, config: dict = None) -> None:
        """
        Initialize with QAQC configuration.

        Args:
            config: Dictionary with thresholds and settings
        """
        self.config = config or {}
        self.contamination_threshold = self.config.get('contamination_threshold', 3.0)  # x MDL
        self.carryover_threshold = self.config.get('carryover_threshold', 5.0)  # %
        self.blank_limit = self.config.get('blank_limit', 0.1)  # absolute value

    def calculate_mdl(self, blanks: list, confidence: float = 0.95) -> float:
        """
        Calculate Method Detection Limit from blanks.

        MDL = t * std_dev(blanks)

        Args:
            blanks: List of blank values
            confidence: Confidence level (default 95%)

        Returns:
            Method Detection Limit
        """
        if len(blanks) < 3:
            return 0.0

        # Student's t-value for 95% confidence
        t_values = {0.90: 1.64, 0.95: 1.96, 0.99: 2.58}
        t_value = t_values.get(confidence, 1.96)

        mean_blank = sum(blanks) / len(blanks)
        variance = sum((b - mean_blank) ** 2 for b in blanks) / (len(blanks) - 1)
        std_dev = variance ** 0.5

        mdl = t_value * std_dev
        return mdl

    def detect_contamination(self, blanks: list, mdl: float = None) -> dict:
        """
        Detect contamination in blank samples.

        Args:
            blanks: List of blank values
            mdl: Method Detection Limit (calculated if not provided)

        Returns:
            Dictionary with contamination assessment
        """
        if mdl is None:
            mdl = self.calculate_mdl(blanks)

        contaminated = [b for b in blanks if b > (mdl * self.contamination_threshold)]
        contamination_rate = len(contaminated) / len(blanks) if blanks else 0

        return {
            'contaminated_samples': contaminated,
            'contamination_rate': contamination_rate,
            'mdl': mdl,
            'threshold': mdl * self.contamination_threshold,
            'acceptable': contamination_rate <= 0.1  # Max 10% contamination
        }

    def detect_carryover(self, blanks: list, previous_samples: list = None) -> dict:
        """
        Detect carry-over effects from previous samples.

        Args:
            blanks: List of blank values
            previous_samples: List of previous sample values (optional)

        Returns:
            Dictionary with carry-over assessment
        """
        if len(blanks) < 2:
            return {'carryover_detected': False, 'carryover_rate': 0}

        # Simple trend analysis
        sorted_blanks = sorted(blanks)
        trend = (sorted_blanks[-1] - sorted_blanks[0]) / len(blanks)

        # Check for increasing trend (potential carry-over)
        carryover_detected = trend > (max(blanks) * self.carryover_threshold / 100)

        return {
            'carryover_detected': carryover_detected,
            'trend': trend,
            'max_blank': max(blanks),
            'min_blank': min(blanks)
        }

    def assess_background(self, blanks: list) -> dict:
        """
        Assess background levels and variability.

        Args:
            blanks: List of blank values

        Returns:
            Dictionary with background assessment
        """
        if not blanks:
            return {'mean': 0, 'std_dev': 0, 'acceptable': True}

        mean_bg = sum(blanks) / len(blanks)
        variance = sum((b - mean_bg) ** 2 for b in blanks) / (len(blanks) - 1) if len(blanks) > 1 else 0
        std_dev = variance ** 0.5

        # Background should be low and consistent
        acceptable = mean_bg <= self.blank_limit and std_dev <= (mean_bg * 0.5)

        return {
            'mean': mean_bg,
            'std_dev': std_dev,
            'cv': (std_dev / mean_bg) * 100 if mean_bg != 0 else 0,
            'acceptable': acceptable,
            'limit': self.blank_limit
        }

    def analyze_blanks(self, data: dict) -> dict:
        """
        Complete blanks analysis.

        Args:
            data: Dictionary with 'blanks' key and optional 'previous_samples'

        Returns:
            Comprehensive analysis results
        """
        blanks = data.get('blanks', [])
        previous_samples = data.get('previous_samples', [])

        # Calculate metrics
        mdl = self.calculate_mdl(blanks)
        contamination = self.detect_contamination(blanks, mdl)
        carryover = self.detect_carryover(blanks, previous_samples)
        background = self.assess_background(blanks)

        # Overall assessment
        overall_acceptable = (
            contamination['acceptable'] and
            not carryover['carryover_detected'] and
            background['acceptable']
        )

        return {
            'overall_acceptable': overall_acceptable,
            'contamination': contamination,
            'carryover': carryover,
            'background': background,
            'mdl': mdl,
            'summary': {
                'n_blanks': len(blanks),
                'mdl': mdl,
                'max_blank': max(blanks) if blanks else 0
            }
        }

class DuplicatesAnalyzer:
    """
    Analyzes duplicate samples for precision assessment.

    Key metrics:
    - Relative Percent Difference (RPD)
    - Precision limits
    - Systematic errors
    - Nugget ratio
    """

    def __init__(self, config: dict = None) -> None:
        """
        Initialize with QAQC configuration.

        Args:
            config: Dictionary with thresholds and settings
        """
        self.config = config or {}
        self.rpd_threshold = self.config.get('rpd_threshold', 20.0)  # %
        self.precision_limit = self.config.get('precision_limit', 15.0)  # %
        self.nugget_threshold = self.config.get('nugget_threshold', 0.3)  # ratio

    def calculate_rpd(self, value1: float, value2: float) -> float:
        """
        Calculate Relative Percent Difference.

        RPD = |value1 - value2| / ((value1 + value2) / 2) * 100

        Args:
            value1: First measurement
            value2: Second measurement

        Returns:
            RPD percentage
        """
        if value1 == 0 and value2 == 0:
            return 0.0

        mean_val = (value1 + value2) / 2
        if mean_val == 0:
            return float('inf')

        rpd = abs(value1 - value2) / mean_val * 100
        return rpd

    def assess_precision(self, duplicates: list) -> dict:
        """
        Assess precision from duplicate pairs.

        Args:
            duplicates: List of [value1, value2] pairs

        Returns:
            Dictionary with precision assessment
        """
        if not duplicates:
            return {'rpd_values': [], 'mean_rpd': 0, 'acceptable': True}

        rpd_values = [self.calculate_rpd(pair[0], pair[1]) for pair in duplicates]
        mean_rpd = sum(rpd_values) / len(rpd_values)
        max_rpd = max(rpd_values)

        # Check if all RPDs are within acceptable limits
        acceptable = all(rpd <= self.rpd_threshold for rpd in rpd_values)

        return {
            'rpd_values': rpd_values,
            'mean_rpd': mean_rpd,
            'max_rpd': max_rpd,
            'acceptable': acceptable,
            'threshold': self.rpd_threshold
        }

    def detect_systematic_errors(self, duplicates: list) -> dict:
        """
        Detect systematic errors in duplicate pairs.

        Args:
            duplicates: List of [value1, value2] pairs

        Returns:
            Dictionary with systematic error assessment
        """
        if len(duplicates) < 3:
            return {'systematic_error': False, 'bias': 0}

        # Calculate bias for each pair
        biases = [(pair[0] - pair[1]) / ((pair[0] + pair[1]) / 2) for pair in duplicates]
        mean_bias = sum(biases) / len(biases)

        # Check for consistent bias (systematic error)
        systematic_error = abs(mean_bias) > 0.1  # 10% consistent bias

        return {
            'systematic_error': systematic_error,
            'bias': mean_bias,
            'biases': biases
        }

    def calculate_nugget_ratio(self, duplicates: list) -> float:
        """
        Calculate nugget ratio for spatial analysis.

        Nugget ratio = nugget / (nugget + sill)

        Args:
            duplicates: List of [value1, value2] pairs

        Returns:
            Nugget ratio (0-1)
        """
        if len(duplicates) < 2:
            return 0.0

        # Simple nugget calculation from duplicate variance
        pair_means = [(pair[0] + pair[1]) / 2 for pair in duplicates]
        pair_diffs = [abs(pair[0] - pair[1]) for pair in duplicates]

        nugget = sum(pair_diffs) / len(pair_diffs)
        sill = sum((mean - sum(pair_means) / len(pair_means)) ** 2 for mean in pair_means) / len(pair_means)

        if nugget + sill == 0:
            return 0.0

        nugget_ratio = nugget / (nugget + sill)
        return nugget_ratio

    def analyze_duplicates(self, data: dict) -> dict:
        """
        Complete duplicates analysis.

        Args:
            data: Dictionary with 'duplicates' key (list of [value1, value2] pairs)

        Returns:
            Comprehensive analysis results
        """
        duplicates = data.get('duplicates', [])

        # Calculate metrics
        precision = self.assess_precision(duplicates)
        systematic = self.detect_systematic_errors(duplicates)
        nugget_ratio = self.calculate_nugget_ratio(duplicates)

        # Overall assessment
        overall_acceptable = (
            precision['acceptable'] and
            not systematic['systematic_error'] and
            nugget_ratio <= self.nugget_threshold
        )

        return {
            'overall_acceptable': overall_acceptable,
            'precision': precision,
            'systematic_errors': systematic,
            'nugget_ratio': nugget_ratio,
            'summary': {
                'n_duplicates': len(duplicates),
                'mean_rpd': precision['mean_rpd'],
                'max_rpd': precision['max_rpd']
            }
        }
