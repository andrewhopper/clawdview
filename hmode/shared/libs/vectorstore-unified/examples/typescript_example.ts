/**
 * Example usage of vectorstore-unified (TypeScript)
 *
 * Run with: npx ts-node typescript_example.ts
 */

import {
  VectorStore,
  fromS3Vectors,
  fromPgVector,
  fromOpenSearch,
} from '../typescript/src/index.js';

// =============================================================================
// EXAMPLE 1: S3 Vectors with Bedrock (recommended for AWS)
// =============================================================================

async function exampleS3Vectors(): Promise<void> {
  console.log('Example 1: S3 Vectors with Bedrock');

  const store = new VectorStore({
    backend: 's3-vectors',
    bucket: 'my-vector-bucket',
    index: 'products',
    embeddings: 'bedrock',
    embeddingModel: 'amazon.titan-embed-text-v2:0',
    region: 'us-east-1',
  });

  // Upsert single item
  await store.upsert(
    'prod_001',
    'Wireless Bluetooth headphones with active noise cancellation, 30 hour battery life',
    { category: 'electronics', price: 149.99, brand: 'Sony' }
  );

  // Upsert multiple items
  await store.upsertMany([
    {
      id: 'prod_002',
      text: 'Ergonomic office chair with lumbar support and adjustable armrests',
      metadata: { category: 'furniture', price: 299.99 },
    },
    {
      id: 'prod_003',
      text: 'USB-C hub with 4K HDMI, 3 USB-A ports, SD card reader',
      metadata: { category: 'electronics', price: 49.99 },
    },
  ]);

  // Search (auto-embeds query)
  const results = await store.search('best headphones for music production', { k: 5 });
  console.log('Search results:');
  for (const r of results) {
    console.log(`  - ${r.id}: ${r.score.toFixed(3)} - ${r.text.slice(0, 50)}...`);
  }

  // Search with filter
  const electronics = await store.search('portable accessories', {
    k: 3,
    filter: { category: 'electronics' },
  });
  console.log(`\nFiltered results: ${electronics.length} items`);

  // Get by ID
  const item = await store.get('prod_001');
  if (item) {
    console.log(`\nRetrieved: ${item.id}`);
  }

  // Delete
  await store.delete('prod_003');
  console.log('\nDeleted prod_003');

  await store.close();
}

// =============================================================================
// EXAMPLE 2: pgvector with OpenAI
// =============================================================================

async function examplePgVector(): Promise<void> {
  console.log('\nExample 2: pgvector with OpenAI');

  const store = new VectorStore({
    backend: 'pgvector',
    connectionString: 'postgresql://user:password@localhost:5432/mydb',
    collection: 'documents',
    embeddings: 'openai',
    embeddingModel: 'text-embedding-3-small',
  });

  // Add documents
  await store.upsertMany([
    { id: 'doc_1', text: 'Machine learning is a subset of artificial intelligence.' },
    { id: 'doc_2', text: 'Deep learning uses neural networks with many layers.' },
    { id: 'doc_3', text: 'Natural language processing enables computers to understand text.' },
  ]);

  // Semantic search
  const results = await store.search('how do computers understand language?', { k: 2 });
  for (const r of results) {
    console.log(`${r.id}: ${r.score.toFixed(3)}`);
  }

  await store.close();
}

// =============================================================================
// EXAMPLE 3: OpenSearch Serverless
// =============================================================================

async function exampleOpenSearch(): Promise<void> {
  console.log('\nExample 3: OpenSearch Serverless');

  const store = new VectorStore({
    backend: 'opensearch-serverless',
    endpoint: 'https://xxx.us-east-1.aoss.amazonaws.com',
    index: 'knowledge-base',
    embeddings: 'bedrock',
    region: 'us-east-1',
  });

  // Index documents
  await store.upsertMany([
    { id: 'kb_1', text: 'AWS Lambda is a serverless compute service.', metadata: { topic: 'compute' } },
    { id: 'kb_2', text: 'Amazon S3 provides object storage in the cloud.', metadata: { topic: 'storage' } },
    { id: 'kb_3', text: 'DynamoDB is a fully managed NoSQL database.', metadata: { topic: 'database' } },
  ]);

  // Search with topic filter
  const results = await store.search('serverless database options', {
    k: 5,
    filter: { topic: 'database' },
  });

  await store.close();
}

// =============================================================================
// EXAMPLE 4: Factory functions
// =============================================================================

async function exampleFactory(): Promise<void> {
  console.log('\nExample 4: Factory Functions');

  // Quick initialization
  const store1 = fromS3Vectors('my-bucket', 'my-index');
  const store2 = fromPgVector('postgresql://localhost/mydb');
  const store3 = fromOpenSearch('https://xxx.aoss.amazonaws.com', 'my-index', {
    embeddings: 'openai',
    apiKey: 'sk-...',
  });

  console.log('Created 3 stores with factory functions');

  await store1.close();
  await store2.close();
  await store3.close();
}

// =============================================================================
// EXAMPLE 5: Pre-computed embeddings
// =============================================================================

async function examplePrecomputed(): Promise<void> {
  console.log('\nExample 5: Pre-computed Embeddings');

  const store = new VectorStore({
    backend: 's3-vectors',
    bucket: 'my-bucket',
    index: 'embeddings',
    embeddings: 'bedrock',
  });

  // Get embedding without storing
  const text = 'This is a test document';
  const embedding = await store.embed(text);
  console.log(`Embedding dimension: ${embedding.length}`);

  // Batch embed
  const texts = ['Document 1', 'Document 2', 'Document 3'];
  const embeddings = await store.embedMany(texts);
  console.log(`Generated ${embeddings.length} embeddings`);

  // Search with pre-computed embedding
  const results = await store.searchByVector(embedding, { k: 5 });

  await store.close();
}

// =============================================================================
// Main
// =============================================================================

async function main(): Promise<void> {
  console.log('VectorStore Unified Examples (TypeScript)');
  console.log('='.repeat(50));

  // Uncomment to run examples (requires appropriate credentials/services)
  // await exampleS3Vectors();
  // await examplePgVector();
  // await exampleOpenSearch();
  // await exampleFactory();
  // await examplePrecomputed();

  console.log('\nExamples ready. Uncomment to run.');
}

main().catch(console.error);
