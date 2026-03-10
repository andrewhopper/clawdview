# TypeScript Vite Template

Gold standard vanilla TypeScript template with Vite for fast development.

## Features

- **TypeScript**: Strict type checking
- **Vite**: Lightning fast HMR and builds
- **Testing**: Vitest with coverage
- **Utilities**: Result type, debounce/throttle, DOM helpers
- **Config**: Zod-validated environment variables

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test

# Type check
npm run typecheck
```

## Project Structure

```
typescript-vite/
├── src/
│   ├── config.ts     # Configuration management
│   ├── logger.ts     # Structured logging
│   ├── utils.ts      # Utility functions
│   ├── dom.ts        # DOM helpers
│   ├── main.ts       # Entry point
│   └── styles.css    # Styles
├── tests/
│   ├── utils.test.ts
│   └── config.test.ts
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── vitest.config.ts
```

## Configuration

Environment variables are validated with Zod. Use `VITE_` prefix for browser-accessible variables.
