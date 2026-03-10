"""
Unified VectorStore Library
============================

Pinecone-like API with Algolia-style text search.

Usage:
    from vectorstore_unified import VectorStore

    store = VectorStore(
        backend="s3-vectors",
        bucket="my-bucket",
        index="products",
        embeddings="bedrock"
    )

    store.upsert("id1", "Product description", {"price": 99})
    results = store.search("wireless headphones", k=10)
"""

from .store import VectorStore
from .backends import S3VectorsBackend, PgVectorBackend, OpenSearchBackend
from .embeddings import BedrockEmbeddings, OpenAIEmbeddings, CohereEmbeddings

__version__ = "0.1.0"
__all__ = [
    "VectorStore",
    "S3VectorsBackend",
    "PgVectorBackend",
    "OpenSearchBackend",
    "BedrockEmbeddings",
    "OpenAIEmbeddings",
    "CohereEmbeddings",
]
