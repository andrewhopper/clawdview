import { Router, Request, Response } from 'express';
import path from 'path';
import { S3Service } from '../services/s3-service';
import { FileService } from '../services/file-service';

interface ValidationSuccess {
  absolutePath: string;
  filename: string;
}

interface ValidationError {
  status: number;
  error: string;
}

function validateFileRequest(
  fileService: FileService,
  filePath: string | undefined,
): ValidationSuccess | ValidationError {
  if (!filePath) {
    return { status: 400, error: 'filePath is required' };
  }

  const filename = path.basename(filePath);

  if (fileService.isHiddenFile(filename)) {
    return { status: 403, error: 'Cannot share hidden files' };
  }

  const ext = path.extname(filename).toLowerCase();
  if (ext && !fileService.isAllowedExtension(ext)) {
    return { status: 403, error: 'File type not allowed for sharing' };
  }

  let absolutePath: string;
  try {
    absolutePath = fileService.getFilePath(filePath);
  } catch {
    return { status: 403, error: 'Path outside watch directory' };
  }

  const content = fileService.readFileIfExists(absolutePath);
  if (content === null) {
    return { status: 404, error: 'File not found' };
  }

  return { absolutePath, filename };
}

function isValidationError(result: ValidationSuccess | ValidationError): result is ValidationError {
  return 'error' in result;
}

export function createShareRoutes(s3Service: S3Service, fileService: FileService): Router {
  const router = Router();

  router.get('/share/status', (_req: Request, res: Response) => {
    res.json({ enabled: s3Service.isConfigured() });
  });

  router.post('/share/presign', async (req: Request, res: Response) => {
    if (!s3Service.isConfigured()) {
      return res.status(503).json({ error: 'S3 sharing is not configured. Set QV_S3_BUCKET environment variable.' });
    }

    const validation = validateFileRequest(fileService, req.body.filePath);
    if (isValidationError(validation)) {
      return res.status(validation.status).json({ error: validation.error });
    }

    try {
      const content = fileService.readFile(validation.absolutePath);
      const result = await s3Service.share(validation.filename, content, req.body.expiresIn);
      res.json({
        success: true,
        url: result.url,
        key: result.key,
        expiresIn: result.expiresIn,
        contentType: result.contentType,
      });
    } catch (error) {
      console.error('S3 share error:', error);
      res.status(500).json({ error: 'Failed to share file' });
    }
  });

  return router;
}
