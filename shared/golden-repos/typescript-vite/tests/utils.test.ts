import { describe, it, expect, vi } from 'vitest';
import {
  Ok,
  Err,
  sleep,
  debounce,
  generateId,
  pick,
  omit,
  deepClone,
} from '../src/utils';

describe('Result helpers', () => {
  it('creates Ok result', () => {
    const result = Ok('success');
    expect(result.ok).toBe(true);
    if (result.ok) expect(result.value).toBe('success');
  });

  it('creates Err result', () => {
    const result = Err(new Error('failed'));
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.error.message).toBe('failed');
  });
});

describe('sleep', () => {
  it('resolves after delay', async () => {
    const start = Date.now();
    await sleep(50);
    expect(Date.now() - start).toBeGreaterThanOrEqual(45);
  });
});

describe('debounce', () => {
  it('debounces function calls', async () => {
    vi.useFakeTimers();
    const fn = vi.fn();
    const debounced = debounce(fn, 100);

    debounced();
    debounced();
    debounced();

    expect(fn).not.toHaveBeenCalled();
    vi.advanceTimersByTime(100);
    expect(fn).toHaveBeenCalledTimes(1);

    vi.useRealTimers();
  });
});

describe('generateId', () => {
  it('generates id of specified length', () => {
    expect(generateId(12)).toHaveLength(12);
  });

  it('generates unique ids', () => {
    const ids = new Set(Array.from({ length: 100 }, () => generateId()));
    expect(ids.size).toBe(100);
  });
});

describe('pick', () => {
  it('picks specified keys', () => {
    const obj = { a: 1, b: 2, c: 3 };
    expect(pick(obj, ['a', 'c'])).toEqual({ a: 1, c: 3 });
  });
});

describe('omit', () => {
  it('omits specified keys', () => {
    const obj = { a: 1, b: 2, c: 3 };
    expect(omit(obj, ['b'])).toEqual({ a: 1, c: 3 });
  });
});

describe('deepClone', () => {
  it('creates a deep copy', () => {
    const obj = { a: { b: 1 } };
    const clone = deepClone(obj);
    clone.a.b = 2;
    expect(obj.a.b).toBe(1);
  });
});
