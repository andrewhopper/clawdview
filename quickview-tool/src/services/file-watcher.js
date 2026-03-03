const chokidar = require('chokidar');

class FileWatcher {
  constructor(watchDir) {
    this.watchDir = watchDir;
    this.watcher = null;
  }

  watch(onChange) {
    this.watcher = chokidar.watch(this.watchDir, {
      ignored: /node_modules|\.git|\.DS_Store/,
      persistent: true,
      ignoreInitial: true
    });

    this.watcher
      .on('add', (filePath) => onChange('add', filePath))
      .on('change', (filePath) => onChange('change', filePath))
      .on('unlink', (filePath) => onChange('unlink', filePath));
  }

  stop() {
    if (this.watcher) {
      this.watcher.close();
    }
  }
}

module.exports = FileWatcher;
