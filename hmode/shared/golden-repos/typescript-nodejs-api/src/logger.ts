/**
 * Structured logging with Pino.
 */

import pino from 'pino';
import { getConfig, isProduction } from './config.js';

export type Logger = pino.Logger;

let loggerInstance: Logger | null = null;

/**
 * Get configured logger instance.
 */
export function getLogger(name?: string): Logger {
  if (!loggerInstance) {
    const config = getConfig();

    const transport = isProduction()
      ? undefined
      : {
          target: 'pino-pretty',
          options: {
            colorize: true,
            translateTime: 'SYS:standard',
            ignore: 'pid,hostname',
          },
        };

    loggerInstance = pino({
      name: config.APP_NAME,
      level: config.LOG_LEVEL,
      transport,
    });
  }

  return name ? loggerInstance.child({ module: name }) : loggerInstance;
}

/**
 * Create a child logger with additional context.
 */
export function createChildLogger(
  bindings: Record<string, unknown>
): Logger {
  return getLogger().child(bindings);
}
