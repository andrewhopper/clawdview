/**
 * Mermaid Renderer — renders Mermaid diagram syntax (.mmd / .mermaid files).
 *
 * Requires Mermaid.js to be loaded before this script.
 * For Mermaid diagrams inside Markdown files, see markdown-renderer.js.
 */
RendererRegistry.register({
  name: 'mermaid',
  extensions: ['.mmd', '.mermaid'],
  priority: 10,

  render(container, content) {
    if (!window.mermaid) {
      container.innerHTML = '<div class="error">Mermaid.js is not loaded — cannot render diagram.</div>';
      return;
    }

    container.innerHTML = '';
    const wrapper = document.createElement('div');
    wrapper.style.cssText = [
      'padding:20px',
      'background:white',
      'min-height:100%',
      'display:flex',
      'justify-content:center',
      'align-items:flex-start',
      'box-sizing:border-box'
    ].join(';');

    const diagramEl = document.createElement('div');
    diagramEl.className = 'mermaid';
    diagramEl.textContent = content.trim();
    wrapper.appendChild(diagramEl);
    container.appendChild(wrapper);

    // mermaid.run() is the modern API (v10+); fall back to mermaid.init() for older versions
    try {
      if (typeof mermaid.run === 'function') {
        mermaid.run({ nodes: [diagramEl] });
      } else {
        mermaid.init(undefined, diagramEl);
      }
    } catch (err) {
      container.innerHTML = `<div class="error">Mermaid render error: ${this._escapeHtml(err.message)}</div>`;
    }
  },

  _escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = String(text);
    return d.innerHTML;
  }
});
