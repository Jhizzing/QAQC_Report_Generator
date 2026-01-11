# Results Interpretation Guide

Complete guide to understanding and interpreting your QAQC analysis results.

## Table of Contents

1. [Results Dashboard Overview](#results-dashboard-overview)
2. [Understanding Control Charts](#understanding-control-charts)
3. [Reading Scatter Plots](#reading-scatter-plots)
4. [Interpreting Histograms](#interpreting-histograms)
5. [Pass/Fail Criteria](#passfail-criteria)
6. [Statistical Metrics Explained](#statistical-metrics-explained)
7. [Troubleshooting Results](#troubleshooting-results)

---

## Results Dashboard Overview

### Summary Cards

The dashboard displays key metrics at a glance:

**Total Samples**: All samples analyzed in your dataset

**Standards**: Number of standard/CRM samples analyzed

**Blanks**: Number of blank samples analyzed

**Duplicates**: Number of duplicate pairs analyzed

**Overall Pass Rate**: Percentage of samples passing all QAQC criteria

**Interpreting Summary**:
- **Pass Rate ≥ 95%**: Excellent quality
- **Pass Rate 90-95%**: Good quality, minor issues
- **Pass Rate < 90%**: Needs attention, investigate failures

### Tab Navigation

**Standards Tab**: Control charts and statistics for CRM/standard samples

**Blanks Tab**: Contamination plots and statistics for blank samples

**Duplicates Tab**: Scatter plots and precision metrics for duplicate pairs

**Switching Tabs**: Click tab headers to view different QAQC types

---

## Understanding Control Charts

### What is a Control Chart?

A control chart is a time-series plot showing measurements against control limits to detect out-of-control processes.

### Control Chart Components

**X-Axis**: Sample sequence or batch number (time order)

**Y-Axis**: Assay result (concentration)

**Target Line**: Certified value for the CRM (horizontal line)

**Control Limits**:
- **±2SD Bands**: Warning limits (yellow/green zone)
- **±3SD Bands**: Action limits (red zone)

**Data Points**:
- **Green points**: Within ±2SD (passing)
- **Yellow points**: Between ±2SD and ±3SD (warning)
- **Red points**: Outside ±3SD (failing)

### Interpreting Control Charts

**Good Performance**:
- Points cluster around target line
- Most points within ±2SD bands
- No systematic trends
- Random scatter around target

**Warning Signs**:
- Points approaching ±2SD limits
- Increasing variability
- Minor trends or shifts

**Problems**:
- Points outside ±3SD limits (failures)
- Systematic trends (drift)
- Shifts in mean value
- Increasing variability over time

### Common Patterns

**In Control**:
- Random scatter around target
- Points within control limits
- No patterns or trends

**Drift**:
- Gradual increase or decrease over time
- Suggests laboratory drift
- May need instrument recalibration

**Shift**:
- Sudden change in mean value
- Suggests method change or instrument issue
- Investigate cause of shift

**Trend**:
- Systematic increase or decrease
- May indicate contamination or method degradation
- Requires investigation

**Cycles**:
- Periodic patterns
- May indicate batch effects or instrument cycles
- Review batch groupings

### Using Control Charts

**For Each CRM**:
- Review control chart for each CRM separately
- Check for CRM-specific issues
- Compare performance across CRMs

**Batch Analysis**:
- Group points by batch
- Identify batches with failures
- Review batch-specific issues

**Trend Analysis**:
- Look for systematic trends
- Identify when problems started
- Track improvement over time

---

## Reading Scatter Plots

### Original vs. Duplicate Scatter Plot

**Purpose**: Compare original and duplicate values to assess precision

**X-Axis**: Original sample value

**Y-Axis**: Duplicate sample value

**1:1 Reference Line**: Perfect agreement line (slope = 1, intercept = 0)

**Data Points**:
- **Green points**: Passing (within precision target)
- **Red points**: Failing (outside precision target)

**Interpreting**:
- **Points on 1:1 line**: Perfect agreement
- **Points near 1:1 line**: Good precision
- **Points scattered**: Poor precision
- **Systematic offset**: Bias between original and duplicate

### RPD Scatter Plot

**Purpose**: Show precision across grade range

**X-Axis**: Mean of original and duplicate values

**Y-Axis**: Relative Percent Difference (RPD)

**Precision Envelope**: Target RPD zone (green area)

**Data Points**:
- **Green points**: Within precision target
- **Red points**: Outside precision target

**Interpreting**:
- **Points in envelope**: Good precision
- **Points above envelope**: Poor precision
- **Higher RPD at low grades**: Normal (expected)
- **High RPD at high grades**: Problem (should be better)

### Bland-Altman Plot

**Purpose**: Detect systematic bias between measurements

**X-Axis**: Mean of original and duplicate values

**Y-Axis**: Difference between original and duplicate

**Mean Difference Line**: Average difference (horizontal line)

**Limits of Agreement**: ±1.96 SD of differences

**Interpreting**:
- **Mean difference near zero**: No systematic bias
- **Mean difference offset**: Systematic bias present
- **Points within limits**: Good agreement
- **Points outside limits**: Poor agreement

---

## Interpreting Histograms

### What is a Histogram?

A histogram shows the distribution of values in your data.

### Histogram Components

**X-Axis**: Value ranges (bins)

**Y-Axis**: Frequency (number of samples in each bin)

**Bars**: Height shows frequency in each range

### Interpreting Histograms

**Normal Distribution**:
- Bell-shaped curve
- Symmetric around mean
- Indicates good data quality

**Skewed Distribution**:
- Asymmetric distribution
- May indicate issues or natural variation
- Common in geological data

**Bimodal Distribution**:
- Two peaks
- May indicate two populations
- Review sample types

**Outliers**:
- Isolated bars far from main distribution
- May indicate errors or special samples
- Investigate outliers

### Standards Histogram

**Purpose**: Show distribution of standard/CRM results

**Expected**: Normal distribution around certified value

**Interpreting**:
- **Centered on certified value**: Good accuracy
- **Shifted from certified value**: Systematic bias
- **Wide distribution**: High variability (poor precision)
- **Narrow distribution**: Low variability (good precision)

### Blanks Histogram

**Purpose**: Show distribution of blank values

**Expected**: Most values near zero, below detection limit

**Interpreting**:
- **Values near zero**: Good (no contamination)
- **Values above detection limit**: Contamination detected
- **Wide distribution**: Variable contamination
- **Narrow distribution**: Consistent blanks

### Duplicates Histogram

**Purpose**: Show distribution of RPD values

**Expected**: Most RPD values below target (e.g., < 20%)

**Interpreting**:
- **Low RPD values**: Good precision
- **High RPD values**: Poor precision
- **Most below target**: Good overall precision
- **Many above target**: Precision issues

---

## Pass/Fail Criteria

### Standards Pass/Fail

**Passing**:
- Result within tolerance of certified value
- Z-score < 2 (or within ±2SD)
- No systematic bias

**Failing**:
- Result outside tolerance
- Z-score ≥ 3 (or outside ±3SD)
- Systematic bias detected

**Warning**:
- Result approaching tolerance limit
- Z-score 2-3 (between ±2SD and ±3SD)
- Monitor closely

### Blanks Pass/Fail

**Passing**:
- Value below detection limit
- No contamination detected

**Failing**:
- Value above detection limit
- Value > contamination multiplier × detection limit
- Contamination detected

**Warning**:
- Value near detection limit
- Monitor closely

### Duplicates Pass/Fail

**Passing**:
- RPD within precision target (e.g., < 20%)
- Good agreement between pairs

**Failing**:
- RPD outside precision target (e.g., > 20%)
- Poor agreement between pairs

**Warning**:
- RPD approaching target limit
- Monitor closely

### Overall Pass Rate

**Calculation**: (Passing samples / Total samples) × 100%

**Interpretation**:
- **≥ 95%**: Excellent quality
- **90-95%**: Good quality, minor issues
- **85-90%**: Acceptable, some issues
- **< 85%**: Needs attention, investigate failures

---

## Statistical Metrics Explained

### Z-Score

**Definition**: Number of standard deviations a value is from the mean

**Formula**: Z = (Value - Mean) / Standard Deviation

**Interpretation**:
- **|Z| < 2**: Acceptable (within ±2SD)
- **2 ≤ |Z| < 3**: Warning (between ±2SD and ±3SD)
- **|Z| ≥ 3**: Failure (outside ±3SD)

**For Standards**: Z-score compares result to certified value

### RPD (Relative Percent Difference)

**Definition**: Measure of precision between duplicate samples

**Formula**: RPD = |Original - Duplicate| / Mean × 100%

**Interpretation**:
- **Lower RPD**: Better precision
- **Higher RPD**: Poorer precision
- **Target**: Typically < 20% for good precision

**Note**: RPD can be high at low grades (normal)

### Mean

**Definition**: Average value

**Formula**: Mean = Sum of values / Number of values

**Interpretation**:
- **For Standards**: Should be near certified value
- **For Blanks**: Should be near zero
- **For Duplicates**: Mean of pairs

### Standard Deviation (SD)

**Definition**: Measure of variability

**Formula**: SD = √(Σ(x - mean)² / n)

**Interpretation**:
- **Low SD**: Low variability (good precision)
- **High SD**: High variability (poor precision)

### Relative Standard Deviation (RSD)

**Definition**: Coefficient of variation (SD as percentage of mean)

**Formula**: RSD = (SD / Mean) × 100%

**Interpretation**:
- **Low RSD**: Good precision
- **High RSD**: Poor precision
- **Typical**: < 10% for good precision

### Bias

**Definition**: Systematic error (difference from true value)

**Formula**: Bias = Mean - Certified Value

**Interpretation**:
- **Near zero**: No bias (good accuracy)
- **Positive**: Overestimation
- **Negative**: Underestimation

### Correlation (r)

**Definition**: Measure of linear relationship

**Range**: -1 to +1

**Interpretation**:
- **r = 1**: Perfect positive correlation
- **r = 0**: No correlation
- **r = -1**: Perfect negative correlation
- **r > 0.9**: Strong correlation (good for duplicates)

---

## Troubleshooting Results

### Too Many Failures

**Possible Causes**:
- Thresholds too strict
- Laboratory issues
- Data quality problems
- Incorrect configuration

**Solutions**:
1. Review flagged samples
2. Check laboratory performance
3. Verify data quality
4. Check configuration settings
5. Adjust thresholds if justified

### Unexpected Results

**Possible Causes**:
- Data import issues
- Incorrect column mapping
- Configuration errors
- Data quality problems

**Solutions**:
1. Verify data imported correctly
2. Check column mappings
3. Review configuration settings
4. Check data for errors
5. Re-import if needed

### No Results Displayed

**Possible Causes**:
- No samples of that type
- Analysis not run
- Data filtering issues

**Solutions**:
1. Check data has samples of that type
2. Verify analysis completed
3. Check filters applied
4. Review data structure

### Charts Not Displaying

**Possible Causes**:
- No data for chart
- Browser issues
- Data format problems

**Solutions**:
1. Check data exists
2. Refresh browser
3. Check browser console for errors
4. Try different browser

---

**Next Steps**: After reviewing results, proceed to [Report Generation Guide](GUIDE_REPORTS.md)

**Need help?** → [FAQ](FAQ.md) | [User Manual](USER_MANUAL.md)
