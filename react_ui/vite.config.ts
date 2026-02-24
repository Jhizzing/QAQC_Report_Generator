import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // Base path for asset URLs — must be "/" for FastAPI static serving
  base: "/",

  resolve: {
    alias: {
      // Polyfill buffer for Plotly.js compatibility
      'buffer/': 'buffer/',
    },
  },
  define: {
    // Ensure Buffer is available globally for Plotly
    'global': 'globalThis',
  },
  optimizeDeps: {
    // Include Plotly runtime pieces used by lazy chart components
    include: ['plotly.js-basic-dist-min', 'react-plotly.js/factory'],
    esbuildOptions: {
      // Node.js global to browser globalThis
      define: {
        global: 'globalThis',
      },
    },
  },
  build: {
    // Output directory — FastAPI's start_api.py looks for dist/
    outDir: "dist",
    emptyOutDir: true,
    // Keep warnings visible for oversized bundles
    chunkSizeWarningLimit: 3000,
    rollupOptions: {
      output: {
        manualChunks: {
          // Separate Plotly runtime into its own lazy chunk for better caching
          plotly: ['plotly.js-basic-dist-min', 'react-plotly.js/factory'],
        },
      },
    },
  },
  server: {
    // Dev server proxy — forward /api calls to FastAPI during development
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
