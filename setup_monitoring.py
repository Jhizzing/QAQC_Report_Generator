#!/usr/bin/env python3
"""
Monitoring Setup Script for QAQC Analysis Application

This script sets up monitoring and logging for production use including:
- Logging configuration
- Performance monitoring
- Error tracking
- Usage analytics
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta

def print_status(message, status="INFO"):
    """Print status message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def setup_logging():
    """Set up comprehensive logging configuration."""
    print_status("Setting up logging configuration...")
    
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    # Logging configuration
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s: %(message)s'
            },
            'json': {
                'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'formatter': 'simple',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'DEBUG',
                'formatter': 'detailed',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/qaqc.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'level': 'ERROR',
                'formatter': 'detailed',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/errors.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'performance': {
                'level': 'INFO',
                'formatter': 'json',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/performance.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 10
            }
        },
        'loggers': {
            'qaqc': {
                'handlers': ['console', 'file', 'error_file'],
                'level': 'DEBUG',
                'propagate': False
            },
            'qaqc.performance': {
                'handlers': ['performance'],
                'level': 'INFO',
                'propagate': False
            },
            'qaqc.analysis': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': False
            }
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': 'INFO'
        }
    }
    
    # Write logging configuration
    with open('config/logging.json', 'w') as f:
        json.dump(log_config, f, indent=2)
    
    print_status("  Created: config/logging.json")
    print_status("Logging configuration set up")

def setup_performance_monitoring():
    """Set up performance monitoring configuration."""
    print_status("Setting up performance monitoring...")
    
    # Performance monitoring configuration
    perf_config = {
        'monitoring': {
            'enabled': True,
            'metrics': {
                'processing_time': {
                    'enabled': True,
                    'threshold_seconds': 300  # 5 minutes
                },
                'memory_usage': {
                    'enabled': True,
                    'threshold_mb': 1000  # 1GB
                },
                'file_size': {
                    'enabled': True,
                    'threshold_mb': 100  # 100MB
                },
                'error_rate': {
                    'enabled': True,
                    'threshold_percent': 5  # 5%
                }
            },
            'alerts': {
                'email': {
                    'enabled': False,
                    'recipients': []
                },
                'log': {
                    'enabled': True,
                    'level': 'WARNING'
                }
            }
        },
        'performance': {
            'tracking': {
                'enabled': True,
                'sample_rate': 1.0  # 100% sampling
            },
            'metrics': {
                'data_processing': True,
                'analysis_time': True,
                'visualization_time': True,
                'report_generation': True
            }
        }
    }
    
    # Write performance configuration
    with open('config/monitoring.yaml', 'w') as f:
        yaml.dump(perf_config, f, default_flow_style=False)
    
    print_status("  Created: config/monitoring.yaml")
    print_status("Performance monitoring configured")

def setup_usage_analytics():
    """Set up usage analytics configuration."""
    print_status("Setting up usage analytics...")
    
    # Usage analytics configuration
    analytics_config = {
        'analytics': {
            'enabled': True,
            'privacy': {
                'anonymize_data': True,
                'retention_days': 90
            },
            'tracking': {
                'usage_frequency': True,
                'feature_usage': True,
                'error_patterns': True,
                'performance_metrics': True
            },
            'reports': {
                'daily_summary': True,
                'weekly_report': True,
                'monthly_analysis': True
            }
        },
        'data_collection': {
            'user_actions': True,
            'system_metrics': True,
            'error_events': True,
            'performance_data': True
        }
    }
    
    # Write analytics configuration
    with open('config/analytics.yaml', 'w') as f:
        yaml.dump(analytics_config, f, default_flow_style=False)
    
    print_status("  Created: config/analytics.yaml")
    print_status("Usage analytics configured")

def create_monitoring_scripts():
    """Create monitoring and maintenance scripts."""
    print_status("Creating monitoring scripts...")
    
    # Daily monitoring script
    daily_monitor = """#!/usr/bin/env python3
\"\"\"
Daily Monitoring Script for QAQC Analysis Application
\"\"\"

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

def check_log_files():
    \"\"\"Check log files for errors and warnings.\"\"\"
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
    \"\"\"Check available disk space.\"\"\"
    import shutil
    
    total, used, free = shutil.disk_usage('.')
    free_gb = free // (1024**3)
    
    print(f"Free disk space: {free_gb} GB")
    return free_gb

def check_output_files():
    \"\"\"Check output directory for recent files.\"\"\"
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
"""
    
    with open('scripts/daily_monitor.py', 'w') as f:
        f.write(daily_monitor)
    
    # Make executable
    os.chmod('scripts/daily_monitor.py', 0o755)
    print_status("  Created: scripts/daily_monitor.py")
    
    # Weekly cleanup script
    weekly_cleanup = """#!/usr/bin/env python3
\"\"\"
Weekly Cleanup Script for QAQC Analysis Application
\"\"\"

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def cleanup_old_logs():
    \"\"\"Clean up old log files.\"\"\"
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
    \"\"\"Clean up old output files.\"\"\"
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
    \"\"\"Archive old reports.\"\"\"
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
"""
    
    with open('scripts/weekly_cleanup.py', 'w') as f:
        f.write(weekly_cleanup)
    
    # Make executable
    os.chmod('scripts/weekly_cleanup.py', 0o755)
    print_status("  Created: scripts/weekly_cleanup.py")
    
    print_status("Monitoring scripts created")

def create_health_check():
    """Create health check script."""
    print_status("Creating health check script...")
    
    health_check = """#!/usr/bin/env python3
\"\"\"
Health Check Script for QAQC Analysis Application
\"\"\"

import sys
import subprocess
from pathlib import Path

def check_python_imports():
    \"\"\"Check if all required modules can be imported.\"\"\"
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
    \"\"\"Check if configuration files exist.\"\"\"
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
    \"\"\"Check if required directories exist.\"\"\"
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
    \"\"\"Check if sample data exists.\"\"\"
    sample_file = Path('data/input/sample_data.csv')
    if sample_file.exists():
        print("✓ Sample data available")
        return True
    else:
        print("✗ Sample data missing")
        return False

def run_basic_test():
    \"\"\"Run a basic functionality test.\"\"\"
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
    print("QAQC Analysis Application - Health Check")
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
        print(f"\\n{name}:")
        if check_func():
            passed += 1
    
    print("\\n" + "=" * 50)
    print(f"Health Check Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("✓ Application is healthy and ready for use")
        sys.exit(0)
    else:
        print("✗ Application has issues that need attention")
        sys.exit(1)
"""
    
    with open('scripts/health_check.py', 'w') as f:
        f.write(health_check)
    
    # Make executable
    os.chmod('scripts/health_check.py', 0o755)
    print_status("  Created: scripts/health_check.py")
    
    print_status("Health check script created")

def main():
    """Main monitoring setup function."""
    print_status("=" * 60)
    print_status("QAQC Analysis Application - Monitoring Setup")
    print_status("=" * 60)
    
    # Create scripts directory
    Path("scripts").mkdir(exist_ok=True)
    
    # Set up logging
    setup_logging()
    
    # Set up performance monitoring
    setup_performance_monitoring()
    
    # Set up usage analytics
    setup_usage_analytics()
    
    # Create monitoring scripts
    create_monitoring_scripts()
    
    # Create health check
    create_health_check()
    
    print_status("=" * 60)
    print_status("Monitoring Setup Complete")
    print_status("=" * 60)
    print_status("Monitoring features:")
    print_status("  - Comprehensive logging with rotation")
    print_status("  - Performance monitoring and alerts")
    print_status("  - Usage analytics and reporting")
    print_status("  - Daily monitoring script")
    print_status("  - Weekly cleanup script")
    print_status("  - Health check script")
    print_status("")
    print_status("Next steps:")
    print_status("1. Run: python scripts/health_check.py")
    print_status("2. Set up daily monitoring: python scripts/daily_monitor.py")
    print_status("3. Schedule weekly cleanup: python scripts/weekly_cleanup.py")
    print_status("4. Review monitoring configuration in config/")
    print_status("=" * 60)

if __name__ == "__main__":
    main()
