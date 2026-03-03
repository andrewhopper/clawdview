require.config({
    paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }
});

require(['vs/editor/editor.main'], function () {

class QuickViewApp {
    constructor() {
        this.socket = io();
        this.currentFile = null;
        this.fileTree = null;
        this.monacoEditor = null;

        this.initMonaco();
        this.setupSocketHandlers();
        this.setupUIHandlers();
        this.setupTabs();
        this.setupResizeHandle();
        this.setupConsoleCapture();
    }

    // ─── Monaco Editor ───────────────────────────────────────────

    initMonaco() {
        this.monacoEditor = monaco.editor.create(document.getElementById('monaco-editor'), {
            value: '',
            language: 'plaintext',
            theme: 'vs-dark',
            readOnly: true,
            minimap: { enabled: true },
            lineNumbers: 'on',
            folding: true,
            scrollBeyondLastLine: false,
            renderWhitespace: 'selection',
            fontFamily: "'JetBrains Mono', 'Fira Code', 'Monaco', 'Menlo', monospace",
            fontSize: 13,
            lineHeight: 20,
            automaticLayout: true,
            scrollbar: {
                useShadows: false,
                verticalScrollbarSize: 6,
                horizontalScrollbarSize: 6
            },
            contextmenu: true,
            wordWrap: 'off',
            overviewRulerBorder: false
        });

        this.monacoEditor.onDidChangeCursorPosition((e) => {
            const pos = e.position;
            document.getElementById('status-pos').textContent = `Ln ${pos.lineNumber}, Col ${pos.column}`;
        });
    }

    updateCodePanel(content, extension) {
        if (!this.monacoEditor) return;

        const language = this.getMonacoLanguage(extension);

        // Dispose old model to avoid memory leaks
        const oldModel = this.monacoEditor.getModel();
        if (oldModel) oldModel.dispose();

        const model = monaco.editor.createModel(content, language);
        this.monacoEditor.setModel(model);
        this.monacoEditor.setScrollPosition({ scrollTop: 0, scrollLeft: 0 });

        // Clear stale error markers
        monaco.editor.setModelMarkers(model, 'python', []);

        // Update status bar
        document.getElementById('status-lang').textContent = this.getLanguageLabel(extension);
        document.getElementById('status-lines').textContent = `${model.getLineCount()} lines`;
        document.getElementById('status-pos').textContent = 'Ln 1, Col 1';
    }

    getMonacoLanguage(extension) {
        const langMap = {
            '.js': 'javascript', '.jsx': 'javascript',
            '.py': 'python', '.html': 'html', '.css': 'css',
            '.json': 'json', '.md': 'markdown', '.svg': 'xml',
            '.yaml': 'yaml', '.yml': 'yaml', '.txt': 'plaintext'
        };
        return langMap[extension] || 'plaintext';
    }

    getLanguageLabel(extension) {
        const labelMap = {
            '.js': 'JavaScript', '.jsx': 'JSX',
            '.py': 'Python', '.html': 'HTML', '.css': 'CSS',
            '.json': 'JSON', '.md': 'Markdown', '.svg': 'SVG',
            '.yaml': 'YAML', '.yml': 'YAML', '.txt': 'Plain Text'
        };
        return labelMap[extension] || 'Plain Text';
    }

    // ─── Error Markers ───────────────────────────────────────────

    setErrorMarkers(stderr) {
        const model = this.monacoEditor && this.monacoEditor.getModel();
        if (!model) return;

        const markers = [];
        // Python traceback: File "...", line 42
        const tracePattern = /File ".*?", line (\d+)/g;
        let match;
        while ((match = tracePattern.exec(stderr)) !== null) {
            const lineNum = parseInt(match[1]);
            if (lineNum >= 1 && lineNum <= model.getLineCount()) {
                markers.push({
                    startLineNumber: lineNum,
                    endLineNumber: lineNum,
                    startColumn: 1,
                    endColumn: model.getLineMaxColumn(lineNum),
                    message: stderr.trim().split('\n').pop() || 'Python error',
                    severity: monaco.MarkerSeverity.Error
                });
            }
        }

        monaco.editor.setModelMarkers(model, 'python', markers);
    }

    // ─── Socket Handlers ─────────────────────────────────────────

    setupSocketHandlers() {
        this.socket.on('connect', () => this.updateStatus('connected'));
        this.socket.on('disconnect', () => this.updateStatus('disconnected'));

        this.socket.on('fileTree', (tree) => {
            this.fileTree = tree;
            this.renderFileTree();
        });

        this.socket.on('fileChange', (data) => {
            if (this.currentFile && data.relativePath === this.currentFile.path) {
                this.loadFile(this.currentFile);
            }
        });

        // Streaming execution: started
        this.socket.on('executionStarted', () => {
            document.querySelector('[data-tab="output"]').click();
            document.getElementById('output-content').innerHTML = '';
        });

        // Streaming execution: each line
        this.socket.on('outputLine', ({ type, text }) => {
            this.appendOutputLine(type, text);
        });

        // Streaming execution: finished
        this.socket.on('executionDone', ({ success, exitCode, stderr, error }) => {
            const outputContent = document.getElementById('output-content');
            const statusEl = document.createElement('div');
            statusEl.className = success ? 'output-status success-text' : 'output-status error-text';
            statusEl.textContent = success
                ? `✅ Process exited (code ${exitCode})`
                : `❌ Process failed (code ${exitCode})${error ? ': ' + error : ''}`;
            outputContent.appendChild(statusEl);

            // Set inline error markers from Python stderr
            if (this.currentFile && this.currentFile.extension === '.py') {
                this.setErrorMarkers(stderr || '');
            }

            const runBtn = document.getElementById('run-code');
            if (runBtn) {
                runBtn.disabled = false;
                runBtn.textContent = '▶️ Run';
            }
        });
    }

    appendOutputLine(type, text) {
        const outputContent = document.getElementById('output-content');

        const placeholder = outputContent.querySelector('.output-placeholder');
        if (placeholder) placeholder.remove();

        const line = document.createElement('div');
        line.className = `output-line ${type}`;
        line.textContent = text;
        outputContent.appendChild(line);

        // Scroll the panel to show latest output
        const panel = document.getElementById('output-panel');
        panel.scrollTop = panel.scrollHeight;
    }

    // ─── Console Capture (from preview iframe) ───────────────────

    setupConsoleCapture() {
        window.addEventListener('message', (event) => {
            if (!event.data || event.data.type !== 'console') return;
            const { method, args } = event.data;
            const type = (method === 'error' || method === 'warn') ? 'stderr' : 'stdout';
            this.appendOutputLine(type, `[console.${method}] ${args.join(' ')}`);
        });
    }

    // ─── UI Handlers ─────────────────────────────────────────────

    setupUIHandlers() {
        document.getElementById('refresh-files').addEventListener('click', () => {
            this.socket.emit('refreshFiles');
        });
        document.getElementById('run-code').addEventListener('click', () => this.runCode());
        document.getElementById('format-code').addEventListener('click', () => this.formatCode());
        document.getElementById('open-external').addEventListener('click', () => this.openExternal());
    }

    setupTabs() {
        const tabs = document.querySelectorAll('#preview-pane .tab');
        const panels = document.querySelectorAll('#preview-pane .panel');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetPanel = tab.dataset.tab;
                tabs.forEach(t => t.classList.remove('active'));
                panels.forEach(p => p.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById(`${targetPanel}-panel`).classList.add('active');
            });
        });
    }

    // ─── Resize Handle ───────────────────────────────────────────

    setupResizeHandle() {
        const handle = document.getElementById('resize-handle');
        const container = document.getElementById('split-container');
        let isResizing = false;

        handle.addEventListener('mousedown', (e) => {
            isResizing = true;
            handle.classList.add('dragging');
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            const rect = container.getBoundingClientRect();
            const offset = e.clientX - rect.left;
            const total = rect.width - 5;
            const leftPct = Math.min(80, Math.max(20, (offset / total) * 100));
            container.style.gridTemplateColumns = `${leftPct}% 5px ${100 - leftPct}%`;
            if (this.monacoEditor) this.monacoEditor.layout();
        });

        document.addEventListener('mouseup', () => {
            if (!isResizing) return;
            isResizing = false;
            handle.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        });
    }

    // ─── File Tree ───────────────────────────────────────────────

    updateStatus(status) {
        document.getElementById('status').className = `status ${status}`;
    }

    renderFileTree() {
        const container = document.getElementById('file-tree');
        container.innerHTML = '';
        if (this.fileTree && this.fileTree.length > 0) {
            this.renderFileItems(this.fileTree, container);
        } else {
            container.innerHTML = '<div class="no-files">No files found</div>';
        }
    }

    renderFileItems(items, container, level = 0) {
        items.forEach(item => {
            const element = document.createElement('div');
            element.className = `file-item ${item.type} ${this.getFileClass(item.extension)}`;
            element.style.paddingLeft = `${12 + (level * 16)}px`;
            element.textContent = item.name;

            if (item.type === 'file') {
                element.addEventListener('click', () => this.selectFile(item, element));
            }

            container.appendChild(element);

            if (item.children && item.children.length > 0) {
                this.renderFileItems(item.children, container, level + 1);
            }
        });
    }

    getFileClass(extension) {
        if (!extension) return 'file';
        const ext = extension.toLowerCase().replace('.', '');
        const classMap = {
            'html': 'html', 'js': 'js', 'jsx': 'js', 'py': 'py',
            'json': 'json', 'md': 'md', 'svg': 'svg', 'css': 'css'
        };
        return classMap[ext] || 'file';
    }

    selectFile(file, element) {
        document.querySelectorAll('.file-item.selected').forEach(item => item.classList.remove('selected'));
        element.classList.add('selected');
        this.currentFile = file;
        this.loadFile(file);
    }

    // ─── File Loading ────────────────────────────────────────────

    async loadFile(file) {
        this.showLoading(true);
        try {
            const response = await fetch(`/api/file/${file.path}`);
            const data = await response.json();

            if (!response.ok) throw new Error(data.error || 'Failed to load file');

            document.getElementById('current-file').textContent = file.name;
            this.updateCodePanel(data.content, data.extension);
            this.updatePreviewPanel(data.content, data.extension, file.name);
            this.updateActionButtons(data.extension);
        } catch (error) {
            console.error('Error loading file:', error);
            this.showError('Failed to load file: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    // ─── Preview Renderers ───────────────────────────────────────

    updatePreviewPanel(content, extension, filename) {
        const previewContent = document.getElementById('preview-content');
        switch (extension) {
            case '.html': this.renderHTML(previewContent, content); break;
            case '.jsx':  this.renderReact(previewContent, content); break;
            case '.py':   this.renderPythonPreview(previewContent, content, filename); break;
            case '.svg':  this.renderSVG(previewContent, content); break;
            case '.md':   this.renderMarkdown(previewContent, content); break;
            case '.json': this.renderJSON(previewContent, content); break;
            default:      this.renderText(previewContent, content);
        }
    }

    renderHTML(container, content) {
        // Reset output panel placeholder when new HTML is loaded
        const outputContent = document.getElementById('output-content');
        if (!outputContent.querySelector('.output-line')) {
            outputContent.innerHTML = '<div class="output-placeholder">Console output will appear here...</div>';
        }

        const iframe = document.createElement('iframe');
        iframe.className = 'preview-iframe';

        // Inject console capture script so console.log etc. flow to the Output panel
        const consoleScript = `<script>(function(){` +
            `var _c={log:console.log,warn:console.warn,error:console.error,info:console.info};` +
            `['log','warn','error','info'].forEach(function(m){` +
            `console[m]=function(){_c[m].apply(console,arguments);` +
            `window.parent.postMessage({type:'console',method:m,` +
            `args:Array.from(arguments).map(String)},'*');};` +
            `});` +
            `window.addEventListener('error',function(e){` +
            `window.parent.postMessage({type:'console',method:'error',` +
            `args:[(e.message||'Error')+' (line '+e.lineno+')']},'*');` +
            `});` +
            `})()\x3c/script>`;

        const injected = content.includes('<head>')
            ? content.replace('<head>', '<head>' + consoleScript)
            : consoleScript + content;

        iframe.srcdoc = injected;
        container.innerHTML = '';
        container.appendChild(iframe);
    }

    renderReact(container, content) {
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
                        typeof window[key] === 'function' &&
                        key[0] === key[0].toUpperCase()
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

    renderPythonPreview(container, content, filename) {
        container.innerHTML = `
            <div style="padding: 20px; color: #333;">
                <h3 style="font-size:1rem; font-weight:600; margin-bottom:8px;">Python Script: ${this.escapeHtml(filename)}</h3>
                <p style="color:#666; font-size:0.875rem;">Click "▶️ Run" to execute and see output in the Output tab.</p>
            </div>
        `;
    }

    renderSVG(container, content) {
        container.innerHTML = `<div style="padding: 20px; text-align: center; background: white;">${content}</div>`;
    }

    renderMarkdown(container, content) {
        const html = content
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
            .replace(/\*(.*)\*/gim, '<em>$1</em>')
            .replace(/\n/gim, '<br>');
        container.innerHTML = `<div style="padding: 20px; color: #333;">${html}</div>`;
    }

    renderJSON(container, content) {
        try {
            const parsed = JSON.parse(content);
            const formatted = JSON.stringify(parsed, null, 2);
            container.innerHTML = `
                <div style="padding: 20px; color: #333;">
                    <pre style="background: #f5f5f5; padding: 15px; border-radius: 6px; overflow-x: auto;">${this.escapeHtml(formatted)}</pre>
                </div>
            `;
        } catch (error) {
            container.innerHTML = `<div class="error">Invalid JSON: ${error.message}</div>`;
        }
    }

    renderText(container, content) {
        container.innerHTML = `
            <div style="padding: 20px; color: #333;">
                <pre style="white-space: pre-wrap; font-family: monospace;">${this.escapeHtml(content)}</pre>
            </div>
        `;
    }

    // ─── Actions ─────────────────────────────────────────────────

    updateActionButtons(extension) {
        document.getElementById('run-code').style.display =
            extension === '.py' ? 'block' : 'none';
        document.getElementById('format-code').style.display =
            ['.js', '.jsx', '.json', '.html', '.css'].includes(extension) ? 'block' : 'none';
        document.getElementById('open-external').style.display =
            extension === '.html' ? 'block' : 'none';
    }

    async runCode() {
        if (!this.currentFile || this.currentFile.extension !== '.py') return;

        try {
            const response = await fetch(`/api/file/${this.currentFile.path}`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to load file');

            const runBtn = document.getElementById('run-code');
            runBtn.disabled = true;
            runBtn.textContent = '⏳ Running...';

            // Clear any existing error markers
            const model = this.monacoEditor && this.monacoEditor.getModel();
            if (model) monaco.editor.setModelMarkers(model, 'python', []);

            // Stream execution via Socket.IO
            this.socket.emit('runPython', {
                code: data.content,
                filename: this.currentFile.name
            });
        } catch (error) {
            this.showError('Failed to run code: ' + error.message);
        }
    }

    async formatCode() {
        if (!this.currentFile) return;
        this.showLoading(true);
        try {
            const response = await fetch('/api/format', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    filepath: this.currentFile.path,
                    extension: this.currentFile.extension
                })
            });
            const result = await response.json();

            if (result.success) {
                this.loadFile(this.currentFile);
                const formatBtn = document.getElementById('format-code');
                const orig = formatBtn.textContent;
                formatBtn.textContent = '✓ Formatted';
                formatBtn.style.background = '#10b981';
                setTimeout(() => {
                    formatBtn.textContent = orig;
                    formatBtn.style.background = '';
                }, 2000);
            } else {
                this.showError('Failed to format: ' + result.error);
            }
        } catch (error) {
            this.showError('Failed to format code: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    openExternal() {
        if (this.currentFile && this.currentFile.extension === '.html') {
            window.open(`/preview/${this.currentFile.path}`, '_blank');
        }
    }

    // ─── Utilities ───────────────────────────────────────────────

    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'flex' : 'none';
    }

    showError(message) {
        document.getElementById('preview-content').innerHTML = `<div class="error">${message}</div>`;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize once Monaco is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new QuickViewApp());
} else {
    new QuickViewApp();
}

}); // end require(['vs/editor/editor.main'], ...)
