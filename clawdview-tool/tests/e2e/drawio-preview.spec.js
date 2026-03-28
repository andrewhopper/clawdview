// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Draw.io preview tests – verify that .drawio files render via the
 * diagrams.net viewer-static.min.js inside an iframe.
 */
test.describe('Draw.io Preview', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForTimeout(500);
  });

  test('renders drawio file inside an iframe', async ({ page }) => {
    await page.getByText('sample.drawio').first().click();
    await page.waitForTimeout(300);

    // Tab text includes emoji prefix, so use substring match
    await page.getByRole('tab', { name: /Preview/ }).first().click();
    await page.waitForTimeout(300);

    const iframe = page.locator('iframe[title="Draw.io Preview"]');
    await expect(iframe).toBeVisible();
  });

  test('iframe loads the viewer and renders the diagram', async ({ page }) => {
    await page.getByText('sample.drawio').first().click();
    await page.waitForTimeout(500);
    await page.getByRole('tab', { name: /Preview/ }).first().click();

    const frame = page.frameLocator('iframe[title="Draw.io Preview"]');

    // The viewer replaces the mxgraph div with rendered SVG content.
    // Wait for the viewer script to load and render (up to 15s for CDN fetch).
    await expect(frame.locator('svg').first()).toBeVisible({ timeout: 15000 });
  });

  test('drawio file is served with XML content via API', async ({ page }) => {
    const response = await page.request.get('/api/file/sample.drawio');
    const data = await response.json();
    expect(data.content).toContain('mxfile');
    expect(data.content).toContain('Hello ClawdView');
    expect(data.extension).toBe('.drawio');
  });
});
