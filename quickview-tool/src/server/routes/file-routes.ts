import { Router, Request, Response } from 'express';
import path from 'path';
import { FileService } from '../services/file-service';

export function createFileRoutes(fileService: FileService): Router {
  const router = Router();

  router.get('/file/*', (req: Request, res: Response) => {
    const requestedPath = req.params[0];
    const filename = path.basename(requestedPath);

    if (fileService.isHiddenFile(filename)) {
      return res.status(403).json({ error: 'Access to hidden files denied' });
    }

    const ext = path.extname(filename).toLowerCase();
    if (ext && !fileService.isAllowedExtension(ext)) {
      return res.status(403).json({ error: 'File type not supported for security reasons' });
    }

    const filePath = fileService.getFilePath(requestedPath);

    if (!fileService.fileExists(filePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    try {
      const content = fileService.readFile(filePath);
      res.json({ content, extension: ext, filename, path: requestedPath });
    } catch {
      res.status(500).json({ error: 'Unable to read file' });
    }
  });

  router.get('/file-info/*', (req: Request, res: Response) => {
    const requestedPath = req.params[0];
    const filename = path.basename(requestedPath);

    if (fileService.isHiddenFile(filename)) {
      return res.status(403).json({ error: 'Access to hidden files denied' });
    }

    const ext = path.extname(filename).toLowerCase();
    if (ext && !fileService.isAllowedForInfo(ext)) {
      return res.status(403).json({ error: 'File type not supported for security reasons' });
    }

    const filePath = fileService.getFilePath(requestedPath);

    if (!fileService.fileExists(filePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    try {
      const info = fileService.getFileInfo(filePath);
      res.json({ ...info, filename, path: requestedPath, extension: ext });
    } catch {
      res.status(500).json({ error: 'Unable to read file info' });
    }
  });

  router.get('/files', (_req: Request, res: Response) => {
    res.json(fileService.getFileTree());
  });

  return router;
}
