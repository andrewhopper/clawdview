# Cloudflare Deployment

Configuration and setup for Cloudflare Pages and Workers.

---

## Overview

Cloudflare offers edge computing with generous free tier. Best for:
- Static sites (unlimited bandwidth)
- Edge workers (serverless at edge)
- Global CDN
- Cost optimization

---

## Products

| Product | Purpose |
|---------|---------|
| Pages | Static site hosting |
| Workers | Serverless functions at edge |
| KV | Key-value storage |
| D1 | SQLite at edge |
| R2 | S3-compatible storage |

---

## Quick Start (Pages)

### 1. Install CLI

```bash
npm i -g wrangler
```

### 2. Login

```bash
wrangler login
```

### 3. Deploy Static Site

```bash
# Direct upload
wrangler pages deploy dist --project-name my-site

# Or connect to Git via Dashboard
```

---

## Quick Start (Workers)

### 1. Copy Config

```bash
cp shared/infra-providers/cloudflare/wrangler.toml ./
```

### 2. Create Worker

```typescript
// src/index.ts
export default {
  async fetch(request: Request): Promise<Response> {
    return new Response('Hello from Workers!');
  },
};
```

### 3. Deploy

```bash
wrangler deploy
```

---

## Configuration

### wrangler.toml

| Field | Purpose |
|-------|---------|
| `name` | Worker/project name |
| `main` | Entry point |
| `compatibility_date` | API version date |
| `routes` | URL patterns |
| `kv_namespaces` | KV bindings |
| `d1_databases` | D1 bindings |
| `r2_buckets` | R2 bindings |
| `vars` | Environment variables |

---

## Environment Variables

### wrangler.toml (non-secret)
```toml
[vars]
MY_VAR = "value"
```

### Secrets (CLI)
```bash
wrangler secret put MY_SECRET
```

### Dashboard
Set in: Workers & Pages > Settings > Variables

---

## Pages Functions

Place functions in `functions/` directory:

```typescript
// functions/api/hello.ts
export const onRequest: PagesFunction = async (context) => {
  return new Response('Hello!');
};
```

Accessible at: `/api/hello`

---

## Common Commands

```bash
# Pages
wrangler pages deploy dist    # Deploy static site
wrangler pages project list   # List projects

# Workers
wrangler deploy               # Deploy worker
wrangler dev                  # Local development
wrangler tail                 # Stream logs

# Secrets
wrangler secret put NAME      # Add secret
wrangler secret list          # List secrets

# KV
wrangler kv namespace create NAME
wrangler kv key put --namespace-id=ID key value

# D1
wrangler d1 create my-database
wrangler d1 execute my-database --file=schema.sql
```

---

## Free Tier Limits

| Resource | Limit |
|----------|-------|
| Pages bandwidth | Unlimited |
| Workers requests | 100,000/day |
| Workers CPU time | 10ms/request |
| KV reads | 100,000/day |
| KV writes | 1,000/day |
| D1 rows read | 5M/day |
| R2 storage | 10 GB |

---

## References

- [Cloudflare Docs](https://developers.cloudflare.com/)
- [Pages Documentation](https://developers.cloudflare.com/pages/)
- [Workers Documentation](https://developers.cloudflare.com/workers/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
