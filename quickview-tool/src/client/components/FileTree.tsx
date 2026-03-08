import { useState, useMemo, useCallback, useRef, useEffect } from 'react';
import { cn } from '@/lib/utils';
import type { FileTreeItem, ViewMode } from '../types';
import { ChevronRight, RefreshCw, Eye } from 'lucide-react';

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
  const containerRef = useRef<HTMLDivElement>(null);

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
        const viewMap: Record<string, ViewMode> = { '1': 'tree', '2': 'recent', '3': 'type' };
        if (viewMap[e.key]) {
          e.preventDefault();
          setViewMode(viewMap[e.key]);
        }
      }
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <aside className="w-72 bg-card border-r border-border flex flex-col overflow-hidden shrink-0">
      {/* Header */}
      <div className="px-3 py-2.5 border-b border-border flex justify-between items-center">
        <h3 className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Files</h3>
        <div className="flex items-center gap-1">
          <span className="text-[10px] text-muted-foreground mr-1">
            {displayFiles.length > 0 ? `${displayFiles.length} file${displayFiles.length !== 1 ? 's' : ''}` : ''}
          </span>
          <button
            onClick={() => setShowIgnored(!showIgnored)}
            className={cn(
              'p-1 rounded-sm text-muted-foreground hover:text-foreground hover:bg-accent transition-colors',
              showIgnored && 'text-foreground bg-accent',
            )}
            title={showIgnored ? 'Showing ignored dirs' : 'Show ignored dirs (node_modules, etc.)'}
          >
            <Eye className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={onRefresh}
            className="p-1 rounded-sm text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
            title="Refresh file tree"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="px-3 py-2 border-b border-border">
        <input
          ref={searchInputRef}
          type="text"
          placeholder="Search files... (Ctrl+F)"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-background border border-border text-foreground rounded-md px-2 py-1.5 text-xs font-sans outline-none transition-colors focus:border-ring placeholder:text-muted-foreground"
        />
      </div>

      {/* View mode toggle */}
      <div className="px-3 py-1.5 border-b border-border flex items-center gap-1">
        {(['tree', 'recent', 'type'] as ViewMode[]).map((mode) => (
          <button
            key={mode}
            onClick={() => setViewMode(mode)}
            className={cn(
              'px-2 py-0.5 rounded-sm text-[11px] border border-transparent transition-colors text-muted-foreground hover:text-foreground hover:bg-accent',
              viewMode === mode && 'text-foreground bg-secondary border-border',
            )}
          >
            {mode === 'tree' ? '🗂 Tree' : mode === 'recent' ? '🕐 Recent' : '📋 Type'}
          </button>
        ))}
      </div>

      {/* Extension filter chips */}
      {extCounts.length > 0 && (
        <div className="flex flex-wrap gap-1 px-2.5 py-1.5 border-b border-border max-h-16 overflow-y-auto">
          {extCounts.map(([ext, count]) => (
            <button
              key={ext}
              onClick={() => toggleExtFilter(ext)}
              className={cn(
                'px-2 py-px rounded-full text-[10px] font-medium border transition-colors whitespace-nowrap',
                activeExtFilters.has(ext)
                  ? 'bg-primary text-primary-foreground border-primary'
                  : 'bg-background border-border text-muted-foreground hover:text-foreground hover:border-muted-foreground',
              )}
              title={`${count} file${count > 1 ? 's' : ''}`}
            >
              {EXT_LABELS[ext] || ext.replace('.', '').toUpperCase()}
            </button>
          ))}
        </div>
      )}

      {/* File tree */}
      <div ref={containerRef} className="flex-1 overflow-y-auto p-1.5" tabIndex={0}>
        {displayFiles.length === 0 ? (
          <div className="text-muted-foreground text-[13px] text-center py-6 px-3">No matching files</div>
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
          <FlatList
            files={[...displayFiles].sort((a, b) => (b.mtime || 0) - (a.mtime || 0))}
            selectedPath={selectedPath}
            onFileSelect={onFileSelect}
            showPath
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
    </aside>
  );
}

// Tree view sub-component
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

        const isCollapsed = collapsedPaths.has(item.path);
        return (
          <div key={item.path}>
            <div
              className="flex items-center gap-1.5 py-1 px-2.5 cursor-pointer rounded-md text-[13px] font-medium text-foreground hover:bg-accent select-none"
              style={{ paddingLeft: `${12 + level * 16}px` }}
              onClick={() => onToggleCollapse(item.path)}
            >
              <ChevronRight
                className={cn('w-3 h-3 text-muted-foreground transition-transform', !isCollapsed && 'rotate-90')}
              />
              <span>{item.name}</span>
            </div>
            {!isCollapsed && item.children && renderItems(item.children, level + 1)}
          </div>
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

    return { grouped, ungrouped };
  }, [files]);

  return (
    <>
      {Object.entries(FILE_TYPE_GROUPS).map(([groupName, { icon }]) => {
        const items = groups.grouped[groupName];
        if (!items || items.length === 0) return null;
        const groupKey = `__group__${groupName}`;
        const isCollapsed = collapsedPaths.has(groupKey);

        return (
          <div key={groupName}>
            <div
              className={cn(
                'text-[11px] font-semibold text-muted-foreground py-2 px-3 cursor-pointer select-none uppercase tracking-wide flex items-center gap-1 hover:text-foreground',
              )}
              onClick={() => onToggleCollapse(groupKey)}
            >
              <ChevronRight
                className={cn('w-2.5 h-2.5 transition-transform', !isCollapsed && 'rotate-90')}
              />
              {icon} {groupName} ({items.length})
            </div>
            {!isCollapsed &&
              items
                .sort((a, b) => a.name.localeCompare(b.name))
                .map((f) => (
                  <FileItem
                    key={f.path}
                    item={f}
                    level={1}
                    isSelected={f.path === selectedPath}
                    onClick={() => onFileSelect(f)}
                  />
                ))}
          </div>
        );
      })}
      {groups.ungrouped.length > 0 && (
        <div>
          <div className="text-[11px] font-semibold text-muted-foreground py-2 px-3 uppercase tracking-wide">
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
        'flex items-center gap-1.5 py-1 px-2.5 cursor-pointer rounded-md text-[13px] transition-colors select-none',
        isSelected
          ? 'bg-primary text-primary-foreground'
          : 'text-foreground hover:bg-accent',
      )}
      style={{ paddingLeft: `${12 + level * 16}px` }}
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
