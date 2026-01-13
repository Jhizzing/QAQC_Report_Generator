# Example Projects

This directory contains example QAQC project files (.qaqc) with pre-configured settings for different analysis types.

## Available Examples

### pXRF Base Metals Example
**File**: `pxrf_base_metals_example.qaqc` (to be created)

**Configuration:**
- Category: pXRF
- Analytical Method: pXRF
- Selected CRMs: OREAS-100, OREAS-101a, OREAS-102a
- Element-specific tolerances:
  - Cu: 12%
  - Pb: 12%
  - Zn: 12%
  - Fe: 8%
  - As: 20%
  - Mn, Rb, Sr: 15%

**Use Case**: Base metals exploration using portable XRF

**Tutorial**: See [pXRF Base Metals Tutorial](../docs/user/TUTORIAL_PXRF_BASE_METALS.md)

### Multi-Element ICP Example
**File**: `multielement_icp_example.qaqc` (to be created)

**Configuration:**
- Category: Multi-element
- Analytical Method: ICP-MS
- Selected CRMs: OREAS-201, OREAS-202, OREAS-400
- Element-specific tolerances:
  - Major elements (Cu, Pb, Zn, Fe, S): 5-10%
  - Trace elements (Ni, Co, As, Mo, Ag, Au): 10-20%

**Use Case**: Multi-element geochemistry from ICP-MS/OES laboratory analysis

**Tutorial**: See [Multi-Element ICP Tutorial](../docs/user/TUTORIAL_MULTIELEMENT_ICP.md)

## How to Use Example Projects

### Method 1: Load Demo Data and Save

1. **Load Demo Data**:
   - Open the application
   - Click "pXRF Base Metals" or "Multi-Element ICP" demo button
   - Configure analysis settings (or use defaults)
   - Run analysis

2. **Save as Example Project**:
   - Click "Save Project"
   - Save to this `examples/` directory
   - Name it appropriately (e.g., `pxrf_base_metals_example.qaqc`)

3. **Load Example Project**:
   - Click "Open Project File"
   - Navigate to `examples/` directory
   - Select the example project file
   - All settings and data are restored

### Method 2: Use Pre-Configured Settings

1. **Load Demo Data** (as above)
2. **Configure Settings** using the recommended values from tutorials
3. **Run Analysis**
4. **Save Project** for future reference

## Recommended Settings

### pXRF Base Metals

**Standards:**
- Tolerance Type: Percentage
- Default Tolerance: 15%
- Element-Specific: Enabled (automatically applied)
- Selected CRMs: OREAS-100, OREAS-101a, OREAS-102a

**Blanks:**
- Detection Limit: 10 ppm (default, element-specific applied)
- Contamination Multiplier: 3×

**Duplicates:**
- Precision Method: HARD
- Default Precision: 20% HARD (element-specific applied)

### Multi-Element ICP

**Standards:**
- Tolerance Type: Percentage
- Default Tolerance: 10%
- Element-Specific: Enabled (automatically applied)
- Selected CRMs: OREAS-201, OREAS-202, OREAS-400

**Blanks:**
- Detection Limit: 1 ppm (default, element-specific applied)
- Contamination Multiplier: 3×

**Duplicates:**
- Precision Method: HARD
- Default Precision: 12% HARD (element-specific applied)

## Creating Your Own Examples

You can create example projects for your specific workflows:

1. **Set up analysis** with your preferred settings
2. **Run analysis** with demo or real data
3. **Save project** to this directory
4. **Document** the example in this README

## Notes

- Example projects include all configuration but may not include actual data (data is loaded separately)
- Settings are preserved and can be reused
- Element-specific settings are automatically applied based on analytical method
- See tutorials for detailed interpretation of results

## Related Documentation

- [pXRF Base Metals Tutorial](../docs/user/TUTORIAL_PXRF_BASE_METALS.md)
- [Multi-Element ICP Tutorial](../docs/user/TUTORIAL_MULTIELEMENT_ICP.md)
- [What Good Looks Like](../docs/user/WHAT_GOOD_LOOKS_LIKE.md)
- [Analysis Configuration Guide](../docs/user/GUIDE_ANALYSIS_CONFIG.md)
