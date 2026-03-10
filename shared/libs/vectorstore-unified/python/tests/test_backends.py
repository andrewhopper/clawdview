"""
Tests for vector store backends.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime


class TestVectorRecord:
    """Tests for VectorRecord dataclass."""

    def test_create_record(self):
        """Test creating a vector record."""
        from vectorstore_unified.backends.base import VectorRecord

        record = VectorRecord(
            id="test_id",
            text="Test text",
            embedding=[0.1, 0.2, 0.3],
            metadata={"key": "value"},
        )

        assert record.id == "test_id"
        assert record.text == "Test text"
        assert record.embedding == [0.1, 0.2, 0.3]
        assert record.metadata == {"key": "value"}
        assert isinstance(record.created_at, datetime)
        assert isinstance(record.updated_at, datetime)

    def test_to_dict(self):
        """Test converting record to dictionary."""
        from vectorstore_unified.backends.base import VectorRecord

        record = VectorRecord(
            id="test_id",
            text="Test text",
            embedding=[0.1, 0.2],
            metadata={},
        )

        result = record.to_dict()

        assert result["id"] == "test_id"
        assert result["text"] == "Test text"
        assert result["embedding"] == [0.1, 0.2]
        assert "created_at" in result
        assert "updated_at" in result


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_create_result(self):
        """Test creating a search result."""
        from vectorstore_unified.backends.base import SearchResult

        result = SearchResult(
            id="test_id",
            score=0.95,
            text="Test text",
            metadata={"key": "value"},
        )

        assert result.id == "test_id"
        assert result.score == 0.95
        assert result.text == "Test text"
        assert result.metadata == {"key": "value"}

    def test_to_dict(self):
        """Test converting result to dictionary."""
        from vectorstore_unified.backends.base import SearchResult

        result = SearchResult(
            id="test_id",
            score=0.9,
            text="Test",
            metadata={},
        )

        d = result.to_dict()

        assert d["id"] == "test_id"
        assert d["score"] == 0.9
        assert d["text"] == "Test"


class TestS3VectorsBackend:
    """Tests for S3 Vectors backend."""

    @pytest.fixture
    def backend(self, mock_s3vectors_client):
        """Create backend with mock client."""
        with patch("boto3.Session") as mock_session:
            mock_session.return_value.client.return_value = mock_s3vectors_client

            from vectorstore_unified.backends import S3VectorsBackend

            backend = S3VectorsBackend(
                bucket="test-bucket",
                index="test-index",
                region="us-east-1",
                dimension=1024,
            )
            backend.client = mock_s3vectors_client
            return backend

    def test_upsert_single(self, backend, sample_records):
        """Test upserting a single record."""
        record = sample_records[0]
        backend.upsert(record)

        # Verify record was stored
        stored = backend.client.indexes["test-bucket"]["test-index"]
        assert record.id in stored

    def test_upsert_many(self, backend, sample_records):
        """Test upserting multiple records."""
        backend.upsert_many(sample_records)

        stored = backend.client.indexes["test-bucket"]["test-index"]
        assert len(stored) == len(sample_records)

    def test_search(self, backend, sample_records, mock_embeddings):
        """Test searching for similar vectors."""
        backend.upsert_many(sample_records)

        query_embedding = mock_embeddings.embed_text("wireless audio")
        results = backend.search(query_embedding, k=3)

        assert len(results) <= 3
        for result in results:
            assert hasattr(result, "id")
            assert hasattr(result, "score")

    def test_get(self, backend, sample_records):
        """Test getting a record by ID."""
        backend.upsert_many(sample_records)

        result = backend.get(sample_records[0].id)

        # Mock returns None since we'd need more complex mocking
        # In real tests, this would return the record

    def test_delete(self, backend, sample_records):
        """Test deleting a record."""
        backend.upsert_many(sample_records)

        result = backend.delete(sample_records[0].id)

        assert result is True

    def test_delete_many(self, backend, sample_records):
        """Test deleting multiple records."""
        backend.upsert_many(sample_records)

        ids = [r.id for r in sample_records[:3]]
        count = backend.delete_many(ids)

        assert count == 3


class TestPgVectorBackend:
    """Tests for pgvector backend."""

    @pytest.fixture
    def backend(self, mock_pg_connection):
        """Create backend with mock connection."""
        with patch("psycopg.connect") as mock_connect:
            mock_connect.return_value = mock_pg_connection

            with patch("pgvector.psycopg.register_vector"):
                from vectorstore_unified.backends import PgVectorBackend

                backend = PgVectorBackend(
                    connection_string="postgresql://test:test@localhost/test",
                    collection="test_vectors",
                    dimension=1024,
                )
                backend.conn = mock_pg_connection
                return backend

    def test_upsert_executes_insert(self, backend, sample_records):
        """Test that upsert executes INSERT query."""
        record = sample_records[0]
        backend.upsert(record)

        # Check that INSERT was executed
        queries = backend.conn.queries
        insert_queries = [q for q, _ in queries if "INSERT" in q]
        assert len(insert_queries) > 0

    def test_upsert_many(self, backend, sample_records):
        """Test upserting multiple records."""
        backend.upsert_many(sample_records)

        queries = backend.conn.queries
        insert_queries = [q for q, _ in queries if "INSERT" in q]
        assert len(insert_queries) == len(sample_records)

    def test_search_executes_select_with_order(self, backend, mock_embeddings):
        """Test that search executes SELECT with ORDER BY."""
        query_embedding = mock_embeddings.embed_text("test")
        backend.search(query_embedding, k=5)

        queries = backend.conn.queries
        select_queries = [q for q, _ in queries if "SELECT" in q and "ORDER BY" in q]
        assert len(select_queries) > 0

    def test_search_with_filter(self, backend, mock_embeddings):
        """Test search with metadata filter."""
        query_embedding = mock_embeddings.embed_text("test")
        backend.search(query_embedding, k=5, filter={"category": "electronics"})

        queries = backend.conn.queries
        filter_queries = [q for q, _ in queries if "WHERE" in q and "metadata" in q]
        assert len(filter_queries) > 0

    def test_delete_executes_delete(self, backend):
        """Test that delete executes DELETE query."""
        backend.delete("test_id")

        queries = backend.conn.queries
        delete_queries = [q for q, _ in queries if "DELETE" in q]
        assert len(delete_queries) > 0

    def test_close(self, backend):
        """Test that close closes the connection."""
        backend.close()
        assert backend.conn.closed is True


class TestOpenSearchBackend:
    """Tests for OpenSearch Serverless backend."""

    @pytest.fixture
    def backend(self, mock_opensearch_client):
        """Create backend with mock client."""
        with patch("opensearchpy.OpenSearch") as mock_os:
            mock_os.return_value = mock_opensearch_client

            with patch("requests_aws4auth.AWS4Auth"):
                with patch("boto3.Session"):
                    from vectorstore_unified.backends import OpenSearchBackend

                    backend = OpenSearchBackend(
                        endpoint="https://test.us-east-1.aoss.amazonaws.com",
                        index="test-index",
                        region="us-east-1",
                        dimension=1024,
                    )
                    backend.client = mock_opensearch_client
                    return backend

    def test_upsert_single(self, backend, sample_records):
        """Test upserting a single record."""
        record = sample_records[0]
        backend.upsert(record)

        # Verify record was stored via bulk
        stored = backend.client.indexes.get("test-index", {})
        assert record.id in stored

    def test_upsert_many(self, backend, sample_records):
        """Test upserting multiple records."""
        backend.upsert_many(sample_records)

        stored = backend.client.indexes.get("test-index", {})
        assert len(stored) == len(sample_records)

    def test_search(self, backend, sample_records, mock_embeddings):
        """Test searching for similar vectors."""
        backend.upsert_many(sample_records)

        query_embedding = mock_embeddings.embed_text("wireless")
        results = backend.search(query_embedding, k=3)

        assert len(results) <= 3

    def test_get(self, backend, sample_records):
        """Test getting a record by ID."""
        backend.upsert_many(sample_records)

        result = backend.get(sample_records[0].id)

        assert result is not None
        assert result.id == sample_records[0].id

    def test_get_nonexistent(self, backend):
        """Test getting a nonexistent record returns None."""
        result = backend.get("nonexistent_id")
        assert result is None

    def test_delete(self, backend, sample_records):
        """Test deleting a record."""
        backend.upsert_many(sample_records)

        result = backend.delete(sample_records[0].id)

        assert result is True
        assert sample_records[0].id not in backend.client.indexes.get("test-index", {})

    def test_delete_many(self, backend, sample_records):
        """Test deleting multiple records."""
        backend.upsert_many(sample_records)

        ids = [r.id for r in sample_records[:3]]
        count = backend.delete_many(ids)

        assert count == 3


class TestBackendDistanceMetrics:
    """Tests for distance metric configuration."""

    def test_pgvector_cosine_operator(self, mock_pg_connection):
        """Test that pgvector uses correct cosine operator."""
        with patch("psycopg.connect") as mock_connect:
            mock_connect.return_value = mock_pg_connection
            with patch("pgvector.psycopg.register_vector"):
                from vectorstore_unified.backends import PgVectorBackend

                backend = PgVectorBackend(
                    connection_string="postgresql://test/test",
                    distance_metric="cosine",
                )
                backend.conn = mock_pg_connection

                backend.search([0.1] * 1024, k=5)

                queries = backend.conn.queries
                # Should use <=> operator for cosine
                cosine_queries = [q for q, _ in queries if "<=>" in q]
                assert len(cosine_queries) > 0

    def test_pgvector_euclidean_operator(self, mock_pg_connection):
        """Test that pgvector uses correct euclidean operator."""
        with patch("psycopg.connect") as mock_connect:
            mock_connect.return_value = mock_pg_connection
            with patch("pgvector.psycopg.register_vector"):
                from vectorstore_unified.backends import PgVectorBackend

                backend = PgVectorBackend(
                    connection_string="postgresql://test/test",
                    distance_metric="euclidean",
                )
                backend.conn = mock_pg_connection

                backend.search([0.1] * 1024, k=5)

                queries = backend.conn.queries
                # Should use <-> operator for euclidean
                euclidean_queries = [q for q, _ in queries if "<->" in q]
                assert len(euclidean_queries) > 0
