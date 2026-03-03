/**
 * YAML Renderer — displays YAML files with syntax highlighting.
 * Uses highlight.js for colouring if available.
 */
RendererRegistry.register({
  name: 'yaml',
  extensions: ['.yaml', '.yml'],
  priority: 10,

  render(container, content) {
    container.innerHTML = '';
    const wrapper = document.createElement('div');
    wrapper.style.cssText = 'padding:20px;min-height:100%;box-sizing:border-box;';

    const pre = document.createElement('pre');
    pre.style.cssText = 'margin:0;border-radius:6px;overflow-x:auto;';

    if (window.hljs) {
      const code = document.createElement('code');
      code.className = 'language-yaml';
      code.textContent = content;
      pre.appendChild(code);
      wrapper.appendChild(pre);
      container.appendChild(wrapper);
      hljs.highlightElement(code);
    } else {
      const code = document.createElement('code');
      code.style.cssText = 'font-family:monospace;font-size:0.875rem;white-space:pre;';
      code.textContent = content;
      pre.appendChild(code);
      wrapper.appendChild(pre);
      container.appendChild(wrapper);
    }
  }
});
