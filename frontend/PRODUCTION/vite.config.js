import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: '127.0.0.1', // Use 127.0.0.1 instead of localhost
    port: 5173,        // Specify the port number if needed
  },

  plugins: [react()],
})
