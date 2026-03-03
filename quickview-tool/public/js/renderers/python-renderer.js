import { escapeHtml } from '../utils.js';

export function renderPythonPreview(container, content, filename) {
  container.innerHTML = `
    <div style="padding: 20px; color: #333;">
      <h3>Python Script: ${filename}</h3>
      <p>Click "Run" to execute this Python script and see the output.</p>
      <div style="margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 6px;">
        <strong>Script Preview:</strong>
        <pre style="margin-top: 10px; overflow-x: auto;">${escapeHtml(content.substring(0, 500))}${content.length > 500 ? '...' : ''}</pre>
      </div>
    </div>
  `;
}
