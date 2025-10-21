#!/usr/bin/env python3
"""
Production Setup Script for QAQC Analysis Application

This script automates the production setup process including:
- Directory structure creation
- Configuration file setup
- Environment validation
- Initial testing
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import yaml
from datetime import datetime

def print_status(message, status="INFO"):
    """Print status message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def check_python_version():
    """Check if Python version is compatible."""
    print_status("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print_status(f"ERROR: Python 3.11+ required, found {version.major}.{version.minor}", "ERROR")
        return False
    print_status(f"Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_dependencies():
    """Check if required dependencies are available."""
    print_status("Checking dependencies...")
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'openpyxl', 'yaml'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print_status(f"  {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print_status(f"  {package} - MISSING", "WARNING")
    
    if missing_packages:
        print_status(f"Missing packages: {', '.join(missing_packages)}", "WARNING")
        print_status("Run: pip install -r requirements.txt", "INFO")
        return False
    
    print_status("All dependencies available")
    return True

def create_directory_structure():
    """Create production directory structure."""
    print_status("Creating directory structure...")
    
    directories = [
        "config",
        "data/input",
        "data/output",
        "data/backup",
        "logs",
        "reports",
        "plots"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print_status(f"  Created: {directory}")
    
    print_status("Directory structure created")

def setup_configuration():
    """Set up production configuration files."""
    print_status("Setting up configuration files...")
    
    # Production configuration
    production_config = {
        'data': {
            'cleaning': {
                'default_detection_limit': 0.01,
                'normalize_sample_types': True,
                'csv_delimiter': ',',
                'encoding': 'utf-8'
            }
        },
        'analysis': {
            'standards': {
                'z_score_threshold': 2.0,
                'recovery_limits': [95, 105],
                'precision_threshold': 5.0
            },
            'blanks': {
                'contamination_threshold': 3.0,
                'carryover_threshold': 2.0,
                'blank_limit': 0.01
            },
            'duplicates': {
                'rpd_threshold': 20.0,
                'precision_limit': 10.0,
                'nugget_threshold': 0.5
            }
        },
        'visualization': {
            'figure_size': [10, 8],
            'dpi': 300,
            'style': 'seaborn-v0_8'
        },
        'reporting': {
            'include_plots': True,
            'include_raw_data': True,
            'page_size': 'A4',
            'margins': [1, 1, 1, 1]
        }
    }
    
    # Write production configuration
    with open('config/production.yaml', 'w') as f:
        yaml.dump(production_config, f, default_flow_style=False)
    print_status("  Created: config/production.yaml")
    
    # Copy CRM database if it exists
    if Path('crm_database.yaml').exists():
        shutil.copy('crm_database.yaml', 'data/crm_database.yaml')
        print_status("  Copied: data/crm_database.yaml")
    else:
        print_status("  Warning: crm_database.yaml not found", "WARNING")
    
    print_status("Configuration files set up")

def create_sample_data():
    """Create sample data for testing."""
    print_status("Creating sample data...")
    
    sample_data = """sample_id,sample_type,result,qualifier,detection_limit,lab_batch,analysis_date,analyst,method
STD-001,STANDARD,0.85,,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay
STD-002,STANDARD,0.87,,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay
STD-003,STANDARD,0.83,,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay
BLK-001,BLANK,0.01,,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay
BLK-002,BLANK,0.02,,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay
DUP-001,DUPLICATE,1.25,,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay
DUP-001,DUPLICATE,1.28,,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay
SMP-001,SAMPLE,1.5,,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay
SMP-002,SAMPLE,2.1,,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay
SMP-003,SAMPLE,0.005,<DL,0.01,BATCH-001,2025-10-21,Analyst A,Fire Assay"""
    
    with open('data/input/sample_data.csv', 'w') as f:
        f.write(sample_data)
    print_status("  Created: data/input/sample_data.csv")
    
    print_status("Sample data created")

def run_initial_test():
    """Run initial test to verify installation."""
    print_status("Running initial test...")
    
    try:
        # Test basic import
        from src.data.importer import DataImporter
        from src.analysis import StandardsAnalyzer, BlanksAnalyzer, DuplicatesAnalyzer
        from src.visualization import PlotGenerator
        from src.reporting import ExcelReporter, PDFReporter
        print_status("  Module imports - OK")
        
        # Test main application
        result = subprocess.run([
            sys.executable, 'main.py', '--input', 'data/input/sample_data.csv',
            '--output', 'data/output', '--auto-crm', '--include-plots',
            '--output-format', 'both', '--verbose'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print_status("  Application test - OK")
            print_status("  Output files created in data/output/")
        else:
            print_status(f"  Application test - FAILED", "ERROR")
            print_status(f"  Error: {result.stderr}", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"  Test failed: {e}", "ERROR")
        return False
    
    print_status("Initial test completed successfully")
    return True

def create_startup_script():
    """Create startup script for easy execution."""
    print_status("Creating startup script...")
    
    # Windows batch file
    windows_script = """@echo off
echo Starting QAQC Analysis Application...
python main.py %*
pause
"""
    
    with open('run_qaqc.bat', 'w') as f:
        f.write(windows_script)
    print_status("  Created: run_qaqc.bat")
    
    # Unix shell script
    unix_script = """#!/bin/bash
echo "Starting QAQC Analysis Application..."
python main.py "$@"
"""
    
    with open('run_qaqc.sh', 'w') as f:
        f.write(unix_script)
    
    # Make executable
    os.chmod('run_qaqc.sh', 0o755)
    print_status("  Created: run_qaqc.sh")
    
    print_status("Startup scripts created")

def create_logging_config():
    """Set up logging configuration."""
    print_status("Setting up logging...")
    
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            }
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': 'logs/qaqc.log',
                'mode': 'a',
            }
        },
        'loggers': {
            '': {
                'handlers': ['default', 'file'],
                'level': 'INFO',
                'propagate': False
            }
        }
    }
    
    import json
    with open('config/logging.json', 'w') as f:
        json.dump(log_config, f, indent=2)
    
    print_status("  Created: config/logging.json")
    print_status("Logging configured")

def main():
    """Main setup function."""
    print_status("=" * 60)
    print_status("QAQC Analysis Application - Production Setup")
    print_status("=" * 60)
    
    # Check system requirements
    if not check_python_version():
        print_status("Setup failed: Python version incompatible", "ERROR")
        sys.exit(1)
    
    if not check_dependencies():
        print_status("Setup failed: Missing dependencies", "ERROR")
        print_status("Please run: pip install -r requirements.txt", "INFO")
        sys.exit(1)
    
    # Create directory structure
    create_directory_structure()
    
    # Set up configuration
    setup_configuration()
    
    # Create sample data
    create_sample_data()
    
    # Set up logging
    create_logging_config()
    
    # Create startup scripts
    create_startup_script()
    
    # Run initial test
    if not run_initial_test():
        print_status("Setup completed with warnings", "WARNING")
        print_status("Please check the test results and fix any issues", "INFO")
    else:
        print_status("Setup completed successfully!", "SUCCESS")
    
    print_status("=" * 60)
    print_status("Production Setup Complete")
    print_status("=" * 60)
    print_status("Next steps:")
    print_status("1. Review configuration in config/production.yaml")
    print_status("2. Add your CRM data to data/crm_database.yaml")
    print_status("3. Test with your laboratory data")
    print_status("4. Train your staff on usage")
    print_status("5. Integrate into your laboratory workflow")
    print_status("")
    print_status("For help, see USER_DEPLOYMENT_GUIDE.md")
    print_status("=" * 60)

if __name__ == "__main__":
    main()
