// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * API endpoint tests using Playwright's request context.
 * These validate the server-side REST API independently of the UI.
 */
test.describe('REST API', () => {
  test.describe('GET /api/files', () => {
    test('returns an array of files', async ({ request }) => {
      const response = await request.get('/api/files');
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(Array.isArray(body)).toBe(true);
    });

    test('fixture files are present in the file list', async ({ request }) => {
      const response = await request.get('/api/files');
      const files = await response.json();
      const names = files.map((f) => f.name);
      expect(names).toContain('sample.html');
      expect(names).toContain('sample.json');
      expect(names).toContain('sample.py');
      expect(names).toContain('sample.md');
    });

    test('file entries have expected shape', async ({ request }) => {
      const response = await request.get('/api/files');
      const files = await response.json();
      const htmlFile = files.find((f) => f.name === 'sample.html');
      expect(htmlFile).toBeDefined();
      expect(htmlFile).toHaveProperty('name');
      expect(htmlFile).toHaveProperty('type', 'file');
      expect(htmlFile).toHaveProperty('path');
      expect(htmlFile).toHaveProperty('extension', '.html');
    });
  });

  test.describe('GET /api/file/:path', () => {
    test('returns content of an HTML file', async ({ request }) => {
      const response = await request.get('/api/file/sample.html');
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body).toHaveProperty('content');
      expect(body.content).toContain('<!DOCTYPE html>');
      expect(body).toHaveProperty('extension', '.html');
      expect(body).toHaveProperty('filename', 'sample.html');
    });

    test('returns content of a JSON file', async ({ request }) => {
      const response = await request.get('/api/file/sample.json');
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body).toHaveProperty('content');
      expect(body.extension).toBe('.json');
      // The content should be valid JSON
      const parsed = JSON.parse(body.content);
      expect(parsed).toHaveProperty('name');
    });

    test('returns content of a Markdown file', async ({ request }) => {
      const response = await request.get('/api/file/sample.md');
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body.content).toContain('# Sample Markdown Fixture');
    });

    test('returns content of a Python file', async ({ request }) => {
      const response = await request.get('/api/file/sample.py');
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body.content).toContain('def greet');
    });

    test('returns 404 for a non-existent file', async ({ request }) => {
      const response = await request.get('/api/file/does-not-exist.html');
      expect(response.status()).toBe(404);
      const body = await response.json();
      expect(body).toHaveProperty('error');
    });

    test('does not expose the full system path in the response', async ({ request }) => {
      const response = await request.get('/api/file/sample.html');
      const body = await response.json();
      // The 'path' field should be the relative path, not an absolute system path
      expect(body.path).not.toMatch(/^\/home|^C:\\/);
    });
  });

  test.describe('POST /api/format', () => {
    test('formats a JSON file and returns success', async ({ request }) => {
      const response = await request.post('/api/format', {
        data: { filepath: 'sample.json', extension: '.json' },
      });
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body.success).toBe(true);
    });

    test('returns 400 when filepath or extension is missing', async ({ request }) => {
      const response = await request.post('/api/format', {
        data: { filepath: 'sample.json' }, // missing extension
      });
      expect(response.status()).toBe(400);
    });

    test('returns 400 for unsupported file type', async ({ request }) => {
      const response = await request.post('/api/format', {
        data: { filepath: 'sample.py', extension: '.py' },
      });
      expect(response.status()).toBe(400);
      const body = await response.json();
      expect(body.success).toBe(false);
    });
  });
});
