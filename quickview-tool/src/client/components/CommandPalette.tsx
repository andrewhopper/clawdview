import { useState, useEffect, useCallback, useRef } from 'react';
import type { FileTreeItem } from '../types';
import { cn } from '@/lib/utils';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  fileTree: FileTreeItem[];
  onSelectFile: (file: FileTreeItem) => void;
}

const ICON_MAP: Record<string, string> = {
  '.html': '🌐', '.js': '📜', '.jsx': '⚛️', '.py': '🐍',
  '.json': '📊', '.md': '📝', '.svg': '🎨', '.css': '🎨',
};

function getFlatFileList(items: FileTreeItem[]): FileTreeItem[] {
  const files: FileTreeItem[] = [];
  const traverse = (nodes: FileTreeItem[]) => {
    for (const node of nodes) {
      if (node.type === 'file') {
        files.push(node);
      } else if (node.children) {
        traverse(node.children);
      }
    }
  };
  traverse(items);
  return files;
}

export function CommandPalette({ isOpen, onClose, fileTree, onSelectFile }: CommandPaletteProps) {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const allFiles = getFlatFileList(fileTree);
  const results = query.trim()
    ? allFiles.filter(f => f.name.toLowerCase().includes(query.toLowerCase()) || f.path.toLowerCase().includes(query.toLowerCase())).slice(0, 20)
    : allFiles.slice(0, 20);

  useEffect(() => {
    if (isOpen) {
      setQuery('');
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 0);
    }
  }, [isOpen]);

  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(i => Math.min(i + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(i => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (results[selectedIndex]) {
        onSelectFile(results[selectedIndex]);
      }
    }
  }, [results, selectedIndex, onClose, onSelectFile]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/60 flex items-start justify-center pt-[15vh]"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="bg-card border border-border rounded-lg shadow-2xl w-full max-w-lg overflow-hidden">
        <div className="p-3 border-b border-border">
          <input
            ref={inputRef}
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search files..."
            className="w-full bg-transparent text-foreground placeholder:text-muted-foreground outline-none text-sm"
          />
        </div>
        <div className="max-h-80 overflow-y-auto">
          {results.length === 0 ? (
            <div className="px-3 py-6 text-center text-sm text-muted-foreground">No files found</div>
          ) : (
            results.map((file, i) => {
              const dir = file.path.includes('/') ? file.path.substring(0, file.path.lastIndexOf('/')) : '';
              const icon = ICON_MAP[file.extension || ''] || '📄';
              return (
                <button
                  key={file.path}
                  className={cn(
                    'w-full text-left px-3 py-2 flex items-center gap-2.5 text-sm hover:bg-accent',
                    i === selectedIndex && 'bg-accent',
                  )}
                  onMouseEnter={() => setSelectedIndex(i)}
                  onClick={() => onSelectFile(file)}
                >
                  <span className="shrink-0">{icon}</span>
                  <span className="font-medium text-foreground truncate">{file.name}</span>
                  {dir && <span className="text-muted-foreground text-xs truncate ml-auto shrink-0">{dir}</span>}
                </button>
              );
            })
          )}
        </div>
        <div className="px-3 py-2 border-t border-border flex gap-3 text-xs text-muted-foreground">
          <span><kbd className="font-mono">↑↓</kbd> navigate</span>
          <span><kbd className="font-mono">↵</kbd> open</span>
          <span><kbd className="font-mono">esc</kbd> close</span>
        </div>
      </div>
    </div>
  );
}
