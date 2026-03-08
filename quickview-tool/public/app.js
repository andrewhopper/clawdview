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
import { PreferencesManager } from './js/managers/preferences-manager.js';

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
    this.s3Enabled = false;

    this.preferencesManager = new PreferencesManager((prefs) => {
      this.onPreferencesChanged(prefs);
    });

    this.tabManager = new TabManager();

    this.fileTreeManager = new FileTreeManager('file-tree', (file) => {
      this.loadFile(file);
    }, this.preferencesManager);

    this.fileTreeManager.initControls();

    this.socketManager = new SocketManager(
      (tree) => this.fileTreeManager.render(tree),
      (data) => {
        if (this.preferencesManager.get('autoOpenOnChange') &&
            this.currentFile && data.relativePath === this.currentFile.path) {
          this.loadFile(this.currentFile);
        }
      }
    );

    this.setupUIHandlers();
    this.checkS3Status();
    this.updateThemeUI();
  }

  onPreferencesChanged(prefs) {
    if (this.fileTreeManager.lastTree) {
      this.fileTreeManager.render(this.fileTreeManager.lastTree);
    }
  }

  setupUIHandlers() {
    document.getElementById('refresh-files').addEventListener('click', () => {
      this.socketManager.requestRefresh();
    });

    document.getElementById('run-code').addEventListener('click', () => this.runCode());
    document.getElementById('format-code').addEventListener('click', () => this.formatCode());
    document.getElementById('open-external').addEventListener('click', () => this.openExternal());
    document.getElementById('share-file').addEventListener('click', () => this.openShareModal());
    document.getElementById('share-modal-close').addEventListener('click', () => this.closeShareModal());
    document.getElementById('share-presign-btn').addEventListener('click', () => this.sharePresigned());
    document.getElementById('share-copy-btn').addEventListener('click', () => this.copyShareUrl());
    document.getElementById('share-modal').addEventListener('click', (e) => {
      if (e.target.id === 'share-modal') this.closeShareModal();
    });

    document.getElementById('file-info').addEventListener('click', () => this.showFileInfo());
    document.getElementById('file-info-close').addEventListener('click', () => this.hideFileInfo());
    document.getElementById('file-info-modal').addEventListener('click', (e) => {
      if (e.target.id === 'file-info-modal') this.hideFileInfo();
    });
    document.getElementById('theme-toggle').addEventListener('click', () => this.toggleTheme());

    document.getElementById('settings-btn').addEventListener('click', () => {
      this.preferencesManager.toggle();
    });
  }

  toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('quickview-theme', isDark ? 'dark' : 'light');
    this.updateThemeUI();
  }

  updateThemeUI() {
    const isDark = document.documentElement.classList.contains('dark');
    document.getElementById('theme-toggle').textContent = isDark ? '☀️' : '🌙';
    document.getElementById('hljs-light').disabled = isDark;
    document.getElementById('hljs-dark').disabled = !isDark;
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
        <div class="preview-text">
          <pre style="white-space: pre-wrap;">${escapeHtml(content)}</pre>
        </div>
      `;
    }
  }

  updateActionButtons(extension) {
    document.getElementById('run-code').style.display = extension === '.py' ? 'block' : 'none';
    document.getElementById('format-code').style.display = FORMATTABLE_EXTENSIONS.includes(extension) ? 'block' : 'none';
    document.getElementById('open-external').style.display = extension === '.html' ? 'block' : 'none';
    document.getElementById('share-file').style.display = this.s3Enabled ? 'block' : 'none';
    document.getElementById('file-info').style.display = 'block';
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
        formatBtn.style.background = 'hsl(142 71% 45%)';
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

  async checkS3Status() {
    try {
      const response = await fetch('/api/share/status');
      const data = await response.json();
      this.s3Enabled = data.enabled;
    } catch {
      this.s3Enabled = false;
    }
  }

  openShareModal() {
    if (!this.currentFile) return;
    document.getElementById('share-filename').textContent = `File: ${this.currentFile.name}`;
    document.getElementById('share-result').style.display = 'none';
    document.getElementById('share-error').style.display = 'none';
    document.getElementById('share-modal').style.display = 'flex';
  }

  closeShareModal() {
    document.getElementById('share-modal').style.display = 'none';
  }

  async sharePresigned() {
    if (!this.currentFile) return;

    const expiresIn = parseInt(document.getElementById('share-expiry').value, 10);
    document.getElementById('share-presign-btn').disabled = true;

    try {
      const response = await fetch('/api/share/presign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filePath: this.currentFile.path, expiresIn })
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.error || 'Failed to create share link');

      this.showShareResult(data.url, `Pre-signed URL expires in ${this.formatExpiry(data.expiresIn)}`);
    } catch (error) {
      this.showShareError(error.message);
    } finally {
      document.getElementById('share-presign-btn').disabled = false;
    }
  }

  showShareResult(url, info) {
    document.getElementById('share-url').value = url;
    document.getElementById('share-info').textContent = info;
    document.getElementById('share-result').style.display = 'block';
    document.getElementById('share-error').style.display = 'none';
  }

  showShareError(message) {
    document.getElementById('share-error').textContent = message;
    document.getElementById('share-error').style.display = 'block';
    document.getElementById('share-result').style.display = 'none';
  }

  async copyShareUrl() {
    const url = document.getElementById('share-url').value;
    try {
      await navigator.clipboard.writeText(url);
      const btn = document.getElementById('share-copy-btn');
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      btn.style.background = '#10b981';
      setTimeout(() => { btn.textContent = original; btn.style.background = ''; }, 2000);
    } catch {
      document.getElementById('share-url').select();
    }
  }

  formatExpiry(seconds) {
    if (seconds < 3600) return `${Math.round(seconds / 60)} minutes`;
    if (seconds < 86400) return `${Math.round(seconds / 3600)} hour(s)`;
    return `${Math.round(seconds / 86400)} day(s)`;
  }

  async showFileInfo() {
    if (!this.currentFile) return;

    const modal = document.getElementById('file-info-modal');
    const title = document.getElementById('file-info-title');
    const body = document.getElementById('file-info-body');

    title.textContent = this.currentFile.name;
    body.innerHTML = '<div style="text-align:center;padding:12px;color:hsl(var(--muted-foreground))">Loading...</div>';
    modal.style.display = 'flex';

    try {
      const response = await fetch(`/api/file-info/${this.currentFile.path}`);
      const data = await response.json();

      if (!response.ok) throw new Error(data.error || 'Failed to load file info');

      const rows = [
        ['Filename', data.filename],
        ['Path', data.path],
        ['Extension', data.extension || 'None'],
        ['Inode', data.inode],
        ['Size', this.formatFileSize(data.size)],
      ];

      if (data.lines != null) rows.push(['Lines', data.lines.toLocaleString()]);
      rows.push(['Modified', new Date(data.modifiedAt).toLocaleString()]);
      rows.push(['Created', new Date(data.createdAt).toLocaleString()]);
      rows.push(['Permissions', data.permissions]);
      if (data.encoding) rows.push(['Encoding', data.encoding]);

      let html = this.renderInfoSection('File', rows);

      if (data.git) {
        const gitRows = [['Status', data.git.status]];
        if (data.git.branch) gitRows.push(['Branch', data.git.branch]);
        if (data.git.lastCommit) {
          gitRows.push(['Last Commit', data.git.lastCommit.hash.substring(0, 8)]);
          gitRows.push(['Author', data.git.lastCommit.author]);
          gitRows.push(['Date', new Date(data.git.lastCommit.date).toLocaleString()]);
          gitRows.push(['Message', data.git.lastCommit.subject]);
        }
        html += this.renderInfoSection('Git', gitRows);
      }

      if (data.uuids && data.uuids.length > 0) {
        const uuidRows = data.uuids.map((uuid, i) => [`UUID ${data.uuids.length > 1 ? i + 1 : ''}`.trim(), uuid]);
        html += this.renderInfoSection('UUIDs Found', uuidRows);
      }

      if (data.exif) {
        const exifLabels = {
          width: 'Width', height: 'Height',
          cameraMake: 'Camera Make', cameraModel: 'Camera Model',
          dateTaken: 'Date Taken', exposureTime: 'Exposure',
          fNumber: 'Aperture', iso: 'ISO',
          focalLength: 'Focal Length',
          gpsLatitude: 'GPS Lat', gpsLongitude: 'GPS Lon',
          software: 'Software', copyright: 'Copyright',
          description: 'Description',
        };
        const exifRows = Object.entries(data.exif)
          .filter(([, v]) => v != null)
          .map(([key, value]) => {
            const label = exifLabels[key] || key;
            if (key === 'dateTaken') value = new Date(value).toLocaleString();
            if (key === 'width' || key === 'height') value = `${value}px`;
            return [label, value];
          });
        if (exifRows.length > 0) {
          html += this.renderInfoSection('EXIF Data', exifRows);
        }
      }

      body.innerHTML = html;
    } catch (error) {
      body.innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
    }
  }

  renderInfoSection(title, rows) {
    const header = `<div class="file-info-section-header">${escapeHtml(title)}</div>`;
    const rowsHtml = rows.map(([label, value]) =>
      `<div class="file-info-row">
        <span class="file-info-label">${escapeHtml(String(label))}</span>
        <span class="file-info-value">${escapeHtml(String(value))}</span>
      </div>`
    ).join('');
    return header + rowsHtml;
  }

  hideFileInfo() {
    document.getElementById('file-info-modal').style.display = 'none';
  }

  formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const units = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return parseFloat((bytes / Math.pow(1024, i)).toFixed(1)) + ' ' + units[i];
  }

  showLoading(show) {
    document.getElementById('loading').style.display = show ? 'flex' : 'none';
  }

  showError(message) {
    document.getElementById('preview-content').innerHTML = `<div class="error">${message}</div>`;
  }
}

document.addEventListener('DOMContentLoaded', () => new QuickViewApp());
