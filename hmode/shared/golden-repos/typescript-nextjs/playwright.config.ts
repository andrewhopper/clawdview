import { defineConfig } from '@playwright/test';
import { allProjects, commonSettings } from '../playwright.devices';

/**
 * Playwright configuration for E2E testing.
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './e2e',
  ...commonSettings,
  use: {
    ...commonSettings.use,
    baseURL: 'http://localhost:3000',
  },
  projects: allProjects,
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
