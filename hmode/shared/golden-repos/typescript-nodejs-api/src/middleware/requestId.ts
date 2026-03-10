/**
 * Request ID middleware - adds unique ID to each request.
 */

import { Request, Response, NextFunction } from 'express';
import { generateId } from '../utils.js';

declare global {
  namespace Express {
    interface Request {
      requestId: string;
    }
  }
}

export function requestIdMiddleware(req: Request, res: Response, next: NextFunction): void {
  const requestId = (req.headers['x-request-id'] as string) || generateId();
  req.requestId = requestId;
  res.setHeader('X-Request-ID', requestId);
  next();
}
