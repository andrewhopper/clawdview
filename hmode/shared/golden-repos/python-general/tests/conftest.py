"""Pytest configuration and fixtures."""

import pytest

from mylib import MyClass, configure_logging


@pytest.fixture(autouse=True)
def setup_logging() -> None:
    """Configure logging for tests."""
    configure_logging(level="DEBUG", format_type="console")


@pytest.fixture
def my_instance() -> MyClass:
    """Provide a configured MyClass instance."""
    return MyClass(name="test", config={"debug": True})
