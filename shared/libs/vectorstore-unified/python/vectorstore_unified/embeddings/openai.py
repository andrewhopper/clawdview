"""OpenAI embeddings provider."""

import os
from typing import List, Optional

from .base import BaseEmbeddings


class OpenAIEmbeddings(BaseEmbeddings):
    """
    OpenAI embeddings.

    Models:
        - text-embedding-3-small (1536 dims, cheap)
        - text-embedding-3-large (3072 dims, better quality)
        - text-embedding-ada-002 (1536 dims, legacy)
    """

    MODEL_DIMENSIONS = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536,
    }

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
    ):
        """
        Initialize OpenAI embeddings.

        Args:
            model: OpenAI model name
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package required: pip install openai")

        self.model = model
        self._dimension = self.MODEL_DIMENSIONS.get(model, 1536)

        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key required")

        self.client = OpenAI(api_key=api_key)

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string."""
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return response.data[0].embedding

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts (batched)."""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]
