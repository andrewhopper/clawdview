import { Settings, Sun, Moon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface HeaderProps {
  currentFileName: string;
  connected: boolean;
  isDark: boolean;
  onToggleTheme: () => void;
  onOpenSettings: () => void;
}

export function Header({
  currentFileName,
  connected,
  isDark,
  onToggleTheme,
  onOpenSettings,
}: HeaderProps) {
  return (
    <header className="bg-card border-b border-border px-5 h-12 flex justify-between items-center shrink-0">
      <h1 className="text-base font-semibold tracking-tight">QuickView</h1>
      <div className="flex items-center gap-2.5 text-sm text-muted-foreground">
        <span
          className={cn(
            'text-base leading-none',
            connected ? 'text-green-500' : 'text-red-500',
          )}
        >
          ●
        </span>
        <span>{currentFileName || 'No file selected'}</span>
        <button
          onClick={onToggleTheme}
          className="border border-border text-foreground p-1 px-2 rounded-md cursor-pointer text-base leading-none transition-colors hover:bg-accent"
          title="Toggle dark mode"
        >
          {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
        <button
          onClick={onOpenSettings}
          className="text-muted-foreground hover:text-foreground hover:bg-accent p-1.5 rounded-md transition-colors leading-none"
          title="Preferences"
        >
          <Settings className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
}
