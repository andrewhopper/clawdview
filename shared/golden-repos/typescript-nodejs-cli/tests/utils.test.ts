import { describe, it, expect } from 'vitest';
import { generateId, formatBytes } from '../src/utils.js';

describe('generateId', () => {
  it('generates ID of default length', () => {
    const id = generateId();
    expect(id).toHaveLength(8);
  });

  it('generates ID of specified length', () => {
    const id = generateId(16);
    expect(id).toHaveLength(16);
  });

  it('generates unique IDs', () => {
    const ids = new Set(Array.from({ length: 100 }, () => generateId()));
    expect(ids.size).toBe(100);
  });
});

describe('formatBytes', () => {
  it('formats bytes', () => {
    expect(formatBytes(500)).toBe('500.0 B');
  });

  it('formats kilobytes', () => {
    expect(formatBytes(1024)).toBe('1.0 KB');
  });

  it('formats megabytes', () => {
    expect(formatBytes(1024 * 1024)).toBe('1.0 MB');
  });

  it('formats gigabytes', () => {
    expect(formatBytes(1024 * 1024 * 1024)).toBe('1.0 GB');
  });
});
