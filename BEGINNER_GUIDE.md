# 🍎 Software Development Guide for MacBook Beginners

## Welcome to Software Development!

This guide is specifically designed for beginners using macOS. It covers the essential concepts, tools, and workflows you'll need to successfully develop your QAQC Analysis Automation application.

---

## 📚 **Glossary of Important Terms**

### **Development Environment Terms**

**Terminal/Command Line**
- A text-based interface where you type commands instead of clicking
- On Mac: Press `Cmd + Space`, type "Terminal", press Enter
- Essential for running Python, managing files, and using Git

**Virtual Environment (venv)**
- An isolated Python environment for your project
- Prevents conflicts between different projects' dependencies
- Think of it as a separate "workspace" for each project

**Package Manager**
- **pip**: Python's package installer (like an app store for Python libraries)
- **Homebrew**: Mac's package manager for installing development tools
- **conda**: Alternative Python package manager (more advanced)

**Dependencies**
- External libraries/code that your project needs to run
- Listed in `requirements.txt` file
- Examples: pandas (data analysis), matplotlib (plotting)

### **Programming Terms**

**IDE (Integrated Development Environment)**
- Software for writing code (like VS Code, PyCharm)
- Provides syntax highlighting, debugging, file management
- Think of it as a specialized word processor for code

**Syntax**
- The rules for writing code in a programming language
- Like grammar rules for a language
- Python is case-sensitive and uses indentation

**Function**
- A reusable block of code that performs a specific task
- Like a recipe that you can use multiple times
- Example: `calculate_z_score()` function

**Class**
- A blueprint for creating objects
- Like a template for a car (all cars have wheels, engine, etc.)
- Your QAQC project uses classes for Sample, Standard, Blank, etc.

**Module**
- A file containing Python code
- Like a chapter in a book
- Your project has modules for data processing, analysis, etc.

**Package**
- A collection of modules
- Like a book with multiple chapters
- Your `src/` directory is a package

### **Version Control Terms**

**Git**
- A system for tracking changes in your code
- Like "Track Changes" in Word, but much more powerful
- Allows you to save different versions and collaborate

**Repository (repo)**
- A folder containing your project and its version history
- Your entire QAQC project folder is a repository

**Commit**
- Saving a snapshot of your code with a message
- Like saving a draft with a note about what you changed
- Example: "Added data import functionality"

**Branch**
- A parallel version of your code
- Like making a copy to try new features without breaking the main version
- Main branch = your working version, feature branches = experiments

**GitHub**
- Online platform for storing and sharing Git repositories
- Like Google Drive for code
- Allows collaboration and backup

### **Testing Terms**

**Unit Test**
- Testing individual pieces of code
- Like testing each ingredient before cooking
- Ensures each function works correctly

**Integration Test**
- Testing how different parts work together
- Like testing the whole recipe
- Ensures the complete workflow functions

**Bug**
- An error or unexpected behavior in your code
- Like a typo that causes problems
- Debugging = finding and fixing bugs

### **Deployment Terms**

**Executable**
- A file that runs your program without needing Python installed
- Like a .app file on Mac
- Created using PyInstaller

**Distribution**
- Sharing your finished application with users
- Like publishing an app to the App Store
- Can be through GitHub, direct download, etc.

---

## 🛠 **MacBook Development Setup Process**

### **Step 1: Install Essential Tools**

#### **Install Homebrew (Package Manager)**
```bash
# Open Terminal and run:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### **Install Python (if not already installed)**
```bash
# Check if Python is installed:
python3 --version

# If not installed, install via Homebrew:
brew install python
```

#### **Install Git**
```bash
# Install Git:
brew install git

# Configure Git with your information:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### **Step 2: Install VS Code (Recommended IDE)**
1. Download from: https://code.visualstudio.com/
2. Install recommended extensions:
   - Python
   - GitLens
   - Python Docstring Generator
   - autoDocstring

### **Step 3: Set Up Your Project Environment**

#### **Navigate to Your Project**
```bash
# Open Terminal and navigate to your project:
cd "/Users/patrickhann/Desktop/QAQC report generator"
```

#### **Create Virtual Environment**
```bash
# Create virtual environment:
python3 -m venv venv

# Activate virtual environment:
source venv/bin/activate

# You should see (venv) at the beginning of your terminal prompt
```

#### **Install Dependencies**
```bash
# Install required packages:
pip install -r requirements.txt

# Install your project in development mode:
pip install -e .
```

---

## 🔄 **Daily Development Workflow**

### **Morning Routine**
1. **Open Terminal**
   ```bash
   cd "/Users/patrickhann/Desktop/QAQC report generator"
   source venv/bin/activate
   ```

2. **Open VS Code**
   ```bash
   code .
   ```

3. **Check Git Status**
   ```bash
   git status
   ```

### **Development Process**

#### **1. Create a Feature Branch**
```bash
# Create and switch to new branch:
git checkout -b feature/data-import

# Work on your feature...
```

#### **2. Make Changes**
- Write code in VS Code
- Test frequently
- Save files regularly (Cmd + S)

#### **3. Test Your Code**
```bash
# Run tests:
pytest

# Run specific test file:
pytest tests/test_data_models.py
```

#### **4. Commit Changes**
```bash
# Add files to staging:
git add .

# Commit with descriptive message:
git commit -m "Add data import functionality for CSV files"
```

#### **5. Push to GitHub**
```bash
# Push branch to GitHub:
git push origin feature/data-import
```

### **End of Day Routine**
1. **Commit any remaining work**
2. **Push to GitHub**
3. **Deactivate virtual environment**
   ```bash
   deactivate
   ```

---

## 📁 **Understanding Your Project Structure**

```
QAQC report generator/
├── .git/                 # Git version control (hidden)
├── .vscode/             # VS Code settings
├── venv/                # Virtual environment (don't edit)
├── src/                 # Your source code
│   ├── data/           # Data processing modules
│   ├── analysis/       # QAQC calculations
│   ├── visualization/  # Plot generation
│   ├── reporting/      # Report creation
│   └── gui/           # User interface
├── tests/              # Test files
├── input/              # Input data files
├── output/             # Generated reports
├── config.yaml         # Configuration settings
├── requirements.txt    # Python dependencies
├── main.py            # Application entry point
└── README.md          # Project documentation
```

---

## 🐍 **Python Development Basics**

### **Running Python Code**

#### **Run Main Application**
```bash
# Activate virtual environment first:
source venv/bin/activate

# Run main application:
python main.py

# Run with help:
python main.py --help
```

#### **Run Individual Modules**
```bash
# Run a specific Python file:
python src/data/models.py

# Run Python interactively:
python
```

#### **Install New Packages**
```bash
# Install a package:
pip install package_name

# Add to requirements.txt:
pip freeze > requirements.txt
```

### **Common Python Commands**

```bash
# Check Python version:
python --version

# Check installed packages:
pip list

# Update a package:
pip install --upgrade package_name

# Uninstall a package:
pip uninstall package_name
```

---

## 🔧 **Troubleshooting Common Issues**

### **Virtual Environment Issues**

**Problem**: "command not found: python"
**Solution**:
```bash
# Use python3 instead:
python3 --version
python3 -m venv venv
```

**Problem**: Virtual environment not activating
**Solution**:
```bash
# Make sure you're in the right directory:
pwd
# Should show: /Users/patrickhann/Desktop/QAQC report generator

# Activate with full path:
source ./venv/bin/activate
```

### **Permission Issues**

**Problem**: "Permission denied" errors
**Solution**:
```bash
# Fix permissions:
chmod +x main.py
```

### **Package Installation Issues**

**Problem**: "pip install" fails
**Solution**:
```bash
# Update pip:
python -m pip install --upgrade pip

# Install with user flag:
pip install --user package_name
```

---

## 📖 **Learning Resources**

### **Python Learning**
- **Official Python Tutorial**: https://docs.python.org/3/tutorial/
- **Python for Beginners**: https://www.python.org/about/gettingstarted/
- **Real Python**: https://realpython.com/ (excellent tutorials)

### **Git Learning**
- **Git Handbook**: https://guides.github.com/introduction/git-handbook/
- **Git Tutorial**: https://www.atlassian.com/git/tutorials

### **VS Code Learning**
- **VS Code Python Tutorial**: https://code.visualstudio.com/docs/python/python-tutorial
- **VS Code Git Integration**: https://code.visualstudio.com/docs/editor/versioncontrol

### **Mac-Specific Resources**
- **Terminal Basics**: https://support.apple.com/guide/terminal/welcome/mac
- **Homebrew Documentation**: https://docs.brew.sh/

---

## 🎯 **Your First Week Goals**

### **Day 1-2: Environment Setup**
- [ ] Install Homebrew, Python, Git
- [ ] Install VS Code and extensions
- [ ] Set up virtual environment
- [ ] Install project dependencies

### **Day 3-4: Basic Git Setup**
- [ ] Initialize Git repository
- [ ] Create first commit
- [ ] Set up GitHub repository
- [ ] Push code to GitHub

### **Day 5-7: First Code**
- [ ] Create simple test file
- [ ] Run basic Python commands
- [ ] Understand project structure
- [ ] Start data import module

---

## 💡 **Pro Tips for Beginners**

1. **Save Frequently**: Use Cmd + S constantly
2. **Test Early**: Run code after every small change
3. **Read Error Messages**: They usually tell you what's wrong
4. **Use Google**: Search for error messages and solutions
5. **Ask Questions**: Join Python communities and forums
6. **Start Small**: Don't try to build everything at once
7. **Document Everything**: Write comments in your code
8. **Use Version Control**: Commit frequently with descriptive messages

---

## 🆘 **Getting Help**

### **When You're Stuck**
1. **Read the error message carefully**
2. **Google the exact error message**
3. **Check the documentation**
4. **Ask on Stack Overflow**
5. **Join Python Discord/Slack communities**

### **Useful Commands for Debugging**
```bash
# Check what's installed:
pip list

# Check Python path:
which python

# Check file permissions:
ls -la

# See recent commands:
history
```

---

## 🎉 **Success Milestones**

- [ ] **Week 1**: Environment set up, first Python code runs
- [ ] **Week 2**: Can import data files, basic calculations work
- [ ] **Week 3**: Generate first plots and reports
- [ ] **Week 4**: Have a working prototype
- [ ] **Week 8**: Complete application with GUI
- [ ] **Week 10**: Production-ready software

---

**Remember**: Every expert was once a beginner. Take it one step at a time, don't be afraid to make mistakes, and celebrate your progress! 🚀
