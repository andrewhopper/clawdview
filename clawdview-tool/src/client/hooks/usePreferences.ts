import { useState, useCallback } from 'react';
import type { Preferences } from '../types';

const STORAGE_KEY = 'clawdview-preferences';

const DEFAULT_PREFERENCES: Preferences = {
  autoOpenOnChange: true,
  maxOpenTabs: 10,
  watchedFileTypes: [
    '.html', '.jsx', '.js', '.py', '.css', '.json',
    '.md', '.svg', '.txt', '.xml', '.yaml', '.yml',
  ],
};

function loadPreferences(): Preferences {
  try {
    const stored = localStorage.getItem(STORAGE_KEY) || localStorage.getItem('quickview-preferences');
    if (stored) {
      // Migrate from old key if needed
      if (!localStorage.getItem(STORAGE_KEY) && localStorage.getItem('quickview-preferences')) {
        localStorage.setItem(STORAGE_KEY, stored);
        localStorage.removeItem('quickview-preferences');
      }
      return { ...DEFAULT_PREFERENCES, ...JSON.parse(stored) };
    }
  } catch (e) {
    console.error('Failed to load preferences:', e);
  }
  return { ...DEFAULT_PREFERENCES };
}

function savePreferences(prefs: Preferences): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
  } catch (e) {
    console.error('Failed to save preferences:', e);
  }
}

export function usePreferences() {
  const [preferences, setPreferences] = useState<Preferences>(loadPreferences);

  const updatePreference = useCallback(<K extends keyof Preferences>(key: K, value: Preferences[K]) => {
    setPreferences((prev) => {
      const next = { ...prev, [key]: value };
      savePreferences(next);
      return next;
    });
  }, []);

  const resetPreferences = useCallback(() => {
    const defaults = { ...DEFAULT_PREFERENCES };
    setPreferences(defaults);
    savePreferences(defaults);
  }, []);

  const isFileTypeWatched = useCallback(
    (ext: string) => preferences.watchedFileTypes.includes(ext),
    [preferences.watchedFileTypes],
  );

  return { preferences, updatePreference, resetPreferences, isFileTypeWatched };
}

export const ALL_FILE_TYPES = [
  { ext: '.html', label: 'HTML', icon: '🌐' },
  { ext: '.jsx', label: 'React JSX', icon: '⚛️' },
  { ext: '.js', label: 'JavaScript', icon: '📜' },
  { ext: '.py', label: 'Python', icon: '🐍' },
  { ext: '.css', label: 'CSS', icon: '🎨' },
  { ext: '.json', label: 'JSON', icon: '📊' },
  { ext: '.md', label: 'Markdown', icon: '📝' },
  { ext: '.svg', label: 'SVG', icon: '🎨' },
  { ext: '.txt', label: 'Text', icon: '📄' },
  { ext: '.xml', label: 'XML', icon: '📄' },
  { ext: '.yaml', label: 'YAML', icon: '📄' },
  { ext: '.yml', label: 'YAML', icon: '📄' },
];
