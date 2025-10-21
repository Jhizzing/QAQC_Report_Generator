#!/usr/bin/env python3
"""
Weekly Cleanup Script for QAQC Analysis Application
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def cleanup_old_logs():
    """Clean up old log files."""
    log_dir = Path('logs')
    if not log_dir.exists():
        return
    
    cutoff = datetime.now() - timedelta(days=30)
    removed_count = 0
    
    for log_file in log_dir.glob('*.log.*'):  # Rotated log files
        if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff:
            log_file.unlink()
            removed_count += 1
    
    print(f"Removed {removed_count} old log files")
    return removed_count

def cleanup_old_outputs():
    """Clean up old output files."""
    output_dir = Path('data/output')
    if not output_dir.exists():
        return
    
    cutoff = datetime.now() - timedelta(days=90)
    removed_count = 0
    
    for file in output_dir.rglob('*'):
        if file.is_file() and datetime.fromtimestamp(file.stat().st_mtime) < cutoff:
            file.unlink()
            removed_count += 1
    
    print(f"Removed {removed_count} old output files")
    return removed_count

def archive_reports():
    """Archive old reports."""
    output_dir = Path('data/output')
    archive_dir = Path('data/archive')
    archive_dir.mkdir(exist_ok=True)
    
    cutoff = datetime.now() - timedelta(days=30)
    archived_count = 0
    
    for file in output_dir.rglob('*.pdf'):
        if datetime.fromtimestamp(file.stat().st_mtime) < cutoff:
            shutil.move(str(file), str(archive_dir / file.name))
            archived_count += 1
    
    print(f"Archived {archived_count} old reports")
    return archived_count

if __name__ == "__main__":
    print(f"Weekly cleanup - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    old_logs = cleanup_old_logs()
    old_outputs = cleanup_old_outputs()
    archived_reports = archive_reports()
    
    print("=" * 50)
    print("Cleanup complete")
