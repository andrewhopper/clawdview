/**
 * RendererRegistry — central registry for QuickView preview pane renderers.
 *
 * Each renderer object must have:
 *   name       {string}   — unique identifier
 *   extensions {string[]} — file extensions this renderer handles (e.g. ['.json'])
 *                           Use ['*'] for a catch-all fallback.
 *   render     {function(container, content, extension, filename)} — renders into the given DOM node
 *
 * Optional:
 *   priority   {number}   — higher wins when multiple renderers claim the same extension (default 0)
 *   canRender  {function(content, extension, filename) → boolean} — fine-grained eligibility check
 *
 * Usage:
 *   RendererRegistry.register({ name: 'my-renderer', extensions: ['.foo'], render(container, content) { ... } });
 *   RendererRegistry.render(container, content, '.foo', 'file.foo');
 */
class RendererRegistry {
  constructor() {
    this._renderers = [];
  }

  /**
   * Register a renderer. Replaces any existing renderer with the same name.
   */
  register(renderer) {
    if (!renderer.name || !renderer.extensions || typeof renderer.render !== 'function') {
      throw new Error(
        '[RendererRegistry] Renderer must have: name (string), extensions (string[]), render (function)'
      );
    }

    // Replace existing renderer with the same name
    this._renderers = this._renderers.filter(r => r.name !== renderer.name);
    this._renderers.push(renderer);

    // Maintain priority order (descending — highest first)
    this._renderers.sort((a, b) => (b.priority || 0) - (a.priority || 0));
    console.log(`[RendererRegistry] Registered renderer: "${renderer.name}" for ${renderer.extensions.join(', ')}`);
  }

  /**
   * Find the best renderer for a given extension and content.
   */
  getRenderer(extension, content, filename) {
    for (const r of this._renderers) {
      // Skip catch-all renderers if a specific one exists for this extension
      if (r.extensions.includes('*')) {
        if (extension && this._hasSpecificRenderer(extension)) continue;
      } else {
        if (!r.extensions.includes(extension)) continue;
      }
      // Optional fine-grained check
      if (typeof r.canRender === 'function' && !r.canRender(content, extension, filename)) continue;
      return r;
    }
    return null;
  }

  _hasSpecificRenderer(extension) {
    return this._renderers.some(
      r => !r.extensions.includes('*') && r.extensions.includes(extension)
    );
  }

  /**
   * Render content into container using the best available renderer.
   */
  render(container, content, extension, filename) {
    const renderer = this.getRenderer(extension, content, filename);
    if (renderer) {
      try {
        renderer.render(container, content, extension, filename);
      } catch (err) {
        console.error(`[RendererRegistry] Renderer "${renderer.name}" threw:`, err);
        this._renderError(container, `Render error in "${renderer.name}": ${err.message}`);
      }
    } else {
      this._renderFallback(container, content);
    }
  }

  _renderError(container, message) {
    container.innerHTML = `<div class="error"><strong>Render error:</strong> ${this._escapeHtml(message)}</div>`;
  }

  _renderFallback(container, content) {
    container.innerHTML = `
      <div style="padding:20px;">
        <pre style="white-space:pre-wrap;font-family:monospace;">${this._escapeHtml(content)}</pre>
      </div>`;
  }

  _escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = String(text);
    return d.innerHTML;
  }

  /**
   * Returns a summary of all registered renderers (useful for debugging).
   */
  list() {
    return this._renderers.map(r => ({
      name: r.name,
      extensions: r.extensions,
      priority: r.priority || 0
    }));
  }
}

// Expose a single global instance
window.RendererRegistry = new RendererRegistry();
