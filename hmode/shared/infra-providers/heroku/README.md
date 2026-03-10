# Heroku Deployment

Configuration and setup for Heroku platform deployment.

---

## Overview

Heroku is a classic PaaS with simple git-based deploys. Best for:
- Traditional server applications
- Apps needing managed Postgres
- Quick deployments
- Dyno-based scaling

---

## Quick Start

### 1. Install CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# npm
npm i -g heroku
```

### 2. Copy Configs

```bash
cp shared/infra-providers/heroku/Procfile ./
cp shared/infra-providers/heroku/app.json ./
```

### 3. Deploy

```bash
# Login
heroku login

# Create app
heroku create my-app-name

# Deploy
git push heroku main
```

---

## Configuration Files

### Procfile

Declares process types:
```
web: npm start
worker: npm run worker
release: npm run migrate
```

### app.json

App manifest for Heroku Button and Review Apps:
- Name and description
- Environment variables
- Add-ons
- Build configuration

---

## Environment Variables

### CLI
```bash
heroku config:set KEY=value
heroku config                  # List all
heroku config:unset KEY        # Remove
```

### Dashboard
Set in: Heroku Dashboard > App > Settings > Config Vars

---

## Buildpacks

Heroku auto-detects language. Override with:

```bash
# Set buildpack
heroku buildpacks:set heroku/nodejs

# Multiple buildpacks
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python
```

---

## Add-ons

```bash
# Postgres
heroku addons:create heroku-postgresql:essential-0

# Redis
heroku addons:create heroku-redis:mini

# List add-ons
heroku addons
```

---

## Common Commands

```bash
# Apps
heroku create NAME            # Create app
heroku apps:destroy NAME      # Delete app
heroku apps:info              # App info

# Deploy
git push heroku main          # Deploy
heroku releases               # List releases
heroku rollback               # Rollback to previous

# Dynos
heroku ps                     # List dynos
heroku ps:scale web=2         # Scale dynos
heroku ps:restart             # Restart all

# Logs
heroku logs --tail            # Stream logs
heroku logs -n 100            # Last 100 lines

# Database
heroku pg:info                # Database info
heroku pg:psql                # Connect to database

# Run commands
heroku run bash               # Interactive shell
heroku run npm run migrate    # Run one-off command
```

---

## Pricing (as of 2025)

| Dyno Type | Sleep? | Price |
|-----------|--------|-------|
| Eco | Yes (30 min) | $5/month pool |
| Basic | No | $7/month |
| Standard-1X | No | $25/month |
| Standard-2X | No | $50/month |

---

## References

- [Heroku Dev Center](https://devcenter.heroku.com/)
- [Procfile Reference](https://devcenter.heroku.com/articles/procfile)
- [app.json Schema](https://devcenter.heroku.com/articles/app-json-schema)
