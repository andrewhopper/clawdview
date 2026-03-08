const DEFAULT_PREFERENCES = {
  autoOpenOnChange: true,
  maxOpenTabs: 10,
  watchedFileTypes: [
    '.html', '.jsx', '.js', '.py', '.css', '.json',
    '.md', '.svg', '.txt', '.xml', '.yaml', '.yml'
  ]
};

const ALL_FILE_TYPES = [
  { ext: '.html', label: 'HTML', icon: '🌐' },
  { ext: '.jsx', label: 'React JSX', icon: '⚛️' },
  { ext: '.js', label: 'JavaScript', icon: '📜' },
  { ext: '.py', label: 'Python', icon: '🐍' },
  { ext: '.css', label: 'CSS', icon: '🎨' },
  { ext: '.json', label: 'JSON', icon: '📊' },
  { ext: '.md', label: 'Markdown', icon: '📝' },
  { ext: '.svg', label: 'SVG', icon: '🎨' },
  { ext: '.txt', label: 'Text', icon: '📄' },
  { ext: '.xml', label: 'XML', icon: '📄' },
  { ext: '.yaml', label: 'YAML', icon: '📄' },
  { ext: '.yml', label: 'YAML', icon: '📄' }
];

const STORAGE_KEY = 'quickview-preferences';

export class PreferencesManager {
  constructor(onChange) {
    this.onChange = onChange;
    this.preferences = this.load();
    this.panelEl = document.getElementById('preferences-panel');
    this.overlayEl = document.getElementById('preferences-overlay');
    this.setupPanel();
  }

  load() {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        return { ...DEFAULT_PREFERENCES, ...JSON.parse(stored) };
      }
    } catch (e) {
      console.error('Failed to load preferences:', e);
    }
    return { ...DEFAULT_PREFERENCES };
  }

  save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.preferences));
    } catch (e) {
      console.error('Failed to save preferences:', e);
    }
    if (this.onChange) this.onChange(this.preferences);
  }

  get(key) {
    return this.preferences[key];
  }

  set(key, value) {
    this.preferences[key] = value;
    this.save();
  }

  isFileTypeWatched(ext) {
    return this.preferences.watchedFileTypes.includes(ext);
  }

  setupPanel() {
    if (!this.panelEl) return;
    this.renderPanel();

    this.overlayEl.addEventListener('click', () => this.close());
    document.getElementById('prefs-close-btn').addEventListener('click', () => this.close());
  }

  open() {
    this.renderPanel();
    this.panelEl.classList.add('open');
    this.overlayEl.classList.add('open');
  }

  close() {
    this.panelEl.classList.remove('open');
    this.overlayEl.classList.remove('open');
  }

  toggle() {
    if (this.panelEl.classList.contains('open')) {
      this.close();
    } else {
      this.open();
    }
  }

  renderPanel() {
    const content = this.panelEl.querySelector('.prefs-content');
    if (!content) return;

    const fileTypeChecks = ALL_FILE_TYPES.map(ft => {
      const checked = this.preferences.watchedFileTypes.includes(ft.ext) ? 'checked' : '';
      return `
        <label class="prefs-file-type">
          <input type="checkbox" data-ext="${ft.ext}" ${checked}>
          <span class="prefs-file-type-icon">${ft.icon}</span>
          <span class="prefs-file-type-label">${ft.label}</span>
          <span class="prefs-file-type-ext">${ft.ext}</span>
        </label>`;
    }).join('');

    content.innerHTML = `
      <div class="prefs-section">
        <h4 class="prefs-section-title">General</h4>

        <label class="prefs-toggle">
          <span class="prefs-toggle-info">
            <span class="prefs-toggle-label">Auto-reload on file change</span>
            <span class="prefs-toggle-desc">Automatically reload the preview when the current file is modified externally</span>
          </span>
          <input type="checkbox" id="pref-auto-open" ${this.preferences.autoOpenOnChange ? 'checked' : ''}>
          <span class="prefs-switch"></span>
        </label>

        <div class="prefs-field">
          <label class="prefs-field-label" for="pref-max-tabs">Max open tabs</label>
          <span class="prefs-field-desc">Maximum number of file tabs that can be open simultaneously</span>
          <input type="number" id="pref-max-tabs" min="1" max="50" value="${this.preferences.maxOpenTabs}" class="prefs-input-number">
        </div>
      </div>

      <div class="prefs-section">
        <h4 class="prefs-section-title">Watched File Types</h4>
        <p class="prefs-section-desc">Select which file types appear in the file tree and trigger change notifications</p>
        <div class="prefs-file-types-actions">
          <button id="prefs-select-all" class="prefs-link-btn">Select All</button>
          <button id="prefs-select-none" class="prefs-link-btn">Select None</button>
        </div>
        <div class="prefs-file-types-grid">
          ${fileTypeChecks}
        </div>
      </div>

      <div class="prefs-section">
        <div class="prefs-actions">
          <button id="prefs-reset-btn" class="prefs-reset-btn">Reset to Defaults</button>
        </div>
      </div>
    `;

    this.bindEvents(content);
  }

  bindEvents(content) {
    content.querySelector('#pref-auto-open').addEventListener('change', (e) => {
      this.set('autoOpenOnChange', e.target.checked);
    });

    content.querySelector('#pref-max-tabs').addEventListener('change', (e) => {
      const val = parseInt(e.target.value, 10);
      if (val >= 1 && val <= 50) {
        this.set('maxOpenTabs', val);
      }
    });

    content.querySelectorAll('.prefs-file-type input[type="checkbox"]').forEach(cb => {
      cb.addEventListener('change', () => {
        const checked = content.querySelectorAll('.prefs-file-type input[type="checkbox"]:checked');
        this.set('watchedFileTypes', Array.from(checked).map(c => c.dataset.ext));
      });
    });

    content.querySelector('#prefs-select-all').addEventListener('click', () => {
      this.set('watchedFileTypes', ALL_FILE_TYPES.map(ft => ft.ext));
      this.renderPanel();
    });

    content.querySelector('#prefs-select-none').addEventListener('click', () => {
      this.set('watchedFileTypes', []);
      this.renderPanel();
    });

    content.querySelector('#prefs-reset-btn').addEventListener('click', () => {
      this.preferences = { ...DEFAULT_PREFERENCES };
      this.save();
      this.renderPanel();
    });
  }
}
