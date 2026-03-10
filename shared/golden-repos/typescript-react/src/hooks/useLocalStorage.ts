import { useState, useCallback, useEffect } from 'react';

/**
 * Hook for persisting state to localStorage.
 *
 * @example
 * ```tsx
 * const [theme, setTheme] = useLocalStorage('theme', 'light');
 * ```
 */
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue;

    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStoredValue((prev) => {
        const nextValue = value instanceof Function ? value(prev) : value;
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(key, JSON.stringify(nextValue));
        }
        return nextValue;
      });
    },
    [key]
  );

  const removeValue = useCallback(() => {
    setStoredValue(initialValue);
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(key);
    }
  }, [key, initialValue]);

  return [storedValue, setValue, removeValue];
}
