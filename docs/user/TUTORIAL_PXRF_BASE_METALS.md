# Tutorial: pXRF Base Metals Analysis

Complete step-by-step guide for analyzing pXRF base metals data using the demo dataset.

## Overview

This tutorial walks you through analyzing portable XRF (pXRF) data for base metals exploration. You'll learn how to:
- Load and configure pXRF demo data
- Set up element-specific QAQC thresholds
- Interpret pXRF-specific results
- Understand matrix effects and spectral interference considerations

**Time**: 15-20 minutes  
**Prerequisites**: None - uses built-in demo data

---

## Step 1: Load Demo Data

1. **Open the application** and navigate to the **Data Import** section
2. **Click "pXRF Base Metals"** button in the demo data section
3. The demo dataset loads automatically with:
   - ~200 samples total
   - Elements: Cu, Pb, Zn, Fe, As, Mn, Rb, Sr
   - QAQC samples: Standards, Blanks, Duplicates
   - Realistic concentration ranges for base metals exploration

**What you'll see:**
- Sample IDs: PX0001, PX0002, etc. (unknowns)
- Standards: OREAS-101a, OREAS-100, OREAS-102a (rotating)
- Blanks: BLANK-PX-1, BLANK-PX-2, etc.
- Duplicates: PX0009-DUP, PX0027-DUP, etc.

---

## Step 2: Configure Analysis

### 2.1 Select Category

1. **Category**: Automatically set to **"pXRF / Multi-element"**
2. This sets appropriate defaults for pXRF analysis

### 2.2 Configure Methodology

**Assay Method**: pXRF (portable X-ray Fluorescence)

**Target Elements**: 
- Cu (Copper)
- Pb (Lead)  
- Zn (Zinc)
- Fe (Iron)
- As (Arsenic)
- Mn (Manganese)
- Rb (Rubidium)
- Sr (Strontium)

**pXRF-Specific Settings**:
- **Matrix Correction**: Enabled (flags potential matrix effects)
- **Spectral Interference**: Enabled (flags known interferences like Pb-As overlap)
- **Insertion Rate**: 5-10% for each QAQC type

### 2.3 Set QAQC Rules

#### Standards Configuration

**Selected CRMs**:
- OREAS-100 (mid-grade)
- OREAS-101a (low-grade)
- OREAS-102a (mid-high grade)

**Tolerance Settings**:
- **Tolerance Type**: Percentage
- **Default Tolerance**: 15% (fallback)
- **Element-Specific Tolerances** (automatically applied):
  - Cu: 12%
  - Pb: 12%
  - Zn: 12%
  - Fe: 8% (major element, stricter)
  - As: 20% (trace element, more lenient)
  - Mn, Rb, Sr: 15% (default)

**Why these tolerances?**
- pXRF has lower precision than lab methods
- Major elements (Fe) require stricter tolerances
- Trace elements (As) have higher variability
- Matrix effects can cause additional scatter

#### Blanks Configuration

**Detection Limits** (element-specific):
- Cu: 10 ppm
- Pb: 10 ppm
- Zn: 10 ppm
- Fe: 0.1% (major element)
- As: 10 ppm
- Mn, Rb, Sr: 10 ppm

**Contamination Threshold**: 3× detection limit

**pXRF Blank Considerations**:
- Field blanks may have higher background than lab blanks
- Particle size and moisture can affect readings
- Some elements (light elements like Na, Mg) are not reliably detected by pXRF

#### Duplicates Configuration

**Precision Targets** (element-specific, HARD method):
- Cu: 15% HARD
- Pb: 15% HARD
- Zn: 15% HARD
- Fe: 10% HARD (major element, better precision)
- As: 25% HARD (trace element, lower precision)
- Mn, Rb, Sr: 20% HARD

**Why HARD instead of RPD?**
- HARD (Half Absolute Relative Difference) is more appropriate for pXRF
- Less sensitive to low concentrations
- Better reflects field precision

---

## Step 3: Run Analysis

1. **Click "Run Analysis"**
2. The analysis processes:
   - Standards against certified values
   - Blanks against detection limits
   - Duplicates for precision assessment
3. Results appear in the **Results Dashboard**

**Expected Processing Time**: < 5 seconds for demo data

---

## Step 4: Interpret Results

### 4.1 Standards Results

**What Good Looks Like:**
- **Pass Rate**: 85-95% (pXRF has lower precision than lab methods)
- **Control Chart**: Most points within ±2SD bands
- **Recovery**: 90-110% of certified values
- **RSD**: 8-15% (relative standard deviation)

**Element-Specific Expectations:**

| Element | Expected Pass Rate | Typical RSD | Notes |
|---------|-------------------|-------------|-------|
| Cu | 85-95% | 10-15% | Good precision for pXRF |
| Pb | 85-95% | 10-15% | Watch for As interference |
| Zn | 85-95% | 10-15% | Good precision |
| Fe | 90-98% | 5-10% | Major element, better precision |
| As | 80-90% | 15-20% | Trace element, lower precision |
| Mn | 85-95% | 10-15% | Good precision |
| Rb, Sr | 80-90% | 12-18% | Trace elements |

**Common Issues:**
- **Low pass rate (<80%)**: Check calibration, matrix effects, or instrument drift
- **Systematic bias**: All values high or low - may need recalibration
- **High scatter**: Matrix effects or particle size issues

**Interpreting Control Charts:**
- Points within green bands (±2SD): Good
- Points in yellow bands (±2-3SD): Warning - investigate
- Points outside red bands (>3SD): Failure - may need recalibration

### 4.2 Blanks Results

**What Good Looks Like:**
- **Contamination Rate**: < 5% of blanks exceed 3×DL
- **Max Values**: Below detection limit for most elements
- **Histogram**: Most values clustered near zero

**Element-Specific Detection Limits:**
- Major elements (Fe): 0.1% detection limit
- Base metals (Cu, Pb, Zn): 10 ppm detection limit
- Trace elements (As, Mn, Rb, Sr): 10 ppm detection limit

**Common Issues:**
- **High contamination**: Check for carry-over from previous samples
- **Field blanks higher than lab blanks**: Normal for pXRF field work
- **Element-specific contamination**: May indicate sample preparation issues

### 4.3 Duplicates Results

**What Good Looks Like:**
- **Within Target**: 80-90% of pairs within precision target
- **Mean RPD/HARD**: Below target precision for each element
- **Scatter Plot**: Points clustered around 1:1 line
- **No systematic bias**: Points evenly distributed above and below line

**Element-Specific Precision Expectations:**

| Element | Expected Precision | Within Target % |
|---------|-------------------|-----------------|
| Cu | 10-15% HARD | 85-95% |
| Pb | 10-15% HARD | 85-95% |
| Zn | 10-15% HARD | 85-95% |
| Fe | 5-10% HARD | 90-98% |
| As | 15-25% HARD | 75-85% |
| Mn | 12-18% HARD | 80-90% |
| Rb, Sr | 15-20% HARD | 75-85% |

**Interpreting Scatter Plots:**
- **Tight cluster**: Good precision
- **Wide scatter**: Lower precision (normal for trace elements)
- **Systematic offset**: Potential bias or matrix effect
- **Outliers**: May indicate sample heterogeneity

**Common Issues:**
- **Low precision for trace elements**: Normal - As, Rb, Sr have higher variability
- **High precision for major elements**: Expected - Fe should have <10% HARD
- **Systematic bias**: One value consistently higher - check for matrix effects

---

## Step 5: Understanding pXRF-Specific Considerations

### 5.1 Matrix Effects

**What are matrix effects?**
- pXRF readings are affected by sample composition
- High Z elements (Fe, Pb) can absorb X-rays
- Light elements (Na, Mg, Al) are poorly detected
- Particle size and moisture affect readings

**How the application handles it:**
- Matrix correction flagging (if enabled)
- Matrix-matched CRMs recommended
- Element-specific tolerances account for matrix effects

**Best Practices:**
- Use CRMs with similar matrix to samples
- Check for systematic bias in standards
- Consider particle size and moisture in field work

### 5.2 Spectral Interference

**Common Interferences:**
- **Pb L-lines overlap with As K-lines**: High Pb can cause false As readings
- **Zn K-lines can interfere with Cu**: Check when both are high
- **Fe can interfere with multiple elements**: High Fe affects other readings

**How the application handles it:**
- Spectral interference flagging (if enabled)
- Element-specific detection limits
- Warnings when interfering elements co-occur

**Best Practices:**
- Check for co-occurring interfering elements
- Use element-specific tolerances
- Consider re-analyzing samples with high interference risk

### 5.3 Field vs. Lab pXRF

**Field pXRF:**
- More variable conditions
- Check CRMs every 20-50 samples
- Higher precision variability
- Moisture and particle size effects more pronounced

**Lab pXRF:**
- Controlled conditions
- Check CRMs every 50-100 samples
- Better precision
- Can apply more sophisticated corrections

**Demo Data Characteristics:**
- Simulates field pXRF conditions
- Appropriate precision expectations
- Realistic QAQC insertion rates

---

## Step 6: Generate Report

1. **Navigate to Report section**
2. **Select Report Type**:
   - **Figures Only**: Quick summary with charts
   - **JORC Report**: Complete analysis report
3. **Configure Options**:
   - Add competent person name
   - Add company name
   - Select figures to include
4. **Export**: Choose format (Excel, PDF, DOCX)

**Report Includes:**
- Summary statistics by element
- Control charts for standards
- Histograms for blanks
- Scatter plots for duplicates
- Element-specific pass rates
- Recommendations for pXRF analysis

---

## Expected Results Summary

### Overall Pass Rates (Good QAQC)

| QAQC Type | Expected Pass Rate | Notes |
|-----------|-------------------|-------|
| Standards | 85-95% | pXRF has lower precision than lab methods |
| Blanks | 95-100% | Most blanks should be below DL |
| Duplicates | 80-90% | Field pXRF has higher variability |

### Element-Specific Summary

**Major Elements (Fe)**:
- Higher precision expected
- Stricter tolerances (8%)
- Better pass rates (90%+)

**Base Metals (Cu, Pb, Zn)**:
- Moderate precision (12% tolerance)
- Good pass rates (85-95%)
- Watch for spectral interference

**Trace Elements (As, Mn, Rb, Sr)**:
- Lower precision (15-25% tolerance)
- More lenient pass rates (75-85%)
- Higher variability expected

---

## Troubleshooting

### Low Standards Pass Rate

**Possible Causes:**
- Instrument drift - recalibrate
- Matrix mismatch - use matrix-matched CRMs
- Particle size issues - check sample preparation
- Moisture effects - dry samples if possible

**Solutions:**
- Recalibrate instrument
- Check CRM matrix matches samples
- Review sample preparation procedures
- Consider lab pXRF for better precision

### High Blank Contamination

**Possible Causes:**
- Carry-over from previous samples
- Contaminated sample preparation area
- Field contamination (dust, etc.)

**Solutions:**
- Clean instrument between samples
- Check sample preparation procedures
- Use field blanks appropriate for conditions
- Review contamination thresholds

### Poor Duplicate Precision

**Possible Causes:**
- Sample heterogeneity (nugget effect)
- Field conditions variability
- Instrument precision limits

**Solutions:**
- Accept higher variability for trace elements
- Use appropriate precision targets
- Consider sample preparation improvements
- Document field conditions

---

## Best Practices Summary

1. **Use Matrix-Matched CRMs**: Select CRMs with similar composition to samples
2. **Check Calibration Regularly**: Analyze CRMs every 20-50 samples in field
3. **Account for Matrix Effects**: Use element-specific tolerances
4. **Watch for Spectral Interference**: Check when interfering elements co-occur
5. **Accept Appropriate Precision**: pXRF has lower precision than lab methods
6. **Document Field Conditions**: Note moisture, particle size, temperature
7. **Use Element-Specific Settings**: Don't apply same tolerance to all elements

---

## Next Steps

- Try the **Multi-Element ICP Tutorial** to compare with lab methods
- Review **What Good Looks Like** guide for visual examples
- Explore **CRM Database** to find appropriate standards
- Read **pXRF Research Findings** for detailed best practices

---

## Additional Resources

- [pXRF and Multi-Element QAQC Research](docs/research/PXRF_MULTIELEMENT_QAQC_RESEARCH.md)
- [CRM Recommendations](docs/research/CRM_RECOMMENDATIONS.md)
- [What Good Looks Like Guide](docs/user/WHAT_GOOD_LOOKS_LIKE.md)
- [Analysis Configuration Guide](docs/user/GUIDE_ANALYSIS_CONFIG.md)
