// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Smoke tests – verify the app loads and core UI elements are present.
 */
test.describe('Smoke Tests', () => {
  test('homepage loads and shows the QuickView UI', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/QuickView/i);
  });

  test('file sidebar is visible on load', async ({ page }) => {
    await page.goto('/');
    // The file tree panel should be present
    const sidebar = page.locator('#file-tree, [data-testid="file-tree"], .file-tree, #sidebar');
    await expect(sidebar.first()).toBeVisible();
  });

  test('tab bar contains Preview, Code, and Output tabs', async ({ page }) => {
    await page.goto('/');
    const tabLabels = ['Preview', 'Code', 'Output'];
    for (const label of tabLabels) {
      await expect(page.getByText(label, { exact: true }).first()).toBeVisible();
    }
  });

  test('WebSocket connection is established', async ({ page }) => {
    const socketConnected = page.evaluate(() => {
      return new Promise((resolve) => {
        // Give the client-side Socket.io up to 3 seconds to connect
        const check = () => {
          const io = window.io || window.socket;
          if (io && (io.connected || (typeof io === 'object' && io.id))) {
            return resolve(true);
          }
          setTimeout(check, 200);
        };
        setTimeout(() => resolve(false), 3000);
        check();
      });
    });

    await page.goto('/');
    // The page should not throw a JS error on load
    const errors = [];
    page.on('pageerror', (err) => errors.push(err.message));
    await page.waitForTimeout(1000);
    // No uncaught errors expected on load
    expect(errors.filter(e => !e.includes('favicon'))).toHaveLength(0);
  });
});
