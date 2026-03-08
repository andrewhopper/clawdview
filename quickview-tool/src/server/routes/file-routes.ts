import { Router, Request, Response } from 'express';
import path from 'path';
import { FileService } from '../services/file-service';

interface ValidatedFile {
  requestedPath: string;
  filename: string;
  ext: string;
  filePath: string;
}

function validateFileRequest(
  req: Request,
  res: Response,
  fileService: FileService,
  checkExtension: (ext: string) => boolean,
): ValidatedFile | null {
  const requestedPath = req.params[0];
  const filename = path.basename(requestedPath);

  if (fileService.isHiddenFile(filename)) {
    res.status(403).json({ error: 'Access to hidden files denied' });
    return null;
  }

  const ext = path.extname(filename).toLowerCase();
  if (ext && !checkExtension(ext)) {
    res.status(403).json({ error: 'File type not supported for security reasons' });
    return null;
  }

  const filePath = fileService.getFilePath(requestedPath);

  if (!fileService.fileExists(filePath)) {
    res.status(404).json({ error: 'File not found' });
    return null;
  }

  return { requestedPath, filename, ext, filePath };
}

export function createFileRoutes(fileService: FileService): Router {
  const router = Router();

  router.get('/file/*', (req: Request, res: Response) => {
    const file = validateFileRequest(req, res, fileService, (ext) => fileService.isAllowedExtension(ext));
    if (!file) return;

    try {
      const content = fileService.readFile(file.filePath);
      res.json({ content, extension: file.ext, filename: file.filename, path: file.requestedPath });
    } catch {
      res.status(500).json({ error: 'Unable to read file' });
    }
  });

  router.get('/file-info/*', (req: Request, res: Response) => {
    const file = validateFileRequest(req, res, fileService, (ext) => fileService.isAllowedForInfo(ext));
    if (!file) return;

    try {
      const info = fileService.getFileInfo(file.filePath);
      res.json({ ...info, filename: file.filename, path: file.requestedPath, extension: file.ext });
    } catch {
      res.status(500).json({ error: 'Unable to read file info' });
    }
  });

  router.get('/files', (_req: Request, res: Response) => {
    res.json(fileService.getFileTree());
  });

  return router;
}
