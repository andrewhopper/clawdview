"""Base embeddings interface."""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddings(ABC):
    """Abstract base class for embedding providers."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the embedding dimension."""
        pass

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string."""
        pass

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple text strings."""
        pass

    def embed_query(self, query: str) -> List[float]:
        """Embed a search query. Override if query embedding differs."""
        return self.embed_text(query)
