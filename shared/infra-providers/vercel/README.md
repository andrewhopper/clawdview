# Vercel Deployment

Configuration and setup for Vercel platform deployment.

---

## Overview

Vercel is the platform created by the Next.js team. Best for:
- Next.js applications (first-class support)
- Edge functions
- Instant rollbacks
- Preview deployments

---

## Quick Start

### 1. Install CLI

```bash
npm i -g vercel
```

### 2. Copy Config

```bash
cp shared/infra-providers/vercel/vercel.json ./
```

### 3. Deploy

```bash
# Link project (first time)
vercel link

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

---

## Configuration

### vercel.json

| Field | Purpose |
|-------|---------|
| `buildCommand` | Custom build command |
| `outputDirectory` | Build output folder |
| `framework` | Auto-detected framework |
| `rewrites` | URL rewrites |
| `redirects` | URL redirects |
| `headers` | Custom headers |
| `env` | Environment variables |

---

## Environment Variables

### Dashboard
Set in: Vercel Dashboard > Project > Settings > Environment Variables

### CLI
```bash
vercel env add MY_VAR
```

### Local Development
Create `.env.local` (gitignored by default)

---

## Framework Presets

Vercel auto-detects frameworks. Override with `vercel.json`:

| Framework | Build Command | Output |
|-----------|---------------|--------|
| Next.js | `next build` | `.next` |
| Vite | `vite build` | `dist` |
| Create React App | `react-scripts build` | `build` |
| Astro | `astro build` | `dist` |

---

## Edge Functions

```typescript
// api/edge-function.ts
export const config = {
  runtime: 'edge',
};

export default function handler(request: Request) {
  return new Response('Hello from the Edge!');
}
```

---

## Common Commands

```bash
# Deploy
vercel                    # Preview deployment
vercel --prod             # Production deployment

# Environment
vercel env ls             # List env vars
vercel env add NAME       # Add env var
vercel env rm NAME        # Remove env var
vercel env pull           # Pull to .env.local

# Domains
vercel domains ls         # List domains
vercel domains add DOMAIN # Add domain

# Logs
vercel logs               # View deployment logs
```

---

## References

- [Vercel Documentation](https://vercel.com/docs)
- [vercel.json Reference](https://vercel.com/docs/projects/project-configuration)
- [CLI Reference](https://vercel.com/docs/cli)
