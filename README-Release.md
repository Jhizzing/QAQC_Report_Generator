# LogiQore Reporter

QAQC analysis and reporting for economic geologists.

## Quick Start (Web UI - Recommended)

The React web interface is the primary way to use LogiQore Reporter.

**Requirements:** Python 3.11+

### macOS / Linux
```bash
chmod +x logiqore.sh
./logiqore.sh
```

### Windows
```
logiqore.bat
```

This will:
1. Install Python dependencies automatically (first run only)
2. Start the analysis server
3. Open the web UI in your default browser at http://localhost:8000

### Options
```
--port 9000      Use a custom port
--no-browser     Start the server without opening a browser
--help           Show all options
```

## Desktop GUI (Alternative)

A native desktop application is also included for users who prefer it.

### macOS / Linux
```bash
./LogiQore-Reporter-Desktop
```

### Windows
```
LogiQore-Reporter-Desktop.exe
```

## Troubleshooting

**"Python not found"**
Install Python 3.11+ from [python.org](https://www.python.org/downloads/).
On Windows, make sure to check "Add Python to PATH" during installation.

**"Port 8000 already in use"**
Use a different port: `./logiqore.sh --port 9000`

**Web UI doesn't load**
Check the terminal for error messages. Make sure no firewall is blocking localhost connections.

## Support

- Website: https://logiqore.io
- Contact: paz@logiqore.io
