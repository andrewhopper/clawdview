/**
 * AWS Bedrock embeddings provider.
 */
import {
  BedrockRuntimeClient,
  InvokeModelCommand,
} from '@aws-sdk/client-bedrock-runtime';
import { BaseEmbeddings } from './base.js';

interface BedrockEmbeddingsOptions {
  modelId?: string;
  region?: string;
  profile?: string;
}

const MODEL_DIMENSIONS: Record<string, number> = {
  'amazon.titan-embed-text-v2:0': 1024,
  'amazon.titan-embed-text-v1': 1536,
  'cohere.embed-english-v3': 1024,
  'cohere.embed-multilingual-v3': 1024,
};

export class BedrockEmbeddings extends BaseEmbeddings {
  readonly dimension: number;
  private readonly client: BedrockRuntimeClient;
  private readonly modelId: string;

  constructor(options: BedrockEmbeddingsOptions = {}) {
    super();
    this.modelId = options.modelId ?? 'amazon.titan-embed-text-v2:0';
    this.dimension = MODEL_DIMENSIONS[this.modelId] ?? 1024;

    this.client = new BedrockRuntimeClient({
      region: options.region ?? 'us-east-1',
    });
  }

  async embedText(text: string): Promise<number[]> {
    if (this.modelId.startsWith('amazon.titan')) {
      return this.embedTitan(text);
    } else if (this.modelId.startsWith('cohere')) {
      const embeddings = await this.embedCohere([text], 'search_document');
      return embeddings[0];
    }
    throw new Error(`Unsupported model: ${this.modelId}`);
  }

  async embedTexts(texts: string[]): Promise<number[][]> {
    if (this.modelId.startsWith('amazon.titan')) {
      // Titan doesn't support batch, embed one by one
      return Promise.all(texts.map((text) => this.embedTitan(text)));
    } else if (this.modelId.startsWith('cohere')) {
      return this.embedCohere(texts, 'search_document');
    }
    throw new Error(`Unsupported model: ${this.modelId}`);
  }

  async embedQuery(query: string): Promise<number[]> {
    if (this.modelId.startsWith('cohere')) {
      const embeddings = await this.embedCohere([query], 'search_query');
      return embeddings[0];
    }
    return this.embedText(query);
  }

  private async embedTitan(text: string): Promise<number[]> {
    const command = new InvokeModelCommand({
      modelId: this.modelId,
      body: JSON.stringify({ inputText: text }),
      accept: 'application/json',
      contentType: 'application/json',
    });

    const response = await this.client.send(command);
    const result = JSON.parse(new TextDecoder().decode(response.body));
    return result.embedding;
  }

  private async embedCohere(
    texts: string[],
    inputType: string
  ): Promise<number[][]> {
    const command = new InvokeModelCommand({
      modelId: this.modelId,
      body: JSON.stringify({
        texts,
        input_type: inputType,
        truncate: 'END',
      }),
      accept: 'application/json',
      contentType: 'application/json',
    });

    const response = await this.client.send(command);
    const result = JSON.parse(new TextDecoder().decode(response.body));
    return result.embeddings;
  }
}
