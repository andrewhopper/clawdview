import type { CSSProperties } from 'react';
import { DrawioRenderer } from './DrawioRenderer';
import { HtmlRenderer } from './HtmlRenderer';
import { JsonRenderer } from './JsonRenderer';
import { MarkdownRenderer } from './MarkdownRenderer';
import { ReactRenderer } from './ReactRenderer';
import { SvgRenderer } from './SvgRenderer';
import { detectKindFromFilename } from './utils';

export type RendererKind =
  | 'html'
  | 'markdown'
  | 'svg'
  | 'json'
  | 'jsx'
  | 'drawio';

export interface RendererProps {
  content: string;
  /**
   * Explicit renderer kind. If omitted, `filename` is used for detection;
   * if both are omitted the content is shown as a preformatted block.
   */
  kind?: RendererKind;
  /**
   * Filename used to infer `kind` from extension when `kind` is not provided.
   */
  filename?: string;
  className?: string;
  style?: CSSProperties;
}

const FALLBACK_STYLE: CSSProperties = {
  padding: '1.25rem',
  fontFamily:
    'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace',
  fontSize: '0.875rem',
  whiteSpace: 'pre-wrap',
  margin: 0,
};

/**
 * Dispatches to the right renderer based on `kind` (explicit) or `filename`
 * (inferred). Falls back to a preformatted block.
 *
 * Use this when you want a single entry point — for example, rendering tool
 * outputs in a chat by passing the filename or extension along with content.
 */
export function Renderer({
  content,
  kind,
  filename,
  className,
  style,
}: RendererProps) {
  const resolved = kind ?? (detectKindFromFilename(filename) as RendererKind | null);

  switch (resolved) {
    case 'html':
      return <HtmlRenderer content={content} className={className} style={style} />;
    case 'markdown':
      return <MarkdownRenderer content={content} className={className} style={style} />;
    case 'svg':
      return <SvgRenderer content={content} className={className} style={style} />;
    case 'json':
      return <JsonRenderer content={content} className={className} style={style} />;
    case 'jsx':
      return <ReactRenderer content={content} className={className} style={style} />;
    case 'drawio':
      return <DrawioRenderer content={content} className={className} style={style} />;
    default:
      return (
        <pre className={className} style={{ ...FALLBACK_STYLE, ...style }}>
          {content}
        </pre>
      );
  }
}
