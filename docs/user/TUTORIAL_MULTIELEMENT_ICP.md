# Tutorial: Multi-Element ICP Analysis

Complete step-by-step guide for analyzing multi-element ICP-MS/OES data using the demo dataset.

## Overview

This tutorial walks you through analyzing multi-element geochemistry data from ICP-MS or ICP-OES laboratory analysis. You'll learn how to:
- Load and configure multi-element ICP demo data
- Understand major vs. trace element differences
- Set up element-specific QAQC thresholds
- Interpret results for different element types

**Time**: 15-20 minutes  
**Prerequisites**: None - uses built-in demo data

---

## Step 1: Load Demo Data

1. **Open the application** and navigate to the **Data Import** section
2. **Click "Multi-Element ICP"** button in the demo data section
3. The demo dataset loads automatically with:
   - ~200 samples total
   - **Major elements**: Cu, Pb, Zn, Fe, S (% levels)
   - **Trace elements**: Ni, Co, As, Mo, Ag, Au (ppm/g/t levels)
   - QAQC samples: Standards, Blanks, Duplicates
   - Realistic concentration ranges for base metals exploration

**What you'll see:**
- Sample IDs: ICP0001, ICP0002, etc. (unknowns)
- Standards: OREAS-201, OREAS-202, OREAS-400 (rotating)
- Blanks: BLANK-ICP-1, BLANK-ICP-2, etc.
- Duplicates: ICP0009-DUP, ICP0027-DUP, etc.

**Element Columns:**
- Major: `Cu_pct`, `Pb_ppm` or `Pb_pct`, `Zn_ppm`, `Fe_pct`, `S_pct`
- Trace: `Au_gpt`, `Ag_ppm`, `Ni_ppm`, `Co_ppm`, `As_ppm`, `Mo_ppm`

---

## Step 2: Configure Analysis

### 2.1 Select Category

1. **Category**: **"pXRF / Multi-element"** (covers multi-element ICP)
2. This sets appropriate defaults for multi-element analysis

### 2.2 Configure Methodology

**Assay Method**: ICP-MS (or ICP-OES for major elements)

**Analytical Method**: ICP-MS (automatically selected)
- This sets element-specific defaults based on method

**Target Elements**: 
- **Major**: Cu, Pb, Zn, Fe, S
- **Trace**: Au, Ag, Ni, Co, As, Mo

**Insertion Rate**: 5-10% for each QAQC type

### 2.3 Set QAQC Rules

#### Standards Configuration

**Selected CRMs**:
- OREAS-201 (low-mid grade porphyry)
- OREAS-202 (mid-grade porphyry)
- OREAS-400 (high-grade VMS)

**Tolerance Settings**:
- **Tolerance Type**: Percentage
- **Default Tolerance**: 10% (fallback)
- **Element-Specific Tolerances** (automatically applied based on ICP-MS method):

| Element | Category | Tolerance | Why |
|---------|----------|-----------|-----|
| Cu | Major | 8% | Good precision for major elements |
| Pb | Major | 8% | Good precision for major elements |
| Zn | Major | 8% | Good precision for major elements |
| Fe | Major | 4% | Very good precision for major elements |
| S | Major | 8% | Good precision for major elements |
| Au | Trace | 12% | Moderate precision, nugget effect |
| Ag | Trace | 12% | Moderate precision |
| Ni | Trace | 12% | Moderate precision |
| Co | Trace | 18% | Lower precision for trace elements |
| As | Trace | 18% | Lower precision for trace elements |
| Mo | Trace | 12% | Moderate precision |

**Why Different Tolerances?**
- **Major elements** (>1%): Require higher precision (5-10%)
- **Trace elements** (<0.1%): Accept lower precision (10-20%)
- **Method precision**: ICP-MS better for trace, ICP-OES better for major
- **Geological variability**: Some elements (Au, Co) have nugget effect

#### Blanks Configuration

**Detection Limits** (element-specific, ICP-MS):

| Element | Detection Limit | Unit | Notes |
|---------|----------------|------|-------|
| Cu | 1 | ppm | Good detection for ICP-MS |
| Pb | 0.5 | ppm | Excellent detection |
| Zn | 1 | ppm | Good detection |
| Fe | 0.01 | % | Major element, uses % |
| S | 0.01 | % | Major element, uses % |
| Au | 0.01 | g/t | Fire assay typically, but ICP can detect |
| Ag | 0.1 | ppm | Good detection |
| Ni | 1 | ppm | Good detection |
| Co | 0.5 | ppm | Good detection |
| As | 2 | ppm | Good detection |
| Mo | 0.5 | ppm | Good detection |

**Contamination Threshold**: 3× detection limit

**ICP Blank Considerations:**
- Lab blanks should be very clean (<DL)
- Method blanks check for contamination in preparation
- Field blanks may have higher background
- Different elements have different detection limits

#### Duplicates Configuration

**Precision Targets** (element-specific, HARD method, ICP-MS):

| Element | Category | Precision Target | Expected Range |
|---------|----------|-----------------|----------------|
| Cu | Major | 6% HARD | 5-8% |
| Pb | Major | 6% HARD | 5-8% |
| Zn | Major | 6% HARD | 5-8% |
| Fe | Major | 3% HARD | 3-5% |
| S | Major | 6% HARD | 5-8% |
| Au | Trace | 12% HARD | 10-15% |
| Ag | Trace | 10% HARD | 8-12% |
| Ni | Trace | 10% HARD | 8-12% |
| Co | Trace | 15% HARD | 12-18% |
| As | Trace | 15% HARD | 12-18% |
| Mo | Trace | 10% HARD | 8-12% |

**Why HARD?**
- HARD is less sensitive to low concentrations
- Better for trace elements
- More appropriate for geochemistry

---

## Step 3: Run Analysis

1. **Click "Run Analysis"**
2. The analysis processes with element-specific thresholds
3. Results appear in the **Results Dashboard**

**Expected Processing Time**: < 5 seconds for demo data

---

## Step 4: Interpret Results

### 4.1 Standards Results

**What Good Looks Like:**
- **Pass Rate**: 90-98% (ICP has better precision than pXRF)
- **Control Chart**: Most points within ±2SD bands
- **Recovery**: 95-105% of certified values
- **RSD**: 3-10% (relative standard deviation)

**Element-Specific Expectations:**

| Element | Category | Expected Pass Rate | Typical RSD | Notes |
|---------|----------|-------------------|-------------|-------|
| Cu | Major | 95-98% | 5-8% | Excellent precision |
| Pb | Major | 95-98% | 5-8% | Excellent precision |
| Zn | Major | 95-98% | 5-8% | Excellent precision |
| Fe | Major | 97-99% | 3-5% | Very good precision |
| S | Major | 95-98% | 5-8% | Excellent precision |
| Au | Trace | 90-95% | 10-15% | Nugget effect possible |
| Ag | Trace | 92-96% | 8-12% | Good precision |
| Ni | Trace | 92-96% | 8-12% | Good precision |
| Co | Trace | 85-92% | 12-18% | Lower precision |
| As | Trace | 85-92% | 12-18% | Lower precision |
| Mo | Trace | 92-96% | 8-12% | Good precision |

**Key Differences: Major vs. Trace**

**Major Elements:**
- Higher precision expected (3-8% RSD)
- Stricter tolerances (4-8%)
- Better pass rates (95%+)
- More consistent results

**Trace Elements:**
- Lower precision acceptable (8-18% RSD)
- More lenient tolerances (12-18%)
- Good pass rates (85-95%)
- Higher variability normal

**Common Issues:**
- **Low pass rate for major elements**: Investigate - should be >95%
- **Low pass rate for trace elements**: May be acceptable if >85%
- **Systematic bias**: Check calibration or method issues
- **High scatter**: Check for contamination or method problems

### 4.2 Blanks Results

**What Good Looks Like:**
- **Contamination Rate**: < 2% of blanks exceed 3×DL
- **Max Values**: Below detection limit for most elements
- **Histogram**: Most values clustered near zero

**Element-Specific Expectations:**

| Element | Detection Limit | Good Max Value | Notes |
|---------|----------------|----------------|-------|
| Cu | 1 ppm | < 1 ppm | Should be very clean |
| Pb | 0.5 ppm | < 0.5 ppm | Excellent detection |
| Zn | 1 ppm | < 1 ppm | Should be very clean |
| Fe | 0.01% | < 0.01% | Major element |
| S | 0.01% | < 0.01% | Major element |
| Au | 0.01 g/t | < 0.01 g/t | Very low detection |
| Ag | 0.1 ppm | < 0.1 ppm | Good detection |
| Ni | 1 ppm | < 1 ppm | Should be clean |
| Co | 0.5 ppm | < 0.5 ppm | Good detection |
| As | 2 ppm | < 2 ppm | Good detection |
| Mo | 0.5 ppm | < 0.5 ppm | Good detection |

**Common Issues:**
- **High contamination**: Check sample preparation procedures
- **Element-specific contamination**: May indicate reagent issues
- **Consistent contamination**: Check for systematic problems

### 4.3 Duplicates Results

**What Good Looks Like:**
- **Within Target**: 90-98% for major elements, 80-90% for trace elements
- **Mean RPD/HARD**: Below target precision for each element
- **Scatter Plot**: Points clustered around 1:1 line
- **No systematic bias**: Points evenly distributed

**Element-Specific Precision Expectations:**

| Element | Category | Expected Precision | Within Target % |
|---------|----------|-------------------|-----------------|
| Cu | Major | 5-8% HARD | 95-98% |
| Pb | Major | 5-8% HARD | 95-98% |
| Zn | Major | 5-8% HARD | 95-98% |
| Fe | Major | 3-5% HARD | 97-99% |
| S | Major | 5-8% HARD | 95-98% |
| Au | Trace | 10-15% HARD | 85-92% |
| Ag | Trace | 8-12% HARD | 90-95% |
| Ni | Trace | 8-12% HARD | 90-95% |
| Co | Trace | 12-18% HARD | 80-88% |
| As | Trace | 12-18% HARD | 80-88% |
| Mo | Trace | 8-12% HARD | 90-95% |

**Key Observations:**

**Major Elements:**
- Very tight precision (3-8% HARD)
- High within-target rates (95%+)
- Points tightly clustered on scatter plot
- Low RSD values

**Trace Elements:**
- Moderate precision (8-18% HARD)
- Good within-target rates (80-90%)
- More scatter on scatter plot (normal)
- Higher RSD values acceptable

**Common Issues:**
- **Poor precision for major elements**: Investigate - should be excellent
- **Poor precision for trace elements**: May be acceptable if within expected range
- **Systematic bias**: Check for method issues
- **Outliers**: May indicate sample heterogeneity (especially for Au)

---

## Step 5: Understanding Major vs. Trace Elements

### 5.1 Why Different Tolerances?

**Major Elements** (>1% typical):
- Higher concentrations = better precision
- Less affected by detection limits
- Require stricter QAQC (5-10% tolerance)
- Expected pass rates: 95%+

**Trace Elements** (<0.1% typical):
- Lower concentrations = lower precision
- More affected by detection limits
- Accept more lenient QAQC (10-20% tolerance)
- Expected pass rates: 85-95%

### 5.2 Method Differences

**ICP-MS** (Inductively Coupled Plasma Mass Spectrometry):
- Best for trace elements
- Lower detection limits
- Higher precision for low concentrations
- Used in this demo

**ICP-OES** (Inductively Coupled Plasma Optical Emission Spectroscopy):
- Best for major elements
- Higher precision for high concentrations
- Faster analysis
- Lower cost

**When to Use Which:**
- **ICP-MS**: Trace elements, low detection limits needed
- **ICP-OES**: Major elements, high throughput needed
- **Both**: Comprehensive analysis (major + trace)

### 5.3 Element-Specific Considerations

**Gold (Au)**:
- Often analyzed by Fire Assay (not ICP)
- Nugget effect common (high variability)
- Lower precision acceptable (12-15% HARD)
- May need special handling

**Base Metals (Cu, Pb, Zn)**:
- Can be major or trace depending on deposit
- Good precision expected (5-10% HARD)
- High pass rates expected (95%+)

**Iron and Sulfur (Fe, S)**:
- Major elements in many deposits
- Very good precision expected (3-5% HARD)
- Highest pass rates expected (97%+)

**Pathfinder Elements (As, Co, Mo)**:
- Trace elements
- Lower precision acceptable (12-18% HARD)
- Good pass rates (80-90%)

---

## Step 6: Generate Report

1. **Navigate to Report section**
2. **Select Report Type**:
   - **Figures Only**: Quick summary
   - **JORC Report**: Complete analysis
3. **Configure Options**:
   - Add metadata
   - Select figures
4. **Export**: Choose format

**Report Includes:**
- Element-specific summary statistics
- Major vs. trace element comparisons
- Control charts by element
- Precision analysis by element type
- Recommendations for multi-element analysis

---

## Expected Results Summary

### Overall Pass Rates (Good QAQC)

| QAQC Type | Expected Pass Rate | Notes |
|-----------|-------------------|-------|
| Standards | 90-98% | ICP has excellent precision |
| Blanks | 98-100% | Lab methods very clean |
| Duplicates | 85-95% | Varies by element type |

### Element-Specific Summary

**Major Elements (Cu, Pb, Zn, Fe, S)**:
- Very high precision (3-8% HARD)
- Stricter tolerances (4-8%)
- Excellent pass rates (95%+)
- Tight control charts

**Trace Elements (Au, Ag, Ni, Co, As, Mo)**:
- Moderate precision (8-18% HARD)
- More lenient tolerances (12-18%)
- Good pass rates (85-95%)
- More scatter acceptable

---

## Troubleshooting

### Low Standards Pass Rate for Major Elements

**Possible Causes:**
- Calibration drift
- Method issues
- Contamination
- Sample preparation problems

**Solutions:**
- Recalibrate instrument
- Check method validation
- Review sample preparation
- Investigate systematic issues

### Low Standards Pass Rate for Trace Elements

**Possible Causes:**
- Normal variability for trace elements
- Detection limit issues
- Geological variability (nugget effect)

**Solutions:**
- Accept if >85% (may be normal)
- Check detection limits appropriate
- Review element-specific tolerances
- Consider geological factors

### High Blank Contamination

**Possible Causes:**
- Contaminated reagents
- Sample preparation contamination
- Instrument contamination

**Solutions:**
- Check reagent blanks
- Review preparation procedures
- Clean instrument
- Investigate source of contamination

### Poor Duplicate Precision

**Possible Causes:**
- Sample heterogeneity
- Method precision limits
- Geological variability

**Solutions:**
- Accept appropriate precision for element type
- Check if within expected range
- Review sample preparation
- Consider geological factors

---

## Best Practices Summary

1. **Use Element-Specific Settings**: Don't apply same tolerance to all elements
2. **Distinguish Major vs. Trace**: Different expectations for each
3. **Select Appropriate CRMs**: Matrix-matched, covering concentration range
4. **Use Method-Specific Defaults**: ICP-MS vs. ICP-OES have different precision
5. **Accept Appropriate Precision**: Trace elements have higher variability
6. **Monitor Element-Specific Metrics**: Check each element separately
7. **Document Method**: Note ICP-MS vs. ICP-OES for each element

---

## Next Steps

- Try the **pXRF Tutorial** to compare field vs. lab methods
- Review **What Good Looks Like** guide for visual examples
- Explore **CRM Database** to find appropriate standards
- Read **Multi-Element QAQC Research** for detailed best practices

---

## Additional Resources

- [pXRF and Multi-Element QAQC Research](docs/research/PXRF_MULTIELEMENT_QAQC_RESEARCH.md)
- [CRM Recommendations](docs/research/CRM_RECOMMENDATIONS.md)
- [What Good Looks Like Guide](docs/user/WHAT_GOOD_LOOKS_LIKE.md)
- [Analysis Configuration Guide](docs/user/GUIDE_ANALYSIS_CONFIG.md)
