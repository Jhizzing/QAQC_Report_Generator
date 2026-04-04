// ============================================================================
// LogiQore Reporter — electron-builder Configuration
// ============================================================================
// Builds native installers for Windows (.exe), macOS (.dmg), and Linux (.AppImage).
//
// Usage:
//   npm run electron:build          # Build for current platform
//   npm run electron:build:win      # Windows NSIS installer
//   npm run electron:build:mac      # macOS DMG
//   npm run electron:build:linux    # Linux AppImage
// ============================================================================

/** @type {import('electron-builder').Configuration} */
module.exports = {
  appId: 'io.logiqore.reporter',
  productName: 'LogiQore Reporter',
  copyright: 'Copyright 2024-2026 LogiQore',

  // ─── Directories ─────────────────────────────────────────
  directories: {
    output: 'release',           // Build output directory
    buildResources: 'electron/resources',
  },

  // ─── Files to Include ────────────────────────────────────
  files: [
    'electron/**/*',             // Electron main process + preload
    '!electron/dev-runner.cjs',  // Exclude dev-only script
  ],

  // ─── Extra Resources (bundled alongside app) ─────────────
  // These are copied to app.asar.unpacked/resources/ or Contents/Resources/
  extraResources: [
    {
      from: 'dist',              // React production build
      to: 'dist',
      filter: ['**/*'],
    },
    {
      from: 'start_api.py',      // FastAPI server entry
      to: 'start_api.py',
    },
    {
      from: 'api',               // FastAPI routes
      to: 'api',
      filter: ['**/*.py'],
    },
    {
      from: '../src',            // Python analysis engine
      to: 'src',
      filter: ['**/*.py', '**/*.yaml', '**/*.yml', '**/*.json'],
    },
    {
      from: '../config.yaml',    // App config
      to: 'config.yaml',
    },
    {
      from: '../crm_database.yaml', // CRM reference data
      to: 'crm_database.yaml',
    },
    {
      from: '../requirements-web.txt',
      to: 'requirements-web.txt',
    },
    {
      from: 'electron/resources/icon.png',
      to: 'icon.png',
    },
  ],

  // ─── macOS ───────────────────────────────────────────────
  mac: {
    category: 'public.app-category.developer-tools',
    icon: 'electron/resources/icon.png',
    target: [
      { target: 'dmg', arch: ['x64', 'arm64'] },
    ],
    darkModeSupport: true,
  },

  dmg: {
    title: 'LogiQore Reporter',
    backgroundColor: '#0F172A',
    window: {
      width: 540,
      height: 380,
    },
    contents: [
      { x: 140, y: 180 },
      { x: 400, y: 180, type: 'link', path: '/Applications' },
    ],
  },

  // ─── Windows ─────────────────────────────────────────────
  win: {
    icon: 'electron/resources/icon.png',
    target: [
      { target: 'nsis', arch: ['x64'] },
    ],
  },

  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true,
    installerIcon: 'electron/resources/icon.png',
    uninstallerIcon: 'electron/resources/icon.png',
    installerHeaderIcon: 'electron/resources/icon.png',
    createDesktopShortcut: true,
    createStartMenuShortcut: true,
    shortcutName: 'LogiQore Reporter',
    license: '../LICENSE',
  },

  // ─── Linux ───────────────────────────────────────────────
  linux: {
    icon: 'electron/resources/icon.png',
    category: 'Science',
    target: [
      { target: 'AppImage', arch: ['x64'] },
      { target: 'deb', arch: ['x64'] },
    ],
    desktop: {
      Name: 'LogiQore Reporter',
      Comment: 'Geological QAQC Analysis Platform',
      Categories: 'Science;Education;Development',
    },
  },

  // ─── Publish (for auto-update, optional) ─────────────────
  publish: null, // Disable auto-publish; releases are handled by GitHub Actions
};
