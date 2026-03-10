# API Reference

## Overview

The API is available at `/api` prefix. All endpoints return JSON.

## Authentication

Most endpoints require Bearer token authentication:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/items
```

## Interactive Documentation

- **Swagger UI**: [/api/docs](http://localhost:8000/api/docs)
- **ReDoc**: [/api/redoc](http://localhost:8000/api/redoc)
- **OpenAPI JSON**: [/api/openapi.json](http://localhost:8000/api/openapi.json)

## Endpoints

### Health Check

::: src.routers.health

### Items

::: src.routers.items

## Models

::: src.models

## Authentication

::: src.auth

## Middleware

::: src.middleware
