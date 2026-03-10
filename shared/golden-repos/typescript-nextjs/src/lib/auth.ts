/**
 * Authentication utilities for Next.js.
 */

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

// Token payload interface
export interface TokenPayload {
  sub: string;
  exp: number;
  iat: number;
}

// User interface
export interface User {
  id: string;
  email: string;
  roles: string[];
}

const AUTH_COOKIE = 'auth-token';

/**
 * Create a JWT token.
 *
 * NOTE: Placeholder implementation. Use jose or jsonwebtoken in production.
 */
export function createToken(userId: string, expiresInHours = 24): string {
  const exp = Math.floor(Date.now() / 1000) + expiresInHours * 3600;
  return `placeholder-token-${userId}-${exp}`;
}

/**
 * Decode a JWT token.
 *
 * NOTE: Placeholder implementation.
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
 * Get current user from cookies (Server Component).
 */
export async function getCurrentUser(): Promise<User | null> {
  const cookieStore = await cookies();
  const token = cookieStore.get(AUTH_COOKIE)?.value;

  if (!token) {
    return null;
  }

  const payload = decodeToken(token);
  if (!payload || payload.exp < Math.floor(Date.now() / 1000)) {
    return null;
  }

  // In production, fetch from database
  return {
    id: payload.sub,
    email: `${payload.sub}@example.com`,
    roles: ['user'],
  };
}

/**
 * Require authentication - redirects to login if not authenticated.
 * Use in Server Components or Server Actions.
 */
export async function requireAuth(): Promise<User> {
  const user = await getCurrentUser();
  if (!user) {
    redirect('/login');
  }
  return user;
}

/**
 * Set auth cookie after login.
 */
export async function setAuthCookie(token: string): Promise<void> {
  const cookieStore = await cookies();
  cookieStore.set(AUTH_COOKIE, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24, // 24 hours
    path: '/',
  });
}

/**
 * Clear auth cookie on logout.
 */
export async function clearAuthCookie(): Promise<void> {
  const cookieStore = await cookies();
  cookieStore.delete(AUTH_COOKIE);
}
