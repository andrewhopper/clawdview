"""PostgreSQL pgvector backend."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseBackend, VectorRecord, SearchResult


class PgVectorBackend(BaseBackend):
    """
    PostgreSQL pgvector backend.

    Uses psycopg3 with pgvector extension for vector similarity search.

    Requires:
        - PostgreSQL with pgvector extension
        - pip install psycopg[binary] pgvector
    """

    def __init__(
        self,
        connection_string: str,
        collection: str = "vectors",
        dimension: int = 1024,
        distance_metric: str = "cosine",
    ):
        """
        Initialize pgvector backend.

        Args:
            connection_string: PostgreSQL connection string
            collection: Table name for vectors
            dimension: Vector dimension
            distance_metric: "cosine", "euclidean", or "inner_product"
        """
        try:
            import psycopg
            from pgvector.psycopg import register_vector
        except ImportError:
            raise ImportError(
                "psycopg and pgvector required: pip install 'psycopg[binary]' pgvector"
            )

        self.collection = collection
        self.dimension = dimension
        self.distance_metric = distance_metric

        # Distance operator mapping
        self.distance_ops = {
            "cosine": "<=>",
            "euclidean": "<->",
            "inner_product": "<#>",
        }

        self.conn = psycopg.connect(connection_string)
        register_vector(self.conn)

        self._ensure_table()

    def _ensure_table(self) -> None:
        """Create table if it doesn't exist."""
        with self.conn.cursor() as cur:
            # Enable pgvector extension
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

            # Create table
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.collection} (
                    id TEXT PRIMARY KEY,
                    text TEXT,
                    embedding vector({self.dimension}),
                    metadata JSONB DEFAULT '{{}}',
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)

            # Create index for vector search
            index_name = f"{self.collection}_embedding_idx"
            if self.distance_metric == "cosine":
                cur.execute(f"""
                    CREATE INDEX IF NOT EXISTS {index_name}
                    ON {self.collection}
                    USING hnsw (embedding vector_cosine_ops)
                """)
            elif self.distance_metric == "euclidean":
                cur.execute(f"""
                    CREATE INDEX IF NOT EXISTS {index_name}
                    ON {self.collection}
                    USING hnsw (embedding vector_l2_ops)
                """)
            else:  # inner_product
                cur.execute(f"""
                    CREATE INDEX IF NOT EXISTS {index_name}
                    ON {self.collection}
                    USING hnsw (embedding vector_ip_ops)
                """)

            self.conn.commit()

    def upsert(self, record: VectorRecord) -> None:
        """Insert or update a single record."""
        self.upsert_many([record])

    def upsert_many(self, records: List[VectorRecord]) -> None:
        """Insert or update multiple records."""
        import json

        with self.conn.cursor() as cur:
            for record in records:
                cur.execute(f"""
                    INSERT INTO {self.collection} (id, text, embedding, metadata, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        text = EXCLUDED.text,
                        embedding = EXCLUDED.embedding,
                        metadata = EXCLUDED.metadata,
                        updated_at = EXCLUDED.updated_at
                """, (
                    record.id,
                    record.text,
                    record.embedding,
                    json.dumps(record.metadata),
                    record.created_at,
                    record.updated_at,
                ))

            self.conn.commit()

    def search(
        self,
        embedding: List[float],
        k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """Search by embedding vector."""
        op = self.distance_ops.get(self.distance_metric, "<=>")

        # Build filter clause
        filter_clause = ""
        filter_params = []
        if filter:
            conditions = []
            for key, value in filter.items():
                conditions.append(f"metadata->>'{key}' = %s")
                filter_params.append(str(value))
            filter_clause = "WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT id, text, metadata, embedding {op} %s AS distance
            FROM {self.collection}
            {filter_clause}
            ORDER BY distance
            LIMIT %s
        """

        with self.conn.cursor() as cur:
            cur.execute(query, [embedding] + filter_params + [k])
            rows = cur.fetchall()

        results = []
        for row in rows:
            import json
            metadata = row[2] if isinstance(row[2], dict) else json.loads(row[2])
            # Convert distance to similarity score (0-1 for cosine)
            distance = float(row[3])
            score = 1 - distance if self.distance_metric == "cosine" else distance

            results.append(SearchResult(
                id=row[0],
                score=score,
                text=row[1],
                metadata=metadata,
            ))

        return results

    def get(self, id: str) -> Optional[VectorRecord]:
        """Get a record by ID."""
        import json

        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT id, text, embedding, metadata, created_at, updated_at
                FROM {self.collection}
                WHERE id = %s
            """, (id,))

            row = cur.fetchone()
            if not row:
                return None

            metadata = row[3] if isinstance(row[3], dict) else json.loads(row[3])

            return VectorRecord(
                id=row[0],
                text=row[1],
                embedding=list(row[2]),
                metadata=metadata,
                created_at=row[4],
                updated_at=row[5],
            )

    def delete(self, id: str) -> bool:
        """Delete a record by ID."""
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.collection} WHERE id = %s", (id,))
            self.conn.commit()
            return cur.rowcount > 0

    def delete_many(self, ids: List[str]) -> int:
        """Delete multiple records."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"DELETE FROM {self.collection} WHERE id = ANY(%s)",
                (ids,)
            )
            self.conn.commit()
            return cur.rowcount

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()
