const express = require('express');

function createExecuteRoutes(pythonExecutor) {
  const router = express.Router();

  router.post('/python', async (req, res) => {
    const { code, filename } = req.body;
    const clientIP = req.ip || req.connection.remoteAddress || 'unknown';

    if (pythonExecutor.isRateLimited(clientIP)) {
      return res.status(429).json({
        error: 'Too many Python executions. Please wait a minute before trying again.',
        success: false
      });
    }

    const validation = pythonExecutor.validateCode(code);
    if (!validation.valid) {
      return res.status(400).json({ error: validation.error, success: false });
    }

    pythonExecutor.recordExecution(clientIP);

    try {
      const result = await pythonExecutor.execute(code, filename);
      res.json(result);
    } catch (err) {
      if (err.code === 'ETIMEDOUT') {
        res.status(408).json({
          success: false,
          error: 'Python script execution timed out (30 second limit)',
          output: '',
          exitCode: -1
        });
      } else {
        res.status(500).json({
          success: false,
          error: 'Failed to execute Python script: ' + err.message,
          output: '',
          exitCode: -1
        });
      }
    }
  });

  return router;
}

module.exports = createExecuteRoutes;
