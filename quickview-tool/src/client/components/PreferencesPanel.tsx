import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog';
import { Switch } from './ui/switch';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Separator } from './ui/separator';
import { ScrollArea } from './ui/scroll-area';
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
    <Dialog open={isOpen} onOpenChange={(open) => { if (!open) onClose(); }}>
      <DialogContent className="max-w-md max-h-[85vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>Preferences</DialogTitle>
          <DialogDescription>Configure QuickView behavior and watched file types.</DialogDescription>
        </DialogHeader>

        <ScrollArea className="flex-1 -mx-6 px-6">
          <div className="space-y-6 pb-4">
            {/* General */}
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">General</h4>

              <div className="flex items-center justify-between gap-3 py-2">
                <div className="flex flex-col gap-0.5 flex-1">
                  <span className="text-sm font-medium">Auto-reload on file change</span>
                  <span className="text-xs text-muted-foreground leading-snug">
                    Automatically reload the preview when the current file is modified externally
                  </span>
                </div>
                <Switch
                  checked={preferences.autoOpenOnChange}
                  onCheckedChange={(checked) => onUpdatePreference('autoOpenOnChange', checked)}
                />
              </div>

              <div className="py-2">
                <label className="text-sm font-medium block">Max open tabs</label>
                <span className="text-xs text-muted-foreground block mt-0.5 mb-2 leading-snug">
                  Maximum number of file tabs that can be open simultaneously
                </span>
                <Input
                  type="number"
                  min={1}
                  max={50}
                  value={preferences.maxOpenTabs}
                  onChange={(e) => {
                    const val = parseInt(e.target.value, 10);
                    if (val >= 1 && val <= 50) onUpdatePreference('maxOpenTabs', val);
                  }}
                  className="w-20 h-8 text-sm"
                />
              </div>
            </div>

            <Separator />

            {/* Watched File Types */}
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1">Watched File Types</h4>
              <p className="text-xs text-muted-foreground mb-3 leading-snug">
                Select which file types appear in the file tree and trigger change notifications
              </p>

              <div className="flex gap-3 mb-2.5">
                <Button
                  variant="link"
                  size="sm"
                  className="h-auto p-0 text-xs"
                  onClick={() => onUpdatePreference('watchedFileTypes', ALL_FILE_TYPES.map((ft) => ft.ext))}
                >
                  Select All
                </Button>
                <Button
                  variant="link"
                  size="sm"
                  className="h-auto p-0 text-xs"
                  onClick={() => onUpdatePreference('watchedFileTypes', [])}
                >
                  Select None
                </Button>
              </div>

              <div className="flex flex-col gap-0.5">
                {ALL_FILE_TYPES.map((ft) => (
                  <label
                    key={ft.ext}
                    className="flex items-center gap-2.5 px-2 py-1.5 rounded-md cursor-pointer transition-colors hover:bg-accent"
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
                      className="w-3.5 h-3.5 accent-primary shrink-0"
                    />
                    <span className="text-sm shrink-0">{ft.icon}</span>
                    <span className="text-sm flex-1">{ft.label}</span>
                    <span className="text-xs text-muted-foreground font-mono">{ft.ext}</span>
                  </label>
                ))}
              </div>
            </div>

            <Separator />

            {/* Reset */}
            <div className="flex justify-end">
              <Button variant="outline" size="sm" onClick={onReset}>
                Reset to Defaults
              </Button>
            </div>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
