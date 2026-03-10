"""
Unified VectorStore - Pinecone-like API with Algolia-style text search.

Usage:
    store = VectorStore(
        backend="s3-vectors",
        bucket="my-bucket",
        index="products",
        embeddings="bedrock"
    )

    store.upsert("id1", "Product description", {"price": 99})
    results = store.search("wireless headphones", k=10)
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from .backends import (
    BaseBackend,
    S3VectorsBackend,
    PgVectorBackend,
    OpenSearchBackend,
    VectorRecord,
    SearchResult,
)
from .embeddings import (
    BaseEmbeddings,
    BedrockEmbeddings,
    OpenAIEmbeddings,
    CohereEmbeddings,
)


BackendType = Literal["s3-vectors", "pgvector", "opensearch-serverless"]
EmbeddingsType = Literal["bedrock", "openai", "cohere"]


class VectorStore:
    """
    Unified vector store with Pinecone-like API and Algolia-style text search.

    Features:
        - Auto-embeds text on upsert and search
        - Multiple backend support (S3 Vectors, pgvector, OpenSearch)
        - Multiple embedding providers (Bedrock, OpenAI, Cohere)
        - Simple, intuitive API
    """

    def __init__(
        self,
        backend: BackendType = "s3-vectors",
        embeddings: Union[EmbeddingsType, BaseEmbeddings] = "bedrock",
        # S3 Vectors options
        bucket: Optional[str] = None,
        index: Optional[str] = None,
        # pgvector options
        connection_string: Optional[str] = None,
        collection: Optional[str] = None,
        # OpenSearch options
        endpoint: Optional[str] = None,
        # Common options
        region: str = "us-east-1",
        dimension: Optional[int] = None,
        distance_metric: str = "cosine",
        profile: Optional[str] = None,
        # Embeddings options
        embedding_model: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize the vector store.

        Args:
            backend: Backend type ("s3-vectors", "pgvector", "opensearch-serverless")
            embeddings: Embedding provider ("bedrock", "openai", "cohere") or instance

            S3 Vectors options:
                bucket: S3 vector bucket name
                index: Vector index name

            pgvector options:
                connection_string: PostgreSQL connection string
                collection: Table name

            OpenSearch options:
                endpoint: OpenSearch Serverless endpoint

            Common options:
                region: AWS region
                dimension: Vector dimension (auto-detected from embeddings)
                distance_metric: "cosine" or "euclidean"
                profile: AWS profile name

            Embeddings options:
                embedding_model: Model ID for embeddings
                api_key: API key for OpenAI/Cohere
        """
        # Initialize embeddings
        self.embeddings = self._init_embeddings(
            embeddings, embedding_model, region, profile, api_key
        )

        # Get dimension from embeddings if not specified
        dim = dimension or self.embeddings.dimension

        # Initialize backend
        self.backend = self._init_backend(
            backend=backend,
            bucket=bucket,
            index=index,
            connection_string=connection_string,
            collection=collection,
            endpoint=endpoint,
            region=region,
            dimension=dim,
            distance_metric=distance_metric,
            profile=profile,
        )

    def _init_embeddings(
        self,
        embeddings: Union[EmbeddingsType, BaseEmbeddings],
        model: Optional[str],
        region: str,
        profile: Optional[str],
        api_key: Optional[str],
    ) -> BaseEmbeddings:
        """Initialize the embedding provider."""
        if isinstance(embeddings, BaseEmbeddings):
            return embeddings

        if embeddings == "bedrock":
            return BedrockEmbeddings(
                model_id=model or "amazon.titan-embed-text-v2:0",
                region=region,
                profile=profile,
            )
        elif embeddings == "openai":
            return OpenAIEmbeddings(
                model=model or "text-embedding-3-small",
                api_key=api_key,
            )
        elif embeddings == "cohere":
            return CohereEmbeddings(
                model=model or "embed-english-v3.0",
                api_key=api_key,
            )
        else:
            raise ValueError(f"Unknown embeddings provider: {embeddings}")

    def _init_backend(
        self,
        backend: BackendType,
        **kwargs,
    ) -> BaseBackend:
        """Initialize the vector store backend."""
        if backend == "s3-vectors":
            if not kwargs.get("bucket") or not kwargs.get("index"):
                raise ValueError("S3 Vectors requires 'bucket' and 'index'")
            return S3VectorsBackend(
                bucket=kwargs["bucket"],
                index=kwargs["index"],
                region=kwargs.get("region", "us-east-1"),
                dimension=kwargs.get("dimension", 1024),
                distance_metric=kwargs.get("distance_metric", "cosine"),
                profile=kwargs.get("profile"),
            )

        elif backend == "pgvector":
            if not kwargs.get("connection_string"):
                raise ValueError("pgvector requires 'connection_string'")
            return PgVectorBackend(
                connection_string=kwargs["connection_string"],
                collection=kwargs.get("collection", "vectors"),
                dimension=kwargs.get("dimension", 1024),
                distance_metric=kwargs.get("distance_metric", "cosine"),
            )

        elif backend == "opensearch-serverless":
            if not kwargs.get("endpoint"):
                raise ValueError("OpenSearch requires 'endpoint'")
            return OpenSearchBackend(
                endpoint=kwargs["endpoint"],
                index=kwargs.get("index") or kwargs.get("collection", "vectors"),
                region=kwargs.get("region", "us-east-1"),
                dimension=kwargs.get("dimension", 1024),
                profile=kwargs.get("profile"),
            )

        else:
            raise ValueError(f"Unknown backend: {backend}")

    # =========================================================================
    # CORE API (Pinecone-style)
    # =========================================================================

    def upsert(
        self,
        id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Insert or update a single record.

        Auto-embeds the text using the configured embedding provider.

        Args:
            id: Unique identifier
            text: Text content to embed and store
            metadata: Optional metadata dictionary
        """
        embedding = self.embeddings.embed_text(text)
        record = VectorRecord(
            id=id,
            text=text,
            embedding=embedding,
            metadata=metadata or {},
        )
        self.backend.upsert(record)

    def upsert_many(
        self,
        items: List[Dict[str, Any]],
    ) -> None:
        """
        Insert or update multiple records.

        Args:
            items: List of dicts with "id", "text", and optional "metadata"
        """
        texts = [item["text"] for item in items]
        embeddings = self.embeddings.embed_texts(texts)

        records = []
        for item, embedding in zip(items, embeddings):
            records.append(VectorRecord(
                id=item["id"],
                text=item["text"],
                embedding=embedding,
                metadata=item.get("metadata", {}),
            ))

        self.backend.upsert_many(records)

    def search(
        self,
        query: str,
        k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar items (Algolia-style).

        Auto-embeds the query and searches the vector store.

        Args:
            query: Search query text
            k: Number of results to return
            filter: Optional metadata filter

        Returns:
            List of results with id, score, text, and metadata
        """
        embedding = self.embeddings.embed_query(query)
        results = self.backend.search(embedding, k=k, filter=filter)
        return [r.to_dict() for r in results]

    def search_by_vector(
        self,
        embedding: List[float],
        k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search using a pre-computed embedding.

        Args:
            embedding: Query vector
            k: Number of results
            filter: Optional metadata filter

        Returns:
            List of results
        """
        results = self.backend.search(embedding, k=k, filter=filter)
        return [r.to_dict() for r in results]

    def get(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get a record by ID.

        Args:
            id: Record identifier

        Returns:
            Record dict or None if not found
        """
        record = self.backend.get(id)
        return record.to_dict() if record else None

    def delete(self, id: str) -> bool:
        """
        Delete a record by ID.

        Args:
            id: Record identifier

        Returns:
            True if deleted, False if not found
        """
        return self.backend.delete(id)

    def delete_many(self, ids: List[str]) -> int:
        """
        Delete multiple records.

        Args:
            ids: List of record identifiers

        Returns:
            Number of records deleted
        """
        return self.backend.delete_many(ids)

    # =========================================================================
    # CONVENIENCE METHODS
    # =========================================================================

    def embed(self, text: str) -> List[float]:
        """
        Get embedding for text without storing.

        Useful for pre-computing embeddings or debugging.
        """
        return self.embeddings.embed_text(text)

    def embed_many(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts."""
        return self.embeddings.embed_texts(texts)

    @property
    def dimension(self) -> int:
        """Get the embedding dimension."""
        return self.embeddings.dimension

    def close(self) -> None:
        """Close any backend connections."""
        self.backend.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Convenience factory functions
def from_s3_vectors(
    bucket: str,
    index: str,
    embeddings: EmbeddingsType = "bedrock",
    **kwargs,
) -> VectorStore:
    """Create a VectorStore with S3 Vectors backend."""
    return VectorStore(
        backend="s3-vectors",
        bucket=bucket,
        index=index,
        embeddings=embeddings,
        **kwargs,
    )


def from_pgvector(
    connection_string: str,
    collection: str = "vectors",
    embeddings: EmbeddingsType = "bedrock",
    **kwargs,
) -> VectorStore:
    """Create a VectorStore with pgvector backend."""
    return VectorStore(
        backend="pgvector",
        connection_string=connection_string,
        collection=collection,
        embeddings=embeddings,
        **kwargs,
    )


def from_opensearch(
    endpoint: str,
    index: str = "vectors",
    embeddings: EmbeddingsType = "bedrock",
    **kwargs,
) -> VectorStore:
    """Create a VectorStore with OpenSearch Serverless backend."""
    return VectorStore(
        backend="opensearch-serverless",
        endpoint=endpoint,
        index=index,
        embeddings=embeddings,
        **kwargs,
    )
