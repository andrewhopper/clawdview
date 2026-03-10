// File UUID: 5a808cba-e6ff-47bf-8464-dbef598ebe96
/**
 * Playwright performance tests for design agent HTML outputs.
 *
 * Measures actual browser paint time metrics:
 * - First Contentful Paint (FCP)
 * - Largest Contentful Paint (LCP)
 * - Cumulative Layout Shift (CLS)
 * - DOM content loaded time
 * - Total file size
 *
 * Usage:
 *   npx playwright test paint-time.spec.ts
 *   npx playwright test paint-time.spec.ts --headed  # watch in browser
 *
 * Environment variables:
 *   ASSET_PATH  - Path to HTML file to test (required)
 *   FCP_LIMIT   - Max First Contentful Paint in ms (default: 1800)
 *   LCP_LIMIT   - Max Largest Contentful Paint in ms (default: 2500)
 *   CLS_LIMIT   - Max Cumulative Layout Shift (default: 0.1)
 *   SIZE_LIMIT  - Max file size in KB (default: 100)
 */
// File UUID: 5f6a7b8c-9d0e-1f2a-3b4c-5d6e7f8a9b0c

import { test, expect } from '@playwright/test';
import { readFileSync, statSync } from 'fs';
import { resolve } from 'path';

// Configuration from environment
const ASSET_PATH = process.env.ASSET_PATH || '';
const FCP_LIMIT = parseInt(process.env.FCP_LIMIT || '1800', 10);
const LCP_LIMIT = parseInt(process.env.LCP_LIMIT || '2500', 10);
const CLS_LIMIT = parseFloat(process.env.CLS_LIMIT || '0.1');
const SIZE_LIMIT_KB = parseInt(process.env.SIZE_LIMIT || '100', 10);

interface PerformanceMetrics {
  fcp: number;
  lcp: number;
  cls: number;
  domContentLoaded: number;
  domComplete: number;
  domNodeCount: number;
  domDepth: number;
  externalResources: number;
  inlineStyleCount: number;
}

interface FileSizeMetrics {
  sizeBytes: number;
  sizeKB: number;
  lineCount: number;
}

test.describe('Design Agent Output - Paint Time & File Size', () => {

  test.beforeAll(() => {
    if (!ASSET_PATH) {
      console.log('Set ASSET_PATH environment variable to test a specific file.');
      console.log('Example: ASSET_PATH=./fixtures/valid_html_asset.html npx playwright test');
    }
  });

  test('file size is within limits', async () => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const stats = statSync(filePath);
    const content = readFileSync(filePath, 'utf-8');

    const metrics: FileSizeMetrics = {
      sizeBytes: stats.size,
      sizeKB: Math.round(stats.size / 1024 * 10) / 10,
      lineCount: content.split('\n').length,
    };

    console.log(`File size: ${metrics.sizeKB} KB (${metrics.lineCount} lines)`);
    console.log(`Limit: ${SIZE_LIMIT_KB} KB`);

    expect(metrics.sizeKB).toBeLessThanOrEqual(SIZE_LIMIT_KB);
  });

  test('First Contentful Paint is within threshold', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const fileUrl = `file://${filePath}`;

    // Navigate and wait for load
    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    // Measure FCP via Performance Observer
    const fcp = await page.evaluate(() => {
      return new Promise<number>((resolve) => {
        const entries = performance.getEntriesByName('first-contentful-paint');
        if (entries.length > 0) {
          resolve(entries[0].startTime);
        } else {
          // Fallback: use PerformanceObserver
          const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
              if (entry.name === 'first-contentful-paint') {
                resolve(entry.startTime);
                observer.disconnect();
              }
            }
          });
          observer.observe({ entryTypes: ['paint'] });

          // Timeout after 5s
          setTimeout(() => resolve(-1), 5000);
        }
      });
    });

    console.log(`FCP: ${Math.round(fcp)}ms (limit: ${FCP_LIMIT}ms)`);

    if (fcp > 0) {
      expect(fcp).toBeLessThanOrEqual(FCP_LIMIT);
    }
  });

  test('DOM metrics are reasonable', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const fileUrl = `file://${filePath}`;

    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    const metrics = await page.evaluate(() => {
      // Count DOM nodes
      const domNodeCount = document.querySelectorAll('*').length;

      // Calculate max DOM depth
      function getMaxDepth(el: Element, depth: number): number {
        let maxD = depth;
        for (const child of el.children) {
          maxD = Math.max(maxD, getMaxDepth(child, depth + 1));
        }
        return maxD;
      }
      const domDepth = getMaxDepth(document.documentElement, 0);

      // Count external resources
      const scripts = document.querySelectorAll('script[src]').length;
      const links = document.querySelectorAll('link[href]').length;
      const images = document.querySelectorAll('img[src]').length;
      const externalResources = scripts + links + images;

      // Count inline styles
      const inlineStyleCount = document.querySelectorAll('[style]').length;

      // Navigation timing
      const timing = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;

      return {
        domNodeCount,
        domDepth,
        externalResources,
        inlineStyleCount,
        domContentLoaded: timing ? timing.domContentLoadedEventEnd - timing.startTime : -1,
        domComplete: timing ? timing.domComplete - timing.startTime : -1,
      };
    });

    console.log('DOM Metrics:');
    console.log(`  Nodes: ${metrics.domNodeCount}`);
    console.log(`  Max depth: ${metrics.domDepth}`);
    console.log(`  External resources: ${metrics.externalResources}`);
    console.log(`  Inline styles: ${metrics.inlineStyleCount}`);
    console.log(`  DOM Content Loaded: ${Math.round(metrics.domContentLoaded)}ms`);
    console.log(`  DOM Complete: ${Math.round(metrics.domComplete)}ms`);

    // Assertions
    expect(metrics.domNodeCount).toBeLessThan(1500);  // Reasonable for a mockup
    expect(metrics.domDepth).toBeLessThan(15);         // Avoid deep nesting
    expect(metrics.inlineStyleCount).toBeLessThan(20); // Prefer classes
  });

  test('Cumulative Layout Shift is minimal', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const fileUrl = `file://${filePath}`;

    // Set up CLS observer before navigation
    await page.addInitScript(() => {
      (window as any).__clsValue = 0;
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!(entry as any).hadRecentInput) {
            (window as any).__clsValue += (entry as any).value;
          }
        }
      });
      observer.observe({ entryTypes: ['layout-shift'] });
    });

    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    // Wait a moment for any shifts to settle
    await page.waitForTimeout(1000);

    const cls = await page.evaluate(() => (window as any).__clsValue || 0);

    console.log(`CLS: ${cls.toFixed(4)} (limit: ${CLS_LIMIT})`);

    expect(cls).toBeLessThanOrEqual(CLS_LIMIT);
  });

  test('Largest Contentful Paint is within threshold', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const fileUrl = `file://${filePath}`;

    // Set up LCP observer before navigation
    await page.addInitScript(() => {
      (window as any).__lcpValue = 0;
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        (window as any).__lcpValue = lastEntry.startTime;
      });
      observer.observe({ entryTypes: ['largest-contentful-paint'] });
    });

    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    // Wait for LCP to settle
    await page.waitForTimeout(500);

    const lcp = await page.evaluate(() => (window as any).__lcpValue || 0);

    console.log(`LCP: ${Math.round(lcp)}ms (limit: ${LCP_LIMIT}ms)`);

    if (lcp > 0) {
      expect(lcp).toBeLessThanOrEqual(LCP_LIMIT);
    }
  });

  test('page renders visible content', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const fileUrl = `file://${filePath}`;

    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    // Check body is visible and has content
    const body = page.locator('body');
    await expect(body).toBeVisible();

    // Page should have some text content
    const textContent = await body.textContent();
    expect(textContent?.trim().length).toBeGreaterThan(0);

    // No console errors
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    // Reload to capture console errors
    await page.reload({ waitUntil: 'networkidle' });
    expect(errors).toHaveLength(0);
  });
});

// =============================================================================
// Responsive Viewport Tests
// =============================================================================

test.describe('Design Agent Output - Responsive Design', () => {

  const viewports = {
    phone: { width: 375, height: 667, name: 'iPhone SE' },
    tablet_vertical: { width: 768, height: 1024, name: 'iPad Portrait' },
    tablet_horizontal: { width: 1024, height: 768, name: 'iPad Landscape' },
    desktop: { width: 1440, height: 900, name: 'Desktop' },
  };

  for (const [viewportName, viewport] of Object.entries(viewports)) {
    test(`renders correctly on ${viewport.name} (${viewport.width}x${viewport.height})`, async ({ page }) => {
      test.skip(!ASSET_PATH, 'No ASSET_PATH set');

      const filePath = resolve(ASSET_PATH);
      const fileUrl = `file://${filePath}`;

      // Set viewport
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto(fileUrl, { waitUntil: 'networkidle' });

      // Check body is visible
      const body = page.locator('body');
      await expect(body).toBeVisible();

      // Check for horizontal overflow (bad for mobile)
      const hasHorizontalOverflow = await page.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
      });

      if (viewportName === 'phone' || viewportName === 'tablet_vertical') {
        expect(hasHorizontalOverflow).toBe(false);
      }

      // Check that content is readable (not too small)
      const fontSizes = await page.evaluate(() => {
        const elements = document.querySelectorAll('p, span, a, button, li, td, th, label');
        const sizes: number[] = [];
        elements.forEach(el => {
          const size = parseFloat(window.getComputedStyle(el).fontSize);
          if (size > 0) sizes.push(size);
        });
        return sizes;
      });

      // Minimum readable font size is 12px
      const tooSmall = fontSizes.filter(s => s < 12);
      expect(tooSmall.length).toBeLessThan(fontSizes.length * 0.1); // < 10% too small

      // Check touch targets on mobile
      if (viewportName === 'phone' || viewportName.includes('tablet')) {
        const smallTouchTargets = await page.evaluate(() => {
          const interactive = document.querySelectorAll('a, button, input, select, textarea, [role="button"]');
          let small = 0;
          interactive.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.width < 44 || rect.height < 44) {
              small++;
            }
          });
          return { small, total: interactive.length };
        });

        console.log(`${viewport.name}: ${smallTouchTargets.small}/${smallTouchTargets.total} touch targets < 44px`);
        // Warn if more than 20% of touch targets are too small
        if (smallTouchTargets.total > 0) {
          expect(smallTouchTargets.small / smallTouchTargets.total).toBeLessThan(0.2);
        }
      }

      console.log(`✓ ${viewport.name}: Passed responsive checks`);
    });
  }

  test('viewport meta tag is present', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const content = readFileSync(filePath, 'utf-8');

    // Check for viewport meta tag
    const hasViewportMeta = /<meta[^>]*name=["']viewport["'][^>]*>/i.test(content);

    expect(hasViewportMeta).toBe(true);
  });

  test('uses responsive Tailwind classes', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const content = readFileSync(filePath, 'utf-8');

    // Check for responsive prefixes
    const responsivePrefixes = ['sm:', 'md:', 'lg:', 'xl:', '2xl:'];
    const foundPrefixes = responsivePrefixes.filter(p => content.includes(p));

    console.log(`Responsive prefixes found: ${foundPrefixes.join(', ') || 'none'}`);

    // At least some responsive classes should be present for non-trivial components
    if (content.length > 1000) {
      expect(foundPrefixes.length).toBeGreaterThan(0);
    }
  });
});

// =============================================================================
// Typography & Contrast Tests
// =============================================================================

test.describe('Design Agent Output - Typography & Contrast', () => {

  test('font sizes meet minimum readable size', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const fileUrl = `file://${filePath}`;

    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    const fontAnalysis = await page.evaluate(() => {
      const textElements = document.querySelectorAll('p, span, a, button, li, td, th, label, h1, h2, h3, h4, h5, h6');
      const sizes: { element: string; size: number }[] = [];

      textElements.forEach(el => {
        const size = parseFloat(window.getComputedStyle(el).fontSize);
        if (size > 0) {
          sizes.push({ element: el.tagName.toLowerCase(), size });
        }
      });

      return sizes;
    });

    console.log('Font sizes found:');
    const sizeGroups: Record<number, number> = {};
    fontAnalysis.forEach(f => {
      sizeGroups[f.size] = (sizeGroups[f.size] || 0) + 1;
    });
    Object.entries(sizeGroups).sort((a, b) => parseFloat(a[0]) - parseFloat(b[0])).forEach(([size, count]) => {
      console.log(`  ${size}px: ${count} elements`);
    });

    // Check minimum font size (12px)
    const tooSmall = fontAnalysis.filter(f => f.size < 12);
    expect(tooSmall.length).toBe(0);
  });

  test('text has sufficient color contrast', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const fileUrl = `file://${filePath}`;

    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    // Check for low contrast issues using computed styles
    const contrastIssues = await page.evaluate(() => {
      const issues: string[] = [];
      const elements = document.querySelectorAll('p, span, a, button, h1, h2, h3, h4, h5, h6');

      elements.forEach(el => {
        const style = window.getComputedStyle(el);
        const color = style.color;
        const bgColor = style.backgroundColor;

        // Parse RGB values
        const parseRgb = (c: string) => {
          const match = c.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
          if (match) {
            return { r: parseInt(match[1]), g: parseInt(match[2]), b: parseInt(match[3]) };
          }
          return null;
        };

        const fg = parseRgb(color);
        const bg = parseRgb(bgColor);

        if (fg && bg) {
          // Calculate relative luminance
          const getLuminance = (rgb: { r: number; g: number; b: number }) => {
            const [r, g, b] = [rgb.r, rgb.g, rgb.b].map(v => {
              v /= 255;
              return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
            });
            return 0.2126 * r + 0.7152 * g + 0.0722 * b;
          };

          const l1 = getLuminance(fg);
          const l2 = getLuminance(bg);
          const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);

          if (ratio < 4.5) {
            issues.push(`${el.tagName}: ${ratio.toFixed(2)}:1 contrast`);
          }
        }
      });

      return issues;
    });

    console.log(`Contrast check: ${contrastIssues.length} issues found`);
    if (contrastIssues.length > 0) {
      console.log('Issues:', contrastIssues.slice(0, 5).join(', '));
    }

    // Allow some issues but not too many
    expect(contrastIssues.length).toBeLessThan(5);
  });

  test('uses design system text colors', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const content = readFileSync(filePath, 'utf-8');

    // Check for raw hex colors in color/fill properties
    const rawColorPattern = /(?:color|fill):\s*#[0-9a-fA-F]{3,8}/gi;
    const rawColors = content.match(rawColorPattern) || [];

    // Filter out colors in comments
    const actualViolations = rawColors.filter(c => {
      const idx = content.indexOf(c);
      const before = content.substring(Math.max(0, idx - 50), idx);
      return !before.includes('NEVER') && !before.includes('❌') && !before.includes('bad');
    });

    console.log(`Raw color declarations: ${actualViolations.length}`);
    expect(actualViolations.length).toBe(0);
  });

  test('heading hierarchy is correct', async ({ page }) => {
    test.skip(!ASSET_PATH, 'No ASSET_PATH set');

    const filePath = resolve(ASSET_PATH);
    const fileUrl = `file://${filePath}`;

    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    const headingAnalysis = await page.evaluate(() => {
      const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
      const levels: number[] = [];
      const issues: string[] = [];

      headings.forEach((h, i) => {
        const level = parseInt(h.tagName[1]);
        levels.push(level);

        // Check for skipped levels (e.g., h1 -> h3)
        if (i > 0 && level > levels[i - 1] + 1) {
          issues.push(`Skipped heading level: h${levels[i - 1]} -> h${level}`);
        }
      });

      return { levels, issues };
    });

    console.log(`Heading levels: ${headingAnalysis.levels.join(' -> ')}`);
    if (headingAnalysis.issues.length > 0) {
      console.log('Heading issues:', headingAnalysis.issues);
    }

    // Should not skip heading levels
    expect(headingAnalysis.issues.length).toBe(0);
  });
});

test.describe('Design Agent Output - Batch Performance Validation', () => {

  test('generate performance report for fixture files', async ({ page }) => {
    const fixtureDir = resolve(__dirname, 'fixtures');
    const validHtml = resolve(fixtureDir, 'valid_html_asset.html');

    // Only run if fixtures exist
    try {
      statSync(validHtml);
    } catch {
      test.skip(true, 'No fixture files found');
      return;
    }

    const fileUrl = `file://${validHtml}`;
    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    const stats = statSync(validHtml);
    const content = readFileSync(validHtml, 'utf-8');

    const domMetrics = await page.evaluate(() => {
      const nodeCount = document.querySelectorAll('*').length;
      const inlineStyles = document.querySelectorAll('[style]').length;

      function getMaxDepth(el: Element, d: number): number {
        let m = d;
        for (const c of el.children) { m = Math.max(m, getMaxDepth(c, d + 1)); }
        return m;
      }

      return {
        nodeCount,
        inlineStyles,
        maxDepth: getMaxDepth(document.documentElement, 0),
      };
    });

    console.log('\n=== Performance Report: valid_html_asset.html ===');
    console.log(`File size: ${Math.round(stats.size / 1024 * 10) / 10} KB`);
    console.log(`Lines: ${content.split('\n').length}`);
    console.log(`DOM nodes: ${domMetrics.nodeCount}`);
    console.log(`DOM depth: ${domMetrics.maxDepth}`);
    console.log(`Inline styles: ${domMetrics.inlineStyles}`);
    console.log('================================================\n');

    // Basic sanity checks
    expect(stats.size).toBeLessThan(150 * 1024); // 150KB max
    expect(domMetrics.nodeCount).toBeLessThan(1500);
    expect(domMetrics.maxDepth).toBeLessThan(15);
  });
});
