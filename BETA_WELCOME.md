# Welcome to the QAQC Report Generator Beta! 🚀

Thank you for helping us test the new automated QAQC reporting tool.
Your feedback is critical to making this tool robust for geologists everywhere.

## What is this tool?
The QAQC Report Generator automates the tedious parts of JORC compliance. It processes your assay data, runs statistical checks (CRM bias, contamination, precision), and generates comprehensive Word/PDF reports with control charts.

---

## ⚡ Quick Start

### 1. Prerequisites
You need two things installed on your computer before running the app. If you don't have them, the launch script will let you know.
*   **Python 3.11+**: [Download Here](https://www.python.org/downloads/)
*   **Node.js (LTS)**: [Download Here](https://nodejs.org/)

### 2. Launching the App
We've included scripts to handle setup and launching.

**Mac / Linux:**
1.  Open Terminal in this folder.
2.  Run: `./start_app.sh`

**Windows:**
1.  Double-click `start_app.bat` (or run from Command Prompt).

*Note: The first run will take a few minutes to install dependencies. Subsequent runs will be instant.*

The app will open in your browser at `http://localhost:5173`.

---

## 📚 Testing Guide
We have prepared a comprehensive guide with **videos**, **screenshots**, and **step-by-step instructions** for every feature.

👉 **[Open QAQC User Manual](docs/TESTING_GUIDE_FULL.md)**

Please try to test:
1.  **Data Import**: Try your own CSV files or use the sample data.
2.  **Custom CRMs**: Add your own standard definitions in the CRM Database.
3.  **Reporting**: Generate a full JORC report and check the output.

---

## 🐛 Giving Feedback
Found a bug? Have a brilliant idea? We want to hear it!

1.  **Check Known Issues**: See the bottom of the User Manual.
2.  **Record Findings**: Use the [Feedback Template](docs/beta/FEEDBACK_TEMPLATE.md) to structure your report.
3.  **Submit**: diverse methods (Email, GitHub Issues, or Slack) depending on your channel.

Happy Testing! ⚒️
