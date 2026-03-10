"""Configuration management for library usage."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


Environment = Literal["local", "dev", "integration", "stage", "prod"]


class LibraryConfig(BaseSettings):
    """Library configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="MYLIB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    env: Environment = Field(default="local", description="Deployment environment")

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    log_format: Literal["json", "console"] = Field(
        default="console", description="Log output format"
    )

    # Feature flags
    enable_debug_logging: bool = Field(default=False, description="Enable verbose debug logging")
    enable_metrics: bool = Field(default=False, description="Enable metrics collection")

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.env == "prod"

    @property
    def is_local(self) -> bool:
        """Check if running locally."""
        return self.env == "local"


_config: LibraryConfig | None = None


def get_config() -> LibraryConfig:
    """Get library configuration."""
    global _config
    if _config is None:
        _config = LibraryConfig()
    return _config


def configure(
    env: Environment | None = None,
    log_level: str | None = None,
    log_format: str | None = None,
    **kwargs,
) -> LibraryConfig:
    """Configure the library programmatically.

    Args:
        env: Deployment environment
        log_level: Logging level
        log_format: Log output format
        **kwargs: Additional configuration options

    Returns:
        Updated configuration
    """
    global _config

    config_dict = {}
    if env is not None:
        config_dict["env"] = env
    if log_level is not None:
        config_dict["log_level"] = log_level
    if log_format is not None:
        config_dict["log_format"] = log_format
    config_dict.update(kwargs)

    _config = LibraryConfig(**config_dict)
    return _config
