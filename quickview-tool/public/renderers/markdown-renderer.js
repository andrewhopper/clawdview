/**
 * Markdown Renderer — renders .md files with full GFM support.
 *
 * Uses marked.js for parsing (loaded via CDN).
 * Applies highlight.js syntax highlighting to fenced code blocks.
 * Detects ```mermaid code blocks and renders them as diagrams if Mermaid.js is available.
 */
RendererRegistry.register({
  name: 'markdown',
  extensions: ['.md'],
  priority: 10,

  render(container, content) {
    let html;

    if (window.marked) {
      // Configure marked with highlight.js integration
      const options = {
        breaks: true,
        gfm: true
      };

      if (window.hljs) {
        options.highlight = (code, lang) => {
          // Don't highlight mermaid blocks — we'll render them as diagrams
          if (lang === 'mermaid') return code;
          if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
          }
          return hljs.highlightAuto(code).value;
        };
      }

      marked.setOptions(options);
      html = marked.parse(content);
    } else {
      // Basic fallback if marked isn't available
      html = this._basicMarkdown(content);
    }

    container.innerHTML = '';
    const wrapper = document.createElement('div');
    wrapper.className = 'markdown-body';
    wrapper.innerHTML = html;
    container.appendChild(wrapper);

    // Convert ```mermaid blocks into rendered diagrams
    if (window.mermaid) {
      const mermaidBlocks = [];
      wrapper.querySelectorAll('pre > code.language-mermaid, code.language-mermaid').forEach(codeEl => {
        const diagramText = codeEl.textContent.trim();
        const diagramEl = document.createElement('div');
        diagramEl.className = 'mermaid';
        diagramEl.textContent = diagramText;

        const pre = codeEl.closest('pre');
        if (pre) {
          pre.replaceWith(diagramEl);
        } else {
          codeEl.replaceWith(diagramEl);
        }
        mermaidBlocks.push(diagramEl);
      });

      if (mermaidBlocks.length > 0) {
        try {
          if (typeof mermaid.run === 'function') {
            mermaid.run({ nodes: mermaidBlocks });
          } else {
            mermaid.init(undefined, mermaidBlocks);
          }
        } catch (err) {
          console.warn('[markdown-renderer] Mermaid render error:', err);
        }
      }
    }

    // Apply syntax highlighting to remaining code blocks
    if (window.hljs) {
      wrapper.querySelectorAll('pre code:not(.language-mermaid)').forEach(block => {
        hljs.highlightElement(block);
      });
    }
  },

  /** Minimal Markdown fallback (no marked.js) */
  _basicMarkdown(content) {
    const escaped = content
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    return escaped
      .replace(/^###### (.*$)/gim, '<h6>$1</h6>')
      .replace(/^##### (.*$)/gim, '<h5>$1</h5>')
      .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/\*\*([^*]+)\*\*/gim, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/gim, '<em>$1</em>')
      .replace(/`([^`]+)`/gim, '<code>$1</code>')
      .replace(/\n/gim, '<br>');
  }
});
