"""Pytest configuration and fixtures."""

import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()
