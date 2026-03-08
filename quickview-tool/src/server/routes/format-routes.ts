import { Router, Request, Response } from 'express';
import { FileService } from '../services/file-service';
import { CodeFormatter } from '../services/code-formatter';

export function createFormatRoutes(
  fileService: FileService,
  codeFormatter: CodeFormatter,
): Router {
  const router = Router();

  router.post('/', (req: Request, res: Response) => {
    const { filepath, extension } = req.body;

    if (!filepath || !extension) {
      return res.status(400).json({ success: false, error: 'Missing filepath or extension' });
    }

    const fullPath = fileService.getFilePath(filepath);

    try {
      const content = fileService.readFile(fullPath);
      const formatted = codeFormatter.format(content, extension);
      fileService.writeFile(fullPath, formatted);
      res.json({ success: true, message: 'File formatted successfully' });
    } catch (error: any) {
      if (error.message === 'File type not supported for formatting') {
        res.status(400).json({ success: false, error: error.message });
      } else {
        res.status(500).json({ success: false, error: error.message });
      }
    }
  });

  return router;
}
