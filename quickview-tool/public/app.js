import { renderHTML } from './js/renderers/html-renderer.js';
import { renderReact } from './js/renderers/react-renderer.js';
import { renderPythonPreview } from './js/renderers/python-renderer.js';
import { renderSVG } from './js/renderers/svg-renderer.js';
import { renderMarkdown } from './js/renderers/markdown-renderer.js';
import { renderJSON } from './js/renderers/json-renderer.js';
import { escapeHtml } from './js/utils.js';
import { FileTreeManager } from './js/managers/file-tree-manager.js';
import { TabManager } from './js/managers/tab-manager.js';
import { SocketManager } from './js/managers/socket-manager.js';

const HIGHLIGHT_LANG_MAP = {
  '.js': 'javascript',
  '.jsx': 'javascript',
  '.py': 'python',
  '.html': 'html',
  '.css': 'css',
  '.json': 'json',
  '.md': 'markdown',
  '.svg': 'xml'
};

const FORMATTABLE_EXTENSIONS = ['.js', '.jsx', '.json', '.html', '.css'];

class QuickViewApp {
  constructor() {
    this.currentFile = null;
    this.fileTree = null;
    this.commandPaletteOpen = false;
    this.commandPaletteSelectedIndex = -1;
    this.commandPaletteResults = [];

    this.tabManager = new TabManager();

    this.fileTreeManager = new FileTreeManager('file-tree', (file) => {
      this.loadFile(file);
    });

    this.socketManager = new SocketManager(
      (tree) => {
        this.fileTree = tree;
        this.fileTreeManager.render(tree);
      },
      (data) => {
        if (this.currentFile && data.relativePath === this.currentFile.path) {
          this.loadFile(this.currentFile);
        }
      }
    );

    this.setupUIHandlers();
    this.setupCommandPalette();
  }

  setupUIHandlers() {
    document.getElementById('refresh-files').addEventListener('click', () => {
      this.socketManager.requestRefresh();
    });

    document.getElementById('open-command-palette').addEventListener('click', () => {
      this.openCommandPalette();
    });

    document.getElementById('run-code').addEventListener('click', () => this.runCode());
    document.getElementById('format-code').addEventListener('click', () => this.formatCode());
    document.getElementById('open-external').addEventListener('click', () => this.openExternal());
  }

  async loadFile(file) {
    this.showLoading(true);

    try {
      const response = await fetch(`/api/file/${file.path}`);
      const data = await response.json();

      if (!response.ok) throw new Error(data.error || 'Failed to load file');

      this.currentFile = file;
      document.getElementById('current-file').textContent = file.name;

      this.updateCodePanel(data.content, data.extension);
      this.updatePreviewPanel(data.content, data.extension, file.name);
      this.updateActionButtons(data.extension);
    } catch (error) {
      this.showError('Failed to load file: ' + error.message);
    } finally {
      this.showLoading(false);
    }
  }

  updateCodePanel(content, extension) {
    const codeElement = document.getElementById('code-content');
    codeElement.textContent = content;

    if (window.hljs) {
      const language = HIGHLIGHT_LANG_MAP[extension];
      if (language) {
        codeElement.className = `language-${language}`;
        hljs.highlightElement(codeElement);
      }
    }
  }

  updatePreviewPanel(content, extension, filename) {
    const previewContent = document.getElementById('preview-content');
    const renderers = {
      '.html': () => renderHTML(previewContent, content),
      '.jsx': () => renderReact(previewContent, content),
      '.py': () => renderPythonPreview(previewContent, content, filename),
      '.svg': () => renderSVG(previewContent, content),
      '.md': () => renderMarkdown(previewContent, content),
      '.json': () => renderJSON(previewContent, content)
    };

    const renderer = renderers[extension];
    if (renderer) {
      renderer();
    } else {
      previewContent.innerHTML = `
        <div style="padding: 20px; color: #333;">
          <pre style="white-space: pre-wrap; font-family: monospace;">${escapeHtml(content)}</pre>
        </div>
      `;
    }
  }

  updateActionButtons(extension) {
    document.getElementById('run-code').style.display = extension === '.py' ? 'block' : 'none';
    document.getElementById('format-code').style.display = FORMATTABLE_EXTENSIONS.includes(extension) ? 'block' : 'none';
    document.getElementById('open-external').style.display = extension === '.html' ? 'block' : 'none';
  }

  async runCode() {
    if (!this.currentFile || this.currentFile.extension !== '.py') return;

    this.showLoading(true);

    try {
      const fileResponse = await fetch(`/api/file/${this.currentFile.path}`);
      const fileData = await fileResponse.json();

      const execResponse = await fetch('/api/execute/python', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: fileData.content, filename: this.currentFile.name })
      });

      const result = await execResponse.json();

      this.tabManager.switchTo('output');

      const outputContent = document.getElementById('output-content');
      outputContent.innerHTML = result.success
        ? `<div class="success"><strong>✅ Execution completed successfully</strong><pre>${escapeHtml(result.output || 'No output')}</pre></div>`
        : `<div class="error"><strong>❌ Execution failed</strong><pre>${escapeHtml(result.error || 'Unknown error')}</pre></div>`;
    } catch (error) {
      this.showError('Failed to execute Python script: ' + error.message);
    } finally {
      this.showLoading(false);
    }
  }

  async formatCode() {
    if (!this.currentFile) return;

    this.showLoading(true);

    try {
      const response = await fetch('/api/format', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filepath: this.currentFile.path,
          extension: this.currentFile.extension
        })
      });

      const result = await response.json();

      if (result.success) {
        this.loadFile(this.currentFile);
        const formatBtn = document.getElementById('format-code');
        const originalText = formatBtn.textContent;
        formatBtn.textContent = '✓ Formatted';
        formatBtn.style.background = '#10b981';
        setTimeout(() => {
          formatBtn.textContent = originalText;
          formatBtn.style.background = '';
        }, 2000);
      } else {
        this.showError('Failed to format code: ' + result.error);
      }
    } catch (error) {
      this.showError('Failed to format code: ' + error.message);
    } finally {
      this.showLoading(false);
    }
  }

  openExternal() {
    if (this.currentFile && this.currentFile.extension === '.html') {
      window.open(`/preview/${this.currentFile.path}`, '_blank');
    }
  }

  showLoading(show) {
    document.getElementById('loading').style.display = show ? 'flex' : 'none';
  }

  showError(message) {
    document.getElementById('preview-content').innerHTML = `<div class="error">${message}</div>`;
  }

  setupCommandPalette() {
    const overlay = document.getElementById('command-palette');
    const input = document.getElementById('command-palette-input');

    // Open with Cmd+K or Ctrl+K
    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        this.openCommandPalette();
        return;
      }

      if (!this.commandPaletteOpen) return;

      if (e.key === 'Escape') {
        e.preventDefault();
        this.closeCommandPalette();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        this.navigateCommandPalette(1);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        this.navigateCommandPalette(-1);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        this.selectCommandPaletteItem();
      }
    });

    // Close when clicking the backdrop
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        this.closeCommandPalette();
      }
    });

    // Filter results as user types
    input.addEventListener('input', () => {
      this.searchCommandPalette(input.value);
    });
  }

  openCommandPalette() {
    this.commandPaletteOpen = true;
    const overlay = document.getElementById('command-palette');
    const input = document.getElementById('command-palette-input');
    overlay.style.display = 'flex';
    input.value = '';
    this.searchCommandPalette('');
    input.focus();
  }

  closeCommandPalette() {
    this.commandPaletteOpen = false;
    const overlay = document.getElementById('command-palette');
    overlay.style.display = 'none';
    this.commandPaletteSelectedIndex = -1;
  }

  getFlatFileList() {
    const files = [];
    const traverse = (items) => {
      for (const item of items) {
        if (item.type === 'file') {
          files.push(item);
        } else if (item.children) {
          traverse(item.children);
        }
      }
    };
    if (this.fileTree) traverse(this.fileTree);
    return files;
  }

  searchCommandPalette(query) {
    const allFiles = this.getFlatFileList();
    let filtered;

    if (!query.trim()) {
      filtered = allFiles.slice(0, 20);
    } else {
      const q = query.toLowerCase();
      filtered = allFiles
        .filter(f => f.name.toLowerCase().includes(q) || f.path.toLowerCase().includes(q))
        .slice(0, 20);
    }

    this.commandPaletteResults = filtered;
    this.commandPaletteSelectedIndex = filtered.length > 0 ? 0 : -1;
    this.renderCommandPaletteResults();
  }

  renderCommandPaletteResults() {
    const container = document.getElementById('command-palette-results');
    container.innerHTML = '';

    if (this.commandPaletteResults.length === 0) {
      container.innerHTML = '<div class="command-palette-empty">No files found</div>';
      return;
    }

    const iconMap = {
      '.html': '🌐', '.js': '📜', '.jsx': '⚛️', '.py': '🐍',
      '.json': '📊', '.md': '📝', '.svg': '🎨', '.css': '🎨'
    };

    this.commandPaletteResults.forEach((file, index) => {
      const item = document.createElement('div');
      item.className = 'command-palette-result-item';
      if (index === this.commandPaletteSelectedIndex) {
        item.classList.add('active');
      }

      const dir = file.path.includes('/')
        ? file.path.substring(0, file.path.lastIndexOf('/'))
        : '';
      const icon = iconMap[file.extension] || '📄';

      item.innerHTML = `
        <span class="command-palette-result-icon">${icon}</span>
        <span class="command-palette-result-name">${escapeHtml(file.name)}</span>
        ${dir ? `<span class="command-palette-result-path">${escapeHtml(dir)}</span>` : ''}
      `;

      item.addEventListener('click', () => {
        this.commandPaletteSelectedIndex = index;
        this.selectCommandPaletteItem();
      });

      item.addEventListener('mouseenter', () => {
        this.commandPaletteSelectedIndex = index;
        this.updateCommandPaletteSelection();
      });

      container.appendChild(item);
    });
  }

  navigateCommandPalette(direction) {
    const len = this.commandPaletteResults.length;
    if (len === 0) return;

    this.commandPaletteSelectedIndex = (this.commandPaletteSelectedIndex + direction + len) % len;
    this.updateCommandPaletteSelection();

    const items = document.querySelectorAll('.command-palette-result-item');
    const activeItem = items[this.commandPaletteSelectedIndex];
    if (activeItem) activeItem.scrollIntoView({ block: 'nearest' });
  }

  updateCommandPaletteSelection() {
    document.querySelectorAll('.command-palette-result-item').forEach((item, index) => {
      item.classList.toggle('active', index === this.commandPaletteSelectedIndex);
    });
  }

  selectCommandPaletteItem() {
    if (this.commandPaletteSelectedIndex < 0 || this.commandPaletteSelectedIndex >= this.commandPaletteResults.length) {
      return;
    }

    const file = this.commandPaletteResults[this.commandPaletteSelectedIndex];
    this.closeCommandPalette();

    this.currentFile = file;
    this.loadFile(file);

    document.querySelectorAll('.file-item.selected').forEach(el => el.classList.remove('selected'));
    const sidebarItem = document.querySelector(`.file-item[data-path="${CSS.escape(file.path)}"]`);
    if (sidebarItem) sidebarItem.classList.add('selected');
  }
}

document.addEventListener('DOMContentLoaded', () => new QuickViewApp());
