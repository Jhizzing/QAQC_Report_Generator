# Data Import Guide

Complete guide to importing and mapping your assay data.

## Table of Contents

1. [Supported File Formats](#supported-file-formats)
2. [Preparing Your Data](#preparing-your-data)
3. [Import Process](#import-process)
4. [Column Mapping](#column-mapping)
5. [Data Validation](#data-validation)
6. [Handling Errors](#handling-errors)
7. [Tips for Large Files](#tips-for-large-files)

---

## Supported File Formats

### CSV Files (.csv)

**Requirements**:
- Comma-separated values
- UTF-8 encoding (recommended)
- Headers in first row
- Data rows below headers

**Example CSV structure**:
```csv
SampleID,Type,Au_ppm,Ag_ppm
STD-001,STD,1.25,15.8
BLK-001,BLK,0.008,0.1
UNK-001,UNK,2.45,18.2
```

**Common Issues**:
- **Wrong delimiter**: Use comma, not semicolon or tab
- **Encoding issues**: Save as UTF-8
- **Extra commas**: Quote text fields that contain commas
- **Empty rows**: Remove completely empty rows

### Excel Files (.xlsx)

**Requirements**:
- Microsoft Excel format
- Headers in first row
- Data in single sheet (or specify sheet name)
- No merged cells in data area

**Example Excel structure**:
| SampleID | Type | Au_ppm | Ag_ppm |
|----------|------|--------|--------|
| STD-001  | STD  | 1.25   | 15.8   |
| BLK-001  | BLK  | 0.008  | 0.1    |
| UNK-001  | UNK  | 2.45   | 18.2   |

**Common Issues**:
- **Multiple sheets**: Application reads first sheet by default
- **Merged cells**: Unmerge cells before importing
- **Formulas**: Convert formulas to values
- **Formatting**: Remove special formatting that may interfere

---

## Preparing Your Data

### Required Columns

Your data file **must** have these columns:

1. **Sample ID**: Unique identifier for each sample
   - Examples: "SampleID", "Sample_ID", "ID", "Sample"
   - Must be unique (no duplicates)
   - Can be text or numbers

2. **Sample Type**: Classification of sample type
   - Examples: "Type", "SampleType", "Category"
   - Values: STD, BLK, UNK (or variations)
   - Case-insensitive

3. **Result**: Numeric assay values
   - Examples: "Result", "Au_ppm", "Value", "Assay"
   - Must contain numbers (not text)
   - Can include qualifiers (<DL, >DL) which are parsed

### Optional Columns

- **Element columns**: Additional elements (Cu, Zn, Pb, etc.)
- **Metadata**: Hole ID, depth, date, etc. (not used in analysis but preserved)

### Data Quality Checklist

Before importing, verify:

- [ ] File is CSV or Excel format
- [ ] Headers are in first row
- [ ] Sample ID column exists and is unique
- [ ] Sample Type column exists with STD/BLK/UNK values
- [ ] Result column exists with numeric values
- [ ] No completely empty rows
- [ ] File isn't corrupted (open in Excel first)
- [ ] File size is reasonable (< 50MB recommended)

---

## Import Process

### Method 1: Drag and Drop (React UI)

1. **Open Data Import section**
2. **Drag file** from file explorer onto upload area
3. **Drop file** when upload area highlights
4. **Wait for processing** (usually < 2 seconds)
5. **Review column mapping** suggestions

### Method 2: Click to Browse

1. **Open Data Import section**
2. **Click upload area** or "Browse" button
3. **Select file** from file dialog
4. **Click "Open"**
5. **Wait for processing**
6. **Review column mapping** suggestions

### Method 3: Load Demo Data

1. **Open Data Import section**
2. **Click "Load Demo Data"**
3. **Select demo dataset**:
   - "Gold Fire Assay" - Sample gold data
   - "PhotonAssay" - Sample PhotonAssay data
4. **Demo data loads automatically**

**Use demo data to**:
- Learn the application
- Test features
- See example data structure

---

## Column Mapping

### Automatic Detection

The application automatically detects columns by:
- **Column name matching**: Looks for common names (SampleID, Type, Result)
- **Content analysis**: Analyzes data to identify sample types and values
- **Heuristic matching**: Uses patterns to suggest mappings

### Manual Mapping

If automatic detection doesn't work:

1. **Review suggested mappings**
2. **Use dropdown menus** to select correct columns
3. **Map each required column**:
   - Sample ID → Select your ID column
   - Sample Type → Select your type column
   - Result → Select your result column
4. **Map element columns** (if applicable):
   - Click "Add Element"
   - Select element column
   - Enter element name

### Mapping Tips

**Sample ID Column**:
- Must be unique
- Can be text or numbers
- Examples: "S001", "STD-001", "12345"

**Sample Type Column**:
- Recognized values: STD, BLK, UNK, DUP
- Case-insensitive
- Variations accepted: "Standard", "Blank", "Unknown"
- For duplicates: Use same ID with -OR and -CK suffixes, or use UNK type

**Result Column**:
- Must contain numbers
- Can include qualifiers: <DL, >DL, ND
- Qualifiers are parsed automatically
- Negative values treated as below detection limit

**Element Columns**:
- Map additional elements if analyzing multi-element data
- Element name should match column name or be specified
- Each element analyzed separately

---

## Data Validation

### Automatic Validation

The application validates:

1. **File format**: Ensures CSV or Excel
2. **Required columns**: Checks for Sample ID, Type, Result
3. **Data types**: Verifies Result column contains numbers
4. **Sample types**: Checks for valid STD/BLK/UNK values
5. **Empty rows**: Detects and handles empty rows
6. **File size**: Warns if file is very large

### Validation Messages

**Success**: "File imported successfully" with row count

**Warnings**:
- "Some columns not detected" - Manual mapping needed
- "Large file detected" - Processing may be slow
- "Empty rows found" - Empty rows will be skipped

**Errors**:
- "Invalid file format" - File must be CSV or Excel
- "Required columns missing" - Sample ID, Type, or Result not found
- "File is empty" - No data rows found
- "File is corrupted" - Cannot read file

### Fixing Validation Issues

**Missing columns**:
- Check column names
- Rename columns to standard names
- Use manual mapping

**Invalid data types**:
- Ensure Result column contains numbers
- Remove text from Result column
- Check for formatting issues

**Invalid sample types**:
- Standardize Sample Type values to STD, BLK, UNK
- Check for typos
- Use consistent naming

---

## Handling Errors

### Common Import Errors

#### Error: "File format not supported"

**Cause**: File is not CSV or Excel

**Solution**:
1. Convert file to CSV or Excel format
2. Save as .csv or .xlsx
3. Try importing again

#### Error: "Required columns missing"

**Cause**: Sample ID, Type, or Result column not found

**Solution**:
1. Check column names in your file
2. Rename columns to standard names
3. Use manual mapping to select columns
4. Ensure columns exist in first row (headers)

#### Error: "File is empty"

**Cause**: No data rows found

**Solution**:
1. Check file has data rows (not just headers)
2. Ensure data starts in row 2 (row 1 = headers)
3. Remove empty rows at top of file
4. Verify file wasn't corrupted during save

#### Error: "Cannot read file"

**Cause**: File is corrupted or in use

**Solution**:
1. Close file in other applications (Excel, etc.)
2. Try opening file in Excel/LibreOffice first
3. Save file again
4. Check file isn't corrupted
5. Try different file format (CSV vs. Excel)

#### Error: "Column mapping failed"

**Cause**: Cannot automatically detect columns

**Solution**:
1. Use manual mapping
2. Select columns from dropdowns
3. Check column names are clear
4. Ensure data types are correct

### Getting Help with Errors

1. **Read error message**: Error messages explain the issue
2. **Check file structure**: Verify file matches requirements
3. **Try demo data**: Verify application works with sample data
4. **Check console**: Browser console may have more details
5. **Review validation**: Check validation messages for clues

---

## Tips for Large Files

### File Size Considerations

**Small files** (< 1,000 rows):
- Process quickly (< 1 second)
- No special considerations

**Medium files** (1,000 - 10,000 rows):
- Process in 1-5 seconds
- May see brief loading indicator

**Large files** (> 10,000 rows):
- Process in 5-30 seconds
- Use backend for faster processing
- Consider splitting into batches

### Optimizing Large Files

**Before Import**:
1. **Remove unnecessary columns**: Delete columns not needed
2. **Remove empty rows**: Clean up data file
3. **Use CSV instead of Excel**: CSV is faster to process
4. **Split large files**: Process in batches if very large

**During Import**:
1. **Use backend**: Server-side processing is faster
2. **Be patient**: Large files take time to process
3. **Don't close browser**: Wait for processing to complete

**After Import**:
1. **Save project**: Save work frequently
2. **Export results**: Export to reduce memory usage
3. **Close unused tabs**: Free up browser resources

### Backend Processing

For very large files, use the backend:

1. **Start backend server**:
   ```bash
   cd react_ui
   python3 -m uvicorn api.main:app --reload --port 8000
   ```

2. **Application auto-detects backend**
3. **File uploads to server** for processing
4. **Faster processing** for large files
5. **Server-side memory** handles large datasets

---

## Best Practices

### File Organization

- **Use consistent naming**: `ProjectName_Assays_Date.csv`
- **Standardize columns**: Use same column names across files
- **Keep backups**: Always keep original data files
- **Document changes**: Note any data modifications

### Data Preparation

- **Clean data first**: Remove empty rows, fix formatting
- **Standardize sample types**: Use STD, BLK, UNK consistently
- **Check data quality**: Verify values are reasonable
- **Document qualifiers**: Note any special values (<DL, etc.)

### Import Workflow

1. **Prepare file**: Clean and organize data
2. **Import file**: Use drag-and-drop or browse
3. **Review mapping**: Verify columns mapped correctly
4. **Fix issues**: Address any validation warnings
5. **Proceed**: Continue to analysis setup

---

**Next Steps**: After importing data, proceed to [Analysis Configuration Guide](GUIDE_ANALYSIS_CONFIG.md)

**Need help?** → [FAQ](FAQ.md) | [User Manual](USER_MANUAL.md)
