import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8080',
      '/upload': 'http://localhost:8080',
      '/logout': 'http://localhost:8080',
      '/login': 'http://localhost:8080',
      '/entry': 'http://localhost:8080'
    }
  }
})
