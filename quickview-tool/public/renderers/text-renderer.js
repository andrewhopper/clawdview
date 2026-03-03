/**
 * Text Renderer — catch-all fallback renderer for unsupported or plain-text files.
 * Uses priority 0 so it's always last in the priority queue.
 */
RendererRegistry.register({
  name: 'text',
  extensions: ['*'],
  priority: 0,

  render(container, content) {
    const d = document.createElement('div');
    d.textContent = content;
    container.innerHTML = `
      <div style="padding:20px;min-height:100%;box-sizing:border-box;">
        <pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.875rem;margin:0;">${d.innerHTML}</pre>
      </div>`;
  }
});
