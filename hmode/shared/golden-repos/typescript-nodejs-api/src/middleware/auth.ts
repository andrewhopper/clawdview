/**
 * Authentication middleware and utilities.
 */

import { Request, Response, NextFunction } from 'express';
import { getLogger } from '../logger.js';

const log = getLogger('auth');

// Token payload interface
export interface TokenPayload {
  sub: string; // Subject (user ID)
  exp: number; // Expiration timestamp
  iat: number; // Issued at timestamp
}

// Authenticated user interface
export interface AuthUser {
  id: string;
  email: string;
  roles: string[];
}

// Extend Express Request type
declare global {
  namespace Express {
    interface Request {
      user?: AuthUser;
    }
  }
}

/**
 * Create a JWT token.
 *
 * NOTE: This is a placeholder. In production, use a proper JWT library:
 * - jsonwebtoken
 * - jose
 *
 * Example with jsonwebtoken:
 *   import jwt from 'jsonwebtoken';
 *   return jwt.sign({ sub: userId }, process.env.JWT_SECRET, { expiresIn: '24h' });
 */
export function createToken(userId: string, expiresInHours = 24): string {
  const exp = Math.floor(Date.now() / 1000) + expiresInHours * 3600;
  return `placeholder-token-${userId}-${exp}`;
}

/**
 * Decode and validate a JWT token.
 *
 * NOTE: This is a placeholder. In production, use a proper JWT library.
 */
export function decodeToken(token: string): TokenPayload | null {
  if (token.startsWith('placeholder-token-')) {
    const parts = token.split('-');
    if (parts.length >= 4) {
      return {
        sub: parts[2],
        exp: parseInt(parts[3], 10),
        iat: Math.floor(Date.now() / 1000),
      };
    }
  }
  return null;
}

/**
 * Extract bearer token from Authorization header.
 */
function extractBearerToken(authHeader: string | undefined): string | null {
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return null;
  }
  return authHeader.slice(7);
}

/**
 * Authentication middleware - requires valid token.
 */
export function requireAuth(req: Request, res: Response, next: NextFunction): void {
  const token = extractBearerToken(req.headers.authorization);

  if (!token) {
    res.status(401).json({ error: 'Authentication required' });
    return;
  }

  const payload = decodeToken(token);
  if (!payload) {
    res.status(401).json({ error: 'Invalid or expired token' });
    return;
  }

  // Check expiration
  if (payload.exp < Math.floor(Date.now() / 1000)) {
    res.status(401).json({ error: 'Token expired' });
    return;
  }

  // In production, fetch user from database
  req.user = {
    id: payload.sub,
    email: `${payload.sub}@example.com`,
    roles: ['user'],
  };

  log.debug({ userId: req.user.id }, 'User authenticated');
  next();
}

/**
 * Optional authentication middleware - attaches user if token present.
 */
export function optionalAuth(req: Request, res: Response, next: NextFunction): void {
  const token = extractBearerToken(req.headers.authorization);

  if (token) {
    const payload = decodeToken(token);
    if (payload && payload.exp >= Math.floor(Date.now() / 1000)) {
      req.user = {
        id: payload.sub,
        email: `${payload.sub}@example.com`,
        roles: ['user'],
      };
    }
  }

  next();
}

/**
 * Role-based authorization middleware factory.
 *
 * Usage:
 *   router.get('/admin', requireAuth, requireRoles('admin'), handler);
 */
export function requireRoles(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.user) {
      res.status(401).json({ error: 'Authentication required' });
      return;
    }

    const hasRole = roles.some((role) => req.user!.roles.includes(role));
    if (!hasRole) {
      res.status(403).json({ error: 'Insufficient permissions' });
      return;
    }

    next();
  };
}
