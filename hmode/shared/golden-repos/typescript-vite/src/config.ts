/**
 * Configuration management with multi-environment support.
 */

import { z } from 'zod';

const environments = ['local', 'dev', 'integration', 'stage', 'prod'] as const;
type Environment = (typeof environments)[number];

const configSchema = z.object({
  // Environment
  ENV: z.enum(environments).default('local'),

  // Application
  APP_NAME: z.string().default('vite-app'),
  APP_VERSION: z.string().default('0.1.0'),
  DEBUG: z.boolean().default(false),

  // API
  API_URL: z.string().url().optional(),

  // Logging
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),

  // Feature flags
  ENABLE_ANALYTICS: z.boolean().default(false),
  ENABLE_DEVTOOLS: z.boolean().default(false),
});

export type Config = z.infer<typeof configSchema>;

/**
 * Parse configuration from environment object.
 */
export function parseConfig(env: Record<string, unknown>): Config {
  const transformed = {
    ENV: env.VITE_ENV ?? env.ENV,
    APP_NAME: env.VITE_APP_NAME ?? env.APP_NAME,
    APP_VERSION: env.VITE_APP_VERSION ?? env.APP_VERSION,
    DEBUG: env.VITE_DEBUG === 'true' || env.DEBUG === 'true',
    API_URL: env.VITE_API_URL ?? env.API_URL,
    LOG_LEVEL: env.VITE_LOG_LEVEL ?? env.LOG_LEVEL,
    ENABLE_ANALYTICS: env.VITE_ENABLE_ANALYTICS === 'true',
    ENABLE_DEVTOOLS: env.VITE_ENABLE_DEVTOOLS === 'true',
  };

  const result = configSchema.safeParse(transformed);

  if (!result.success) {
    console.error('Configuration error:', result.error.format());
    throw new Error('Invalid configuration');
  }

  // Apply environment-specific defaults
  const config = result.data;
  if (config.ENV === 'local' || config.ENV === 'dev') {
    config.DEBUG = config.DEBUG ?? true;
    config.ENABLE_DEVTOOLS = config.ENABLE_DEVTOOLS ?? true;
  }

  return config;
}

let _config: Config | null = null;

export function getConfig(): Config {
  if (!_config) {
    _config = parseConfig(import.meta.env);
  }
  return _config;
}

export function isProduction(): boolean {
  return getConfig().ENV === 'prod';
}

export function isLocal(): boolean {
  return getConfig().ENV === 'local';
}

export function isDevelopment(): boolean {
  const env = getConfig().ENV;
  return env === 'local' || env === 'dev';
}

export function getEnvironment(): Environment {
  return getConfig().ENV;
}
