import { useState, useCallback, useRef, useEffect } from 'react';
import { Header } from './components/Header';
import { FileTree } from './components/FileTree';
import { PreferencesPanel } from './components/PreferencesPanel';
import { FileInfoModal } from './components/FileInfoModal';
import { HtmlRenderer } from './components/renderers/HtmlRenderer';
import { ReactRenderer } from './components/renderers/ReactRenderer';
import { PythonRenderer } from './components/renderers/PythonRenderer';
import { SvgRenderer } from './components/renderers/SvgRenderer';
import { MarkdownRenderer } from './components/renderers/MarkdownRenderer';
import { JsonRenderer } from './components/renderers/JsonRenderer';
import { useSocket } from './hooks/useSocket';
import { usePreferences } from './hooks/usePreferences';
import { useTheme } from './hooks/useTheme';
import { escapeHtml } from './lib/utils';
import { cn } from './lib/utils';
import type { FileTreeItem, FileData, CurrentFile, TabName } from './types';

declare const hljs: any;

const HIGHLIGHT_LANG_MAP: Record<string, string> = {
  '.js': 'javascript', '.jsx': 'javascript', '.py': 'python',
  '.html': 'html', '.css': 'css', '.json': 'json',
  '.md': 'markdown', '.svg': 'xml',
};

const FORMATTABLE_EXTENSIONS = ['.js', '.jsx', '.json', '.html', '.css'];

export function App() {
  const [fileTree, setFileTree] = useState<FileTreeItem[]>([]);
  const [currentFile, setCurrentFile] = useState<CurrentFile | null>(null);
  const [fileContent, setFileContent] = useState<string>('');
  const [fileExtension, setFileExtension] = useState<string>('');
  const [activeTab, setActiveTab] = useState<TabName>('preview');
  const [outputContent, setOutputContent] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [prefsOpen, setPrefsOpen] = useState(false);
  const [fileInfoOpen, setFileInfoOpen] = useState(false);
  const [selectedPath, setSelectedPath] = useState<string | null>(null);

  const codeRef = useRef<HTMLElement>(null);
  const currentFileRef = useRef(currentFile);
  currentFileRef.current = currentFile;

  const { isDark, toggleTheme } = useTheme();
  const { preferences, updatePreference, resetPreferences, isFileTypeWatched } = usePreferences();

  const onFileTree = useCallback((tree: FileTreeItem[]) => {
    setFileTree(tree);
  }, []);

  const onFileChange = useCallback((data: { relativePath: string }) => {
    if (
      preferences.autoOpenOnChange &&
      currentFileRef.current &&
      data.relativePath === currentFileRef.current.path
    ) {
      loadFile(currentFileRef.current);
    }
  }, [preferences.autoOpenOnChange]);

  const { connected, requestRefresh } = useSocket(onFileTree, onFileChange);

  const loadFile = useCallback(async (file: CurrentFile | FileTreeItem) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/file/${file.path}`);
      const data: FileData = await response.json();
      if (!response.ok) throw new Error((data as any).error || 'Failed to load file');

      const current: CurrentFile = {
        name: file.name,
        path: file.path,
        extension: data.extension,
      };
      setCurrentFile(current);
      setSelectedPath(file.path);
      setFileContent(data.content);
      setFileExtension(data.extension);
    } catch (error: any) {
      setFileContent('');
      setFileExtension('');
    } finally {
      setLoading(false);
    }
  }, []);

  // Highlight code when content or tab changes
  useEffect(() => {
    if (activeTab === 'code' && codeRef.current && fileContent && typeof hljs !== 'undefined') {
      const language = HIGHLIGHT_LANG_MAP[fileExtension];
      codeRef.current.textContent = fileContent;
      if (language) {
        codeRef.current.className = `language-${language}`;
        hljs.highlightElement(codeRef.current);
      }
    }
  }, [activeTab, fileContent, fileExtension]);

  const runCode = useCallback(async () => {
    if (!currentFile || currentFile.extension !== '.py') return;
    setLoading(true);
    try {
      const fileResponse = await fetch(`/api/file/${currentFile.path}`);
      const fileData = await fileResponse.json();

      const execResponse = await fetch('/api/execute/python', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: fileData.content, filename: currentFile.name }),
      });
      const result = await execResponse.json();
      setActiveTab('output');

      if (result.success) {
        setOutputContent(`<div class="p-3.5 m-3 bg-green-500/10 text-green-700 dark:text-green-400 rounded-md border-l-3 border-green-500 text-sm"><strong>Execution completed successfully</strong><pre class="mt-2 p-2.5 bg-green-500/10 rounded-sm text-[13px] font-mono overflow-x-auto">${escapeHtml(result.output || 'No output')}</pre></div>`);
      } else {
        setOutputContent(`<div class="p-3.5 m-3 bg-destructive/10 text-red-700 dark:text-red-400 rounded-md border-l-3 border-destructive text-sm"><strong>Execution failed</strong><pre class="mt-2 p-2.5 bg-destructive/10 rounded-sm text-[13px] font-mono overflow-x-auto">${escapeHtml(result.error || 'Unknown error')}</pre></div>`);
      }
    } catch (error: any) {
      setOutputContent(`<div class="p-4 m-3 text-destructive">Failed to execute: ${escapeHtml(error.message)}</div>`);
    } finally {
      setLoading(false);
    }
  }, [currentFile]);

  const formatCode = useCallback(async () => {
    if (!currentFile) return;
    setLoading(true);
    try {
      const response = await fetch('/api/format', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filepath: currentFile.path, extension: currentFile.extension }),
      });
      const result = await response.json();
      if (result.success) {
        loadFile(currentFile);
      }
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }, [currentFile, loadFile]);

  const openExternal = useCallback(() => {
    if (currentFile?.extension === '.html') {
      window.open(`/preview/${currentFile.path}`, '_blank');
    }
  }, [currentFile]);

  // Keyboard shortcuts for tabs
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) {
        e.preventDefault();
        const tabs: TabName[] = ['preview', 'code', 'output'];
        const idx = tabs.indexOf(activeTab);
        const next = e.key === 'ArrowRight'
          ? tabs[(idx + 1) % tabs.length]
          : tabs[(idx - 1 + tabs.length) % tabs.length];
        setActiveTab(next);
      }
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [activeTab]);

  const renderPreview = () => {
    if (!fileContent) {
      return (
        <div className="px-10 py-16 text-center text-muted-foreground">
          <h2 className="text-2xl font-semibold text-foreground mb-3">Welcome to QuickView!</h2>
          <p className="text-muted-foreground text-sm">Select a file from the sidebar to start previewing</p>
          <div className="mt-8 text-left max-w-xs mx-auto">
            <h3 className="text-xs font-medium uppercase tracking-wider text-muted-foreground mb-3">Supported formats</h3>
            <ul className="space-y-2">
              <li className="text-sm text-muted-foreground">🌐 HTML/CSS/JavaScript</li>
              <li className="text-sm text-muted-foreground">⚛️ React Components (JSX)</li>
              <li className="text-sm text-muted-foreground">🐍 Python Scripts</li>
              <li className="text-sm text-muted-foreground">🎨 SVG Graphics</li>
              <li className="text-sm text-muted-foreground">📝 Markdown</li>
              <li className="text-sm text-muted-foreground">📊 JSON/YAML</li>
            </ul>
          </div>
        </div>
      );
    }

    switch (fileExtension) {
      case '.html': return <HtmlRenderer content={fileContent} />;
      case '.jsx': return <ReactRenderer content={fileContent} />;
      case '.py': return <PythonRenderer content={fileContent} filename={currentFile?.name || ''} />;
      case '.svg': return <SvgRenderer content={fileContent} />;
      case '.md': return <MarkdownRenderer content={fileContent} />;
      case '.json': return <JsonRenderer content={fileContent} />;
      default: return (
        <div className="p-5">
          <pre className="whitespace-pre-wrap text-foreground text-sm font-mono">{fileContent}</pre>
        </div>
      );
    }
  };

  const tabs: { name: TabName; label: string; icon: string }[] = [
    { name: 'preview', label: 'Preview', icon: '🖥️' },
    { name: 'code', label: 'Code', icon: '📝' },
    { name: 'output', label: 'Output', icon: '📊' },
  ];

  return (
    <div className="flex flex-col h-screen">
      <Header
        currentFileName={currentFile?.name || ''}
        connected={connected}
        isDark={isDark}
        onToggleTheme={toggleTheme}
        onOpenSettings={() => setPrefsOpen(true)}
      />

      <div className="flex flex-1 overflow-hidden min-h-0">
        <FileTree
          tree={fileTree}
          selectedPath={selectedPath}
          onFileSelect={loadFile}
          onRefresh={requestRefresh}
          isFileTypeWatched={isFileTypeWatched}
        />

        <div className="flex-1 flex flex-col overflow-hidden min-w-0">
          {/* Tab bar */}
          <div className="flex bg-card border-b border-border shrink-0">
            {tabs.map((tab) => (
              <button
                key={tab.name}
                onClick={() => setActiveTab(tab.name)}
                className={cn(
                  'bg-transparent border-none text-muted-foreground py-2.5 px-4.5 cursor-pointer text-sm border-b-2 border-b-transparent transition-colors hover:text-foreground hover:bg-accent',
                  activeTab === tab.name && 'text-foreground border-b-primary',
                )}
              >
                {tab.icon} {tab.label}
              </button>
            ))}
          </div>

          {/* Panel content */}
          <div className="flex-1 relative overflow-hidden">
            {/* Preview */}
            <div className={cn('absolute inset-0 overflow-auto', activeTab !== 'preview' && 'hidden')}>
              <div className="h-full bg-background">
                {renderPreview()}
              </div>
            </div>

            {/* Code */}
            <div className={cn('absolute inset-0 overflow-auto', activeTab !== 'code' && 'hidden')}>
              <pre className="min-h-full">
                <code
                  ref={codeRef}
                  className="block bg-background text-foreground p-5 font-mono text-sm leading-relaxed min-h-full overflow-auto whitespace-pre"
                />
              </pre>
            </div>

            {/* Output */}
            <div className={cn('absolute inset-0 overflow-auto', activeTab !== 'output' && 'hidden')}>
              <div className="bg-background text-green-600 dark:text-green-400 font-mono text-sm leading-relaxed p-5 min-h-full">
                {outputContent ? (
                  <div dangerouslySetInnerHTML={{ __html: outputContent }} />
                ) : (
                  <div className="text-muted-foreground text-center mt-12 text-sm">
                    Script output will appear here...
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Action buttons */}
          <div className="bg-card border-t border-border px-4 py-2 flex gap-2 shrink-0">
            {currentFile?.extension === '.py' && (
              <button onClick={runCode} className="bg-secondary text-secondary-foreground border border-border px-3.5 py-1 rounded-md cursor-pointer text-[13px] font-medium transition-colors hover:bg-accent">
                ▶️ Run
              </button>
            )}
            {currentFile && FORMATTABLE_EXTENSIONS.includes(currentFile.extension) && (
              <button onClick={formatCode} className="bg-secondary text-secondary-foreground border border-border px-3.5 py-1 rounded-md cursor-pointer text-[13px] font-medium transition-colors hover:bg-accent">
                ✨ Format
              </button>
            )}
            {currentFile?.extension === '.html' && (
              <button onClick={openExternal} className="bg-secondary text-secondary-foreground border border-border px-3.5 py-1 rounded-md cursor-pointer text-[13px] font-medium transition-colors hover:bg-accent">
                🔗 Open External
              </button>
            )}
            {currentFile && (
              <button onClick={() => setFileInfoOpen(true)} className="bg-secondary text-secondary-foreground border border-border px-3.5 py-1 rounded-md cursor-pointer text-[13px] font-medium transition-colors hover:bg-accent">
                ℹ️ Info
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Loading overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black/80 flex flex-col justify-center items-center z-50">
          <div className="w-8 h-8 border-2 border-border border-t-primary rounded-full animate-spin" />
          <p className="text-sm text-foreground mt-4">Processing...</p>
        </div>
      )}

      <PreferencesPanel
        isOpen={prefsOpen}
        preferences={preferences}
        onClose={() => setPrefsOpen(false)}
        onUpdatePreference={updatePreference}
        onReset={resetPreferences}
      />

      <FileInfoModal
        file={currentFile}
        isOpen={fileInfoOpen}
        onClose={() => setFileInfoOpen(false)}
      />
    </div>
  );
}
