// File UUID: d4e8f9a1-2b3c-4d5e-6f7a-8b9c0d1e2f3a
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// Custom plugin to watch docs directory and trigger HMR
function docsWatcher() {
  return {
    name: 'docs-watcher',
    configureServer(server: any) {
      const docsPath = resolve(__dirname, '../docs')
      server.watcher.add(docsPath)

      server.watcher.on('change', (path: string) => {
        if (path.includes('/docs/') && path.endsWith('.md')) {
          server.ws.send({
            type: 'full-reload',
            path: '*'
          })
        }
      })
    }
  }
}

export default defineConfig({
  plugins: [react(), docsWatcher()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@docs': resolve(__dirname, '../docs')
    }
  },
  server: {
    port: 3000,
    open: true
  }
})
