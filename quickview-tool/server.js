const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const chokidar = require('chokidar');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const open = require('open');

class ClawdViewServer {
  constructor(options = {}) {
    this.port = options.port || 3333;
    this.watchDir = options.watchDir || process.cwd();
    this.app = express();
    this.server = http.createServer(this.app);
    this.io = socketIo(this.server);
    this.pythonExecutionCount = new Map(); // Rate limiting for Python execution
    this.setupMiddleware();
    this.setupRoutes();
    this.setupSocketHandlers();
    this.setupFileWatcher();
  }

  setupMiddleware() {
    this.app.use(express.static(path.join(__dirname, 'public')));
    this.app.use('/preview', express.static(this.watchDir));
    this.app.use(express.json());
  }

  setupRoutes() {
    // Main preview interface
    this.app.get('/', (req, res) => {
      res.sendFile(path.join(__dirname, 'public', 'index.html'));
    });

    // API to get file content
    this.app.get('/api/file/*', (req, res) => {
      const requestedPath = req.params[0];
      const filename = path.basename(requestedPath);
      
      // Security: Prevent serving hidden/sensitive files
      if (filename.startsWith('.') && !filename.endsWith('.html')) {
        return res.status(403).json({ error: 'Access to hidden files denied' });
      }
      
      // Security: Basic file type restrictions
      const allowedExtensions = ['.html', '.jsx', '.js', '.py', '.css', '.json', '.md', '.svg', '.txt', '.xml', '.yaml', '.yml'];
      const ext = path.extname(filename).toLowerCase();
      if (ext && !allowedExtensions.includes(ext)) {
        return res.status(403).json({ error: 'File type not supported for security reasons' });
      }
      
      const filePath = path.join(this.watchDir, requestedPath);
      
      if (!fs.existsSync(filePath)) {
        return res.status(404).json({ error: 'File not found' });
      }

      try {
        const content = fs.readFileSync(filePath, 'utf8');
        
        res.json({
          content,
          extension: ext,
          filename: filename,
          path: requestedPath // Don't expose full system path
        });
      } catch (error) {
        res.status(500).json({ error: 'Unable to read file' });
      }
    });

    // API to execute Python scripts
    this.app.post('/api/execute/python', (req, res) => {
      const { code, filename } = req.body;
      const clientIP = req.ip || req.connection.remoteAddress || 'unknown';
      
      // Simple rate limiting: max 5 executions per minute per IP
      const now = Date.now();
      const executions = this.pythonExecutionCount.get(clientIP) || [];
      const recentExecutions = executions.filter(time => now - time < 60000); // Last minute
      
      if (recentExecutions.length >= 5) {
        return res.status(429).json({ 
          error: 'Too many Python executions. Please wait a minute before trying again.',
          success: false 
        });
      }
      
      // Update execution count
      recentExecutions.push(now);
      this.pythonExecutionCount.set(clientIP, recentExecutions);
      
      // Basic input validation
      if (!code || typeof code !== 'string') {
        return res.status(400).json({ error: 'Invalid Python code provided', success: false });
      }
      
      if (code.length > 50000) { // 50KB limit
        return res.status(400).json({ error: 'Python code too large (max 50KB)', success: false });
      }
      
      const tempFile = path.join(__dirname, 'temp', `${filename || 'temp'}_${Date.now()}.py`);
      
      // Ensure temp directory exists
      const tempDir = path.dirname(tempFile);
      if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir, { recursive: true });
      }

      try {
        fs.writeFileSync(tempFile, code);
      } catch (error) {
        return res.status(500).json({ error: 'Failed to create temp file', success: false });
      }

      const python = spawn('python3', [tempFile], {
        timeout: 30000, // 30 second timeout
        killSignal: 'SIGKILL'
      });
      let output = '';
      let error = '';

      python.stdout.on('data', (data) => {
        output += data.toString();
      });

      python.stderr.on('data', (data) => {
        error += data.toString();
      });

      python.on('close', (code) => {
        // Clean up temp file
        try {
          fs.unlinkSync(tempFile);
        } catch (cleanupError) {
          console.warn('Failed to clean up temp file:', tempFile);
        }
        
        res.json({
          success: code === 0,
          output: output,
          error: error,
          exitCode: code
        });
      });

      // Handle timeout
      python.on('error', (err) => {
        try {
          fs.unlinkSync(tempFile);
        } catch (cleanupError) {
          console.warn('Failed to clean up temp file after error:', tempFile);
        }
        
        if (err.code === 'ETIMEDOUT') {
          res.status(408).json({
            success: false,
            error: 'Python script execution timed out (30 second limit)',
            output: output,
            exitCode: -1
          });
        } else {
          res.status(500).json({
            success: false,
            error: 'Failed to execute Python script: ' + err.message,
            output: output,
            exitCode: -1
          });
        }
      });
    });

    // API to list files in directory
    this.app.get('/api/files', (req, res) => {
      const files = this.getFileTree(this.watchDir);
      res.json(files);
    });

    // API to format code files
    this.app.post('/api/format', (req, res) => {
      const { filepath, extension } = req.body;
      
      if (!filepath || !extension) {
        return res.status(400).json({ success: false, error: 'Missing filepath or extension' });
      }
      
      const fullPath = path.join(this.watchDir, filepath);
      
      try {
        // Read current file content
        const content = fs.readFileSync(fullPath, 'utf8');
        let formattedContent;
        
        // Format based on file type
        switch (extension) {
          case '.js':
          case '.jsx':
            formattedContent = this.formatJavaScript(content);
            break;
          case '.json':
            formattedContent = this.formatJSON(content);
            break;
          case '.html':
            formattedContent = this.formatHTML(content);
            break;
          case '.css':
            formattedContent = this.formatCSS(content);
            break;
          default:
            return res.status(400).json({ success: false, error: 'File type not supported for formatting' });
        }
        
        // Write formatted content back to file
        fs.writeFileSync(fullPath, formattedContent, 'utf8');
        
        res.json({ success: true, message: 'File formatted successfully' });
        
      } catch (error) {
        res.status(500).json({ success: false, error: error.message });
      }
    });
  }

  setupSocketHandlers() {
    this.io.on('connection', (socket) => {
      console.log('Client connected');
      
      socket.on('disconnect', () => {
        console.log('Client disconnected');
      });

      // Send initial file list
      socket.emit('fileTree', this.getFileTree(this.watchDir));
    });
  }

  setupFileWatcher() {
    this.watcher = chokidar.watch(this.watchDir, {
      ignored: /node_modules|\.git|\.DS_Store/,
      persistent: true,
      ignoreInitial: true
    });

    this.watcher
      .on('add', (filePath) => this.handleFileChange('add', filePath))
      .on('change', (filePath) => this.handleFileChange('change', filePath))
      .on('unlink', (filePath) => this.handleFileChange('unlink', filePath));
  }

  handleFileChange(event, filePath) {
    console.log(`File ${event}: ${filePath}`);
    
    // Emit file change to all connected clients
    this.io.emit('fileChange', {
      event,
      path: filePath,
      relativePath: path.relative(this.watchDir, filePath),
      content: event !== 'unlink' ? this.readFileIfExists(filePath) : null
    });

    // Update file tree
    this.io.emit('fileTree', this.getFileTree(this.watchDir));
  }

  readFileIfExists(filePath) {
    try {
      return fs.readFileSync(filePath, 'utf8');
    } catch (error) {
      return null;
    }
  }

  getFileTree(dir, prefix = '') {
    const items = [];
    
    try {
      const files = fs.readdirSync(dir);
      
      for (const file of files) {
        if (file.startsWith('.') && !file.endsWith('.html')) continue;
        if (file === 'node_modules') continue;
        
        const fullPath = path.join(dir, file);
        const relativePath = path.join(prefix, file);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
          items.push({
            name: file,
            type: 'directory',
            path: relativePath,
            children: this.getFileTree(fullPath, relativePath)
          });
        } else {
          items.push({
            name: file,
            type: 'file',
            path: relativePath,
            extension: path.extname(file).toLowerCase(),
            size: stat.size
          });
        }
      }
    } catch (error) {
      console.error('Error reading directory:', error);
    }
    
    return items.sort((a, b) => {
      if (a.type === b.type) return a.name.localeCompare(b.name);
      return a.type === 'directory' ? -1 : 1;
    });
  }

  // Formatting methods
  formatJavaScript(content) {
    // Basic JavaScript/JSX formatting
    let formatted = content
      // Add spacing around operators
      .replace(/([^=!<>])=([^=])/g, '$1 = $2')
      .replace(/([^=!<>])==([^=])/g, '$1 == $2')
      .replace(/([^=!<>])===([^=])/g, '$1 === $2')
      // Add spacing around braces
      .replace(/\{([^\s])/g, '{ $1')
      .replace(/([^\s])\}/g, '$1 }')
      // Fix indentation (basic)
      .split('\n')
      .map(line => line.trim())
      .map((line, i, arr) => {
        let indent = 0;
        for (let j = 0; j < i; j++) {
          const prevLine = arr[j];
          if (prevLine.includes('{')) indent += 2;
          if (prevLine.includes('}')) indent -= 2;
        }
        if (line.includes('}')) indent -= 2;
        return ' '.repeat(Math.max(0, indent)) + line;
      })
      .join('\n');
    
    return formatted;
  }

  formatJSON(content) {
    try {
      const parsed = JSON.parse(content);
      return JSON.stringify(parsed, null, 2);
    } catch (error) {
      throw new Error('Invalid JSON content');
    }
  }

  formatHTML(content) {
    // Basic HTML formatting
    let formatted = content
      // Add newlines after tags
      .replace(/></g, '>\n<')
      // Fix indentation
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0)
      .map((line, i, arr) => {
        let indent = 0;
        for (let j = 0; j < i; j++) {
          const prevLine = arr[j];
          if (prevLine.match(/<[^\/][^>]*[^\/]>/)) indent += 2;
          if (prevLine.match(/<\/[^>]*>/)) indent -= 2;
        }
        if (line.match(/<\/[^>]*>/)) indent -= 2;
        return ' '.repeat(Math.max(0, indent)) + line;
      })
      .join('\n');
    
    return formatted;
  }

  formatCSS(content) {
    // Basic CSS formatting
    let formatted = content
      // Add spacing around braces
      .replace(/\{/g, ' {\n  ')
      .replace(/\}/g, '\n}\n')
      // Add spacing after colons
      .replace(/:\s*([^;]+);/g, ': $1;')
      // Add newlines after semicolons
      .replace(/;\s*([^}])/g, ';\n  $1')
      // Clean up multiple newlines
      .replace(/\n\s*\n/g, '\n')
      .trim();
    
    return formatted;
  }

  start() {
    this.server.listen(this.port, () => {
      console.log(`🚀 ClawdView Server running at http://localhost:${this.port}`);
      console.log(`📁 Watching directory: ${this.watchDir}`);
      
      console.log('💡 Open http://localhost:' + this.port + ' in your browser');
    });
  }

  stop() {
    if (this.watcher) {
      this.watcher.close();
    }
    this.server.close();
  }
}

// Export for use as module or run directly
if (require.main === module) {
  const server = new ClawdViewServer({
    port: process.env.PORT || 3333,
    watchDir: process.argv[2] || process.cwd()
  });
  
  server.start();

  // Graceful shutdown
  process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down ClawdView Server...');
    server.stop();
    process.exit(0);
  });
}

module.exports = ClawdViewServer;