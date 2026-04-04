/**
 * Type declarations for the LogiQore Electron preload API.
 *
 * When running inside Electron, `window.logiqore` is exposed via contextBridge.
 * In a regular browser this will be `undefined`.
 *
 * Usage:
 *   if (window.logiqore?.isElectron) {
 *     // Running inside the desktop app
 *   }
 */

export interface LogiQoreElectronAPI {
  /** Always true when running inside the Electron wrapper */
  isElectron: true;
  /** OS platform: 'darwin' | 'win32' | 'linux' */
  platform: NodeJS.Platform;
  /** App version string */
  version: string;

  /** Get the Electron app version */
  getAppVersion: () => Promise<string>;

  /** Window controls */
  minimize: () => void;
  maximize: () => void;
  close: () => void;

  /** Listen for menu events dispatched from the main process */
  onOpenProject: (callback: () => void) => () => void;
  onSaveProject: (callback: () => void) => () => void;
}

declare global {
  interface Window {
    logiqore?: LogiQoreElectronAPI;
  }
}
