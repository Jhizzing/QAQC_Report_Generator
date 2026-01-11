# QAQC Report Generator - Tutorials

Step-by-step tutorials for common QAQC analysis scenarios.

## Table of Contents

1. [Tutorial 1: Gold Fire Assay Analysis](#tutorial-1-gold-fire-assay-analysis)
2. [Tutorial 2: Multi-element Analysis (pXRF/ICP)](#tutorial-2-multi-element-analysis-pxrficp)
3. [Tutorial 3: Batch Processing Multiple Files](#tutorial-3-batch-processing-multiple-files)
4. [Tutorial 4: Custom Report Templates](#tutorial-4-custom-report-templates)
5. [Tutorial 5: Using CRM Database](#tutorial-5-using-crm-database)
6. [Tutorial 6: Advanced Settings Configuration](#tutorial-6-advanced-settings-configuration)

---

## Tutorial 1: Gold Fire Assay Analysis

**Objective**: Complete a full QAQC analysis for gold fire assay data.

**Time**: 10-15 minutes

**Prerequisites**: Gold fire assay data in CSV or Excel format

### Step 1: Prepare Your Data

Ensure your data file has:
- **Sample ID** column (e.g., "SampleID", "Sample_ID")
- **Sample Type** column with values: STD, BLK, UNK (or similar)
- **Result** column with numeric gold values (e.g., "Au_ppm", "Gold")

**Example data structure**:
```
SampleID,Type,Au_ppm
STD-001,STD,1.25
BLK-001,BLK,0.008
UNK-001,UNK,2.45
UNK-002,UNK,2.38
```

### Step 2: Import Data

1. **Open the application** (React UI or PyQt GUI)
2. **Navigate to Data Import**
3. **Upload your file**:
   - Drag and drop your CSV/Excel file, OR
   - Click to browse and select file
4. **Review column mapping**:
   - Verify Sample ID → your Sample ID column
   - Verify Sample Type → your Type column
   - Verify Result → your Au_ppm column
5. **Click "Proceed to Analysis Setup"**

### Step 3: Configure Analysis

**3.1 Select Category**:
- Click **"Gold (Fire Assay)"**
- This sets appropriate defaults for gold analysis

**3.2 Configure Methodology**:
- **Assay Method**: Select "Fire Assay"
- **Duplicate Type**: 
  - Choose "Field Duplicate" if duplicates taken at drill
  - Choose "Pulp Duplicate" if duplicates from same pulp
- **Insertion Rate**: Enter 5.0 (if 5% of samples are QAQC)

**3.3 Set QAQC Rules**:

**Standards Tab**:
1. Click "Standards" tab
2. **Select CRMs**: 
   - Check boxes for relevant CRMs (e.g., OREAS 101, OREAS 102)
   - Or search for specific CRMs
3. **Tolerance**: 
   - Type: Percentage
   - Value: 10% (default, adjust if needed)
4. **Failure Threshold**: 3 (max failures per batch)

**Blanks Tab**:
1. Click "Blanks" tab
2. **Detection Limit**: 0.01 ppm (default for gold)
3. **Unit**: ppm
4. **Contamination Multiplier**: 3 (flags blanks > 3× DL)

**Duplicates Tab**:
1. Click "Duplicates" tab
2. **Precision Target**: 20% RPD (default)
3. **Precision Method**: Hard limit
4. **Failure Threshold**: 3

**3.4 Run Analysis**:
- Click "Run Analysis" button
- Wait for processing (usually < 5 seconds)

### Step 4: Review Results

**4.1 Check Summary**:
- **Total Samples**: Should match your data
- **Standards**: Count of STD samples
- **Blanks**: Count of BLK samples
- **Duplicates**: Count of duplicate pairs
- **Overall Pass Rate**: Should be ≥ 95% for good data

**4.2 Review Standards Tab**:
- **Control Chart**: 
  - Points should cluster around target line
  - Most points within ±2SD bands
  - Red points indicate failures
- **Statistics Table**:
  - Check pass rate per CRM
  - Review mean, SD, RSD values
- **Flagged Batches**: Review any batches with failures

**4.3 Review Blanks Tab**:
- **Contamination Plot**:
  - Points should be below detection limit line
  - Red points indicate contamination
- **Statistics**:
  - Max value should be < detection limit
  - Contamination rate should be low (< 5%)

**4.4 Review Duplicates Tab**:
- **Scatter Plot**:
  - Points should cluster along 1:1 line
  - Green points = passing, Red = failing
- **RPD Plot**:
  - Points should be within precision envelope
  - Lower grades may have higher RPD (normal)
- **Statistics**:
  - Mean RPD should be < 20%
  - Within target percentage should be high

### Step 5: Generate Report

1. **Click "Create Report"**
2. **Select Report Type**:
   - **Figures Only**: For quick summaries
   - **JORC Report**: For complete analysis
3. **Configure Options**:
   - Add competent person name
   - Add company name
   - Select figures to include
4. **Export**:
   - Click "Export Figures (DOCX)" or "Export JORC Report"
   - Choose format: Excel, PDF, or DOCX
   - File downloads automatically

### Expected Results

**Good QAQC Results**:
- Pass rate ≥ 95%
- Standards within ±2SD
- Blanks below detection limit
- Duplicates with RPD < 20%

**Action Items if Failures**:
- Review flagged samples
- Check for laboratory issues
- Consider re-assaying failed samples
- Document failures in report

---

## Tutorial 2: Multi-element Analysis (pXRF/ICP)

**Objective**: Analyze multi-element data from pXRF or ICP-MS.

**Time**: 10-15 minutes

**Prerequisites**: Multi-element data with multiple element columns

### Step 1: Prepare Your Data

Your data should have:
- Sample ID column
- Sample Type column (STD, BLK, UNK)
- Multiple element columns (e.g., Cu_ppm, Zn_ppm, Pb_ppm)

**Example structure**:
```
SampleID,Type,Cu_ppm,Zn_ppm,Pb_ppm
STD-001,STD,1250,850,450
BLK-001,BLK,2,1,0.5
UNK-001,UNK,980,720,380
```

### Step 2: Import and Map Data

1. **Import your file**
2. **Map columns**:
   - Sample ID → SampleID
   - Sample Type → Type
   - Result → Select primary element (e.g., Cu_ppm)
   - Elements → Map additional elements (Zn_ppm, Pb_ppm, etc.)

**Note**: The application analyzes one element at a time. You'll need to run separate analyses for each element, or the application may process all elements if configured.

### Step 3: Configure Analysis

**3.1 Select Category**:
- Click **"pXRF / Multi-element"**
- This sets defaults for multi-element analysis

**3.2 Configure Methodology**:
- **Assay Method**: Select appropriate method (ICP-MS, AAS, etc.)
- **Duplicate Type**: Field or Pulp
- **Insertion Rate**: Your QAQC insertion rate

**3.3 Set QAQC Rules**:

**Standards**:
- Select CRMs appropriate for your elements
- Tolerance: 10-15% (may be higher for multi-element)
- Adjust based on element and method

**Blanks**:
- Detection Limit: 1 ppm (default for multi-element)
- Adjust per element if needed
- Contamination Multiplier: 3

**Duplicates**:
- Precision Target: 20-25% (may be higher for multi-element)
- Hard limit method

### Step 4: Review Results

Review results for each element:
- Check pass rates
- Review control charts
- Assess precision
- Identify any element-specific issues

### Step 5: Generate Report

Generate comprehensive report with all elements analyzed.

---

## Tutorial 3: Batch Processing Multiple Files

**Objective**: Process multiple assay files efficiently.

**Time**: 15-20 minutes

### Method 1: Sequential Processing (Manual)

1. **Process first file**:
   - Import, configure, analyze, export
   - Save project as `Project1.qaqc`

2. **Process second file**:
   - Create new project
   - Import second file
   - Configure and analyze
   - Export

3. **Repeat** for additional files

### Method 2: Using CLI (Automated)

**Batch process directory**:
```bash
python main.py --input data/ --output results/ \
  --infer-mapping --normalize-results --yes \
  --output-format excel
```

**Process specific files**:
```bash
python main.py --input file1.csv file2.csv file3.csv \
  --output results/ --infer-mapping --yes
```

### Method 3: Project Templates

1. **Create template project**:
   - Configure analysis settings once
   - Save as `Template.qaqc`

2. **Load template for each file**:
   - Open template project
   - Import new data file
   - Settings are already configured
   - Run analysis and export

### Tips for Batch Processing

- **Standardize file formats**: Use consistent column names
- **Save configurations**: Reuse analysis settings
- **Organize output**: Use descriptive file names
- **Document changes**: Note any file-specific adjustments

---

## Tutorial 4: Custom Report Templates

**Objective**: Customize JORC report templates for your needs.

**Time**: 20-30 minutes

### Step 1: Access Template Editor

1. **Navigate to Template Editor**:
   - Click "Templates" in sidebar (if available)
   - Or access from Report Workflow

### Step 2: Understand Template Structure

Templates consist of:
- **Sections**: Major report sections (e.g., Executive Summary, Methodology)
- **Blocks**: Content blocks within sections (e.g., paragraphs, tables, figures)
- **Properties**: Styling and formatting options

### Step 3: Customize Template

**Add Section**:
1. Click "Add Section"
2. Enter section name
3. Choose section type

**Add Block**:
1. Select section
2. Click "Add Block"
3. Choose block type (text, table, figure, etc.)
4. Configure content

**Reorder Elements**:
- Drag and drop to reorder sections/blocks
- Use up/down arrows

**Edit Properties**:
- Select element
- Edit properties panel
- Adjust formatting, styling

### Step 4: Save Template

1. Click "Save Template"
2. Enter template name
3. Template saved for future use

### Step 5: Use Custom Template

1. When generating report
2. Select your custom template
3. Report uses your template structure

### Example Customizations

**Add Company Logo**:
- Add image block
- Upload logo file
- Position in header

**Custom Sections**:
- Add "Project Background" section
- Add "Geological Context" section
- Add "Recommendations" section

**Custom Formatting**:
- Adjust font sizes
- Change color scheme
- Modify page layout

---

## Tutorial 5: Using CRM Database

**Objective**: Browse and select appropriate CRMs for your analysis.

**Time**: 5-10 minutes

### Step 1: Access CRM Database

1. **Navigate to CRM Database**:
   - Click "CRM Database" in sidebar
   - Or access from Analysis Setup → Standards tab

### Step 2: Browse CRMs

**View All CRMs**:
- See complete list of available CRMs
- Information includes:
  - Batch number
  - Certified value
  - Uncertainty
  - Expiry date
  - Matrix type
  - Elements

**Filter by Category**:
- Click category filter (Gold, Base Metals, etc.)
- View CRMs for specific commodity

**Search CRMs**:
- Enter search term (e.g., "OREAS")
- Filter results by name

### Step 3: Select CRMs for Analysis

1. **Review CRM Information**:
   - Check certified values match your grade range
   - Verify expiry dates (should be current)
   - Confirm matrix type is appropriate

2. **Select CRMs**:
   - Check boxes for relevant CRMs
   - Or click "Select" button

3. **CRMs Added to Analysis**:
   - Selected CRMs appear in Standards configuration
   - Used for standards analysis

### Step 4: Understand CRM Information

**Certified Value**: The accepted true value for the CRM

**Uncertainty**: Range of uncertainty in certified value

**Expiry Date**: Date after which CRM may not be valid

**Matrix**: Material type (e.g., Gold Ore, Soil, Sediment)

**Elements**: Elements certified in the CRM

### Best Practices

- **Select Multiple CRMs**: Use 2-3 CRMs covering your grade range
- **Check Expiry Dates**: Ensure CRMs are current
- **Match Grade Range**: Select CRMs near your sample grades
- **Verify Matrix**: Ensure matrix type is appropriate

---

## Tutorial 6: Advanced Settings Configuration

**Objective**: Configure application defaults for your workflow.

**Time**: 10-15 minutes

### Step 1: Access Settings

1. **Navigate to Settings**:
   - Click "Settings" in sidebar
   - Or use keyboard shortcut

### Step 2: Configure Export Defaults

**Default Format**:
- Choose your most-used format (PDF, Excel, DOCX)
- Saves time on each export

**Figure Resolution**:
- **150 DPI**: For screen viewing, smaller files
- **300 DPI**: For printing, good quality (recommended)
- **600 DPI**: For high-quality printing, larger files

**Cover Page**:
- Enable if you always want cover pages
- Disable for quick reports

**JORC Table**:
- Enable for JORC-compliant reports
- Disable for simple summaries

### Step 3: Configure Analysis Defaults

**Standards Tolerance**:
- Default: 10%
- Adjust based on:
  - Commodity (gold vs. base metals)
  - Laboratory precision
  - Project requirements

**Precision Target**:
- Default: 20% RPD
- Adjust based on:
  - Sample type (field vs. pulp duplicates)
  - Commodity characteristics
  - Project standards

**Contamination Multiplier**:
- Default: 3× detection limit
- Adjust based on:
  - Detection limit accuracy
  - Laboratory capabilities
  - Project requirements

**Failure Threshold**:
- Default: 3 failures per batch
- Adjust based on:
  - Batch size
  - Quality requirements
  - Risk tolerance

### Step 4: Configure Report Defaults

**Report Title**:
- Set default title (e.g., "QAQC Analysis Report")
- Or leave blank to customize each time

**Logo URL**:
- Add company logo URL or path
- Logo included in reports

**Color Scheme**:
- Default: Colorful charts
- Grayscale: For printing

**Font Size**:
- Small: More content per page
- Medium: Balanced (recommended)
- Large: Easier reading

**Page Layout**:
- Portrait: Standard reports
- Landscape: Wide charts/tables

**Figure Options**:
- Set defaults for which figures to include
- Can override when generating reports

### Step 5: Configure API Settings (Optional)

**Backend URL**:
- Default: `http://localhost:8000`
- Change if using remote backend

**Auto-connect**:
- Enable to automatically connect to backend
- Disable for manual connection

**Health Check Interval**:
- How often to check backend status (seconds)
- Default: 30 seconds

### Step 6: Save and Test

1. **Settings auto-save**: Changes saved immediately
2. **Test defaults**: Create new analysis to verify
3. **Reset if needed**: Click "Reset to Defaults"

### Tips

- **Start with defaults**: Use defaults first, adjust as needed
- **Document changes**: Note why you changed defaults
- **Project-specific**: Some projects may need different defaults
- **Team consistency**: Share settings with team for consistency

---

**Need more help?** → [User Manual](USER_MANUAL.md) | [FAQ](FAQ.md)
