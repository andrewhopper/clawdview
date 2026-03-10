import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useToggle } from '../src/hooks/useToggle';
import { useDebounce } from '../src/hooks/useDebounce';

describe('useToggle', () => {
  it('returns initial value', () => {
    const { result } = renderHook(() => useToggle(false));
    expect(result.current[0]).toBe(false);
  });

  it('toggles value', () => {
    const { result } = renderHook(() => useToggle(false));
    act(() => result.current[1]());
    expect(result.current[0]).toBe(true);
  });

  it('sets specific value', () => {
    const { result } = renderHook(() => useToggle(false));
    act(() => result.current[2](true));
    expect(result.current[0]).toBe(true);
  });
});

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('test', 500));
    expect(result.current).toBe('test');
  });

  it('debounces value changes', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: 'initial' } }
    );

    rerender({ value: 'updated' });
    expect(result.current).toBe('initial');

    act(() => {
      vi.advanceTimersByTime(500);
    });
    expect(result.current).toBe('updated');
  });
});
