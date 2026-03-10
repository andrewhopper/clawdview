# Python Script Template

Gold standard template for Python CLI scripts with structured logging, configuration management, and testing.

## Features

- **Configuration**: Pydantic Settings with environment variable support
- **Logging**: Structured logging with structlog (JSON/console output)
- **CLI**: Typer-based CLI with rich output
- **Testing**: pytest with fixtures and coverage
- **Linting**: ruff + mypy for code quality

## Quick Start

```bash
# Install dependencies
uv sync

# Run the script
uv run main run --help
uv run main run input.txt --verbose

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Type check
uv run mypy src

# Lint
uv run ruff check src tests
```

## Project Structure

```
python-script/
├── src/
│   ├── __init__.py
│   ├── config.py          # Settings with env var support
│   ├── logging_config.py  # Structured logging setup
│   └── main.py            # CLI entry point
├── tests/
│   ├── conftest.py        # Shared fixtures
│   ├── test_config.py
│   └── test_main.py
├── pyproject.toml
├── .env.example
└── README.md
```

## Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

All settings can be overridden via environment variables.
