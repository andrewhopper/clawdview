/**
 * Tests for the main VectorStore class.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock all external dependencies
vi.mock('@aws-sdk/client-bedrock-runtime', () => ({
  BedrockRuntimeClient: vi.fn().mockImplementation(() => ({
    send: vi.fn().mockResolvedValue({
      body: new TextEncoder().encode(
        JSON.stringify({ embedding: Array(1024).fill(0.1) })
      ),
    }),
  })),
  InvokeModelCommand: vi.fn(),
}));

vi.mock('pg', () => ({
  default: {
    Pool: vi.fn().mockImplementation(() => ({
      connect: vi.fn().mockResolvedValue({
        query: vi.fn().mockResolvedValue({ rows: [], rowCount: 0 }),
        release: vi.fn(),
      }),
      query: vi.fn().mockResolvedValue({ rows: [], rowCount: 0 }),
      end: vi.fn(),
    })),
  },
}));

describe('VectorStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('initialization', () => {
    it('should initialize with s3-vectors backend', async () => {
      const { VectorStore } = await import('../src/store.js');

      const store = new VectorStore({
        backend: 's3-vectors',
        bucket: 'test-bucket',
        index: 'test-index',
        embeddings: 'bedrock',
      });

      expect(store).toBeDefined();
      expect(store.dimension).toBe(1024);
    });

    it('should initialize with pgvector backend', async () => {
      const { VectorStore } = await import('../src/store.js');

      const store = new VectorStore({
        backend: 'pgvector',
        connectionString: 'postgresql://test/test',
        embeddings: 'bedrock',
      });

      expect(store).toBeDefined();
    });

    it('should throw error for missing bucket with s3-vectors', async () => {
      const { VectorStore } = await import('../src/store.js');

      expect(
        () =>
          new VectorStore({
            backend: 's3-vectors',
            index: 'test-index',
            embeddings: 'bedrock',
          })
      ).toThrow("'bucket'");
    });

    it('should throw error for missing connection string with pgvector', async () => {
      const { VectorStore } = await import('../src/store.js');

      expect(
        () =>
          new VectorStore({
            backend: 'pgvector',
            embeddings: 'bedrock',
          })
      ).toThrow("'connectionString'");
    });

    it('should throw error for unknown backend', async () => {
      const { VectorStore } = await import('../src/store.js');

      expect(
        () =>
          new VectorStore({
            backend: 'unknown' as 's3-vectors',
            embeddings: 'bedrock',
          })
      ).toThrow('Unknown backend');
    });

    it('should throw error for unknown embeddings', async () => {
      const { VectorStore } = await import('../src/store.js');

      expect(
        () =>
          new VectorStore({
            backend: 's3-vectors',
            bucket: 'test',
            index: 'test',
            embeddings: 'unknown' as 'bedrock',
          })
      ).toThrow('Unknown embeddings');
    });
  });

  describe('operations', () => {
    it('should upsert a single item', async () => {
      const { VectorStore } = await import('../src/store.js');

      const store = new VectorStore({
        backend: 's3-vectors',
        bucket: 'test-bucket',
        index: 'test-index',
        embeddings: 'bedrock',
      });

      // Should not throw
      await expect(
        store.upsert('test-id', 'Test text', { key: 'value' })
      ).resolves.not.toThrow();
    });

    it('should upsert multiple items', async () => {
      const { VectorStore } = await import('../src/store.js');

      const store = new VectorStore({
        backend: 's3-vectors',
        bucket: 'test-bucket',
        index: 'test-index',
        embeddings: 'bedrock',
      });

      const items = [
        { id: 'item-1', text: 'First item' },
        { id: 'item-2', text: 'Second item' },
        { id: 'item-3', text: 'Third item' },
      ];

      await expect(store.upsertMany(items)).resolves.not.toThrow();
    });

    it('should search and return results', async () => {
      const { VectorStore } = await import('../src/store.js');

      const store = new VectorStore({
        backend: 's3-vectors',
        bucket: 'test-bucket',
        index: 'test-index',
        embeddings: 'bedrock',
      });

      const results = await store.search('test query', { k: 5 });

      expect(Array.isArray(results)).toBe(true);
    });

    it('should search by vector', async () => {
      const { VectorStore } = await import('../src/store.js');

      const store = new VectorStore({
        backend: 's3-vectors',
        bucket: 'test-bucket',
        index: 'test-index',
        embeddings: 'bedrock',
      });

      const embedding = Array(1024).fill(0.1);
      const results = await store.searchByVector(embedding, { k: 5 });

      expect(Array.isArray(results)).toBe(true);
    });

    it('should embed text without storing', async () => {
      const { VectorStore } = await import('../src/store.js');

      const store = new VectorStore({
        backend: 's3-vectors',
        bucket: 'test-bucket',
        index: 'test-index',
        embeddings: 'bedrock',
      });

      const embedding = await store.embed('Test text');

      expect(Array.isArray(embedding)).toBe(true);
      expect(embedding.length).toBe(1024);
    });

    it('should embed multiple texts', async () => {
      const { VectorStore } = await import('../src/store.js');

      const store = new VectorStore({
        backend: 's3-vectors',
        bucket: 'test-bucket',
        index: 'test-index',
        embeddings: 'bedrock',
      });

      const embeddings = await store.embedMany(['Text 1', 'Text 2', 'Text 3']);

      expect(embeddings.length).toBe(3);
      expect(embeddings.every((e) => e.length === 1024)).toBe(true);
    });
  });

  describe('dimension property', () => {
    it('should return embedding dimension', async () => {
      const { VectorStore } = await import('../src/store.js');

      const store = new VectorStore({
        backend: 's3-vectors',
        bucket: 'test-bucket',
        index: 'test-index',
        embeddings: 'bedrock',
      });

      expect(store.dimension).toBe(1024);
    });
  });
});

describe('Factory functions', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should create store with fromS3Vectors', async () => {
    const { fromS3Vectors } = await import('../src/store.js');

    const store = fromS3Vectors('my-bucket', 'my-index');

    expect(store).toBeDefined();
  });

  it('should create store with fromPgVector', async () => {
    const { fromPgVector } = await import('../src/store.js');

    const store = fromPgVector('postgresql://test/test');

    expect(store).toBeDefined();
  });

  it('should accept additional options in factory functions', async () => {
    const { fromS3Vectors } = await import('../src/store.js');

    const store = fromS3Vectors('my-bucket', 'my-index', {
      region: 'us-west-2',
      embeddingModel: 'amazon.titan-embed-text-v1',
    });

    expect(store).toBeDefined();
  });
});

describe('Search options', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should support k parameter', async () => {
    const { VectorStore } = await import('../src/store.js');

    const store = new VectorStore({
      backend: 's3-vectors',
      bucket: 'test-bucket',
      index: 'test-index',
      embeddings: 'bedrock',
    });

    // Should not throw with k parameter
    await expect(store.search('query', { k: 10 })).resolves.not.toThrow();
  });

  it('should support filter parameter', async () => {
    const { VectorStore } = await import('../src/store.js');

    const store = new VectorStore({
      backend: 's3-vectors',
      bucket: 'test-bucket',
      index: 'test-index',
      embeddings: 'bedrock',
    });

    // Should not throw with filter parameter
    await expect(
      store.search('query', {
        k: 5,
        filter: { category: 'electronics' },
      })
    ).resolves.not.toThrow();
  });
});

describe('UpsertItem interface', () => {
  it('should support metadata in upsert items', async () => {
    const { VectorStore } = await import('../src/store.js');

    const store = new VectorStore({
      backend: 's3-vectors',
      bucket: 'test-bucket',
      index: 'test-index',
      embeddings: 'bedrock',
    });

    const items = [
      {
        id: 'item-1',
        text: 'Item with metadata',
        metadata: { category: 'test', price: 99.99 },
      },
      {
        id: 'item-2',
        text: 'Item without metadata',
      },
    ];

    await expect(store.upsertMany(items)).resolves.not.toThrow();
  });
});
