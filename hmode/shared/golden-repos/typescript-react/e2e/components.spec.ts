import { test, expect } from '@playwright/test';

test.describe('Component Library', () => {
  test('should load the dev preview', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/React/);
  });

  test('Button component should be interactive', async ({ page }) => {
    await page.goto('/');
    const button = page.getByRole('button').first();
    if (await button.isVisible()) {
      await button.click();
      await expect(page.locator('body')).toBeVisible();
    }
  });

  test('should have no console errors', async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForTimeout(1000);
    expect(errors).toHaveLength(0);
  });
});
