import { useState, useCallback, useRef, useEffect, useMemo } from 'react';
import { Play, Sparkles, ExternalLink, Info } from 'lucide-react';
import { Header } from './components/Header';
import { FileTree } from './components/FileTree';
import { PreferencesPanel } from './components/PreferencesPanel';
import { FileInfoModal } from './components/FileInfoModal';
import { CommandPalette } from './components/CommandPalette';
import { HtmlRenderer } from './components/renderers/HtmlRenderer';
import { ReactRenderer } from './components/renderers/ReactRenderer';
import { PythonRenderer } from './components/renderers/PythonRenderer';
import { SvgRenderer } from './components/renderers/SvgRenderer';
import { MarkdownRenderer } from './components/renderers/MarkdownRenderer';
import { JsonRenderer } from './components/renderers/JsonRenderer';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './components/ui/tabs';
import { Button } from './components/ui/button';
import { Separator } from './components/ui/separator';
import { TooltipProvider } from './components/ui/tooltip';
import { useSocket } from './hooks/useSocket';
import { usePreferences } from './hooks/usePreferences';
import { useTheme } from './hooks/useTheme';
import { cn } from './lib/utils';
import type { FileTreeItem, FileData, CurrentFile, TabName } from './types';

declare const hljs: any;

const HIGHLIGHT_LANG_MAP: Record<string, string> = {
  '.js': 'javascript', '.jsx': 'javascript', '.py': 'python',
  '.html': 'html', '.css': 'css', '.json': 'json',
  '.md': 'markdown', '.svg': 'xml',
};

const FORMATTABLE_EXTENSIONS = ['.js', '.jsx', '.json', '.html', '.css'];

interface OutputResult {
  success: boolean;
  text: string;
}

export function App() {
  const [fileTree, setFileTree] = useState<FileTreeItem[]>([]);
  const [currentFile, setCurrentFile] = useState<CurrentFile | null>(null);
  const [fileContent, setFileContent] = useState<string>('');
  const [activeTab, setActiveTab] = useState<TabName>('preview');
  const [outputResult, setOutputResult] = useState<OutputResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [prefsOpen, setPrefsOpen] = useState(false);
  const [fileInfoOpen, setFileInfoOpen] = useState(false);
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);

  const codeRef = useRef<HTMLElement>(null);
  const currentFileRef = useRef(currentFile);
  currentFileRef.current = currentFile;
  const fileContentRef = useRef(fileContent);
  fileContentRef.current = fileContent;

  const fileExtension = currentFile?.extension || '';

  const { isDark, toggleTheme } = useTheme();
  const { preferences, updatePreference, resetPreferences, isFileTypeWatched } = usePreferences();

  const loadFile = useCallback(async (file: CurrentFile | FileTreeItem) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/file/${file.path}`);
      const data: FileData = await response.json();
      if (!response.ok) throw new Error((data as any).error || 'Failed to load file');

      setCurrentFile({ name: file.name, path: file.path, extension: data.extension });
      setFileContent(data.content);
    } catch {
      setFileContent('');
    } finally {
      setLoading(false);
    }
  }, []);

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
  }, [preferences.autoOpenOnChange, loadFile]);

  const { connected, requestRefresh } = useSocket(onFileTree, onFileChange);

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
      const execResponse = await fetch('/api/execute/python', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: fileContentRef.current, filename: currentFile.name }),
      });
      const result = await execResponse.json();
      setActiveTab('output');

      if (result.success) {
        setOutputResult({ success: true, text: result.output || 'No output' });
      } else {
        setOutputResult({ success: false, text: result.error || 'Unknown error' });
      }
    } catch (error: any) {
      setOutputResult({ success: false, text: `Failed to execute: ${error.message}` });
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

  // Keyboard shortcuts for tabs - no deps needed, uses setActiveTab functional form
  useEffect(() => {
    const tabNames: TabName[] = ['preview', 'code', 'output'];
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) {
        e.preventDefault();
        setActiveTab((prev) => {
          const idx = tabNames.indexOf(prev);
          return e.key === 'ArrowRight'
            ? tabNames[(idx + 1) % tabNames.length]
            : tabNames[(idx - 1 + tabNames.length) % tabNames.length];
        });
      }
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Command palette keyboard shortcut
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(true);
      }
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  const previewContent = useMemo(() => {
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
  }, [fileContent, fileExtension, currentFile?.name]);

  return (
    <TooltipProvider delayDuration={300}>
      <div className="flex flex-col h-screen">
        <Header
          currentFileName={currentFile?.name || ''}
          connected={connected}
          isDark={isDark}
          onToggleTheme={toggleTheme}
          onOpenSettings={() => setPrefsOpen(true)}
          onOpenCommandPalette={() => setCommandPaletteOpen(true)}
        />

        <div className="flex flex-1 overflow-hidden min-h-0">
          <FileTree
            tree={fileTree}
            selectedPath={currentFile?.path ?? null}
            onFileSelect={loadFile}
            onRefresh={requestRefresh}
            isFileTypeWatched={isFileTypeWatched}
          />

          <div className="flex-1 flex flex-col overflow-hidden min-w-0">
            <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as TabName)} className="flex-1 flex flex-col overflow-hidden">
              <div className="bg-card border-b border-border px-2 shrink-0">
                <TabsList className="h-9 bg-transparent gap-1 rounded-none">
                  <TabsTrigger value="preview" className="data-[state=active]:shadow-none data-[state=active]:bg-accent rounded-md text-xs gap-1.5">
                    🖥️ Preview
                  </TabsTrigger>
                  <TabsTrigger value="code" className="data-[state=active]:shadow-none data-[state=active]:bg-accent rounded-md text-xs gap-1.5">
                    📝 Code
                  </TabsTrigger>
                  <TabsTrigger value="output" className="data-[state=active]:shadow-none data-[state=active]:bg-accent rounded-md text-xs gap-1.5">
                    📊 Output
                  </TabsTrigger>
                </TabsList>
              </div>

              <div className="flex-1 relative overflow-hidden">
                <TabsContent value="preview" className="absolute inset-0 overflow-auto mt-0 ring-0 focus-visible:ring-0">
                  <div className="h-full bg-background">
                    {previewContent}
                  </div>
                </TabsContent>

                <TabsContent value="code" className="absolute inset-0 overflow-auto mt-0 ring-0 focus-visible:ring-0">
                  <pre className="min-h-full">
                    <code
                      ref={codeRef}
                      className="block bg-background text-foreground p-5 font-mono text-sm leading-relaxed min-h-full overflow-auto whitespace-pre"
                    />
                  </pre>
                </TabsContent>

                <TabsContent value="output" className="absolute inset-0 overflow-auto mt-0 ring-0 focus-visible:ring-0">
                  <div className="bg-background text-green-600 dark:text-green-400 font-mono text-sm leading-relaxed p-5 min-h-full">
                    {outputResult ? (
                      <div className={cn(
                        'p-3.5 m-3 rounded-md border-l-3 text-sm',
                        outputResult.success
                          ? 'bg-green-500/10 text-green-700 dark:text-green-400 border-green-500'
                          : 'bg-destructive/10 text-red-700 dark:text-red-400 border-destructive',
                      )}>
                        <strong>{outputResult.success ? 'Execution completed successfully' : 'Execution failed'}</strong>
                        <pre className={cn(
                          'mt-2 p-2.5 rounded-sm text-[13px] font-mono overflow-x-auto',
                          outputResult.success ? 'bg-green-500/10' : 'bg-destructive/10',
                        )}>{outputResult.text}</pre>
                      </div>
                    ) : (
                      <div className="text-muted-foreground text-center mt-12 text-sm">
                        Script output will appear here...
                      </div>
                    )}
                  </div>
                </TabsContent>
              </div>
            </Tabs>

            <div className="bg-card border-t border-border px-3 py-1.5 flex items-center gap-1.5 shrink-0">
              {currentFile?.extension === '.py' && (
                <Button variant="secondary" size="sm" onClick={runCode} className="gap-1.5 text-xs">
                  <Play className="h-3 w-3" /> Run
                </Button>
              )}
              {currentFile && FORMATTABLE_EXTENSIONS.includes(currentFile.extension) && (
                <Button variant="secondary" size="sm" onClick={formatCode} className="gap-1.5 text-xs">
                  <Sparkles className="h-3 w-3" /> Format
                </Button>
              )}
              {currentFile?.extension === '.html' && (
                <Button variant="secondary" size="sm" onClick={openExternal} className="gap-1.5 text-xs">
                  <ExternalLink className="h-3 w-3" /> Open External
                </Button>
              )}
              {currentFile && (
                <>
                  <Separator orientation="vertical" className="h-4 mx-0.5" />
                  <Button variant="ghost" size="sm" onClick={() => setFileInfoOpen(true)} className="gap-1.5 text-xs">
                    <Info className="h-3 w-3" /> Info
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>

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

        <CommandPalette
          isOpen={commandPaletteOpen}
          onClose={() => setCommandPaletteOpen(false)}
          fileTree={fileTree}
          onSelectFile={(file) => {
            setCommandPaletteOpen(false);
            loadFile(file);
          }}
        />
      </div>
    </TooltipProvider>
  );
}
