// @ts-check
const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

/**
 * Security tests – verify that the server enforces its security rules:
 *  - Hidden/sensitive files are blocked
 *  - Unsupported (potentially dangerous) file types are rejected
 *  - Python execution rate-limiting kicks in
 *  - Oversized Python code is rejected
 */
test.describe('Security', () => {
  test.describe('Hidden file protection', () => {
    test('blocks access to hidden files (dot-prefixed, non-.html)', async ({ request }) => {
      const response = await request.get('/api/file/.env');
      expect(response.status()).toBe(403);
      const body = await response.json();
      expect(body.error).toMatch(/hidden/i);
    });

    test('blocks access to .ssh directory traversal', async ({ request }) => {
      const response = await request.get('/api/file/.ssh/id_rsa');
      expect(response.status()).toBe(403);
    });
  });

  test.describe('File type restrictions', () => {
    test('blocks executable file types (.exe)', async ({ request }) => {
      const response = await request.get('/api/file/malware.exe');
      expect(response.status()).toBe(403);
      const body = await response.json();
      expect(body.error).toMatch(/not supported/i);
    });

    test('blocks shell scripts (.sh)', async ({ request }) => {
      const response = await request.get('/api/file/script.sh');
      expect(response.status()).toBe(403);
    });

    test('blocks batch files (.bat)', async ({ request }) => {
      const response = await request.get('/api/file/run.bat');
      expect(response.status()).toBe(403);
    });

    test('allows .html files even if dot-prefixed (edge case)', async ({ request }) => {
      // Per server.js logic: hidden files ending in .html are NOT blocked
      // This test documents the behaviour; it may 404 if the file doesn't exist.
      const response = await request.get('/api/file/.hidden.html');
      // Should not be 403; could be 404 if file doesn't exist
      expect(response.status()).not.toBe(403);
    });
  });

  test.describe('Python execution safety', () => {
    test('rejects empty or missing code', async ({ request }) => {
      const response = await request.post('/api/execute/python', {
        data: { code: '', filename: 'test.py' },
      });
      expect(response.status()).toBe(400);
      const body = await response.json();
      expect(body.success).toBe(false);
    });

    test('rejects code that exceeds the 50KB size limit', async ({ request }) => {
      const oversizedCode = 'x = 1\n'.repeat(10000); // ~70KB
      const response = await request.post('/api/execute/python', {
        data: { code: oversizedCode, filename: 'big.py' },
      });
      expect(response.status()).toBe(400);
      const body = await response.json();
      expect(body.error).toMatch(/too large/i);
    });

    test('enforces rate limit after 5 executions per minute', async ({ request }) => {
      const code = 'print("ok")';
      // Exhaust the rate limit (5 allowed per minute)
      for (let i = 0; i < 5; i++) {
        await request.post('/api/execute/python', { data: { code, filename: 'test.py' } });
      }
      // 6th request should be throttled
      const response = await request.post('/api/execute/python', {
        data: { code, filename: 'test.py' },
      });
      expect(response.status()).toBe(429);
      const body = await response.json();
      expect(body.error).toMatch(/too many/i);
    });
  });
});
