const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const exifParser = require('exif-parser');

const ALLOWED_EXTENSIONS = [
  '.html', '.jsx', '.js', '.py', '.css', '.json',
  '.md', '.svg', '.txt', '.xml', '.yaml', '.yml'
];

const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.webp', '.gif'];

const UUID_PATTERN = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi;

class FileService {
  constructor(watchDir) {
    this.watchDir = watchDir;
  }

  isAllowedExtension(ext) {
    return !ext || ALLOWED_EXTENSIONS.includes(ext);
  }

  isImageExtension(ext) {
    return IMAGE_EXTENSIONS.includes(ext);
  }

  isAllowedForInfo(ext) {
    return !ext || ALLOWED_EXTENSIONS.includes(ext) || IMAGE_EXTENSIONS.includes(ext);
  }

  isHiddenFile(filename) {
    return filename.startsWith('.') && !filename.endsWith('.html');
  }

  getFilePath(requestedPath) {
    return path.join(this.watchDir, requestedPath);
  }

  readFile(filePath) {
    return fs.readFileSync(filePath, 'utf8');
  }

  readFileIfExists(filePath) {
    try {
      return fs.readFileSync(filePath, 'utf8');
    } catch {
      return null;
    }
  }

  writeFile(filePath, content) {
    fs.writeFileSync(filePath, content, 'utf8');
  }

  fileExists(filePath) {
    return fs.existsSync(filePath);
  }

  getFileInfo(filePath) {
    const stat = fs.statSync(filePath);
    const ext = path.extname(filePath).toLowerCase();
    const isImage = this.isImageExtension(ext);

    const info = {
      size: stat.size,
      inode: stat.ino,
      createdAt: stat.birthtime.toISOString(),
      modifiedAt: stat.mtime.toISOString(),
      permissions: '0' + (stat.mode & parseInt('777', 8)).toString(8),
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

  getGitInfo(filePath) {
    try {
      const dir = path.dirname(filePath);
      const opts = { cwd: dir, stdio: ['pipe', 'pipe', 'pipe'], timeout: 5000 };

      // Check if inside a git repo
      try {
        execSync('git rev-parse --is-inside-work-tree', opts);
      } catch {
        return null;
      }

      const git = {};

      // Get file status
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

      // Get last commit info for this file
      try {
        const log = execSync(
          `git log -1 --format="%H%n%an%n%aI%n%s" -- "${filePath}"`,
          opts
        ).toString().trim();

        if (log) {
          const [hash, author, date, subject] = log.split('\n');
          git.lastCommit = { hash, author, date, subject };
        }
      } catch {
        // File may have never been committed
      }

      // Get current branch
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

  extractUUIDs(content) {
    const matches = content.match(UUID_PATTERN);
    if (!matches) return [];
    return [...new Set(matches)];
  }

  extractExif(filePath) {
    try {
      const buffer = fs.readFileSync(filePath);
      const parser = exifParser.create(buffer);
      parser.enableSimpleValues(true);
      const result = parser.parse();

      const exif = {};
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

  getFileTree(dir = this.watchDir, prefix = '') {
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
}

module.exports = FileService;
