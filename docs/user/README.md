# QAQC Report Generator - User Documentation

Welcome to the QAQC Report Generator user documentation! This guide will help you get started and master the application.

## 📚 Documentation Index

### Getting Started
- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
  - Installation instructions
  - Your first analysis
  - Basic workflow overview

### Comprehensive Guides
- **[User Manual](USER_MANUAL.md)** - Complete reference guide
  - All features explained
  - Detailed workflows
  - Configuration options
  - Troubleshooting

- **[Tutorials](TUTORIALS.md)** - Step-by-step walkthroughs
  - Gold Fire Assay Analysis
  - Multi-element Analysis
  - Batch Processing
  - Custom Reports
  - And more...

### Feature-Specific Guides
- **[Data Import Guide](GUIDE_DATA_IMPORT.md)** - Importing and mapping your data
- **[Analysis Configuration Guide](GUIDE_ANALYSIS_CONFIG.md)** - Setting up your analysis
- **[Results Interpretation Guide](GUIDE_RESULTS.md)** - Understanding your results
- **[Report Generation Guide](GUIDE_REPORTS.md)** - Creating professional reports

### Reference
- **[FAQ](FAQ.md)** - Frequently asked questions and troubleshooting

## 🚀 Quick Navigation

**New to QAQC Analysis?**
1. Start with the [Quick Start Guide](QUICK_START.md)
2. Try the [First Tutorial](TUTORIALS.md#tutorial-1-gold-fire-assay-analysis)
3. Read the [User Manual](USER_MANUAL.md) for details

**Need Help with a Specific Task?**
- Importing data? → [Data Import Guide](GUIDE_DATA_IMPORT.md)
- Configuring analysis? → [Analysis Configuration Guide](GUIDE_ANALYSIS_CONFIG.md)
- Understanding results? → [Results Interpretation Guide](GUIDE_RESULTS.md)
- Generating reports? → [Report Generation Guide](GUIDE_REPORTS.md)

**Having Issues?**
- Check the [FAQ](FAQ.md)
- Review the [Troubleshooting section](USER_MANUAL.md#troubleshooting) in the User Manual

## 📖 Application Overview

The QAQC Report Generator is a professional tool for analyzing Quality Assurance/Quality Control (QAQC) data from laboratory assays. It helps geologists and mining engineers:

- **Analyze Standards** - Monitor laboratory performance using Certified Reference Materials (CRMs)
- **Check Blanks** - Detect contamination in blank samples
- **Evaluate Duplicates** - Assess precision using duplicate sample pairs
- **Generate Reports** - Create professional Excel, PDF, and Word reports
- **Visualize Data** - Interactive charts and graphs for data interpretation

## 🎯 Which Interface Should I Use?

The application offers three interfaces:

1. **React UI (Recommended)** - Modern web-based interface
   - Best for: Most users, interactive workflows, modern experience
   - Location: `react_ui/` directory
   - See: [Quick Start Guide - React UI](QUICK_START.md#react-ui-installation)

2. **PyQt Desktop GUI** - Traditional desktop application
   - Best for: Offline use, familiar desktop experience
   - Location: `src/gui/` directory
   - See: [Quick Start Guide - PyQt GUI](QUICK_START.md#pyqt-gui-installation)

3. **Command Line Interface (CLI)** - Terminal-based
   - Best for: Automation, batch processing, scripting
   - Location: `main.py` in project root
   - See: [User Manual - CLI Usage](USER_MANUAL.md#command-line-interface)

## 💡 Key Concepts

Before diving in, it helps to understand:

- **Standards (CRMs)**: Certified Reference Materials used to verify laboratory accuracy
- **Blanks**: Samples with no analyte to detect contamination
- **Duplicates**: Paired samples to assess precision
- **Z-scores**: Statistical measure of how many standard deviations a result is from the expected value
- **RPD**: Relative Percent Difference between duplicate samples
- **Control Charts**: Time-series plots showing performance over time

Learn more in the [User Manual - Introduction](USER_MANUAL.md#introduction-to-qaqc-analysis).

## 🆘 Getting Help

- **Documentation**: Browse the guides above
- **FAQ**: Check [FAQ.md](FAQ.md) for common questions
- **Troubleshooting**: See the [Troubleshooting section](USER_MANUAL.md#troubleshooting)
- **Education Center**: Use the in-app Education Center for QAQC concepts

## 📝 Documentation Updates

This documentation is continuously updated. If you find errors or have suggestions, please report them.

---

**Ready to get started?** → [Quick Start Guide](QUICK_START.md)
