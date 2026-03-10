/**
 * Tests for embedding providers.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock AWS SDK
vi.mock('@aws-sdk/client-bedrock-runtime', () => ({
  BedrockRuntimeClient: vi.fn().mockImplementation(() => ({
    send: vi.fn().mockResolvedValue({
      body: new TextEncoder().encode(JSON.stringify({ embedding: Array(1024).fill(0.1) })),
    }),
  })),
  InvokeModelCommand: vi.fn(),
}));

describe('BedrockEmbeddings', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should have correct dimension for Titan v2', async () => {
    const { BedrockEmbeddings } = await import('../src/embeddings/bedrock.js');

    const embeddings = new BedrockEmbeddings({
      modelId: 'amazon.titan-embed-text-v2:0',
    });

    expect(embeddings.dimension).toBe(1024);
  });

  it('should have correct dimension for Titan v1', async () => {
    const { BedrockEmbeddings } = await import('../src/embeddings/bedrock.js');

    const embeddings = new BedrockEmbeddings({
      modelId: 'amazon.titan-embed-text-v1',
    });

    expect(embeddings.dimension).toBe(1536);
  });

  it('should embed text and return array', async () => {
    const { BedrockEmbeddings } = await import('../src/embeddings/bedrock.js');

    const embeddings = new BedrockEmbeddings();
    const result = await embeddings.embedText('Hello world');

    expect(Array.isArray(result)).toBe(true);
    expect(result.length).toBe(1024);
  });

  it('should embed multiple texts', async () => {
    const { BedrockEmbeddings } = await import('../src/embeddings/bedrock.js');

    const embeddings = new BedrockEmbeddings();
    const results = await embeddings.embedTexts(['Hello', 'World', 'Test']);

    expect(results.length).toBe(3);
    expect(results.every((r) => r.length === 1024)).toBe(true);
  });
});

describe('OpenAIEmbeddings', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env.OPENAI_API_KEY = 'test-key';
  });

  it('should have correct dimension for text-embedding-3-small', async () => {
    const { OpenAIEmbeddings } = await import('../src/embeddings/openai.js');

    const embeddings = new OpenAIEmbeddings({
      model: 'text-embedding-3-small',
      apiKey: 'test-key',
    });

    expect(embeddings.dimension).toBe(1536);
  });

  it('should have correct dimension for text-embedding-3-large', async () => {
    const { OpenAIEmbeddings } = await import('../src/embeddings/openai.js');

    const embeddings = new OpenAIEmbeddings({
      model: 'text-embedding-3-large',
      apiKey: 'test-key',
    });

    expect(embeddings.dimension).toBe(3072);
  });

  it('should throw error if API key is missing', async () => {
    delete process.env.OPENAI_API_KEY;

    const { OpenAIEmbeddings } = await import('../src/embeddings/openai.js');

    expect(() => new OpenAIEmbeddings({ apiKey: '' })).toThrow('API key required');
  });
});

describe('CohereEmbeddings', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env.COHERE_API_KEY = 'test-key';
  });

  it('should have correct dimension for embed-english-v3.0', async () => {
    const { CohereEmbeddings } = await import('../src/embeddings/cohere.js');

    const embeddings = new CohereEmbeddings({
      model: 'embed-english-v3.0',
      apiKey: 'test-key',
    });

    expect(embeddings.dimension).toBe(1024);
  });

  it('should have correct dimension for light model', async () => {
    const { CohereEmbeddings } = await import('../src/embeddings/cohere.js');

    const embeddings = new CohereEmbeddings({
      model: 'embed-english-light-v3.0',
      apiKey: 'test-key',
    });

    expect(embeddings.dimension).toBe(384);
  });

  it('should throw error if API key is missing', async () => {
    delete process.env.COHERE_API_KEY;

    const { CohereEmbeddings } = await import('../src/embeddings/cohere.js');

    expect(() => new CohereEmbeddings({ apiKey: '' })).toThrow('API key required');
  });
});
