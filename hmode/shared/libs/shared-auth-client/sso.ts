// File UUID: f1a2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c

/**
 * SSO (Single Sign-On) utilities for cross-subdomain authentication
 *
 * Launcher passes tokens via URL fragment: #auth_token=<jwt>
 * Target apps should call initSSO() on page load to receive tokens
 *
 * Install: copy this file into your project's lib/ directory
 * Usage:
 *   import { initSSO, redirectToLauncher } from '@/lib/sso';
 *   const tokenData = initSSO();
 *   if (!tokenData) redirectToLauncher(window.location.href);
 */

export interface SSOTokenData {
  idToken: string;
  accessToken?: string;
  refreshToken?: string;
  expiresAt: number;
  user: {
    email: string;
    sub: string;
    name?: string;
    picture?: string;
  };
}

/**
 * Decode JWT payload without verification (client-side)
 */
function decodeJwt(token: string): Record<string, unknown> | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const payload = atob(parts[1].replace(/-/g, '+').replace(/_/g, '/'));
    return JSON.parse(payload);
  } catch {
    return null;
  }
}

/**
 * Check if token is expired
 */
function isTokenExpired(token: string): boolean {
  const payload = decodeJwt(token);
  if (!payload || typeof payload.exp !== 'number') return true;
  return payload.exp * 1000 < Date.now();
}

/**
 * Extract auth token from URL fragment
 */
function getTokenFromFragment(): string | null {
  const hash = window.location.hash;
  if (!hash.includes('auth_token=')) return null;

  const params = new URLSearchParams(hash.slice(1));
  return params.get('auth_token');
}

/**
 * Remove auth token from URL fragment without page reload
 */
function clearTokenFromFragment(): void {
  const hash = window.location.hash;
  if (!hash.includes('auth_token=')) return;

  const params = new URLSearchParams(hash.slice(1));
  params.delete('auth_token');

  const newHash = params.toString();
  const newUrl = window.location.pathname + window.location.search + (newHash ? `#${newHash}` : '');
  window.history.replaceState(null, '', newUrl);
}

/**
 * Initialize SSO - call this on app startup
 *
 * @param storageKey - localStorage key to store auth data (default: 'app_auth')
 * @returns Token data if received from launcher, null otherwise
 */
export function initSSO(storageKey = 'app_auth'): SSOTokenData | null {
  // Check for token in URL fragment (from launcher)
  const idToken = getTokenFromFragment();

  if (idToken) {
    // Validate token is not expired
    if (isTokenExpired(idToken)) {
      console.warn('[SSO] Received expired token, ignoring');
      clearTokenFromFragment();
      return null;
    }

    // Decode token to get user info
    const payload = decodeJwt(idToken);
    if (!payload) {
      console.warn('[SSO] Failed to decode token');
      clearTokenFromFragment();
      return null;
    }

    // Build token data
    const tokenData: SSOTokenData = {
      idToken,
      expiresAt: (payload.exp as number) * 1000,
      user: {
        email: payload.email as string,
        sub: payload.sub as string,
        name: payload.name as string | undefined,
        picture: payload.picture as string | undefined,
      },
    };

    // Store in localStorage
    localStorage.setItem(storageKey, JSON.stringify(tokenData));
    console.log('[SSO] Token received and stored from launcher');

    // Clean up URL
    clearTokenFromFragment();

    return tokenData;
  }

  // Check for existing stored token
  try {
    const stored = localStorage.getItem(storageKey);
    if (stored) {
      const data = JSON.parse(stored) as SSOTokenData;
      if (data.expiresAt > Date.now()) {
        return data;
      }
      // Token expired, clean up
      localStorage.removeItem(storageKey);
    }
  } catch {
    localStorage.removeItem(storageKey);
  }

  return null;
}

/**
 * Get current SSO token data from storage
 */
export function getSSOToken(storageKey = 'app_auth'): SSOTokenData | null {
  try {
    const stored = localStorage.getItem(storageKey);
    if (stored) {
      const data = JSON.parse(stored) as SSOTokenData;
      if (data.expiresAt > Date.now()) {
        return data;
      }
    }
  } catch {
    // Ignore
  }
  return null;
}

/**
 * Clear SSO session
 */
export function clearSSO(storageKey = 'app_auth'): void {
  localStorage.removeItem(storageKey);
}

/**
 * Detect launcher URL from current hostname context
 */
function getLauncherUrl(): string {
  const hostname = window.location.hostname;
  if (hostname.includes('aws.demo1983.com')) {
    return 'https://launcher.b.aws.demo1983.com';
  }
  return 'https://launcher.b.lfg.new';
}

/**
 * Redirect to launcher for login
 */
export function redirectToLauncher(returnUrl?: string): void {
  const launcherUrl = getLauncherUrl();
  const url = returnUrl
    ? `${launcherUrl}?return=${encodeURIComponent(returnUrl)}`
    : launcherUrl;
  window.location.href = url;
}
