import { useMemo } from 'react';

interface JsonRendererProps {
  content: string;
}

export function JsonRenderer({ content }: JsonRendererProps) {
  const { formatted, error } = useMemo(() => {
    try {
      return { formatted: JSON.stringify(JSON.parse(content), null, 2), error: null };
    } catch (e: any) {
      return { formatted: null, error: e.message };
    }
  }, [content]);

  if (error) {
    return (
      <div className="p-4 m-3 bg-destructive/10 text-destructive rounded-md border-l-3 border-destructive text-sm">
        Invalid JSON: {error}
      </div>
    );
  }

  return (
    <div className="p-5">
      <pre className="p-4 bg-muted rounded-md text-sm font-mono overflow-x-auto text-foreground">
        {formatted}
      </pre>
    </div>
  );
}
