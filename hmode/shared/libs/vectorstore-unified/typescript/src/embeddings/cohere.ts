/**
 * Cohere embeddings provider (direct API).
 */
import { BaseEmbeddings } from './base.js';

interface CohereEmbeddingsOptions {
  model?: string;
  apiKey?: string;
}

const MODEL_DIMENSIONS: Record<string, number> = {
  'embed-english-v3.0': 1024,
  'embed-multilingual-v3.0': 1024,
  'embed-english-light-v3.0': 384,
};

export class CohereEmbeddings extends BaseEmbeddings {
  readonly dimension: number;
  private readonly model: string;
  private readonly apiKey: string;

  constructor(options: CohereEmbeddingsOptions = {}) {
    super();
    this.model = options.model ?? 'embed-english-v3.0';
    this.dimension = MODEL_DIMENSIONS[this.model] ?? 1024;
    this.apiKey = options.apiKey ?? process.env.COHERE_API_KEY ?? '';

    if (!this.apiKey) {
      throw new Error('Cohere API key required');
    }
  }

  async embedText(text: string): Promise<number[]> {
    const embeddings = await this.callCohere([text], 'search_document');
    return embeddings[0];
  }

  async embedTexts(texts: string[]): Promise<number[][]> {
    return this.callCohere(texts, 'search_document');
  }

  async embedQuery(query: string): Promise<number[]> {
    const embeddings = await this.callCohere([query], 'search_query');
    return embeddings[0];
  }

  private async callCohere(
    texts: string[],
    inputType: string
  ): Promise<number[][]> {
    const response = await fetch('https://api.cohere.ai/v1/embed', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        texts,
        model: this.model,
        input_type: inputType,
      }),
    });

    if (!response.ok) {
      throw new Error(`Cohere API error: ${response.statusText}`);
    }

    const result = await response.json();
    return result.embeddings;
  }
}
