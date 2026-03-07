const express = require('express');

function createShareRoutes(s3Service, fileService) {
  const router = express.Router();

  // Check if S3 sharing is available
  router.get('/share/status', (req, res) => {
    res.json({
      enabled: s3Service.isConfigured(),
      bucket: s3Service.isConfigured() ? s3Service.bucket : null,
      region: s3Service.isConfigured() ? s3Service.region : null,
    });
  });

  // Share a file via pre-signed URL
  router.post('/share/presign', async (req, res) => {
    if (!s3Service.isConfigured()) {
      return res.status(503).json({ error: 'S3 sharing is not configured. Set QV_S3_BUCKET environment variable.' });
    }

    const { filePath, expiresIn } = req.body;

    if (!filePath) {
      return res.status(400).json({ error: 'filePath is required' });
    }

    const filename = require('path').basename(filePath);

    if (fileService.isHiddenFile(filename)) {
      return res.status(403).json({ error: 'Cannot share hidden files' });
    }

    const ext = require('path').extname(filename).toLowerCase();
    if (ext && !fileService.isAllowedExtension(ext)) {
      return res.status(403).json({ error: 'File type not allowed for sharing' });
    }

    const absolutePath = fileService.getFilePath(filePath);
    if (!fileService.fileExists(absolutePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    try {
      const content = fileService.readFile(absolutePath);
      const result = await s3Service.shareWithPresignedUrl(filename, content, expiresIn);
      res.json({
        success: true,
        url: result.url,
        key: result.key,
        expiresIn: result.expiresIn,
        contentType: result.contentType,
      });
    } catch (error) {
      console.error('S3 share error:', error);
      res.status(500).json({ error: 'Failed to share file: ' + error.message });
    }
  });

  // Publish a file publicly to S3
  router.post('/share/publish', async (req, res) => {
    if (!s3Service.isConfigured()) {
      return res.status(503).json({ error: 'S3 sharing is not configured. Set QV_S3_BUCKET environment variable.' });
    }

    const { filePath } = req.body;

    if (!filePath) {
      return res.status(400).json({ error: 'filePath is required' });
    }

    const filename = require('path').basename(filePath);

    if (fileService.isHiddenFile(filename)) {
      return res.status(403).json({ error: 'Cannot publish hidden files' });
    }

    const ext = require('path').extname(filename).toLowerCase();
    if (ext && !fileService.isAllowedExtension(ext)) {
      return res.status(403).json({ error: 'File type not allowed for publishing' });
    }

    const absolutePath = fileService.getFilePath(filePath);
    if (!fileService.fileExists(absolutePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    try {
      const content = fileService.readFile(absolutePath);
      const result = await s3Service.publish(filename, content);
      res.json({
        success: true,
        publicUrl: result.publicUrl,
        key: result.key,
        contentType: result.contentType,
      });
    } catch (error) {
      console.error('S3 publish error:', error);
      res.status(500).json({ error: 'Failed to publish file: ' + error.message });
    }
  });

  return router;
}

module.exports = createShareRoutes;
