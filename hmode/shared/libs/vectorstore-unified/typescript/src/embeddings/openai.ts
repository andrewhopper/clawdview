/**
 * OpenAI embeddings provider.
 */
import { BaseEmbeddings } from './base.js';

interface OpenAIEmbeddingsOptions {
  model?: string;
  apiKey?: string;
}

const MODEL_DIMENSIONS: Record<string, number> = {
  'text-embedding-3-small': 1536,
  'text-embedding-3-large': 3072,
  'text-embedding-ada-002': 1536,
};

export class OpenAIEmbeddings extends BaseEmbeddings {
  readonly dimension: number;
  private readonly model: string;
  private readonly apiKey: string;

  constructor(options: OpenAIEmbeddingsOptions = {}) {
    super();
    this.model = options.model ?? 'text-embedding-3-small';
    this.dimension = MODEL_DIMENSIONS[this.model] ?? 1536;
    this.apiKey = options.apiKey ?? process.env.OPENAI_API_KEY ?? '';

    if (!this.apiKey) {
      throw new Error('OpenAI API key required');
    }
  }

  async embedText(text: string): Promise<number[]> {
    const embeddings = await this.embedTexts([text]);
    return embeddings[0];
  }

  async embedTexts(texts: string[]): Promise<number[][]> {
    // Dynamic import to avoid requiring openai package unless used
    const { default: OpenAI } = await import('openai');
    const client = new OpenAI({ apiKey: this.apiKey });

    const response = await client.embeddings.create({
      model: this.model,
      input: texts,
    });

    return response.data.map((item) => item.embedding);
  }
}
