/**
 * JSON Renderer — renders JSON as an interactive, collapsible tree view.
 * Click the ▾/▸ toggle to expand or collapse objects and arrays.
 */
RendererRegistry.register({
  name: 'json',
  extensions: ['.json'],
  priority: 10,

  render(container, content) {
    let parsed;
    try {
      parsed = JSON.parse(content);
    } catch (err) {
      container.innerHTML = `<div class="error">Invalid JSON: ${this._escapeHtml(err.message)}</div>`;
      return;
    }

    container.innerHTML = '';
    const viewer = document.createElement('div');
    viewer.className = 'json-viewer';
    viewer.appendChild(this._buildNode(parsed, null, true));
    container.appendChild(viewer);
  },

  /**
   * Recursively build a DOM node for a JSON value.
   * @param {*} value — the JSON value
   * @param {string|number|null} key — the key for this value, or null if root
   * @param {boolean} isRoot — whether this is the top-level call
   */
  _buildNode(value, key, isRoot) {
    const type = value === null ? 'null' : Array.isArray(value) ? 'array' : typeof value;
    const row = document.createElement('div');
    row.className = 'jv-row';

    // Render the key label (skip for root)
    if (key !== null) {
      const keyEl = document.createElement('span');
      keyEl.className = 'jv-key';
      keyEl.textContent = JSON.stringify(key) + ': ';
      row.appendChild(keyEl);
    }

    if (type === 'null') {
      const val = document.createElement('span');
      val.className = 'jv-null';
      val.textContent = 'null';
      row.appendChild(val);
      return row;
    }

    if (type === 'object' || type === 'array') {
      const entries = type === 'array'
        ? value.map((v, i) => [i, v])
        : Object.entries(value);
      const count = entries.length;
      const brackets = type === 'array' ? ['[', ']'] : ['{', '}'];

      // Build summary for collapsed state
      const previewKeys = type === 'array'
        ? `Array(${count})`
        : `{ ${Object.keys(value).slice(0, 3).map(k => JSON.stringify(k)).join(', ')}${count > 3 ? ', …' : ''} }`;

      const toggle = document.createElement('span');
      toggle.className = 'jv-toggle';
      toggle.textContent = '▾';
      toggle.title = 'Click to collapse/expand';

      const openBracket = document.createElement('span');
      openBracket.className = 'jv-bracket';
      openBracket.textContent = brackets[0];

      const summary = document.createElement('span');
      summary.className = 'jv-summary';
      summary.textContent = ' ' + previewKeys;
      summary.style.display = 'none';

      const children = document.createElement('div');
      children.className = 'jv-children';

      entries.forEach(([k, v]) => {
        children.appendChild(this._buildNode(v, k, false));
      });

      const closeRow = document.createElement('div');
      closeRow.className = 'jv-row jv-close-row';
      const closeBracket = document.createElement('span');
      closeBracket.className = 'jv-bracket';
      closeBracket.textContent = brackets[1];
      closeRow.appendChild(closeBracket);

      // Count badge
      const badge = document.createElement('span');
      badge.className = 'jv-count';
      badge.textContent = ` // ${count} ${type === 'array' ? 'item' : 'key'}${count !== 1 ? 's' : ''}`;
      openBracket.appendChild(badge);

      toggle.addEventListener('click', () => {
        const isCollapsed = children.style.display === 'none';
        children.style.display = isCollapsed ? '' : 'none';
        closeRow.style.display = isCollapsed ? '' : 'none';
        summary.style.display = isCollapsed ? 'none' : '';
        toggle.textContent = isCollapsed ? '▾' : '▸';
      });

      row.appendChild(toggle);
      row.appendChild(openBracket);
      row.appendChild(summary);
      row.appendChild(children);
      row.appendChild(closeRow);
    } else {
      // Primitive value
      const val = document.createElement('span');
      val.className = `jv-${type}`;
      val.textContent = JSON.stringify(value);
      row.appendChild(val);
    }

    return row;
  },

  _escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = String(text);
    return d.innerHTML;
  }
});
