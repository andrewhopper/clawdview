const path = require('path');
const fs = require('fs');

const ALLOWED_EXTENSIONS = [
  '.html', '.jsx', '.js', '.py', '.css', '.json',
  '.md', '.svg', '.txt', '.xml', '.yaml', '.yml'
];

class FileService {
  constructor(watchDir) {
    this.watchDir = watchDir;
  }

  isAllowedExtension(ext) {
    return !ext || ALLOWED_EXTENSIONS.includes(ext);
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
