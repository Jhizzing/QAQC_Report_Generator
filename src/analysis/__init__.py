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
        self.westgard_config = self.config.get('westgard_rules', {'enable': False, 'rules': []})

    @staticmethod
    def _coerce_float(value):
        """Best-effort numeric conversion."""
        try:
            converted = float(value)
        except (TypeError, ValueError):
            return None
        if converted != converted:  # NaN guard
            return None
        return converted

    def _extract_measured_values(self, records) -> list:
        """Extract measured values from either numeric lists or row dictionaries."""
        if not records:
            return []

        measured = []
        if isinstance(records, dict):
            records = [records]

        # Raw numeric list
        if isinstance(records, list) and records and not isinstance(records[0], dict):
            for item in records:
                value = self._coerce_float(item)
                if value is not None:
                    measured.append(value)
            return measured

        preferred_keys = (
            'result', 'value', 'measured', 'assay', 'au_ppm', 'au_gpt',
            'cu_ppm', 'pb_ppm', 'zn_ppm', 'fe_pct',
        )
        for row in records:
            if not isinstance(row, dict):
                continue

            chosen = None
            for key in preferred_keys:
                if key in row:
                    chosen = self._coerce_float(row.get(key))
                    if chosen is not None:
                        break

            # Fallback: first numeric-looking value in row
            if chosen is None:
                for value in row.values():
                    chosen = self._coerce_float(value)
                    if chosen is not None:
                        break

            if chosen is not None:
                measured.append(chosen)

        return measured

    def analyze(self, standards, *, certified_value: float = 0.0, uncertainty: float = None) -> dict:
        """Backward-compatible wrapper for legacy callers using ``analyze(...)``."""
        if isinstance(standards, dict):
            payload = standards
        else:
            payload = {
                'measured': self._extract_measured_values(standards),
                'certified': certified_value,
                'uncertainty': uncertainty,
            }
        return self.analyze_standards(payload)

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

    def check_westgard_rules(self, z_scores: list) -> dict:
        """
        Check Westgard rules for process control.

        Implemented Rules:
        - 1:3s: One value outside +/- 3SD (Failure)
        - 2:2s: Two consecutive values outside +/- 2SD (Failure)
        - R:4s: Range between consecutive values > 4SD (Failure)
        - 10:x: Ten consecutive values on same side of mean (Warning/Bias)

        Args:
            z_scores: List of Z-scores (chronological order)

        Returns:
            Dictionary with rule violations
        """
        if not self.westgard_config.get('enable', False):
            return {'violations': [], 'failed': False}

        violations = []
        rules = self.westgard_config.get('rules', [])
        n = len(z_scores)

        for i in range(n):
            z = z_scores[i]
            prev_z = z_scores[i-1] if i > 0 else 0

            # 1:3s Rule (Random Error)
            if "1_3s" in rules and abs(z) > 3:
                violations.append(f"1_3s failure at index {i}: Z={z:.2f}")

            # 2:2s Rule (Systematic Error)
            if "2_2s" in rules and i > 0:
                if (z > 2 and prev_z > 2) or (z < -2 and prev_z < -2):
                    violations.append(f"2_2s failure at index {i}: Consecutive > 2SD")

            # R:4s Rule (Random Error)
            if "R_4s" in rules and i > 0:
                if abs(z - prev_z) > 4:
                    violations.append(f"R_4s failure at index {i}: Range > 4SD")

        # 10:x Rule (Systematic Bias)
        if "10_x" in rules and n >= 10:
            # Check the last 10 points
            last_10 = z_scores[-10:]
            if all(v > 0 for v in last_10) or all(v < 0 for v in last_10):
                violations.append("10_x warning: Last 10 values on same side of mean")

        return {
            'violations': violations,
            'failed': any("failure" in v for v in violations)
        }

    def calculate_drift(self, z_scores: list, window: int = 5) -> dict:
        """
        Calculate rolling drift.

        Args:
            z_scores: List of Z-scores
            window: Rolling window size

        Returns:
            Dictionary with drift analysis
        """
        if len(z_scores) < window:
            return {'drift_detected': False, 'trend': 0.0}

        # Simple rolling mean of last 'window' points
        recent_mean = sum(z_scores[-window:]) / window
        
        # Drift is significant if rolling mean > 1.5 SD
        drift_detected = abs(recent_mean) > 1.5

        return {
            'drift_detected': drift_detected,
            'recent_mean_z': recent_mean,
            'trend': "Positive" if recent_mean > 0 else "Negative"
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
        westgard_assessment = self.check_westgard_rules(z_scores)
        drift_assessment = self.calculate_drift(z_scores)
        recoveries = self.calculate_recovery(measured, certified)
        recovery_assessment = self.assess_recovery(recoveries)
        precision_assessment = self.calculate_precision(measured)

        # Overall assessment
        overall_acceptable = (
            not bias_assessment['bias_detected'] and
            not westgard_assessment['failed'] and
            recovery_assessment['acceptable'] and
            precision_assessment['acceptable']
        )

        return {
            'overall_acceptable': overall_acceptable,
            'bias': bias_assessment,
            'westgard': westgard_assessment,
            'drift': drift_assessment,
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

    @staticmethod
    def _coerce_float(value):
        try:
            converted = float(value)
        except (TypeError, ValueError):
            return None
        if converted != converted:  # NaN guard
            return None
        return converted

    def _extract_blank_values(self, blanks) -> list:
        """Extract blank values from simple numeric lists or row dictionaries."""
        if not blanks:
            return []

        if isinstance(blanks, dict):
            blanks = [blanks]

        values = []
        if isinstance(blanks, list) and blanks and not isinstance(blanks[0], dict):
            for item in blanks:
                value = self._coerce_float(item)
                if value is not None:
                    values.append(value)
            return values

        preferred_keys = ('result', 'value', 'measured', 'blank')
        for row in blanks:
            if not isinstance(row, dict):
                continue

            chosen = None
            for key in preferred_keys:
                if key in row:
                    chosen = self._coerce_float(row.get(key))
                    if chosen is not None:
                        break

            if chosen is None:
                for value in row.values():
                    chosen = self._coerce_float(value)
                    if chosen is not None:
                        break

            if chosen is not None:
                values.append(chosen)

        return values

    def analyze(self, blanks, *, detection_limit: float = None, previous_samples: list = None) -> dict:
        """Backward-compatible wrapper for legacy callers using ``analyze(...)``."""
        if isinstance(blanks, dict):
            payload = blanks
        else:
            payload = {
                'blanks': self._extract_blank_values(blanks),
                'previous_samples': previous_samples or [],
            }

        result = self.analyze_blanks(payload)
        if detection_limit is not None:
            result.setdefault('summary', {})['detection_limit'] = detection_limit
        return result

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
        blanks = self._extract_blank_values(data.get('blanks', []))
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
        self.precision_method = self.config.get('precision_method', 'simple_rpd')
        self.hyperbolic_m = self.config.get('hyperbolic_m', 1.0)
        self.hyperbolic_c = self.config.get('hyperbolic_c', 0.0)

    @staticmethod
    def _coerce_float(value):
        try:
            converted = float(value)
        except (TypeError, ValueError):
            return None
        if converted != converted:  # NaN guard
            return None
        return converted

    def _extract_numeric_from_row(self, row: dict):
        preferred_keys = (
            'result', 'value', 'measured', 'assay', 'original', 'duplicate',
            'or', 'ck', 'au_ppm', 'au_gpt', 'cu_ppm', 'pb_ppm', 'zn_ppm', 'fe_pct',
        )
        for key in preferred_keys:
            if key in row:
                value = self._coerce_float(row.get(key))
                if value is not None:
                    return value
        for value in row.values():
            coerced = self._coerce_float(value)
            if coerced is not None:
                return coerced
        return None

    def _extract_duplicate_pairs(self, duplicates) -> list:
        """Extract duplicate pairs from legacy representations."""
        if not duplicates:
            return []

        # Already in pair format
        if isinstance(duplicates, list) and duplicates and isinstance(duplicates[0], (list, tuple)):
            pairs = []
            for pair in duplicates:
                if len(pair) < 2:
                    continue
                left = self._coerce_float(pair[0])
                right = self._coerce_float(pair[1])
                if left is not None and right is not None:
                    pairs.append([left, right])
            return pairs

        # Scalar list -> pair consecutive values
        if isinstance(duplicates, list) and duplicates and not isinstance(duplicates[0], dict):
            numeric = [self._coerce_float(v) for v in duplicates]
            numeric = [v for v in numeric if v is not None]
            return [[numeric[i], numeric[i + 1]] for i in range(0, len(numeric) - 1, 2)]

        if not isinstance(duplicates, list):
            return []

        pairs = []

        # Dicts with explicit pair keys
        explicit_keys = (
            ('original', 'duplicate'),
            ('primary', 'duplicate'),
            ('value1', 'value2'),
            ('or', 'ck'),
        )
        for row in duplicates:
            if not isinstance(row, dict):
                continue
            for left_key, right_key in explicit_keys:
                if left_key in row and right_key in row:
                    left = self._coerce_float(row.get(left_key))
                    right = self._coerce_float(row.get(right_key))
                    if left is not None and right is not None:
                        pairs.append([left, right])
                    break

        if pairs:
            return pairs

        # Group by sample ID root (e.g., RC0001 + RC0001-DUP)
        grouped = {}
        for row in duplicates:
            if not isinstance(row, dict):
                continue
            sample_id = None
            for id_key in ('sample_id', 'sampleid', 'sample', 'id', 'Sample_ID', 'SampleID'):
                if id_key in row:
                    sample_id = str(row.get(id_key, '')).strip().upper()
                    break
            value = self._extract_numeric_from_row(row)
            if not sample_id or value is None:
                continue

            for suffix in ('-DUPLICATE', '_DUPLICATE', '-DUP', '_DUP', '-CK', '_CK'):
                if sample_id.endswith(suffix):
                    sample_id = sample_id[:-len(suffix)]
                    break
            grouped.setdefault(sample_id, []).append(value)

        for values in grouped.values():
            if len(values) >= 2:
                pairs.append([values[0], values[1]])

        if pairs:
            return pairs

        # Final fallback: numeric values from rows, paired in order
        numeric_values = []
        for row in duplicates:
            if isinstance(row, dict):
                value = self._extract_numeric_from_row(row)
                if value is not None:
                    numeric_values.append(value)
        return [[numeric_values[i], numeric_values[i + 1]] for i in range(0, len(numeric_values) - 1, 2)]

    def analyze(self, duplicates) -> dict:
        """Backward-compatible wrapper for legacy callers using ``analyze(...)``."""
        if isinstance(duplicates, dict):
            payload = duplicates
        else:
            payload = {'duplicates': self._extract_duplicate_pairs(duplicates)}
        return self.analyze_duplicates(payload)

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

    def calculate_hyperbolic_precision(self, duplicates: list) -> dict:
        """
        Calculate precision using the Hyperbolic Method (Simandl, 1997).
        
        y^2 = m^2 * x^2 + c^2
        Where y = Absolute Difference, x = Mean Value
        
        Args:
            duplicates: List of [value1, value2] pairs

        Returns:
            Dictionary with hyperbolic precision assessment
        """
        if not duplicates:
            return {'failures': [], 'failure_rate': 0, 'acceptable': True}

        failures = []
        m = self.hyperbolic_m
        c = self.hyperbolic_c

        for i, (v1, v2) in enumerate(duplicates):
            mean_val = (v1 + v2) / 2
            abs_diff = abs(v1 - v2)
            
            # Calculate max allowed difference (hyperbolic curve)
            max_diff = (m**2 * mean_val**2 + c**2) ** 0.5
            
            if abs_diff > max_diff:
                failures.append({
                    'index': i,
                    'mean': mean_val,
                    'diff': abs_diff,
                    'limit': max_diff
                })

        failure_rate = len(failures) / len(duplicates)
        acceptable = failure_rate <= 0.1  # Max 10% failure rate

        return {
            'method': 'hyperbolic',
            'failures': failures,
            'failure_rate': failure_rate,
            'acceptable': acceptable,
            'params': {'m': m, 'c': c}
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

    def calculate_correlation(self, duplicates: list) -> dict:
        """
        Calculate Pearson correlation coefficient for duplicate pairs.
        
        Args:
            duplicates: List of [value1, value2] pairs
            
        Returns:
            Dictionary with correlation coefficient, p-value, and interpretation
        """
        if len(duplicates) < 3:
            return {
                'coefficient': 0.0,
                'p_value': 1.0,
                'strength': 'insufficient_data',
                'meets_threshold': False
            }
        
        try:
            from scipy.stats import pearsonr
            import numpy as np
            
            # Extract original and duplicate values
            original_values = [pair[0] for pair in duplicates]
            duplicate_values = [pair[1] for pair in duplicates]
            
            # Calculate Pearson correlation
            correlation_coef, p_value = pearsonr(original_values, duplicate_values)
            
            # Interpret correlation strength
            abs_coef = abs(correlation_coef)
            if abs_coef >= 0.8:
                strength = 'strong'
            elif abs_coef >= 0.5:
                strength = 'moderate'
            else:
                strength = 'weak'
            
            # Check against threshold (default 0.8 from config)
            correlation_threshold = self.config.get('correlation_threshold', 0.8)
            meets_threshold = abs_coef >= correlation_threshold
            
            return {
                'coefficient': float(correlation_coef),
                'p_value': float(p_value),
                'strength': strength,
                'meets_threshold': meets_threshold,
                'threshold': correlation_threshold,
                'statistically_significant': p_value < 0.05
            }
        except ImportError:
            # Fallback if scipy not available
            return {
                'coefficient': 0.0,
                'p_value': 1.0,
                'strength': 'calculation_unavailable',
                'meets_threshold': False,
                'error': 'scipy not available'
            }

    def calculate_nugget_ratio(self, duplicates: list) -> dict:
        """
        Calculate nugget ratio for spatial analysis with detailed statistics.

        Nugget ratio = nugget / (nugget + sill)
        
        Where:
        - Nugget = average absolute difference between pairs (measurement error)
        - Sill = variance of pair means (spatial variance)
        - Ratio indicates proportion of variance due to measurement error

        Args:
            duplicates: List of [value1, value2] pairs

        Returns:
            Dictionary with nugget ratio, nugget, sill, and interpretation
        """
        if len(duplicates) < 2:
            return {
                'ratio': 0.0,
                'nugget': 0.0,
                'sill': 0.0,
                'interpretation': 'insufficient_data',
                'meets_threshold': True
            }

        # Calculate pair means and absolute differences
        pair_means = [(pair[0] + pair[1]) / 2 for pair in duplicates]
        pair_diffs = [abs(pair[0] - pair[1]) for pair in duplicates]

        # Nugget = average absolute difference (measurement precision)
        nugget = sum(pair_diffs) / len(pair_diffs) if pair_diffs else 0.0
        
        # Sill = variance of pair means (spatial variability)
        mean_of_means = sum(pair_means) / len(pair_means) if pair_means else 0.0
        sill = sum((mean - mean_of_means) ** 2 for mean in pair_means) / len(pair_means) if pair_means else 0.0

        # Calculate ratio
        if nugget + sill == 0:
            ratio = 0.0
        else:
            ratio = nugget / (nugget + sill)

        # Interpret ratio
        # Low ratio (<0.3) = good precision, most variance is spatial
        # Moderate (0.3-0.6) = acceptable, some measurement error
        # High (>0.6) = poor precision, most variance is measurement error
        if ratio < 0.3:
            interpretation = 'low'
        elif ratio < 0.6:
            interpretation = 'moderate'
        else:
            interpretation = 'high'
        
        # Check against threshold (default 0.3 from config)
        nugget_threshold = self.config.get('nugget_threshold', 0.3)
        meets_threshold = ratio <= nugget_threshold

        return {
            'ratio': float(ratio),
            'nugget': float(nugget),
            'sill': float(sill),
            'interpretation': interpretation,
            'meets_threshold': meets_threshold,
            'threshold': nugget_threshold,
            'pair_count': len(duplicates)
        }

    def analyze_duplicates(self, data: dict) -> dict:
        """
        Complete duplicates analysis.

        Args:
            data: Dictionary with 'duplicates' key (list of [value1, value2] pairs)

        Returns:
            Comprehensive analysis results
        """
        duplicates = self._extract_duplicate_pairs(data.get('duplicates', []))

        # Calculate metrics
        if self.precision_method == 'hyperbolic':
            precision = self.calculate_hyperbolic_precision(duplicates)
            # Add RPD stats for reference
            rpd_stats = self.assess_precision(duplicates)
            precision['mean_rpd'] = rpd_stats['mean_rpd']
            precision['max_rpd'] = rpd_stats['max_rpd']
        else:
            precision = self.assess_precision(duplicates)

        systematic = self.detect_systematic_errors(duplicates)
        nugget_ratio_result = self.calculate_nugget_ratio(duplicates)
        correlation_result = self.calculate_correlation(duplicates)

        # Overall assessment
        overall_acceptable = (
            precision['acceptable'] and
            not systematic['systematic_error'] and
            nugget_ratio_result['meets_threshold'] and
            correlation_result.get('meets_threshold', True)  # Correlation is informational, not blocking
        )

        return {
            'overall_acceptable': overall_acceptable,
            'precision': precision,
            'systematic_errors': systematic,
            'nugget_ratio': nugget_ratio_result.get('ratio', 0.0),
            'nugget_ratio_details': nugget_ratio_result,
            'correlation': correlation_result,
            'summary': {
                'n_duplicates': len(duplicates),
                'mean_rpd': precision.get('mean_rpd', 0),
                'max_rpd': precision.get('max_rpd', 0),
                'correlation_coefficient': correlation_result.get('coefficient', 0.0),
                'nugget_ratio': nugget_ratio_result.get('ratio', 0.0)
            }
        }
