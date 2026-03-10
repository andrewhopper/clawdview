"""Configuration management for FastAPI application."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, SecretStr
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
    app_name: str = Field(default="fastapi-backend", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=1, description="Number of workers")

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    log_format: Literal["json", "console"] = Field(
        default="console", description="Log output format"
    )

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"], description="Allowed CORS origins"
    )

    # API
    api_prefix: str = Field(default="/api/v1", description="API prefix")

    # Database (optional)
    database_url: SecretStr | None = Field(default=None, description="Database connection URL")

    # Redis/Cache (optional)
    redis_url: str | None = Field(default=None, description="Redis connection URL")

    # Feature flags
    enable_metrics: bool = Field(default=False, description="Enable metrics endpoint")
    enable_tracing: bool = Field(default=False, description="Enable distributed tracing")
    enable_docs: bool = Field(default=True, description="Enable API documentation")

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

    @field_validator("enable_docs", mode="before")
    @classmethod
    def set_docs_from_env(cls, v, info):
        """Disable docs in production by default."""
        if v is None:
            env = info.data.get("env", "local")
            return env != "prod"
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.env == "prod"

    @property
    def is_local(self) -> bool:
        """Check if running locally."""
        return self.env == "local"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
