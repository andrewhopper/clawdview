import { Settings, Sun, Moon, Github } from 'lucide-react';
import { Logo } from './Logo';
import { Button } from './ui/button';
import { Tooltip, TooltipContent, TooltipTrigger } from './ui/tooltip';
import { Separator } from './ui/separator';
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
    <header className="bg-card border-b border-border px-4 h-12 flex justify-between items-center shrink-0">
      <div className="flex items-center gap-2">
        <Logo size={22} />
        <h1 className="text-sm font-semibold tracking-tight">ClawdView</h1>
      </div>
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <div className="flex items-center gap-1.5">
          <span
            className={cn(
              'inline-block w-2 h-2 rounded-full',
              connected ? 'bg-green-500' : 'bg-red-500',
            )}
          />
          <span className="text-xs">{currentFileName || 'No file selected'}</span>
        </div>
        <Separator orientation="vertical" className="h-4 mx-1" />
        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="ghost" size="icon-sm" onClick={onToggleTheme}>
              {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>
          </TooltipTrigger>
          <TooltipContent>Toggle dark mode</TooltipContent>
        </Tooltip>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="ghost" size="icon-sm" onClick={onOpenSettings}>
              <Settings className="h-4 w-4" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>Preferences</TooltipContent>
        </Tooltip>
        <Tooltip>
          <TooltipTrigger asChild>
            <a href="https://github.com/andrewhopper/clawdview" target="_blank" rel="noopener noreferrer">
              <Button variant="ghost" size="icon-sm" asChild>
                <span><Github className="h-4 w-4" /></span>
              </Button>
            </a>
          </TooltipTrigger>
          <TooltipContent>GitHub</TooltipContent>
        </Tooltip>
      </div>
    </header>
  );
}
