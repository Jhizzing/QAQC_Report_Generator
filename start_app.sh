#!/bin/bash

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BACKEND_PORT=8000
FRONTEND_PORT=5173

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting QAQC Report Generator...${NC}"

# 1. Check Prerequisites
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 could not be found.${NC}"
    echo "Please install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm could not be found.${NC}"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# 2. Setup Python Environment
echo "Checking Python environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing/Updating backend dependencies..."
pip install -r requirements.txt > /dev/null

# 3. Setup React Environment
echo "Checking React environment..."
cd react_ui

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies (this may take a minute)..."
    npm install > /dev/null 2>&1
fi

# 4. Start Servers
echo -e "${GREEN}Starting servers...${NC}"

# Cleanup function
cleanup() {
    echo -e "\n${RED}Shutting down...${NC}"
    # Kill the background process groups
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT EXIT

# Start Backend (from react_ui dir where we are)
# Ideally backend should run from root or define python path
# Previously: cd react_ui && python3 -m uvicorn api.main:app
# But requirements.txt in root?
# Let's adjust path.
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Start Backend
# We need to be able to import 'react_ui.api.main' or 'api.main' if in react_ui
# Existing dev workflow: cd react_ui && python3 -m uvicorn api.main:app
# So let's stick to that.
cd react_ui
python3 -m uvicorn api.main:app --host 127.0.0.1 --port $BACKEND_PORT &
BACKEND_PID=$!

# Start Frontend
npm run dev -- --port $FRONTEND_PORT &
FRONTEND_PID=$!

echo -e "${GREEN}Application started!${NC}"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Open your browser to http://localhost:$FRONTEND_PORT"
echo "Press Ctrl+C to stop the application."

wait
