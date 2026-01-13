# Quick Start Guide

Get up and running with the QAQC Report Generator in just a few minutes!

## Prerequisites

Before you begin, ensure you have:

- **Node.js** v18 or higher ([Download](https://nodejs.org/))
- **npm** v9 or higher (comes with Node.js)
- **Python 3.11+** (optional, for backend features) ([Download](https://www.python.org/))

To check your versions:
```bash
node --version
npm --version
python3 --version
```

## Installation

### React UI (Recommended)

The React UI is the modern, web-based interface. It's the easiest way to get started.

#### Step 1: Install Dependencies

```bash
cd react_ui
npm install
```

This installs all required packages (may take 2-3 minutes).

#### Step 2: Start the Application

```bash
npm run dev
```

The application will open in your browser at `http://localhost:5173` (or the next available port).

**That's it!** You're ready to use the application.

### PyQt Desktop GUI (Alternative)

If you prefer a traditional desktop application:

#### Step 1: Install Python Dependencies

```bash
# From project root
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Step 2: Launch the GUI

```bash
python3 launch_gui_simple.py
```

The desktop application window will open.

## Your First Analysis (5-Minute Tutorial)

Follow these steps to complete your first QAQC analysis:

### Step 1: Import Data

1. **Open the application** (React UI or PyQt GUI)
2. **Click "Data Import"** or use the drag-and-drop area
3. **Choose one of these options**:
   - **Option A**: Click a demo data button:
     - **"Gold Fire Assay"** - Gold analysis with Fire Assay method
     - **"PhotonAssay"** - Chrysos PhotonAssay gold analysis
     - **"pXRF Base Metals"** - Portable XRF base metals exploration data
     - **"Multi-Element ICP"** - ICP-MS/OES multi-element laboratory data
   - **Option B**: Drag and drop your own CSV/Excel file

**What happens**: The application reads your file and suggests column mappings.

**💡 Tip**: Start with demo data to learn the application! Each demo includes:
- Realistic QAQC samples (standards, blanks, duplicates)
- Pre-configured element-specific settings
- Expected results documented in tutorials

### Step 2: Map Your Columns

1. **Review the suggested mappings** (usually auto-detected correctly)
2. **Verify these columns are mapped**:
   - Sample ID → Your sample identifier column
   - Sample Type → Column with STD, BLK, UNK, etc.
   - Result → Your assay result column
3. **Click "Proceed"** or "Confirm Mapping"

**Tip**: If columns aren't detected, manually select them from the dropdowns.

### Step 3: Configure Analysis

1. **Select Analysis Category**:
   - Choose "Gold (Fire Assay)" for gold analysis
   - Choose "pXRF / Multi-element" for pXRF or multi-element ICP data
   - Choose "Chrysos PhotonAssay" for PhotonAssay data

2. **Configure Methodology**:
   - **Assay Method**: Select your lab method (e.g., Fire Assay, ICP-MS, pXRF)
   - **Analytical Method**: Automatically set based on category (can be overridden)
   - **Duplicate Type**: Choose Field Duplicate or Pulp Duplicate
   - **Insertion Rate**: How often QAQC samples are inserted (e.g., 5-10%)

3. **Set QAQC Rules**:
   - **Standards**: Select CRMs and set tolerance
     - **Element-specific tolerances** are automatically applied based on analytical method
     - Major elements (Cu, Pb, Zn, Fe, S): 5-10% tolerance
     - Trace elements (As, Ni, Co, Au): 10-20% tolerance
   - **Blanks**: Set detection limit (element-specific defaults applied)
   - **Duplicates**: Set precision target (element-specific defaults applied)

4. **Click "Run Analysis"**

**What happens**: The application processes your data and runs QAQC calculations.

### Step 4: Review Results

1. **View the Results Dashboard**:
   - **Summary Cards**: See total samples, standards, blanks, duplicates, and pass rate
   - **Tabs**: Switch between Standards, Blanks, and Duplicates
   - **Charts**: Interactive control charts, scatter plots, and histograms
   - **Tables**: Detailed results with pass/fail indicators

2. **Interpret the Results**:
   - **Green indicators**: Passing samples
   - **Red indicators**: Failing samples
   - **Charts**: Visual representation of data quality

### Step 5: Generate a Report

1. **Click "Create Report"** or navigate to Report section
2. **Choose Report Type**:
   - **Figures Only**: Charts and tables for presentations
   - **JORC Report**: Full analysis report with metadata
3. **Configure Report Options**:
   - Select which figures to include
   - Add report metadata (competent person, company, etc.)
4. **Click "Export"** and choose format:
   - **Excel (.xlsx)**: Detailed data and charts
   - **PDF (.pdf)**: Professional formatted report
   - **Word (.docx)**: Editable document

**Congratulations!** You've completed your first QAQC analysis.

## Next Steps

Now that you've completed your first analysis, here's what to explore:

### Learn More
- **[User Manual](USER_MANUAL.md)** - Comprehensive guide to all features
- **[Tutorials](TUTORIALS.md)** - Detailed walkthroughs for specific scenarios
- **[pXRF Base Metals Tutorial](TUTORIAL_PXRF_BASE_METALS.md)** - Complete pXRF analysis walkthrough
- **[Multi-Element ICP Tutorial](TUTORIAL_MULTIELEMENT_ICP.md)** - Complete ICP analysis walkthrough
- **[What Good Looks Like](WHAT_GOOD_LOOKS_LIKE.md)** - Visual guide to interpreting QAQC results
- **In-App Education Center** - Learn QAQC concepts (click "Learn" in sidebar)

### Common Tasks
- **Save Your Project**: Click "Save Project" to save your work as a `.qaqc` file
- **Load a Project**: Click "Open Project File" to resume previous work
- **Adjust Settings**: Click "Settings" to configure defaults
- **Browse CRMs**: Click "CRM Database" to view available reference materials

### Advanced Features
- **Custom Report Templates**: Edit JORC report templates
- **Batch Processing**: Process multiple files at once
- **Backend Integration**: Connect to Python backend for server-side analysis

## Troubleshooting

**Application won't start?**
- Check Node.js version: `node --version` (needs v18+)
- Try deleting `node_modules` and running `npm install` again
- Check for error messages in the terminal

**Can't import my file?**
- Ensure file is CSV or Excel format (.csv, .xlsx)
- Check that file isn't corrupted
- Try the demo data first to verify installation

**Analysis fails?**
- Verify column mappings are correct
- Check that Sample Type column contains STD, BLK, or UNK values
- Ensure Result column contains numeric values

**Need more help?**
- Check the [FAQ](FAQ.md)
- Review the [Troubleshooting section](USER_MANUAL.md#troubleshooting) in the User Manual

## Quick Reference

### Keyboard Shortcuts (React UI)
- `Ctrl/Cmd + S`: Save project
- `Ctrl/Cmd + O`: Open project
- `Esc`: Close modals/dialogs

### File Formats Supported
- **CSV**: Comma-separated values (.csv)
- **Excel**: Microsoft Excel (.xlsx, .xls)

### Required Columns
Your data file must have:
- **Sample ID**: Unique identifier for each sample
- **Sample Type**: STD (standard), BLK (blank), UNK (unknown/duplicate)
- **Result**: Numeric assay value

### Common Sample Types
- `STD` or `STD-*`: Standard/CRM samples
- `BLK` or `BLK-*`: Blank samples
- `UNK`, `DUP`, or sample pairs: Unknown/duplicate samples

---

**Ready for more?** → [User Manual](USER_MANUAL.md) | [Tutorials](TUTORIALS.md)
