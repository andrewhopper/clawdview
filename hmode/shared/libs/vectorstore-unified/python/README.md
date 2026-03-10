# vectorstore-unified

Pinecone-like API with Algolia-style text search. Unified interface for multiple vector backends.

## Features

- **Simple API**: Upsert text, search with text (auto-embeds)
- **Multiple backends**: S3 Vectors, pgvector, OpenSearch Serverless
- **Multiple embeddings**: AWS Bedrock, OpenAI, Cohere
- **Zero-config text search**: Just `store.search("query")` - no manual embedding

## Installation

```bash
# Core + Bedrock (default)
pip install vectorstore-unified

# With specific backends/embeddings
pip install vectorstore-unified[pgvector]
pip install vectorstore-unified[opensearch]
pip install vectorstore-unified[openai]
pip install vectorstore-unified[all]
```

## Quick Start

```python
from vectorstore_unified import VectorStore

# Initialize with S3 Vectors + Bedrock
store = VectorStore(
    backend="s3-vectors",
    bucket="my-vector-bucket",
    index="products",
    embeddings="bedrock",  # Uses Titan by default
)

# Upsert - auto-embeds text
store.upsert(
    id="prod_123",
    text="Wireless Bluetooth headphones with active noise cancellation",
    metadata={"category": "electronics", "price": 99.99}
)

# Batch upsert
store.upsert_many([
    {"id": "prod_1", "text": "Laptop stand adjustable height", "metadata": {"category": "accessories"}},
    {"id": "prod_2", "text": "USB-C hub with HDMI output", "metadata": {"category": "accessories"}},
])

# Search - auto-embeds query (Algolia-style!)
results = store.search("best headphones for music", k=10)
# Returns: [{"id": "prod_123", "score": 0.92, "text": "...", "metadata": {...}}]

# Search with filter
results = store.search(
    "wireless audio",
    k=5,
    filter={"category": "electronics"}
)

# Get by ID
item = store.get("prod_123")

# Delete
store.delete("prod_123")
```

## Backends

### S3 Vectors (AWS)

```python
store = VectorStore(
    backend="s3-vectors",
    bucket="my-vector-bucket",
    index="my-index",
    region="us-east-1",
)
```

**Pros**: Serverless, cheap storage ($0.06/GB), scales to billions
**Cons**: Higher latency (100-800ms), best for infrequent queries

### pgvector (PostgreSQL)

```python
store = VectorStore(
    backend="pgvector",
    connection_string="postgresql://user:pass@host:5432/db",
    collection="vectors",
)
```

**Pros**: Low latency (10-50ms), SQL integration, mature ecosystem
**Cons**: Requires running PostgreSQL

### OpenSearch Serverless

```python
store = VectorStore(
    backend="opensearch-serverless",
    endpoint="https://xxx.us-east-1.aoss.amazonaws.com",
    index="vectors",
)
```

**Pros**: Hybrid search (vector + keyword), serverless, real-time
**Cons**: Higher cost than S3 Vectors

## Embedding Providers

### AWS Bedrock (default)

```python
store = VectorStore(
    embeddings="bedrock",
    embedding_model="amazon.titan-embed-text-v2:0",  # 1024 dims
    region="us-east-1",
)
```

### OpenAI

```python
store = VectorStore(
    embeddings="openai",
    embedding_model="text-embedding-3-small",  # 1536 dims
    api_key="sk-...",  # Or set OPENAI_API_KEY
)
```

### Cohere

```python
store = VectorStore(
    embeddings="cohere",
    embedding_model="embed-english-v3.0",  # 1024 dims
    api_key="...",  # Or set COHERE_API_KEY
)
```

## Factory Functions

```python
from vectorstore_unified import from_s3_vectors, from_pgvector, from_opensearch

# Quick initialization
store = from_s3_vectors("my-bucket", "my-index")
store = from_pgvector("postgresql://...")
store = from_opensearch("https://xxx.aoss.amazonaws.com", "my-index")
```

## Advanced Usage

### Pre-computed Embeddings

```python
# Get embedding without storing
embedding = store.embed("some text")

# Search with pre-computed embedding
results = store.search_by_vector(embedding, k=10)
```

### Context Manager

```python
with VectorStore(...) as store:
    store.upsert("id", "text")
    results = store.search("query")
# Connection auto-closed
```

### Custom Embeddings

```python
from vectorstore_unified.embeddings import BaseEmbeddings

class MyEmbeddings(BaseEmbeddings):
    @property
    def dimension(self) -> int:
        return 768

    def embed_text(self, text: str) -> list[float]:
        # Your embedding logic
        return [...]

store = VectorStore(
    backend="s3-vectors",
    bucket="...",
    index="...",
    embeddings=MyEmbeddings(),
)
```

## Comparison with Alternatives

| Feature | vectorstore-unified | LangChain | Pinecone SDK |
|---------|--------------------|-----------| -------------|
| Auto-embed on search | ✅ | ❌ | ❌ |
| Multi-backend | ✅ | ✅ | ❌ |
| Simple API | ✅ | ❌ | ✅ |
| S3 Vectors support | ✅ | ✅ | ❌ |
| Zero dependencies* | ✅ | ❌ | ✅ |

*Core only requires boto3

## License

MIT
