"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import tempfile

from src.config import Settings


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def test_settings(temp_dir: Path) -> Settings:
    """Provide test settings with temp directories."""
    return Settings(
        app_env="development",
        debug=True,
        log_level="DEBUG",
        data_dir=temp_dir / "data",
        output_dir=temp_dir / "output",
    )
