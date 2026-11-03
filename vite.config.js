import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    // El fondo 3D (three.js, ~900 kB sin comprimir / ~240 kB gzip) va en su
    // propio archivo y se descarga DESPUÉS de que la página ya se ve, así que
    // no afecta la carga inicial. Subimos el límite para que no avise por él.
    chunkSizeWarningLimit: 1000,
  },
})
