// File UUID: e2f3a4b5-8c7d-4e9f-9f4a-6b9c1d2e3f5a

import { homedir } from 'os';
import { join } from 'path';

/**
 * Resolve the global database path (~/.hopper-status.db)
 */
export function getDbPath(): string {
  return join(homedir(), '.hopper-status.db');
}
