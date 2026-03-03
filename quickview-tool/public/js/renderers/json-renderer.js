import { escapeHtml } from '../utils.js';

export function renderJSON(container, content) {
  try {
    const formatted = JSON.stringify(JSON.parse(content), null, 2);
    container.innerHTML = `
      <div style="padding: 20px; color: #333;">
        <pre style="background: #f5f5f5; padding: 15px; border-radius: 6px; overflow-x: auto;">${escapeHtml(formatted)}</pre>
      </div>
    `;
  } catch (error) {
    container.innerHTML = `<div class="error">Invalid JSON: ${error.message}</div>`;
  }
}
