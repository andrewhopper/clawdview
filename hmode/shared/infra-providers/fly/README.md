# Fly.io Deployment

Configuration and setup for Fly.io platform deployment.

---

## Overview

Fly.io runs containers globally at the edge. Best for:
- Docker-based applications
- Global low-latency deployment
- Long-running processes
- WebSocket applications

---

## Quick Start

### 1. Install CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### 2. Login

```bash
fly auth login
```

### 3. Launch App

```bash
# New app (creates fly.toml)
fly launch

# Or copy existing config
cp shared/infra-providers/fly/fly.toml ./
fly deploy
```

---

## Configuration

### fly.toml

| Section | Purpose |
|---------|---------|
| `app` | Application name |
| `primary_region` | Default deployment region |
| `[build]` | Build configuration |
| `[http_service]` | HTTP service settings |
| `[env]` | Environment variables |
| `[[services]]` | Service definitions |
| `[[vm]]` | Machine size |

---

## Dockerfile

Fly.io uses Dockerfiles. Minimal example:

```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

---

## Environment Variables

### fly.toml (non-secret)
```toml
[env]
  NODE_ENV = "production"
```

### Secrets (CLI)
```bash
fly secrets set MY_SECRET=value
fly secrets list
```

---

## Regions

```bash
# List available regions
fly platform regions

# Popular regions
# iad - Ashburn, Virginia
# sjc - San Jose, California
# lhr - London
# fra - Frankfurt
# nrt - Tokyo
# syd - Sydney
```

---

## Scaling

```bash
# Scale VM count
fly scale count 3

# Scale VM size
fly scale vm shared-cpu-1x
fly scale vm shared-cpu-2x

# Scale memory
fly scale memory 512
fly scale memory 1024
```

---

## Common Commands

```bash
# Deploy
fly deploy                    # Deploy app
fly deploy --local-only       # Build locally, deploy

# Apps
fly apps create NAME          # Create app
fly apps destroy NAME         # Delete app
fly apps list                 # List apps

# Status
fly status                    # App status
fly logs                      # Stream logs
fly logs -i INSTANCE          # Instance logs

# Machines
fly machine list              # List machines
fly machine stop ID           # Stop machine
fly machine start ID          # Start machine

# Secrets
fly secrets set KEY=value     # Set secret
fly secrets list              # List secrets
fly secrets unset KEY         # Remove secret

# Database (Postgres)
fly postgres create           # Create Postgres
fly postgres connect -a DB    # Connect to database

# SSH
fly ssh console               # SSH into machine
fly ssh issue                 # Issue SSH certificate
```

---

## Pricing

| VM Size | CPU | RAM | Price |
|---------|-----|-----|-------|
| shared-cpu-1x | Shared | 256 MB | ~$1.94/month |
| shared-cpu-2x | Shared | 512 MB | ~$3.88/month |
| shared-cpu-4x | Shared | 1 GB | ~$7.76/month |
| performance-1x | 1 | 2 GB | ~$29/month |

Free allowance: 3 shared-cpu-1x VMs

---

## References

- [Fly.io Documentation](https://fly.io/docs/)
- [fly.toml Reference](https://fly.io/docs/reference/configuration/)
- [Fly CLI Reference](https://fly.io/docs/flyctl/)
