"""Pydantic models for API request/response validation."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single chat message."""

    role: Literal["user", "assistant"] = Field(
        description="The role of the message sender"
    )
    content: str = Field(
        min_length=1,
        max_length=100000,
        description="The content of the message"
    )


class ChatRequest(BaseModel):
    """Chat completion request."""

    messages: list[ChatMessage] = Field(
        min_length=1,
        description="List of messages in the conversation"
    )
    model: str = Field(
        default="anthropic.claude-3-5-sonnet-20241022-v2:0",
        description="Bedrock model ID to use"
    )
    system: str | None = Field(
        default=None,
        max_length=10000,
        description="Optional system prompt"
    )
    max_tokens: int = Field(
        default=1024,
        ge=1,
        le=4096,
        description="Maximum tokens to generate"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Sampling temperature"
    )


class ChatResponse(BaseModel):
    """Chat completion response."""

    content: str = Field(description="Generated response content")
    model: str = Field(description="Model used for generation")
    usage: dict[str, int] = Field(description="Token usage statistics")
    stop_reason: str = Field(description="Reason for stopping generation")


class EmbeddingRequest(BaseModel):
    """Embedding generation request."""

    texts: list[str] = Field(
        min_length=1,
        max_length=100,
        description="List of texts to embed"
    )
    model: str = Field(
        default="amazon.titan-embed-text-v2:0",
        description="Bedrock embedding model ID"
    )


class EmbeddingResponse(BaseModel):
    """Embedding generation response."""

    embeddings: list[list[float]] = Field(description="Generated embeddings")
    model: str = Field(description="Model used for embeddings")
    dimensions: int = Field(description="Embedding dimensions")


class ItemBase(BaseModel):
    """Base model for items."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=10000)


class ItemCreate(ItemBase):
    """Model for creating items."""
    pass


class ItemUpdate(BaseModel):
    """Model for updating items."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=10000)


class Item(ItemBase):
    """Full item model with metadata."""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
