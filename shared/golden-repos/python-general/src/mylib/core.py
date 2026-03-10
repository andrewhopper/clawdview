"""Core library functionality."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from .logging import get_logger

T = TypeVar("T")


class BaseEntity(BaseModel):
    """Base model with common fields."""

    id: str = Field(description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()


@dataclass
class Result(Generic[T]):
    """Generic result wrapper for operations."""

    success: bool
    data: T | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, data: T, **metadata: Any) -> "Result[T]":
        """Create a successful result."""
        return cls(success=True, data=data, metadata=metadata)

    @classmethod
    def fail(cls, error: str, **metadata: Any) -> "Result[T]":
        """Create a failed result."""
        return cls(success=False, error=error, metadata=metadata)


class MyClass:
    """Example class demonstrating library patterns."""

    def __init__(self, name: str, config: dict[str, Any] | None = None) -> None:
        """Initialize MyClass.

        Args:
            name: Instance name for identification
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self._log = get_logger(f"mylib.{name}")
        self._log.info("Initialized", config_keys=list(self.config.keys()))

    def process(self, data: dict[str, Any]) -> Result[dict[str, Any]]:
        """Process input data and return result.

        Args:
            data: Input data to process

        Returns:
            Result wrapper with processed data or error
        """
        self._log.debug("Processing data", keys=list(data.keys()))

        try:
            # Example processing logic
            processed = {
                "input": data,
                "processor": self.name,
                "timestamp": datetime.utcnow().isoformat(),
            }
            self._log.info("Processing complete")
            return Result.ok(processed, processor=self.name)

        except Exception as e:
            self._log.exception("Processing failed", error=str(e))
            return Result.fail(str(e))

    def configure(self, **kwargs: Any) -> None:
        """Update configuration.

        Args:
            **kwargs: Configuration key-value pairs
        """
        self.config.update(kwargs)
        self._log.debug("Configuration updated", keys=list(kwargs.keys()))
