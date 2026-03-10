"""Tests for configuration module."""

import os
from pathlib import Path

import pytest

from src.config import Settings, get_settings


class TestSettings:
    """Tests for Settings class."""

    def test_default_values(self) -> None:
        """Test default settings values."""
        settings = Settings()
        assert settings.app_name == "python-script"
        assert settings.app_env == "development"
        assert settings.debug is False
        assert settings.log_level == "INFO"

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test environment variable overrides."""
        monkeypatch.setenv("APP_ENV", "production")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")

        settings = Settings()
        assert settings.app_env == "production"
        assert settings.debug is True
        assert settings.log_level == "DEBUG"

    def test_ensure_dirs(self, temp_dir: Path) -> None:
        """Test directory creation."""
        settings = Settings(
            data_dir=temp_dir / "data",
            output_dir=temp_dir / "output",
        )
        settings.ensure_dirs()

        assert settings.data_dir.exists()
        assert settings.output_dir.exists()


class TestGetSettings:
    """Tests for get_settings function."""

    def test_returns_settings(self) -> None:
        """Test that get_settings returns a Settings instance."""
        settings = get_settings()
        assert isinstance(settings, Settings)

    def test_caching(self) -> None:
        """Test that settings are cached."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2
