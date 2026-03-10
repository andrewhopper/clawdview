"""AWS S3 Vectors backend."""

import json
from typing import Any, Dict, List, Optional

import boto3

from .base import BaseBackend, VectorRecord, SearchResult


class S3VectorsBackend(BaseBackend):
    """
    AWS S3 Vectors backend.

    Uses the native S3 Vectors API (GA July 2025) for serverless vector storage.

    Requires:
        - Vector bucket created via AWS Console or CLI
        - IAM permissions for s3vectors:* operations
    """

    def __init__(
        self,
        bucket: str,
        index: str,
        region: str = "us-east-1",
        dimension: int = 1024,
        distance_metric: str = "cosine",
        profile: Optional[str] = None,
    ):
        """
        Initialize S3 Vectors backend.

        Args:
            bucket: S3 vector bucket name
            index: Vector index name within the bucket
            region: AWS region
            dimension: Vector dimension (must match embeddings)
            distance_metric: "cosine" or "euclidean"
            profile: AWS profile name (optional)
        """
        self.bucket = bucket
        self.index = index
        self.region = region
        self.dimension = dimension
        self.distance_metric = distance_metric

        session_kwargs = {"region_name": region}
        if profile:
            session_kwargs["profile_name"] = profile

        session = boto3.Session(**session_kwargs)
        self.client = session.client("s3vectors")

        # Ensure index exists
        self._ensure_index()

    def _ensure_index(self) -> None:
        """Create index if it doesn't exist."""
        try:
            self.client.get_vector_index(
                vectorBucketName=self.bucket,
                indexName=self.index,
            )
        except self.client.exceptions.ResourceNotFoundException:
            self.client.create_vector_index(
                vectorBucketName=self.bucket,
                indexName=self.index,
                vectorDimension=self.dimension,
                distanceMetric=self.distance_metric,
            )

    def upsert(self, record: VectorRecord) -> None:
        """Insert or update a single record."""
        self.upsert_many([record])

    def upsert_many(self, records: List[VectorRecord]) -> None:
        """Insert or update multiple records."""
        vectors = []
        for record in records:
            vector_data = {
                "key": record.id,
                "data": {"float32": record.embedding},
                "metadata": {
                    "text": record.text,
                    **record.metadata,
                    "_created_at": record.created_at.isoformat(),
                    "_updated_at": record.updated_at.isoformat(),
                },
            }
            vectors.append(vector_data)

        # S3 Vectors API supports batch upsert
        self.client.put_vectors(
            vectorBucketName=self.bucket,
            indexName=self.index,
            vectors=vectors,
        )

    def search(
        self,
        embedding: List[float],
        k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """Search by embedding vector."""
        query_params = {
            "vectorBucketName": self.bucket,
            "indexName": self.index,
            "queryVector": {"float32": embedding},
            "topK": k,
            "returnMetadata": True,
        }

        # Add filter if provided
        if filter:
            query_params["filter"] = self._build_filter(filter)

        response = self.client.query_vectors(**query_params)

        results = []
        for match in response.get("vectors", []):
            metadata = match.get("metadata", {})
            text = metadata.pop("text", "")
            metadata.pop("_created_at", None)
            metadata.pop("_updated_at", None)

            results.append(SearchResult(
                id=match["key"],
                score=match.get("distance", 0.0),
                text=text,
                metadata=metadata,
            ))

        return results

    def _build_filter(self, filter: Dict[str, Any]) -> Dict[str, Any]:
        """Convert simple filter dict to S3 Vectors filter format."""
        # S3 Vectors uses a specific filter syntax
        # This is a simplified implementation
        conditions = []
        for key, value in filter.items():
            if isinstance(value, dict):
                # Handle operators like {"$eq": value}
                for op, v in value.items():
                    conditions.append({
                        "field": key,
                        "operator": op.replace("$", ""),
                        "value": v,
                    })
            else:
                # Simple equality
                conditions.append({
                    "field": key,
                    "operator": "eq",
                    "value": value,
                })

        if len(conditions) == 1:
            return conditions[0]
        return {"and": conditions}

    def get(self, id: str) -> Optional[VectorRecord]:
        """Get a record by ID."""
        try:
            response = self.client.get_vectors(
                vectorBucketName=self.bucket,
                indexName=self.index,
                keys=[id],
                returnMetadata=True,
            )

            vectors = response.get("vectors", [])
            if not vectors:
                return None

            vec = vectors[0]
            metadata = vec.get("metadata", {})
            text = metadata.pop("text", "")
            created_at = metadata.pop("_created_at", None)
            updated_at = metadata.pop("_updated_at", None)

            from datetime import datetime

            return VectorRecord(
                id=vec["key"],
                text=text,
                embedding=vec["data"]["float32"],
                metadata=metadata,
                created_at=datetime.fromisoformat(created_at) if created_at else datetime.utcnow(),
                updated_at=datetime.fromisoformat(updated_at) if updated_at else datetime.utcnow(),
            )

        except Exception:
            return None

    def delete(self, id: str) -> bool:
        """Delete a record by ID."""
        return self.delete_many([id]) > 0

    def delete_many(self, ids: List[str]) -> int:
        """Delete multiple records."""
        try:
            self.client.delete_vectors(
                vectorBucketName=self.bucket,
                indexName=self.index,
                keys=ids,
            )
            return len(ids)
        except Exception:
            return 0
