const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const FileService = require('./src/services/file-service');
const PythonExecutor = require('./src/services/python-executor');
const CodeFormatter = require('./src/services/code-formatter');
const FileWatcher = require('./src/services/file-watcher');

const createFileRoutes = require('./src/routes/file-routes');
const createExecuteRoutes = require('./src/routes/execute-routes');
const createFormatRoutes = require('./src/routes/format-routes');

const RATE_LIMIT_COUNT = 5;
const RATE_LIMIT_WINDOW = 60000; // 1 minute
const TIMEOUT = 30000; // 30 seconds
const MAX_CODE_SIZE = 50000; // 50KB

class QuickViewServer {
  constructor(options = {}) {
    this.port = options.port || 3333;
    this.watchDir = options.watchDir || process.cwd();

    this.app = express();
    this.server = http.createServer(this.app);
    this.io = socketIo(this.server);

    this.fileService = new FileService(this.watchDir);
    this.pythonExecutor = new PythonExecutor();
    this.codeFormatter = new CodeFormatter();
    this.fileWatcher = new FileWatcher(this.watchDir);

    this.streamingExecutionCount = new Map(); // Rate limiting for streaming execution

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
    this.app.get('/', (req, res) => {
      res.sendFile(path.join(__dirname, 'public', 'index.html'));
    });

    this.app.use('/api', createFileRoutes(this.fileService));
    this.app.use('/api/execute', createExecuteRoutes(this.pythonExecutor));
    this.app.use('/api/format', createFormatRoutes(this.fileService, this.codeFormatter));
  }

  setupSocketHandlers() {
    this.io.on('connection', (socket) => {
      console.log('Client connected');
      socket.on('disconnect', () => console.log('Client disconnected'));
      socket.emit('fileTree', this.fileService.getFileTree());

      // Streaming Python execution via Socket.IO
      socket.on('runPython', ({ code, filename }) => {
        const clientIP = socket.handshake.address || 'unknown';

        // Rate limiting: max 5 executions per minute per IP
        const now = Date.now();
        const executions = this.streamingExecutionCount.get(clientIP) || [];
        const recentExecutions = executions.filter(t => now - t < RATE_LIMIT_WINDOW);

        if (recentExecutions.length >= RATE_LIMIT_COUNT) {
          socket.emit('executionDone', {
            success: false,
            exitCode: -1,
            error: 'Too many Python executions. Please wait a minute.'
          });
          return;
        }

        recentExecutions.push(now);
        this.streamingExecutionCount.set(clientIP, recentExecutions);

        if (!code || typeof code !== 'string' || code.length > MAX_CODE_SIZE) {
          socket.emit('executionDone', { success: false, exitCode: -1, error: 'Invalid code' });
          return;
        }

        const tempDir = path.join(__dirname, 'temp');
        if (!fs.existsSync(tempDir)) {
          fs.mkdirSync(tempDir, { recursive: true });
        }

        const safeFilename = (filename || 'temp').replace(/[^a-zA-Z0-9_.-]/g, '_');
        const tempFile = path.join(tempDir, `${safeFilename}_${Date.now()}.py`);

        try {
          fs.writeFileSync(tempFile, code);
        } catch (err) {
          socket.emit('executionDone', { success: false, exitCode: -1, error: 'Failed to create temp file' });
          return;
        }

        socket.emit('executionStarted', {});

        const python = spawn('python3', [tempFile], { timeout: TIMEOUT, killSignal: 'SIGKILL' });
        let stderrBuffer = '';

        python.stdout.on('data', (data) => {
          socket.emit('outputLine', { type: 'stdout', text: data.toString() });
        });

        python.stderr.on('data', (data) => {
          const text = data.toString();
          stderrBuffer += text;
          socket.emit('outputLine', { type: 'stderr', text });
        });

        python.on('close', (exitCode) => {
          try { fs.unlinkSync(tempFile); } catch (e) { /* ignore */ }
          socket.emit('executionDone', {
            success: exitCode === 0,
            exitCode,
            stderr: stderrBuffer
          });
        });

        python.on('error', (err) => {
          try { fs.unlinkSync(tempFile); } catch (e) { /* ignore */ }
          socket.emit('executionDone', {
            success: false,
            exitCode: -1,
            error: err.message
          });
        });
      });
    });
  }

  setupFileWatcher() {
    this.fileWatcher.watch((event, filePath) => {
      console.log(`File ${event}: ${filePath}`);

      this.io.emit('fileChange', {
        event,
        path: filePath,
        relativePath: path.relative(this.watchDir, filePath),
        content: event !== 'unlink' ? this.fileService.readFileIfExists(filePath) : null
      });

      this.io.emit('fileTree', this.fileService.getFileTree());
    });
  }

  start() {
    this.server.listen(this.port, () => {
      console.log(`🚀 QuickView Server running at http://localhost:${this.port}`);
      console.log(`📁 Watching directory: ${this.watchDir}`);
      console.log('💡 Open http://localhost:' + this.port + ' in your browser');
    });
  }

  stop() {
    this.fileWatcher.stop();
    this.server.close();
  }
}

if (require.main === module) {
  const server = new QuickViewServer({
    port: process.env.PORT || 3333,
    watchDir: process.argv[2] || process.cwd()
  });

  server.start();

  process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down QuickView Server...');
    server.stop();
    process.exit(0);
  });
}

module.exports = QuickViewServer;
