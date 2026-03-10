/**
 * Configuration management with multi-environment support.
 */

import { config as dotenvConfig } from 'dotenv';
import { z } from 'zod';

// Load .env file
dotenvConfig();

const environments = ['local', 'dev', 'integration', 'stage', 'prod'] as const;
type Environment = (typeof environments)[number];

const envSchema = z.object({
  // Environment
  NODE_ENV: z.enum(environments).default('local'),

  // Application
  APP_NAME: z.string().default('nodejs-app'),
  APP_VERSION: z.string().default('0.1.0'),
  DEBUG: z
    .string()
    .transform((val) => val === 'true')
    .default('false'),

  // Logging
  LOG_LEVEL: z
    .enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace'])
    .default('info'),
  LOG_FORMAT: z.enum(['json', 'pretty']).default('pretty'),

  // Server
  PORT: z.coerce.number().default(3000),
  HOST: z.string().default('0.0.0.0'),

  // Database (optional)
  DATABASE_URL: z.string().optional(),

  // Redis (optional)
  REDIS_URL: z.string().optional(),

  // Feature flags
  ENABLE_METRICS: z
    .string()
    .transform((val) => val === 'true')
    .default('false'),
  ENABLE_TRACING: z
    .string()
    .transform((val) => val === 'true')
    .default('false'),
});

export type Config = z.infer<typeof envSchema>;

let configInstance: Config | null = null;

/**
 * Get validated configuration from environment variables.
 */
export function getConfig(): Config {
  if (!configInstance) {
    const result = envSchema.safeParse(process.env);

    if (!result.success) {
      console.error('❌ Invalid environment configuration:');
      console.error(result.error.format());
      process.exit(1);
    }

    configInstance = result.data;

    // Apply environment-specific defaults
    if (configInstance.LOG_FORMAT === 'pretty' && !isLocal()) {
      configInstance = { ...configInstance, LOG_FORMAT: 'json' };
    }
  }

  return configInstance;
}

/**
 * Check if running in production environment.
 */
export function isProduction(): boolean {
  return getConfig().NODE_ENV === 'prod';
}

/**
 * Check if running in local environment.
 */
export function isLocal(): boolean {
  return getConfig().NODE_ENV === 'local';
}

/**
 * Check if running in development environment (local or dev).
 */
export function isDevelopment(): boolean {
  const env = getConfig().NODE_ENV;
  return env === 'local' || env === 'dev';
}

/**
 * Get current environment.
 */
export function getEnvironment(): Environment {
  return getConfig().NODE_ENV;
}
