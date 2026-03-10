"""AWS Bedrock embeddings provider."""

import json
from typing import List, Optional

import boto3

from .base import BaseEmbeddings


class BedrockEmbeddings(BaseEmbeddings):
    """
    AWS Bedrock embeddings using Titan or Cohere models.

    Models:
        - amazon.titan-embed-text-v2:0 (1024 dims, recommended)
        - amazon.titan-embed-text-v1 (1536 dims)
        - cohere.embed-english-v3 (1024 dims)
        - cohere.embed-multilingual-v3 (1024 dims)
    """

    MODEL_DIMENSIONS = {
        "amazon.titan-embed-text-v2:0": 1024,
        "amazon.titan-embed-text-v1": 1536,
        "cohere.embed-english-v3": 1024,
        "cohere.embed-multilingual-v3": 1024,
    }

    def __init__(
        self,
        model_id: str = "amazon.titan-embed-text-v2:0",
        region: str = "us-east-1",
        profile: Optional[str] = None,
    ):
        """
        Initialize Bedrock embeddings.

        Args:
            model_id: Bedrock model ID
            region: AWS region
            profile: AWS profile name (optional)
        """
        self.model_id = model_id
        self.region = region

        session_kwargs = {"region_name": region}
        if profile:
            session_kwargs["profile_name"] = profile

        session = boto3.Session(**session_kwargs)
        self.client = session.client("bedrock-runtime")

        self._dimension = self.MODEL_DIMENSIONS.get(model_id, 1024)

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string using Bedrock."""
        if self.model_id.startswith("amazon.titan"):
            return self._embed_titan(text)
        elif self.model_id.startswith("cohere"):
            return self._embed_cohere([text], input_type="search_document")[0]
        else:
            raise ValueError(f"Unsupported model: {self.model_id}")

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts."""
        if self.model_id.startswith("amazon.titan"):
            # Titan doesn't support batch, embed one by one
            return [self._embed_titan(text) for text in texts]
        elif self.model_id.startswith("cohere"):
            return self._embed_cohere(texts, input_type="search_document")
        else:
            raise ValueError(f"Unsupported model: {self.model_id}")

    def embed_query(self, query: str) -> List[float]:
        """Embed a search query."""
        if self.model_id.startswith("cohere"):
            # Cohere uses different input type for queries
            return self._embed_cohere([query], input_type="search_query")[0]
        return self.embed_text(query)

    def _embed_titan(self, text: str) -> List[float]:
        """Embed using Amazon Titan."""
        body = json.dumps({"inputText": text})

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        result = json.loads(response["body"].read())
        return result["embedding"]

    def _embed_cohere(
        self, texts: List[str], input_type: str = "search_document"
    ) -> List[List[float]]:
        """Embed using Cohere via Bedrock."""
        body = json.dumps({
            "texts": texts,
            "input_type": input_type,
            "truncate": "END",
        })

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        result = json.loads(response["body"].read())
        return result["embeddings"]
