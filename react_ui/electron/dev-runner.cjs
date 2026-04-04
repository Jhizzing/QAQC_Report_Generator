#!/usr/bin/env node
// ============================================================================
// LogiQore Reporter — Electron Development Runner
// ============================================================================
// Orchestrates all three processes for local development:
//   1. FastAPI backend (Python)   → port 8000
//   2. Vite dev server (React)    → port 5173
//   3. Electron window            → loads localhost:5173
//
// Usage:  npm run electron:dev
// ============================================================================

const { spawn, execSync } = require('child_process');
const http = require('http');
const path = require('path');

const REACT_UI_DIR = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(REACT_UI_DIR, '..');
const FASTAPI_PORT = 8000;
const VITE_PORT = 5173;

const processes = [];
let isShuttingDown = false;

// ─── Utilities ─────────────────────────────────────────────

function log(source, msg) {
  const colors = {
    FastAPI: '\x1b[33m',   // Yellow
    Vite: '\x1b[36m',      // Cyan
    Electron: '\x1b[35m',  // Magenta
    Runner: '\x1b[32m',    // Green
  };
  const reset = '\x1b[0m';
  const color = colors[source] || '';
  console.log(`${color}[${source}]${reset} ${msg}`);
}

function waitForServer(port, label, timeoutMs = 30000) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    function poll() {
      if (Date.now() - start > timeoutMs) {
        reject(new Error(`${label} did not start within ${timeoutMs / 1000}s`));
        return;
      }
      const req = http.get(`http://localhost:${port}`, (res) => {
        // Must consume response body to free the socket
        res.resume();
        log(label, `Server ready (status ${res.statusCode})`);
        resolve();
      });
      req.on('error', () => setTimeout(poll, 500));
      req.setTimeout(3000, () => {
        req.destroy();
        setTimeout(poll, 500);
      });
    }
    setTimeout(poll, 1000);
  });
}

function findPython() {
  const candidates = process.platform === 'win32'
    ? ['python', 'python3']
    : ['python3', 'python'];

  for (const cmd of candidates) {
    try {
      const ver = execSync(`${cmd} --version 2>&1`, { encoding: 'utf8', timeout: 5000 });
      if (ver.includes('Python 3.')) return cmd;
    } catch (e) { /* next */ }
  }
  return null;
}

function cleanup() {
  if (isShuttingDown) return;
  isShuttingDown = true;
  log('Runner', 'Shutting down all processes...');
  for (const proc of processes) {
    try {
      if (process.platform === 'win32') {
        spawn('taskkill', ['/pid', String(proc.pid), '/f', '/t']);
      } else {
        proc.kill('SIGTERM');
      }
    } catch (e) { /* already dead */ }
  }
  setTimeout(() => process.exit(0), 2000);
}

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
process.on('exit', cleanup);

// ─── Main ──────────────────────────────────────────────────

async function main() {
  log('Runner', '╔══════════════════════════════════════════════╗');
  log('Runner', '║  LogiQore Reporter — Development Mode        ║');
  log('Runner', '╚══════════════════════════════════════════════╝');
  log('Runner', '');

  // 1. Start FastAPI backend
  const python = findPython();
  if (!python) {
    log('FastAPI', 'ERROR: Python 3 not found. Install from https://python.org');
    process.exit(1);
  }

  log('FastAPI', `Starting backend on port ${FASTAPI_PORT}...`);
  const fastapi = spawn(python, [
    '-c',
    `import uvicorn; import os; os.environ["LOGIQORE_PORT"]="${FASTAPI_PORT}"; uvicorn.run("start_api:create_app", factory=True, host="127.0.0.1", port=${FASTAPI_PORT}, reload=True, reload_dirs=["api"], log_level="info")`,
  ], {
    cwd: REACT_UI_DIR,
    env: { ...process.env, LOGIQORE_PORT: String(FASTAPI_PORT) },
    stdio: ['pipe', 'pipe', 'pipe'],
  });

  processes.push(fastapi);
  fastapi.stdout.on('data', (d) => log('FastAPI', d.toString().trim()));
  fastapi.stderr.on('data', (d) => {
    const msg = d.toString().trim();
    if (msg && !msg.includes('WatchFiles')) log('FastAPI', msg);
  });
  fastapi.on('exit', (code) => {
    if (!isShuttingDown) log('FastAPI', `Exited with code ${code}`);
  });

  // 2. Start Vite dev server
  log('Vite', `Starting dev server on port ${VITE_PORT}...`);
  const npmCmd = process.platform === 'win32' ? 'npm.cmd' : 'npm';
  const vite = spawn(npmCmd, ['run', 'dev'], {
    cwd: REACT_UI_DIR,
    env: process.env,
    stdio: ['pipe', 'pipe', 'pipe'],
  });

  processes.push(vite);
  vite.stdout.on('data', (d) => log('Vite', d.toString().trim()));
  vite.stderr.on('data', (d) => {
    const msg = d.toString().trim();
    if (msg) log('Vite', msg);
  });
  vite.on('exit', (code) => {
    if (!isShuttingDown) log('Vite', `Exited with code ${code}`);
  });

  // 3. Wait for both servers to be ready
  try {
    log('Runner', 'Waiting for servers to start...');
    await Promise.all([
      waitForServer(FASTAPI_PORT, 'FastAPI'),
      waitForServer(VITE_PORT, 'Vite'),
    ]);
    log('Runner', 'Both servers ready!');
  } catch (err) {
    log('Runner', `ERROR: ${err.message}`);
    cleanup();
    return;
  }

  // 4. Launch Electron
  log('Electron', 'Opening application window...');

  const electronPath = require('electron');
  const electron = spawn(String(electronPath), ['.'], {
    cwd: REACT_UI_DIR,
    env: {
      ...process.env,
      ELECTRON_DEV: '1',
      LOGIQORE_PORT: String(VITE_PORT), // Point Electron at Vite, not FastAPI
    },
    stdio: 'inherit',
  });

  processes.push(electron);
  electron.on('exit', () => {
    if (!isShuttingDown) {
      log('Electron', 'Window closed. Shutting down...');
      cleanup();
    }
  });

  log('Runner', '');
  log('Runner', `  FastAPI Backend:  http://127.0.0.1:${FASTAPI_PORT}`);
  log('Runner', `  Vite Dev Server:  http://127.0.0.1:${VITE_PORT}`);
  log('Runner', `  API Docs:         http://127.0.0.1:${FASTAPI_PORT}/docs`);
  log('Runner', '');
  log('Runner', '  Press Ctrl+C to stop all processes');
  log('Runner', '');
}

main().catch((err) => {
  console.error('Fatal error:', err);
  cleanup();
});
