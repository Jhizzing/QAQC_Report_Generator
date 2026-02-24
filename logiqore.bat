@echo off
REM ============================================================================
REM LogiQore Reporter - Primary Launcher (Windows)
REM ============================================================================
REM Starts the React web UI via FastAPI and opens it in your default browser.
REM
REM Usage:
REM   logiqore.bat                  Start on default port 8000
REM   logiqore.bat --port 9000      Start on custom port
REM   logiqore.bat --no-browser     Start without opening browser
REM ============================================================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PORT=8000"
set "OPEN_BROWSER=1"

REM ─── Parse Arguments ───────────────────────────────────────
:parse_args
if "%~1"=="" goto :args_done
if "%~1"=="--port" (
    set "PORT=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--no-browser" (
    set "OPEN_BROWSER=0"
    shift
    goto :parse_args
)
if "%~1"=="--help" goto :show_help
if "%~1"=="-h" goto :show_help
echo Unknown option: %~1
echo Run 'logiqore.bat --help' for usage information.
exit /b 1

:show_help
echo LogiQore Reporter - Web UI Launcher
echo.
echo Usage: logiqore.bat [OPTIONS]
echo.
echo Options:
echo   --port PORT     Set the server port (default: 8000)
echo   --no-browser    Don't open the browser automatically
echo   --help, -h      Show this help message
echo.
echo The desktop GUI is also available:
echo   LogiQore-Reporter-Desktop.exe
exit /b 0

:args_done

REM ─── Check Python ──────────────────────────────────────────
echo LogiQore Reporter - Starting Web UI...
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    where python3 >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python 3 is required but not found.
        echo.
        echo Please install Python 3.11 or later from:
        echo   https://www.python.org/downloads/
        echo.
        echo Make sure to check "Add Python to PATH" during installation.
        echo.
        echo Alternatively, use the desktop GUI:
        echo   LogiQore-Reporter-Desktop.exe
        pause
        exit /b 1
    )
    set "PYTHON=python3"
) else (
    set "PYTHON=python"
)

REM ─── Install Dependencies ──────────────────────────────────
set "REQUIREMENTS=%SCRIPT_DIR%requirements-web.txt"
if exist "%REQUIREMENTS%" (
    echo Checking Python dependencies...
    %PYTHON% -m pip install -q -r "%REQUIREMENTS%" >nul 2>&1
    if %errorlevel% neq 0 (
        echo Installing Python dependencies...
        %PYTHON% -m pip install -r "%REQUIREMENTS%"
    )
)

REM ─── Check React Build ────────────────────────────────────
set "DIST_DIR=%SCRIPT_DIR%react_ui\dist"
if not exist "%DIST_DIR%\index.html" (
    echo ERROR: React build not found at $DIST_DIR%
    echo The web UI has not been compiled.
    echo.
    echo If you have Node.js installed, you can build it manually:
    echo   cd react_ui ^&^& npm install ^&^& npm run build
    echo.
    echo Alternatively, use the desktop GUI:
    echo   LogiQore-Reporter-Desktop.exe
    pause
    exit /b 1
)

REM ─── Start Server ──────────────────────────────────────────
echo Starting LogiQore Reporter on http://localhost:%PORT% ...
echo.

cd /d "%SCRIPT_DIR%react_ui"

REM Start server in background
start /b "" %PYTHON% -c "import uvicorn; import os; os.environ['LOGIQORE_PORT']='%PORT%'; uvicorn.run('start_api:create_app', factory=True, host='0.0.0.0', port=%PORT%, reload=False, log_level='info')"

REM ─── Wait for Server Ready ────────────────────────────────
echo Waiting for server to start...
set /a "WAITED=0"
set /a "MAX_WAIT=15"

:wait_loop
if %WAITED% geq %MAX_WAIT% goto :wait_done
timeout /t 1 /nobreak >nul 2>&1
%PYTHON% -c "import urllib.request; urllib.request.urlopen('http://localhost:%PORT%/api/health')" >nul 2>&1
if %errorlevel% equ 0 goto :wait_done
set /a "WAITED+=1"
goto :wait_loop

:wait_done

REM ─── Open Browser ──────────────────────────────────────────
if "%OPEN_BROWSER%"=="1" (
    echo.
    echo Opening http://localhost:%PORT% in your browser...
    start "" "http://localhost:%PORT%"
)

echo.
echo ============================================================
echo   LogiQore Reporter is running at http://localhost:%PORT%
echo   Press Ctrl+C to stop the server, or close this window.
echo ============================================================
echo.

REM Keep the window open so the server stays running
%PYTHON% -c "import uvicorn; import os; os.environ['LOGIQORE_PORT']='%PORT%'; uvicorn.run('start_api:create_app', factory=True, host='0.0.0.0', port=%PORT%, reload=False, log_level='info')"
