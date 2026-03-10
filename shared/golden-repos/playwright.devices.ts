/**
 * Shared Playwright device configurations for all golden repos.
 * Import this in your playwright.config.ts to maintain consistency.
 */
import { devices } from '@playwright/test';

/** Desktop browser configurations */
export const desktopDevices = {
  chromium: { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  firefox: { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  webkit: { name: 'webkit', use: { ...devices['Desktop Safari'] } },
};

/** Mobile device configurations */
export const mobileDevices = {
  'mobile-chrome': { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
  'mobile-safari': { name: 'mobile-safari', use: { ...devices['iPhone 12'] } },
};

/** All devices combined */
export const allDevices = { ...desktopDevices, ...mobileDevices };

/** Desktop-only project list */
export const desktopProjects = Object.values(desktopDevices);

/** Mobile-only project list */
export const mobileProjects = Object.values(mobileDevices);

/** Full project list (desktop + mobile) */
export const allProjects = Object.values(allDevices);

/** Common Playwright settings */
export const commonSettings = {
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html' as const,
  use: {
    trace: 'on-first-retry' as const,
    screenshot: 'only-on-failure' as const,
  },
};
