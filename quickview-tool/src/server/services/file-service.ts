import path from 'path';
import fs from 'fs';
import { execSync, ExecSyncOptions } from 'child_process';
import exifParser from 'exif-parser';

const ALLOWED_EXTENSIONS = [
  '.html', '.jsx', '.js', '.py', '.css', '.json',
  '.md', '.svg', '.txt', '.xml', '.yaml', '.yml',
];

const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.webp', '.gif'];

const UUID_PATTERN = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi;

export interface FileTreeItem {
  name: string;
  type: 'file' | 'directory';
  path: string;
  extension?: string;
  size?: number;
  mtime?: number;
  children?: FileTreeItem[];
}

export interface GitInfo {
  status: string;
  branch?: string;
  lastCommit?: {
    hash: string;
    author: string;
    date: string;
    subject: string;
  };
}

export interface ExifData {
  width?: number;
  height?: number;
  cameraMake?: string;
  cameraModel?: string;
  dateTaken?: string;
  exposureTime?: string;
  fNumber?: string;
  iso?: number;
  focalLength?: string;
  gpsLatitude?: number;
  gpsLongitude?: number;
  software?: string;
  copyright?: string;
  description?: string;
}

export interface FileInfo {
  size: number;
  inode: number;
  createdAt: string;
  modifiedAt: string;
  permissions: string;
  lines?: number;
  encoding?: string;
  uuids?: string[];
  git: GitInfo | null;
  exif?: ExifData | null;
}

export class FileService {
  private watchDir: string;

  constructor(watchDir: string) {
    this.watchDir = watchDir;
  }

  isAllowedExtension(ext: string): boolean {
    return !ext || ALLOWED_EXTENSIONS.includes(ext);
  }

  isImageExtension(ext: string): boolean {
    return IMAGE_EXTENSIONS.includes(ext);
  }

  isAllowedForInfo(ext: string): boolean {
    return !ext || ALLOWED_EXTENSIONS.includes(ext) || IMAGE_EXTENSIONS.includes(ext);
  }

  isHiddenFile(filename: string): boolean {
    return filename.startsWith('.') && !filename.endsWith('.html');
  }

  getFilePath(requestedPath: string): string {
    return path.join(this.watchDir, requestedPath);
  }

  readFile(filePath: string): string {
    return fs.readFileSync(filePath, 'utf8');
  }

  readFileIfExists(filePath: string): string | null {
    try {
      return fs.readFileSync(filePath, 'utf8');
    } catch {
      return null;
    }
  }

  writeFile(filePath: string, content: string): void {
    fs.writeFileSync(filePath, content, 'utf8');
  }

  fileExists(filePath: string): boolean {
    return fs.existsSync(filePath);
  }

  getFileInfo(filePath: string): FileInfo {
    const stat = fs.statSync(filePath);
    const ext = path.extname(filePath).toLowerCase();
    const isImage = this.isImageExtension(ext);

    const info: FileInfo = {
      size: stat.size,
      inode: stat.ino,
      createdAt: stat.birthtime.toISOString(),
      modifiedAt: stat.mtime.toISOString(),
      permissions: '0' + (stat.mode & parseInt('777', 8)).toString(8),
      git: null,
    };

    if (isImage) {
      info.exif = this.extractExif(filePath);
    } else {
      const content = fs.readFileSync(filePath, 'utf8');
      info.lines = content.split('\n').length;
      info.encoding = 'utf-8';

      const uuids = this.extractUUIDs(content);
      if (uuids.length > 0) {
        info.uuids = uuids;
      }
    }

    info.git = this.getGitInfo(filePath);

    return info;
  }

  private getGitInfo(filePath: string): GitInfo | null {
    try {
      const dir = path.dirname(filePath);
      const opts: ExecSyncOptions = { cwd: dir, stdio: 'pipe', timeout: 5000 };

      try {
        execSync('git rev-parse --is-inside-work-tree', opts);
      } catch {
        return null;
      }

      const git: GitInfo = { status: '' };

      const statusOutput = execSync(`git status --porcelain -- "${filePath}"`, opts).toString().trim();
      if (!statusOutput) {
        git.status = 'committed';
      } else {
        const code = statusOutput.substring(0, 2);
        if (code === '??') git.status = 'untracked';
        else if (code[0] === 'A') git.status = 'added (staged)';
        else if (code[0] === 'M' && code[1] === ' ') git.status = 'modified (staged)';
        else if (code[0] === ' ' && code[1] === 'M') git.status = 'modified (unstaged)';
        else if (code === 'MM') git.status = 'modified (staged + unstaged)';
        else if (code[0] === 'D') git.status = 'deleted';
        else if (code[0] === 'R') git.status = 'renamed';
        else git.status = statusOutput.substring(0, 2).trim();
      }

      try {
        const log = execSync(
          `git log -1 --format="%H%n%an%n%aI%n%s" -- "${filePath}"`,
          opts,
        ).toString().trim();

        if (log) {
          const [hash, author, date, subject] = log.split('\n');
          git.lastCommit = { hash, author, date, subject };
        }
      } catch {
        // File may have never been committed
      }

      try {
        git.branch = execSync('git rev-parse --abbrev-ref HEAD', opts).toString().trim();
      } catch {
        // ignore
      }

      return git;
    } catch {
      return null;
    }
  }

  private extractUUIDs(content: string): string[] {
    const matches = content.match(UUID_PATTERN);
    if (!matches) return [];
    return [...new Set(matches)];
  }

  private extractExif(filePath: string): ExifData | null {
    try {
      const buffer = fs.readFileSync(filePath);
      const parser = exifParser.create(buffer);
      parser.enableSimpleValues(true);
      const result = parser.parse();

      const exif: ExifData = {};
      const tags = result.tags || {};

      if (result.imageSize) {
        exif.width = result.imageSize.width;
        exif.height = result.imageSize.height;
      }
      if (tags.Make) exif.cameraMake = tags.Make;
      if (tags.Model) exif.cameraModel = tags.Model;
      if (tags.DateTimeOriginal) {
        exif.dateTaken = new Date(tags.DateTimeOriginal * 1000).toISOString();
      }
      if (tags.ExposureTime) exif.exposureTime = `1/${Math.round(1 / tags.ExposureTime)}s`;
      if (tags.FNumber) exif.fNumber = `f/${tags.FNumber}`;
      if (tags.ISO || tags.ISOSpeedRatings) exif.iso = tags.ISO || tags.ISOSpeedRatings;
      if (tags.FocalLength) exif.focalLength = `${tags.FocalLength}mm`;
      if (tags.GPSLatitude && tags.GPSLongitude) {
        exif.gpsLatitude = tags.GPSLatitude;
        exif.gpsLongitude = tags.GPSLongitude;
      }
      if (tags.Software) exif.software = tags.Software;
      if (tags.Copyright) exif.copyright = tags.Copyright;
      if (tags.ImageDescription) exif.description = tags.ImageDescription;

      return Object.keys(exif).length > 0 ? exif : null;
    } catch {
      return null;
    }
  }

  getFileTree(dir: string = this.watchDir, prefix: string = ''): FileTreeItem[] {
    const items: FileTreeItem[] = [];

    try {
      const files = fs.readdirSync(dir);

      for (const file of files) {
        if (this.isHiddenFile(file)) continue;
        if (file === 'node_modules') continue;

        const fullPath = path.join(dir, file);
        const relativePath = path.join(prefix, file);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
          items.push({
            name: file,
            type: 'directory',
            path: relativePath,
            children: this.getFileTree(fullPath, relativePath),
          });
        } else {
          items.push({
            name: file,
            type: 'file',
            path: relativePath,
            extension: path.extname(file).toLowerCase(),
            size: stat.size,
            mtime: stat.mtimeMs,
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
}
