"""Configuration management using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Environment
    app_env: str = "development"
    debug: bool = False

    # Logging
    log_level: str = "INFO"
    log_format: str = "console"  # console or json


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
