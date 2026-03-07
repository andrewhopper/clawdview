import { escapeHtml } from '../utils.js';

export function renderJSON(container, content) {
  try {
    const formatted = JSON.stringify(JSON.parse(content), null, 2);
    container.innerHTML = `
      <div class="preview-text">
        <pre>${escapeHtml(formatted)}</pre>
      </div>
    `;
  } catch (error) {
    container.innerHTML = `<div class="error">Invalid JSON: ${error.message}</div>`;
  }
}
