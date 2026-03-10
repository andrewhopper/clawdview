"""OpenSearch Serverless backend."""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseBackend, VectorRecord, SearchResult


class OpenSearchBackend(BaseBackend):
    """
    OpenSearch Serverless backend.

    Supports vector search with optional hybrid (keyword + vector) search.

    Requires:
        - OpenSearch Serverless collection
        - pip install opensearch-py requests-aws4auth
    """

    def __init__(
        self,
        endpoint: str,
        index: str,
        region: str = "us-east-1",
        dimension: int = 1024,
        profile: Optional[str] = None,
    ):
        """
        Initialize OpenSearch Serverless backend.

        Args:
            endpoint: OpenSearch Serverless endpoint URL
            index: Index name
            region: AWS region
            dimension: Vector dimension
            profile: AWS profile name (optional)
        """
        try:
            from opensearchpy import OpenSearch, RequestsHttpConnection
            from requests_aws4auth import AWS4Auth
            import boto3
        except ImportError:
            raise ImportError(
                "Required packages: pip install opensearch-py requests-aws4auth boto3"
            )

        self.index = index
        self.dimension = dimension

        # Get AWS credentials
        session_kwargs = {"region_name": region}
        if profile:
            session_kwargs["profile_name"] = profile

        session = boto3.Session(**session_kwargs)
        credentials = session.get_credentials()

        auth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            region,
            "aoss",  # OpenSearch Serverless service name
            session_token=credentials.token,
        )

        # Remove https:// prefix if present for host
        host = endpoint.replace("https://", "").replace("http://", "")

        self.client = OpenSearch(
            hosts=[{"host": host, "port": 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )

        self._ensure_index()

    def _ensure_index(self) -> None:
        """Create index if it doesn't exist."""
        if not self.client.indices.exists(index=self.index):
            self.client.indices.create(
                index=self.index,
                body={
                    "settings": {
                        "index": {
                            "knn": True,
                            "knn.algo_param.ef_search": 100,
                        }
                    },
                    "mappings": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "text": {"type": "text"},
                            "embedding": {
                                "type": "knn_vector",
                                "dimension": self.dimension,
                                "method": {
                                    "name": "hnsw",
                                    "space_type": "cosinesimil",
                                    "engine": "nmslib",
                                    "parameters": {
                                        "ef_construction": 128,
                                        "m": 24,
                                    },
                                },
                            },
                            "metadata": {"type": "object", "enabled": True},
                            "created_at": {"type": "date"},
                            "updated_at": {"type": "date"},
                        }
                    },
                },
            )

    def upsert(self, record: VectorRecord) -> None:
        """Insert or update a single record."""
        self.upsert_many([record])

    def upsert_many(self, records: List[VectorRecord]) -> None:
        """Insert or update multiple records using bulk API."""
        actions = []
        for record in records:
            actions.append({"index": {"_index": self.index, "_id": record.id}})
            actions.append({
                "id": record.id,
                "text": record.text,
                "embedding": record.embedding,
                "metadata": record.metadata,
                "created_at": record.created_at.isoformat(),
                "updated_at": record.updated_at.isoformat(),
            })

        if actions:
            self.client.bulk(body=actions, refresh=True)

    def search(
        self,
        embedding: List[float],
        k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
        mode: str = "vector",  # "vector", "keyword", "hybrid"
        alpha: float = 0.7,  # For hybrid: weight of vector vs keyword
    ) -> List[SearchResult]:
        """
        Search by embedding vector.

        Args:
            embedding: Query vector
            k: Number of results
            filter: Metadata filter
            mode: Search mode ("vector", "keyword", "hybrid")
            alpha: For hybrid search, weight of vector (0-1)
        """
        # Build filter clause
        filter_clause = []
        if filter:
            for key, value in filter.items():
                filter_clause.append({"term": {f"metadata.{key}": value}})

        # Vector search query
        query = {
            "size": k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": embedding,
                        "k": k,
                    }
                }
            },
        }

        # Add filter if provided
        if filter_clause:
            query["query"] = {
                "bool": {
                    "must": [query["query"]],
                    "filter": filter_clause,
                }
            }

        response = self.client.search(index=self.index, body=query)

        results = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            results.append(SearchResult(
                id=hit["_id"],
                score=hit["_score"],
                text=source.get("text", ""),
                metadata=source.get("metadata", {}),
            ))

        return results

    def hybrid_search(
        self,
        query_text: str,
        embedding: List[float],
        k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
        alpha: float = 0.7,
    ) -> List[SearchResult]:
        """
        Hybrid search combining vector and keyword search.

        Args:
            query_text: Text query for keyword search
            embedding: Query vector for vector search
            k: Number of results
            filter: Metadata filter
            alpha: Weight of vector search (0-1)
        """
        # Build filter clause
        filter_clause = []
        if filter:
            for key, value in filter.items():
                filter_clause.append({"term": {f"metadata.{key}": value}})

        # Hybrid query using function_score
        query = {
            "size": k,
            "query": {
                "bool": {
                    "should": [
                        # Vector search component
                        {
                            "function_score": {
                                "query": {"knn": {"embedding": {"vector": embedding, "k": k * 2}}},
                                "weight": alpha,
                            }
                        },
                        # Keyword search component
                        {
                            "function_score": {
                                "query": {"match": {"text": query_text}},
                                "weight": 1 - alpha,
                            }
                        },
                    ],
                    "filter": filter_clause if filter_clause else None,
                }
            },
        }

        # Remove None filter
        if not filter_clause:
            del query["query"]["bool"]["filter"]

        response = self.client.search(index=self.index, body=query)

        results = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            results.append(SearchResult(
                id=hit["_id"],
                score=hit["_score"],
                text=source.get("text", ""),
                metadata=source.get("metadata", {}),
            ))

        return results

    def get(self, id: str) -> Optional[VectorRecord]:
        """Get a record by ID."""
        try:
            response = self.client.get(index=self.index, id=id)
            source = response["_source"]

            return VectorRecord(
                id=response["_id"],
                text=source.get("text", ""),
                embedding=source.get("embedding", []),
                metadata=source.get("metadata", {}),
                created_at=datetime.fromisoformat(source.get("created_at", datetime.utcnow().isoformat())),
                updated_at=datetime.fromisoformat(source.get("updated_at", datetime.utcnow().isoformat())),
            )
        except Exception:
            return None

    def delete(self, id: str) -> bool:
        """Delete a record by ID."""
        try:
            self.client.delete(index=self.index, id=id, refresh=True)
            return True
        except Exception:
            return False

    def delete_many(self, ids: List[str]) -> int:
        """Delete multiple records."""
        deleted = 0
        for id in ids:
            if self.delete(id):
                deleted += 1
        return deleted

    def close(self) -> None:
        """Close the OpenSearch client."""
        self.client.close()
