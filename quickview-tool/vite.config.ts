import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  root: '.',
  build: {
    outDir: 'dist/public',
    emptyOutDir: true,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src/client'),
    },
  },
  server: {
    proxy: {
      '/api': 'http://localhost:3333',
      '/preview': 'http://localhost:3333',
      '/socket.io': {
        target: 'http://localhost:3333',
        ws: true,
      },
    },
  },
});
