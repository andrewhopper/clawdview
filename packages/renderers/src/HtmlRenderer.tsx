import type { CSSProperties } from 'react';

export interface HtmlRendererProps {
  content: string;
  className?: string;
  style?: CSSProperties;
  title?: string;
  /**
   * iframe sandbox attribute. Default keeps scripts enabled so artifacts behave
   * as in the original ClawdView preview. Tighten this when rendering untrusted
   * content in a chat (e.g. "" for fully sandboxed, no-scripts).
   */
  sandbox?: string;
}

const DEFAULT_STYLE: CSSProperties = {
  width: '100%',
  height: '100%',
  border: 'none',
  background: '#fff',
};

export function HtmlRenderer({
  content,
  className,
  style,
  title = 'HTML Preview',
  sandbox,
}: HtmlRendererProps) {
  return (
    <iframe
      className={className}
      style={{ ...DEFAULT_STYLE, ...style }}
      srcDoc={content}
      title={title}
      sandbox={sandbox}
    />
  );
}
