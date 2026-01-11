# Frequently Asked Questions (FAQ)

Common questions and answers about the QAQC Report Generator.

## Table of Contents

- [Installation & Setup](#installation--setup)
- [Data Import Issues](#data-import-issues)
- [Analysis Questions](#analysis-questions)
- [Report Generation](#report-generation)
- [Performance & Errors](#performance--errors)
- [Best Practices](#best-practices)

---

## Installation & Setup

### Q: What are the system requirements?

**A**: 
- **Node.js**: v18 or higher
- **npm**: v9 or higher
- **Python**: 3.11+ (optional, for backend)
- **Operating System**: Windows, macOS, or Linux
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge) for React UI

### Q: How do I install the application?

**A**: See the [Quick Start Guide](QUICK_START.md) for detailed installation instructions.

**React UI**:
```bash
cd react_ui
npm install
npm run dev
```

**PyQt GUI**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 launch_gui_simple.py
```

### Q: Do I need to install Python if I'm using the React UI?

**A**: No, the React UI works standalone without Python. Python is only needed if you want to use the FastAPI backend for server-side analysis.

### Q: The application won't start. What should I do?

**A**: 
1. Check Node.js version: `node --version` (needs v18+)
2. Delete `node_modules` and run `npm install` again
3. Check terminal for error messages
4. Try clearing browser cache
5. Ensure port 5173 (or configured port) is available

### Q: Can I use the application offline?

**A**: Yes! The React UI works completely offline. The PyQt GUI also works offline. Only backend features require an internet connection (and only if using a remote backend server).

---

## Data Import Issues

### Q: What file formats are supported?

**A**: 
- **CSV** (.csv) - Comma-separated values
- **Excel** (.xlsx, .xls) - Microsoft Excel files

### Q: My file won't import. What's wrong?

**A**: Common issues:
1. **File format**: Ensure file is CSV or Excel
2. **File size**: Very large files (> 50MB) may timeout
3. **File encoding**: Use UTF-8 encoding for CSV files
4. **File structure**: Ensure file has headers and data rows
5. **File corruption**: Try opening file in Excel/LibreOffice first

### Q: Columns aren't being detected. How do I fix this?

**A**: 
1. **Manual mapping**: Use dropdown menus to manually select columns
2. **Check column names**: Ensure columns exist in your file
3. **Rename columns**: Try using standard names (SampleID, Type, Result)
4. **Check data types**: Result column must contain numbers

### Q: What columns are required?

**A**: 
- **Sample ID**: Unique identifier for each sample (required)
- **Sample Type**: Column with STD, BLK, UNK values (required)
- **Result**: Numeric assay values (required)
- **Elements**: Additional element columns (optional)

### Q: What values should be in the Sample Type column?

**A**: 
- **STD** or **STD-***: Standard/CRM samples
- **BLK** or **BLK-***: Blank samples
- **UNK**, **DUP**, or sample pairs: Unknown/duplicate samples

The application is flexible and recognizes variations like "Standard", "Blank", etc.

### Q: My file is very large (> 10,000 rows). Will it work?

**A**: Yes, but:
- Processing may take longer (5-30 seconds)
- Use backend for faster processing of large files
- Consider splitting very large files into batches
- Ensure sufficient memory available

### Q: Can I import multiple files at once?

**A**: Currently, import one file at a time. For multiple files:
- Process files sequentially
- Use CLI for batch processing
- Or combine files into one before importing

---

## Analysis Questions

### Q: What's the difference between Field Duplicate and Pulp Duplicate?

**A**: 
- **Field Duplicate**: Two samples taken at the drill site (assesses sampling + analytical precision)
- **Pulp Duplicate**: Same sample split into two pulps (assesses analytical precision only)

Choose based on your duplicate sampling strategy.

### Q: How do I select the right CRMs?

**A**: 
1. **Match grade range**: Select CRMs near your sample grades
2. **Check expiry dates**: Ensure CRMs are current
3. **Verify matrix**: Ensure matrix type is appropriate
4. **Use multiple CRMs**: Select 2-3 CRMs covering your range
5. **Browse CRM Database**: Use the CRM Database feature to explore options

### Q: What tolerance should I use for standards?

**A**: 
- **Gold**: 10% is typical
- **Base Metals**: 10-15% depending on element
- **Multi-element**: May be higher (15-20%)
- **Adjust based on**: Laboratory precision, project requirements, industry standards

### Q: What detection limit should I use for blanks?

**A**: 
- **Gold (Fire Assay)**: 0.01 ppm (default)
- **Multi-element (ICP)**: 1 ppm (default)
- **Adjust based on**: Laboratory capabilities, method detection limits, project requirements

### Q: What RPD target should I use for duplicates?

**A**: 
- **Field Duplicates**: 20-25% is typical
- **Pulp Duplicates**: 10-15% is typical (better precision expected)
- **Adjust based on**: Commodity, sample type, project standards

### Q: My analysis shows many failures. What does this mean?

**A**: 
- **Review flagged samples**: Check which samples failed and why
- **Check laboratory performance**: High failure rate may indicate lab issues
- **Verify data quality**: Ensure data imported correctly
- **Check thresholds**: Ensure thresholds are appropriate for your data
- **Consider re-assaying**: Failed samples may need re-analysis

### Q: What's a good pass rate?

**A**: 
- **Industry standard**: ≥ 95% pass rate
- **Excellent**: ≥ 98% pass rate
- **Acceptable**: 90-95% pass rate
- **Needs attention**: < 90% pass rate

---

## Report Generation

### Q: What's the difference between "Figures Only" and "JORC Report"?

**A**: 
- **Figures Only**: Charts and tables only, quick summary
- **JORC Report**: Complete analysis report with metadata, methodology, interpretation

Choose based on your reporting needs.

### Q: Which export format should I use?

**A**: 
- **Excel**: For detailed data, further analysis, data sharing
- **PDF**: For professional reports, printing, final documentation
- **Word (DOCX)**: For editable reports, custom formatting

### Q: Can I customize the report?

**A**: Yes! You can:
- Add report metadata (competent person, company, etc.)
- Select which figures to include
- Choose color scheme and font size
- Set page layout
- Use template editor for advanced customization

### Q: My report is too large. How do I reduce file size?

**A**: 
1. **Reduce figure resolution**: Use 150 DPI instead of 600 DPI
2. **Include fewer figures**: Select only necessary charts
3. **Split report**: Generate separate reports for standards, blanks, duplicates
4. **Use Excel**: Excel files are typically smaller than PDF

### Q: Can I add my company logo to reports?

**A**: Yes! 
1. Go to Settings → Report Defaults
2. Enter logo URL or path
3. Logo will be included in reports

Or add logo when generating report (if option available).

---

## Performance & Errors

### Q: Analysis is slow. How can I speed it up?

**A**: 
1. **Use backend**: Server-side processing is faster for large files
2. **Close other tabs**: Free up browser resources
3. **Process in batches**: Split large files
4. **Use CSV instead of Excel**: CSV is faster to process

### Q: I'm getting "Out of Memory" errors. What should I do?

**A**: 
1. **Close other applications**: Free up system memory
2. **Process smaller files**: Split large files into chunks
3. **Use backend**: Server-side processing uses server memory
4. **Increase browser memory**: Close other browser tabs

### Q: The application crashes. What should I do?

**A**: 
1. **Check browser console**: Look for error messages
2. **Try different browser**: Some browsers handle large data better
3. **Clear browser cache**: May resolve caching issues
4. **Restart application**: Close and reopen
5. **Report the issue**: Note error messages and steps to reproduce

### Q: Backend won't connect. How do I fix this?

**A**: 
1. **Check backend is running**: Verify API server is started
2. **Check URL**: Verify backend URL in settings (default: http://localhost:8000)
3. **Check port**: Ensure port 8000 is available
4. **Check firewall**: Ensure firewall allows connection
5. **Use client-side mode**: Application works without backend

### Q: I see "Network Error" messages. What does this mean?

**A**: 
- **Backend not running**: Start the backend server
- **Wrong URL**: Check backend URL in settings
- **Firewall blocking**: Check firewall settings
- **Network issues**: Check internet connection (if using remote backend)

**Solution**: Application works in standalone mode without backend.

---

## Best Practices

### Q: How should I organize my data files?

**A**: 
- **Use consistent naming**: e.g., `ProjectName_Assays_Date.csv`
- **Standardize columns**: Use consistent column names across files
- **Keep backups**: Always keep original data files
- **Document changes**: Note any data cleaning or modifications

### Q: How often should I run QAQC analysis?

**A**: 
- **During drilling**: After each batch or daily
- **Before resource estimation**: Complete analysis of all data
- **For reporting**: Before finalizing reports
- **Regular monitoring**: Weekly or monthly for ongoing projects

### Q: What should I do if I find failures?

**A**: 
1. **Document failures**: Note which samples failed and why
2. **Review flagged samples**: Check for patterns or trends
3. **Investigate causes**: Determine if lab error, contamination, or sampling issue
4. **Take action**: Re-assay if needed, contact laboratory if systematic issues
5. **Report findings**: Include failure analysis in reports

### Q: How do I ensure JORC compliance?

**A**: 
1. **Use appropriate CRMs**: Select current, certified CRMs
2. **Set appropriate thresholds**: Follow industry standards
3. **Document methodology**: Record analysis settings
4. **Report failures**: Include failure analysis in reports
5. **Maintain records**: Keep analysis files and reports
6. **Use JORC Report format**: Generate JORC-compliant reports

### Q: Should I save my projects?

**A**: Yes! 
- **Save regularly**: Save projects as you work
- **Use descriptive names**: Name projects clearly
- **Keep project files**: `.qaqc` files contain complete project state
- **Version control**: Save different versions if making changes

### Q: Can I share my analysis with others?

**A**: Yes! 
- **Share project files**: Send `.qaqc` files to colleagues
- **Export reports**: Generate Excel/PDF reports to share
- **Export data**: Export results to CSV for further analysis
- **Document settings**: Note analysis configuration when sharing

### Q: How do I ensure data quality?

**A**: 
1. **Verify imports**: Check imported data matches source
2. **Review mappings**: Ensure columns mapped correctly
3. **Check statistics**: Review summary statistics for reasonableness
4. **Validate results**: Compare to expected values
5. **Document issues**: Note any data quality concerns

---

## Still Have Questions?

- **Check the [User Manual](USER_MANUAL.md)** for comprehensive documentation
- **Review [Tutorials](TUTORIALS.md)** for step-by-step guides
- **Use the Education Center** in the application for QAQC concepts
- **Check the [Troubleshooting section](USER_MANUAL.md#troubleshooting)** in the User Manual

---

**Need more help?** → [User Manual](USER_MANUAL.md) | [Tutorials](TUTORIALS.md)
