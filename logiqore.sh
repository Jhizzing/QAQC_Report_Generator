#!/usr/bin/env bash
# ============================================================================
# LogiQore Reporter - Primary Launcher (macOS / Linux)
# ============================================================================
# Starts the React web UI via FastAPI and opens it in your default browser.
#
# Usage:
#   ./logiqore.sh              Start on default port 8000
#   ./logiqore.sh --port 9000  Start on custom port
#   ./logiqore.sh --no-browser Start without opening browser
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-8000}"
OPEN_BROWSER=true
PID_FILE="$SCRIPT_DIR/.logiqore-server.pid"

# ─── Parse Arguments ─────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --port)
            PORT="$2"
            shift 2
            ;;
        --no-browser)
            OPEN_BROWSER=false
            shift
            ;;
        --help|-h)
            echo "LogiQore Reporter - Web UI Launcher"
            echo ""
            echo "Usage: ./logiqore.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --port PORT     Set the server port (default: 8000)"
            echo "  --no-browser    Don't open the browser automatically"
            echo "  --help, -h      Show this help message"
            echo ""
            echo "The desktop GUI is also available:"
            echo "  ./LogiQore-Reporter-Desktop"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Run './logiqore.sh --help' for usage information."
            exit 1
            ;;
    esac
done

# ─── Check Python ────────────────────────────────────────────
echo "LogiQore Reporter - Starting Web UI..."
echo ""

if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "ERROR: Python 3 is required but not found."
    echo ""
    echo "Please install Python 3.11 or later:"
    echo "  macOS:  brew install python3"
    echo "  Ubuntu: sudo apt install python3 python3-pip"
    echo ""
    echo "Alternatively, use the desktop GUI:"
    echo "  ./LogiQore-Reporter-Desktop"
    exit 1
fi

# Verify Python version >= 3.11
PY_VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")

if [[ "$PY_MAJOR" -lt 3 ]] || [[ "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 11 ]]; then
    echo "WARNING: Python $PY_VERSION detected. Python 3.11+ is recommended."
    echo "Some features may not work correctly."
    echo ""
fi

# ─── Install Dependencies ────────────────────────────────────
REQUIREMENTS="$SCRIPT_DIR/requirements-web.txt"
if [[ -f "$REQUIREMENTS" ]]; then
    echo "Checking Python dependencies..."
    $PYTHON -m pip install -q -r "$REQUIREMENTS" 2>/dev/null || {
        echo "Installing Python dependencies..."
        $PYTHON -m pip install -r "$REQUIREMENTS"
    }
fi

# ─── Check React Build ──────────────────────────────────────
DIST_DIR="$SCRIPT_DIR/react_ui/dist"
if [[ ! -f "$DIST_DIR/index.html" ]]; then
    echo "ERROR: React build not found at $DIST_DIR"
    echo "The web UI has not been compiled. This usually means the"
    echo "release package is incomplete."
    echo ""
    echo "If you have Node.js installed, you can build it manually:"
    echo "  cd react_ui && npm install && npm run build"
    echo ""
    echo "Alternatively, use the desktop GUI:"
    echo "  ./LogiQore-Reporter-Desktop"
    exit 1
fi

# ─── Stop Previous Instance ──────────────────────────────────
if [[ -f "$PID_FILE" ]]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "Stopping previous server instance (PID: $OLD_PID)..."
        kill "$OLD_PID" 2>/dev/null || true
        sleep 1
    fi
    rm -f "$PID_FILE"
fi

# ─── Start Server ────────────────────────────────────────────
echo "Starting LogiQore Reporter on http://localhost:$PORT ..."
echo ""

cd "$SCRIPT_DIR/react_ui"

$PYTHON -c "
import uvicorn
import os
os.environ['LOGIQORE_PORT'] = '$PORT'
uvicorn.run(
    'start_api:create_app',
    factory=True,
    host='0.0.0.0',
    port=$PORT,
    reload=False,
    log_level='info',
)
" &

SERVER_PID=$!
echo "$SERVER_PID" > "$PID_FILE"

# ─── Wait for Server Ready ──────────────────────────────────
echo "Waiting for server to start..."
MAX_WAIT=15
WAITED=0
while [[ $WAITED -lt $MAX_WAIT ]]; do
    if curl -s "http://localhost:$PORT/api/health" >/dev/null 2>&1; then
        break
    fi
    sleep 1
    WAITED=$((WAITED + 1))
done

if [[ $WAITED -ge $MAX_WAIT ]]; then
    echo "WARNING: Server may not have started correctly."
    echo "Check the terminal output for errors."
fi

# ─── Open Browser ────────────────────────────────────────────
if [[ "$OPEN_BROWSER" = true ]]; then
    URL="http://localhost:$PORT"
    echo ""
    echo "Opening $URL in your browser..."

    if command -v xdg-open &>/dev/null; then
        xdg-open "$URL" 2>/dev/null &
    elif command -v open &>/dev/null; then
        open "$URL" 2>/dev/null &
    else
        echo "Could not detect browser. Please open: $URL"
    fi
fi

echo ""
echo "============================================================"
echo "  LogiQore Reporter is running at http://localhost:$PORT"
echo "  Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

# ─── Wait for Server Process ────────────────────────────────
cleanup() {
    echo ""
    echo "Shutting down LogiQore Reporter..."
    kill "$SERVER_PID" 2>/dev/null || true
    rm -f "$PID_FILE"
    echo "Server stopped."
}

trap cleanup EXIT INT TERM

wait "$SERVER_PID"
