# 🍎 MacBook Development Setup Checklist

## Pre-Development Setup (Do This First!)

### ✅ **Step 1: Install Homebrew (Package Manager)**
```bash
# Open Terminal (Cmd + Space, type "Terminal")
# Copy and paste this command:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the prompts and enter your password when asked
```

### ✅ **Step 2: Install Python**
```bash
# Check if Python is already installed:
python3 --version

# If you see a version number (like 3.11.x), you're good!
# If not, install Python:
brew install python
```

### ✅ **Step 3: Install Git**
```bash
# Install Git:
brew install git

# Configure Git with your information:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### ✅ **Step 4: Install VS Code**
1. Go to: https://code.visualstudio.com/
2. Download the Mac version
3. Install the .dmg file
4. Open VS Code
5. Install these extensions:
   - Python (by Microsoft)
   - GitLens (by Eric Amodio)
   - Python Docstring Generator (by Nils Werner)

---

## Project Setup (Do This Next!)

### ✅ **Step 5: Navigate to Your Project**
```bash
# Open Terminal and run:
cd "/Users/patrickhann/Desktop/QAQC report generator"

# Verify you're in the right place:
pwd
# Should show: /Users/patrickhann/Desktop/QAQC report generator
```

### ✅ **Step 6: Create Virtual Environment**
```bash
# Create virtual environment:
python3 -m venv venv

# Activate virtual environment:
source venv/bin/activate

# You should see (venv) at the start of your terminal prompt
# If you see (venv) at the beginning, you're successful!
```

### ✅ **Step 7: Install Project Dependencies**
```bash
# Make sure virtual environment is activated (you should see (venv))
# Install required packages:
pip install -r requirements.txt

# This will take a few minutes to download and install everything
```

### ✅ **Step 8: Test Your Setup**
```bash
# Test that everything works:
python main.py --help

# You should see help text for the QAQC application
# If you see an error, don't worry - we'll fix it!
```

---

## Git Setup (Version Control)

### ✅ **Step 9: Initialize Git Repository**
```bash
# Make sure you're in your project directory:
cd "/Users/patrickhann/Desktop/QAQC report generator"

# Initialize Git:
git init

# Add all files:
git add .

# Create first commit:
git commit -m "Initial project setup"
```

### ✅ **Step 10: Create GitHub Repository**
1. Go to: https://github.com
2. Sign up for an account (if you don't have one)
3. Click "New Repository"
4. Name it: `qaqc-report-generator`
5. Make it private (for now)
6. Don't initialize with README (you already have one)
7. Click "Create Repository"

### ✅ **Step 11: Connect Local Project to GitHub**
```bash
# Add GitHub as remote origin (replace YOUR_USERNAME):
git remote add origin https://github.com/YOUR_USERNAME/qaqc-report-generator.git

# Push your code to GitHub:
git push -u origin main
```

---

## Daily Workflow Setup

### ✅ **Step 12: Create Daily Workflow Script**
Create a file called `start_dev.sh`:
```bash
#!/bin/bash
cd "/Users/patrickhann/Desktop/QAQC report generator"
source venv/bin/activate
code .
echo "Development environment ready!"
```

Make it executable:
```bash
chmod +x start_dev.sh
```

Now you can start development by running:
```bash
./start_dev.sh
```

---

## Verification Checklist

### ✅ **Everything Working?**
- [ ] Terminal opens and shows your username
- [ ] `python3 --version` shows Python 3.11 or higher
- [ ] `git --version` shows Git version
- [ ] VS Code opens when you type `code .`
- [ ] Virtual environment activates (shows `(venv)`)
- [ ] `pip list` shows installed packages
- [ ] `python main.py --help` shows help text
- [ ] Git repository is initialized
- [ ] GitHub repository is created and connected

### ✅ **If Something's Not Working:**
1. **Check your Terminal path**: Make sure you're in the right directory
2. **Check virtual environment**: Make sure you see `(venv)` in your prompt
3. **Check Python version**: Should be 3.11 or higher
4. **Check file permissions**: Make sure you can read/write files

---

## Common Issues & Solutions

### ❌ **"command not found: python"**
**Solution**: Use `python3` instead of `python`
```bash
python3 --version
python3 -m venv venv
```

### ❌ **"Permission denied"**
**Solution**: Fix permissions
```bash
chmod +x start_dev.sh
chmod +x main.py
```

### ❌ **"No such file or directory"**
**Solution**: Check your current directory
```bash
pwd
ls -la
```

### ❌ **Virtual environment not activating**
**Solution**: Use full path
```bash
source ./venv/bin/activate
```

### ❌ **"pip install" fails**
**Solution**: Update pip first
```bash
python -m pip install --upgrade pip
```

---

## Next Steps After Setup

### 🎯 **Your First Development Session**
1. **Open development environment**:
   ```bash
   ./start_dev.sh
   ```

2. **Create your first test file**:
   ```bash
   # In VS Code, create a new file: test_setup.py
   print("Hello, QAQC Analysis!")
   print("Python is working correctly!")
   ```

3. **Run your test**:
   ```bash
   python test_setup.py
   ```

4. **Start working on data import**:
   - Open `src/data/importer.py` in VS Code
   - Begin implementing the data import functionality

### 📚 **Learning Resources**
- **Python Tutorial**: https://docs.python.org/3/tutorial/
- **VS Code Python Guide**: https://code.visualstudio.com/docs/python/python-tutorial
- **Git Basics**: https://guides.github.com/introduction/git-handbook/

---

## 🎉 **Congratulations!**

If you've completed this checklist, you now have:
- ✅ A fully configured MacBook development environment
- ✅ Python 3.11+ with all necessary packages
- ✅ VS Code with helpful extensions
- ✅ Git version control set up
- ✅ GitHub repository connected
- ✅ Virtual environment for your project
- ✅ Ready to start coding!

**You're now ready to begin developing your QAQC Analysis Automation application!** 🚀

---

## 📞 **Need Help?**

If you get stuck at any step:
1. **Read the error message carefully**
2. **Google the exact error message**
3. **Check the BEGINNER_GUIDE.md for more details**
4. **Ask for help in Python communities**

**Remember**: Every developer started exactly where you are now. You've got this! 💪
