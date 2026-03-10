/**
 * Error handling middleware.
 */

import { Request, Response, NextFunction } from 'express';
import { getLogger } from '../logger.js';

const log = getLogger('errorHandler');

export interface AppError extends Error {
  statusCode?: number;
  isOperational?: boolean;
}

export function errorHandler(
  err: AppError,
  req: Request,
  res: Response,
  _next: NextFunction
): void {
  const statusCode = err.statusCode || 500;
  const isOperational = err.isOperational ?? false;

  log.error(
    {
      err,
      requestId: req.requestId,
      path: req.path,
      method: req.method,
      statusCode,
      isOperational,
    },
    'Request error'
  );

  if (statusCode >= 500 && !isOperational) {
    res.status(500).json({ error: 'Internal server error' });
    return;
  }

  res.status(statusCode).json({
    error: err.message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
}
