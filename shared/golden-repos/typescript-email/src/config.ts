/**
 * Email configuration with multi-environment support.
 */

import { z } from 'zod';

const environments = ['local', 'dev', 'integration', 'stage', 'prod'] as const;
type Environment = (typeof environments)[number];

const configSchema = z.object({
  // Environment
  ENV: z.enum(environments).default('local'),

  // Email Provider
  RESEND_API_KEY: z.string().min(1),

  // Sender Defaults
  DEFAULT_FROM_EMAIL: z.string().email().default('noreply@example.com'),
  DEFAULT_FROM_NAME: z.string().default('My App'),

  // Application
  APP_URL: z.string().url().default('http://localhost:3000'),

  // Feature flags
  ENABLE_EMAIL_LOGGING: z.boolean().default(false),
  ENABLE_EMAIL_PREVIEW: z.boolean().default(false),

  // Development
  PREVIEW_EMAIL: z.string().email().optional(),
});

export type Config = z.infer<typeof configSchema>;

let _config: Config | null = null;

export function getConfig(): Config {
  if (!_config) {
    const result = configSchema.safeParse({
      ENV: process.env.ENV,
      RESEND_API_KEY: process.env.RESEND_API_KEY,
      DEFAULT_FROM_EMAIL: process.env.DEFAULT_FROM_EMAIL,
      DEFAULT_FROM_NAME: process.env.DEFAULT_FROM_NAME,
      APP_URL: process.env.APP_URL,
      ENABLE_EMAIL_LOGGING: process.env.ENABLE_EMAIL_LOGGING === 'true',
      ENABLE_EMAIL_PREVIEW: process.env.ENABLE_EMAIL_PREVIEW === 'true',
      PREVIEW_EMAIL: process.env.PREVIEW_EMAIL,
    });

    if (!result.success) {
      console.error('Configuration error:', result.error.format());
      throw new Error('Invalid email configuration');
    }

    _config = result.data;

    // Apply environment-specific defaults
    if (_config.ENV === 'local' || _config.ENV === 'dev') {
      _config.ENABLE_EMAIL_LOGGING = true;
      _config.ENABLE_EMAIL_PREVIEW = true;
    }
  }
  return _config;
}

export function getFromAddress(): string {
  const config = getConfig();
  return `${config.DEFAULT_FROM_NAME} <${config.DEFAULT_FROM_EMAIL}>`;
}

export function isProduction(): boolean {
  return getConfig().ENV === 'prod';
}

export function isLocal(): boolean {
  return getConfig().ENV === 'local';
}

export function shouldLogEmails(): boolean {
  return getConfig().ENABLE_EMAIL_LOGGING;
}

export function shouldPreviewEmails(): boolean {
  const config = getConfig();
  return config.ENABLE_EMAIL_PREVIEW && !!config.PREVIEW_EMAIL;
}
