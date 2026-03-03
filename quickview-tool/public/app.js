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

    this.tabManager = new TabManager();

    this.fileTreeManager = new FileTreeManager('file-tree', (file) => {
      this.loadFile(file);
    });

    this.socketManager = new SocketManager(
      (tree) => this.fileTreeManager.render(tree),
      (data) => {
        if (this.currentFile && data.relativePath === this.currentFile.path) {
          this.loadFile(this.currentFile);
        }
      }
    );

    this.setupUIHandlers();
  }

  setupUIHandlers() {
    document.getElementById('refresh-files').addEventListener('click', () => {
      this.socketManager.requestRefresh();
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
}

document.addEventListener('DOMContentLoaded', () => new QuickViewApp());
