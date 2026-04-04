// ============================================================================
// LogiQore Reporter — Electron Preload Script
// ============================================================================
// Exposes a minimal, safe API to the renderer process via contextBridge.
// The React UI can use window.logiqore to detect it's running inside Electron
// and access native features (file dialogs, app info, etc.).
// ============================================================================

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('logiqore', {
  // ─── Environment ──────────────────────────────────────────
  isElectron: true,
  platform: process.platform,
  version: process.env.npm_package_version || '2.0.0',

  // ─── App Info ─────────────────────────────────────────────
  getAppVersion: () => ipcRenderer.invoke('app:version'),

  // ─── Window Controls ─────────────────────────────────────
  minimize: () => ipcRenderer.send('window:minimize'),
  maximize: () => ipcRenderer.send('window:maximize'),
  close: () => ipcRenderer.send('window:close'),

  // ─── Event Listeners ─────────────────────────────────────
  // Listen for menu-triggered events from the main process
  onOpenProject: (callback) => {
    const handler = () => callback();
    document.addEventListener('logiqore:open-project', handler);
    return () => document.removeEventListener('logiqore:open-project', handler);
  },
  onSaveProject: (callback) => {
    const handler = () => callback();
    document.addEventListener('logiqore:save-project', handler);
    return () => document.removeEventListener('logiqore:save-project', handler);
  },
});
