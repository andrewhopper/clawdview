import { X } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Preferences } from '../types';
import { ALL_FILE_TYPES } from '../hooks/usePreferences';

interface PreferencesPanelProps {
  isOpen: boolean;
  preferences: Preferences;
  onClose: () => void;
  onUpdatePreference: <K extends keyof Preferences>(key: K, value: Preferences[K]) => void;
  onReset: () => void;
}

export function PreferencesPanel({
  isOpen, preferences, onClose, onUpdatePreference, onReset,
}: PreferencesPanelProps) {
  return (
    <>
      {/* Overlay */}
      <div
        className={cn(
          'fixed inset-0 bg-black/50 z-90 transition-opacity',
          isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none',
        )}
        onClick={onClose}
      />

      {/* Panel */}
      <div
        className={cn(
          'fixed top-0 right-0 bottom-0 w-[380px] max-w-full bg-card border-l border-border z-100 flex flex-col transition-transform shadow-[-4px_0_24px_rgba(0,0,0,0.3)]',
          isOpen ? 'translate-x-0' : 'translate-x-full',
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-border shrink-0">
          <h2 className="text-[15px] font-semibold text-foreground">Preferences</h2>
          <button
            onClick={onClose}
            className="text-muted-foreground hover:text-foreground hover:bg-accent p-1 rounded-md transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto py-2">
          {/* General */}
          <div className="px-5 py-3 border-b border-border">
            <h4 className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground mb-3">General</h4>

            <label className="flex items-start justify-between gap-3 cursor-pointer py-2">
              <div className="flex flex-col gap-0.5 flex-1">
                <span className="text-[13px] font-medium text-foreground">Auto-reload on file change</span>
                <span className="text-xs text-muted-foreground leading-snug">
                  Automatically reload the preview when the current file is modified externally
                </span>
              </div>
              <input
                type="checkbox"
                checked={preferences.autoOpenOnChange}
                onChange={(e) => onUpdatePreference('autoOpenOnChange', e.target.checked)}
                className="sr-only peer"
              />
              <div className="relative w-9 h-5 bg-muted rounded-full peer-checked:bg-green-500 shrink-0 mt-0.5 transition-colors after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:w-4 after:h-4 after:bg-foreground after:rounded-full after:transition-transform peer-checked:after:translate-x-4" />
            </label>

            <div className="py-2">
              <label className="text-[13px] font-medium text-foreground block">Max open tabs</label>
              <span className="text-xs text-muted-foreground block mt-0.5 mb-2 leading-snug">
                Maximum number of file tabs that can be open simultaneously
              </span>
              <input
                type="number"
                min={1}
                max={50}
                value={preferences.maxOpenTabs}
                onChange={(e) => {
                  const val = parseInt(e.target.value, 10);
                  if (val >= 1 && val <= 50) onUpdatePreference('maxOpenTabs', val);
                }}
                className="w-18 px-2 py-1 text-[13px] bg-background text-foreground border border-border rounded-md outline-none transition-colors focus:border-ring"
              />
            </div>
          </div>

          {/* Watched File Types */}
          <div className="px-5 py-3 border-b border-border">
            <h4 className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground mb-1">Watched File Types</h4>
            <p className="text-xs text-muted-foreground mb-3 leading-snug">
              Select which file types appear in the file tree and trigger change notifications
            </p>

            <div className="flex gap-3 mb-2.5">
              <button
                onClick={() => onUpdatePreference('watchedFileTypes', ALL_FILE_TYPES.map((ft) => ft.ext))}
                className="text-xs text-blue-400 underline underline-offset-2 hover:text-blue-300 bg-transparent border-none cursor-pointer"
              >
                Select All
              </button>
              <button
                onClick={() => onUpdatePreference('watchedFileTypes', [])}
                className="text-xs text-blue-400 underline underline-offset-2 hover:text-blue-300 bg-transparent border-none cursor-pointer"
              >
                Select None
              </button>
            </div>

            <div className="flex flex-col gap-0.5">
              {ALL_FILE_TYPES.map((ft) => (
                <label
                  key={ft.ext}
                  className="flex items-center gap-2 px-2 py-1 rounded-md cursor-pointer transition-colors hover:bg-accent"
                >
                  <input
                    type="checkbox"
                    checked={preferences.watchedFileTypes.includes(ft.ext)}
                    onChange={() => {
                      const current = preferences.watchedFileTypes;
                      const next = current.includes(ft.ext)
                        ? current.filter((e) => e !== ft.ext)
                        : [...current, ft.ext];
                      onUpdatePreference('watchedFileTypes', next);
                    }}
                    className="w-3.5 h-3.5 accent-green-500 shrink-0"
                  />
                  <span className="text-sm shrink-0">{ft.icon}</span>
                  <span className="text-[13px] text-foreground flex-1">{ft.label}</span>
                  <span className="text-xs text-muted-foreground font-mono">{ft.ext}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Reset */}
          <div className="px-5 py-3 flex justify-end">
            <button
              onClick={onReset}
              className="bg-secondary text-muted-foreground border border-border px-3.5 py-1.5 rounded-md cursor-pointer text-xs transition-colors hover:bg-accent hover:text-foreground"
            >
              Reset to Defaults
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
