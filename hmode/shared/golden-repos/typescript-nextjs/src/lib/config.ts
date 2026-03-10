/**
 * Application configuration with multi-environment support.
 */

import { z } from 'zod';

const environments = ['local', 'dev', 'integration', 'stage', 'prod'] as const;
type Environment = (typeof environments)[number];

const envSchema = z.object({
  // Environment
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  NEXT_PUBLIC_ENV: z.enum(environments).default('local'),

  // Application
  NEXT_PUBLIC_APP_NAME: z.string().default('Next.js App'),
  NEXT_PUBLIC_APP_VERSION: z.string().default('0.1.0'),
  NEXT_PUBLIC_API_URL: z.string().url().optional(),

  // Feature flags
  NEXT_PUBLIC_ENABLE_ANALYTICS: z
    .string()
    .transform((val) => val === 'true')
    .default('false'),
  NEXT_PUBLIC_ENABLE_DEBUG: z
    .string()
    .transform((val) => val === 'true')
    .default('false'),
});

export type Config = z.infer<typeof envSchema>;

function getConfig(): Config {
  const result = envSchema.safeParse({
    NODE_ENV: process.env.NODE_ENV,
    NEXT_PUBLIC_ENV: process.env.NEXT_PUBLIC_ENV,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
    NEXT_PUBLIC_APP_VERSION: process.env.NEXT_PUBLIC_APP_VERSION,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_ENABLE_ANALYTICS: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS,
    NEXT_PUBLIC_ENABLE_DEBUG: process.env.NEXT_PUBLIC_ENABLE_DEBUG,
  });

  if (!result.success) {
    console.error('Invalid environment configuration:', result.error.format());
    throw new Error('Invalid environment configuration');
  }

  return result.data;
}

export const config = getConfig();

export const isProduction = config.NEXT_PUBLIC_ENV === 'prod';
export const isLocal = config.NEXT_PUBLIC_ENV === 'local';
export const isDevelopment = config.NEXT_PUBLIC_ENV === 'local' || config.NEXT_PUBLIC_ENV === 'dev';
export const getEnvironment = (): Environment => config.NEXT_PUBLIC_ENV;
