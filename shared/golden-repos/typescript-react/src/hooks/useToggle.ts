import { useCallback, useState } from 'react';

/**
 * Hook for boolean toggle state.
 *
 * @example
 * ```tsx
 * const [isOpen, toggle, setIsOpen] = useToggle(false);
 * ```
 */
export function useToggle(
  initialValue = false
): [boolean, () => void, (value: boolean) => void] {
  const [value, setValue] = useState(initialValue);
  const toggle = useCallback(() => setValue((v) => !v), []);
  return [value, toggle, setValue];
}
