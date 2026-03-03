/**
 * HTML Renderer — renders .html files in a sandboxed iframe.
 */
RendererRegistry.register({
  name: 'html',
  extensions: ['.html'],
  priority: 10,

  render(container, content) {
    const iframe = document.createElement('iframe');
    iframe.className = 'preview-iframe';
    iframe.srcdoc = content;
    container.innerHTML = '';
    container.appendChild(iframe);
  }
});
