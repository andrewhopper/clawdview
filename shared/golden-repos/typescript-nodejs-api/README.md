# TypeScript Node.js API Template

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://typescriptlang.org)
[![Node](https://img.shields.io/badge/Node.js-20+-green)](https://nodejs.org)

Gold standard TypeScript Node.js API template with Express and Swagger.

## Quick Start

```bash
npm install
cp .env.example .env
npm run dev
```

Visit http://localhost:3000/api/docs for interactive API documentation.

## Features

- **Express** - Fast, unopinionated web framework
- **Swagger/OpenAPI** - Auto-generated API documentation
- **TypeScript** - Full type safety
- **Zod** - Runtime validation
- **Pino** - Structured JSON logging
- **Vitest** - Fast unit testing
- **Docker** - Multi-stage production builds

## Project Structure

```
src/
├── index.ts           # Entry point
├── server.ts          # Express app setup
├── config.ts          # Configuration
├── swagger.ts         # OpenAPI config
├── middleware/        # Express middleware
│   ├── auth.ts        # Authentication
│   ├── errorHandler.ts
│   └── requestId.ts
├── routes/            # API routes
│   ├── health.ts
│   └── items.ts
└── logger.ts          # Logging setup
```

## API Documentation

### Interactive Docs
- Swagger UI: http://localhost:3000/api/docs
- OpenAPI JSON: http://localhost:3000/api/docs.json

### Code Documentation
```bash
npm run docs        # Generate TypeDoc
npm run docs:serve  # Serve locally
```

## Development

```bash
npm run dev          # Start with hot reload
npm test             # Run tests
npm run test:watch   # Watch mode
npm run lint         # Lint code
npm run typecheck    # Type check
npm run build        # Build for production
```

## Docker

```bash
# Development
docker build --target dev -t api:dev .
docker run -p 3000:3000 api:dev

# Production
docker build --target prod -t api:prod .
docker run -p 3000:3000 api:prod
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `NODE_ENV` | Environment | `development` |
| `LOG_LEVEL` | Log level | `info` |

## Authentication

JWT auth middleware included. See `src/middleware/auth.ts`:

```typescript
import { requireAuth, requireRoles } from './middleware/auth.js';

// Require authentication
router.get('/protected', requireAuth, handler);

// Require specific roles
router.get('/admin', requireAuth, requireRoles('admin'), handler);
```

## License

MIT
