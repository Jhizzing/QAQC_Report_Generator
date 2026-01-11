# QAQC Report Generator - User Manual

Complete reference guide for the QAQC Report Generator application.

## Table of Contents

1. [Introduction to QAQC Analysis](#introduction-to-qaqc-analysis)
2. [Application Overview](#application-overview)
3. [Workflow Guide](#workflow-guide)
4. [Features Reference](#features-reference)
5. [Settings & Configuration](#settings--configuration)
6. [Export Options](#export-options)
7. [Troubleshooting](#troubleshooting)
8. [Glossary](#glossary)

---

## Introduction to QAQC Analysis

### What is QAQC?

QAQC (Quality Assurance/Quality Control) is a systematic process used in mining and exploration to ensure laboratory data is accurate, precise, and reliable. It involves analyzing three types of samples:

1. **Standards (CRMs)**: Certified Reference Materials with known values
   - Purpose: Verify laboratory accuracy
   - Expected: Results should match certified values within tolerance

2. **Blanks**: Samples with no analyte (should be zero)
   - Purpose: Detect contamination
   - Expected: Results should be below detection limit

3. **Duplicates**: Paired samples from the same location
   - Purpose: Assess precision and sampling variability
   - Expected: Results should be similar (low RPD)

### Why QAQC Matters

QAQC analysis helps you:
- **Verify Data Quality**: Ensure your assay results are reliable
- **Detect Problems**: Identify laboratory errors or contamination early
- **Meet Standards**: Comply with JORC Code 2012 requirements
- **Make Decisions**: Confidently use data for resource estimation

### Key Metrics Explained

- **Z-Score**: Number of standard deviations from expected value
  - |Z| < 2: Acceptable
  - 2 ≤ |Z| < 3: Warning
  - |Z| ≥ 3: Failure

- **RPD (Relative Percent Difference)**: Precision measure for duplicates
  - RPD = |Original - Duplicate| / Mean × 100%
  - Lower is better (typically < 20% for good precision)

- **Pass Rate**: Percentage of samples passing QAQC criteria
  - Industry standard: ≥ 95% pass rate

---

## Application Overview

### Interface Options

The QAQC Report Generator offers three interfaces:

#### 1. React UI (Web-Based) - Recommended
- **Best for**: Most users, interactive workflows
- **Features**: Drag-and-drop, interactive charts, modern UI
- **Location**: `react_ui/` directory
- **Start**: `npm run dev` from `react_ui/` directory

#### 2. PyQt Desktop GUI
- **Best for**: Offline use, traditional desktop experience
- **Features**: Native desktop application, file dialogs
- **Location**: `src/gui/` directory
- **Start**: `python3 launch_gui_simple.py`

#### 3. Command Line Interface (CLI)
- **Best for**: Automation, batch processing, scripting
- **Features**: Terminal-based, scriptable
- **Location**: `main.py` in project root
- **Start**: `python main.py --help`

### Main Components

**React UI Components**:
- **Sidebar Navigation**: Quick access to all features
- **Workflow Stepper**: Visual progress indicator
- **Header**: Project management and save/load
- **Main Content Area**: Feature-specific interfaces

**Key Features**:
- Data Import with smart column mapping
- Analysis Setup wizards
- Interactive Results Dashboard
- Report Generation
- Project Persistence (.qaqc files)
- Settings Management
- CRM Database Browser
- Education Center

---

## Workflow Guide

### Complete Workflow Overview

The typical QAQC analysis workflow follows these steps:

```
1. Import Data → 2. Configure Analysis → 3. Run Analysis → 4. Review Results → 5. Generate Report
```

### Step-by-Step Workflow

#### Step 1: Import Data

**Location**: Data Import section (sidebar or workflow stepper)

**Options**:
1. **Drag & Drop**: Drag CSV/Excel files onto the upload area
2. **Click to Browse**: Click the upload area to select files
3. **Load Demo Data**: Use sample data to explore features

**What Happens**:
- File is read and parsed
- Column mapping is auto-detected
- Data preview is shown

**Column Mapping**:
- **Sample ID**: Unique identifier (required)
- **Sample Type**: STD, BLK, UNK, etc. (required)
- **Result**: Numeric assay value (required)
- **Elements**: Additional element columns (optional)

**Validation**:
- File format checked (CSV/XLSX)
- Required columns verified
- Data types validated
- Row count displayed

**Next**: Click "Proceed to Analysis Setup"

#### Step 2: Configure Analysis

**Location**: Analysis Setup section

**Sub-steps**:

**2.1 Select Analysis Category**
- **Gold (Fire Assay)**: For gold analysis
  - Default detection limit: 0.01 ppm
  - Suitable CRMs: OREAS, SRM series
- **pXRF / Multi-element**: For portable XRF or ICP-MS
  - Default detection limit: 1 ppm
  - Suitable for: Cu, Zn, Pb, etc.
- **Chrysos PhotonAssay**: For PhotonAssay data
  - High-energy X-ray analysis
  - Suitable for: Au, Ag, Cu

**2.2 Configure Methodology**
- **Assay Method**: Select laboratory method
  - Fire Assay (FA)
  - ICP-MS
  - AAS
  - Other
- **Duplicate Strategy**:
  - **Field Duplicate**: Samples taken at drill
  - **Pulp Duplicate**: Split from same pulp
- **Insertion Rate**: Frequency of QAQC samples (e.g., 5% = every 20th sample)

**2.3 Set QAQC Rules**

**Standards Configuration**:
- **Select CRMs**: Choose from available Certified Reference Materials
- **Tolerance Type**: Percentage or absolute
- **Tolerance Value**: Acceptable deviation (default: 10%)
- **Failure Threshold**: Max failures per batch (default: 3)

**Blanks Configuration**:
- **Detection Limit**: Maximum acceptable value (default: 0.01 ppm for gold)
- **Detection Limit Unit**: ppm, ppb, etc.
- **Contamination Multiplier**: Factor above DL to flag (default: 3×)

**Duplicates Configuration**:
- **Precision Target**: Target RPD (default: 20%)
- **Precision Method**: Hard limit or percentage-based
- **Failure Threshold**: Max failures per batch

**Next**: Click "Run Analysis"

#### Step 3: Run Analysis

**What Happens**:
- Data is processed and categorized
- Standards are matched to CRMs
- Blanks are checked for contamination
- Duplicates are paired and analyzed
- Statistics are calculated
- Results are displayed

**Processing Time**:
- Small files (< 1000 rows): < 1 second
- Medium files (1000-10000 rows): 1-5 seconds
- Large files (> 10000 rows): 5-30 seconds

**Progress Indicators**:
- Loading spinner during processing
- Status messages
- Error notifications if issues occur

**Next**: Results Dashboard appears automatically

#### Step 4: Review Results

**Location**: Results Dashboard

**Summary Cards**:
- **Total Samples**: All samples analyzed
- **Standards**: Number of CRM/standard samples
- **Blanks**: Number of blank samples
- **Duplicates**: Number of duplicate pairs
- **Overall Pass Rate**: Percentage passing all criteria

**Interactive Tabs**:

**Standards Tab**:
- **Control Chart**: Time-series plot with control limits
- **Statistics Table**: Mean, SD, RSD, pass rate per CRM
- **Flagged Batches**: Batches with failures
- **Z-Score Distribution**: Histogram of Z-scores

**Blanks Tab**:
- **Contamination Plot**: Sequential plot with detection limit
- **Statistics**: Max, mean, median, contamination rate
- **Flagged Blanks**: Samples exceeding limits
- **Distribution**: Histogram of blank values

**Duplicates Tab**:
- **Scatter Plot**: Original vs. Duplicate with 1:1 line
- **RPD Plot**: Precision plot with target envelope
- **Statistics**: Mean RPD, within target percentage
- **Flagged Pairs**: Pairs exceeding precision limits

**Data Tables**:
- Sortable columns
- Filterable rows
- Export to CSV
- Click rows to highlight on charts

**Next**: Click "Create Report" or navigate to Report section

#### Step 5: Generate Report

**Location**: Report Workflow section

**Report Types**:

**Figures Only**:
- Charts and tables
- Suitable for: Presentations, appendices
- Formats: DOCX, Excel

**JORC Report**:
- Complete analysis report
- Includes: Metadata, methodology, results, interpretation
- Suitable for: JORC-compliant reporting
- Formats: DOCX, PDF, Excel

**Configuration Options**:

**Report Metadata**:
- Competent Person name
- Company name
- Laboratory name
- Drilling company
- Sample type
- Comments

**Figure Options**:
- Include Control Charts: Yes/No
- Include Scatter Plots: Yes/No
- Include Histograms: Yes/No
- Include Summary Tables: Yes/No
- Figure size: Small, Medium, Large
- Color scheme: Default, Grayscale

**Export Formats**:
- **Excel (.xlsx)**: Multi-sheet workbook with data and charts
- **PDF (.pdf)**: Professional formatted report
- **Word (.docx)**: Editable document

**Next**: Click "Export" and choose format

---

## Features Reference

### Project Management

**Save Project**:
- Click "Save Project" in header
- Downloads `.qaqc` file
- Contains: Data, configuration, results, workflow state

**Load Project**:
- Click "Open Project File" in header or entry screen
- Select `.qaqc` file
- Restores complete project state

**Project Metadata**:
- Project name
- Deposit name
- Commodity type
- Campaign (optional)
- Created/modified dates

### Data Import Features

**Supported Formats**:
- CSV (Comma-Separated Values)
- Excel (.xlsx, .xls)

**Smart Column Mapping**:
- Auto-detects Sample ID, Type, Result columns
- Suggests element columns
- Manual override available

**Data Validation**:
- File format checking
- Required column verification
- Data type validation
- Empty row detection

**Large File Handling**:
- Chunked processing
- Progress indicators
- Memory-efficient loading

### Analysis Features

**Standards Analysis**:
- CRM matching
- Z-score calculation
- Bias calculation
- Pass/fail determination
- Batch statistics

**Blanks Analysis**:
- Contamination detection
- Detection limit checking
- Carry-over detection
- Statistical summary

**Duplicates Analysis**:
- Pair matching
- RPD calculation
- HARD (absolute difference) calculation
- Correlation analysis
- Precision metrics

### Visualization Features

**Control Charts**:
- Time-series plots
- Control limits (±2SD, ±3SD)
- Target line
- Interactive zoom/pan

**Scatter Plots**:
- Original vs. Duplicate
- 1:1 reference line
- Precision envelopes
- Point highlighting

**Histograms**:
- Distribution plots
- Bin customization
- Statistical overlays

**Synchronized Tables**:
- Click rows to highlight on charts
- Sortable columns
- Filterable data
- Export functionality

### Report Features

**Report Types**:
- Figures Only: Charts and tables
- JORC Report: Complete analysis report

**Customization**:
- Report title
- Logo inclusion
- Color schemes
- Font sizes
- Page layout (portrait/landscape)

**Export Formats**:
- Excel: Multi-sheet workbooks
- PDF: Professional formatted reports
- Word: Editable documents

### Settings Features

**Export Defaults**:
- Default format (PDF, Excel, DOCX)
- Figure resolution (150, 300, 600 DPI)
- Include cover page
- Include JORC table

**Analysis Defaults**:
- Standards tolerance (percentage)
- Precision target (percentage)
- Contamination multiplier
- Failure threshold

**Report Defaults**:
- Report title
- Logo URL
- Color scheme
- Font size
- Page layout
- Figure inclusion toggles

**API Settings**:
- Backend URL
- Auto-connect
- Health check interval

### CRM Database

**Browse CRMs**:
- View all available CRMs
- Search by name
- Filter by category
- View certified values
- Check expiry dates

**CRM Information**:
- Batch number
- Certified value
- Uncertainty
- Expiry date
- Matrix type
- Elements

### Education Center

**Topics Covered**:
- Graphs & Charts (Control charts, Bland-Altman, etc.)
- Assay Methods (Fire Assay, ICP-MS, etc.)
- Commodities (Gold, Silver, Copper, etc.)
- QAQC Concepts (Standards, Blanks, Duplicates)

**Features**:
- Search functionality
- Category filtering
- Topic cards with summaries
- Key points and examples

---

## Settings & Configuration

### Accessing Settings

**React UI**: Click "Settings" in sidebar or header menu

**PyQt GUI**: File → Settings

### Settings Categories

#### Export Defaults

Configure default export behavior:

- **Default Format**: PDF, Excel, or DOCX
- **Figure Resolution**: 150, 300, or 600 DPI
  - Higher DPI = better quality, larger file size
- **Include Cover Page**: Yes/No
- **Include JORC Table**: Yes/No

**When to Change**:
- If you always export in a specific format
- If you need high-resolution figures for publications
- If you want cover pages by default

#### Analysis Defaults

Set default QAQC thresholds:

- **Standards Tolerance (%)**: Default: 10%
  - Acceptable deviation from CRM value
- **Precision Target (%)**: Default: 20%
  - Target RPD for duplicates
- **Contamination Multiplier**: Default: 3×
  - Factor above detection limit to flag blanks
- **Failure Threshold**: Default: 3
  - Max failures per batch before flagging

**When to Change**:
- For different commodities (e.g., base metals may need higher tolerance)
- For different laboratories (some labs have tighter precision)
- For specific project requirements

#### Report Defaults

Configure default report appearance:

- **Report Title**: Default: "QAQC Analysis Report"
- **Logo URL**: URL or path to company logo
- **Color Scheme**: Default or Grayscale
- **Font Size**: Small, Medium, or Large
- **Page Layout**: Portrait or Landscape
- **Include Control Charts**: Yes/No
- **Include Scatter Plots**: Yes/No
- **Include Histograms**: Yes/No
- **Include Summary Tables**: Yes/No
- **Figure Title**: Default: "QAQC Figures"
- **Figure Size**: Small, Medium, or Large

**When to Change**:
- For company branding
- For specific report requirements
- For different output purposes (presentation vs. print)

#### API Settings

Configure backend connection (optional):

- **Backend URL**: Default: `http://localhost:8000`
- **Auto-connect**: Automatically connect to backend on startup
- **Health Check Interval**: How often to check backend (seconds)

**When to Change**:
- If using remote backend server
- If backend runs on different port
- To adjust connection checking frequency

### Saving Settings

Settings are automatically saved to browser local storage (React UI) or configuration file (PyQt GUI).

**Reset to Defaults**: Click "Reset to Defaults" button in Settings page.

---

## Export Options

### Export Formats

#### Excel (.xlsx)

**Best for**: Detailed data analysis, further processing

**Contents**:
- Multiple sheets (Summary, Standards, Blanks, Duplicates)
- Raw data tables
- Embedded charts
- Statistics summaries
- Pivot tables (if applicable)

**Use Cases**:
- Further analysis in Excel
- Data sharing
- Archival purposes

#### PDF (.pdf)

**Best for**: Professional reports, printing, sharing

**Contents**:
- Formatted report pages
- Embedded charts
- Summary tables
- Executive summary
- Methodology section

**Use Cases**:
- Final reports
- Presentations
- Printing
- Email sharing

#### Word (.docx)

**Best for**: Editable reports, custom formatting

**Contents**:
- Editable document
- Charts and tables
- Customizable formatting
- JORC-compliant structure

**Use Cases**:
- Reports requiring editing
- Custom formatting needs
- Integration with other documents

### Report Types

#### Figures Only

**Contents**:
- Selected charts (control charts, scatter plots, histograms)
- Summary tables
- Figure captions

**Best for**: Appendices, presentations, quick summaries

#### JORC Report

**Contents**:
- Cover page (if enabled)
- Executive summary
- Methodology section
- Results and interpretation
- All figures and tables
- Competent person information
- Company metadata

**Best for**: JORC-compliant reporting, formal documentation

### Customization Options

**Report Metadata**:
- Competent Person
- Company Name
- Laboratory
- Drilling Company
- Sample Type
- Comments

**Visual Options**:
- Color scheme (Default, Grayscale)
- Font size (Small, Medium, Large)
- Page layout (Portrait, Landscape)
- Logo inclusion

**Content Options**:
- Which figures to include
- Figure size
- Table inclusion
- Summary sections

---

## Troubleshooting

### Common Issues

#### Application Won't Start

**Symptoms**: Application doesn't launch or shows errors

**Solutions**:
1. Check Node.js version: `node --version` (needs v18+)
2. Delete `node_modules` and run `npm install` again
3. Check for error messages in terminal
4. Verify all dependencies installed: `npm install`
5. Try clearing browser cache (for React UI)

#### File Import Fails

**Symptoms**: File upload fails or shows errors

**Solutions**:
1. **Check file format**: Must be CSV or Excel (.csv, .xlsx)
2. **Check file size**: Very large files (> 50MB) may timeout
3. **Check file encoding**: Use UTF-8 encoding for CSV files
4. **Check file structure**: Ensure file has headers and data rows
5. **Try demo data**: Verify installation works with sample data
6. **Check file isn't corrupted**: Open file in Excel/LibreOffice first

#### Column Mapping Issues

**Symptoms**: Columns not detected or wrong columns mapped

**Solutions**:
1. **Manual mapping**: Use dropdowns to manually select columns
2. **Check column names**: Ensure Sample ID, Type, Result columns exist
3. **Check data types**: Result column must contain numbers
4. **Check Sample Type values**: Must contain STD, BLK, UNK, etc.
5. **Try renaming columns**: Use standard names (SampleID, Type, Result)

#### Analysis Fails

**Symptoms**: Analysis doesn't run or shows errors

**Solutions**:
1. **Check data quality**: Ensure numeric values in Result column
2. **Check Sample Types**: Must have STD, BLK, or duplicate pairs
3. **Check CRM selection**: Select at least one CRM for standards analysis
4. **Check thresholds**: Ensure tolerance values are reasonable
5. **Review error messages**: Check console/terminal for specific errors

#### Results Don't Make Sense

**Symptoms**: Results seem incorrect or unexpected

**Solutions**:
1. **Check data**: Verify imported data is correct
2. **Check configuration**: Review analysis settings
3. **Check CRM values**: Ensure correct CRMs selected
4. **Check Sample Types**: Verify STD/BLK/UNK classification
5. **Review statistics**: Check mean, SD values for reasonableness

#### Report Generation Fails

**Symptoms**: Export doesn't work or file is corrupted

**Solutions**:
1. **Check browser permissions**: Ensure downloads allowed
2. **Check disk space**: Ensure sufficient space for large reports
3. **Try different format**: Excel vs. PDF vs. DOCX
4. **Check report configuration**: Ensure valid settings
5. **Try smaller report**: Reduce figure count or data size

#### Backend Connection Issues

**Symptoms**: Backend not connecting or analysis fails

**Solutions**:
1. **Check backend running**: Verify API server is running
2. **Check URL**: Verify backend URL in settings
3. **Check port**: Ensure port 8000 (or configured port) is available
4. **Check firewall**: Ensure firewall allows connection
5. **Use client-side mode**: Application works without backend

### Performance Issues

#### Slow Analysis

**Causes**:
- Very large files (> 10,000 rows)
- Complex calculations
- Browser performance

**Solutions**:
- Use backend for large files (faster processing)
- Close other browser tabs
- Use more powerful computer
- Process files in batches

#### Slow File Import

**Causes**:
- Large file size
- Complex Excel files
- Browser limitations

**Solutions**:
- Use CSV instead of Excel for large files
- Split large files into smaller chunks
- Use backend upload for large files
- Close other applications

### Getting Help

**Documentation**:
- Check this User Manual
- Review [FAQ](FAQ.md)
- Read [Tutorials](TUTORIALS.md)

**In-App Help**:
- Education Center: Learn QAQC concepts
- Tooltips: Hover over icons/buttons
- Onboarding: First-time user guide

**Error Messages**:
- Read error messages carefully
- Check console/terminal for details
- Note error codes or messages
- Search FAQ for error-specific help

---

## Glossary

**Assay**: Laboratory analysis to determine element concentration

**Bias**: Systematic error in measurements (difference from true value)

**Blank**: Sample with no analyte, used to detect contamination

**Certified Reference Material (CRM)**: Standard with known, certified values

**Control Chart**: Time-series plot showing measurements against control limits

**Detection Limit (DL)**: Minimum concentration that can be reliably detected

**Duplicate**: Paired samples from same location to assess precision

**Field Duplicate**: Duplicate sample taken at drill site

**JORC Code**: Joint Ore Reserves Committee Code for reporting mineral resources

**Nugget Effect**: High variability in duplicate samples due to sample heterogeneity

**Pass Rate**: Percentage of samples passing QAQC criteria

**Precision**: Measure of reproducibility (how similar repeated measurements are)

**Pulp Duplicate**: Duplicate created by splitting same pulverized sample

**QAQC**: Quality Assurance/Quality Control

**Relative Percent Difference (RPD)**: Measure of precision: |A-B|/Mean × 100%

**Standard (STD)**: Certified Reference Material or standard sample

**Standard Deviation (SD)**: Measure of variability in data

**Z-Score**: Number of standard deviations a value is from the mean

---

**Need more help?** → [FAQ](FAQ.md) | [Tutorials](TUTORIALS.md)
