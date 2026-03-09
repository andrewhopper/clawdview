import { useState, useMemo, useCallback, useRef, useEffect } from 'react';
import { cn } from '@/lib/utils';
import type { FileTreeItem, ViewMode } from '../types';
import { ChevronRight, RefreshCw, Eye, Search, FolderTree, Clock, LayoutList, type LucideIcon } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from './ui/collapsible';
import { Tooltip, TooltipContent, TooltipTrigger } from './ui/tooltip';

const IGNORED_DIRS = new Set([
  'node_modules', '.git', '__pycache__', '.svn', '.hg',
  'dist', 'build', '.next', '.nuxt', '.cache', '.parcel-cache',
  'coverage', '.nyc_output', '.tox', '.venv', 'venv', 'env',
  '.idea', '.vscode', '.DS_Store', 'bower_components',
  '.terraform', '.serverless',
]);

const FILE_TYPE_GROUPS: Record<string, { extensions: Set<string>; icon: string }> = {
  'Web': { extensions: new Set(['.html', '.css', '.svg']), icon: '🌐' },
  'Script': { extensions: new Set(['.js', '.jsx', '.py']), icon: '📜' },
  'Data': { extensions: new Set(['.json', '.xml', '.yaml', '.yml']), icon: '📊' },
  'Docs': { extensions: new Set(['.md', '.txt']), icon: '📝' },
};

const EXT_LABELS: Record<string, string> = {
  '.html': 'HTML', '.css': 'CSS', '.js': 'JS', '.jsx': 'JSX',
  '.py': 'Python', '.json': 'JSON', '.md': 'MD', '.svg': 'SVG',
  '.txt': 'TXT', '.xml': 'XML', '.yaml': 'YAML', '.yml': 'YML',
};

const FILE_ICONS: Record<string, string> = {
  html: '🌐', js: '📜', jsx: '📜', py: '🐍',
  json: '📊', md: '📝', svg: '🎨', css: '🎨',
};

const VIEW_MODES: { mode: ViewMode; icon: LucideIcon; label: string }[] = [
  { mode: 'tree', icon: FolderTree, label: 'Tree' },
  { mode: 'recent', icon: Clock, label: 'Recent' },
  { mode: 'type', icon: LayoutList, label: 'Type' },
];

interface FileTreeProps {
  tree: FileTreeItem[];
  selectedPath: string | null;
  onFileSelect: (file: FileTreeItem) => void;
  onRefresh: () => void;
  isFileTypeWatched: (ext: string) => boolean;
}

export function FileTree({ tree, selectedPath, onFileSelect, onRefresh, isFileTypeWatched }: FileTreeProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('tree');
  const [searchQuery, setSearchQuery] = useState('');
  const [collapsedPaths, setCollapsedPaths] = useState<Set<string>>(new Set());
  const [activeExtFilters, setActiveExtFilters] = useState<Set<string>>(new Set());
  const [showIgnored, setShowIgnored] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);

  const filteredTree = useMemo(() => {
    function filterByPrefs(items: FileTreeItem[]): FileTreeItem[] {
      return items
        .map((item) => {
          if (item.type === 'directory') {
            const children = filterByPrefs(item.children || []);
            return children.length > 0 ? { ...item, children } : null;
          }
          return isFileTypeWatched(item.extension || '') ? item : null;
        })
        .filter(Boolean) as FileTreeItem[];
    }
    return filterByPrefs(tree);
  }, [tree, isFileTypeWatched]);

  const flatFiles = useMemo(() => {
    const result: FileTreeItem[] = [];
    function walk(items: FileTreeItem[]) {
      for (const item of items) {
        if (item.type === 'file') {
          result.push(item);
        } else if (item.children && (showIgnored || !IGNORED_DIRS.has(item.name))) {
          walk(item.children);
        }
      }
    }
    walk(filteredTree);
    return result;
  }, [filteredTree, showIgnored]);

  const displayFiles = useMemo(() => {
    let files = flatFiles;
    if (activeExtFilters.size > 0) {
      files = files.filter((f) => activeExtFilters.has(f.extension || ''));
    }
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      files = files.filter(
        (f) => f.name.toLowerCase().includes(q) || f.path.toLowerCase().includes(q),
      );
    }
    return files;
  }, [flatFiles, activeExtFilters, searchQuery]);

  const extCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const f of flatFiles) {
      if (f.extension) {
        counts[f.extension] = (counts[f.extension] || 0) + 1;
      }
    }
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  }, [flatFiles]);

  const toggleCollapse = useCallback((path: string) => {
    setCollapsedPaths((prev) => {
      const next = new Set(prev);
      if (next.has(path)) next.delete(path);
      else next.add(path);
      return next;
    });
  }, []);

  const toggleExtFilter = useCallback((ext: string) => {
    setActiveExtFilters((prev) => {
      const next = new Set(prev);
      if (next.has(ext)) next.delete(ext);
      else next.add(ext);
      return next;
    });
  }, []);

  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.ctrlKey || e.metaKey) && (e.key === 'p' || e.key === 'f')) {
        const tag = (document.activeElement as HTMLElement)?.tagName;
        if (tag === 'TEXTAREA' || (tag === 'INPUT' && document.activeElement !== searchInputRef.current)) return;
        e.preventDefault();
        searchInputRef.current?.focus();
        searchInputRef.current?.select();
      }
      if (e.altKey && !e.ctrlKey && !e.metaKey) {
        const idx = parseInt(e.key) - 1;
        if (idx >= 0 && idx < VIEW_MODES.length) {
          e.preventDefault();
          setViewMode(VIEW_MODES[idx].mode);
        }
      }
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <aside className="w-72 bg-card border-r border-border flex flex-col overflow-hidden shrink-0">
      {/* Header */}
      <div className="px-3 py-2 border-b border-border flex justify-between items-center">
        <h3 className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Files</h3>
        <div className="flex items-center gap-0.5">
          {displayFiles.length > 0 && (
            <span className="text-[10px] text-muted-foreground mr-1">
              {displayFiles.length} file{displayFiles.length !== 1 ? 's' : ''}
            </span>
          )}
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant={showIgnored ? 'secondary' : 'ghost'}
                size="icon-sm"
                onClick={() => setShowIgnored(!showIgnored)}
              >
                <Eye className="w-3.5 h-3.5" />
              </Button>
            </TooltipTrigger>
            <TooltipContent>{showIgnored ? 'Showing ignored dirs' : 'Show ignored dirs'}</TooltipContent>
          </Tooltip>
          <Tooltip>
            <TooltipTrigger asChild>
              <Button variant="ghost" size="icon-sm" onClick={onRefresh}>
                <RefreshCw className="w-3.5 h-3.5" />
              </Button>
            </TooltipTrigger>
            <TooltipContent>Refresh file tree</TooltipContent>
          </Tooltip>
        </div>
      </div>

      {/* Search */}
      <div className="px-3 py-2 border-b border-border">
        <div className="relative">
          <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
          <Input
            ref={searchInputRef}
            placeholder="Search files... (Ctrl+F)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="h-7 pl-7 text-xs"
          />
        </div>
      </div>

      {/* View mode toggle */}
      <div className="px-3 py-1.5 border-b border-border flex items-center gap-1">
        {VIEW_MODES.map(({ mode, icon: Icon, label }) => (
          <Button
            key={mode}
            variant={viewMode === mode ? 'secondary' : 'ghost'}
            size="sm"
            className="h-6 px-2 text-[11px] gap-1"
            onClick={() => setViewMode(mode)}
          >
            <Icon className="w-3 h-3" />
            {label}
          </Button>
        ))}
      </div>

      {/* Extension filter chips */}
      {extCounts.length > 0 && (
        <div className="flex flex-wrap gap-1 px-2.5 py-1.5 border-b border-border max-h-16 overflow-y-auto">
          {extCounts.map(([ext, count]) => (
            <Badge
              key={ext}
              variant={activeExtFilters.has(ext) ? 'default' : 'outline'}
              className="cursor-pointer text-[10px] px-2 py-0"
              onClick={() => toggleExtFilter(ext)}
              title={`${count} file${count > 1 ? 's' : ''}`}
            >
              {EXT_LABELS[ext] || ext.replace('.', '').toUpperCase()}
            </Badge>
          ))}
        </div>
      )}

      {/* File tree content */}
      <ScrollArea className="flex-1">
        <div className="p-1.5">
          {displayFiles.length === 0 ? (
            <div className="text-muted-foreground text-sm text-center py-6 px-3">No matching files</div>
          ) : viewMode === 'tree' ? (
            <TreeView
              tree={filteredTree}
              displayFiles={displayFiles}
              collapsedPaths={collapsedPaths}
              selectedPath={selectedPath}
              showIgnored={showIgnored}
              searchQuery={searchQuery}
              activeExtFilters={activeExtFilters}
              onFileSelect={onFileSelect}
              onToggleCollapse={toggleCollapse}
            />
          ) : viewMode === 'recent' ? (
            <RecentView
              files={displayFiles}
              selectedPath={selectedPath}
              onFileSelect={onFileSelect}
            />
          ) : (
            <TypeView
              files={displayFiles}
              collapsedPaths={collapsedPaths}
              selectedPath={selectedPath}
              onFileSelect={onFileSelect}
              onToggleCollapse={toggleCollapse}
            />
          )}
        </div>
      </ScrollArea>
    </aside>
  );
}

// Tree view using shadcn Collapsible
function TreeView({
  tree, displayFiles, collapsedPaths, selectedPath, showIgnored,
  searchQuery, activeExtFilters, onFileSelect, onToggleCollapse,
}: {
  tree: FileTreeItem[];
  displayFiles: FileTreeItem[];
  collapsedPaths: Set<string>;
  selectedPath: string | null;
  showIgnored: boolean;
  searchQuery: string;
  activeExtFilters: Set<string>;
  onFileSelect: (file: FileTreeItem) => void;
  onToggleCollapse: (path: string) => void;
}) {
  const matchingPaths = useMemo(() => new Set(displayFiles.map((f) => f.path)), [displayFiles]);

  const ancestorPaths = useMemo(() => {
    const ancestors = new Set<string>();
    for (const f of displayFiles) {
      const parts = f.path.split(/[\\/]/);
      let cur = '';
      for (let i = 0; i < parts.length - 1; i++) {
        cur = cur ? cur + '/' + parts[i] : parts[i];
        ancestors.add(cur);
      }
    }
    return ancestors;
  }, [displayFiles]);

  function renderItems(items: FileTreeItem[], level: number) {
    return items.map((item) => {
      if (item.type === 'directory') {
        if (!showIgnored && IGNORED_DIRS.has(item.name)) return null;
        if ((searchQuery || activeExtFilters.size > 0) && !ancestorPaths.has(item.path)) return null;

        const isOpen = !collapsedPaths.has(item.path);
        return (
          <Collapsible key={item.path} open={isOpen} onOpenChange={() => onToggleCollapse(item.path)}>
            <CollapsibleTrigger className="flex items-center gap-1.5 w-full py-1 px-2 cursor-pointer rounded-md text-sm font-medium text-foreground hover:bg-accent select-none" style={{ paddingLeft: `${8 + level * 16}px` }}>
              <ChevronRight className={cn('w-3 h-3 text-muted-foreground transition-transform', isOpen && 'rotate-90')} />
              <span className="truncate">{item.name}</span>
            </CollapsibleTrigger>
            <CollapsibleContent>
              {item.children && renderItems(item.children, level + 1)}
            </CollapsibleContent>
          </Collapsible>
        );
      }

      if (!matchingPaths.has(item.path)) return null;
      return (
        <FileItem
          key={item.path}
          item={item}
          level={level}
          isSelected={item.path === selectedPath}
          onClick={() => onFileSelect(item)}
        />
      );
    });
  }

  return <>{renderItems(tree, 0)}</>;
}

function RecentView({
  files, selectedPath, onFileSelect,
}: {
  files: FileTreeItem[];
  selectedPath: string | null;
  onFileSelect: (file: FileTreeItem) => void;
}) {
  const sorted = useMemo(
    () => [...files].sort((a, b) => (b.mtime || 0) - (a.mtime || 0)),
    [files],
  );
  return <FlatList files={sorted} selectedPath={selectedPath} onFileSelect={onFileSelect} showPath />;
}

function FlatList({
  files, selectedPath, onFileSelect, showPath,
}: {
  files: FileTreeItem[];
  selectedPath: string | null;
  onFileSelect: (file: FileTreeItem) => void;
  showPath?: boolean;
}) {
  return (
    <>
      {files.map((file) => (
        <FileItem
          key={file.path}
          item={file}
          level={0}
          isSelected={file.path === selectedPath}
          onClick={() => onFileSelect(file)}
          showPath={showPath}
        />
      ))}
    </>
  );
}

function TypeView({
  files, collapsedPaths, selectedPath, onFileSelect, onToggleCollapse,
}: {
  files: FileTreeItem[];
  collapsedPaths: Set<string>;
  selectedPath: string | null;
  onFileSelect: (file: FileTreeItem) => void;
  onToggleCollapse: (path: string) => void;
}) {
  const groups = useMemo(() => {
    const grouped: Record<string, FileTreeItem[]> = {};
    const ungrouped: FileTreeItem[] = [];

    for (const f of files) {
      let placed = false;
      for (const [groupName, { extensions }] of Object.entries(FILE_TYPE_GROUPS)) {
        if (extensions.has(f.extension || '')) {
          (grouped[groupName] = grouped[groupName] || []).push(f);
          placed = true;
          break;
        }
      }
      if (!placed) ungrouped.push(f);
    }

    // Pre-sort each group by name
    for (const items of Object.values(grouped)) {
      items.sort((a, b) => a.name.localeCompare(b.name));
    }
    ungrouped.sort((a, b) => a.name.localeCompare(b.name));

    return { grouped, ungrouped };
  }, [files]);

  return (
    <>
      {Object.entries(FILE_TYPE_GROUPS).map(([groupName, { icon }]) => {
        const items = groups.grouped[groupName];
        if (!items || items.length === 0) return null;
        const groupKey = `__group__${groupName}`;
        const isOpen = !collapsedPaths.has(groupKey);

        return (
          <Collapsible key={groupName} open={isOpen} onOpenChange={() => onToggleCollapse(groupKey)}>
            <CollapsibleTrigger className="flex items-center gap-1 w-full text-xs font-semibold text-muted-foreground py-2 px-3 cursor-pointer select-none uppercase tracking-wide hover:text-foreground">
              <ChevronRight className={cn('w-2.5 h-2.5 transition-transform', isOpen && 'rotate-90')} />
              {icon} {groupName} ({items.length})
            </CollapsibleTrigger>
            <CollapsibleContent>
              {items.map((f) => (
                  <FileItem
                    key={f.path}
                    item={f}
                    level={1}
                    isSelected={f.path === selectedPath}
                    onClick={() => onFileSelect(f)}
                  />
                ))}
            </CollapsibleContent>
          </Collapsible>
        );
      })}
      {groups.ungrouped.length > 0 && (
        <div>
          <div className="text-xs font-semibold text-muted-foreground py-2 px-3 uppercase tracking-wide">
            📄 Other ({groups.ungrouped.length})
          </div>
          {groups.ungrouped.map((f) => (
            <FileItem
              key={f.path}
              item={f}
              level={1}
              isSelected={f.path === selectedPath}
              onClick={() => onFileSelect(f)}
            />
          ))}
        </div>
      )}
    </>
  );
}

function FileItem({
  item, level, isSelected, onClick, showPath,
}: {
  item: FileTreeItem;
  level: number;
  isSelected: boolean;
  onClick: () => void;
  showPath?: boolean;
}) {
  const ext = (item.extension || '').replace('.', '');
  const icon = FILE_ICONS[ext] || '📄';

  return (
    <div
      className={cn(
        'flex items-center gap-1.5 py-1 px-2 cursor-pointer rounded-md text-sm transition-colors select-none',
        isSelected
          ? 'bg-primary text-primary-foreground'
          : 'text-foreground hover:bg-accent',
      )}
      style={{ paddingLeft: `${8 + level * 16}px` }}
      onClick={onClick}
    >
      <span className="text-sm shrink-0">{icon}</span>
      {showPath && item.path.includes('/') && (
        <span className="text-[11px] text-muted-foreground opacity-70">
          {item.path.substring(0, item.path.lastIndexOf('/') + 1)}
        </span>
      )}
      <span className="truncate">{item.name}</span>
    </div>
  );
}
