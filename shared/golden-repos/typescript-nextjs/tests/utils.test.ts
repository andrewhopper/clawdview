import { describe, it, expect } from 'vitest';
import { formatDate, truncate, generateId } from '../src/lib/utils';

describe('formatDate', () => {
  it('should format date string', () => {
    const result = formatDate('2024-01-15T10:30:00Z');
    expect(result).toContain('Jan');
    expect(result).toContain('15');
    expect(result).toContain('2024');
  });
});

describe('truncate', () => {
  it('should truncate long text', () => {
    const result = truncate('This is a very long text', 10);
    expect(result).toBe('This is...');
  });

  it('should not truncate short text', () => {
    const result = truncate('Short', 10);
    expect(result).toBe('Short');
  });
});

describe('generateId', () => {
  it('should generate id of specified length', () => {
    const id = generateId(12);
    expect(id).toHaveLength(12);
  });

  it('should generate unique ids', () => {
    const ids = new Set(Array.from({ length: 100 }, () => generateId()));
    expect(ids.size).toBe(100);
  });
});
