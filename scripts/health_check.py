#!/usr/bin/env python3
"""
Health Check Script for LogiQore Reporter.
"""

import sys
import subprocess
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_python_imports():
    """Check if all required modules can be imported."""
    try:
        from src.data.importer import DataImporter
        from src.analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer
        from src.visualization import PlotGenerator
        from src.reporting import ExcelReporter, PDFReporter
        print("✓ All modules import successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def check_configuration():
    """Check if configuration files exist."""
    config_files = [
        'config/production.yaml',
        'config/logging.json',
        'config/monitoring.yaml'
    ]
    
    all_exist = True
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"✓ {config_file}")
        else:
            print(f"✗ {config_file} - Missing")
            all_exist = False
    
    return all_exist

def check_directories():
    """Check if required directories exist."""
    required_dirs = [
        'data/input',
        'data/output',
        'logs',
        'config'
    ]
    
    all_exist = True
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✓ {directory}")
        else:
            print(f"✗ {directory} - Missing")
            all_exist = False
    
    return all_exist

def check_sample_data():
    """Check if sample data exists."""
    sample_file = Path('data/input/sample_data.csv')
    if sample_file.exists():
        print("✓ Sample data available")
        return True
    else:
        print("✗ Sample data missing")
        return False

def run_basic_test():
    """Run a basic functionality test."""
    try:
        result = subprocess.run([
            sys.executable, 'main.py', '--input', 'data/input/sample_data.csv',
            '--output', 'data/output', '--auto-crm', '--include-plots',
            '--output-format', 'both', '--verbose'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ Basic functionality test passed")
            return True
        else:
            print(f"✗ Basic functionality test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Test error: {e}")
        return False

if __name__ == "__main__":
    print("LogiQore Reporter - Health Check")
    print("=" * 50)
    
    checks = [
        ("Python Imports", check_python_imports),
        ("Configuration", check_configuration),
        ("Directories", check_directories),
        ("Sample Data", check_sample_data),
        ("Basic Test", run_basic_test)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n{name}:")
        if check_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Health Check Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("✓ Application is healthy and ready for use")
        sys.exit(0)
    else:
        print("✗ Application has issues that need attention")
        sys.exit(1)
