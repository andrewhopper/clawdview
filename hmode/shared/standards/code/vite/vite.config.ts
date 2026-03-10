/**
 * Vite Configuration - Reference Example
 *
 * Demonstrates:
 * - TypeScript configuration
 * - Plugin setup
 * - Path aliases
 * - Build optimization
 * - Development server config
 * - Environment variables
 */

import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load env file based on mode
  const env = loadEnv(mode, process.cwd(), '');

  const isDevelopment = mode === 'development';
  const isProduction = mode === 'production';

  return {
    // Plugins
    plugins: [
      react({
        // Fast refresh
        fastRefresh: true,
        // Babel configuration
        babel: {
          plugins: [
            // Add babel plugins here if needed
          ],
        },
      }),
    ],

    // Path resolution
    resolve: {
      alias: {
        '@': resolve(__dirname, './src'),
        '@components': resolve(__dirname, './src/components'),
        '@utils': resolve(__dirname, './src/utils'),
        '@hooks': resolve(__dirname, './src/hooks'),
        '@types': resolve(__dirname, './src/types'),
        '@assets': resolve(__dirname, './src/assets'),
        '@styles': resolve(__dirname, './src/styles'),
        '@config': resolve(__dirname, './src/config'),
      },
    },

    // Development server
    server: {
      port: 3000,
      host: true, // Listen on all addresses
      strictPort: false, // Try next port if busy
      open: true, // Auto-open browser

      // CORS
      cors: true,

      // Proxy API requests
      proxy: {
        '/api': {
          target: env.VITE_API_URL || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },

      // HMR
      hmr: {
        overlay: true, // Show errors in browser
      },
    },

    // Build options
    build: {
      // Output directory
      outDir: 'dist',

      // Generate sourcemaps for production
      sourcemap: isProduction ? false : true,

      // Chunk size warning limit
      chunkSizeWarningLimit: 1000,

      // Rollup options
      rollupOptions: {
        output: {
          // Manual chunks for better caching
          manualChunks: {
            // Vendor chunk for node_modules
            vendor: [
              'react',
              'react-dom',
              'react-router-dom',
            ],
            // UI library chunk
            ui: [
              // Add UI library imports here
            ],
          },

          // Asset file naming
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name.split('.');
            const ext = info[info.length - 1];

            if (/\.(png|jpe?g|svg|gif|tiff|bmp|ico)$/i.test(assetInfo.name)) {
              return `assets/images/[name]-[hash][extname]`;
            }

            if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name)) {
              return `assets/fonts/[name]-[hash][extname]`;
            }

            return `assets/[name]-[hash][extname]`;
          },

          // Chunk file naming
          chunkFileNames: 'assets/js/[name]-[hash].js',
          entryFileNames: 'assets/js/[name]-[hash].js',
        },
      },

      // Minify options
      minify: 'esbuild',

      // Target browsers
      target: 'es2015',

      // CSS code splitting
      cssCodeSplit: true,
    },

    // CSS options
    css: {
      // CSS modules
      modules: {
        localsConvention: 'camelCase',
      },

      // PostCSS config
      postcss: './postcss.config.js',

      // Preprocessor options
      preprocessorOptions: {
        scss: {
          additionalData: `@import "@/styles/variables.scss";`,
        },
      },
    },

    // Environment variables
    envPrefix: 'VITE_',

    // Define global constants
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
      __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    },

    // Optimizations
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        'react-router-dom',
      ],
      exclude: [
        // Exclude dependencies from optimization
      ],
    },

    // Testing
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: './src/test/setup.ts',
      coverage: {
        provider: 'v8',
        reporter: ['text', 'json', 'html'],
      },
    },

    // Preview server (for production build)
    preview: {
      port: 3000,
      host: true,
      strictPort: false,
      open: true,
    },

    // Enable/disable logging
    logLevel: isDevelopment ? 'info' : 'warn',
  };
});
