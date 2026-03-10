// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Playwright configuration for QuickView e2e tests.
 * A dedicated test server is started automatically via webServer config,
 * pointing at tests/fixtures so real files are available during tests.
 */
module.exports = defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false, // Tests share a single server; run sequentially to avoid interference
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: [
    ['html', { outputFolder: 'tests/playwright-report', open: 'never' }],
    ['list'],
  ],
  use: {
    baseURL: 'http://localhost:3334', // Avoid conflict with dev server on 3333
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],

  // Start a dedicated test server pointing at the fixtures directory
  webServer: {
    command: 'node tests/test-server.js',
    url: 'http://localhost:3334',
    reuseExistingServer: !process.env.CI,
    timeout: 15000,
  },
});
