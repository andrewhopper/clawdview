class QuickViewApp {
    constructor() {
        this.socket = io();
        this.currentFile = null;
        this.fileTree = null;
        this._slidevKeyHandler = null;
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
            const isSlidev = item.type === 'file' && item.extension === '.md' && item.name.startsWith('slides-');
            const fileClass = isSlidev ? 'slides' : this.getFileClass(item.extension);
            const element = document.createElement('div');
            element.className = `file-item ${item.type} ${fileClass}`;
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
            'css': 'css'
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
        // Clean up any active Slidev keyboard listener
        if (this._slidevKeyHandler) {
            document.removeEventListener('keydown', this._slidevKeyHandler);
            this._slidevKeyHandler = null;
        }
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
            '.svg': 'xml'
        };
        
        return langMap[extension] || null;
    }

    updatePreviewPanel(content, extension, filename) {
        const previewContent = document.getElementById('preview-content');
        
        switch (extension) {
            case '.html':
                this.renderHTML(previewContent, content);
                break;
                
            case '.jsx':
                this.renderReact(previewContent, content);
                break;
                
            case '.py':
                this.renderPythonPreview(previewContent, content, filename);
                break;
                
            case '.svg':
                this.renderSVG(previewContent, content);
                break;
                
            case '.md':
                if (this.isSlidevFile(filename, content)) {
                    this.renderSlidev(previewContent, content, filename);
                } else {
                    this.renderMarkdown(previewContent, content);
                }
                break;
                
            case '.json':
                this.renderJSON(previewContent, content);
                break;
                
            default:
                this.renderText(previewContent, content);
        }
    }

    renderHTML(container, content) {
        const iframe = document.createElement('iframe');
        iframe.className = 'preview-iframe';
        iframe.srcdoc = content;
        
        container.innerHTML = '';
        container.appendChild(iframe);
    }

    renderReact(container, content) {
        try {
            // Create a wrapper for React component
            const wrapper = document.createElement('div');
            wrapper.id = 'react-preview';
            container.innerHTML = '';
            container.appendChild(wrapper);
            
            // Transform JSX using Babel
            const transformed = Babel.transform(content, {
                presets: ['react']
            }).code;
            
            // Create and execute the component
            const script = document.createElement('script');
            script.textContent = `
                try {
                    ${transformed}
                    
                    // Try to find and render the component
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
                <h3>Python Script: ${filename}</h3>
                <p>Click "Run" to execute this Python script and see the output.</p>
                <div style="margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 6px;">
                    <strong>Script Preview:</strong>
                    <pre style="margin-top: 10px; overflow-x: auto;">${this.escapeHtml(content.substring(0, 500))}${content.length > 500 ? '...' : ''}</pre>
                </div>
            </div>
        `;
    }

    renderSVG(container, content) {
        container.innerHTML = `
            <div style="padding: 20px; text-align: center; background: white;">
                ${content}
            </div>
        `;
    }

    renderMarkdown(container, content) {
        const html = this.renderMarkdownToHtml(content);
        container.innerHTML = `<div style="padding: 20px; color: #333; line-height: 1.6;">${html}</div>`;
        container.querySelectorAll('pre code').forEach(el => {
            if (window.hljs) hljs.highlightElement(el);
        });
    }

    renderMarkdownToHtml(content) {
        if (window.marked) {
            return marked.parse(content);
        }
        // Fallback basic renderer
        return content
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    isSlidevFile(filename, content) {
        // Detect by naming convention
        if (filename.startsWith('slides-')) return true;
        // Detect by Slidev frontmatter (starts with --- and has Slidev-specific keys)
        const frontmatterMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
        if (frontmatterMatch) {
            const fm = frontmatterMatch[1];
            if (/^(theme|transition|highlighter|lineNumbers|colorSchema|layout):/m.test(fm)) return true;
        }
        return false;
    }

    parseSimpleYaml(yamlStr) {
        const result = {};
        for (const line of yamlStr.split('\n')) {
            const match = line.match(/^([\w-]+):\s*(.*)$/);
            if (match) result[match[1]] = match[2].trim();
        }
        return result;
    }

    parseSlidevSlides(content) {
        // Split on lines that are exactly ---
        const blocks = content.split(/^---\s*$/m).map(b => b.trim()).filter(b => b);

        if (blocks.length === 0) return [{ frontmatter: {}, content }];

        // A block is YAML-like if every non-empty line is a key: value pair or indented
        const isYaml = (str) => {
            const lines = str.split('\n').filter(l => l.trim());
            return lines.length > 0 && lines.every(l => /^[\w-]+:/.test(l) || /^\s/.test(l));
        };

        const slides = [];
        let i = 0;

        // Skip global frontmatter (first block if it's YAML)
        if (i < blocks.length && isYaml(blocks[i])) i++;

        while (i < blocks.length) {
            // Slide-level frontmatter followed by content
            if (isYaml(blocks[i]) && i + 1 < blocks.length && !isYaml(blocks[i + 1])) {
                slides.push({ frontmatter: this.parseSimpleYaml(blocks[i]), content: blocks[i + 1] });
                i += 2;
            } else {
                slides.push({ frontmatter: {}, content: blocks[i] });
                i++;
            }
        }

        return slides.length > 0 ? slides : [{ frontmatter: {}, content }];
    }

    renderSlidev(container, content, filename) {
        const slides = this.parseSlidevSlides(content);

        if (slides.length === 0) {
            container.innerHTML = '<div class="error">No slides found in this file</div>';
            return;
        }

        const viewerId = 'slidev-' + Date.now();
        container.innerHTML = `
            <div class="slidev-viewer" id="${viewerId}">
                <div class="slidev-stage">
                    <div class="slidev-slide-container">
                        <div class="slidev-slide layout-default" id="${viewerId}-slide"></div>
                    </div>
                </div>
                <div class="slidev-nav">
                    <button class="slidev-btn" id="${viewerId}-prev">◀ Prev</button>
                    <span class="slidev-counter" id="${viewerId}-counter">1 / ${slides.length}</span>
                    <button class="slidev-btn" id="${viewerId}-next">Next ▶</button>
                    <button class="slidev-btn" id="${viewerId}-fullscreen">⛶ Fullscreen</button>
                </div>
            </div>
        `;

        let currentIndex = 0;
        const slideEl = document.getElementById(`${viewerId}-slide`);
        const counterEl = document.getElementById(`${viewerId}-counter`);
        const prevBtn = document.getElementById(`${viewerId}-prev`);
        const nextBtn = document.getElementById(`${viewerId}-next`);
        const fullscreenBtn = document.getElementById(`${viewerId}-fullscreen`);

        const showSlide = (index) => {
            const slide = slides[index];
            const layout = slide.frontmatter.layout || 'default';
            slideEl.className = `slidev-slide layout-${layout}`;

            let slideContent = slide.content;

            // Handle two-cols layout with ::right:: separator
            if (layout === 'two-cols') {
                const parts = slideContent.split(/^::right::\s*$/m);
                const leftHtml = this.renderMarkdownToHtml(parts[0] || '');
                const rightHtml = this.renderMarkdownToHtml(parts[1] || '');
                slideEl.innerHTML = `
                    <div class="slidev-col">${leftHtml}</div>
                    <div class="slidev-col">${rightHtml}</div>
                `;
            } else {
                slideEl.innerHTML = this.renderMarkdownToHtml(slideContent);
            }

            slideEl.querySelectorAll('pre code').forEach(el => {
                if (window.hljs) hljs.highlightElement(el);
            });

            counterEl.textContent = `${index + 1} / ${slides.length}`;
            prevBtn.disabled = index === 0;
            nextBtn.disabled = index === slides.length - 1;
        };

        prevBtn.addEventListener('click', () => {
            if (currentIndex > 0) showSlide(--currentIndex);
        });

        nextBtn.addEventListener('click', () => {
            if (currentIndex < slides.length - 1) showSlide(++currentIndex);
        });

        fullscreenBtn.addEventListener('click', () => {
            const viewer = document.getElementById(viewerId);
            if (document.fullscreenElement) {
                document.exitFullscreen();
            } else {
                viewer.requestFullscreen();
            }
        });

        const keyHandler = (e) => {
            if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) {
                if (currentIndex < slides.length - 1) showSlide(++currentIndex);
                e.preventDefault();
            } else if (['ArrowLeft', 'ArrowUp'].includes(e.key)) {
                if (currentIndex > 0) showSlide(--currentIndex);
                e.preventDefault();
            }
        };

        document.addEventListener('keydown', keyHandler);
        this._slidevKeyHandler = keyHandler;

        showSlide(0);
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

    updateActionButtons(extension) {
        const runBtn = document.getElementById('run-code');
        const formatBtn = document.getElementById('format-code');
        const openBtn = document.getElementById('open-external');
        
        // Show/hide buttons based on file type
        const isSlidev = extension === '.md' && this.currentFile && this.isSlidevFile(this.currentFile.name, '');
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