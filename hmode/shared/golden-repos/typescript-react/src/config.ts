/**
 * Configuration for React component library.
 */

export const environments = ['local', 'dev', 'integration', 'stage', 'prod'] as const;
export type Environment = (typeof environments)[number];

export interface LibraryConfig {
  /** Current environment */
  env: Environment;
  /** Enable debug logging */
  debug: boolean;
  /** Enable analytics/metrics */
  enableMetrics: boolean;
}

const defaultConfig: LibraryConfig = {
  env: 'local',
  debug: false,
  enableMetrics: false,
};

let currentConfig: LibraryConfig = { ...defaultConfig };

/**
 * Configure the library.
 */
export function configure(config: Partial<LibraryConfig>): void {
  currentConfig = { ...currentConfig, ...config };

  // Auto-enable debug in local/dev
  if (config.env && !('debug' in config)) {
    currentConfig.debug = config.env === 'local' || config.env === 'dev';
  }
}

/**
 * Get current configuration.
 */
export function getConfig(): LibraryConfig {
  return { ...currentConfig };
}

/**
 * Check if in production.
 */
export function isProduction(): boolean {
  return currentConfig.env === 'prod';
}

/**
 * Check if in local environment.
 */
export function isLocal(): boolean {
  return currentConfig.env === 'local';
}
