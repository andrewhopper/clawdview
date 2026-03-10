"""Pydantic models for API requests and responses."""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(description="Health status")
    version: str = Field(description="Application version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    details: dict | None = Field(default=None, description="Additional details")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""

    items: list[T] = Field(description="List of items")
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    has_next: bool = Field(description="Whether there are more pages")


# Example domain model
class ItemCreate(BaseModel):
    """Request model for creating an item."""

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class ItemResponse(BaseModel):
    """Response model for an item."""

    id: str = Field(description="Item ID")
    name: str = Field(description="Item name")
    description: str | None = Field(description="Item description")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
