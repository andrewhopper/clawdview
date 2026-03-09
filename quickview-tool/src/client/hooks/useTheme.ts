import { useState, useCallback, useEffect } from 'react';

export function useTheme() {
  const [isDark, setIsDark] = useState(() =>
    document.documentElement.classList.contains('dark'),
  );

  const toggleTheme = useCallback(() => {
    setIsDark((prev) => {
      const next = !prev;
      if (next) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      localStorage.setItem('quickview-theme', next ? 'dark' : 'light');
      return next;
    });
  }, []);

  useEffect(() => {
    const hljsLight = document.getElementById('hljs-light') as HTMLLinkElement | null;
    const hljsDark = document.getElementById('hljs-dark') as HTMLLinkElement | null;
    if (hljsLight) hljsLight.disabled = isDark;
    if (hljsDark) hljsDark.disabled = !isDark;
  }, [isDark]);

  return { isDark, toggleTheme };
}
