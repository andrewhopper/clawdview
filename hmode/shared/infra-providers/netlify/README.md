# Netlify Deployment

Configuration and setup for Netlify platform deployment.

---

## Overview

Netlify is a JAMstack platform with excellent static site support. Best for:
- Static sites
- JAMstack applications
- Serverless functions
- Form handling

---

## Quick Start

### 1. Install CLI

```bash
npm i -g netlify-cli
```

### 2. Copy Config

```bash
cp shared/infra-providers/netlify/netlify.toml ./
```

### 3. Deploy

```bash
# Link project (first time)
netlify init

# Deploy to preview
netlify deploy

# Deploy to production
netlify deploy --prod
```

---

## Configuration

### netlify.toml

| Section | Purpose |
|---------|---------|
| `[build]` | Build settings |
| `[build.environment]` | Build-time env vars |
| `[[redirects]]` | URL redirects |
| `[[headers]]` | Custom headers |
| `[functions]` | Serverless functions config |
| `[dev]` | Local dev server settings |

---

## Environment Variables

### Dashboard
Set in: Netlify Dashboard > Site > Site configuration > Environment variables

### CLI
```bash
netlify env:set MY_VAR value
netlify env:list
```

### Local Development
Create `.env` file (add to .gitignore)

---

## Serverless Functions

### Location
Place functions in `netlify/functions/` or configure in `netlify.toml`:

```toml
[functions]
  directory = "functions"
```

### Example Function

```typescript
// netlify/functions/hello.ts
import type { Handler } from '@netlify/functions';

export const handler: Handler = async (event, context) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello!' }),
  };
};
```

Accessible at: `/.netlify/functions/hello`

---

## Common Commands

```bash
# Deploy
netlify deploy            # Preview deployment
netlify deploy --prod     # Production deployment

# Development
netlify dev               # Local dev server
netlify dev --live        # Live share URL

# Environment
netlify env:set KEY value # Set env var
netlify env:list          # List env vars
netlify env:unset KEY     # Remove env var

# Functions
netlify functions:create  # Scaffold new function
netlify functions:serve   # Local function server

# Logs
netlify logs              # View function logs
```

---

## Forms

Netlify automatically handles forms with `netlify` attribute:

```html
<form name="contact" method="POST" data-netlify="true">
  <input type="text" name="name" />
  <input type="email" name="email" />
  <button type="submit">Send</button>
</form>
```

---

## References

- [Netlify Documentation](https://docs.netlify.com/)
- [netlify.toml Reference](https://docs.netlify.com/configure-builds/file-based-configuration/)
- [CLI Reference](https://docs.netlify.com/cli/get-started/)
