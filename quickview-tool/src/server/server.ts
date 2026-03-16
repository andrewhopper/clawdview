import express from 'express';
import http from 'http';
import { Server as SocketIOServer } from 'socket.io';
import path from 'path';

import { PythonExecutor } from './services/python-executor';
import { CodeFormatter } from './services/code-formatter';
import { MultiDirManager } from './services/multi-dir-manager';

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
  private app: express.Application;
  private server: http.Server;
  private io: SocketIOServer;
  private dirManager: MultiDirManager;
  private pythonExecutor: PythonExecutor;
  private codeFormatter: CodeFormatter;

  constructor(options: QuickViewServerOptions = {}) {
    this.port = options.port || 3333;
    this.host = options.host || 'localhost';

    const watchDir = options.watchDir || process.cwd();

    this.app = express();
    this.server = http.createServer(this.app);
    this.io = new SocketIOServer(this.server, {
      cors: {
        origin: [`http://localhost:${this.port}`, `http://127.0.0.1:${this.port}`],
      },
    });

    this.dirManager = new MultiDirManager(watchDir);
    this.pythonExecutor = new PythonExecutor();
    this.codeFormatter = new CodeFormatter();

    this.setupMiddleware();
    this.setupRoutes();
    this.setupSocketHandlers();
    this.setupFileWatcher();
  }

  private setupMiddleware(): void {
    this.app.use(express.static(path.join(__dirname, '../../dist/public')));
    this.app.use('/preview', (req, res, next) => {
      const fileService = this.dirManager.getFileServiceFor(req.path.slice(1));
      if (fileService) {
        try {
          const filePath = fileService.getFilePath(req.path.slice(1));
          return res.sendFile(filePath);
        } catch {
          // fall through
        }
      }
      next();
    });
    this.app.use(express.json());
  }

  private setupRoutes(): void {
    this.app.get('/', (_req, res) => {
      res.sendFile(path.join(__dirname, '../../dist/public', 'index.html'));
    });

    this.app.use('/api', createFileRoutes(this.dirManager.getPrimaryFileService()));
    this.app.use('/api/execute', createExecuteRoutes(this.pythonExecutor));
    this.app.use('/api/format', createFormatRoutes(this.dirManager.getPrimaryFileService(), this.codeFormatter));
  }

  private setupSocketHandlers(): void {
    this.io.on('connection', (socket) => {
      console.log('Client connected');
      socket.on('disconnect', () => console.log('Client disconnected'));

      socket.on('refreshFiles', () => {
        socket.emit('fileTree', this.dirManager.getMergedFileTree());
        socket.emit('watchedDirs', this.dirManager.getWatchedDirs());
      });

      socket.on('addDir', (dir: string) => {
        const added = this.dirManager.addDir(dir);
        if (added) {
          console.log(`Added watched directory: ${dir}`);
          this.setupFileWatcher();
        }
        this.io.emit('fileTree', this.dirManager.getMergedFileTree());
        this.io.emit('watchedDirs', this.dirManager.getWatchedDirs());
      });

      socket.on('removeDir', (dir: string) => {
        const removed = this.dirManager.removeDir(dir);
        if (removed) {
          console.log(`Removed watched directory: ${dir}`);
        }
        this.io.emit('fileTree', this.dirManager.getMergedFileTree());
        this.io.emit('watchedDirs', this.dirManager.getWatchedDirs());
      });

      // Send initial data
      socket.emit('fileTree', this.dirManager.getMergedFileTree());
      socket.emit('watchedDirs', this.dirManager.getWatchedDirs());
    });
  }

  private setupFileWatcher(): void {
    this.dirManager.watchAll((event, filePath, rootDir) => {
      console.log(`File ${event}: ${filePath}`);

      this.io.emit('fileChange', {
        event,
        path: filePath,
        relativePath: path.relative(rootDir, filePath),
      });

      this.io.emit('fileTree', this.dirManager.getMergedFileTree());
    });
  }

  private static isPortAvailable(port: number, host: string): Promise<boolean> {
    return new Promise((resolve) => {
      const tester = http.createServer();
      tester.once('error', () => resolve(false));
      tester.listen(port, host, () => {
        tester.close(() => resolve(true));
      });
    });
  }

  private async findAvailablePort(startPort: number, maxAttempts = 20): Promise<number> {
    for (let i = 0; i < maxAttempts; i++) {
      const port = startPort + i;
      if (await QuickViewServer.isPortAvailable(port, this.host)) {
        return port;
      }
      if (i === 0) {
        console.log(`  Port ${port} in use, finding next available...`);
      } else {
        console.log(`  Port ${port} also in use...`);
      }
    }
    throw new Error(`No available port found (tried ${startPort}-${startPort + maxAttempts - 1})`);
  }

  async start(): Promise<number> {
    const availablePort = await this.findAvailablePort(this.port);
    this.port = availablePort;

    // Update CORS origins to match actual port
    this.io.engine.opts.cors = {
      origin: [`http://localhost:${availablePort}`, `http://127.0.0.1:${availablePort}`],
    };

    return new Promise((resolve, reject) => {
      this.server.once('error', reject);
      this.server.listen(availablePort, this.host, () => {
        console.log(`  Server:   http://${this.host}:${availablePort}`);
        console.log(`  Watching: ${this.dirManager.getWatchedDirs().map(d => d.absolutePath).join(', ')}`);
        resolve(availablePort);
      });
    });
  }

  getPort(): number {
    return this.port;
  }

  stop(): void {
    this.dirManager.stopAll();
    this.server.close();
  }
}

if (require.main === module) {
  const server = new QuickViewServer({
    port: Number(process.env.PORT) || 3333,
    watchDir: process.argv[2] || process.cwd(),
  });

  server.start().then((port) => {
    console.log(`Open http://localhost:${port} in your browser`);
  }).catch((err) => {
    console.error(`Failed to start server: ${err.message}`);
    process.exit(1);
  });

  process.on('SIGINT', () => {
    console.log('\nShutting down QuickView Server...');
    server.stop();
    process.exit(0);
  });
}
