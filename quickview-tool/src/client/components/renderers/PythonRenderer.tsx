import { escapeHtml } from '@/lib/utils';

interface PythonRendererProps {
  content: string;
  filename: string;
}

export function PythonRenderer({ content, filename }: PythonRendererProps) {
  const preview = content.substring(0, 500) + (content.length > 500 ? '...' : '');

  return (
    <div className="p-5 text-foreground">
      <h3 className="text-lg font-semibold mb-2">Python Script: {filename}</h3>
      <p className="text-muted-foreground text-sm mb-5">
        Click &quot;Run&quot; to execute this Python script and see the output.
      </p>
      <div>
        <strong className="text-sm">Script Preview:</strong>
        <pre className="mt-2.5 p-4 bg-muted rounded-md text-sm font-mono overflow-x-auto">
          {preview}
        </pre>
      </div>
    </div>
  );
}
