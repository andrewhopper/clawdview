# Railway Deployment

Configuration and setup for Railway platform deployment.

---

## Overview

Railway is a modern PaaS focused on developer experience. Best for:
- Quick deployments
- GitHub integration
- Managed databases
- Team collaboration

---

## Quick Start

### 1. Install CLI

```bash
npm i -g @railway/cli
```

### 2. Login

```bash
railway login
```

### 3. Deploy

```bash
# Initialize project
railway init

# Link to existing project
railway link

# Deploy
railway up
```

---

## Configuration

### railway.json (optional)

Configuration is optional - Railway auto-detects most settings. Use `railway.json` for explicit configuration.

---

## GitHub Integration

1. Connect GitHub in Railway Dashboard
2. Select repository
3. Railway auto-deploys on push

### Branch Deployments
- Each branch gets a unique URL
- Preview deployments auto-created for PRs

---

## Environment Variables

### CLI
```bash
railway variables set KEY=value
railway variables list
railway variables delete KEY
```

### Dashboard
Set in: Railway Dashboard > Project > Variables

### Local Development
```bash
# Run with Railway env vars
railway run npm start

# Create local .env
railway variables > .env
```

---

## Services

Railway supports multiple services:

| Service | Command |
|---------|---------|
| PostgreSQL | `railway add postgresql` |
| MySQL | `railway add mysql` |
| MongoDB | `railway add mongodb` |
| Redis | `railway add redis` |

---

## Common Commands

```bash
# Project
railway init              # Initialize new project
railway link              # Link to existing project
railway status            # Project status

# Deploy
railway up                # Deploy current directory
railway up --detach       # Deploy without logs

# Variables
railway variables set K=V # Set variable
railway variables list    # List variables
railway variables delete K # Delete variable

# Logs
railway logs              # Stream logs
railway logs --build      # Build logs

# Services
railway add postgres      # Add Postgres
railway add redis         # Add Redis
railway connect postgres  # Connect to Postgres

# Local Development
railway run CMD           # Run command with env vars
railway shell             # Interactive shell with env vars

# Domains
railway domain            # Generate domain
railway domain add DOMAIN # Add custom domain
```

---

## Nixpacks

Railway uses [Nixpacks](https://nixpacks.com/) for builds:
- Auto-detects language
- Creates optimized builds
- No Dockerfile required

Override with `nixpacks.toml` or use `Dockerfile` instead.

---

## Pricing

| Plan | Price | Included |
|------|-------|----------|
| Trial | Free | $5 credit |
| Hobby | $5/month | $5 usage |
| Pro | $20/user/month | Team features |

Usage-based pricing:
- $0.000463/vCPU/minute
- $0.000231/GB memory/minute

---

## References

- [Railway Documentation](https://docs.railway.app/)
- [CLI Reference](https://docs.railway.app/reference/cli-api)
- [Nixpacks](https://nixpacks.com/docs)
