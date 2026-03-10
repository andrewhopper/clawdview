/**
 * OpenSearch Serverless backend.
 */
import {
  BaseBackend,
  VectorRecord,
  SearchResult,
  SearchOptions,
} from './base.js';

interface OpenSearchBackendOptions {
  endpoint: string;
  index: string;
  region?: string;
  dimension?: number;
}

export class OpenSearchBackend extends BaseBackend {
  private readonly endpoint: string;
  private readonly index: string;
  private readonly region: string;
  private readonly dimension: number;
  private client: unknown; // OpenSearch client

  constructor(options: OpenSearchBackendOptions) {
    super();
    this.endpoint = options.endpoint;
    this.index = options.index;
    this.region = options.region ?? 'us-east-1';
    this.dimension = options.dimension ?? 1024;

    this.initClient();
  }

  private async initClient(): Promise<void> {
    try {
      const { Client } = await import('@opensearch-project/opensearch');
      const { AwsSigv4Signer } = await import(
        '@opensearch-project/opensearch/aws'
      );
      const { defaultProvider } = await import('@aws-sdk/credential-provider-node');

      const host = this.endpoint.replace('https://', '').replace('http://', '');

      this.client = new Client({
        ...AwsSigv4Signer({
          region: this.region,
          service: 'aoss',
          getCredentials: () => {
            const provider = defaultProvider();
            return provider();
          },
        }),
        node: `https://${host}`,
      });

      await this.ensureIndex();
    } catch (error) {
      console.warn(
        'OpenSearch packages not installed. Install with: npm install @opensearch-project/opensearch'
      );
    }
  }

  private async ensureIndex(): Promise<void> {
    const client = this.client as import('@opensearch-project/opensearch').Client;

    const exists = await client.indices.exists({ index: this.index });
    if (!exists.body) {
      await client.indices.create({
        index: this.index,
        body: {
          settings: {
            index: {
              knn: true,
              'knn.algo_param.ef_search': 100,
            },
          },
          mappings: {
            properties: {
              id: { type: 'keyword' },
              text: { type: 'text' },
              embedding: {
                type: 'knn_vector',
                dimension: this.dimension,
                method: {
                  name: 'hnsw',
                  space_type: 'cosinesimil',
                  engine: 'nmslib',
                  parameters: {
                    ef_construction: 128,
                    m: 24,
                  },
                },
              },
              metadata: { type: 'object', enabled: true },
              created_at: { type: 'date' },
              updated_at: { type: 'date' },
            },
          },
        },
      });
    }
  }

  async upsert(record: VectorRecord): Promise<void> {
    await this.upsertMany([record]);
  }

  async upsertMany(records: VectorRecord[]): Promise<void> {
    const client = this.client as import('@opensearch-project/opensearch').Client;

    const body: unknown[] = [];
    for (const record of records) {
      body.push({ index: { _index: this.index, _id: record.id } });
      body.push({
        id: record.id,
        text: record.text,
        embedding: record.embedding,
        metadata: record.metadata,
        created_at: record.createdAt.toISOString(),
        updated_at: record.updatedAt.toISOString(),
      });
    }

    if (body.length > 0) {
      await client.bulk({ body, refresh: true });
    }
  }

  async search(
    embedding: number[],
    options: SearchOptions = {}
  ): Promise<SearchResult[]> {
    const client = this.client as import('@opensearch-project/opensearch').Client;
    const k = options.k ?? 10;

    // Build filter clause
    const filterClauses: unknown[] = [];
    if (options.filter) {
      for (const [key, value] of Object.entries(options.filter)) {
        filterClauses.push({ term: { [`metadata.${key}`]: value } });
      }
    }

    const query: Record<string, unknown> = {
      knn: {
        embedding: {
          vector: embedding,
          k,
        },
      },
    };

    // Wrap with bool if filters exist
    const body: Record<string, unknown> = {
      size: k,
      query: filterClauses.length > 0
        ? {
            bool: {
              must: [query],
              filter: filterClauses,
            },
          }
        : query,
    };

    const response = await client.search({
      index: this.index,
      body,
    });

    interface Hit {
      _id: string;
      _score: number;
      _source: {
        text?: string;
        metadata?: Record<string, unknown>;
      };
    }

    return (response.body.hits.hits as Hit[]).map((hit) => ({
      id: hit._id,
      score: hit._score,
      text: hit._source.text ?? '',
      metadata: hit._source.metadata ?? {},
    }));
  }

  async get(id: string): Promise<VectorRecord | null> {
    const client = this.client as import('@opensearch-project/opensearch').Client;

    try {
      const response = await client.get({ index: this.index, id });
      const source = response.body._source as Record<string, unknown>;

      return {
        id: response.body._id as string,
        text: (source.text as string) ?? '',
        embedding: (source.embedding as number[]) ?? [],
        metadata: (source.metadata as Record<string, unknown>) ?? {},
        createdAt: new Date((source.created_at as string) ?? new Date()),
        updatedAt: new Date((source.updated_at as string) ?? new Date()),
      };
    } catch {
      return null;
    }
  }

  async delete(id: string): Promise<boolean> {
    const client = this.client as import('@opensearch-project/opensearch').Client;

    try {
      await client.delete({ index: this.index, id, refresh: true });
      return true;
    } catch {
      return false;
    }
  }

  async deleteMany(ids: string[]): Promise<number> {
    let deleted = 0;
    for (const id of ids) {
      if (await this.delete(id)) {
        deleted++;
      }
    }
    return deleted;
  }

  async close(): Promise<void> {
    const client = this.client as import('@opensearch-project/opensearch').Client;
    await client.close();
  }
}
