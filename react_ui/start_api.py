#!/usr/bin/env python3
"""
LogiQore Reporter API server launcher.

Starts the FastAPI backend server and serves the React web UI.
The React UI is the primary interface - when a production build exists
in dist/, it will be served automatically at http://localhost:8000.

All API routes are prefixed with /api/ to avoid conflicts with the
React Router catch-all.
"""

import os
import sys
from pathlib import Path


# Configuration
HOST = "0.0.0.0"
PORT = int(os.environ.get("LOGIQORE_PORT", 8000))
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
DIST_DIR = SCRIPT_DIR / "dist"


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


def create_app():
    """Create and configure the FastAPI application with React UI serving."""
    from fastapi import FastAPI, Request
    from fastapi.responses import FileResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="LogiQore Reporter API",
        description="QAQC Report Generator - Analysis Backend",
        version="2.0.0",
    )

    # CORS middleware (needed in dev when React runs on different port)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add project root to path for imports
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

    # Import and include the existing API router
    try:
        from api.main import app as api_app
        for route in api_app.routes:
            app.routes.append(route)
    except ImportError:
        pass  # API module not available, serve UI only

    @app.get("/api/health")
    async def health_check():
        """Health check endpoint."""
        return JSONResponse({"status": "ok", "version": "2.0.0"})

    # React Static File Serving
    # Serves the compiled React build from dist/
    # Must come AFTER all API route registrations

    if DIST_DIR.exists() and (DIST_DIR / "index.html").exists():
        assets_dir = DIST_DIR / "assets"
        if assets_dir.exists():
            app.mount(
                "/assets",
                StaticFiles(directory=str(assets_dir)),
                name="static_assets",
            )

        @app.get("/favicon.ico")
        async def favicon():
            favicon_path = DIST_DIR / "favicon.ico"
            if favicon_path.exists():
                return FileResponse(str(favicon_path))
            return JSONResponse({"error": "not found"}, status_code=404)

        # Catch-all: serves index.html for React Router
        @app.get("/{path:path}")
        async def serve_react_app(request: Request, path: str):
            if "." in path:
                file_path = DIST_DIR / path
                if file_path.exists() and file_path.is_file():
                    return FileResponse(str(file_path))
            return FileResponse(str(DIST_DIR / "index.html"))

        print(f"\n{'='*60}")
        print(f"  LogiQore Reporter - Web UI")
        print(f"  Open your browser to: http://localhost:{PORT}")
        print(f"  API docs: http://localhost:{PORT}/docs")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print(f"  LogiQore Reporter - API Only Mode")
        print(f"  React build not found at: {DIST_DIR}")
        print(f"  To build: cd react_ui && npm install && npm run build")
        print(f"  API available at: http://localhost:{PORT}/api/")
        print(f"{'='*60}\n")

    return app


def main():
    """Entry point: check deps, create app, run server."""
    print("=" * 60)
    print("LogiQore Reporter")
    print("=" * 60)

    missing = check_dependencies()
    if missing:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        print("\nInstall them with:")
        print(f"  pip install {' '.join(missing)}")
        print("\nOr install all API requirements:")
        print("  pip install -r requirements-web.txt")
        sys.exit(1)

    print("Dependencies loaded")

    import uvicorn

    os.chdir(SCRIPT_DIR)

    uvicorn.run(
        "start_api:create_app",
        factory=True,
        host=HOST,
        port=PORT,
        reload=True,
        reload_dirs=[str(SCRIPT_DIR / "api")],
    )


if __name__ == "__main__":
    main()
