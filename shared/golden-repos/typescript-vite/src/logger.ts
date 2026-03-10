/**
 * Simple structured logging for browser and Node.js.
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  [key: string]: unknown;
}

const LOG_LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

class Logger {
  private minLevel: LogLevel;
  private context: Record<string, unknown>;

  constructor(level: LogLevel = 'info', context: Record<string, unknown> = {}) {
    this.minLevel = level;
    this.context = context;
  }

  private shouldLog(level: LogLevel): boolean {
    return LOG_LEVELS[level] >= LOG_LEVELS[this.minLevel];
  }

  private log(level: LogLevel, message: string, data?: Record<string, unknown>): void {
    if (!this.shouldLog(level)) return;

    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...this.context,
      ...data,
    };

    const method = level === 'error' ? 'error' : level === 'warn' ? 'warn' : 'log';
    console[method](JSON.stringify(entry));
  }

  debug(message: string, data?: Record<string, unknown>): void {
    this.log('debug', message, data);
  }

  info(message: string, data?: Record<string, unknown>): void {
    this.log('info', message, data);
  }

  warn(message: string, data?: Record<string, unknown>): void {
    this.log('warn', message, data);
  }

  error(message: string, data?: Record<string, unknown>): void {
    this.log('error', message, data);
  }

  child(context: Record<string, unknown>): Logger {
    return new Logger(this.minLevel, { ...this.context, ...context });
  }
}

export const logger = new Logger('info');
export const createLogger = (level: LogLevel, context?: Record<string, unknown>) =>
  new Logger(level, context);
