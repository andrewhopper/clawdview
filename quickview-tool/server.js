const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');

const FileService = require('./src/services/file-service');
const PythonExecutor = require('./src/services/python-executor');
const CodeFormatter = require('./src/services/code-formatter');
const FileWatcher = require('./src/services/file-watcher');

const createFileRoutes = require('./src/routes/file-routes');
const createExecuteRoutes = require('./src/routes/execute-routes');
const createFormatRoutes = require('./src/routes/format-routes');

class ClawdViewServer {
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
      console.log(`🚀 ClawdView Server running at http://localhost:${this.port}`);
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
  const server = new ClawdViewServer({
    port: process.env.PORT || 3333,
    watchDir: process.argv[2] || process.cwd()
  });

  server.start();

  process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down ClawdView Server...');
    server.stop();
    process.exit(0);
  });
}

module.exports = ClawdViewServer;
