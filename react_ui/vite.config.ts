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
    // Include plotly.js in dependency optimization
    include: ['plotly.js', 'react-plotly.js'],
    esbuildOptions: {
      // Node.js global to browser globalThis
      define: {
        global: 'globalThis',
      },
    },
  },
  build: {
    // Increase chunk size warning limit for Plotly
    chunkSizeWarningLimit: 5000,
    rollupOptions: {
      output: {
        manualChunks: {
          // Separate Plotly into its own chunk for better caching
          plotly: ['plotly.js', 'react-plotly.js'],
        },
      },
    },
  },
})
