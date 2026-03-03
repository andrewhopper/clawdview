const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const RATE_LIMIT_COUNT = 5;
const RATE_LIMIT_WINDOW = 60000; // 1 minute
const TIMEOUT = 30000; // 30 seconds
const MAX_CODE_SIZE = 50000; // 50KB
const TEMP_DIR = path.join(__dirname, '../../temp');

class PythonExecutor {
  constructor() {
    this.executionCount = new Map();
  }

  isRateLimited(clientIP) {
    const now = Date.now();
    const executions = this.executionCount.get(clientIP) || [];
    const recent = executions.filter(t => now - t < RATE_LIMIT_WINDOW);
    return recent.length >= RATE_LIMIT_COUNT;
  }

  recordExecution(clientIP) {
    const now = Date.now();
    const executions = this.executionCount.get(clientIP) || [];
    const recent = executions.filter(t => now - t < RATE_LIMIT_WINDOW);
    recent.push(now);
    this.executionCount.set(clientIP, recent);
  }

  validateCode(code) {
    if (!code || typeof code !== 'string') {
      return { valid: false, error: 'Invalid Python code provided' };
    }
    if (code.length > MAX_CODE_SIZE) {
      return { valid: false, error: 'Python code too large (max 50KB)' };
    }
    return { valid: true };
  }

  execute(code, filename) {
    return new Promise((resolve, reject) => {
      if (!fs.existsSync(TEMP_DIR)) {
        fs.mkdirSync(TEMP_DIR, { recursive: true });
      }

      const tempFile = path.join(TEMP_DIR, `${filename || 'temp'}_${Date.now()}.py`);

      try {
        fs.writeFileSync(tempFile, code);
      } catch (error) {
        return reject(new Error('Failed to create temp file'));
      }

      const python = spawn('python3', [tempFile], {
        timeout: TIMEOUT,
        killSignal: 'SIGKILL'
      });

      let output = '';
      let error = '';

      python.stdout.on('data', (data) => { output += data.toString(); });
      python.stderr.on('data', (data) => { error += data.toString(); });

      const cleanup = () => {
        try { fs.unlinkSync(tempFile); } catch {
          console.warn('Failed to clean up temp file:', tempFile);
        }
      };

      python.on('close', (code) => {
        cleanup();
        resolve({ success: code === 0, output, error, exitCode: code });
      });

      python.on('error', (err) => {
        cleanup();
        reject(err);
      });
    });
  }
}

module.exports = PythonExecutor;
