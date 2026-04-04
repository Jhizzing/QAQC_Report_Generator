// ============================================================================
// LogiQore Reporter — Electron Main Process
// ============================================================================
// Launches the Python FastAPI backend as a child process, waits for it to
// become healthy, then opens a BrowserWindow pointing at localhost.
//
// Handles: app lifecycle, backend spawning, graceful shutdown, port management,
// native menu bar, tray icon, window state persistence.
// ============================================================================

const { app, BrowserWindow, Menu, shell, dialog, Tray, nativeImage } = require('electron');
const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const http = require('http');
const net = require('net');

// ─── Configuration ─────────────────────────────────────────
const APP_NAME = 'LogiQore Reporter';
const DEFAULT_PORT = 8000;
const HEALTH_ENDPOINT = '/api/health';
const HEALTH_TIMEOUT_MS = 30000;   // Max time to wait for backend
const HEALTH_POLL_MS = 500;        // Poll interval
const WINDOW_MIN_WIDTH = 1100;
const WINDOW_MIN_HEIGHT = 700;
const WINDOW_DEFAULT_WIDTH = 1440;
const WINDOW_DEFAULT_HEIGHT = 900;

// ─── Paths ─────────────────────────────────────────────────
const isDev = !app.isPackaged;
const isDevRunner = process.env.ELECTRON_DEV === '1'; // Launched by dev-runner.cjs
const ROOT_DIR = isDev
  ? path.resolve(__dirname, '..')
  : path.resolve(process.resourcesPath);

const REACT_DIST = isDev
  ? path.join(__dirname, '..', 'dist')
  : path.join(process.resourcesPath, 'dist');

const PYTHON_BACKEND = isDev
  ? path.join(__dirname, '..', 'start_api.py')
  : path.join(process.resourcesPath, 'start_api.py');

const LOGO_PATH = isDev
  ? path.join(__dirname, 'resources', 'icon.png')
  : path.join(process.resourcesPath, 'icon.png');

// ─── State ─────────────────────────────────────────────────
let mainWindow = null;
let backendProcess = null;
let tray = null;
let serverPort = DEFAULT_PORT;
let isQuitting = false;

// ─── Window State Persistence ──────────────────────────────
const STATE_FILE = path.join(app.getPath('userData'), 'window-state.json');

function loadWindowState() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    }
  } catch (e) {
    // Ignore corrupted state
  }
  return null;
}

function saveWindowState() {
  if (!mainWindow) return;
  try {
    const bounds = mainWindow.getBounds();
    const isMaximized = mainWindow.isMaximized();
    fs.writeFileSync(STATE_FILE, JSON.stringify({ bounds, isMaximized }));
  } catch (e) {
    // Non-critical
  }
}

// ─── Port Management ───────────────────────────────────────
function findFreePort(startPort) {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.listen(startPort, () => {
      const port = server.address().port;
      server.close(() => resolve(port));
    });
    server.on('error', () => {
      // Port in use, try next
      if (startPort < 65535) {
        resolve(findFreePort(startPort + 1));
      } else {
        reject(new Error('No free port found'));
      }
    });
  });
}

// ─── Python Detection ──────────────────────────────────────
function findPython() {
  // 1. Check for bundled Python (PyInstaller executable)
  const bundledPaths = [
    path.join(process.resourcesPath || '', 'python', 'logiqore-api'),
    path.join(process.resourcesPath || '', 'python', 'logiqore-api.exe'),
  ];
  for (const p of bundledPaths) {
    if (fs.existsSync(p)) return { type: 'bundled', path: p };
  }

  // 2. Check system Python
  const pythonCandidates = process.platform === 'win32'
    ? ['python', 'python3', 'py -3']
    : ['python3', 'python'];

  for (const cmd of pythonCandidates) {
    try {
      const version = execSync(`${cmd} --version 2>&1`, { encoding: 'utf8', timeout: 5000 });
      if (version.includes('Python 3.')) {
        return { type: 'system', path: cmd };
      }
    } catch (e) {
      // Not found, try next
    }
  }

  return null;
}

// ─── Backend Management ────────────────────────────────────
function startBackend(port) {
  return new Promise((resolve, reject) => {
    const python = findPython();

    if (!python) {
      reject(new Error(
        'Python 3 not found.\n\n' +
        'LogiQore Reporter requires Python 3.11+ for the analysis backend.\n\n' +
        'Please install Python from https://python.org'
      ));
      return;
    }

    console.log(`[Electron] Starting backend with ${python.type} Python: ${python.path}`);
    console.log(`[Electron] Backend script: ${PYTHON_BACKEND}`);
    console.log(`[Electron] Port: ${port}`);

    const env = {
      ...process.env,
      LOGIQORE_PORT: String(port),
      PYTHONDONTWRITEBYTECODE: '1',
    };

    if (python.type === 'bundled') {
      // Run the PyInstaller-bundled executable directly
      backendProcess = spawn(python.path, [], {
        env,
        cwd: path.dirname(PYTHON_BACKEND),
        stdio: ['pipe', 'pipe', 'pipe'],
      });
    } else {
      // Run via system Python with uvicorn
      backendProcess = spawn(python.path, [
        '-c',
        `import uvicorn; import os; os.environ["LOGIQORE_PORT"]="${port}"; uvicorn.run("start_api:create_app", factory=True, host="127.0.0.1", port=${port}, log_level="warning")`,
      ], {
        env,
        cwd: path.join(__dirname, '..'),
        stdio: ['pipe', 'pipe', 'pipe'],
      });
    }

    backendProcess.stdout.on('data', (data) => {
      console.log(`[Backend] ${data.toString().trim()}`);
    });

    backendProcess.stderr.on('data', (data) => {
      const msg = data.toString().trim();
      if (msg) console.log(`[Backend] ${msg}`);
    });

    backendProcess.on('error', (err) => {
      console.error(`[Backend] Failed to start: ${err.message}`);
      reject(err);
    });

    backendProcess.on('exit', (code) => {
      console.log(`[Backend] Process exited with code ${code}`);
      if (!isQuitting) {
        // Unexpected exit — show error to user
        dialog.showErrorBox(
          'Backend Error',
          `The analysis backend stopped unexpectedly (code ${code}).\n\nPlease restart ${APP_NAME}.`
        );
      }
      backendProcess = null;
    });

    // Wait for health check
    waitForHealth(port)
      .then(() => resolve(port))
      .catch((err) => {
        stopBackend();
        reject(err);
      });
  });
}

function waitForHealth(port) {
  const startTime = Date.now();

  return new Promise((resolve, reject) => {
    function poll() {
      if (Date.now() - startTime > HEALTH_TIMEOUT_MS) {
        reject(new Error(`Backend did not start within ${HEALTH_TIMEOUT_MS / 1000}s`));
        return;
      }

      const req = http.get(`http://localhost:${port}${HEALTH_ENDPOINT}`, (res) => {
        res.resume(); // Consume response body to free socket
        if (res.statusCode === 200) {
          console.log('[Electron] Backend is healthy');
          resolve();
        } else {
          setTimeout(poll, HEALTH_POLL_MS);
        }
      });

      req.on('error', () => {
        setTimeout(poll, HEALTH_POLL_MS);
      });

      req.setTimeout(2000, () => {
        req.destroy();
        setTimeout(poll, HEALTH_POLL_MS);
      });
    }

    // Give backend a moment to initialize before first poll
    setTimeout(poll, 800);
  });
}

function stopBackend() {
  if (backendProcess) {
    console.log('[Electron] Stopping backend...');
    try {
      // Graceful: SIGTERM on Unix, taskkill on Windows
      if (process.platform === 'win32') {
        spawn('taskkill', ['/pid', String(backendProcess.pid), '/f', '/t']);
      } else {
        backendProcess.kill('SIGTERM');
        // Force kill after 3 seconds if still running
        setTimeout(() => {
          if (backendProcess) {
            try { backendProcess.kill('SIGKILL'); } catch (e) { /* already dead */ }
          }
        }, 3000);
      }
    } catch (e) {
      console.error('[Electron] Error stopping backend:', e.message);
    }
    backendProcess = null;
  }
}

// ─── Window Creation ───────────────────────────────────────
function createWindow(port) {
  const saved = loadWindowState();

  mainWindow = new BrowserWindow({
    width: saved?.bounds?.width || WINDOW_DEFAULT_WIDTH,
    height: saved?.bounds?.height || WINDOW_DEFAULT_HEIGHT,
    x: saved?.bounds?.x,
    y: saved?.bounds?.y,
    minWidth: WINDOW_MIN_WIDTH,
    minHeight: WINDOW_MIN_HEIGHT,
    title: APP_NAME,
    icon: fs.existsSync(LOGO_PATH) ? LOGO_PATH : undefined,
    backgroundColor: '#0F172A', // Slate-900 — matches React UI background
    show: false,                // Show after ready-to-show to avoid flash
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  if (saved?.isMaximized) {
    mainWindow.maximize();
  }

  // Show window once content is painted (no white flash)
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    mainWindow.focus();
  });

  // Save window state on move/resize
  mainWindow.on('resize', saveWindowState);
  mainWindow.on('move', saveWindowState);

  // Handle close vs quit
  mainWindow.on('close', (e) => {
    if (!isQuitting && process.platform === 'darwin') {
      // macOS: hide to dock instead of quitting
      e.preventDefault();
      mainWindow.hide();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Open external links in system browser
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Load the React UI
  mainWindow.loadURL(`http://localhost:${port}`);
}

// ─── Application Menu ──────────────────────────────────────
function createMenu() {
  const isMac = process.platform === 'darwin';

  const template = [
    // App menu (macOS only)
    ...(isMac ? [{
      label: APP_NAME,
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide' },
        { role: 'hideOthers' },
        { role: 'unhide' },
        { type: 'separator' },
        { role: 'quit' },
      ],
    }] : []),

    // File
    {
      label: 'File',
      submenu: [
        {
          label: 'Open Project...',
          accelerator: 'CmdOrCtrl+O',
          click: () => {
            if (mainWindow) {
              mainWindow.webContents.executeJavaScript(
                'document.dispatchEvent(new CustomEvent("logiqore:open-project"))'
              );
            }
          },
        },
        {
          label: 'Save Project',
          accelerator: 'CmdOrCtrl+S',
          click: () => {
            if (mainWindow) {
              mainWindow.webContents.executeJavaScript(
                'document.dispatchEvent(new CustomEvent("logiqore:save-project"))'
              );
            }
          },
        },
        { type: 'separator' },
        isMac ? { role: 'close' } : { role: 'quit' },
      ],
    },

    // Edit
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
        { role: 'selectAll' },
      ],
    },

    // View
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        ...(isDev ? [{ role: 'toggleDevTools' }] : []),
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' },
      ],
    },

    // Window
    {
      label: 'Window',
      submenu: [
        { role: 'minimize' },
        { role: 'zoom' },
        ...(isMac ? [
          { type: 'separator' },
          { role: 'front' },
        ] : [
          { role: 'close' },
        ]),
      ],
    },

    // Help
    {
      label: 'Help',
      submenu: [
        {
          label: 'LogiQore Website',
          click: () => shell.openExternal('https://logiqore.io'),
        },
        {
          label: 'Documentation',
          click: () => shell.openExternal('https://logiqore.io/docs'),
        },
        { type: 'separator' },
        {
          label: 'Report Issue',
          click: () => shell.openExternal('https://github.com/Jhizzing/QAQC_Report_Generator/issues'),
        },
        ...(isDev ? [
          { type: 'separator' },
          {
            label: 'API Documentation',
            click: () => shell.openExternal(`http://127.0.0.1:${serverPort}/docs`),
          },
        ] : []),
      ],
    },
  ];

  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

// ─── Splash / Loading Screen ───────────────────────────────
function createSplashWindow() {
  const splash = new BrowserWindow({
    width: 420,
    height: 320,
    frame: false,
    transparent: true,
    resizable: false,
    alwaysOnTop: true,
    skipTaskbar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  const splashHtml = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
          background: transparent;
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100vh;
          -webkit-app-region: drag;
          user-select: none;
        }
        .container {
          background: #0F172A;
          border: 1px solid #334155;
          border-radius: 20px;
          padding: 48px;
          text-align: center;
          box-shadow: 0 25px 50px rgba(0,0,0,0.5);
          width: 380px;
        }
        .logo {
          width: 80px;
          height: 80px;
          margin: 0 auto 20px;
          border-radius: 16px;
          background: linear-gradient(135deg, #F59E0B, #D97706);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 36px;
          font-weight: 800;
          color: #0F172A;
          box-shadow: 0 0 30px rgba(245, 158, 11, 0.3);
        }
        h1 {
          color: #F8FAFC;
          font-size: 22px;
          font-weight: 700;
          letter-spacing: -0.5px;
          margin-bottom: 6px;
        }
        .subtitle {
          color: #94A3B8;
          font-size: 13px;
          margin-bottom: 28px;
        }
        .progress-track {
          height: 4px;
          background: #1E293B;
          border-radius: 4px;
          overflow: hidden;
          margin-bottom: 14px;
        }
        .progress-bar {
          height: 100%;
          background: linear-gradient(90deg, #F59E0B, #FBBF24);
          border-radius: 4px;
          width: 0%;
          animation: loading 4s ease-in-out forwards;
        }
        @keyframes loading {
          0%   { width: 0%; }
          30%  { width: 40%; }
          60%  { width: 65%; }
          80%  { width: 80%; }
          100% { width: 95%; }
        }
        .status {
          color: #64748B;
          font-size: 12px;
        }
        .dot {
          animation: pulse 1.5s infinite;
          display: inline-block;
        }
        .dot:nth-child(2) { animation-delay: 0.2s; }
        .dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes pulse {
          0%, 80%, 100% { opacity: 0.3; }
          40% { opacity: 1; }
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="logo">LQ</div>
        <h1>LogiQore Reporter</h1>
        <p class="subtitle">Geological QAQC Analysis Platform</p>
        <div class="progress-track">
          <div class="progress-bar"></div>
        </div>
        <p class="status">Starting analysis engine<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></p>
      </div>
    </body>
    </html>
  `;

  splash.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(splashHtml)}`);
  return splash;
}

// ─── App Lifecycle ─────────────────────────────────────────
app.whenReady().then(async () => {
  console.log(`[Electron] ${APP_NAME} starting...`);
  console.log(`[Electron] isDev: ${isDev}, isDevRunner: ${isDevRunner}`);
  console.log(`[Electron] resourcesPath: ${process.resourcesPath || 'N/A'}`);

  if (isDevRunner) {
    // ── Dev mode: dev-runner.cjs already started Vite + FastAPI ──
    // Just read the port from env and open the window
    serverPort = parseInt(process.env.LOGIQORE_PORT || '5173', 10);
    console.log(`[Electron] Dev mode — connecting to Vite at port ${serverPort}`);

    createMenu();
    createWindow(serverPort);

    // DevTools available via View > Toggle Developer Tools (Cmd+Option+I)

  } else {
    // ── Production mode: spawn backend ourselves ──
    const splash = createSplashWindow();

    try {
      // Find a free port
      serverPort = await findFreePort(DEFAULT_PORT);
      console.log(`[Electron] Using port ${serverPort}`);

      // Start the Python backend
      await startBackend(serverPort);

      // Backend is ready — create the main window
      createMenu();
      createWindow(serverPort);

      // Close splash once main window is showing
      mainWindow.once('ready-to-show', () => {
        if (splash && !splash.isDestroyed()) {
          splash.close();
        }
      });

    } catch (err) {
      console.error('[Electron] Startup failed:', err.message);
      if (splash && !splash.isDestroyed()) {
        splash.close();
      }

      dialog.showErrorBox(
        `${APP_NAME} - Startup Error`,
        err.message + '\n\nThe application will now close.'
      );
      app.quit();
    }
  }
});

// macOS: re-create window when dock icon clicked
app.on('activate', () => {
  if (mainWindow === null) {
    createWindow(serverPort);
  } else {
    mainWindow.show();
  }
});

// Quit when all windows closed (except macOS)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Graceful shutdown
app.on('before-quit', () => {
  isQuitting = true;
  saveWindowState();
  stopBackend();
});

app.on('will-quit', () => {
  stopBackend();
});

// Security: prevent new webview creation
app.on('web-contents-created', (_, contents) => {
  contents.on('will-attach-webview', (event) => {
    event.preventDefault();
  });
});
