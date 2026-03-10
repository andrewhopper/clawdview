# Python CLI Template

Gold standard Python CLI application template.

## Features

- Click for argument parsing
- Rich for colored output and progress bars
- Pydantic for configuration validation
- Structlog for structured logging
- Pytest for testing

## Getting Started

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"

# Run CLI
mycli --help

# Run tests
pytest
```

## Commands

```bash
# Greet command
mycli greet <name> [--loud]

# Process command
mycli process <files...> [--dry-run]
```

## Project Structure

```
src/
├── __init__.py
├── cli.py           # CLI entry point
├── commands/        # Command implementations
│   ├── __init__.py
│   ├── greet.py
│   └── process.py
├── config.py        # Configuration
└── logging_config.py # Logging setup
tests/
└── test_cli.py
```
