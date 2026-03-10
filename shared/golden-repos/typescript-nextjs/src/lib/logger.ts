/**
 * Simple structured logging for Next.js.
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogContext {
  [key: string]: unknown;
}

function formatLog(
  level: LogLevel,
  message: string,
  context?: LogContext
): string {
  const timestamp = new Date().toISOString();
  const entry = {
    timestamp,
    level,
    message,
    ...context,
  };
  return JSON.stringify(entry);
}

function createLogger(module?: string) {
  const baseContext = module ? { module } : {};

  return {
    debug(message: string, context?: LogContext): void {
      if (process.env.NODE_ENV === 'development') {
        console.debug(formatLog('debug', message, { ...baseContext, ...context }));
      }
    },
    info(message: string, context?: LogContext): void {
      console.info(formatLog('info', message, { ...baseContext, ...context }));
    },
    warn(message: string, context?: LogContext): void {
      console.warn(formatLog('warn', message, { ...baseContext, ...context }));
    },
    error(message: string, context?: LogContext): void {
      console.error(formatLog('error', message, { ...baseContext, ...context }));
    },
  };
}

export const logger = createLogger();
export const getLogger = (module: string) => createLogger(module);
