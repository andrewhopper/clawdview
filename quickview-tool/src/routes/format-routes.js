const express = require('express');

function createFormatRoutes(fileService, codeFormatter) {
  const router = express.Router();

  router.post('/', (req, res) => {
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
    } catch (error) {
      if (error.message === 'File type not supported for formatting') {
        res.status(400).json({ success: false, error: error.message });
      } else {
        res.status(500).json({ success: false, error: error.message });
      }
    }
  });

  return router;
}

module.exports = createFormatRoutes;
