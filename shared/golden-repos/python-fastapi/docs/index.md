# FastAPI Backend Template

Welcome to the FastAPI Backend Template documentation.

## Overview

This is a gold standard FastAPI backend template with:

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation with Python type hints
- **Structlog** - Structured logging
- **OpenAPI** - Auto-generated API documentation

## Quick Start

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"

# Run development server
uvicorn src.main:app --reload
```

Visit [http://localhost:8000/api/docs](http://localhost:8000/api/docs) for interactive API docs.

## Features

| Feature | Description |
|---------|-------------|
| Type Safety | Full type hints with Pydantic |
| Auth Ready | JWT auth utilities included |
| Logging | Structured logging with request IDs |
| Testing | Pytest with async support |
| Docker | Multi-stage Dockerfile |

## Project Structure

```
src/
├── main.py          # Application entry point
├── config.py        # Settings management
├── auth.py          # Authentication utilities
├── middleware.py    # Custom middleware
├── models.py        # Pydantic models
├── routers/         # API route handlers
│   ├── health.py
│   └── items.py
└── logging_config.py
tests/
├── conftest.py      # Test fixtures
├── test_health.py
└── test_items.py
```

## Next Steps

- [Installation Guide](getting-started/installation.md)
- [Configuration Options](getting-started/configuration.md)
- [API Reference](api/overview.md)
