// File UUID: 3e8f7b2c-4d1a-4e8f-9c3b-7e6d5f4a3b2c

import { SSMResolver } from './index';

describe('SSMResolver', () => {
  describe('path generation', () => {
    const config = {
      accountType: 'work' as const,
      environment: 'dev' as const,
      project: 'gocoder',
    };

    // Create mock scope
    const mockScope = {} as any;
    const resolver = new SSMResolver(mockScope, config);

    test('generates project-scoped path', () => {
      expect(resolver.path('auth', 'google-client-id', 'project')).toBe(
        '/work/dev/gocoder/auth/google-client-id'
      );
    });

    test('generates environment-scoped path', () => {
      expect(resolver.path('auth', 'google-client-id', 'environment')).toBe(
        '/work/dev/auth/google-client-id'
      );
    });

    test('generates account-scoped path', () => {
      expect(resolver.path('auth', 'google-client-id', 'account')).toBe(
        '/work/auth/google-client-id'
      );
    });

    test('generates shared-scoped path', () => {
      expect(resolver.path('auth', 'google-client-id', 'shared')).toBe(
        '/shared/auth/google-client-id'
      );
    });

    test('handles nested categories', () => {
      expect(resolver.path('auth/cognito', 'user-pool-id', 'project')).toBe(
        '/work/dev/gocoder/auth/cognito/user-pool-id'
      );
    });
  });

  describe('fallback chain', () => {
    const config = {
      accountType: 'work' as const,
      environment: 'prod' as const,
      project: 'ppm',
    };

    const mockScope = {} as any;
    const resolver = new SSMResolver(mockScope, config);

    test('builds correct fallback order', () => {
      // Access private method for testing via type assertion
      const chain = (resolver as any).buildFallbackChain('auth', 'client-id');

      expect(chain).toEqual([
        '/work/prod/ppm/auth/client-id',      // Most specific
        '/work/prod/auth/client-id',           // Environment
        '/work/auth/client-id',                // Account
        '/shared/auth/client-id',              // Shared (most general)
      ]);
    });
  });

  describe('configuration', () => {
    test('stores configuration correctly', () => {
      const mockScope = {} as any;
      const config = {
        accountType: 'personal' as const,
        environment: 'dev' as const,
        project: 'test-app',
      };

      const resolver = new SSMResolver(mockScope, config);
      const storedConfig = resolver.getConfig();

      expect(storedConfig).toEqual(config);
    });
  });

  describe('ID sanitization', () => {
    const mockScope = {} as any;
    const config = {
      accountType: 'work' as const,
      environment: 'dev' as const,
      project: 'test',
    };

    const resolver = new SSMResolver(mockScope, config);

    test('sanitizes special characters in category', () => {
      // This would create a CDK construct ID, so we can't directly test sanitizeId
      // but we can verify paths with special chars work
      expect(resolver.path('auth/google', 'client-id', 'project')).toBe(
        '/work/dev/test/auth/google/client-id'
      );
    });
  });

  describe('description generation', () => {
    const mockScope = {} as any;
    const config = {
      accountType: 'work' as const,
      environment: 'dev' as const,
      project: 'gocoder',
    };

    const resolver = new SSMResolver(mockScope, config);

    test('generates description with scope info', () => {
      const desc = (resolver as any).generateDescription('auth', 'client-id', 'project');
      expect(desc).toContain('work/dev/gocoder');
      expect(desc).toContain('auth/client-id');
      expect(desc).toContain('project');
    });
  });
});
