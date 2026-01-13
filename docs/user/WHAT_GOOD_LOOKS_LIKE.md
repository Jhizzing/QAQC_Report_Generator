# What Good QAQC Looks Like

Visual guide to interpreting QAQC results and understanding what constitutes good quality control in geochemical analysis.

## Overview

This guide helps you understand:
- What good QAQC results look like
- Expected pass rates by element type
- How to interpret charts and graphs
- Common failure patterns and their meanings
- Troubleshooting guide

---

## 1. Standards (CRM) Results

### 1.1 Pass Rate Expectations

**Overall Standards Pass Rate:**

| Analysis Type | Good Pass Rate | Excellent Pass Rate | Notes |
|--------------|---------------|-------------------|-------|
| Gold (Fire Assay) | 90-95% | 95-98% | High precision method |
| pXRF | 85-95% | 90-95% | Field method, lower precision |
| ICP-MS (Trace) | 90-95% | 95-98% | Excellent for trace elements |
| ICP-OES (Major) | 95-98% | 97-99% | Excellent for major elements |

**Element-Specific Pass Rates:**

| Element | Category | Good Pass Rate | Excellent | Method |
|---------|----------|---------------|-----------|--------|
| Au | Trace | 90-95% | 95-98% | Fire Assay |
| Cu | Major | 95-98% | 97-99% | ICP-OES |
| Cu | Trace | 90-95% | 95-98% | ICP-MS |
| Cu | Base Metal | 85-95% | 90-95% | pXRF |
| Pb | Major | 95-98% | 97-99% | ICP-OES |
| Pb | Base Metal | 85-95% | 90-95% | pXRF |
| Zn | Major | 95-98% | 97-99% | ICP-OES |
| Zn | Base Metal | 85-95% | 90-95% | pXRF |
| Fe | Major | 97-99% | 98-99% | ICP-OES |
| Fe | Major | 90-98% | 95-98% | pXRF |
| As | Trace | 85-92% | 90-95% | ICP-MS |
| As | Trace | 80-90% | 85-92% | pXRF |
| Ni | Trace | 92-96% | 95-98% | ICP-MS |
| Co | Trace | 85-92% | 90-95% | ICP-MS |

### 1.2 Control Chart Interpretation

**Good Control Chart Characteristics:**

✅ **Most points within ±2SD bands** (green/yellow zones)
✅ **Points evenly distributed** above and below mean
✅ **No systematic trends** (drift, shift, cycles)
✅ **Few points outside ±3SD** (red zone)
✅ **Recovery near 100%** (95-105%)

**Visual Indicators:**

```
Good Control Chart:
Certified Value: 100 ppm
Mean: 98.5 ppm (Recovery: 98.5%)
RSD: 6.2%

Points distribution:
- Within ±2SD: 18/20 (90%) ✅
- Within ±3SD: 19/20 (95%) ✅
- Outside ±3SD: 1/20 (5%) ✅
- Recovery: 98.5% ✅
```

**Warning Signs:**

⚠️ **Systematic bias**: All points on one side of mean
⚠️ **Drift**: Gradual trend up or down
⚠️ **High scatter**: Many points outside limits
⚠️ **Low recovery**: Mean far from certified value

**Failure Patterns:**

❌ **>10% failures**: Investigate calibration or method
❌ **Systematic bias >5%**: Recalibration needed
❌ **Drift trend**: Instrument drift or contamination
❌ **High RSD (>15% for major)**: Method precision issues

### 1.3 Recovery Percentages

**What Recovery Means:**
- Recovery = (Mean Measured / Certified Value) × 100%
- 100% = Perfect accuracy
- 95-105% = Excellent
- 90-110% = Good
- <90% or >110% = Bias, investigate

**Element-Specific Recovery Expectations:**

| Element | Category | Good Recovery | Excellent | Notes |
|---------|----------|--------------|-----------|-------|
| Major Elements | All | 95-105% | 97-103% | Very consistent |
| Base Metals | pXRF | 90-110% | 95-105% | Field method |
| Trace Elements | ICP-MS | 92-108% | 95-105% | Good precision |
| Trace Elements | pXRF | 85-115% | 90-110% | Lower precision |
| Au | Fire Assay | 95-105% | 97-103% | High precision |

---

## 2. Blanks Results

### 2.1 Contamination Rate Expectations

**Good Blank Results:**

| Analysis Type | Good Contamination Rate | Excellent | Notes |
|--------------|------------------------|-----------|-------|
| Lab Methods (ICP, Fire Assay) | < 2% | < 1% | Very clean |
| pXRF Field | < 5% | < 3% | Field conditions |
| pXRF Lab | < 3% | < 2% | Controlled conditions |

**Element-Specific Expectations:**

| Element | Detection Limit | Good Max | Excellent Max | Notes |
|---------|----------------|----------|--------------|-------|
| Au | 0.01 g/t | < 0.01 g/t | < 0.005 g/t | Very low |
| Cu | 1 ppm (ICP) | < 1 ppm | < 0.5 ppm | Clean |
| Cu | 10 ppm (pXRF) | < 10 ppm | < 5 ppm | Field method |
| Pb | 0.5 ppm (ICP) | < 0.5 ppm | < 0.3 ppm | Excellent |
| Fe | 0.01% | < 0.01% | < 0.005% | Major element |
| As | 2 ppm (ICP) | < 2 ppm | < 1 ppm | Good |
| As | 10 ppm (pXRF) | < 10 ppm | < 5 ppm | Field method |

### 2.2 Histogram Interpretation

**Good Blank Histogram:**

✅ **Most values near zero** (left side of histogram)
✅ **Peak at low values** (below detection limit)
✅ **Few high values** (right tail minimal)
✅ **No outliers** above contamination threshold

**Visual Pattern:**

```
Good Blank Distribution:
Detection Limit: 1 ppm
Contamination Threshold: 3 ppm

Distribution:
- Below DL: 18/20 (90%) ✅
- DL to 3×DL: 2/20 (10%) ✅
- Above 3×DL: 0/20 (0%) ✅
- Max Value: 2.1 ppm ✅
```

**Warning Signs:**

⚠️ **Multiple values above DL**: Check for contamination
⚠️ **Right tail in histogram**: Some contamination present
⚠️ **Outliers**: May indicate specific contamination events

**Failure Patterns:**

❌ **>5% above contamination threshold**: Significant contamination
❌ **Systematic elevation**: Contaminated reagents or preparation
❌ **Increasing trend**: Progressive contamination

---

## 3. Duplicates Results

### 3.1 Precision Expectations

**Overall Precision (Within Target %):**

| Analysis Type | Good | Excellent | Notes |
|--------------|------|-----------|-------|
| Gold (Fire Assay) | 85-92% | 90-95% | High precision |
| pXRF | 80-90% | 85-92% | Field method |
| ICP-MS (Trace) | 85-92% | 90-95% | Good precision |
| ICP-OES (Major) | 95-98% | 97-99% | Excellent precision |

**Element-Specific Precision (HARD %):**

| Element | Category | Good Precision | Excellent | Method |
|---------|----------|---------------|-----------|--------|
| Au | Trace | 10-15% HARD | 8-12% HARD | Fire Assay |
| Cu | Major | 5-8% HARD | 3-5% HARD | ICP-OES |
| Cu | Base Metal | 10-15% HARD | 8-12% HARD | pXRF |
| Pb | Major | 5-8% HARD | 3-5% HARD | ICP-OES |
| Zn | Major | 5-8% HARD | 3-5% HARD | ICP-OES |
| Fe | Major | 3-5% HARD | 2-4% HARD | ICP-OES |
| Fe | Major | 8-12% HARD | 6-10% HARD | pXRF |
| As | Trace | 12-18% HARD | 10-15% HARD | ICP-MS |
| As | Trace | 18-25% HARD | 15-20% HARD | pXRF |
| Ni | Trace | 8-12% HARD | 6-10% HARD | ICP-MS |
| Co | Trace | 12-18% HARD | 10-15% HARD | ICP-MS |

### 3.2 Scatter Plot Interpretation

**Good Scatter Plot Characteristics:**

✅ **Points clustered around 1:1 line**
✅ **Even distribution** above and below line
✅ **Tight cluster** for major elements
✅ **Reasonable scatter** for trace elements
✅ **No systematic bias** (one value consistently higher)

**Visual Patterns:**

**Major Elements (Cu, Pb, Zn, Fe, S):**
```
Good Scatter Plot (Major Elements):
- Points: Tightly clustered
- 1:1 Line: Points evenly distributed
- Correlation: >0.98
- Mean HARD: 4.2%
- Within Target: 96%
```

**Trace Elements (As, Ni, Co, Au):**
```
Good Scatter Plot (Trace Elements):
- Points: Moderate scatter (normal)
- 1:1 Line: Points evenly distributed
- Correlation: >0.90
- Mean HARD: 12.5%
- Within Target: 88%
```

**Warning Signs:**

⚠️ **Wide scatter**: Lower precision (may be normal for trace elements)
⚠️ **Systematic offset**: One value consistently higher/lower
⚠️ **Outliers**: May indicate sample heterogeneity

**Failure Patterns:**

❌ **Poor correlation (<0.80)**: Significant precision issues
❌ **Systematic bias**: Method or preparation issues
❌ **Many outliers**: Sample heterogeneity or method problems

### 3.3 RPD vs. HARD

**When to Use Which:**

- **RPD (Relative Percent Difference)**: Good for moderate to high concentrations
- **HARD (Half Absolute Relative Difference)**: Better for low concentrations, less sensitive to outliers

**Good RPD Values:**

| Element | Category | Good RPD | Excellent | Notes |
|---------|----------|----------|-----------|-------|
| Major Elements | All | < 10% | < 5% | Very good |
| Base Metals | pXRF | < 15% | < 10% | Field method |
| Trace Elements | ICP-MS | < 15% | < 10% | Good |
| Trace Elements | pXRF | < 20% | < 15% | Field method |

**Good HARD Values:**

| Element | Category | Good HARD | Excellent | Notes |
|---------|----------|-----------|-----------|-------|
| Major Elements | All | < 8% | < 5% | Very good |
| Base Metals | pXRF | < 15% | < 12% | Field method |
| Trace Elements | ICP-MS | < 15% | < 12% | Good |
| Trace Elements | pXRF | < 25% | < 20% | Field method |

---

## 4. Overall QAQC Summary

### 4.1 Good Overall Pass Rate

**Combined QAQC Pass Rate:**

| Analysis Type | Good | Excellent | Notes |
|--------------|------|-----------|-------|
| Gold (Fire Assay) | 88-92% | 92-96% | High precision |
| pXRF | 83-90% | 88-93% | Field method |
| ICP-MS | 88-93% | 92-96% | Excellent precision |
| ICP-OES | 92-96% | 95-98% | Very high precision |

**Calculation:**
- Overall Pass Rate = (Standards Pass + Blanks Pass + Duplicates Pass) / 3
- Each component weighted equally

### 4.2 Element-Specific Overall Summary

**Major Elements (Cu, Pb, Zn, Fe, S):**
- Standards: 95-98% pass
- Blanks: 98-100% pass
- Duplicates: 95-98% within target
- **Overall: 96-99%** ✅

**Trace Elements (As, Ni, Co, Au, Ag, Mo):**
- Standards: 85-95% pass
- Blanks: 95-100% pass
- Duplicates: 80-90% within target
- **Overall: 87-95%** ✅

**Base Metals (pXRF):**
- Standards: 85-95% pass
- Blanks: 90-98% pass
- Duplicates: 80-90% within target
- **Overall: 85-94%** ✅

---

## 5. Common Failure Patterns

### 5.1 Standards Failures

**Pattern 1: Systematic Bias**
- **Symptom**: All values consistently high or low
- **Cause**: Calibration drift, method bias
- **Solution**: Recalibrate, check method validation

**Pattern 2: High Scatter**
- **Symptom**: Many points outside limits, high RSD
- **Cause**: Method precision issues, matrix effects
- **Solution**: Review method, check matrix matching

**Pattern 3: Drift Trend**
- **Symptom**: Gradual increase or decrease over time
- **Cause**: Instrument drift, contamination buildup
- **Solution**: Recalibrate, clean instrument

**Pattern 4: Low Recovery**
- **Symptom**: Mean far from certified value
- **Cause**: Calibration error, method issues
- **Solution**: Recalibrate, validate method

### 5.2 Blanks Failures

**Pattern 1: Systematic Contamination**
- **Symptom**: All blanks elevated
- **Cause**: Contaminated reagents, preparation area
- **Solution**: Check reagents, clean preparation area

**Pattern 2: Progressive Contamination**
- **Symptom**: Blanks increasing over time
- **Cause**: Contamination buildup, carry-over
- **Solution**: Clean between samples, check procedures

**Pattern 3: Element-Specific Contamination**
- **Symptom**: One element consistently high
- **Cause**: Contaminated reagent for that element
- **Solution**: Check element-specific reagents

### 5.3 Duplicates Failures

**Pattern 1: Poor Precision**
- **Symptom**: High RPD/HARD, low within-target %
- **Cause**: Method precision limits, sample heterogeneity
- **Solution**: Accept if within expected range for element type

**Pattern 2: Systematic Bias**
- **Symptom**: One value consistently higher
- **Cause**: Method bias, preparation issues
- **Solution**: Check method, review preparation

**Pattern 3: Outliers**
- **Symptom**: Few pairs with very high RPD/HARD
- **Cause**: Sample heterogeneity (nugget effect)
- **Solution**: Accept if isolated, document if systematic

---

## 6. Troubleshooting Guide

### 6.1 Low Standards Pass Rate

**Checklist:**
- [ ] Are CRMs matrix-matched to samples?
- [ ] Is calibration current and valid?
- [ ] Are tolerances appropriate for element type?
- [ ] Is method validated and working correctly?
- [ ] Are there systematic biases?

**Actions:**
1. Review element-specific pass rates (may vary by element)
2. Check for systematic bias (all high or low)
3. Verify CRM matrix matches samples
4. Recalibrate if needed
5. Review method validation

### 6.2 High Blank Contamination

**Checklist:**
- [ ] Are reagents clean and fresh?
- [ ] Is preparation area clean?
- [ ] Are detection limits appropriate?
- [ ] Is there carry-over from previous samples?
- [ ] Are field blanks appropriate for conditions?

**Actions:**
1. Check reagent blanks
2. Review preparation procedures
3. Clean instrument/preparation area
4. Verify detection limits
5. Check for systematic contamination

### 6.3 Poor Duplicate Precision

**Checklist:**
- [ ] Are precision targets appropriate for element type?
- [ ] Is precision within expected range for method?
- [ ] Is there sample heterogeneity (nugget effect)?
- [ ] Are preparation procedures consistent?
- [ ] Is method precision validated?

**Actions:**
1. Check element-specific precision expectations
2. Review if within expected range for element type
3. Accept appropriate precision for trace elements
4. Check for sample heterogeneity
5. Review preparation procedures

---

## 7. Quick Reference: Good vs. Bad

### 7.1 Standards

| Metric | Good | Bad | Action |
|--------|------|-----|--------|
| Pass Rate (Major) | >95% | <90% | Investigate |
| Pass Rate (Trace) | >85% | <75% | Review |
| Recovery | 95-105% | <90% or >110% | Recalibrate |
| RSD (Major) | <10% | >15% | Review method |
| RSD (Trace) | <15% | >25% | Review method |

### 7.2 Blanks

| Metric | Good | Bad | Action |
|--------|------|-----|--------|
| Contamination Rate | <2% | >5% | Investigate |
| Max Value | <DL | >3×DL | Check contamination |
| Below DL % | >95% | <90% | Review procedures |

### 7.3 Duplicates

| Metric | Good | Bad | Action |
|--------|------|-----|--------|
| Within Target (Major) | >95% | <90% | Investigate |
| Within Target (Trace) | >80% | <70% | Review |
| Mean HARD (Major) | <8% | >12% | Review method |
| Mean HARD (Trace) | <15% | >25% | Review if systematic |
| Correlation | >0.90 | <0.80 | Investigate |

---

## 8. Visual Examples

### 8.1 Good Control Chart

**Characteristics:**
- Most points within ±2SD (green zone)
- Points evenly distributed
- Mean near certified value
- Low RSD
- Few outliers

**What to Look For:**
- Tight cluster around mean
- Even distribution
- No trends or patterns
- Recovery near 100%

### 8.2 Good Scatter Plot

**Major Elements:**
- Tight cluster around 1:1 line
- High correlation (>0.98)
- Even distribution
- Low HARD values

**Trace Elements:**
- Moderate scatter (normal)
- Good correlation (>0.90)
- Even distribution
- Acceptable HARD values

### 8.3 Good Blank Histogram

**Characteristics:**
- Peak at low values (near zero)
- Most values below detection limit
- Minimal right tail
- No outliers

**What to Look For:**
- Left-skewed distribution
- Most values <DL
- Few values above DL
- No contamination spikes

---

## 9. Summary

### Key Takeaways

1. **Element-Specific Expectations**: Major and trace elements have different QAQC requirements
2. **Method-Specific Precision**: pXRF has lower precision than lab methods (ICP, Fire Assay)
3. **Accept Appropriate Variability**: Trace elements have higher variability (normal)
4. **Use Element-Specific Settings**: Don't apply same tolerance to all elements
5. **Monitor Overall Trends**: Look for systematic issues, not just individual failures

### Good QAQC Checklist

- [ ] Standards pass rate appropriate for element type and method
- [ ] Blanks mostly below detection limit
- [ ] Duplicates within precision targets for element type
- [ ] No systematic biases or trends
- [ ] Element-specific settings applied correctly
- [ ] Overall pass rate meets expectations for method

---

## Additional Resources

- [pXRF Tutorial](docs/user/TUTORIAL_PXRF_BASE_METALS.md)
- [Multi-Element ICP Tutorial](docs/user/TUTORIAL_MULTIELEMENT_ICP.md)
- [Analysis Configuration Guide](docs/user/GUIDE_ANALYSIS_CONFIG.md)
- [QAQC Research Findings](docs/research/PXRF_MULTIELEMENT_QAQC_RESEARCH.md)
