import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
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
})
