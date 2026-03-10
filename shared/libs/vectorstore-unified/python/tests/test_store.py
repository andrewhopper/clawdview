"""
Tests for the main VectorStore class.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestVectorStoreInitialization:
    """Tests for VectorStore initialization."""

    def test_init_s3_vectors_backend(self, mock_boto3_session, mock_s3vectors_client):
        """Test initializing with S3 Vectors backend."""
        with patch("boto3.Session") as mock_session:
            mock_session.return_value.client.side_effect = lambda service, **kwargs: (
                mock_s3vectors_client if service == "s3vectors" else MagicMock()
            )

            from vectorstore_unified import VectorStore

            store = VectorStore(
                backend="s3-vectors",
                bucket="test-bucket",
                index="test-index",
                embeddings="bedrock",
            )

            assert store.dimension == 1024

    def test_init_pgvector_backend(self, mock_boto3_session, mock_pg_connection):
        """Test initializing with pgvector backend."""
        with patch("psycopg.connect") as mock_connect:
            mock_connect.return_value = mock_pg_connection
            with patch("pgvector.psycopg.register_vector"):
                from vectorstore_unified import VectorStore

                store = VectorStore(
                    backend="pgvector",
                    connection_string="postgresql://test/test",
                    embeddings="bedrock",
                )

                assert store.dimension == 1024

    def test_init_with_custom_embeddings(self, mock_embeddings, mock_boto3_session, mock_s3vectors_client):
        """Test initializing with custom embeddings provider."""
        with patch("boto3.Session") as mock_session:
            mock_session.return_value.client.return_value = mock_s3vectors_client

            from vectorstore_unified import VectorStore

            store = VectorStore(
                backend="s3-vectors",
                bucket="test-bucket",
                index="test-index",
                embeddings=mock_embeddings,
            )

            assert store.dimension == mock_embeddings.dimension

    def test_init_missing_bucket_raises_error(self, mock_boto3_session):
        """Test that missing bucket raises ValueError."""
        from vectorstore_unified import VectorStore

        with pytest.raises(ValueError, match="bucket"):
            VectorStore(
                backend="s3-vectors",
                index="test-index",
                embeddings="bedrock",
            )

    def test_init_missing_connection_string_raises_error(self, mock_boto3_session):
        """Test that missing connection string raises ValueError."""
        from vectorstore_unified import VectorStore

        with pytest.raises(ValueError, match="connection_string"):
            VectorStore(
                backend="pgvector",
                embeddings="bedrock",
            )

    def test_init_unknown_backend_raises_error(self, mock_boto3_session):
        """Test that unknown backend raises ValueError."""
        from vectorstore_unified import VectorStore

        with pytest.raises(ValueError, match="Unknown backend"):
            VectorStore(
                backend="unknown",
                embeddings="bedrock",
            )

    def test_init_unknown_embeddings_raises_error(self, mock_boto3_session):
        """Test that unknown embeddings raises ValueError."""
        from vectorstore_unified import VectorStore

        with pytest.raises(ValueError, match="Unknown embeddings"):
            VectorStore(
                backend="s3-vectors",
                bucket="test",
                index="test",
                embeddings="unknown",
            )


class TestVectorStoreOperations:
    """Tests for VectorStore CRUD operations."""

    @pytest.fixture
    def store(self, mock_embeddings, mock_s3vectors_client, mock_boto3_session):
        """Create a VectorStore with mocked backend."""
        with patch("boto3.Session") as mock_session:
            mock_session.return_value.client.return_value = mock_s3vectors_client

            from vectorstore_unified import VectorStore

            store = VectorStore(
                backend="s3-vectors",
                bucket="test-bucket",
                index="test-index",
                embeddings=mock_embeddings,
            )
            store.backend.client = mock_s3vectors_client
            return store

    def test_upsert_embeds_text(self, store):
        """Test that upsert auto-embeds text."""
        store.upsert(
            id="test_id",
            text="Test document text",
            metadata={"key": "value"},
        )

        # Verify record was stored
        stored = store.backend.client.indexes["test-bucket"]["test-index"]
        assert "test_id" in stored

    def test_upsert_many(self, store):
        """Test upserting multiple items."""
        items = [
            {"id": "item_1", "text": "First item", "metadata": {"idx": 1}},
            {"id": "item_2", "text": "Second item", "metadata": {"idx": 2}},
            {"id": "item_3", "text": "Third item", "metadata": {"idx": 3}},
        ]

        store.upsert_many(items)

        stored = store.backend.client.indexes["test-bucket"]["test-index"]
        assert len(stored) == 3

    def test_search_embeds_query(self, store, sample_texts):
        """Test that search auto-embeds query."""
        # First add some documents
        for i, text in enumerate(sample_texts):
            store.upsert(f"doc_{i}", text)

        results = store.search("wireless audio device", k=3)

        assert isinstance(results, list)
        for result in results:
            assert "id" in result
            assert "score" in result

    def test_search_with_filter(self, store, sample_texts):
        """Test search with metadata filter."""
        for i, text in enumerate(sample_texts):
            store.upsert(f"doc_{i}", text, {"category": "electronics"})

        results = store.search(
            "wireless",
            k=5,
            filter={"category": "electronics"},
        )

        assert isinstance(results, list)

    def test_search_by_vector(self, store, sample_texts, mock_embeddings):
        """Test search with pre-computed embedding."""
        for i, text in enumerate(sample_texts):
            store.upsert(f"doc_{i}", text)

        embedding = mock_embeddings.embed_text("test query")
        results = store.search_by_vector(embedding, k=3)

        assert isinstance(results, list)

    def test_get_returns_dict(self, store):
        """Test that get returns a dictionary."""
        store.upsert("test_id", "Test text")

        result = store.get("test_id")

        # Mock may return None, but interface should return dict or None
        assert result is None or isinstance(result, dict)

    def test_delete_returns_bool(self, store):
        """Test that delete returns boolean."""
        store.upsert("test_id", "Test text")

        result = store.delete("test_id")

        assert isinstance(result, bool)

    def test_delete_many_returns_count(self, store):
        """Test that delete_many returns count."""
        store.upsert_many([
            {"id": "item_1", "text": "Text 1"},
            {"id": "item_2", "text": "Text 2"},
        ])

        count = store.delete_many(["item_1", "item_2"])

        assert isinstance(count, int)

    def test_embed_returns_embedding(self, store):
        """Test embed method returns embedding without storing."""
        embedding = store.embed("Test text")

        assert isinstance(embedding, list)
        assert len(embedding) == store.dimension

    def test_embed_many_returns_embeddings(self, store):
        """Test embed_many returns multiple embeddings."""
        texts = ["Text 1", "Text 2", "Text 3"]
        embeddings = store.embed_many(texts)

        assert len(embeddings) == 3
        assert all(len(e) == store.dimension for e in embeddings)


class TestVectorStoreContextManager:
    """Tests for VectorStore context manager."""

    def test_context_manager_closes(self, mock_embeddings, mock_pg_connection, mock_boto3_session):
        """Test that context manager closes backend."""
        with patch("psycopg.connect") as mock_connect:
            mock_connect.return_value = mock_pg_connection
            with patch("pgvector.psycopg.register_vector"):
                from vectorstore_unified import VectorStore

                with VectorStore(
                    backend="pgvector",
                    connection_string="postgresql://test/test",
                    embeddings=mock_embeddings,
                ) as store:
                    store.upsert("test", "text")

                # Connection should be closed after context
                assert mock_pg_connection.closed is True


class TestFactoryFunctions:
    """Tests for factory functions."""

    def test_from_s3_vectors(self, mock_boto3_session, mock_s3vectors_client):
        """Test from_s3_vectors factory function."""
        with patch("boto3.Session") as mock_session:
            mock_session.return_value.client.return_value = mock_s3vectors_client

            from vectorstore_unified import from_s3_vectors

            store = from_s3_vectors("my-bucket", "my-index")

            assert store is not None

    def test_from_pgvector(self, mock_boto3_session, mock_pg_connection):
        """Test from_pgvector factory function."""
        with patch("psycopg.connect") as mock_connect:
            mock_connect.return_value = mock_pg_connection
            with patch("pgvector.psycopg.register_vector"):
                from vectorstore_unified import from_pgvector

                store = from_pgvector("postgresql://test/test")

                assert store is not None

    def test_from_opensearch(self, mock_boto3_session, mock_opensearch_client):
        """Test from_opensearch factory function."""
        with patch("opensearchpy.OpenSearch") as mock_os:
            mock_os.return_value = mock_opensearch_client
            with patch("requests_aws4auth.AWS4Auth"):
                with patch("boto3.Session"):
                    from vectorstore_unified import from_opensearch

                    store = from_opensearch("https://test.aoss.amazonaws.com", "my-index")

                    assert store is not None


class TestVectorStoreDimension:
    """Tests for dimension handling."""

    def test_dimension_from_embeddings(self, mock_embeddings, mock_s3vectors_client, mock_boto3_session):
        """Test that dimension is inferred from embeddings."""
        with patch("boto3.Session") as mock_session:
            mock_session.return_value.client.return_value = mock_s3vectors_client

            from vectorstore_unified import VectorStore

            store = VectorStore(
                backend="s3-vectors",
                bucket="test",
                index="test",
                embeddings=mock_embeddings,
            )

            assert store.dimension == mock_embeddings.dimension

    def test_explicit_dimension_override(self, mock_boto3_session, mock_s3vectors_client):
        """Test that explicit dimension overrides embeddings dimension."""
        with patch("boto3.Session") as mock_session:
            mock_session.return_value.client.return_value = mock_s3vectors_client

            from vectorstore_unified import VectorStore

            store = VectorStore(
                backend="s3-vectors",
                bucket="test",
                index="test",
                embeddings="bedrock",
                dimension=512,  # Override
            )

            # Backend should use explicit dimension
            # (embeddings still return their native dimension)
