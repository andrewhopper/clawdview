const express = require('express');
const path = require('path');

function validateFileRequest(fileService, filePath) {
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

  const absolutePath = path.resolve(fileService.watchDir, filePath);
  if (!absolutePath.startsWith(path.resolve(fileService.watchDir))) {
    return { status: 403, error: 'Path outside watch directory' };
  }

  if (!fileService.fileExists(absolutePath)) {
    return { status: 404, error: 'File not found' };
  }

  return { absolutePath, filename };
}

function createShareRoutes(s3Service, fileService) {
  const router = express.Router();

  router.get('/share/status', (req, res) => {
    res.json({ enabled: s3Service.isConfigured() });
  });

  router.post('/share/presign', async (req, res) => {
    if (!s3Service.isConfigured()) {
      return res.status(503).json({ error: 'S3 sharing is not configured. Set QV_S3_BUCKET environment variable.' });
    }

    const validation = validateFileRequest(fileService, req.body.filePath);
    if (validation.error) {
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

module.exports = createShareRoutes;
