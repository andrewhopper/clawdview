import path from 'path';
import fs from 'fs';
import { FileService } from './file-service';
import { FileWatcher } from './file-watcher';
import type { FileTreeItem, WatchedDirInfo } from '../../shared/types';

type ChangeCallback = (event: string, filePath: string, rootDir: string) => void;

export class MultiDirManager {
  private dirs: Map<string, { fileService: FileService; watcher: FileWatcher; watching: boolean }> = new Map();
  private onChange: ChangeCallback | null = null;

  constructor(initialDir: string) {
    this.addDir(initialDir);
  }

  private resolveDir(dir: string): string {
    return path.resolve(dir);
  }

  addDir(dir: string): boolean {
    const abs = this.resolveDir(dir);
    if (this.dirs.has(abs)) return false;
    if (!fs.existsSync(abs) || !fs.statSync(abs).isDirectory()) return false;

    const fileService = new FileService(abs);
    const watcher = new FileWatcher(abs);
    let watching = false;

    if (this.onChange) {
      const cb = this.onChange;
      watcher.watch((event, filePath) => cb(event, filePath, abs));
      watching = true;
    }

    this.dirs.set(abs, { fileService, watcher, watching });
    return true;
  }

  removeDir(dir: string): boolean {
    const abs = this.resolveDir(dir);
    const entry = this.dirs.get(abs);
    if (!entry) return false;
    if (this.dirs.size <= 1) return false; // keep at least one
    entry.watcher.stop();
    this.dirs.delete(abs);
    return true;
  }

  watchAll(onChange: ChangeCallback): void {
    this.onChange = onChange;
    for (const [abs, entry] of this.dirs) {
      if (entry.watching) continue;
      const rootDir = abs;
      entry.watcher.watch((event, filePath) => onChange(event, filePath, rootDir));
      entry.watching = true;
    }
  }

  getMergedFileTree(): FileTreeItem[] {
    const roots: FileTreeItem[] = [];
    for (const [abs, { fileService }] of this.dirs) {
      const label = path.basename(abs);
      const children = fileService.getFileTree();
      // Tag all items with rootDir
      tagRootDir(children, abs);
      roots.push({
        name: label,
        type: 'directory',
        path: abs,
        children,
        rootDir: abs,
      });
    }
    // If single dir, return its children directly (no wrapper)
    if (roots.length === 1) return roots[0].children || [];
    return roots;
  }

  getWatchedDirs(): WatchedDirInfo[] {
    return Array.from(this.dirs.keys()).map((abs) => ({
      absolutePath: abs,
      label: path.basename(abs),
    }));
  }

  getFileServiceFor(filePath: string): FileService | null {
    // Try to find which root owns this path
    for (const [abs, { fileService }] of this.dirs) {
      // If the file path starts with the root label or is relative within it
      const resolved = path.resolve(abs, filePath);
      if (resolved.startsWith(abs)) return fileService;
    }
    // Fallback to first
    const first = this.dirs.values().next().value;
    return first ? first.fileService : null;
  }

  getPrimaryFileService(): FileService {
    return this.dirs.values().next().value!.fileService;
  }

  stopAll(): void {
    for (const { watcher } of this.dirs.values()) {
      watcher.stop();
    }
  }

  hasSingleDir(): boolean {
    return this.dirs.size === 1;
  }

  getDirCount(): number {
    return this.dirs.size;
  }
}

function tagRootDir(items: FileTreeItem[], rootDir: string): void {
  for (const item of items) {
    item.rootDir = rootDir;
    if (item.children) tagRootDir(item.children, rootDir);
  }
}
