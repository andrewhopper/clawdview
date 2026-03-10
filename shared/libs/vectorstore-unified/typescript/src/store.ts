/**
 * Unified VectorStore - Pinecone-like API with Algolia-style text search.
 */
import {
  BaseBackend,
  VectorRecord,
  SearchResult,
  S3VectorsBackend,
  PgVectorBackend,
  OpenSearchBackend,
} from './backends/index.js';
import {
  BaseEmbeddings,
  BedrockEmbeddings,
  OpenAIEmbeddings,
  CohereEmbeddings,
} from './embeddings/index.js';

export type BackendType = 's3-vectors' | 'pgvector' | 'opensearch-serverless';
export type EmbeddingsType = 'bedrock' | 'openai' | 'cohere';

export interface VectorStoreOptions {
  backend: BackendType;
  embeddings?: EmbeddingsType | BaseEmbeddings;

  // S3 Vectors options
  bucket?: string;
  index?: string;

  // pgvector options
  connectionString?: string;
  collection?: string;

  // OpenSearch options
  endpoint?: string;

  // Common options
  region?: string;
  dimension?: number;
  distanceMetric?: 'cosine' | 'euclidean';

  // Embeddings options
  embeddingModel?: string;
  apiKey?: string;
}

export interface SearchOptions {
  k?: number;
  filter?: Record<string, unknown>;
}

export interface UpsertItem {
  id: string;
  text: string;
  metadata?: Record<string, unknown>;
}

/**
 * Unified vector store with Pinecone-like API and Algolia-style text search.
 */
export class VectorStore {
  private readonly backend: BaseBackend;
  private readonly embeddings: BaseEmbeddings;

  constructor(options: VectorStoreOptions) {
    // Initialize embeddings
    this.embeddings = this.initEmbeddings(options);

    // Get dimension from embeddings if not specified
    const dimension = options.dimension ?? this.embeddings.dimension;

    // Initialize backend
    this.backend = this.initBackend({ ...options, dimension });
  }

  private initEmbeddings(options: VectorStoreOptions): BaseEmbeddings {
    const embeddings = options.embeddings ?? 'bedrock';

    if (typeof embeddings !== 'string') {
      return embeddings;
    }

    switch (embeddings) {
      case 'bedrock':
        return new BedrockEmbeddings({
          modelId: options.embeddingModel,
          region: options.region,
        });
      case 'openai':
        return new OpenAIEmbeddings({
          model: options.embeddingModel,
          apiKey: options.apiKey,
        });
      case 'cohere':
        return new CohereEmbeddings({
          model: options.embeddingModel,
          apiKey: options.apiKey,
        });
      default:
        throw new Error(`Unknown embeddings provider: ${embeddings}`);
    }
  }

  private initBackend(options: VectorStoreOptions & { dimension: number }): BaseBackend {
    switch (options.backend) {
      case 's3-vectors':
        if (!options.bucket || !options.index) {
          throw new Error("S3 Vectors requires 'bucket' and 'index'");
        }
        return new S3VectorsBackend({
          bucket: options.bucket,
          index: options.index,
          region: options.region,
          dimension: options.dimension,
          distanceMetric: options.distanceMetric,
        });

      case 'pgvector':
        if (!options.connectionString) {
          throw new Error("pgvector requires 'connectionString'");
        }
        return new PgVectorBackend({
          connectionString: options.connectionString,
          collection: options.collection,
          dimension: options.dimension,
          distanceMetric: options.distanceMetric,
        });

      case 'opensearch-serverless':
        if (!options.endpoint) {
          throw new Error("OpenSearch requires 'endpoint'");
        }
        return new OpenSearchBackend({
          endpoint: options.endpoint,
          index: options.index ?? options.collection ?? 'vectors',
          region: options.region,
          dimension: options.dimension,
        });

      default:
        throw new Error(`Unknown backend: ${options.backend}`);
    }
  }

  // =========================================================================
  // CORE API (Pinecone-style)
  // =========================================================================

  /**
   * Insert or update a single record.
   * Auto-embeds the text using the configured embedding provider.
   */
  async upsert(
    id: string,
    text: string,
    metadata: Record<string, unknown> = {}
  ): Promise<void> {
    const embedding = await this.embeddings.embedText(text);
    const record: VectorRecord = {
      id,
      text,
      embedding,
      metadata,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    await this.backend.upsert(record);
  }

  /**
   * Insert or update multiple records.
   */
  async upsertMany(items: UpsertItem[]): Promise<void> {
    const texts = items.map((item) => item.text);
    const embeddings = await this.embeddings.embedTexts(texts);

    const records: VectorRecord[] = items.map((item, idx) => ({
      id: item.id,
      text: item.text,
      embedding: embeddings[idx],
      metadata: item.metadata ?? {},
      createdAt: new Date(),
      updatedAt: new Date(),
    }));

    await this.backend.upsertMany(records);
  }

  /**
   * Search for similar items (Algolia-style).
   * Auto-embeds the query and searches the vector store.
   */
  async search(
    query: string,
    options: SearchOptions = {}
  ): Promise<SearchResult[]> {
    const embedding = await this.embeddings.embedQuery(query);
    return this.backend.search(embedding, options);
  }

  /**
   * Search using a pre-computed embedding.
   */
  async searchByVector(
    embedding: number[],
    options: SearchOptions = {}
  ): Promise<SearchResult[]> {
    return this.backend.search(embedding, options);
  }

  /**
   * Get a record by ID.
   */
  async get(id: string): Promise<VectorRecord | null> {
    return this.backend.get(id);
  }

  /**
   * Delete a record by ID.
   */
  async delete(id: string): Promise<boolean> {
    return this.backend.delete(id);
  }

  /**
   * Delete multiple records.
   */
  async deleteMany(ids: string[]): Promise<number> {
    return this.backend.deleteMany(ids);
  }

  // =========================================================================
  // CONVENIENCE METHODS
  // =========================================================================

  /**
   * Get embedding for text without storing.
   */
  async embed(text: string): Promise<number[]> {
    return this.embeddings.embedText(text);
  }

  /**
   * Get embeddings for multiple texts.
   */
  async embedMany(texts: string[]): Promise<number[][]> {
    return this.embeddings.embedTexts(texts);
  }

  /**
   * Get the embedding dimension.
   */
  get dimension(): number {
    return this.embeddings.dimension;
  }

  /**
   * Close any backend connections.
   */
  async close(): Promise<void> {
    await this.backend.close();
  }
}

// Factory functions
export function fromS3Vectors(
  bucket: string,
  index: string,
  options: Partial<VectorStoreOptions> = {}
): VectorStore {
  return new VectorStore({
    backend: 's3-vectors',
    bucket,
    index,
    ...options,
  });
}

export function fromPgVector(
  connectionString: string,
  collection = 'vectors',
  options: Partial<VectorStoreOptions> = {}
): VectorStore {
  return new VectorStore({
    backend: 'pgvector',
    connectionString,
    collection,
    ...options,
  });
}

export function fromOpenSearch(
  endpoint: string,
  index = 'vectors',
  options: Partial<VectorStoreOptions> = {}
): VectorStore {
  return new VectorStore({
    backend: 'opensearch-serverless',
    endpoint,
    index,
    ...options,
  });
}
