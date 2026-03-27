import chokidar, { FSWatcher } from 'chokidar';

type WatchCallback = (event: string, filePath: string) => void;

export class FileWatcher {
  private watchDir: string;
  private watcher: FSWatcher | null;

  constructor(watchDir: string) {
    this.watchDir = watchDir;
    this.watcher = null;
  }

  watch(onChange: WatchCallback): void {
    this.watcher = chokidar.watch(this.watchDir, {
      ignored: /node_modules|\.git|\.DS_Store/,
      persistent: true,
      ignoreInitial: true,
    });

    this.watcher
      .on('add', (filePath: string) => onChange('add', filePath))
      .on('change', (filePath: string) => onChange('change', filePath))
      .on('unlink', (filePath: string) => onChange('unlink', filePath));
  }

  stop(): void {
    if (this.watcher) {
      this.watcher.close();
    }
  }
}
