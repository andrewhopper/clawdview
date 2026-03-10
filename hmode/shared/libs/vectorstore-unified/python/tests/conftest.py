"""
Pytest fixtures and mocks for vectorstore-unified tests.
"""

import pytest
from unittest.mock import MagicMock, patch
from typing import List
import json


# =============================================================================
# MOCK EMBEDDINGS
# =============================================================================

class MockEmbeddings:
    """Mock embedding provider for testing."""

    def __init__(self, dimension: int = 1024):
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_text(self, text: str) -> List[float]:
        """Generate deterministic embedding based on text hash."""
        import hashlib
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        # Generate pseudo-random but deterministic values
        return [(hash_val >> i) % 1000 / 1000.0 for i in range(self._dimension)]

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(text) for text in texts]

    def embed_query(self, query: str) -> List[float]:
        return self.embed_text(query)


@pytest.fixture
def mock_embeddings():
    """Fixture providing mock embeddings."""
    return MockEmbeddings(dimension=1024)


@pytest.fixture
def mock_embeddings_small():
    """Fixture providing small dimension mock embeddings."""
    return MockEmbeddings(dimension=128)


# =============================================================================
# MOCK BEDROCK CLIENT
# =============================================================================

@pytest.fixture
def mock_bedrock_client():
    """Mock AWS Bedrock client."""
    mock_client = MagicMock()

    def invoke_model(modelId, body, **kwargs):
        request = json.loads(body)

        if modelId.startswith("amazon.titan"):
            # Titan response
            embedding = [0.1] * 1024
            return {
                "body": MagicMock(
                    read=lambda: json.dumps({"embedding": embedding}).encode()
                )
            }
        elif modelId.startswith("cohere"):
            # Cohere response
            texts = request.get("texts", [])
            embeddings = [[0.2] * 1024 for _ in texts]
            return {
                "body": MagicMock(
                    read=lambda: json.dumps({"embeddings": embeddings}).encode()
                )
            }

        raise ValueError(f"Unknown model: {modelId}")

    mock_client.invoke_model = MagicMock(side_effect=invoke_model)
    return mock_client


@pytest.fixture
def mock_boto3_session(mock_bedrock_client):
    """Mock boto3 session that returns mock Bedrock client."""
    with patch("boto3.Session") as mock_session_class:
        mock_session = MagicMock()
        mock_session.client.return_value = mock_bedrock_client
        mock_session_class.return_value = mock_session
        yield mock_session


# =============================================================================
# MOCK S3 VECTORS CLIENT
# =============================================================================

class MockS3VectorsClient:
    """In-memory mock of S3 Vectors client."""

    def __init__(self):
        self.indexes = {}  # bucket -> index -> vectors
        self.exceptions = MagicMock()
        self.exceptions.ResourceNotFoundException = Exception

    def create_vector_index(self, vectorBucketName, indexName, **kwargs):
        if vectorBucketName not in self.indexes:
            self.indexes[vectorBucketName] = {}
        self.indexes[vectorBucketName][indexName] = {}

    def get_vector_index(self, vectorBucketName, indexName):
        if vectorBucketName not in self.indexes:
            raise Exception("ResourceNotFoundException")
        if indexName not in self.indexes[vectorBucketName]:
            raise Exception("ResourceNotFoundException")
        return {"indexName": indexName}

    def put_vectors(self, vectorBucketName, indexName, vectors):
        if vectorBucketName not in self.indexes:
            self.indexes[vectorBucketName] = {}
        if indexName not in self.indexes[vectorBucketName]:
            self.indexes[vectorBucketName][indexName] = {}

        for vec in vectors:
            self.indexes[vectorBucketName][indexName][vec["key"]] = vec

    def get_vectors(self, vectorBucketName, indexName, keys, **kwargs):
        bucket = self.indexes.get(vectorBucketName, {})
        index = bucket.get(indexName, {})
        vectors = [index[k] for k in keys if k in index]
        return {"vectors": vectors}

    def delete_vectors(self, vectorBucketName, indexName, keys):
        bucket = self.indexes.get(vectorBucketName, {})
        index = bucket.get(indexName, {})
        for key in keys:
            index.pop(key, None)

    def query_vectors(self, vectorBucketName, indexName, queryVector, topK, **kwargs):
        bucket = self.indexes.get(vectorBucketName, {})
        index = bucket.get(indexName, {})

        # Simple mock: return all vectors with fake distances
        results = []
        for key, vec in list(index.items())[:topK]:
            results.append({
                "key": key,
                "distance": 0.1,
                "metadata": vec.get("metadata", {}),
            })

        return {"vectors": results}


@pytest.fixture
def mock_s3vectors_client():
    """Fixture providing mock S3 Vectors client."""
    return MockS3VectorsClient()


# =============================================================================
# MOCK POSTGRESQL CONNECTION (pgvector)
# =============================================================================

class MockPgCursor:
    """Mock PostgreSQL cursor."""

    def __init__(self, connection):
        self.connection = connection
        self.rowcount = 0
        self._results = []

    def execute(self, query, params=None):
        # Track queries for assertions
        self.connection.queries.append((query, params))

        # Simulate some basic operations
        if "DELETE" in query:
            self.rowcount = 1
        elif "SELECT" in query:
            # Return mock results
            self._results = self.connection.mock_results

    def fetchall(self):
        return self._results

    def fetchone(self):
        return self._results[0] if self._results else None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class MockPgConnection:
    """Mock PostgreSQL connection."""

    def __init__(self):
        self.queries = []
        self.mock_results = []
        self.closed = False

    def cursor(self):
        return MockPgCursor(self)

    def commit(self):
        pass

    def close(self):
        self.closed = True


@pytest.fixture
def mock_pg_connection():
    """Fixture providing mock PostgreSQL connection."""
    return MockPgConnection()


# =============================================================================
# MOCK OPENSEARCH CLIENT
# =============================================================================

class MockOpenSearchClient:
    """In-memory mock of OpenSearch client."""

    def __init__(self):
        self.indexes = {}  # index -> documents

    @property
    def indices(self):
        return self

    def exists(self, index):
        class Response:
            body = index in self.indexes
        return Response()

    def create(self, index, body):
        self.indexes[index] = {}

    def bulk(self, body, refresh=False):
        # Process bulk operations
        i = 0
        while i < len(body):
            action = body[i]
            if "index" in action:
                index_name = action["index"]["_index"]
                doc_id = action["index"]["_id"]
                doc = body[i + 1]
                if index_name not in self.indexes:
                    self.indexes[index_name] = {}
                self.indexes[index_name][doc_id] = doc
                i += 2
            else:
                i += 1

    def search(self, index, body):
        docs = self.indexes.get(index, {})
        k = body.get("size", 10)

        hits = []
        for doc_id, doc in list(docs.items())[:k]:
            hits.append({
                "_id": doc_id,
                "_score": 0.9,
                "_source": doc,
            })

        return {"hits": {"hits": hits}}

    def get(self, index, id):
        docs = self.indexes.get(index, {})
        if id not in docs:
            raise Exception("Not found")
        return {"_id": id, "_source": docs[id]}

    def delete(self, index, id, refresh=False):
        docs = self.indexes.get(index, {})
        if id in docs:
            del docs[id]

    def close(self):
        pass


@pytest.fixture
def mock_opensearch_client():
    """Fixture providing mock OpenSearch client."""
    return MockOpenSearchClient()


# =============================================================================
# SAMPLE DATA
# =============================================================================

@pytest.fixture
def sample_texts():
    """Sample texts for testing."""
    return [
        "Wireless Bluetooth headphones with noise cancellation",
        "Ergonomic office chair with lumbar support",
        "USB-C hub with HDMI and multiple ports",
        "Mechanical keyboard with RGB lighting",
        "4K monitor with HDR support",
    ]


@pytest.fixture
def sample_records(sample_texts, mock_embeddings):
    """Sample records with embeddings."""
    from vectorstore_unified.backends.base import VectorRecord

    records = []
    for i, text in enumerate(sample_texts):
        records.append(VectorRecord(
            id=f"item_{i}",
            text=text,
            embedding=mock_embeddings.embed_text(text),
            metadata={"category": "electronics", "index": i},
        ))
    return records
