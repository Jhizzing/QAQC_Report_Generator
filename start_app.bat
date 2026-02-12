@echo off
TITLE QAQC Report Generator

echo Starting QAQC Report Generator...

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check Node
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

:: Setup Python Virtual Environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt
) else (
    echo Virtual environment found.
)

:: Install Frontend Dependencies
if not exist "react_ui\node_modules" (
    echo Installing frontend dependencies...
    cd react_ui
    call npm install
    cd ..
)

echo Starting servers...

:: Start Backend
:: Using --app-dir to specify root
start "QAQC Backend" cmd /k "venv\Scripts\python -m uvicorn api.main:app --app-dir react_ui --host 127.0.0.1 --port 8000"

:: Start Frontend
cd react_ui
start "QAQC Frontend" cmd /k "npm run dev -- --host"

echo Application started!
echo Open your browser to http://localhost:5173
echo.
pause
