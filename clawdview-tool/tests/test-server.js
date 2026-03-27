/**
 * Test server launcher for Playwright e2e tests.
 * Starts ClawdView on port 3334, watching the tests/fixtures directory.
 */
const path = require('path');

// Use tsx to load TypeScript source
try { require('tsx/cjs'); } catch {}

let ClawdViewServer;
try {
  ({ ClawdViewServer } = require('../src/server/server'));
} catch {
  ({ ClawdViewServer } = require('../dist/server/server'));
}

const server = new ClawdViewServer({
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
