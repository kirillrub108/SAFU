import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    // Настройка CSP для development с поддержкой расширений браузера
    headers: {
      'Content-Security-Policy': [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' 'wasm-unsafe-eval' chrome-extension: https:",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data: https:",
        "font-src 'self' data:",
        "connect-src 'self' http://localhost:8000 http://127.0.0.1:8000 ws://localhost:5173 ws://127.0.0.1:5173",
        "object-src 'none'",
        "base-uri 'self'",
      ].join('; '),
    },
  },
  // Для production можно настроить более строгий CSP
  build: {
    rollupOptions: {
      output: {
        // Генерируем nonce для inline скриптов в production
        manualChunks: undefined,
      },
    },
  },
})

