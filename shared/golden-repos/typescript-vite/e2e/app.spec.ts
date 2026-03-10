import { test, expect } from '@playwright/test';

test.describe('Vite App', () => {
  test('should load the application', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('body')).toBeVisible();
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

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    await expect(page.locator('body')).toBeVisible();
  });
});
