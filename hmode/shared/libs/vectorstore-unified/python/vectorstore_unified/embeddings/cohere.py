"""Cohere embeddings provider (direct API)."""

import os
from typing import List, Optional

from .base import BaseEmbeddings


class CohereEmbeddings(BaseEmbeddings):
    """
    Cohere embeddings via direct API.

    Models:
        - embed-english-v3.0 (1024 dims)
        - embed-multilingual-v3.0 (1024 dims)
        - embed-english-light-v3.0 (384 dims, faster)
    """

    MODEL_DIMENSIONS = {
        "embed-english-v3.0": 1024,
        "embed-multilingual-v3.0": 1024,
        "embed-english-light-v3.0": 384,
    }

    def __init__(
        self,
        model: str = "embed-english-v3.0",
        api_key: Optional[str] = None,
    ):
        """
        Initialize Cohere embeddings.

        Args:
            model: Cohere model name
            api_key: Cohere API key (defaults to COHERE_API_KEY env var)
        """
        try:
            import cohere
        except ImportError:
            raise ImportError("cohere package required: pip install cohere")

        self.model = model
        self._dimension = self.MODEL_DIMENSIONS.get(model, 1024)

        api_key = api_key or os.environ.get("COHERE_API_KEY")
        if not api_key:
            raise ValueError("Cohere API key required")

        self.client = cohere.Client(api_key)

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string."""
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type="search_document",
        )
        return response.embeddings[0]

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts."""
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type="search_document",
        )
        return response.embeddings

    def embed_query(self, query: str) -> List[float]:
        """Embed a search query."""
        response = self.client.embed(
            texts=[query],
            model=self.model,
            input_type="search_query",
        )
        return response.embeddings[0]
