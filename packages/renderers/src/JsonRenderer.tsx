import { useMemo, type CSSProperties } from 'react';

export interface JsonRendererProps {
  content: string;
  className?: string;
  style?: CSSProperties;
  indent?: number;
}

const WRAPPER_STYLE: CSSProperties = {
  padding: '1.25rem',
};

const PRE_STYLE: CSSProperties = {
  padding: '1rem',
  borderRadius: '0.375rem',
  fontFamily:
    'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace',
  fontSize: '0.875rem',
  overflowX: 'auto',
  background: 'rgba(127, 127, 127, 0.12)',
  margin: 0,
};

const ERROR_STYLE: CSSProperties = {
  padding: '1rem',
  margin: '0.75rem',
  borderLeft: '3px solid #ef4444',
  background: 'rgba(239, 68, 68, 0.1)',
  color: '#ef4444',
  borderRadius: '0.375rem',
  fontSize: '0.875rem',
};

export function JsonRenderer({
  content,
  className,
  style,
  indent = 2,
}: JsonRendererProps) {
  const { formatted, error } = useMemo(() => {
    try {
      return {
        formatted: JSON.stringify(JSON.parse(content), null, indent),
        error: null as string | null,
      };
    } catch (e) {
      return { formatted: null, error: (e as Error).message };
    }
  }, [content, indent]);

  if (error !== null) {
    return (
      <div className={className} style={{ ...ERROR_STYLE, ...style }}>
        Invalid JSON: {error}
      </div>
    );
  }

  return (
    <div className={className} style={{ ...WRAPPER_STYLE, ...style }}>
      <pre style={PRE_STYLE}>{formatted}</pre>
    </div>
  );
}
