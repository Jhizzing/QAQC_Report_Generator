#!/usr/bin/env python3
"""
QAQC API Server Launcher

Quick script to start the FastAPI backend server.
Ensures all dependencies are available and runs uvicorn.
"""

import subprocess
import sys
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed."""
    required = ['fastapi', 'uvicorn', 'pydantic']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing


def main():
    print("=" * 50)
    print("QAQC Analysis API Server")
    print("=" * 50)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("\nInstall them with:")
        print(f"  pip install {' '.join(missing)}")
        print("\nOr install all API requirements:")
        print("  pip install -r react_ui/api/requirements.txt")
        sys.exit(1)
    
    print("✓ Dependencies loaded")
    
    # Add project root to path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root / "src"))
    
    print("✓ Project paths configured")
    print("\n🚀 Starting API server at http://localhost:8000")
    print("   API docs: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop\n")
    
    # Import and run
    import uvicorn
    from api.main import app
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(Path(__file__).parent / "api")]
    )


if __name__ == "__main__":
    main()

