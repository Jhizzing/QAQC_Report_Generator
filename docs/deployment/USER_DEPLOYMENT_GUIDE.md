# QAQC Analysis Application - User Deployment Guide

## 🎯 Quick Start for Laboratory Staff

This guide will help you deploy and use the QAQC Analysis Application in your laboratory environment.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux Ubuntu 20.04+
- **Python**: Version 3.11 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended for large datasets)
- **Storage**: 2GB free disk space
- **Internet**: Required for initial setup

### Check Your System
```bash
# Check Python version
python --version
# Should show Python 3.11 or higher

# Check available memory
# Windows: Task Manager → Performance
# macOS: Activity Monitor → Memory
# Linux: free -h
```

## 🚀 Installation Steps

### Step 1: Download the Application
```bash
# Option 1: Clone from GitHub (Recommended)
git clone https://github.com/Jhizzing/QAQC_Report_Generator.git
cd QAQC_Report_Generator

# Option 2: Download ZIP file
# Go to: https://github.com/Jhizzing/QAQC_Report_Generator
# Click "Code" → "Download ZIP"
# Extract the ZIP file
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment
python -m venv qaqc_env

# Activate virtual environment
# Windows:
qaqc_env\Scripts\activate
# macOS/Linux:
source qaqc_env/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

### Step 3: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python main.py --help
```

### Step 4: Set Up Directories
```bash
# Create necessary directories
mkdir -p data/input
mkdir -p data/output
mkdir -p config
mkdir -p logs

# Copy configuration files
cp config.yaml config/production.yaml
cp crm_database.yaml data/
```

## 🔧 Configuration

### 1. Basic Configuration
Edit `config/production.yaml` to match your laboratory's requirements:

```yaml
# Detection limits for your laboratory
data:
  cleaning:
    default_detection_limit: 0.01  # Adjust based on your methods
    
# Analysis thresholds
analysis:
  standards:
    z_score_threshold: 2.0        # Z-score limit for standards
    recovery_limits: [95, 105]    # Acceptable recovery range (%)
    
  blanks:
    contamination_threshold: 3.0   # Contamination threshold
    blank_limit: 0.01             # Blank limit
    
  duplicates:
    rpd_threshold: 20.0           # RPD threshold (%)
```

### 2. CRM Database Setup
Edit `data/crm_database.yaml` to include your laboratory's CRMs:

```yaml
crms:
  - name: "Your CRM Name"
    certified_value: 1.25
    uncertainty: 0.05
    units: "g/t"
    matrix: "Gold Ore"
    expiry_date: "2026-12-31"
    batch_number: "BATCH-001"
    supplier: "Your Supplier"
```

## 📊 First Analysis

### Step 1: Prepare Your Data
Ensure your CSV file has these columns:
- `sample_id`: Unique sample identifier
- `sample_type`: STANDARD, BLANK, DUPLICATE, or SAMPLE
- `result`: Numerical result value
- `qualifier`: Optional qualifier (<DL, >DL, etc.)
- `detection_limit`: Optional detection limit

### Step 2: Run Basic Analysis
```bash
# Basic analysis with auto-mapping
python main.py --input data/input/your_data.csv --output data/output --infer-mapping --normalize-results --yes --auto-crm --include-plots

# Analysis with specific CRM
python main.py --input data/input/your_data.csv --output data/output --crm-name "Your CRM Name" --include-plots --output-format both
```

### Step 3: Review Results
Check the output directory for:
- **Excel Report**: `qaqc_report_YYYYMMDD_HHMMSS.xlsx`
- **PDF Report**: `qaqc_report_YYYYMMDD_HHMMSS.pdf`
- **Plots**: `plots/` directory with visualizations
- **Cleaned Data**: `your_data_clean.csv`

## 🔍 Understanding the Output

### Excel Report Structure
- **Summary Sheet**: Executive overview with pass/fail status
- **Standards Sheet**: Detailed standards analysis results
- **Blanks Sheet**: Contamination and carry-over analysis
- **Duplicates Sheet**: Precision and correlation analysis
- **Raw Data Sheet**: Complete dataset with analysis flags

### PDF Report Contents
- **Executive Summary**: High-level findings and recommendations
- **Detailed Analysis**: Comprehensive analysis results
- **Visualizations**: Embedded plots and charts
- **Recommendations**: Actionable insights and next steps

### Key Metrics to Review
- **Standards Analysis**: Z-scores, bias, recovery percentages
- **Blanks Analysis**: Contamination levels, carry-over effects
- **Duplicates Analysis**: RPD values, precision assessment
- **Overall Status**: PASS/FAIL for each analysis type

## 🛠️ Common Usage Scenarios

### Scenario 1: Daily QAQC Analysis
```bash
# Process daily batch
python main.py --input data/input/daily_batch.csv --output data/output --infer-mapping --normalize-results --yes --auto-crm --include-plots
```

### Scenario 2: Weekly Report Generation
```bash
# Generate comprehensive weekly report
python main.py --input data/input/weekly_data.csv --output data/output --crm-name "Weekly CRM" --include-plots --output-format both
```

### Scenario 3: Specific Analysis Types
```bash
# Skip specific analyses
python main.py --input data/input/data.csv --output data/output --skip-standards --skip-duplicates

# Only standards analysis
python main.py --input data/input/data.csv --output data/output --skip-blanks --skip-duplicates
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Python Version Error
```
Error: Python 3.11+ required
Solution: Install Python 3.11 or higher
```

#### 2. Missing Dependencies
```
Error: ModuleNotFoundError
Solution: Run `pip install -r requirements.txt`
```

#### 3. Data Format Issues
```
Error: Missing required columns
Solution: Check your CSV has sample_id, sample_type, result columns
```

#### 4. Permission Errors
```
Error: Permission denied
Solution: Check file permissions and directory access
```

### Getting Help

#### 1. Check Documentation
- **README.md**: Main documentation
- **BEGINNER_GUIDE.md**: Detailed user guide
- **Module Documents**: Specific module documentation

#### 2. Run with Verbose Output
```bash
python main.py --input data.csv --output results --verbose
```

#### 3. Check Logs
Look for error messages in the console output and check log files.

#### 4. GitHub Support
- **Issues**: https://github.com/Jhizzing/QAQC_Report_Generator/issues
- **Discussions**: GitHub Discussions for community support

## 📈 Best Practices

### 1. Data Preparation
- **Consistent Format**: Use consistent column names and formats
- **Data Quality**: Ensure data is clean and complete
- **Backup**: Always backup your original data
- **Validation**: Check data before analysis

### 2. Analysis Workflow
- **Regular Analysis**: Run QAQC analysis regularly
- **Documentation**: Keep records of analysis results
- **Review**: Review results and take action on failures
- **Improvement**: Use results to improve laboratory processes

### 3. Output Management
- **Organization**: Organize output files by date and batch
- **Archival**: Archive old reports and data
- **Sharing**: Share results with relevant stakeholders
- **Follow-up**: Take action on analysis recommendations

## 🔄 Maintenance

### Daily Tasks
- **Check Logs**: Review application logs for errors
- **Data Backup**: Backup input and output data
- **Performance**: Monitor processing time and memory usage

### Weekly Tasks
- **Update CRM**: Update CRM database if needed
- **Review Results**: Review analysis results and trends
- **Clean Output**: Clean up old output files

### Monthly Tasks
- **System Update**: Check for application updates
- **Configuration Review**: Review and update configuration
- **Performance Review**: Review system performance and optimization

## 📞 Support and Resources

### Documentation
- **README.md**: Main project documentation
- **BEGINNER_GUIDE.md**: Detailed user guide
- **Module Documents**: Specific module documentation
- **Deployment Plan**: Comprehensive deployment guide

### Community Support
- **GitHub Repository**: https://github.com/Jhizzing/QAQC_Report_Generator
- **Issues**: Report bugs and request features
- **Discussions**: Community support and knowledge sharing

### Professional Support
- **Technical Support**: Available for enterprise users
- **Training**: Custom training sessions available
- **Consulting**: Implementation and optimization consulting

## 🎯 Next Steps

### Immediate (This Week)
1. **Complete Installation**: Follow installation steps
2. **Test with Sample Data**: Run analysis with sample data
3. **Review Output**: Understand the analysis results
4. **Configure Settings**: Adjust configuration for your laboratory

### Short-term (Next 2 Weeks)
1. **Train Staff**: Train laboratory staff on usage
2. **Integrate Workflow**: Integrate into daily laboratory workflow
3. **Optimize Settings**: Fine-tune configuration based on results
4. **Establish Procedures**: Create standard operating procedures

### Long-term (Next Month)
1. **Full Integration**: Complete integration into laboratory processes
2. **Performance Monitoring**: Monitor and optimize performance
3. **User Feedback**: Collect and implement user feedback
4. **Continuous Improvement**: Regular updates and improvements

---

**Ready to Deploy**: The application is production-ready and fully tested
**Support Available**: Comprehensive documentation and community support
**Last Updated**: October 21, 2025
**Version**: 2.0.0
