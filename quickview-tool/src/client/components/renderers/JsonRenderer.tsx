import { escapeHtml } from '@/lib/utils';

interface JsonRendererProps {
  content: string;
}

export function JsonRenderer({ content }: JsonRendererProps) {
  try {
    const formatted = JSON.stringify(JSON.parse(content), null, 2);
    return (
      <div className="p-5">
        <pre className="p-4 bg-muted rounded-md text-sm font-mono overflow-x-auto text-foreground">
          {formatted}
        </pre>
      </div>
    );
  } catch (error: any) {
    return (
      <div className="p-4 m-3 bg-destructive/10 text-destructive rounded-md border-l-3 border-destructive text-sm">
        Invalid JSON: {error.message}
      </div>
    );
  }
}
