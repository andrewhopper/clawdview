import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should load the home page', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Next/);
  });

  test('should be accessible', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  });

  test('should be responsive', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('main')).toBeVisible();
  });
});

test.describe('Health Endpoint', () => {
  test('should return healthy status', async ({ request }) => {
    const response = await request.get('/api/health');
    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    expect(body.status).toBe('healthy');
  });
});
