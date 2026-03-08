import { useEffect, useRef } from 'react';

declare const Babel: any;

interface ReactRendererProps {
  content: string;
}

export function ReactRenderer({ content }: ReactRendererProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    try {
      const transformed = Babel.transform(content, { presets: ['react'] }).code;

      const wrapper = document.createElement('div');
      wrapper.id = 'react-preview';
      containerRef.current.innerHTML = '';
      containerRef.current.appendChild(wrapper);

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
            '<div class="text-destructive p-4">React Error: ' + error.message + '</div>';
        }
      `;

      document.head.appendChild(script);
      setTimeout(() => document.head.removeChild(script), 100);
    } catch (error: any) {
      if (containerRef.current) {
        containerRef.current.innerHTML = `<div class="text-destructive p-4">Failed to render React component: ${error.message}</div>`;
      }
    }
  }, [content]);

  return <div ref={containerRef} className="h-full" />;
}
