/**
 * Tests for configuration module.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

describe('config', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    vi.resetModules();
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it('should use default values', async () => {
    const { getConfig } = await import('../src/config.js');
    const config = getConfig();

    expect(config.NODE_ENV).toBe('development');
    expect(config.APP_NAME).toBe('nodejs-app');
    expect(config.LOG_LEVEL).toBe('info');
  });

  it('should read from environment', async () => {
    process.env.NODE_ENV = 'production';
    process.env.APP_NAME = 'test-app';
    process.env.LOG_LEVEL = 'debug';

    const { getConfig } = await import('../src/config.js');
    const config = getConfig();

    expect(config.NODE_ENV).toBe('production');
    expect(config.APP_NAME).toBe('test-app');
    expect(config.LOG_LEVEL).toBe('debug');
  });
});
