/**
 * SVG Renderer — inlines SVG content with a white centred background.
 */
RendererRegistry.register({
  name: 'svg',
  extensions: ['.svg'],
  priority: 10,

  render(container, content) {
    // Sanitise: strip <script> tags before inlining
    const safe = content.replace(/<script[\s\S]*?<\/script>/gi, '');
    container.innerHTML = `
      <div style="padding:20px;text-align:center;background:white;min-height:100%;box-sizing:border-box;">
        ${safe}
      </div>`;
  }
});
