"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from src.main import create_app
from src.config import Settings


@pytest.fixture
def settings() -> Settings:
    """Provide test settings."""
    return Settings(
        app_env="development",
        debug=True,
        log_level="DEBUG",
    )


@pytest.fixture
def client() -> TestClient:
    """Provide test client."""
    app = create_app()
    return TestClient(app)
