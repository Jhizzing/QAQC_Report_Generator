#!/usr/bin/env python3
"""
Daily Monitoring Script for QAQC Analysis Application
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

def check_log_files():
    """Check log files for errors and warnings."""
    log_dir = Path('logs')
    if not log_dir.exists():
        print("No logs directory found")
        return
    
    error_count = 0
    warning_count = 0
    
    for log_file in log_dir.glob('*.log'):
        with open(log_file, 'r') as f:
            for line in f:
                if 'ERROR' in line:
                    error_count += 1
                elif 'WARNING' in line:
                    warning_count += 1
    
    print(f"Errors: {error_count}, Warnings: {warning_count}")
    return error_count, warning_count

def check_disk_space():
    """Check available disk space."""
    import shutil
    
    total, used, free = shutil.disk_usage('.')
    free_gb = free // (1024**3)
    
    print(f"Free disk space: {free_gb} GB")
    return free_gb

def check_output_files():
    """Check output directory for recent files."""
    output_dir = Path('data/output')
    if not output_dir.exists():
        print("No output directory found")
        return 0
    
    recent_files = 0
    cutoff = datetime.now() - timedelta(days=1)
    
    for file in output_dir.rglob('*'):
        if file.is_file() and datetime.fromtimestamp(file.stat().st_mtime) > cutoff:
            recent_files += 1
    
    print(f"Recent output files: {recent_files}")
    return recent_files

if __name__ == "__main__":
    print(f"Daily monitoring report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    errors, warnings = check_log_files()
    free_space = check_disk_space()
    recent_files = check_output_files()
    
    print("=" * 50)
    print("Monitoring complete")
