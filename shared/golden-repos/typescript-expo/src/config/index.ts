import { z } from 'zod';
import Constants from 'expo-constants';

const configSchema = z.object({
  apiUrl: z.string().url(),
  environment: z.enum(['development', 'staging', 'production']),
  appVersion: z.string(),
  buildNumber: z.string().optional(),
});

export type Config = z.infer<typeof configSchema>;

function getEnvironment(): Config['environment'] {
  const env = Constants.expoConfig?.extra?.environment;
  if (env === 'production' || env === 'staging' || env === 'development') {
    return env;
  }
  return __DEV__ ? 'development' : 'production';
}

function getApiUrl(): string {
  const environment = getEnvironment();

  switch (environment) {
    case 'production':
      return Constants.expoConfig?.extra?.apiUrl ?? 'https://api.example.com';
    case 'staging':
      return Constants.expoConfig?.extra?.apiUrl ?? 'https://api-staging.example.com';
    case 'development':
    default:
      return Constants.expoConfig?.extra?.apiUrl ?? 'http://localhost:3000';
  }
}

export function getConfig(): Config {
  const rawConfig = {
    apiUrl: getApiUrl(),
    environment: getEnvironment(),
    appVersion: Constants.expoConfig?.version ?? '1.0.0',
    buildNumber: Constants.expoConfig?.ios?.buildNumber ?? Constants.expoConfig?.android?.versionCode?.toString(),
  };

  return configSchema.parse(rawConfig);
}

let cachedConfig: Config | null = null;

export function config(): Config {
  if (!cachedConfig) {
    cachedConfig = getConfig();
  }
  return cachedConfig;
}
