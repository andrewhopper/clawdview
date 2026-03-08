import express from 'express';
import http from 'http';
import { Server as SocketIOServer } from 'socket.io';
import path from 'path';

import { FileService } from './services/file-service';
import { PythonExecutor } from './services/python-executor';
import { CodeFormatter } from './services/code-formatter';
import { FileWatcher } from './services/file-watcher';

import { createFileRoutes } from './routes/file-routes';
import { createExecuteRoutes } from './routes/execute-routes';
import { createFormatRoutes } from './routes/format-routes';

interface QuickViewServerOptions {
  port?: number;
  host?: string;
  watchDir?: string;
  autoOpen?: boolean;
}

export class QuickViewServer {
  private port: number;
  private host: string;
  private watchDir: string;
  private app: express.Application;
  private server: http.Server;
  private io: SocketIOServer;
  private fileService: FileService;
  private pythonExecutor: PythonExecutor;
  private codeFormatter: CodeFormatter;
  private fileWatcher: FileWatcher;

  constructor(options: QuickViewServerOptions = {}) {
    this.port = options.port || 3333;
    this.host = options.host || 'localhost';
    this.watchDir = options.watchDir || process.cwd();

    this.app = express();
    this.server = http.createServer(this.app);
    this.io = new SocketIOServer(this.server, {
      cors: {
        origin: [`http://localhost:${this.port}`, `http://127.0.0.1:${this.port}`],
      },
    });

    this.fileService = new FileService(this.watchDir);
    this.pythonExecutor = new PythonExecutor();
    this.codeFormatter = new CodeFormatter();
    this.fileWatcher = new FileWatcher(this.watchDir);

    this.setupMiddleware();
    this.setupRoutes();
    this.setupSocketHandlers();
    this.setupFileWatcher();
  }

  private setupMiddleware(): void {
    this.app.use(express.static(path.join(__dirname, '../../dist/public')));
    this.app.use('/preview', express.static(this.watchDir));
    this.app.use(express.json());
  }

  private setupRoutes(): void {
    this.app.get('/', (_req, res) => {
      res.sendFile(path.join(__dirname, '../../dist/public', 'index.html'));
    });

    this.app.use('/api', createFileRoutes(this.fileService));
    this.app.use('/api/execute', createExecuteRoutes(this.pythonExecutor));
    this.app.use('/api/format', createFormatRoutes(this.fileService, this.codeFormatter));
  }

  private setupSocketHandlers(): void {
    this.io.on('connection', (socket) => {
      console.log('Client connected');
      socket.on('disconnect', () => console.log('Client disconnected'));
      socket.emit('fileTree', this.fileService.getFileTree());
    });
  }

  private setupFileWatcher(): void {
    this.fileWatcher.watch((event, filePath) => {
      console.log(`File ${event}: ${filePath}`);

      this.io.emit('fileChange', {
        event,
        path: filePath,
        relativePath: path.relative(this.watchDir, filePath),
        content: event !== 'unlink' ? this.fileService.readFileIfExists(filePath) : null,
      });

      this.io.emit('fileTree', this.fileService.getFileTree());
    });
  }

  start(): void {
    this.server.listen(this.port, this.host, () => {
      console.log(`QuickView Server running at http://${this.host}:${this.port}`);
      console.log(`Watching directory: ${this.watchDir}`);
      console.log('Open http://localhost:' + this.port + ' in your browser');
    });
  }

  stop(): void {
    this.fileWatcher.stop();
    this.server.close();
  }
}

if (require.main === module) {
  const server = new QuickViewServer({
    port: Number(process.env.PORT) || 3333,
    watchDir: process.argv[2] || process.cwd(),
  });

  server.start();

  process.on('SIGINT', () => {
    console.log('\nShutting down QuickView Server...');
    server.stop();
    process.exit(0);
  });
}
