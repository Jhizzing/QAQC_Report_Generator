# Analysis Configuration Guide

Complete guide to configuring your QAQC analysis settings.

## Table of Contents

1. [Category Selection](#category-selection)
2. [Methodology Configuration](#methodology-configuration)
3. [QAQC Rules Setup](#qaqc-rules-setup)
4. [CRM Selection](#crm-selection)
5. [Threshold Configuration](#threshold-configuration)
6. [Best Practices](#best-practices)

---

## Category Selection

### Available Categories

#### Gold (Fire Assay)

**Best for**: Gold analysis using fire assay method

**Default Settings**:
- Detection Limit: 0.01 ppm
- Suitable CRMs: OREAS series, SRM series
- Typical Tolerance: 10%

**When to Use**:
- Gold exploration projects
- Fire assay laboratory data
- High-precision gold analysis

**Characteristics**:
- Low detection limits
- High precision requirements
- Standard CRMs available

#### pXRF / Multi-element

**Best for**: Portable XRF or ICP-MS multi-element data

**Default Settings**:
- Detection Limit: 1 ppm
- Suitable CRMs: Multi-element CRMs
- Typical Tolerance: 10-15%

**When to Use**:
- Base metal exploration
- Multi-element analysis
- Portable XRF data
- ICP-MS data

**Characteristics**:
- Higher detection limits
- Multiple elements
- Variable precision by element

#### Chrysos PhotonAssay

**Best for**: PhotonAssay high-energy X-ray analysis

**Default Settings**:
- Detection Limit: 0.01 ppm (gold)
- Suitable CRMs: Gold CRMs
- Typical Tolerance: 10%

**When to Use**:
- PhotonAssay laboratory data
- High-throughput gold analysis
- Non-destructive analysis

**Characteristics**:
- Fast analysis
- Non-destructive
- High precision

### Selecting the Right Category

**Consider**:
1. **Commodity**: What element(s) are you analyzing?
2. **Method**: What laboratory method was used?
3. **Precision**: What precision is required?
4. **Standards**: What CRMs are available?

**If Unsure**:
- Start with category closest to your data
- Adjust thresholds as needed
- Review results and refine

---

## Methodology Configuration

### Assay Method

Select the laboratory method used:

**Fire Assay (FA)**:
- Traditional gold analysis
- High precision
- Suitable for: Gold, Silver, PGEs

**ICP-MS**:
- Inductively Coupled Plasma Mass Spectrometry
- Multi-element analysis
- Suitable for: Most elements

**AAS**:
- Atomic Absorption Spectroscopy
- Single element analysis
- Suitable for: Base metals

**Other**:
- Custom methods
- Specify in comments if needed

### Duplicate Type

**Field Duplicate**:
- Two samples taken at drill site
- Assesses: Sampling + Analytical precision
- Higher variability expected
- Typical RPD: 20-25%

**Pulp Duplicate**:
- Same sample split into two pulps
- Assesses: Analytical precision only
- Lower variability expected
- Typical RPD: 10-15%

**Choosing**:
- Use Field Duplicate if duplicates taken at drill
- Use Pulp Duplicate if duplicates from same pulp
- Field duplicates show total variability
- Pulp duplicates show analytical precision only

### Insertion Rate

**Definition**: Percentage of samples that are QAQC samples

**Common Rates**:
- **5%**: Standard practice (1 in 20 samples)
- **10%**: High-quality projects (1 in 10 samples)
- **20%**: Very high-quality projects (1 in 5 samples)

**Calculation**:
- Insertion Rate = (QAQC samples / Total samples) × 100%
- Example: 50 QAQC samples / 1000 total = 5%

**Setting**:
- Enter as percentage (e.g., 5.0 for 5%)
- Used for reporting and statistics
- Doesn't affect analysis calculations

---

## QAQC Rules Setup

### Standards Configuration

**Purpose**: Monitor laboratory accuracy using Certified Reference Materials

#### Selecting CRMs

**How to Select**:
1. **Browse CRM Database**: Click "Browse CRMs" or use CRM Database
2. **Search**: Enter CRM name (e.g., "OREAS")
3. **Filter**: Filter by category (Gold, Base Metals, etc.)
4. **Select**: Check boxes for relevant CRMs
5. **Review**: Check certified values and expiry dates

**Best Practices**:
- **Select 2-3 CRMs**: Cover your grade range
- **Match grade range**: Select CRMs near your sample grades
- **Check expiry dates**: Ensure CRMs are current
- **Verify matrix**: Ensure matrix type is appropriate

**Example**:
- Low-grade project (0.1-1 ppm Au): Select OREAS 101 (0.5 ppm)
- High-grade project (5-50 ppm Au): Select OREAS 102 (10 ppm)
- Wide range: Select multiple CRMs covering range

#### Tolerance Settings

**Tolerance Type**:
- **Percentage**: Relative tolerance (e.g., 10% of certified value)
- **Absolute**: Fixed tolerance (e.g., ±0.1 ppm)

**Tolerance Value**:
- **Gold**: 10% is typical
- **Base Metals**: 10-15% depending on element
- **Multi-element**: May be higher (15-20%)

**Setting Tolerance**:
- Start with default (10%)
- Adjust based on:
  - Laboratory precision
  - Project requirements
  - Industry standards
  - Commodity characteristics

**Failure Threshold**:
- Maximum failures per batch before flagging
- Default: 3 failures
- Adjust based on batch size and requirements

### Blanks Configuration

**Purpose**: Detect contamination in blank samples

#### Detection Limit

**Definition**: Maximum acceptable value for blank samples

**Default Values**:
- **Gold (Fire Assay)**: 0.01 ppm
- **Multi-element (ICP)**: 1 ppm
- **Adjust based on**: Laboratory capabilities, method detection limits

**Setting Detection Limit**:
- Enter numeric value
- Select unit (ppm, ppb, %)
- Should match laboratory detection limit
- Lower is better (more sensitive)

#### Contamination Multiplier

**Definition**: Factor above detection limit to flag contamination

**Default**: 3× detection limit

**Example**:
- Detection Limit: 0.01 ppm
- Contamination Multiplier: 3×
- Flag if blank > 0.03 ppm

**Setting**:
- Default: 3× (recommended)
- Higher: Less sensitive (fewer flags)
- Lower: More sensitive (more flags)

**Best Practice**: Use 3× unless specific requirements

### Duplicates Configuration

**Purpose**: Assess precision using duplicate sample pairs

#### Precision Target

**Definition**: Target RPD (Relative Percent Difference) for duplicates

**Default Values**:
- **Field Duplicates**: 20% RPD
- **Pulp Duplicates**: 15% RPD

**Setting Precision Target**:
- Enter as percentage (e.g., 20 for 20%)
- Adjust based on:
  - Duplicate type (field vs. pulp)
  - Commodity characteristics
  - Project requirements
  - Industry standards

**Typical Values**:
- **Gold (Field)**: 20-25%
- **Gold (Pulp)**: 10-15%
- **Base Metals (Field)**: 20-30%
- **Base Metals (Pulp)**: 15-20%

#### Precision Method

**Hard Limit**:
- Fixed RPD threshold
- All samples must meet target
- Simple and clear

**Percentage-Based**:
- Variable threshold based on grade
- Lower grades allow higher RPD
- More realistic for low-grade samples

**Recommendation**: Use Hard Limit for simplicity

#### Failure Threshold

**Definition**: Maximum failures per batch before flagging

**Default**: 3 failures

**Setting**:
- Adjust based on batch size
- Larger batches: Higher threshold
- Smaller batches: Lower threshold

---

## CRM Selection

### Accessing CRM Database

**From Analysis Setup**:
1. Click "Standards" tab
2. Click "Browse CRMs" button
3. CRM Database opens

**From Sidebar**:
1. Click "CRM Database" in sidebar
2. Browse all available CRMs

### Understanding CRM Information

**Batch Number**: Unique identifier for CRM batch

**Certified Value**: Accepted true value for the CRM

**Uncertainty**: Range of uncertainty in certified value (± value)

**Expiry Date**: Date after which CRM may not be valid

**Matrix**: Material type (e.g., Gold Ore, Soil, Sediment)

**Elements**: Elements certified in the CRM

### Selecting Appropriate CRMs

**Grade Range Matching**:
- Select CRMs near your sample grades
- Low-grade samples: Use low-grade CRMs
- High-grade samples: Use high-grade CRMs
- Wide range: Use multiple CRMs

**Expiry Date Checking**:
- Ensure CRMs are current (not expired)
- Expired CRMs may not be valid
- Check expiry dates before selecting

**Matrix Verification**:
- Ensure matrix type is appropriate
- Gold ore CRMs for gold ore samples
- Soil CRMs for soil samples
- Match matrix to sample type

**Multiple CRMs**:
- Use 2-3 CRMs covering your range
- Provides better quality control
- Detects grade-dependent issues

### CRM Best Practices

- **Select current CRMs**: Check expiry dates
- **Match grade range**: Select CRMs near your grades
- **Use multiple CRMs**: 2-3 CRMs recommended
- **Verify matrix**: Ensure appropriate matrix type
- **Document selection**: Note which CRMs used and why

---

## Threshold Configuration

### Understanding Thresholds

**Thresholds define**:
- Acceptable ranges for results
- Pass/fail criteria
- Quality control limits

**Types of Thresholds**:
- **Standards**: Tolerance from certified value
- **Blanks**: Detection limit and contamination multiplier
- **Duplicates**: Precision target (RPD)

### Setting Appropriate Thresholds

**Consider**:
1. **Laboratory capabilities**: What precision can lab achieve?
2. **Project requirements**: What quality is required?
3. **Industry standards**: What are typical thresholds?
4. **Commodity characteristics**: What's realistic for this element?

**Starting Points**:
- Use defaults as starting point
- Adjust based on results
- Document changes and reasons

### Adjusting Thresholds

**If Too Many Failures**:
- Check if thresholds too strict
- Review laboratory performance
- Consider adjusting thresholds (if justified)
- Document reasons for changes

**If Too Few Failures**:
- Check if thresholds too lenient
- Verify data quality
- Consider tightening thresholds
- Ensure quality standards met

**Best Practice**: Start with defaults, adjust only if justified

---

## Best Practices

### Configuration Workflow

1. **Select Category**: Choose appropriate category
2. **Configure Methodology**: Set method and duplicate type
3. **Select CRMs**: Choose 2-3 appropriate CRMs
4. **Set Thresholds**: Use defaults or adjust as needed
5. **Review Settings**: Verify all settings correct
6. **Run Analysis**: Execute analysis
7. **Review Results**: Check if thresholds appropriate
8. **Adjust if Needed**: Refine based on results

### Documentation

**Document Your Configuration**:
- Note which CRMs selected and why
- Record threshold values and reasons
- Note any adjustments made
- Keep configuration records for reports

### Consistency

**Use Consistent Settings**:
- Same settings across batches
- Document any changes
- Explain reasons for changes
- Maintain quality standards

### Quality Assurance

**Verify Configuration**:
- Double-check CRM selection
- Verify threshold values
- Ensure settings appropriate for data
- Review before running analysis

---

**Next Steps**: After configuring analysis, proceed to [Results Interpretation Guide](GUIDE_RESULTS.md)

**Need help?** → [FAQ](FAQ.md) | [User Manual](USER_MANUAL.md)
