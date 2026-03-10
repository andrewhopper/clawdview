/**
 * Base backend interface and data types.
 */

export interface VectorRecord {
  id: string;
  text: string;
  embedding: number[];
  metadata: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
}

export interface SearchResult {
  id: string;
  score: number;
  text: string;
  metadata: Record<string, unknown>;
}

export interface SearchOptions {
  k?: number;
  filter?: Record<string, unknown>;
}

export abstract class BaseBackend {
  /** Insert or update a single record. */
  abstract upsert(record: VectorRecord): Promise<void>;

  /** Insert or update multiple records. */
  abstract upsertMany(records: VectorRecord[]): Promise<void>;

  /** Search by embedding vector. */
  abstract search(
    embedding: number[],
    options?: SearchOptions
  ): Promise<SearchResult[]>;

  /** Get a record by ID. */
  abstract get(id: string): Promise<VectorRecord | null>;

  /** Delete a record by ID. Returns true if deleted. */
  abstract delete(id: string): Promise<boolean>;

  /** Delete multiple records. Returns count deleted. */
  abstract deleteMany(ids: string[]): Promise<number>;

  /** Close any connections. Override if needed. */
  async close(): Promise<void> {
    // Default no-op
  }
}
