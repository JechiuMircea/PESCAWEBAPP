import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // Configurazioni per build responsive
  build: {
    // Ottimizzazioni CSS per responsive design
    cssCodeSplit: true,
    rollupOptions: {
      output: {
        // Chunk separati per CSS responsive
        manualChunks: {
          'responsive-base': ['react', 'react-dom'],
          'responsive-components': ['./src/components']
        }
      }
    }
  },
  
  // Server di sviluppo con supporto responsive
  server: {
    host: true, // Accesso da dispositivi esterni per testing responsive
    port: 5173
  },
  
  // Preview per testing responsive
  preview: {
    port: 4173,
    host: true
  }
})
