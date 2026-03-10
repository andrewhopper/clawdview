import { describe, it, expect } from 'vitest';
import { parseConfig } from '../src/config';

describe('parseConfig', () => {
  it('uses default values', () => {
    const config = parseConfig({});
    expect(config.APP_NAME).toBe('vite-app');
    expect(config.DEBUG).toBe(false);
    expect(config.LOG_LEVEL).toBe('info');
  });

  it('reads VITE_ prefixed variables', () => {
    const config = parseConfig({
      VITE_APP_NAME: 'my-app',
      VITE_DEBUG: 'true',
      VITE_LOG_LEVEL: 'debug',
    });
    expect(config.APP_NAME).toBe('my-app');
    expect(config.DEBUG).toBe(true);
    expect(config.LOG_LEVEL).toBe('debug');
  });

  it('reads non-prefixed variables', () => {
    const config = parseConfig({
      APP_NAME: 'test-app',
      DEBUG: 'true',
    });
    expect(config.APP_NAME).toBe('test-app');
    expect(config.DEBUG).toBe(true);
  });

  it('throws on invalid config', () => {
    expect(() =>
      parseConfig({ VITE_LOG_LEVEL: 'invalid' })
    ).toThrow();
  });
});
