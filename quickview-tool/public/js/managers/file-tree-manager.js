// Directories/files to always ignore in the tree
const IGNORED_DIRS = new Set([
  'node_modules', '.git', '__pycache__', '.svn', '.hg',
  'dist', 'build', '.next', '.nuxt', '.cache', '.parcel-cache',
  'coverage', '.nyc_output', '.tox', '.venv', 'venv', 'env',
  '.idea', '.vscode', '.DS_Store', 'bower_components',
  '.terraform', '.serverless'
]);

const FILE_TYPE_GROUPS = {
  'Web':      { extensions: new Set(['.html', '.css', '.svg']), icon: '🌐' },
  'Script':   { extensions: new Set(['.js', '.jsx', '.py']),    icon: '📜' },
  'Data':     { extensions: new Set(['.json', '.xml', '.yaml', '.yml']), icon: '📊' },
  'Docs':     { extensions: new Set(['.md', '.txt']),           icon: '📝' },
};

// Map extension to a short label for filter chips
const EXT_LABELS = {
  '.html': 'HTML', '.css': 'CSS', '.js': 'JS', '.jsx': 'JSX',
  '.py': 'Python', '.json': 'JSON', '.md': 'MD', '.svg': 'SVG',
  '.txt': 'TXT', '.xml': 'XML', '.yaml': 'YAML', '.yml': 'YML'
};

const VIEW_MODES = { TREE: 'tree', RECENT: 'recent', TYPE: 'type' };

// How many items to render per batch (virtual windowing lite)
const RENDER_BATCH = 200;

export class FileTreeManager {
  constructor(containerId, onFileSelect) {
    this.container = document.getElementById(containerId);
    this.onFileSelect = onFileSelect;

    // State
    this.rawTree = [];
    this.flatFiles = [];           // flattened list of all files (no dirs)
    this.collapsedPaths = new Set();
    this.viewMode = VIEW_MODES.TREE;
    this.searchQuery = '';
    this.activeExtFilters = new Set(); // when empty → show all
    this.showIgnored = false;
    this.selectedPath = null;

    // DOM refs (set by initControls after HTML is ready)
    this.searchInput = null;
    this.filterBar = null;
    this.viewBtns = {};
    this.fileCount = null;

    // Debounce handle for search
    this._searchTimeout = null;

    // Batch rendering
    this._renderQueue = [];
    this._renderRAF = null;
  }

  /* ------------------------------------------------------------------
   * Initialise external controls (called once after DOM ready)
   * ----------------------------------------------------------------*/
  initControls() {
    this.searchInput = document.getElementById('nav-search');
    this.filterBar = document.getElementById('nav-filter-chips');
    this.fileCount = document.getElementById('nav-file-count');

    // View mode buttons
    ['tree', 'recent', 'type'].forEach(mode => {
      const btn = document.getElementById(`nav-view-${mode}`);
      if (btn) {
        this.viewBtns[mode] = btn;
        btn.addEventListener('click', () => this.setViewMode(mode));
      }
    });

    // Search
    if (this.searchInput) {
      this.searchInput.addEventListener('input', () => {
        clearTimeout(this._searchTimeout);
        this._searchTimeout = setTimeout(() => {
          this.searchQuery = this.searchInput.value.trim().toLowerCase();
          this.renderCurrentView();
        }, 150);
      });
    }

    // Toggle ignored dirs
    const toggleIgnored = document.getElementById('nav-toggle-ignored');
    if (toggleIgnored) {
      toggleIgnored.addEventListener('click', () => {
        this.showIgnored = !this.showIgnored;
        toggleIgnored.classList.toggle('active', this.showIgnored);
        toggleIgnored.title = this.showIgnored ? 'Showing ignored dirs' : 'Hiding ignored dirs';
        this.renderCurrentView();
      });
    }
  }

  /* ------------------------------------------------------------------
   * Receive a new file tree from the server
   * ----------------------------------------------------------------*/
  render(fileTree) {
    this.rawTree = fileTree || [];
    this.flatFiles = this._flatten(this.rawTree);
    this._buildFilterChips();
    this.renderCurrentView();
  }

  /* ------------------------------------------------------------------
   * View mode switching
   * ----------------------------------------------------------------*/
  setViewMode(mode) {
    this.viewMode = mode;
    Object.entries(this.viewBtns).forEach(([m, btn]) => {
      btn.classList.toggle('active', m === mode);
    });
    this.renderCurrentView();
  }

  /* ------------------------------------------------------------------
   * Master render dispatcher
   * ----------------------------------------------------------------*/
  renderCurrentView() {
    // Cancel any pending batch render
    if (this._renderRAF) cancelAnimationFrame(this._renderRAF);

    this.container.innerHTML = '';

    const filtered = this._applyFilters();

    if (filtered.length === 0) {
      this.container.innerHTML = '<div class="no-files">No matching files</div>';
      this._updateCount(0);
      return;
    }

    switch (this.viewMode) {
      case VIEW_MODES.TREE:
        this._renderTree(filtered);
        break;
      case VIEW_MODES.RECENT:
        this._renderRecent(filtered);
        break;
      case VIEW_MODES.TYPE:
        this._renderByType(filtered);
        break;
    }
  }

  /* ------------------------------------------------------------------
   * TREE VIEW — hierarchical with collapsible dirs
   * ----------------------------------------------------------------*/
  _renderTree(files) {
    // When searching or filtering, we need to show a filtered tree.
    // Build a set of matching file paths + their ancestor dirs.
    const matchingPaths = new Set(files.map(f => f.path));
    const ancestorPaths = new Set();
    for (const f of files) {
      const parts = f.path.split(/[\\/]/);
      let cur = '';
      for (let i = 0; i < parts.length - 1; i++) {
        cur = cur ? cur + '/' + parts[i] : parts[i];
        ancestorPaths.add(cur);
      }
    }

    const frag = document.createDocumentFragment();
    let count = 0;

    const walk = (items, level) => {
      for (const item of items) {
        if (item.type === 'directory') {
          // Skip ignored dirs unless toggled on
          if (!this.showIgnored && IGNORED_DIRS.has(item.name)) continue;

          // If searching/filtering, only show dirs that lead to matching files
          if ((this.searchQuery || this.activeExtFilters.size > 0) && !ancestorPaths.has(item.path)) continue;

          const isCollapsed = this.collapsedPaths.has(item.path);

          const dirEl = this._makeDirElement(item, level, isCollapsed);
          frag.appendChild(dirEl);

          if (!isCollapsed && item.children) {
            walk(item.children, level + 1);
          }
        } else {
          // Only show files that passed the filter
          if (!matchingPaths.has(item.path)) continue;
          frag.appendChild(this._makeFileElement(item, level));
          count++;
        }
      }
    };

    walk(this.rawTree, 0);
    this.container.appendChild(frag);
    this._updateCount(count);
  }

  /* ------------------------------------------------------------------
   * RECENT VIEW — flat, sorted by mtime desc
   * ----------------------------------------------------------------*/
  _renderRecent(files) {
    const sorted = [...files].sort((a, b) => (b.mtime || 0) - (a.mtime || 0));
    this._renderFlatList(sorted);
  }

  /* ------------------------------------------------------------------
   * TYPE VIEW — grouped by file type category
   * ----------------------------------------------------------------*/
  _renderByType(files) {
    const groups = {};
    const ungrouped = [];

    for (const f of files) {
      let placed = false;
      for (const [groupName, { extensions }] of Object.entries(FILE_TYPE_GROUPS)) {
        if (extensions.has(f.extension)) {
          (groups[groupName] = groups[groupName] || []).push(f);
          placed = true;
          break;
        }
      }
      if (!placed) ungrouped.push(f);
    }

    const frag = document.createDocumentFragment();
    let count = 0;

    for (const [groupName, { icon }] of Object.entries(FILE_TYPE_GROUPS)) {
      const items = groups[groupName];
      if (!items || items.length === 0) continue;

      const header = document.createElement('div');
      header.className = 'nav-group-header';
      header.textContent = `${icon} ${groupName} (${items.length})`;
      const groupKey = `__group__${groupName}`;
      const isCollapsed = this.collapsedPaths.has(groupKey);
      header.classList.toggle('collapsed', isCollapsed);
      header.addEventListener('click', () => {
        if (this.collapsedPaths.has(groupKey)) {
          this.collapsedPaths.delete(groupKey);
        } else {
          this.collapsedPaths.add(groupKey);
        }
        this.renderCurrentView();
      });
      frag.appendChild(header);

      if (!isCollapsed) {
        const sorted = items.sort((a, b) => a.name.localeCompare(b.name));
        for (const f of sorted) {
          frag.appendChild(this._makeFileElement(f, 1));
          count++;
        }
      } else {
        count += items.length;
      }
    }

    if (ungrouped.length > 0) {
      const header = document.createElement('div');
      header.className = 'nav-group-header';
      header.textContent = `📄 Other (${ungrouped.length})`;
      frag.appendChild(header);
      for (const f of ungrouped) {
        frag.appendChild(this._makeFileElement(f, 1));
        count++;
      }
    }

    this.container.appendChild(frag);
    this._updateCount(count);
  }

  /* ------------------------------------------------------------------
   * Flat list renderer (used by recent view) — batched for perf
   * ----------------------------------------------------------------*/
  _renderFlatList(files) {
    this._updateCount(files.length);

    if (files.length <= RENDER_BATCH) {
      const frag = document.createDocumentFragment();
      for (const f of files) {
        frag.appendChild(this._makeFileElement(f, 0, true));
      }
      this.container.appendChild(frag);
      return;
    }

    // Batch render for large lists
    this._renderQueue = [...files];
    this._drainRenderQueue();
  }

  _drainRenderQueue() {
    const batch = this._renderQueue.splice(0, RENDER_BATCH);
    if (batch.length === 0) return;

    const frag = document.createDocumentFragment();
    for (const f of batch) {
      frag.appendChild(this._makeFileElement(f, 0, true));
    }
    this.container.appendChild(frag);

    if (this._renderQueue.length > 0) {
      this._renderRAF = requestAnimationFrame(() => this._drainRenderQueue());
    }
  }

  /* ------------------------------------------------------------------
   * DOM element builders
   * ----------------------------------------------------------------*/
  _makeDirElement(item, level, isCollapsed) {
    const el = document.createElement('div');
    el.className = 'file-item directory';
    el.style.paddingLeft = `${12 + level * 16}px`;

    const chevron = document.createElement('span');
    chevron.className = `nav-chevron ${isCollapsed ? '' : 'open'}`;
    chevron.textContent = '▶';
    el.appendChild(chevron);

    const label = document.createTextNode(item.name);
    el.appendChild(label);

    el.addEventListener('click', () => {
      if (this.collapsedPaths.has(item.path)) {
        this.collapsedPaths.delete(item.path);
      } else {
        this.collapsedPaths.add(item.path);
      }
      this.renderCurrentView();
    });

    return el;
  }

  _makeFileElement(item, level, showPath = false) {
    const el = document.createElement('div');
    el.className = `file-item file ${this._fileClass(item.extension)}`;
    el.style.paddingLeft = `${12 + level * 16}px`;

    if (showPath && item.path.includes('/')) {
      const dir = document.createElement('span');
      dir.className = 'nav-file-dir';
      dir.textContent = item.path.substring(0, item.path.lastIndexOf('/') + 1);
      el.appendChild(dir);
    }

    const name = document.createTextNode(item.name);
    el.appendChild(name);

    if (item.path === this.selectedPath) {
      el.classList.add('selected');
    }

    el.addEventListener('click', () => {
      document.querySelectorAll('.file-item.selected').forEach(s => s.classList.remove('selected'));
      el.classList.add('selected');
      this.selectedPath = item.path;
      this.onFileSelect(item);
    });

    return el;
  }

  /* ------------------------------------------------------------------
   * Filter chips — auto-generated from discovered extensions
   * ----------------------------------------------------------------*/
  _buildFilterChips() {
    if (!this.filterBar) return;
    this.filterBar.innerHTML = '';

    const extCounts = {};
    for (const f of this.flatFiles) {
      if (f.extension) {
        extCounts[f.extension] = (extCounts[f.extension] || 0) + 1;
      }
    }

    // Sort by count desc
    const sorted = Object.entries(extCounts).sort((a, b) => b[1] - a[1]);

    for (const [ext, count] of sorted) {
      const chip = document.createElement('button');
      chip.className = 'nav-chip';
      chip.textContent = `${EXT_LABELS[ext] || ext.replace('.', '').toUpperCase()}`;
      chip.title = `${count} file${count > 1 ? 's' : ''}`;
      chip.classList.toggle('active', this.activeExtFilters.has(ext));

      chip.addEventListener('click', () => {
        if (this.activeExtFilters.has(ext)) {
          this.activeExtFilters.delete(ext);
        } else {
          this.activeExtFilters.add(ext);
        }
        chip.classList.toggle('active', this.activeExtFilters.has(ext));
        this.renderCurrentView();
      });

      this.filterBar.appendChild(chip);
    }
  }

  /* ------------------------------------------------------------------
   * Helpers
   * ----------------------------------------------------------------*/
  _flatten(tree) {
    const result = [];
    const walk = (items) => {
      for (const item of items) {
        if (item.type === 'file') {
          result.push(item);
        } else if (item.children) {
          // Skip ignored dirs
          if (!this.showIgnored && IGNORED_DIRS.has(item.name)) continue;
          walk(item.children);
        }
      }
    };
    walk(tree);
    return result;
  }

  _applyFilters() {
    let files = this.flatFiles;

    // Extension filter
    if (this.activeExtFilters.size > 0) {
      files = files.filter(f => this.activeExtFilters.has(f.extension));
    }

    // Search filter
    if (this.searchQuery) {
      files = files.filter(f => {
        return f.name.toLowerCase().includes(this.searchQuery) ||
               f.path.toLowerCase().includes(this.searchQuery);
      });
    }

    return files;
  }

  _fileClass(extension) {
    if (!extension) return 'file';
    const ext = extension.toLowerCase().replace('.', '');
    const classMap = {
      html: 'html', js: 'js', jsx: 'js', py: 'py',
      json: 'json', md: 'md', svg: 'svg', css: 'css'
    };
    return classMap[ext] || 'file';
  }

  _updateCount(n) {
    if (this.fileCount) {
      this.fileCount.textContent = n > 0 ? `${n} file${n !== 1 ? 's' : ''}` : '';
    }
  }
}
