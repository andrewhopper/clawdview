export function renderReact(container, content) {
  try {
    const wrapper = document.createElement('div');
    wrapper.id = 'react-preview';
    container.innerHTML = '';
    container.appendChild(wrapper);

    const transformed = Babel.transform(content, { presets: ['react'] }).code;

    const script = document.createElement('script');
    script.textContent = `
      try {
        ${transformed}
        const componentName = Object.keys(window).find(key =>
          typeof window[key] === 'function' && key[0] === key[0].toUpperCase()
        );
        if (componentName) {
          const Component = window[componentName];
          ReactDOM.render(React.createElement(Component), document.getElementById('react-preview'));
        }
      } catch (error) {
        document.getElementById('react-preview').innerHTML =
          '<div class="error">React Error: ' + error.message + '</div>';
      }
    `;

    document.head.appendChild(script);
    setTimeout(() => document.head.removeChild(script), 100);
  } catch (error) {
    container.innerHTML = `<div class="error">Failed to render React component: ${error.message}</div>`;
  }
}
