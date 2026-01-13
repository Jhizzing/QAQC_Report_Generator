# Installation Guide

Complete installation instructions for the QAQC Report Generator on Windows, macOS, and Linux.

## Prerequisites

### System Requirements

- **Operating System**: 
  - Windows 10/11 (64-bit)
  - macOS 10.15 (Catalina) or later
  - Linux Ubuntu 20.04+ or equivalent
- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free disk space
- **Internet**: Required for initial installation

### Check Python Version

```bash
python --version
# or
python3 --version
```

Should show Python 3.11 or higher. If not, install from [python.org](https://www.python.org/downloads/).

## Installation Methods

### Method 1: Standalone Executable (Recommended)

The easiest way to use the application is with pre-built executables.

#### Windows

1. Download `QAQC-GUI-Setup.exe` from releases
2. Run the installer
3. Follow the installation wizard
4. Launch from Start Menu or desktop shortcut

#### macOS

1. Download `QAQC-GUI.dmg` from releases
2. Open the DMG file
3. Drag `QAQC-GUI.app` to Applications folder
4. Launch from Applications

**Note**: macOS may show a security warning. To allow:
- Right-click the app → Open
- Click "Open" in the security dialog

#### Linux

1. Download `QAQC-GUI.AppImage` from releases
2. Make executable: `chmod +x QAQC-GUI.AppImage`
3. Run: `./QAQC-GUI.AppImage`

### Method 2: Python Package Installation

For development or customization.

#### Step 1: Clone Repository

```bash
git clone https://github.com/Jhizzing/QAQC_Report_Generator.git
cd QAQC_Report_Generator
```

#### Step 2: Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Verify Installation

```bash
python main.py --help
```

### Method 3: React UI (Web Interface)

For the modern web-based interface.

#### Step 1: Install Node.js

Download and install Node.js 18+ from [nodejs.org](https://nodejs.org/).

#### Step 2: Install Dependencies

```bash
cd react_ui
npm install
```

#### Step 3: Start Development Server

```bash
npm run dev
```

The application will open at `http://localhost:5173`.

#### Step 4: Build for Production

```bash
npm run build
```

Built files will be in `react_ui/dist/`.

## Post-Installation

### Verify Installation

1. **CLI Test**:
   ```bash
   python main.py --input mock_data/complex_test_data.csv --output output --auto-crm
   ```

2. **GUI Test**:
   ```bash
   python launch_gui_simple.py
   ```

3. **React UI Test**:
   ```bash
   cd react_ui
   npm run dev
   ```

### Configuration

1. **Review Configuration**:
   - Edit `config.yaml` for application settings
   - Edit `crm_database.yaml` to add your CRMs

2. **Create Directories**:
   ```bash
   mkdir -p data/input data/output logs
   ```

3. **Set Permissions** (Linux/macOS):
   ```bash
   chmod -R 755 data/
   ```

## Troubleshooting

### Python Not Found

**Windows:**
- Add Python to PATH during installation
- Or use full path: `C:\Python311\python.exe`

**macOS/Linux:**
- Use `python3` instead of `python`
- Install Python via Homebrew (macOS) or package manager (Linux)

### Module Not Found Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Permission Errors

**Linux/macOS:**
```bash
# Fix permissions
chmod +x launch_gui_simple.py
chmod -R 755 data/
```

**Windows:**
- Run as Administrator if needed
- Check folder permissions in Properties

### GUI Won't Start

1. **Check Dependencies**:
   ```bash
   pip list | grep -i pyqt
   ```

2. **Reinstall PyQt6**:
   ```bash
   pip install --upgrade PyQt6
   ```

3. **Check Display** (Linux):
   ```bash
   echo $DISPLAY
   # If empty, set: export DISPLAY=:0
   ```

### React UI Build Errors

1. **Clear Cache**:
   ```bash
   cd react_ui
   rm -rf node_modules dist
   npm install
   ```

2. **Check Node Version**:
   ```bash
   node --version  # Should be 18+
   ```

3. **Update Dependencies**:
   ```bash
   npm update
   ```

## Uninstallation

### Standalone Executable

**Windows:**
- Use Control Panel → Programs → Uninstall
- Or run uninstaller from installation directory

**macOS:**
- Drag app to Trash
- Empty Trash

**Linux:**
- Delete AppImage file
- Remove desktop entry if created

### Python Installation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove repository
cd ..
rm -rf QAQC_Report_Generator
```

## Next Steps

After installation:

1. **Read Quick Start Guide**: [QUICK_START.md](QUICK_START.md)
2. **Review User Manual**: [USER_MANUAL.md](USER_MANUAL.md)
3. **Try Demo Data**: Load sample data from the application
4. **Configure Settings**: Adjust defaults in Settings page

## Getting Help

- **Documentation**: See `docs/user/` directory
- **Issues**: Report on GitHub Issues
- **FAQ**: [FAQ.md](FAQ.md)
