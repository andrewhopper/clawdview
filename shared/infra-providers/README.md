# Infrastructure Providers

Unified deploy configurations, CLI wrappers, and templates for multiple hosting providers.

---

## Overview

This directory provides drop-in configurations and utilities for deploying prototypes to various infrastructure providers. Each provider folder contains:
- README with setup instructions
- Config templates ready for copy/paste
- CLI helper scripts (where applicable)

---

## Provider Comparison

| Provider | Type | Best For | Free Tier | Config File |
|----------|------|----------|-----------|-------------|
| **AWS Amplify** | Full-stack | SSR apps, AWS ecosystem | Limited | `amplify.yml` |
| **Vercel** | Frontend + Edge | Next.js, React | Generous | `vercel.json` |
| **Netlify** | JAMstack | Static sites, serverless | Generous | `netlify.toml` |
| **Heroku** | PaaS | Traditional apps, Postgres | Eco dynos | `Procfile` |
| **Cloudflare** | Edge | Static + Workers | Unlimited BW | `wrangler.toml` |
| **Fly.io** | Edge Containers | Global apps, Docker | Free allowance | `fly.toml` |
| **Railway** | Modern PaaS | Quick deploys, databases | $5/month | `railway.json` |

---

## Quick Start

### 1. Choose Provider
Based on your needs:
- **AWS ecosystem** → AWS Amplify
- **Next.js** → Vercel (creators of Next.js)
- **Static/JAMstack** → Netlify or Cloudflare
- **Containers** → Fly.io
- **Traditional PaaS** → Heroku or Railway

### 2. Copy Config
```bash
# Example: Copy Vercel config to your project
cp shared/infra-providers/vercel/vercel.json prototypes/my-project/
```

### 3. Customize
Edit the config file for your project's needs (build commands, environment variables, etc.)

### 4. Deploy
Follow the provider-specific README for deployment instructions.

---

## Directory Structure

```
infra-providers/
├── README.md           # This file
├── aws/                # AWS Amplify, CodeBuild
├── vercel/             # Vercel platform
├── netlify/            # Netlify platform
├── heroku/             # Heroku PaaS
├── cloudflare/         # Cloudflare Pages/Workers
├── fly/                # Fly.io containers
└── railway/            # Railway PaaS
```

---

## Relationship to Other Directories

**`shared/aws/`** - Low-level AWS SDK wrappers (boto3, auth)
- Use for: AWS service clients, credential handling

**`shared/infra-providers/aws/`** - Deploy-time configurations
- Use for: Amplify builds, CodeBuild specs, CDK and Terraform templates

**`shared/golden-repos/typescript-cdk/`** - CDK golden repo template
- Use for: AWS-only infrastructure (rank 1 IaC preference)

**`shared/golden-repos/terraform-hcl/`** - Terraform golden repo template
- Use for: Multi-cloud or Terraform-preferred infrastructure (rank 2 IaC preference)

**`shared/scripts/`** - One-off automation scripts
- Use for: Custom deploy scripts, migrations

---

## Adding New Providers

1. Create directory: `shared/infra-providers/{provider}/`
2. Add README.md following existing format
3. Add config template(s)
4. Update this file's comparison table
5. Update `shared/README.md`

---

## Provider Selection Guide

### Decision Tree

```
Start
  │
  ├─ AWS ecosystem? ─────────────────► AWS Amplify
  │
  ├─ Next.js app? ───────────────────► Vercel
  │
  ├─ Static site? ───┬── Need CDN? ──► Cloudflare
  │                  └── Functions? ─► Netlify
  │
  ├─ Docker container? ──────────────► Fly.io
  │
  ├─ Traditional server? ────────────► Heroku or Railway
  │
  └─ Quick prototype? ───────────────► Railway
```

---

## References

- Tech preferences: `shared/tech-preferences/infrastructure.json`
- AWS utilities: `shared/aws/`
- Deploy scripts: `shared/scripts/amplify_deploy.py`

---

**Last Updated:** 2025-11-27
**Maintainer:** Protoflow
