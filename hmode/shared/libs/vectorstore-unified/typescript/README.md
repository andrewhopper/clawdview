# vectorstore-unified (TypeScript)

Pinecone-like API with Algolia-style text search. Unified interface for multiple vector backends.

## Installation

```bash
npm install vectorstore-unified

# Optional peer dependencies by backend
npm install pg pgvector                        # for pgvector
npm install @opensearch-project/opensearch     # for OpenSearch
npm install openai                             # for OpenAI embeddings
```

## Quick Start

```typescript
import { VectorStore } from 'vectorstore-unified';

// Initialize with S3 Vectors + Bedrock
const store = new VectorStore({
  backend: 's3-vectors',
  bucket: 'my-vector-bucket',
  index: 'products',
  embeddings: 'bedrock',
});

// Upsert - auto-embeds text
await store.upsert(
  'prod_123',
  'Wireless Bluetooth headphones with active noise cancellation',
  { category: 'electronics', price: 99.99 }
);

// Batch upsert
await store.upsertMany([
  { id: 'prod_1', text: 'Laptop stand adjustable height', metadata: { category: 'accessories' } },
  { id: 'prod_2', text: 'USB-C hub with HDMI output', metadata: { category: 'accessories' } },
]);

// Search - auto-embeds query (Algolia-style!)
const results = await store.search('best headphones for music', { k: 10 });
// Returns: [{ id: 'prod_123', score: 0.92, text: '...', metadata: {...} }]

// Search with filter
const filtered = await store.search('wireless audio', {
  k: 5,
  filter: { category: 'electronics' },
});

// Get by ID
const item = await store.get('prod_123');

// Delete
await store.delete('prod_123');

// Clean up
await store.close();
```

## Backends

### S3 Vectors (AWS)

```typescript
const store = new VectorStore({
  backend: 's3-vectors',
  bucket: 'my-vector-bucket',
  index: 'my-index',
  region: 'us-east-1',
});
```

### pgvector (PostgreSQL)

```typescript
const store = new VectorStore({
  backend: 'pgvector',
  connectionString: 'postgresql://user:pass@host:5432/db',
  collection: 'vectors',
});
```

### OpenSearch Serverless

```typescript
const store = new VectorStore({
  backend: 'opensearch-serverless',
  endpoint: 'https://xxx.us-east-1.aoss.amazonaws.com',
  index: 'vectors',
});
```

## Embedding Providers

### AWS Bedrock (default)

```typescript
const store = new VectorStore({
  backend: 's3-vectors',
  bucket: '...',
  index: '...',
  embeddings: 'bedrock',
  embeddingModel: 'amazon.titan-embed-text-v2:0',
  region: 'us-east-1',
});
```

### OpenAI

```typescript
const store = new VectorStore({
  backend: 'pgvector',
  connectionString: '...',
  embeddings: 'openai',
  embeddingModel: 'text-embedding-3-small',
  apiKey: 'sk-...', // or set OPENAI_API_KEY
});
```

### Cohere

```typescript
const store = new VectorStore({
  backend: 'opensearch-serverless',
  endpoint: '...',
  embeddings: 'cohere',
  embeddingModel: 'embed-english-v3.0',
  apiKey: '...', // or set COHERE_API_KEY
});
```

## Factory Functions

```typescript
import { fromS3Vectors, fromPgVector, fromOpenSearch } from 'vectorstore-unified';

const store1 = fromS3Vectors('my-bucket', 'my-index');
const store2 = fromPgVector('postgresql://...');
const store3 = fromOpenSearch('https://xxx.aoss.amazonaws.com', 'my-index');
```

## Advanced Usage

### Pre-computed Embeddings

```typescript
// Get embedding without storing
const embedding = await store.embed('some text');

// Search with pre-computed embedding
const results = await store.searchByVector(embedding, { k: 10 });
```

### Custom Embeddings

```typescript
import { BaseEmbeddings, VectorStore } from 'vectorstore-unified';

class MyEmbeddings extends BaseEmbeddings {
  readonly dimension = 768;

  async embedText(text: string): Promise<number[]> {
    // Your embedding logic
    return [];
  }

  async embedTexts(texts: string[]): Promise<number[][]> {
    return Promise.all(texts.map(t => this.embedText(t)));
  }
}

const store = new VectorStore({
  backend: 's3-vectors',
  bucket: '...',
  index: '...',
  embeddings: new MyEmbeddings(),
});
```

## License

MIT
