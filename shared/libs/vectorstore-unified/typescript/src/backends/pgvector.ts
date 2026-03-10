/**
 * PostgreSQL pgvector backend.
 */
import {
  BaseBackend,
  VectorRecord,
  SearchResult,
  SearchOptions,
} from './base.js';

interface PgVectorBackendOptions {
  connectionString: string;
  collection?: string;
  dimension?: number;
  distanceMetric?: 'cosine' | 'euclidean' | 'inner_product';
}

export class PgVectorBackend extends BaseBackend {
  private readonly connectionString: string;
  private readonly collection: string;
  private readonly dimension: number;
  private readonly distanceMetric: string;
  private pool: unknown; // pg.Pool

  private readonly distanceOps: Record<string, string> = {
    cosine: '<=>',
    euclidean: '<->',
    inner_product: '<#>',
  };

  constructor(options: PgVectorBackendOptions) {
    super();
    this.connectionString = options.connectionString;
    this.collection = options.collection ?? 'vectors';
    this.dimension = options.dimension ?? 1024;
    this.distanceMetric = options.distanceMetric ?? 'cosine';

    this.initPool();
  }

  private async initPool(): Promise<void> {
    try {
      const pg = await import('pg');
      this.pool = new pg.default.Pool({
        connectionString: this.connectionString,
      });

      // Ensure table exists
      await this.ensureTable();
    } catch (error) {
      console.warn('pg package not installed. Install with: npm install pg pgvector');
    }
  }

  private async ensureTable(): Promise<void> {
    const pool = this.pool as import('pg').Pool;
    const client = await pool.connect();

    try {
      // Enable pgvector extension
      await client.query('CREATE EXTENSION IF NOT EXISTS vector');

      // Create table
      await client.query(`
        CREATE TABLE IF NOT EXISTS ${this.collection} (
          id TEXT PRIMARY KEY,
          text TEXT,
          embedding vector(${this.dimension}),
          metadata JSONB DEFAULT '{}',
          created_at TIMESTAMPTZ DEFAULT NOW(),
          updated_at TIMESTAMPTZ DEFAULT NOW()
        )
      `);

      // Create index
      const indexName = `${this.collection}_embedding_idx`;
      const opsClass =
        this.distanceMetric === 'cosine'
          ? 'vector_cosine_ops'
          : this.distanceMetric === 'euclidean'
            ? 'vector_l2_ops'
            : 'vector_ip_ops';

      await client.query(`
        CREATE INDEX IF NOT EXISTS ${indexName}
        ON ${this.collection}
        USING hnsw (embedding ${opsClass})
      `);
    } finally {
      client.release();
    }
  }

  async upsert(record: VectorRecord): Promise<void> {
    await this.upsertMany([record]);
  }

  async upsertMany(records: VectorRecord[]): Promise<void> {
    const pool = this.pool as import('pg').Pool;
    const client = await pool.connect();

    try {
      for (const record of records) {
        await client.query(
          `
          INSERT INTO ${this.collection} (id, text, embedding, metadata, created_at, updated_at)
          VALUES ($1, $2, $3, $4, $5, $6)
          ON CONFLICT (id) DO UPDATE SET
            text = EXCLUDED.text,
            embedding = EXCLUDED.embedding,
            metadata = EXCLUDED.metadata,
            updated_at = EXCLUDED.updated_at
        `,
          [
            record.id,
            record.text,
            `[${record.embedding.join(',')}]`,
            JSON.stringify(record.metadata),
            record.createdAt,
            record.updatedAt,
          ]
        );
      }
    } finally {
      client.release();
    }
  }

  async search(
    embedding: number[],
    options: SearchOptions = {}
  ): Promise<SearchResult[]> {
    const pool = this.pool as import('pg').Pool;
    const k = options.k ?? 10;
    const op = this.distanceOps[this.distanceMetric] ?? '<=>';

    // Build filter clause
    let filterClause = '';
    const filterParams: string[] = [];

    if (options.filter) {
      const conditions = Object.entries(options.filter).map(
        ([key, value], idx) => {
          filterParams.push(String(value));
          return `metadata->>'${key}' = $${idx + 2}`;
        }
      );
      filterClause = 'WHERE ' + conditions.join(' AND ');
    }

    const embeddingStr = `[${embedding.join(',')}]`;

    const result = await pool.query(
      `
      SELECT id, text, metadata, embedding ${op} $1 AS distance
      FROM ${this.collection}
      ${filterClause}
      ORDER BY distance
      LIMIT $${filterParams.length + 2}
    `,
      [embeddingStr, ...filterParams, k]
    );

    return result.rows.map((row: Record<string, unknown>) => {
      const distance = Number(row.distance);
      const score = this.distanceMetric === 'cosine' ? 1 - distance : distance;

      return {
        id: String(row.id),
        score,
        text: String(row.text),
        metadata: row.metadata as Record<string, unknown>,
      };
    });
  }

  async get(id: string): Promise<VectorRecord | null> {
    const pool = this.pool as import('pg').Pool;

    const result = await pool.query(
      `
      SELECT id, text, embedding, metadata, created_at, updated_at
      FROM ${this.collection}
      WHERE id = $1
    `,
      [id]
    );

    if (result.rows.length === 0) {
      return null;
    }

    const row = result.rows[0] as Record<string, unknown>;
    return {
      id: String(row.id),
      text: String(row.text),
      embedding: row.embedding as number[],
      metadata: row.metadata as Record<string, unknown>,
      createdAt: new Date(row.created_at as string),
      updatedAt: new Date(row.updated_at as string),
    };
  }

  async delete(id: string): Promise<boolean> {
    const pool = this.pool as import('pg').Pool;

    const result = await pool.query(
      `DELETE FROM ${this.collection} WHERE id = $1`,
      [id]
    );

    return (result.rowCount ?? 0) > 0;
  }

  async deleteMany(ids: string[]): Promise<number> {
    const pool = this.pool as import('pg').Pool;

    const result = await pool.query(
      `DELETE FROM ${this.collection} WHERE id = ANY($1)`,
      [ids]
    );

    return result.rowCount ?? 0;
  }

  async close(): Promise<void> {
    const pool = this.pool as import('pg').Pool;
    await pool.end();
  }
}
