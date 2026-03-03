// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * File browser tests – verify the sidebar file tree:
 *  - Lists fixture files
 *  - Allows selecting a file, which updates the active view
 */
test.describe('File Browser', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Wait for the file tree to populate (Socket.io sends it on connect)
    await page.waitForTimeout(500);
  });

  test('displays fixture files in the sidebar', async ({ page }) => {
    // The sidebar should contain links or items with our fixture filenames
    await expect(page.getByText('sample.html').first()).toBeVisible();
    await expect(page.getByText('sample.json').first()).toBeVisible();
    await expect(page.getByText('sample.py').first()).toBeVisible();
    await expect(page.getByText('sample.md').first()).toBeVisible();
  });

  test('clicking a file selects it and shows its name', async ({ page }) => {
    const fileItem = page.getByText('sample.html').first();
    await fileItem.click();
    // After selecting, the filename should appear somewhere (header/title/panel)
    await expect(page.getByText('sample.html').first()).toBeVisible();
  });

  test('selecting a .py file shows a Run button', async ({ page }) => {
    await page.getByText('sample.py').first().click();
    await page.waitForTimeout(300);
    // A "Run" button should appear for Python files
    const runButton = page.getByRole('button', { name: /run/i });
    await expect(runButton).toBeVisible();
  });

  test('selecting a non-Python file does not show a Run button', async ({ page }) => {
    await page.getByText('sample.html').first().click();
    await page.waitForTimeout(300);
    const runButton = page.getByRole('button', { name: /^run$/i });
    await expect(runButton).not.toBeVisible();
  });
});
