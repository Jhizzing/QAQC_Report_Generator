# pXRF and Multi-Element Geochemistry QAQC Research Findings

## Executive Summary

This document summarizes research findings on best practices for pXRF (portable X-ray Fluorescence) and multi-element geochemistry QAQC processes. The research identifies key differences between pXRF and traditional laboratory methods, element-specific precision requirements, and industry standards for quality control in geochemical exploration.

## 1. pXRF QAQC Best Practices

### 1.1 Matrix Effects and Correction

**Key Findings:**
- pXRF measurements are highly sensitive to matrix effects (composition, density, particle size, moisture content)
- Matrix-matched CRMs are essential for accurate calibration and validation
- Correction algorithms should be applied to account for:
  - Absorption effects (high Z elements absorbing low-energy X-rays)
  - Enhancement effects (secondary fluorescence)
  - Particle size effects (finer particles = better precision)
  - Moisture content (affects density and X-ray transmission)

**Industry Practice:**
- Use CRMs with matrix composition similar to samples
- Apply matrix correction factors based on certified standards analyzed alongside samples
- Software tools (e.g., Isogonal Geo pXRF Correction) can assist with correction calculations

**Current Implementation Gap:**
- Matrix correction is mentioned in MethodologyWizard but not implemented in analysis engines
- No particle size or moisture content considerations

### 1.2 Spectral Interference

**Key Findings:**
- pXRF suffers from spectral overlaps that can cause false positives/negatives
- Common interferences:
  - Pb L-lines overlap with As K-lines
  - Zn K-lines can interfere with Cu measurements
  - Fe can interfere with multiple elements
  - Rare earth elements have complex overlapping spectra

**Industry Practice:**
- Check for known spectral interferences during analysis
- Flag potential interference issues when elements are co-located
- Use element-specific detection limits that account for interference

**Current Implementation Gap:**
- Spectral interference checking is mentioned but not implemented
- No element-specific interference detection

### 1.3 Element-Specific Detection Limits and Precision

**Key Findings:**
- Detection limits vary significantly by element and concentration
- Typical pXRF detection limits (approximate):
  - Major elements (Fe, Ca, K, Ti): 0.01-0.1%
  - Base metals (Cu, Pb, Zn): 5-50 ppm
  - Trace elements (As, Ni, Co): 10-100 ppm
  - Light elements (Na, Mg, Al): Poor detection, often not reliable

**Precision Requirements:**
- Major elements (>1%): 5-10% RPD acceptable
- Base metals (0.1-1%): 10-15% RPD acceptable
- Trace elements (<0.1%): 15-25% RPD acceptable
- Lower concentrations require higher tolerance

**Current Implementation Gap:**
- Single tolerance value (10-15%) applied to all elements
- No element-specific detection limits
- No distinction between major and trace elements

### 1.4 Calibration Verification

**Key Findings:**
- pXRF instruments require regular calibration verification using CRMs
- Calibration should be checked:
  - At start of each session
  - After instrument warm-up period
  - When analyzing different matrix types
  - When switching between major and trace element modes

**Industry Practice:**
- Analyze 2-3 CRMs covering the concentration range of interest
- Verify CRM results are within ±2SD of certified values
- Document calibration checks in QAQC records

**Current Implementation:**
- Standards analysis exists but doesn't distinguish calibration checks from routine QAQC

### 1.5 Field vs. Lab pXRF QAQC

**Key Findings:**
- Field pXRF: More variable conditions, requires more frequent checks
- Lab pXRF: More controlled conditions, can use more sophisticated corrections
- Both require matrix-matched CRMs and regular calibration verification

**Industry Practice:**
- Field: Check CRMs every 20-50 samples
- Lab: Check CRMs every 50-100 samples
- Both: Analyze blanks and duplicates at standard rates (5-10%)

## 2. Multi-Element Geochemistry QAQC

### 2.1 Element-Specific Tolerance Thresholds

**Key Findings:**
- Different elements require different precision targets based on:
  - Analytical method (ICP-MS vs. ICP-OES vs. AAS)
  - Concentration level (major vs. trace)
  - Geological variability (nugget effect for some elements)

**Industry-Accepted Precision Targets:**

| Element | Method | Major/Trace | Typical RPD Target | Notes |
|---------|--------|-------------|-------------------|-------|
| Au | Fire Assay | Trace | 10-15% | Nugget effect common |
| Cu | ICP-MS/OES | Major | 5-10% | Good precision expected |
| Pb | ICP-MS/OES | Major | 5-10% | Good precision expected |
| Zn | ICP-MS/OES | Major | 5-10% | Good precision expected |
| As | ICP-MS | Trace | 15-20% | Lower precision acceptable |
| Ni | ICP-MS/OES | Trace | 10-15% | Moderate precision |
| Co | ICP-MS | Trace | 15-20% | Lower precision acceptable |
| Fe | ICP-OES | Major | 3-5% | Very good precision |
| S | ICP-OES | Major | 5-10% | Good precision |

**Current Implementation Gap:**
- Single precision target (20% RPD) for all elements
- No method-specific considerations
- No distinction between major and trace elements

### 2.2 Major vs. Trace Elements

**Key Findings:**
- Major elements (>1%): Require higher precision (5-10% RPD)
- Trace elements (<0.1%): Acceptable precision varies (10-25% RPD)
- Transition zone (0.1-1%): Intermediate precision (10-15% RPD)

**Industry Practice:**
- Apply stricter tolerances to major elements
- Allow more lenient tolerances for trace elements
- Consider geological variability (nugget effect) for some elements

**Current Implementation Gap:**
- No distinction between major and trace elements
- Same tolerance applied regardless of concentration

### 2.3 ICP Method Differences

**Key Findings:**
- **ICP-MS**: Best for trace elements, lower detection limits, higher precision for low concentrations
- **ICP-OES**: Best for major elements, higher precision for high concentrations, faster analysis
- **AAS**: Older method, still used for specific elements, moderate precision

**Precision Expectations:**
- ICP-MS trace elements: 10-20% RPD
- ICP-OES major elements: 3-10% RPD
- AAS: 10-15% RPD (method dependent)

**Current Implementation Gap:**
- No method-specific precision targets
- No consideration of analytical method in QAQC rules

### 2.4 Matrix-Matched Standards

**Key Findings:**
- CRMs should match sample matrix for best accuracy
- Different matrices require different CRMs:
  - Silicate rocks: USGS standards (G-2, AGV-1, BCR-1)
  - Sulfide ores: OREAS VMS standards, CDN GS series
  - Carbonates: Limestone/dolomite CRMs
  - Soils/sediments: NIST soil standards

**Industry Practice:**
- Select 2-3 CRMs covering:
  - Concentration range of samples
  - Matrix type of samples
  - Elements of interest

**Current Implementation:**
- CRM selection exists but no matrix matching guidance
- Limited CRM database coverage

## 3. Industry Standards and Guidelines

### 3.1 JORC Code Requirements

**Key Findings:**
- JORC Code requires QAQC documentation for all analytical data
- Standards: Minimum 5% insertion rate
- Blanks: Minimum 5% insertion rate
- Duplicates: Minimum 5% insertion rate
- Check assays: Minimum 5% insertion rate
- Total QAQC: Minimum 20% insertion rate

**pXRF Specific:**
- JORC recognizes pXRF as a valid analytical method
- Requires documentation of:
  - Calibration procedures
  - Matrix effects and corrections
  - Detection limits by element
  - Precision and accuracy validation

**Current Implementation:**
- Insertion rate tracking exists in config
- No JORC-specific reporting or validation

### 3.2 NI 43-101 Requirements

**Key Findings:**
- Similar to JORC but with additional emphasis on:
  - Method validation
  - Laboratory accreditation (ISO 17025)
  - Chain of custody
  - Data verification

**Current Implementation:**
- No NI 43-101 specific features

### 3.3 ISO 17025

**Key Findings:**
- Laboratory accreditation standard
- Requires:
  - Documented QAQC procedures
  - Regular calibration verification
  - Method validation
  - Uncertainty estimation
  - Traceability to certified standards

**Current Implementation:**
- QAQC procedures exist but not fully documented for ISO compliance

## 4. Recommended QAQC Thresholds by Element

### 4.1 Standards (CRM) Tolerances

| Element | Category | Tolerance Type | Tolerance Value | Notes |
|---------|----------|----------------|-----------------|-------|
| Au | Trace | Percentage | 10-15% | Fire assay, nugget effect |
| Cu | Major | Percentage | 5-10% | Good precision expected |
| Pb | Major | Percentage | 5-10% | Good precision expected |
| Zn | Major | Percentage | 5-10% | Good precision expected |
| Ag | Trace | Percentage | 10-15% | Moderate precision |
| As | Trace | Percentage | 15-20% | Lower precision acceptable |
| Fe | Major | Percentage | 3-5% | Very good precision |
| S | Major | Percentage | 5-10% | Good precision |
| Ni | Trace | Percentage | 10-15% | Moderate precision |
| Co | Trace | Percentage | 15-20% | Lower precision acceptable |
| Mo | Trace | Percentage | 10-15% | Moderate precision |

### 4.2 Blanks Detection Limits

| Element | Method | Typical Detection Limit | Contamination Threshold |
|---------|--------|------------------------|------------------------|
| Au | Fire Assay | 0.01 ppm | 0.03 ppm (3×) |
| Cu | ICP-MS | 1 ppm | 3 ppm (3×) |
| Pb | ICP-MS | 0.5 ppm | 1.5 ppm (3×) |
| Zn | ICP-MS | 1 ppm | 3 ppm (3×) |
| As | ICP-MS | 2 ppm | 6 ppm (3×) |
| Fe | ICP-OES | 0.01% | 0.03% (3×) |
| S | ICP-OES | 0.01% | 0.03% (3×) |

### 4.3 Duplicates Precision Targets

| Element | Category | RPD Target | HARD Target | Notes |
|---------|----------|------------|-------------|-------|
| Au | Trace | 15-20% | 10-15% | Nugget effect |
| Cu | Major | 5-10% | 5-8% | Good precision |
| Pb | Major | 5-10% | 5-8% | Good precision |
| Zn | Major | 5-10% | 5-8% | Good precision |
| Ag | Trace | 10-15% | 8-12% | Moderate precision |
| As | Trace | 15-20% | 12-18% | Lower precision |
| Fe | Major | 3-5% | 3-5% | Very good precision |
| S | Major | 5-10% | 5-8% | Good precision |
| Ni | Trace | 10-15% | 8-12% | Moderate precision |
| Co | Trace | 15-20% | 12-18% | Lower precision |

## 5. Key Recommendations

### 5.1 Immediate Improvements

1. **Element-Specific Tolerances**: Implement element-specific tolerance thresholds for standards analysis
2. **Major vs. Trace Distinction**: Add logic to distinguish major and trace elements
3. **Method-Specific Precision**: Consider analytical method in precision targets
4. **Matrix Matching Guidance**: Add UI guidance for selecting matrix-matched CRMs

### 5.2 Medium-Term Enhancements

1. **Matrix Correction**: Implement matrix correction algorithms for pXRF
2. **Spectral Interference Detection**: Add spectral interference checking
3. **Element-Specific Detection Limits**: Configure detection limits by element
4. **Calibration Verification**: Distinguish calibration checks from routine QAQC

### 5.3 Long-Term Enhancements

1. **Method Validation**: Add method validation features
2. **Uncertainty Estimation**: Calculate and report measurement uncertainties
3. **ISO 17025 Compliance**: Add features for ISO compliance documentation
4. **Advanced Statistics**: Implement Westgard rules, CUSUM charts, etc.

## 6. References

- OREAS Certified Reference Materials: https://www.oreas.com/
- USGS Geochemical Reference Materials: https://www.usgs.gov/
- International Association of Geoanalysts: https://www.geoanalyst.org/
- JORC Code 2012 Edition
- NI 43-101 Standards of Disclosure for Mineral Projects
- ISO/IEC 17025:2017 General requirements for the competence of testing and calibration laboratories

## 7. Conclusion

The current QAQC implementation provides a solid foundation but requires enhancements to align with industry best practices for pXRF and multi-element geochemistry. Key improvements include element-specific tolerances, matrix correction for pXRF, and better distinction between major and trace elements. The recommended thresholds and practices documented here should guide future development priorities.
