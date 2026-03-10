# Vite Reference Example

## Overview
Gold standard Vite configuration for React/TypeScript projects with production optimizations.

## Key Features

### Path Aliases
- `@` → src root
- `@components` → components directory
- `@utils`, `@hooks`, `@types`, etc.
- Clean imports across the project

### Development Server
- Hot Module Replacement (HMR)
- API proxy configuration
- CORS support
- Auto-open browser

### Build Optimization
- Code splitting (manual chunks)
- Asset organization (images, fonts)
- CSS code splitting
- Minification with esbuild
- Source maps configuration

### Environment Management
- `.env` file support
- Environment-specific configs
- Type-safe env variables
- Global constants

## Files
- `vite.config.ts` - Complete Vite configuration

## Usage
```bash
npm install vite @vitejs/plugin-react

# Development
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

## Environment Variables
```env
# .env.local
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=My App
```

## Standards Demonstrated
- **TypeScript:** Full type safety in config
- **Plugins:** React Fast Refresh
- **Aliases:** Organized import paths
- **Optimization:** Manual chunks for caching
- **Proxy:** API request forwarding
- **Build:** Production-ready output structure
