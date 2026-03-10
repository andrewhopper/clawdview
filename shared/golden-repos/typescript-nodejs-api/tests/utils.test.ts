/**
 * Tests for utility functions.
 */

import { describe, it, expect, vi } from 'vitest';
import { sleep, retry, ok, err, chunk, generateId } from '../src/utils.js';

describe('sleep', () => {
  it('should wait for specified time', async () => {
    const start = Date.now();
    await sleep(50);
    const elapsed = Date.now() - start;
    expect(elapsed).toBeGreaterThanOrEqual(45);
  });
});

describe('retry', () => {
  it('should return result on success', async () => {
    const fn = vi.fn().mockResolvedValue('success');
    const result = await retry(fn);
    expect(result).toBe('success');
    expect(fn).toHaveBeenCalledTimes(1);
  });

  it('should retry on failure', async () => {
    const fn = vi
      .fn()
      .mockRejectedValueOnce(new Error('fail'))
      .mockResolvedValue('success');

    const result = await retry(fn, { initialDelay: 10 });
    expect(result).toBe('success');
    expect(fn).toHaveBeenCalledTimes(2);
  });

  it('should throw after max attempts', async () => {
    const fn = vi.fn().mockRejectedValue(new Error('always fails'));

    await expect(
      retry(fn, { maxAttempts: 2, initialDelay: 10 })
    ).rejects.toThrow('always fails');
    expect(fn).toHaveBeenCalledTimes(2);
  });
});

describe('Result helpers', () => {
  it('should create ok result', () => {
    const result = ok('data');
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data).toBe('data');
    }
  });

  it('should create err result', () => {
    const result = err(new Error('failed'));
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.message).toBe('failed');
    }
  });
});

describe('chunk', () => {
  it('should split array into chunks', () => {
    expect(chunk([1, 2, 3, 4, 5], 2)).toEqual([[1, 2], [3, 4], [5]]);
  });

  it('should handle empty array', () => {
    expect(chunk([], 2)).toEqual([]);
  });

  it('should handle array smaller than chunk size', () => {
    expect(chunk([1, 2], 5)).toEqual([[1, 2]]);
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
