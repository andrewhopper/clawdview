/**
 * Next.js middleware for request processing.
 */

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Middleware runs before every request.
 * Use for: auth checks, redirects, headers, logging.
 */
export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // Add request ID header
  const requestId = crypto.randomUUID().slice(0, 8);
  response.headers.set('x-request-id', requestId);

  // Add security headers
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Example: Protect /dashboard routes (uncomment to enable)
  // if (request.nextUrl.pathname.startsWith('/dashboard')) {
  //   const token = request.cookies.get('auth-token');
  //   if (!token) {
  //     return NextResponse.redirect(new URL('/login', request.url));
  //   }
  // }

  // Example: Rate limiting headers
  // response.headers.set('X-RateLimit-Limit', '100');
  // response.headers.set('X-RateLimit-Remaining', '99');

  return response;
}

/**
 * Configure which paths the middleware runs on.
 */
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|public/).*)',
  ],
};
