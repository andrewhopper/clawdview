class QuickViewApp {
    constructor() {
        this.socket = io();
        this.currentFile = null;
        this.fileTree = null;
        this.setupSocketHandlers();
        this.setupUIHandlers();
        this.setupTabs();
    }

    setupSocketHandlers() {
        this.socket.on('connect', () => {
            this.updateStatus('connected');
            console.log('Connected to QuickView server');
        });

        this.socket.on('disconnect', () => {
            this.updateStatus('disconnected');
            console.log('Disconnected from QuickView server');
        });

        this.socket.on('fileTree', (tree) => {
            this.fileTree = tree;
            this.renderFileTree();
        });

        this.socket.on('fileChange', (data) => {
            console.log('File changed:', data);
            if (this.currentFile && data.relativePath === this.currentFile.path) {
                this.loadFile(this.currentFile);
            }
            // Update file tree if needed
            if (data.event === 'add' || data.event === 'unlink') {
                // File tree will be updated via fileTree event
            }
        });
    }

    setupUIHandlers() {
        document.getElementById('refresh-files').addEventListener('click', () => {
            this.socket.emit('refreshFiles');
        });

        document.getElementById('run-code').addEventListener('click', () => {
            this.runCode();
        });

        document.getElementById('format-code').addEventListener('click', () => {
            this.formatCode();
        });

        document.getElementById('open-external').addEventListener('click', () => {
            this.openExternal();
        });
    }

    setupTabs() {
        const tabs = document.querySelectorAll('.tab');
        const panels = document.querySelectorAll('.panel');

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

    updateStatus(status) {
        const statusElement = document.getElementById('status');
        statusElement.className = `status ${status}`;
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
                element.addEventListener('click', () => {
                    this.selectFile(item, element);
                });
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
            'html': 'html',
            'js': 'js',
            'jsx': 'js',
            'py': 'py',
            'json': 'json',
            'md': 'md',
            'svg': 'svg',
            'css': 'css',
            'yaml': 'yaml',
            'yml': 'yaml',
            'mmd': 'mermaid',
            'mermaid': 'mermaid'
        };
        
        return classMap[ext] || 'file';
    }

    selectFile(file, element) {
        // Remove previous selection
        document.querySelectorAll('.file-item.selected').forEach(item => {
            item.classList.remove('selected');
        });
        
        // Add selection to clicked item
        element.classList.add('selected');
        
        this.currentFile = file;
        this.loadFile(file);
    }

    async loadFile(file) {
        this.showLoading(true);
        
        try {
            const response = await fetch(`/api/file/${file.path}`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to load file');
            }
            
            document.getElementById('current-file').textContent = file.name;
            
            // Update code panel
            this.updateCodePanel(data.content, data.extension);
            
            // Update preview panel
            this.updatePreviewPanel(data.content, data.extension, file.name);
            
            // Update action buttons
            this.updateActionButtons(data.extension);
            
        } catch (error) {
            console.error('Error loading file:', error);
            this.showError('Failed to load file: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    updateCodePanel(content, extension) {
        const codeElement = document.getElementById('code-content');
        codeElement.textContent = content;
        
        // Apply syntax highlighting
        if (window.hljs) {
            const language = this.getHighlightLanguage(extension);
            if (language) {
                codeElement.className = `language-${language}`;
                hljs.highlightElement(codeElement);
            }
        }
    }

    getHighlightLanguage(extension) {
        const langMap = {
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.py': 'python',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.md': 'markdown',
            '.svg': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.mmd': 'plaintext',
            '.mermaid': 'plaintext'
        };

        return langMap[extension] || null;
    }

    updatePreviewPanel(content, extension, filename) {
        const previewContent = document.getElementById('preview-content');
        // Delegate to the modular renderer registry.
        // To add a new renderer: create a file in public/renderers/ and add a <script> tag in index.html.
        window.RendererRegistry.render(previewContent, content, extension, filename);
    }

    updateActionButtons(extension) {
        const runBtn = document.getElementById('run-code');
        const formatBtn = document.getElementById('format-code');
        const openBtn = document.getElementById('open-external');
        
        // Show/hide buttons based on file type
        runBtn.style.display = extension === '.py' ? 'block' : 'none';
        formatBtn.style.display = ['.js', '.jsx', '.json', '.html', '.css'].includes(extension) ? 'block' : 'none';
        openBtn.style.display = extension === '.html' ? 'block' : 'none';
    }

    async runCode() {
        if (!this.currentFile || this.currentFile.extension !== '.py') return;
        
        this.showLoading(true);
        
        try {
            const response = await fetch(`/api/file/${this.currentFile.path}`);
            const data = await response.json();
            
            const execResponse = await fetch('/api/execute/python', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: data.content,
                    filename: this.currentFile.name
                })
            });
            
            const result = await execResponse.json();
            
            // Switch to output tab and show results
            document.querySelector('[data-tab="output"]').click();
            
            const outputContent = document.getElementById('output-content');
            if (result.success) {
                outputContent.innerHTML = `
                    <div class="success">
                        <strong>✅ Execution completed successfully</strong>
                        <pre>${this.escapeHtml(result.output || 'No output')}</pre>
                    </div>
                `;
            } else {
                outputContent.innerHTML = `
                    <div class="error">
                        <strong>❌ Execution failed</strong>
                        <pre>${this.escapeHtml(result.error || 'Unknown error')}</pre>
                    </div>
                `;
            }
            
        } catch (error) {
            console.error('Error running code:', error);
            this.showError('Failed to execute Python script: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async formatCode() {
        if (!this.currentFile) return;
        
        this.showLoading(true);
        
        try {
            const response = await fetch(`/api/format`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filepath: this.currentFile.path,
                    extension: this.currentFile.extension
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Reload the file to show formatted content
                this.loadFile(this.currentFile);
                
                // Show success message briefly
                const formatBtn = document.getElementById('format-code');
                const originalText = formatBtn.textContent;
                formatBtn.textContent = '✓ Formatted';
                formatBtn.style.background = '#10b981';
                
                setTimeout(() => {
                    formatBtn.textContent = originalText;
                    formatBtn.style.background = '';
                }, 2000);
            } else {
                this.showError('Failed to format code: ' + result.error);
            }
            
        } catch (error) {
            console.error('Error formatting code:', error);
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

    showLoading(show) {
        const loading = document.getElementById('loading');
        loading.style.display = show ? 'flex' : 'none';
    }

    showError(message) {
        const previewContent = document.getElementById('preview-content');
        previewContent.innerHTML = `<div class="error">${message}</div>`;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new QuickViewApp();
});