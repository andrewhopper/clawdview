# Python Library Template

Gold standard template for Python libraries with structured logging, typing, and testing.

## Features

- **Type Safety**: Full type hints with mypy strict mode
- **Pydantic Models**: Data validation and serialization
- **Structured Logging**: structlog integration
- **Testing**: pytest with fixtures and coverage
- **Linting**: ruff + mypy

## Installation

```bash
# Development install
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

## Usage

```python
from mylib import MyClass, configure_logging

# Configure logging (optional)
configure_logging(level="INFO", format_type="console")

# Create instance
processor = MyClass(name="example", config={"debug": True})

# Process data
result = processor.process({"key": "value"})
if result.success:
    print(result.data)
else:
    print(f"Error: {result.error}")
```

## Development

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/mylib --cov-report=term-missing

# Type check
uv run mypy src

# Lint
uv run ruff check src tests
```

## Project Structure

```
python-general/
├── src/mylib/
│   ├── __init__.py      # Public API
│   ├── core.py          # Core classes
│   ├── utils.py         # Utility functions
│   ├── logging.py       # Logging config
│   └── exceptions.py    # Custom exceptions
├── tests/
│   ├── conftest.py
│   ├── test_core.py
│   └── test_utils.py
├── pyproject.toml
└── README.md
```
