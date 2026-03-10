"""Base backend interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class VectorRecord:
    """A vector record with text, embedding, and metadata."""

    id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class SearchResult:
    """A search result with score."""

    id: str
    score: float
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "score": self.score,
            "text": self.text,
            "metadata": self.metadata,
        }


class BaseBackend(ABC):
    """Abstract base class for vector store backends."""

    @abstractmethod
    def upsert(self, record: VectorRecord) -> None:
        """Insert or update a single record."""
        pass

    @abstractmethod
    def upsert_many(self, records: List[VectorRecord]) -> None:
        """Insert or update multiple records."""
        pass

    @abstractmethod
    def search(
        self,
        embedding: List[float],
        k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """Search by embedding vector."""
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[VectorRecord]:
        """Get a record by ID."""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete a record by ID. Returns True if deleted."""
        pass

    @abstractmethod
    def delete_many(self, ids: List[str]) -> int:
        """Delete multiple records. Returns count deleted."""
        pass

    def close(self) -> None:
        """Close any connections. Override if needed."""
        pass
