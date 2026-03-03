/**
 * React/JSX Renderer — transpiles JSX with Babel and renders the component.
 */
RendererRegistry.register({
  name: 'react',
  extensions: ['.jsx'],
  priority: 10,

  render(container, content) {
    if (!window.Babel || !window.React || !window.ReactDOM) {
      container.innerHTML = '<div class="error">React or Babel is not loaded — cannot render JSX.</div>';
      return;
    }

    const wrapperId = 'react-preview-' + Date.now();
    const wrapper = document.createElement('div');
    wrapper.id = wrapperId;
    wrapper.style.cssText = 'height:100%;padding:20px;';
    container.innerHTML = '';
    container.appendChild(wrapper);

    let transformed;
    try {
      transformed = Babel.transform(content, { presets: ['react'] }).code;
    } catch (err) {
      container.innerHTML = `<div class="error">JSX transform error: ${this._escapeHtml(err.message)}</div>`;
      return;
    }

    const script = document.createElement('script');
    script.textContent = `
      (function() {
        try {
          ${transformed}
          // Find a React component (function/class starting with uppercase)
          const EXCLUDED = new Set(['Array','Boolean','Date','Error','Function',
            'JSON','Math','Number','Object','RegExp','String','Symbol','Promise']);
          const name = Object.keys(window).find(k =>
            /^[A-Z]/.test(k) &&
            !EXCLUDED.has(k) &&
            typeof window[k] === 'function'
          );
          if (name) {
            ReactDOM.render(
              React.createElement(window[name]),
              document.getElementById('${wrapperId}')
            );
          } else {
            document.getElementById('${wrapperId}').innerHTML =
              '<div class="error">No React component found. Export a function/class that starts with an uppercase letter.</div>';
          }
        } catch (e) {
          const el = document.getElementById('${wrapperId}');
          if (el) el.innerHTML = '<div class="error">React render error: ' + e.message + '</div>';
        }
      })();
    `;
    document.head.appendChild(script);
    setTimeout(() => {
      if (script.parentNode) script.parentNode.removeChild(script);
    }, 200);
  },

  _escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = String(text);
    return d.innerHTML;
  }
});
