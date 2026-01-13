# Analysis Methods Documentation

Technical documentation for QAQC analysis methods and statistical calculations.

## Table of Contents

1. [Correlation Analysis](#correlation-analysis)
2. [Nugget Ratio Calculation](#nugget-ratio-calculation)
3. [Statistical Interpretation Guidelines](#statistical-interpretation-guidelines)

---

## Correlation Analysis

### Overview

Correlation analysis measures the linear relationship between original and duplicate sample values. It provides insight into analytical precision and consistency.

### Method

**Pearson Correlation Coefficient (r)**

Calculated using the standard Pearson correlation formula:

```
r = Σ((x - x̄)(y - ȳ)) / √(Σ(x - x̄)² × Σ(y - ȳ)²)
```

Where:
- x = original sample values
- y = duplicate sample values
- x̄ = mean of original values
- ȳ = mean of duplicate values

### Statistical Significance

**P-Value Calculation**

The p-value is calculated using a t-test:

```
t = r × √((n - 2) / (1 - r²))
```

Where n is the number of pairs.

For large sample sizes (n > 30), a simplified approximation is used.

### Interpretation

**Correlation Strength**:
- **Strong (r ≥ 0.8)**: Excellent precision, strong linear relationship
- **Moderate (0.5 ≤ r < 0.8)**: Acceptable precision, moderate relationship
- **Weak (r < 0.5)**: Poor precision, weak relationship

**Statistical Significance**:
- **p < 0.05**: Statistically significant (reliable correlation)
- **p ≥ 0.05**: Not statistically significant (may be due to chance)

### Thresholds

**Default Threshold**: 0.8

**Configuration**: Adjustable in QAQC settings

**Use Cases**:
- Assess analytical precision
- Identify systematic relationships
- Detect precision issues
- Validate duplicate analysis quality

---

## Nugget Ratio Calculation

### Overview

Nugget ratio is a geostatistical measure that quantifies the proportion of total variance attributable to measurement error versus spatial variability.

### Method

**Nugget Ratio Formula**:

```
Nugget Ratio = Nugget / (Nugget + Sill)
```

**Nugget Calculation**:

```
Nugget = (1/n) × Σ|original_i - duplicate_i|
```

Where:
- n = number of duplicate pairs
- original_i = value of original sample in pair i
- duplicate_i = value of duplicate sample in pair i

**Sill Calculation**:

```
Sill = (1/n) × Σ(mean_i - mean_of_means)²
```

Where:
- mean_i = (original_i + duplicate_i) / 2 (mean of pair i)
- mean_of_means = average of all pair means

### Interpretation

**Ratio Interpretation**:
- **Low (<0.3)**: Good precision, most variance is spatial (natural variation)
- **Moderate (0.3-0.6)**: Acceptable, some measurement error present
- **High (>0.6)**: Poor precision, most variance is measurement error

**Component Interpretation**:
- **Low Nugget**: Small differences between pairs (good precision)
- **High Nugget**: Large differences between pairs (poor precision)
- **Low Sill**: Little spatial variation (homogeneous samples)
- **High Sill**: High spatial variation (heterogeneous samples)

### Thresholds

**Default Threshold**: 0.3

**Configuration**: Adjustable in QAQC settings

**Use Cases**:
- Assess measurement precision relative to spatial variability
- Identify precision issues
- Validate analytical method performance
- Guide sampling strategy improvements

---

## Statistical Interpretation Guidelines

### Minimum Sample Sizes

**Correlation Analysis**:
- Minimum: 3 pairs (for calculation)
- Recommended: ≥10 pairs (for reliable statistics)
- Optimal: ≥30 pairs (for robust p-value)

**Nugget Ratio**:
- Minimum: 2 pairs (for calculation)
- Recommended: ≥5 pairs (for meaningful interpretation)
- Optimal: ≥20 pairs (for stable ratio)

### Data Quality Requirements

**For Reliable Correlation**:
- Pairs should span a range of values
- Avoid duplicate pairs with identical values
- Check for outliers that may skew results

**For Reliable Nugget Ratio**:
- Pairs should represent spatial variation
- Avoid systematic bias in pair selection
- Ensure pairs are from similar sample types

### Common Issues

**Correlation Issues**:
- **Low correlation with good RPD**: May indicate non-linear relationship or outliers
- **High correlation with poor RPD**: May indicate systematic bias
- **Insufficient data**: Need more pairs for reliable statistics

**Nugget Ratio Issues**:
- **High nugget, low sill**: Measurement error dominates (precision problem)
- **Low nugget, high sill**: Good precision, high spatial variation (normal)
- **Both high**: Both measurement error and spatial variation are high

### Best Practices

1. **Enable both metrics** for comprehensive assessment
2. **Review thresholds** based on analytical method and project requirements
3. **Compare across elements** to identify method-specific issues
4. **Monitor trends** over time to detect degradation
5. **Use in combination** with RPD/HARD for complete precision assessment

---

## References

- Pearson, K. (1896). Mathematical contributions to the theory of evolution. *Philosophical Transactions of the Royal Society of London*, 189, 71-110.
- Simandl, G. J. (1997). Quality control in exploration geochemistry. *Exploration and Mining Geology*, 6(3), 225-236.
- Stanley, C. R. (2006). On the special application of Thompson-Howarth error analysis to geochemical variables exhibiting a nugget effect. *Geochemistry: Exploration, Environment, Analysis*, 6(4), 357-368.
