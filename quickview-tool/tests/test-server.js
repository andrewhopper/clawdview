/**
 * Test server launcher for Playwright e2e tests.
 * Starts QuickView on port 3334, watching the tests/fixtures directory.
 */
const path = require('path');

// Use tsx to load TypeScript source
try { require('tsx/cjs'); } catch {}

let QuickViewServer;
try {
  ({ QuickViewServer } = require('../src/server/server'));
} catch {
  ({ QuickViewServer } = require('../dist/server/server'));
}

const server = new QuickViewServer({
  port: 3334,
  watchDir: path.join(__dirname, 'fixtures'),
});

server.start();

process.on('SIGINT', () => {
  server.stop();
  process.exit(0);
});

process.on('SIGTERM', () => {
  server.stop();
  process.exit(0);
});
