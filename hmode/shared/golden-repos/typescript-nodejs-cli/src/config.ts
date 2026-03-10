/**
 * Configuration management using Zod for validation.
 */

import { z } from 'zod';
import 'dotenv/config';

const ConfigSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  LOG_LEVEL: z.enum(['trace', 'debug', 'info', 'warn', 'error', 'fatal']).default('info'),
});

export type Config = z.infer<typeof ConfigSchema>;

let config: Config | null = null;

export function getConfig(): Config {
  if (!config) {
    config = ConfigSchema.parse(process.env);
  }
  return config;
}
