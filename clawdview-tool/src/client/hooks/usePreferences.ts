import { useState, useCallback } from 'react';
import type { Preferences } from '../types';
import FILE_TYPES, { DEFAULT_WATCHED_FILE_TYPES } from '../../shared/file-types';

const STORAGE_KEY = 'clawdview-preferences';

const DEFAULT_PREFERENCES: Preferences = {
  autoOpenOnChange: true,
  maxOpenTabs: 10,
  watchedFileTypes: DEFAULT_WATCHED_FILE_TYPES,
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

export const ALL_FILE_TYPES = FILE_TYPES;
