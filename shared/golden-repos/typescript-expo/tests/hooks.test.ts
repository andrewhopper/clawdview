import { renderHook, act } from '@testing-library/react-native';
import { useToggle } from '@/hooks/useToggle';
import { useDebounce } from '@/hooks/useDebounce';

describe('useToggle', () => {
  it('initializes with false by default', () => {
    const { result } = renderHook(() => useToggle());
    expect(result.current[0]).toBe(false);
  });

  it('initializes with provided value', () => {
    const { result } = renderHook(() => useToggle(true));
    expect(result.current[0]).toBe(true);
  });

  it('toggles value when toggle is called', () => {
    const { result } = renderHook(() => useToggle());

    act(() => {
      result.current[1](); // toggle
    });

    expect(result.current[0]).toBe(true);

    act(() => {
      result.current[1](); // toggle again
    });

    expect(result.current[0]).toBe(false);
  });

  it('sets specific value with setValue', () => {
    const { result } = renderHook(() => useToggle());

    act(() => {
      result.current[2](true); // setValue
    });

    expect(result.current[0]).toBe(true);
  });
});

describe('useDebounce', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
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

    expect(result.current).toBe('initial');

    rerender({ value: 'updated' });
    expect(result.current).toBe('initial');

    act(() => {
      jest.advanceTimersByTime(499);
    });
    expect(result.current).toBe('initial');

    act(() => {
      jest.advanceTimersByTime(1);
    });
    expect(result.current).toBe('updated');
  });
});
