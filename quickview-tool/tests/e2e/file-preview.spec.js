// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * File preview tests – verify that selecting a file renders the correct
 * preview content in the Preview, Code, and Output tabs.
 */
test.describe('File Preview', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForTimeout(500);
  });

  test.describe('HTML preview', () => {
    test('renders HTML file inside an iframe', async ({ page }) => {
      await page.getByText('sample.html').first().click();
      await page.waitForTimeout(300);

      // Click the Preview tab to make sure it's active
      await page.getByText('Preview', { exact: true }).first().click();
      await page.waitForTimeout(300);

      // An iframe should be present in the preview area
      const iframe = page.locator('iframe').first();
      await expect(iframe).toBeVisible();
    });

    test('HTML preview iframe contains the fixture heading', async ({ page }) => {
      await page.getByText('sample.html').first().click();
      await page.waitForTimeout(500);
      await page.getByText('Preview', { exact: true }).first().click();
      await page.waitForTimeout(500);

      const iframeLocator = page.frameLocator('iframe').first();
      await expect(iframeLocator.getByText('Sample HTML File')).toBeVisible();
    });
  });

  test.describe('Code tab', () => {
    test('Code tab shows raw file content', async ({ page }) => {
      await page.getByText('sample.json').first().click();
      await page.waitForTimeout(300);
      await page.getByText('Code', { exact: true }).first().click();
      await page.waitForTimeout(300);

      // The code panel should contain the JSON key we put in the fixture
      await expect(page.getByText('QuickView Test Fixture').first()).toBeVisible();
    });

    test('Code tab shows Python source', async ({ page }) => {
      await page.getByText('sample.py').first().click();
      await page.waitForTimeout(300);
      await page.getByText('Code', { exact: true }).first().click();
      await page.waitForTimeout(300);

      await expect(page.getByText('def greet').first()).toBeVisible();
    });
  });

  test.describe('Markdown preview', () => {
    test('Markdown file renders formatted HTML in preview', async ({ page }) => {
      await page.getByText('sample.md').first().click();
      await page.waitForTimeout(300);
      await page.getByText('Preview', { exact: true }).first().click();
      await page.waitForTimeout(300);

      // The rendered markdown heading should appear in the preview area
      await expect(page.getByText('Sample Markdown Fixture').first()).toBeVisible();
    });
  });

  test.describe('Python execution', () => {
    test('clicking Run executes the script and shows output', async ({ page }) => {
      await page.getByText('sample.py').first().click();
      await page.waitForTimeout(300);

      const runButton = page.getByRole('button', { name: /run/i });
      await runButton.click();

      // Switch to Output tab to see the result
      await page.getByText('Output', { exact: true }).first().click();
      await page.waitForTimeout(2000); // Allow time for Python to execute

      // The fixture script prints "Hello, QuickView!" and "Fixture script complete."
      await expect(page.getByText('Hello, QuickView!').first()).toBeVisible();
    });
  });
});
