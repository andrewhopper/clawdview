"""
Example usage of vectorstore-unified (Python)

Run with: python python_example.py
"""

from vectorstore_unified import VectorStore, from_s3_vectors

# =============================================================================
# EXAMPLE 1: S3 Vectors with Bedrock (recommended for AWS)
# =============================================================================

def example_s3_vectors():
    """Use S3 Vectors with Bedrock embeddings."""

    store = VectorStore(
        backend="s3-vectors",
        bucket="my-vector-bucket",
        index="products",
        embeddings="bedrock",
        embedding_model="amazon.titan-embed-text-v2:0",
        region="us-east-1",
    )

    # Upsert single item
    store.upsert(
        id="prod_001",
        text="Wireless Bluetooth headphones with active noise cancellation, 30 hour battery life",
        metadata={"category": "electronics", "price": 149.99, "brand": "Sony"}
    )

    # Upsert multiple items
    store.upsert_many([
        {
            "id": "prod_002",
            "text": "Ergonomic office chair with lumbar support and adjustable armrests",
            "metadata": {"category": "furniture", "price": 299.99}
        },
        {
            "id": "prod_003",
            "text": "USB-C hub with 4K HDMI, 3 USB-A ports, SD card reader",
            "metadata": {"category": "electronics", "price": 49.99}
        },
    ])

    # Search (auto-embeds query)
    results = store.search("best headphones for music production", k=5)
    print("Search results:")
    for r in results:
        print(f"  - {r['id']}: {r['score']:.3f} - {r['text'][:50]}...")

    # Search with filter
    electronics = store.search(
        "portable accessories",
        k=3,
        filter={"category": "electronics"}
    )
    print(f"\nFiltered results: {len(electronics)} items")

    # Get by ID
    item = store.get("prod_001")
    if item:
        print(f"\nRetrieved: {item['id']}")

    # Delete
    store.delete("prod_003")
    print("\nDeleted prod_003")


# =============================================================================
# EXAMPLE 2: pgvector with OpenAI
# =============================================================================

def example_pgvector():
    """Use pgvector with OpenAI embeddings."""

    store = VectorStore(
        backend="pgvector",
        connection_string="postgresql://user:password@localhost:5432/mydb",
        collection="documents",
        embeddings="openai",
        embedding_model="text-embedding-3-small",
    )

    # Add documents
    store.upsert_many([
        {"id": "doc_1", "text": "Machine learning is a subset of artificial intelligence."},
        {"id": "doc_2", "text": "Deep learning uses neural networks with many layers."},
        {"id": "doc_3", "text": "Natural language processing enables computers to understand text."},
    ])

    # Semantic search
    results = store.search("how do computers understand language?", k=2)
    for r in results:
        print(f"{r['id']}: {r['score']:.3f}")

    store.close()


# =============================================================================
# EXAMPLE 3: OpenSearch Serverless with hybrid search
# =============================================================================

def example_opensearch():
    """Use OpenSearch Serverless for hybrid search."""

    store = VectorStore(
        backend="opensearch-serverless",
        endpoint="https://xxx.us-east-1.aoss.amazonaws.com",
        index="knowledge-base",
        embeddings="bedrock",
        region="us-east-1",
    )

    # Index documents
    store.upsert_many([
        {"id": "kb_1", "text": "AWS Lambda is a serverless compute service.", "metadata": {"topic": "compute"}},
        {"id": "kb_2", "text": "Amazon S3 provides object storage in the cloud.", "metadata": {"topic": "storage"}},
        {"id": "kb_3", "text": "DynamoDB is a fully managed NoSQL database.", "metadata": {"topic": "database"}},
    ])

    # Search with topic filter
    results = store.search(
        "serverless database options",
        k=5,
        filter={"topic": "database"}
    )

    store.close()


# =============================================================================
# EXAMPLE 4: Factory functions (quick initialization)
# =============================================================================

def example_factory():
    """Use factory functions for quick setup."""

    # S3 Vectors
    store1 = from_s3_vectors("my-bucket", "my-index")

    # Or with options
    from vectorstore_unified import from_pgvector, from_opensearch

    store2 = from_pgvector(
        "postgresql://localhost/mydb",
        collection="vectors",
        embeddings="bedrock",
    )

    store3 = from_opensearch(
        "https://xxx.aoss.amazonaws.com",
        index="vectors",
        embeddings="openai",
        api_key="sk-...",
    )


# =============================================================================
# EXAMPLE 5: Pre-computed embeddings
# =============================================================================

def example_precomputed():
    """Use pre-computed embeddings for efficiency."""

    store = VectorStore(
        backend="s3-vectors",
        bucket="my-bucket",
        index="embeddings",
        embeddings="bedrock",
    )

    # Get embedding without storing
    text = "This is a test document"
    embedding = store.embed(text)
    print(f"Embedding dimension: {len(embedding)}")

    # Batch embed
    texts = ["Document 1", "Document 2", "Document 3"]
    embeddings = store.embed_many(texts)
    print(f"Generated {len(embeddings)} embeddings")

    # Search with pre-computed embedding
    results = store.search_by_vector(embedding, k=5)


# =============================================================================
# EXAMPLE 6: Context manager
# =============================================================================

def example_context_manager():
    """Use context manager for automatic cleanup."""

    with VectorStore(
        backend="pgvector",
        connection_string="postgresql://localhost/mydb",
        embeddings="bedrock",
    ) as store:
        store.upsert("id", "text content")
        results = store.search("query")
    # Connection auto-closed


if __name__ == "__main__":
    print("VectorStore Unified Examples")
    print("=" * 50)

    # Run the S3 Vectors example (requires AWS credentials)
    # example_s3_vectors()

    print("\nExamples ready. Uncomment to run.")
