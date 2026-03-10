# Unified VectorStore Library

## 1.0 OVERVIEW

Pinecone-like API with Algolia-style text search, supporting multiple backends.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        VectorStore (unified API)                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  .upsert(id, text, metadata)     # Auto-embeds text         │    │
│  │  .search(query_text, k=10)       # Auto-embeds query        │    │
│  │  .delete(id)                     # Remove by ID             │    │
│  │  .get(id)                        # Fetch by ID              │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌───────────┐   ┌───────────┐   ┌───────────────┐
        │ S3Vectors │   │ pgvector  │   │ OpenSearch    │
        │  Backend  │   │  Backend  │   │  Serverless   │
        └───────────┘   └───────────┘   └───────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Embeddings Provider │
                    │  ┌─────────────────┐  │
                    │  │ Bedrock (Titan) │  │
                    │  │ Cohere          │  │
                    │  │ OpenAI          │  │
                    │  └─────────────────┘  │
                    └───────────────────────┘
```

## 2.0 API DESIGN (Pinecone + Algolia style)

### 2.1 Initialization
```python
from vectorstore_unified import VectorStore

# S3 Vectors backend (default)
store = VectorStore(
    backend="s3-vectors",
    bucket="my-vector-bucket",
    index="products",
    embeddings="bedrock",  # or "openai", "cohere"
    model="amazon.titan-embed-text-v2:0"
)

# pgvector backend
store = VectorStore(
    backend="pgvector",
    connection_string="postgresql://...",
    collection="products"
)

# OpenSearch Serverless backend
store = VectorStore(
    backend="opensearch-serverless",
    endpoint="https://xxx.us-east-1.aoss.amazonaws.com",
    index="products"
)
```

### 2.2 Core Operations
```python
# Upsert - auto-embeds text
store.upsert(
    id="prod_123",
    text="Wireless Bluetooth headphones with noise cancellation",
    metadata={"category": "electronics", "price": 99.99}
)

# Batch upsert
store.upsert_many([
    {"id": "prod_1", "text": "...", "metadata": {...}},
    {"id": "prod_2", "text": "...", "metadata": {...}},
])

# Search - auto-embeds query (Algolia-style)
results = store.search(
    query="best headphones for music",
    k=10,
    filter={"category": "electronics"}
)
# Returns: [{"id": "prod_123", "score": 0.92, "text": "...", "metadata": {...}}]

# Get by ID
item = store.get("prod_123")

# Delete
store.delete("prod_123")
store.delete_many(["prod_1", "prod_2"])
```

### 2.3 Advanced Features
```python
# Hybrid search (text + vector)
results = store.search(
    query="noise cancelling",
    mode="hybrid",  # "vector" | "keyword" | "hybrid"
    alpha=0.7  # 70% vector, 30% keyword
)

# Search with pre-computed embedding
results = store.search_by_vector(
    embedding=[0.1, 0.2, ...],
    k=10
)

# Namespace/collection isolation
store = VectorStore(..., namespace="production")
```

## 3.0 BACKEND COMPARISON

| Feature | S3 Vectors | pgvector | OpenSearch Serverless |
|---------|------------|----------|----------------------|
| Latency | 100-800ms | 10-50ms | 20-100ms |
| Scale | 2B vectors | 10M+ | 100M+ |
| Cost | $0.06/GB | DB instance | Per-OCU |
| Serverless | ✓ | ✗ | ✓ |
| Hybrid Search | ✗ | ✗ | ✓ |
| Best For | Archival, batch | OLTP apps | Real-time search |

## 4.0 EMBEDDING PROVIDERS

| Provider | Model | Dimensions | Cost |
|----------|-------|------------|------|
| Bedrock (Titan) | amazon.titan-embed-text-v2:0 | 1024 | $0.0001/1K tokens |
| Bedrock (Cohere) | cohere.embed-english-v3 | 1024 | $0.0001/1K tokens |
| OpenAI | text-embedding-3-small | 1536 | $0.00002/1K tokens |
| Cohere | embed-english-v3.0 | 1024 | $0.0001/1K tokens |

## 5.0 FILE STRUCTURE

```
vectorstore-unified/
├── python/
│   ├── vectorstore_unified/
│   │   ├── __init__.py
│   │   ├── store.py           # Main VectorStore class
│   │   ├── backends/
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # Abstract backend
│   │   │   ├── s3_vectors.py  # AWS S3 Vectors
│   │   │   ├── pgvector.py    # PostgreSQL pgvector
│   │   │   └── opensearch.py  # OpenSearch Serverless
│   │   └── embeddings/
│   │       ├── __init__.py
│   │       ├── base.py        # Abstract embeddings
│   │       ├── bedrock.py     # AWS Bedrock
│   │       ├── openai.py      # OpenAI
│   │       └── cohere.py      # Cohere
│   ├── pyproject.toml
│   └── README.md
├── typescript/
│   ├── src/
│   │   ├── index.ts
│   │   ├── store.ts
│   │   ├── backends/
│   │   │   ├── index.ts
│   │   │   ├── base.ts
│   │   │   ├── s3-vectors.ts
│   │   │   ├── pgvector.ts
│   │   │   └── opensearch.ts
│   │   └── embeddings/
│   │       ├── index.ts
│   │       ├── base.ts
│   │       ├── bedrock.ts
│   │       ├── openai.ts
│   │       └── cohere.ts
│   ├── package.json
│   └── tsconfig.json
└── ARCHITECTURE.md
```
