# Next.js Template

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://typescriptlang.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org)

Gold standard Next.js template with App Router, TypeScript, and Tailwind CSS.

## Quick Start

```bash
npm install
cp .env.example .env
npm run dev
```

Visit http://localhost:3000

## Features

- **Next.js 14** - App Router, Server Components
- **TypeScript** - Full type safety
- **Tailwind CSS** - Utility-first styling
- **Jest + Vitest** - Unit testing
- **Playwright** - E2E testing
- **Docker** - Production-ready builds
- **TypeDoc** - API documentation

## Project Structure

```
src/
├── app/               # App Router pages
│   ├── api/           # API routes
│   │   └── health/
│   ├── layout.tsx     # Root layout
│   ├── page.tsx       # Home page
│   └── globals.css    # Global styles
├── lib/               # Utilities
│   ├── auth.ts        # Auth utilities
│   ├── config.ts      # Configuration
│   └── utils.ts       # Helper functions
└── middleware.ts      # Edge middleware
tests/                 # Unit tests
e2e/                   # Playwright E2E tests
```

## Development

```bash
npm run dev          # Start dev server
npm test             # Run Jest tests
npm run test:vitest  # Run Vitest tests
npm run test:e2e     # Run Playwright E2E
npm run lint         # Lint code
npm run typecheck    # Type check
npm run build        # Production build
```

## Documentation

```bash
npm run docs         # Generate TypeDoc
npm run docs:serve   # Serve locally
```

## Testing

### Unit Tests (Jest)
```bash
npm test             # Run all tests
npm run test:watch   # Watch mode
npm run test:coverage # With coverage
```

### E2E Tests (Playwright)
```bash
npm run test:e2e     # Run E2E tests
npm run test:e2e:ui  # Interactive UI mode
```

## Docker

```bash
# Build and run
docker build -t nextjs:prod .
docker run -p 3000:3000 nextjs:prod
```

Note: Requires `output: 'standalone'` in `next.config.mjs`.

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Environment | `development` |
| `NEXT_PUBLIC_*` | Client-side env vars | - |

## Authentication

Cookie-based auth utilities in `src/lib/auth.ts`:

```typescript
import { getCurrentUser, requireAuth } from '@/lib/auth';

// Server Component
export default async function Page() {
  const user = await getCurrentUser();
  // or: const user = await requireAuth(); // redirects if not auth'd
}
```

## Middleware

Edge middleware in `src/middleware.ts`:
- Adds security headers
- Request ID tracking
- Auth redirects (optional)

## License

MIT
