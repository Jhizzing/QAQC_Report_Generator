# QAQC Gap Analysis: Current vs. Recommended Implementation

## Executive Summary

This document compares the current QAQC implementation with industry best practices for pXRF and multi-element geochemistry, identifying gaps, misalignments, and missing features. Recommendations are prioritized for implementation.

## 1. Standards Analysis Gaps

### 1.1 Current Implementation

**Location**: `react_ui/src/features/analysis/standardsEngine.ts`

**Current Features:**
- Three tolerance types: percentage, absolute, SD-based
- Single tolerance value applied to all elements
- Pass/fail based on upper/lower limits
- Statistics calculation (mean, SD, RSD, pass rate)
- Consecutive failure detection

**Current Defaults:**
- Tolerance type: Percentage
- Tolerance value: 10% (from settings, category-dependent: 10-15% for pXRF/multi-element)
- Failure threshold: 3 consecutive failures

### 1.2 Recommended Implementation

**Industry Best Practices:**
- Element-specific tolerance thresholds
- Major vs. trace element distinction
- Method-specific tolerances (ICP-MS vs. ICP-OES vs. pXRF)
- Matrix-matched CRM validation
- Calibration verification separate from routine QAQC

**Recommended Tolerances by Element:**

| Element | Category | Current | Recommended | Gap |
|---------|----------|---------|-------------|-----|
| Au | Trace | 10% | 10-15% | ✓ Acceptable |
| Cu | Major | 10-15% | 5-10% | ✗ Too lenient |
| Pb | Major | 10-15% | 5-10% | ✗ Too lenient |
| Zn | Major | 10-15% | 5-10% | ✗ Too lenient |
| Fe | Major | 10-15% | 3-5% | ✗ Too lenient |
| S | Major | 10-15% | 5-10% | ✗ Too lenient |
| As | Trace | 10-15% | 15-20% | ✓ Acceptable |
| Ni | Trace | 10-15% | 10-15% | ✓ Acceptable |
| Co | Trace | 10-15% | 15-20% | ✓ Acceptable |

### 1.3 Identified Gaps

**Critical Gaps:**
1. **No element-specific tolerances**: Single tolerance applied to all elements
2. **No major vs. trace distinction**: Same tolerance for major (>1%) and trace (<0.1%) elements
3. **No method-specific tolerances**: No consideration of analytical method (ICP-MS, ICP-OES, pXRF)
4. **No matrix matching validation**: No check if selected CRMs match sample matrix

**Medium Priority Gaps:**
1. **No calibration verification mode**: Can't distinguish calibration checks from routine QAQC
2. **Limited tolerance types**: Missing concentration-dependent tolerances (hyperbolic)
3. **No Westgard rules**: Mentioned in config but not implemented in analysis engine

**Low Priority Gaps:**
1. **No bias detection**: No systematic bias calculation or tracking
2. **No recovery percentage tracking**: Recovery calculated but not used for bias detection

### 1.4 Recommendations

**Priority 1 (Critical):**
1. Implement element-specific tolerance configuration
2. Add major vs. trace element classification
3. Add method-specific tolerance presets

**Priority 2 (High):**
1. Add matrix matching validation/guidance
2. Implement calibration verification mode
3. Add concentration-dependent tolerance options

**Priority 3 (Medium):**
1. Implement Westgard rules (from config.yaml)
2. Add bias detection and tracking
3. Enhance recovery percentage analysis

## 2. Blanks Analysis Gaps

### 2.1 Current Implementation

**Location**: `react_ui/src/features/analysis/blanksEngine.ts`

**Current Features:**
- Detection limit configuration
- Contamination threshold (detection limit × multiplier)
- Three-tier status: pass, warning, fail
- Statistics calculation (max, mean, median, contamination rate)

**Current Defaults:**
- Detection limit: 0.01 ppm (gold), 1 ppm (pXRF/multi-element)
- Contamination multiplier: 3× (from settings)
- Unit: ppm (category-dependent)

### 2.2 Recommended Implementation

**Industry Best Practices:**
- Element-specific detection limits
- Method-specific detection limits
- Concentration-dependent contamination thresholds
- Carry-over detection (mentioned in config but not implemented)

**Recommended Detection Limits by Element:**

| Element | Method | Current | Recommended | Gap |
|---------|--------|---------|-------------|-----|
| Au | Fire Assay | 0.01 ppm | 0.01 ppm | ✓ Correct |
| Cu | ICP-MS | 1 ppm | 1 ppm | ✓ Correct |
| Pb | ICP-MS | 1 ppm | 0.5 ppm | ✗ Too high |
| Zn | ICP-MS | 1 ppm | 1 ppm | ✓ Correct |
| As | ICP-MS | 1 ppm | 2 ppm | ✓ Acceptable |
| Fe | ICP-OES | 1 ppm | 0.01% (100 ppm) | ✗ Wrong unit/scale |
| S | ICP-OES | 1 ppm | 0.01% (100 ppm) | ✗ Wrong unit/scale |

### 2.3 Identified Gaps

**Critical Gaps:**
1. **No element-specific detection limits**: Single detection limit for all elements
2. **No method-specific detection limits**: Same limit for ICP-MS, ICP-OES, pXRF
3. **Unit confusion for major elements**: Fe and S should use % not ppm for detection limits
4. **No carry-over detection**: Mentioned in config.yaml but not implemented

**Medium Priority Gaps:**
1. **No concentration-dependent thresholds**: Contamination threshold is fixed multiplier
2. **No blank type distinction**: Field blank vs. lab blank vs. method blank

**Low Priority Gaps:**
1. **Limited statistics**: Could add more detailed contamination analysis
2. **No trend detection**: No detection of increasing contamination over time

### 2.4 Recommendations

**Priority 1 (Critical):**
1. Implement element-specific detection limits
2. Add method-specific detection limit presets
3. Fix unit handling for major elements (Fe, S use %, not ppm)
4. Implement carry-over detection (from config.yaml)

**Priority 2 (High):**
1. Add blank type classification
2. Implement concentration-dependent contamination thresholds
3. Add trend detection for contamination

**Priority 3 (Medium):**
1. Enhance statistics and reporting
2. Add contamination source identification

## 3. Duplicates Analysis Gaps

### 3.1 Current Implementation

**Location**: `react_ui/src/features/analysis/duplicatesEngine.ts`

**Current Features:**
- RPD (Relative Percent Difference) calculation
- HARD (Half Absolute Relative Difference) calculation
- Precision method selection (RPD or HARD)
- Single precision target for all elements
- Statistics calculation (mean RPD, mean HARD, within target %)

**Current Defaults:**
- Precision target: 20% (from settings)
- Precision method: HARD (from settings)
- Failure threshold: 3 consecutive failures

### 3.2 Recommended Implementation

**Industry Best Practices:**
- Element-specific precision targets
- Major vs. trace element distinction
- Method-specific precision expectations
- Concentration-dependent precision (hyperbolic mentioned in config but not implemented)
- Field duplicate vs. pulp duplicate distinction

**Recommended Precision Targets by Element:**

| Element | Category | Current | Recommended RPD | Recommended HARD | Gap |
|---------|----------|---------|-----------------|------------------|-----|
| Au | Trace | 20% | 15-20% | 10-15% | ✓ Acceptable |
| Cu | Major | 20% | 5-10% | 5-8% | ✗ Too lenient |
| Pb | Major | 20% | 5-10% | 5-8% | ✗ Too lenient |
| Zn | Major | 20% | 5-10% | 5-8% | ✗ Too lenient |
| Fe | Major | 20% | 3-5% | 3-5% | ✗ Too lenient |
| S | Major | 20% | 5-10% | 5-8% | ✗ Too lenient |
| As | Trace | 20% | 15-20% | 12-18% | ✓ Acceptable |
| Ni | Trace | 20% | 10-15% | 8-12% | ✗ Too lenient |
| Co | Trace | 20% | 15-20% | 12-18% | ✓ Acceptable |

### 3.3 Identified Gaps

**Critical Gaps:**
1. **No element-specific precision targets**: Single target (20%) for all elements
2. **No major vs. trace distinction**: Same precision expected for major and trace elements
3. **No method-specific precision**: No consideration of analytical method
4. **Hyperbolic precision not implemented**: Mentioned in config.yaml but not in analysis engine

**Medium Priority Gaps:**
1. **No duplicate type distinction**: Field duplicate vs. pulp duplicate
2. **Limited precision methods**: Only RPD and HARD, missing other methods
3. **No concentration-dependent precision**: Precision should vary with concentration

**Low Priority Gaps:**
1. **No correlation analysis**: Correlation threshold mentioned in config but not used
2. **No nugget ratio calculation**: Nugget ratio threshold mentioned but not implemented

### 3.4 Recommendations

**Priority 1 (Critical):**
1. Implement element-specific precision targets
2. Add major vs. trace element classification
3. Add method-specific precision presets
4. Implement hyperbolic precision method (from config.yaml)

**Priority 2 (High):**
1. Add duplicate type classification (field vs. pulp)
2. Implement concentration-dependent precision
3. Add correlation analysis

**Priority 3 (Medium):**
1. Implement nugget ratio calculation
2. Add additional precision methods if needed
3. Enhance statistics and reporting

## 4. pXRF-Specific Gaps

### 4.1 Current Implementation

**Location**: `react_ui/src/features/analysis/MethodologyWizard.tsx`

**Current Features:**
- pXRF category selection
- Matrix correction toggle (mentioned but not implemented)
- Spectral interference toggle (mentioned but not implemented)
- Target elements selection

**Current Gaps:**
- Matrix correction: Toggle exists but no implementation
- Spectral interference: Toggle exists but no implementation
- No pXRF-specific analysis logic
- No element-specific detection limits for pXRF
- No moisture/particle size considerations

### 4.2 Recommended Implementation

**Industry Best Practices:**
- Matrix correction algorithms
- Spectral interference detection and flagging
- Element-specific detection limits for pXRF
- Calibration verification procedures
- Moisture and particle size considerations

### 4.3 Identified Gaps

**Critical Gaps:**
1. **No matrix correction**: Toggle exists but no implementation
2. **No spectral interference detection**: Toggle exists but no implementation
3. **No pXRF-specific detection limits**: Uses generic multi-element limits
4. **No calibration verification mode**: Can't distinguish calibration from routine QAQC

**Medium Priority Gaps:**
1. **No moisture content handling**: No consideration of moisture effects
2. **No particle size considerations**: No particle size effect correction
3. **No pXRF-specific precision targets**: Uses generic targets

**Low Priority Gaps:**
1. **No instrument-specific settings**: No pXRF instrument model considerations
2. **No analysis mode selection**: No distinction between major and trace element modes

### 4.4 Recommendations

**Priority 1 (Critical):**
1. Implement matrix correction algorithms (or at least flagging)
2. Implement spectral interference detection
3. Add pXRF-specific detection limits
4. Add calibration verification workflow

**Priority 2 (High):**
1. Add moisture content input/consideration
2. Add particle size input/consideration
3. Implement pXRF-specific precision targets

**Priority 3 (Medium):**
1. Add instrument-specific settings
2. Add analysis mode selection

## 5. CRM Database Gaps

### 5.1 Current Implementation

**Location**: `react_ui/src/data/crmDatabase.ts`

**Current Coverage:**
- Gold CRMs: 14 entries (good)
- Multi-element CRMs: 10 entries (moderate)
- pXRF CRMs: 6 entries (limited)

**Current Features:**
- CRM lookup by ID
- CRM lookup by category
- Certified value lookup by element
- Uncertainty values included

### 5.2 Recommended Implementation

**Industry Best Practices:**
- Comprehensive CRM coverage for all matrix types
- Matrix type classification
- Element coverage documentation
- Supplier information
- Availability and expiry tracking

### 5.3 Identified Gaps

**Critical Gaps:**
1. **Limited USGS standards**: Only G-2 and NIST 2711a
2. **Missing common standards**: USGS AGV-1, BCR-1 not included
3. **Limited pXRF CRMs**: Only 6 pXRF-specific CRMs
4. **No matrix type filtering**: Can't filter CRMs by matrix type

**Medium Priority Gaps:**
1. **No CANMET standards**: Canadian standards not included
2. **Limited carbonate CRMs**: Only mentioned in recommendations, not in database
3. **No soil-specific CRMs**: Limited soil/sediment coverage beyond NIST

**Low Priority Gaps:**
1. **No expiry date tracking**: No way to track CRM expiry
2. **No supplier contact information**: Limited supplier details
3. **No element coverage summary**: Can't easily see which elements are covered

### 5.4 Recommendations

**Priority 1 (Critical):**
1. Add USGS AGV-1 and BCR-1 standards
2. Expand pXRF CRM database
3. Add matrix type classification and filtering

**Priority 2 (High):**
1. Add CANMET standards (if available)
2. Add more carbonate CRMs
3. Expand soil/sediment CRM coverage

**Priority 3 (Medium):**
1. Add expiry date tracking
2. Enhance supplier information
3. Add element coverage summaries

## 6. Configuration and Settings Gaps

### 6.1 Current Implementation

**Location**: 
- `react_ui/src/stores/settingsStore.ts`
- `config.yaml`
- `react_ui/src/features/analysis/QAQCRuleConfig.tsx`

**Current Features:**
- Category-based defaults (gold, pXRF, multi-element)
- Configurable tolerance, detection limits, precision targets
- Settings persistence

### 6.2 Identified Gaps

**Critical Gaps:**
1. **No element-specific configuration**: Can't set tolerances per element
2. **No method-specific presets**: No ICP-MS vs. ICP-OES vs. pXRF presets
3. **Limited category customization**: Can't easily customize category defaults

**Medium Priority Gaps:**
1. **No matrix-specific settings**: No settings for different matrix types
2. **No project-specific presets**: Can't save project-specific QAQC configurations

**Low Priority Gaps:**
1. **Limited validation**: No validation of configuration values
2. **No configuration templates**: No pre-built templates for common scenarios

### 6.3 Recommendations

**Priority 1 (Critical):**
1. Add element-specific configuration UI
2. Add method-specific preset selection
3. Enhance category customization

**Priority 2 (High):**
1. Add matrix-specific settings
2. Add project-specific configuration presets

**Priority 3 (Medium):**
1. Add configuration validation
2. Add configuration templates

## 7. Documentation Gaps

### 7.1 Current Documentation

**Location**: `docs/user/`

**Current Coverage:**
- User manual
- Quick start guide
- Analysis configuration guide
- Tutorials
- FAQ

### 7.2 Identified Gaps

**Critical Gaps:**
1. **No pXRF-specific guidance**: Limited pXRF best practices
2. **No element-specific guidance**: No guidance on element-specific tolerances
3. **No matrix matching guidance**: Limited guidance on CRM selection

**Medium Priority Gaps:**
1. **No method-specific guidance**: Limited guidance on ICP method differences
2. **No troubleshooting guide**: Limited troubleshooting information

**Low Priority Gaps:**
1. **No advanced topics**: Limited advanced QAQC topics
2. **No case studies**: No real-world examples

### 7.3 Recommendations

**Priority 1 (Critical):**
1. Add pXRF-specific user guide
2. Add element-specific tolerance guidance
3. Add matrix matching guide

**Priority 2 (High):**
1. Add method-specific guidance
2. Add troubleshooting guide

**Priority 3 (Medium):**
1. Add advanced topics documentation
2. Add case studies

## 8. Priority Summary

### 8.1 Critical Priority (Implement First)

1. **Element-specific tolerances and precision targets**
   - Standards: Element-specific tolerance configuration
   - Duplicates: Element-specific precision targets
   - Blanks: Element-specific detection limits

2. **Major vs. trace element distinction**
   - Classification logic
   - Different tolerances for major vs. trace

3. **Method-specific presets**
   - ICP-MS, ICP-OES, pXRF presets
   - Method-specific defaults

4. **pXRF-specific features**
   - Matrix correction (at least flagging)
   - Spectral interference detection
   - pXRF-specific detection limits

5. **CRM database expansion**
   - Add USGS AGV-1, BCR-1
   - Expand pXRF CRMs
   - Add matrix type classification

### 8.2 High Priority (Implement Second)

1. **Carry-over detection** (from config.yaml)
2. **Hyperbolic precision method** (from config.yaml)
3. **Westgard rules** (from config.yaml)
4. **Matrix matching validation/guidance**
5. **Calibration verification mode**
6. **Unit fixes for major elements** (Fe, S use % not ppm)

### 8.3 Medium Priority (Implement Third)

1. **Configuration templates**
2. **Project-specific presets**
3. **Enhanced statistics and reporting**
4. **Correlation analysis** (duplicates)
5. **Nugget ratio calculation** (duplicates)
6. **Documentation enhancements**

## 9. Implementation Roadmap

### Phase 1: Critical Gaps (Weeks 1-4)

**Week 1-2: Element-Specific Configuration**
- Add element-specific tolerance configuration UI
- Implement element-specific tolerance logic in standards engine
- Add element classification (major vs. trace)

**Week 2-3: Method-Specific Presets**
- Create method-specific preset system
- Implement ICP-MS, ICP-OES, pXRF presets
- Update configuration UI

**Week 3-4: pXRF Enhancements**
- Implement spectral interference detection
- Add pXRF-specific detection limits
- Add matrix correction flagging (if full implementation not possible)

### Phase 2: High Priority Gaps (Weeks 5-8)

**Week 5-6: Config Implementation**
- Implement carry-over detection
- Implement hyperbolic precision method
- Implement Westgard rules

**Week 6-7: CRM Database**
- Add USGS AGV-1, BCR-1
- Expand pXRF CRM database
- Add matrix type classification

**Week 7-8: Unit Fixes and Validation**
- Fix unit handling for major elements
- Add matrix matching validation
- Add calibration verification mode

### Phase 3: Medium Priority (Weeks 9-12)

**Week 9-10: Enhanced Features**
- Add configuration templates
- Add project-specific presets
- Enhance statistics and reporting

**Week 10-11: Advanced Analysis**
- Implement correlation analysis
- Implement nugget ratio calculation
- Add trend detection

**Week 11-12: Documentation**
- Update user documentation
- Add pXRF-specific guides
- Add troubleshooting guide

## 10. Conclusion

The current QAQC implementation provides a solid foundation but requires significant enhancements to align with industry best practices for pXRF and multi-element geochemistry. The most critical gaps are:

1. **Element-specific configuration**: Currently uses single values for all elements
2. **Major vs. trace distinction**: No differentiation between element types
3. **Method-specific presets**: No consideration of analytical method
4. **pXRF-specific features**: Matrix correction and spectral interference not implemented
5. **CRM database**: Limited coverage, especially for pXRF and USGS standards

Addressing these gaps will significantly improve the application's alignment with industry standards and user needs for geochemical QAQC analysis.
