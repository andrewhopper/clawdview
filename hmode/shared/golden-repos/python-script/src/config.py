"""Configuration management with multi-environment support."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


Environment = Literal["local", "dev", "integration", "stage", "prod"]


class Settings(BaseSettings):
    """Application settings with environment-aware configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    env: Environment = Field(default="local", description="Deployment environment")

    # Application
    app_name: str = Field(default="python-script", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    log_format: Literal["json", "console"] = Field(
        default="console", description="Log output format"
    )

    # Paths
    data_dir: Path = Field(default=Path("./data"), description="Data directory")
    output_dir: Path = Field(default=Path("./output"), description="Output directory")

    # Feature flags
    enable_metrics: bool = Field(default=False, description="Enable metrics collection")
    enable_tracing: bool = Field(default=False, description="Enable distributed tracing")

    @field_validator("debug", mode="before")
    @classmethod
    def set_debug_from_env(cls, v, info):
        """Auto-enable debug in local/dev environments."""
        if v is None:
            env = info.data.get("env", "local")
            return env in ("local", "dev")
        return v

    @field_validator("log_format", mode="before")
    @classmethod
    def set_log_format_from_env(cls, v, info):
        """Use JSON logging in non-local environments."""
        if v is None:
            env = info.data.get("env", "local")
            return "console" if env == "local" else "json"
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.env == "prod"

    @property
    def is_local(self) -> bool:
        """Check if running locally."""
        return self.env == "local"

    def ensure_dirs(self) -> None:
        """Create required directories if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
