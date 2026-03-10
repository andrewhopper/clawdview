// File UUID: 2366fd04-0066-4702-a235-4103b0129e06
// File UUID: g4h5i6j7-1k2l-4m8n-9o3p-6q7r8s9t1u2v

import Database from 'better-sqlite3';
import { ulid } from 'ulid';
import type { StatusEvent, StatusEventType } from '../domain/types.js';
import { getDbPath } from '../utils/db-path.js';

/**
 * Event store for status tracking
 * - Append-only SQLite storage
 * - WAL mode for concurrent writes
 * - Prepared statements for performance
 */
export class EventStore {
  private db: Database.Database;

  constructor(dbPath?: string) {
    const path = dbPath || getDbPath();
    this.db = new Database(path);
    this.db.pragma('journal_mode = WAL');
    this.initialize();
  }

  /**
   * Initialize database schema
   */
  private initialize(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        type TEXT NOT NULL,
        project_id TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        payload TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
      );

      CREATE INDEX IF NOT EXISTS idx_events_project_id ON events(project_id);
      CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
      CREATE INDEX IF NOT EXISTS idx_events_entity_id ON events(entity_id);
      CREATE INDEX IF NOT EXISTS idx_events_type ON events(type);
    `);
  }

  /**
   * Append a new event to the store
   */
  append(
    type: StatusEventType,
    projectId: string,
    entityId: string,
    payload: Record<string, unknown>
  ): StatusEvent {
    const event: StatusEvent = {
      id: ulid(),
      timestamp: new Date().toISOString(),
      type,
      projectId,
      entityId,
      payload,
    };

    const stmt = this.db.prepare(`
      INSERT INTO events (id, timestamp, type, project_id, entity_id, payload)
      VALUES (?, ?, ?, ?, ?, ?)
    `);

    stmt.run(
      event.id,
      event.timestamp,
      event.type,
      event.projectId,
      event.entityId,
      JSON.stringify(event.payload)
    );

    return event;
  }

  /**
   * Get all events for a project (optionally up to a specific time)
   */
  getEvents(projectId?: string, asOf?: Date): StatusEvent[] {
    let query = 'SELECT * FROM events';
    const params: unknown[] = [];

    if (projectId) {
      query += ' WHERE project_id = ?';
      params.push(projectId);

      if (asOf) {
        query += ' AND timestamp <= ?';
        params.push(asOf.toISOString());
      }
    } else if (asOf) {
      query += ' WHERE timestamp <= ?';
      params.push(asOf.toISOString());
    }

    query += ' ORDER BY timestamp ASC';

    const stmt = this.db.prepare(query);
    const rows = stmt.all(...params) as Array<{
      id: string;
      timestamp: string;
      type: StatusEventType;
      project_id: string;
      entity_id: string;
      payload: string;
      created_at: string;
    }>;

    return rows.map((row) => ({
      id: row.id,
      timestamp: row.timestamp,
      type: row.type,
      projectId: row.project_id,
      entityId: row.entity_id,
      payload: JSON.parse(row.payload),
      createdAt: row.created_at,
    }));
  }

  /**
   * Get events for a specific entity
   */
  getEventsForEntity(entityId: string): StatusEvent[] {
    const stmt = this.db.prepare(`
      SELECT * FROM events
      WHERE entity_id = ?
      ORDER BY timestamp ASC
    `);

    const rows = stmt.all(entityId) as Array<{
      id: string;
      timestamp: string;
      type: StatusEventType;
      project_id: string;
      entity_id: string;
      payload: string;
      created_at: string;
    }>;

    return rows.map((row) => ({
      id: row.id,
      timestamp: row.timestamp,
      type: row.type,
      projectId: row.project_id,
      entityId: row.entity_id,
      payload: JSON.parse(row.payload),
      createdAt: row.created_at,
    }));
  }

  /**
   * Get recent events for activity feed
   */
  getRecentEvents(projectId?: string, limit = 50): StatusEvent[] {
    let query = 'SELECT * FROM events';
    const params: unknown[] = [];

    if (projectId) {
      query += ' WHERE project_id = ?';
      params.push(projectId);
    }

    query += ' ORDER BY timestamp DESC LIMIT ?';
    params.push(limit);

    const stmt = this.db.prepare(query);
    const rows = stmt.all(...params) as Array<{
      id: string;
      timestamp: string;
      type: StatusEventType;
      project_id: string;
      entity_id: string;
      payload: string;
      created_at: string;
    }>;

    return rows.map((row) => ({
      id: row.id,
      timestamp: row.timestamp,
      type: row.type,
      projectId: row.project_id,
      entityId: row.entity_id,
      payload: JSON.parse(row.payload),
      createdAt: row.created_at,
    }));
  }

  /**
   * Close the database connection
   */
  close(): void {
    this.db.close();
  }
}
