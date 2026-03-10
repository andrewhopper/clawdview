export const STORAGE_KEYS = {
  USER_PREFERENCES: '@app/user_preferences',
  AUTH_TOKEN: '@app/auth_token',
  ONBOARDING_COMPLETE: '@app/onboarding_complete',
} as const;

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
  },
  USER: {
    PROFILE: '/user/profile',
    SETTINGS: '/user/settings',
  },
} as const;

export const ANIMATION_DURATION = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500,
} as const;
