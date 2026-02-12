# Troubleshooting Guide

Common issues and solutions for the QAQC Report Generator.

## Installation Issues

### Python Not Found

**Problem**: `python: command not found` or `python3: command not found`

**Solutions**:
- **Windows**: Reinstall Python and check "Add Python to PATH" during installation
- **macOS**: Install via Homebrew: `brew install python3`
- **Linux**: Install via package manager: `sudo apt install python3` (Ubuntu/Debian)

### Module Import Errors

**Problem**: `ModuleNotFoundError: No module named 'X'`

**Solutions**:
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# Or install specific module
pip install <module-name>
```

### Permission Denied Errors

**Problem**: Permission errors when running scripts or accessing files

**Solutions**:
- **Linux/macOS**: 
  ```bash
  chmod +x launch_gui_simple.py
  chmod -R 755 data/
  ```
- **Windows**: Run as Administrator or check folder permissions

## Application Issues

### GUI Won't Start

**Problem**: GUI application doesn't launch or crashes immediately

**Solutions**:
1. **Check PyQt6 installation**:
   ```bash
   pip list | grep -i pyqt
   pip install --upgrade PyQt6
   ```

2. **Check Python version**:
   ```bash
   python --version  # Should be 3.11+
   ```

3. **Try alternative launcher**:
   ```bash
   python launch_gui_simple.py
   ```

4. **Check logs**: Look for error messages in console output

### React UI Won't Load

**Problem**: React UI shows blank page or errors

**Solutions**:
1. **Clear cache and reinstall**:
   ```bash
   cd react_ui
   rm -rf node_modules dist
   npm install
   npm run dev
   ```

2. **Check Node.js version**:
   ```bash
   node --version  # Should be 18+
   ```

3. **Check port availability**:
   - Default port is 5173
   - Try different port: `npm run dev -- --port 5174`

4. **Check browser console**: Open DevTools (F12) for error messages

### Backend API Not Available

**Problem**: React UI shows "Backend offline" or connection errors

**Solutions**:
1. **Start backend server**:
   ```bash
   cd react_ui/api
   python start_api.py
   ```

2. **Check backend port**: Default is 8000
   - Verify no other service is using port 8000
   - Check firewall settings

3. **Verify CORS settings**: Backend should allow requests from React UI origin

## Data Import Issues

### File Won't Import

**Problem**: CSV/Excel file import fails

**Solutions**:
1. **Check file format**:
   - Must be CSV (.csv) or Excel (.xlsx)
   - Check file isn't corrupted
   - Verify file encoding (should be UTF-8)

2. **Check file size**:
   - Maximum file size: 50MB
   - Split large files if needed

3. **Check column names**:
   - Ensure required columns exist (Sample_ID, Sample_Type, etc.)
   - Check for special characters in column names

4. **Try sample data first**: Use demo data to verify installation

### Column Mapping Errors

**Problem**: Columns not detected or mapped incorrectly

**Solutions**:
1. **Manual mapping**: Use dropdown menus to manually map columns
2. **Check column names**: Ensure column names are clear and consistent
3. **Review data format**: Check that data types match expected formats

### Invalid Data Errors

**Problem**: "Invalid data" or "Validation error" messages

**Solutions**:
1. **Check data types**: Ensure numeric columns contain numbers
2. **Check for missing values**: Fill or remove rows with missing required data
3. **Check qualifiers**: Ensure qualifiers like `<DL` are properly formatted
4. **Review error message**: Error message should indicate which field is problematic

## Analysis Issues

### Analysis Fails

**Problem**: Analysis doesn't complete or shows errors

**Solutions**:
1. **Check data completeness**:
   - Ensure standards, blanks, and duplicates are present
   - Verify sample types are correctly identified

2. **Check CRM selection**:
   - Ensure CRMs are selected for standards analysis
   - Verify CRM values match your data

3. **Check configuration**:
   - Review tolerance settings
   - Verify detection limits
   - Check precision targets

4. **Review error message**: Check console or logs for specific error

### Incorrect Results

**Problem**: Analysis results seem wrong

**Solutions**:
1. **Verify CRM values**: Check that certified values match your CRMs
2. **Check units**: Ensure units are consistent (ppm vs %, g/t vs ppm)
3. **Review settings**: Verify tolerance and precision targets are appropriate
4. **Compare with manual calculation**: Spot-check a few samples manually

### Slow Performance

**Problem**: Analysis takes too long

**Solutions**:
1. **Check dataset size**: Large datasets (>1000 samples) take longer
2. **Close other applications**: Free up memory and CPU
3. **Check system resources**: Ensure sufficient RAM available
4. **Use backend**: Backend analysis may be faster for large datasets

## Report Generation Issues

### Report Won't Generate

**Problem**: Report generation fails or produces errors

**Solutions**:
1. **Check output directory**: Ensure directory exists and is writable
2. **Check disk space**: Ensure sufficient free space
3. **Check file permissions**: Verify write permissions for output directory
4. **Review error message**: Check for specific error details

### Report Format Issues

**Problem**: Generated report has formatting problems

**Solutions**:
1. **Excel issues**:
   - Ensure Excel is not open when generating report
   - Try different output filename
   - Check Excel version compatibility

2. **PDF issues**:
   - Ensure ReportLab is installed: `pip install reportlab`
   - Check PDF viewer compatibility

3. **Word issues**:
   - Ensure python-docx is installed: `pip install python-docx`
   - Check Word version compatibility

### Missing Charts or Figures

**Problem**: Report doesn't include expected charts

**Solutions**:
1. **Check analysis completed**: Charts require completed analysis
2. **Verify chart generation**: Check that plots were generated during analysis
3. **Review report options**: Ensure charts are selected in report configuration
4. **Check file paths**: Verify plot files exist in expected location

## Configuration Issues

### Settings Not Saving

**Problem**: Settings changes don't persist

**Solutions**:
1. **Check file permissions**: Ensure config file is writable
2. **Check file location**: Verify config file path is correct
3. **Restart application**: Some settings require restart
4. **Check for errors**: Review console for save errors

### CRM Database Issues

**Problem**: CRMs not found or incorrect values

**Solutions**:
1. **Check CRM database file**: Verify `crm_database.yaml` exists
2. **Verify CRM IDs**: Ensure CRM IDs match exactly (case-sensitive)
3. **Check element names**: Verify element names match your data
4. **Add missing CRMs**: Add your CRMs to the database file

## Performance Issues

### Application Slow or Unresponsive

**Problem**: Application is slow or freezes

**Solutions**:
1. **Check system resources**: 
   - Close other applications
   - Check memory usage
   - Verify sufficient disk space

2. **Reduce dataset size**: Process smaller batches
3. **Use backend**: Backend analysis may be faster
4. **Check for memory leaks**: Restart application periodically

### High Memory Usage

**Problem**: Application uses too much memory

**Solutions**:
1. **Process in batches**: Split large datasets
2. **Close unused features**: Close charts/tables not in use
3. **Restart application**: Clear memory by restarting
4. **Check for memory leaks**: Monitor memory usage over time

## Error Messages

### Common Error Messages

**"File not found"**:
- Check file path is correct
- Verify file exists
- Check file permissions

**"Invalid file format"**:
- Ensure file is CSV or Excel format
- Check file isn't corrupted
- Verify file encoding

**"Analysis failed"**:
- Check data completeness
- Verify CRM selection
- Review configuration settings

**"Out of memory"**:
- Reduce dataset size
- Close other applications
- Process in batches

## Getting More Help

### Check Logs

Application logs may contain detailed error information:
- **CLI**: Check console output
- **GUI**: Check console or log files
- **React UI**: Check browser console (F12)

### Report Issues

If problems persist:
1. **Document the issue**: Note error messages, steps to reproduce
2. **Check documentation**: Review relevant guides
3. **Search issues**: Check GitHub Issues for similar problems
4. **Create issue**: Report on GitHub with details

### Contact Support

- **GitHub Issues**: [Create an issue](https://github.com/Jhizzing/QAQC_Report_Generator/issues)
- **Documentation**: See `docs/` directory
- **FAQ**: [FAQ.md](FAQ.md)
