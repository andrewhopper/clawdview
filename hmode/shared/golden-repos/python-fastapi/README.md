# FastAPI Backend Template

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)](https://fastapi.tiangolo.com)

Gold standard FastAPI backend template with OpenAPI documentation.

## Quick Start

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uvicorn src.main:app --reload
```

Visit http://localhost:8000/api/docs for interactive API documentation.

## Features

- **FastAPI** - Modern async Python framework
- **Pydantic** - Data validation with type hints
- **OpenAPI** - Auto-generated API docs (Swagger + ReDoc)
- **Structlog** - Structured JSON logging
- **Pytest** - Async testing support
- **Docker** - Multi-stage production builds
- **MkDocs** - Documentation site generation

## Project Structure

```
src/
├── main.py            # Application entry point
├── config.py          # Settings management
├── auth.py            # JWT authentication
├── middleware.py      # Request logging
├── models.py          # Pydantic models
├── logging_config.py  # Structured logging
└── routers/           # API endpoints
    ├── health.py
    └── items.py
tests/
├── conftest.py        # Pytest fixtures
├── test_health.py
└── test_items.py
docs/
└── ...                # MkDocs documentation
```

## API Documentation

### Interactive Docs
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI JSON: http://localhost:8000/api/openapi.json

### Documentation Site
```bash
uv pip install -e ".[docs]"
mkdocs serve           # Serve locally
mkdocs build           # Build static site
```

## Development

```bash
uvicorn src.main:app --reload  # Development server
pytest                          # Run tests
pytest --cov                    # With coverage
ruff check src                  # Lint
mypy src                        # Type check
```

## Docker

```bash
# Development
docker build --target dev -t api:dev .
docker run -p 8000:8000 api:dev

# Production
docker build --target prod -t api:prod .
docker run -p 8000:8000 api:prod
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Environment | `development` |
| `DEBUG` | Debug mode | `false` |
| `HOST` | Bind host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Log level | `INFO` |
| `CORS_ORIGINS` | CORS origins | `["*"]` |

## Authentication

JWT auth utilities included. See `src/auth.py`:

```python
from fastapi import Depends
from src.auth import get_current_user, require_roles, User

# Require authentication
@router.get("/protected")
async def protected(user: User = Depends(get_current_user)):
    return {"user_id": user.id}

# Require specific roles
@router.get("/admin")
async def admin_only(user: User = Depends(require_roles("admin"))):
    return {"message": "Welcome admin"}
```

## License

MIT
