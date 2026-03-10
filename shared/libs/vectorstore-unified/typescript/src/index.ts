/**
 * Unified VectorStore Library
 *
 * Pinecone-like API with Algolia-style text search.
 *
 * @example
 * ```typescript
 * import { VectorStore } from 'vectorstore-unified';
 *
 * const store = new VectorStore({
 *   backend: 's3-vectors',
 *   bucket: 'my-bucket',
 *   index: 'products',
 *   embeddings: 'bedrock',
 * });
 *
 * await store.upsert('id1', 'Product description', { price: 99 });
 * const results = await store.search('wireless headphones', 10);
 * ```
 */

export { VectorStore, VectorStoreOptions } from './store.js';
export {
  BaseBackend,
  VectorRecord,
  SearchResult,
  S3VectorsBackend,
  PgVectorBackend,
  OpenSearchBackend,
} from './backends/index.js';
export {
  BaseEmbeddings,
  BedrockEmbeddings,
  OpenAIEmbeddings,
  CohereEmbeddings,
} from './embeddings/index.js';
