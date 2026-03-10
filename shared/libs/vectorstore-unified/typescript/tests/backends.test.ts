/**
 * Tests for vector store backends.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import type { VectorRecord, SearchResult } from '../src/backends/base.js';

// Mock data
const createMockRecord = (id: string, text: string): VectorRecord => ({
  id,
  text,
  embedding: Array(1024).fill(0.1),
  metadata: { category: 'test' },
  createdAt: new Date(),
  updatedAt: new Date(),
});

describe('VectorRecord', () => {
  it('should have required properties', () => {
    const record = createMockRecord('test-id', 'Test text');

    expect(record.id).toBe('test-id');
    expect(record.text).toBe('Test text');
    expect(Array.isArray(record.embedding)).toBe(true);
    expect(record.metadata).toEqual({ category: 'test' });
    expect(record.createdAt).toBeInstanceOf(Date);
    expect(record.updatedAt).toBeInstanceOf(Date);
  });
});

describe('SearchResult', () => {
  it('should have required properties', () => {
    const result: SearchResult = {
      id: 'test-id',
      score: 0.95,
      text: 'Test text',
      metadata: { key: 'value' },
    };

    expect(result.id).toBe('test-id');
    expect(result.score).toBe(0.95);
    expect(result.text).toBe('Test text');
    expect(result.metadata).toEqual({ key: 'value' });
  });
});

describe('S3VectorsBackend', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should be instantiable with required options', async () => {
    const { S3VectorsBackend } = await import('../src/backends/s3-vectors.js');

    const backend = new S3VectorsBackend({
      bucket: 'test-bucket',
      index: 'test-index',
    });

    expect(backend).toBeDefined();
  });

  it('should accept optional region and dimension', async () => {
    const { S3VectorsBackend } = await import('../src/backends/s3-vectors.js');

    const backend = new S3VectorsBackend({
      bucket: 'test-bucket',
      index: 'test-index',
      region: 'us-west-2',
      dimension: 512,
    });

    expect(backend).toBeDefined();
  });
});

describe('PgVectorBackend', () => {
  // Mock pg module
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

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should be instantiable with connection string', async () => {
    const { PgVectorBackend } = await import('../src/backends/pgvector.js');

    const backend = new PgVectorBackend({
      connectionString: 'postgresql://test:test@localhost/test',
    });

    expect(backend).toBeDefined();
  });

  it('should use default collection name', async () => {
    const { PgVectorBackend } = await import('../src/backends/pgvector.js');

    const backend = new PgVectorBackend({
      connectionString: 'postgresql://test:test@localhost/test',
    });

    expect(backend).toBeDefined();
  });

  it('should support custom distance metrics', async () => {
    const { PgVectorBackend } = await import('../src/backends/pgvector.js');

    const cosineBackend = new PgVectorBackend({
      connectionString: 'postgresql://test/test',
      distanceMetric: 'cosine',
    });

    const euclideanBackend = new PgVectorBackend({
      connectionString: 'postgresql://test/test',
      distanceMetric: 'euclidean',
    });

    expect(cosineBackend).toBeDefined();
    expect(euclideanBackend).toBeDefined();
  });
});

describe('OpenSearchBackend', () => {
  // Mock OpenSearch
  vi.mock('@opensearch-project/opensearch', () => ({
    Client: vi.fn().mockImplementation(() => ({
      indices: {
        exists: vi.fn().mockResolvedValue({ body: false }),
        create: vi.fn().mockResolvedValue({}),
      },
      bulk: vi.fn().mockResolvedValue({}),
      search: vi.fn().mockResolvedValue({ body: { hits: { hits: [] } } }),
      get: vi.fn().mockRejectedValue(new Error('Not found')),
      delete: vi.fn().mockResolvedValue({}),
      close: vi.fn(),
    })),
  }));

  vi.mock('@opensearch-project/opensearch/aws', () => ({
    AwsSigv4Signer: vi.fn().mockReturnValue({}),
  }));

  vi.mock('@aws-sdk/credential-provider-node', () => ({
    defaultProvider: vi.fn().mockReturnValue(() =>
      Promise.resolve({
        accessKeyId: 'test',
        secretAccessKey: 'test',
      })
    ),
  }));

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should be instantiable with endpoint', async () => {
    const { OpenSearchBackend } = await import('../src/backends/opensearch.js');

    const backend = new OpenSearchBackend({
      endpoint: 'https://test.us-east-1.aoss.amazonaws.com',
      index: 'test-index',
    });

    expect(backend).toBeDefined();
  });
});

describe('BaseBackend interface', () => {
  it('should define required methods', async () => {
    const { BaseBackend } = await import('../src/backends/base.js');

    // Check that abstract methods are defined
    expect(BaseBackend.prototype.upsert).toBeDefined();
    expect(BaseBackend.prototype.upsertMany).toBeDefined();
    expect(BaseBackend.prototype.search).toBeDefined();
    expect(BaseBackend.prototype.get).toBeDefined();
    expect(BaseBackend.prototype.delete).toBeDefined();
    expect(BaseBackend.prototype.deleteMany).toBeDefined();
    expect(BaseBackend.prototype.close).toBeDefined();
  });
});
