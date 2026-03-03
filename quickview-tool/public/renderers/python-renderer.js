/**
 * Python Renderer — shows a preview of Python scripts with a "Run" prompt.
 * Actual execution is triggered by the toolbar "Run" button in app.js.
 */
RendererRegistry.register({
  name: 'python',
  extensions: ['.py'],
  priority: 10,

  render(container, content, extension, filename) {
    const preview = content.length > 600 ? content.substring(0, 600) + '\n...' : content;
    const lines = content.split('\n').length;
    const docstring = this._extractDocstring(content);

    container.innerHTML = `
      <div style="padding:20px;color:hsl(var(--foreground, #333));">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
          <span style="font-size:1.5rem;">🐍</span>
          <div>
            <h3 style="margin:0;font-size:0.9375rem;font-weight:600;">${this._escapeHtml(filename)}</h3>
            <span style="font-size:0.75rem;color:#888;">${lines} lines</span>
          </div>
        </div>
        ${docstring ? `<div style="padding:10px 14px;background:rgba(99,102,241,0.08);border-left:3px solid #6366f1;border-radius:4px;margin-bottom:14px;font-size:0.8125rem;color:#aaa;">${this._escapeHtml(docstring)}</div>` : ''}
        <p style="margin:0 0 14px;font-size:0.875rem;color:#888;">
          Click <strong style="color:hsl(var(--foreground,#eee));">▶ Run</strong> in the toolbar to execute this script.
        </p>
        <div style="background:hsl(220,13%,8%);border:1px solid hsl(240,3.7%,15.9%);border-radius:6px;padding:16px;overflow-x:auto;">
          <div style="font-size:0.6875rem;text-transform:uppercase;letter-spacing:.06em;color:#555;margin-bottom:8px;">Script preview</div>
          <pre style="margin:0;font-family:'JetBrains Mono',monospace;font-size:0.8125rem;color:#c9d1d9;white-space:pre;">${this._escapeHtml(preview)}</pre>
        </div>
      </div>`;
  },

  _extractDocstring(content) {
    const match = content.match(/^(?:[\s\S]*?def\s+\w+[^)]*\):\s*\n\s*)?"""([\s\S]*?)"""/);
    return match ? match[1].trim() : null;
  },

  _escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = String(text);
    return d.innerHTML;
  }
});
