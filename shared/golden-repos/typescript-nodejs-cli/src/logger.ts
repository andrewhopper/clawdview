/**
 * Logging configuration using Pino.
 */

import pino from 'pino';
import { getConfig } from './config.js';

const config = getConfig();

const baseLogger = pino({
  level: config.LOG_LEVEL,
  transport:
    config.NODE_ENV === 'development'
      ? {
          target: 'pino-pretty',
          options: {
            colorize: true,
            translateTime: 'SYS:standard',
            ignore: 'pid,hostname',
          },
        }
      : undefined,
});

export function getLogger(name: string): pino.Logger {
  return baseLogger.child({ name });
}
