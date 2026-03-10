// File UUID: 9f3e8b2c-4d1a-4e8f-9c3b-7e6d5f4a3b2c

/**
 * SSM Parameter Store Hierarchical Resolver
 *
 * Provides automatic fallback chain for SSM parameters:
 * 1. Project-specific: /{account}/{env}/{project}/{category}/{key}
 * 2. Environment-shared: /{account}/{env}/{category}/{key}
 * 3. Account-shared: /{account}/{category}/{key}
 * 4. Global-shared: /shared/{category}/{key}
 *
 * Benefits:
 * - No duplicate values (DRY)
 * - Projects inherit from environment defaults
 * - Easy multi-environment deployments
 * - Clear ownership/scope from path structure
 */

import * as ssm from 'aws-cdk-lib/aws-ssm';
import { Construct } from 'constructs';

export type AccountType = 'work' | 'personal' | 'shared';
export type Environment = 'dev' | 'prod' | 'beta' | 'staging';
export type ParameterScope = 'project' | 'environment' | 'account' | 'shared';

export interface SSMResolverConfig {
  /** Account type: work | personal | shared */
  accountType: AccountType;
  /** Deployment environment: dev | prod | beta | staging */
  environment: Environment;
  /** Project identifier (e.g., gocoder, ppm, story-wizard) */
  project: string;
}

export interface ResolveOptions {
  /** Use SecureString type (for secrets) */
  secure?: boolean;
  /** Throw error if parameter not found in any fallback path */
  required?: boolean;
  /** Enable debug logging to console */
  debug?: boolean;
}

export interface WriteOptions {
  /** Parameter scope (where to write) */
  scope?: ParameterScope;
  /** Use SecureString type */
  secure?: boolean;
  /** Custom description */
  description?: string;
}

/**
 * SSM Parameter Resolver with Hierarchical Fallback
 *
 * Usage:
 * ```typescript
 * const ssm = new SSMResolver(this, {
 *   accountType: 'work',
 *   environment: 'dev',
 *   project: 'gocoder',
 * });
 *
 * // Resolves with fallback chain
 * const clientId = ssm.resolve('auth', 'google-client-id');
 *
 * // Write project-specific value
 * ssm.write('auth', 'cognito-client-id', appClient.userPoolClientId);
 * ```
 */
export class SSMResolver {
  private readonly scope: Construct;
  private readonly config: SSMResolverConfig;

  constructor(scope: Construct, config: SSMResolverConfig) {
    this.scope = scope;
    this.config = config;
  }

  /**
   * Resolve parameter with automatic fallback chain
   *
   * Tries paths in order (most specific to most general):
   * 1. /{account}/{env}/{project}/{category}/{key}
   * 2. /{account}/{env}/{category}/{key}
   * 3. /{account}/{category}/{key}
   * 4. /shared/{category}/{key}
   *
   * @param category - Category path (e.g., 'auth', 'auth/cognito', 'iot')
   * @param key - Parameter key (e.g., 'client-id', 'user-pool-id')
   * @param options - Resolution options
   * @returns Parameter value or empty string if not found
   * @throws Error if required=true and parameter not found
   */
  resolve(category: string, key: string, options: ResolveOptions = {}): string {
    const paths = this.buildFallbackChain(category, key);

    if (options.debug) {
      console.log(`[SSMResolver] Resolving ${category}/${key}`);
      console.log(`[SSMResolver] Fallback chain:`, paths);
    }

    // Try each path in fallback order
    for (const path of paths) {
      try {
        const value = ssm.StringParameter.valueFromLookup(this.scope, path);

        // CDK returns dummy value when parameter doesn't exist during synth
        if (value && value !== 'dummy-value-for-missing-parameter') {
          if (options.debug) {
            console.log(`[SSMResolver] Found at: ${path}`);
          }
          return value;
        }
      } catch (error) {
        if (options.debug) {
          console.log(`[SSMResolver] Not found at: ${path}`);
        }
        continue;
      }
    }

    if (options.required) {
      throw new Error(
        `Required SSM parameter not found: ${category}/${key}\n` +
        `Tried paths:\n${paths.map(p => `  - ${p}`).join('\n')}`
      );
    }

    if (options.debug) {
      console.log(`[SSMResolver] Not found in any fallback path (returning empty string)`);
    }

    return '';
  }

  /**
   * Get IStringParameter for runtime access (Lambda environment variables)
   *
   * Use this when you need to pass parameter to Lambda or grant read access.
   * Does NOT use fallback chain - you must specify exact path scope.
   *
   * @param category - Category path
   * @param key - Parameter key
   * @param scope - Exact scope to read from (default: 'project')
   * @returns IStringParameter for grants and references
   */
  fromName(
    category: string,
    key: string,
    scope: ParameterScope = 'project'
  ): ssm.IStringParameter {
    const path = this.path(category, key, scope);
    return ssm.StringParameter.fromStringParameterName(
      this.scope,
      `Param-${this.sanitizeId(category)}-${this.sanitizeId(key)}`,
      path
    );
  }

  /**
   * Get IStringParameter for secure parameter (SecureString)
   */
  fromSecureName(
    category: string,
    key: string,
    scope: ParameterScope = 'project'
  ): ssm.IStringParameter {
    const path = this.path(category, key, scope);
    return ssm.StringParameter.fromSecureStringParameterAttributes(
      this.scope,
      `SecureParam-${this.sanitizeId(category)}-${this.sanitizeId(key)}`,
      { parameterName: path }
    );
  }

  /**
   * Write parameter to SSM
   *
   * @param category - Category path
   * @param key - Parameter key
   * @param value - Parameter value
   * @param options - Write options
   * @returns StringParameter construct
   */
  write(
    category: string,
    key: string,
    value: string,
    options: WriteOptions = {}
  ): ssm.StringParameter {
    const scope = options.scope || 'project';
    const paramPath = this.path(category, key, scope);

    return new ssm.StringParameter(
      this.scope,
      `SSM-${this.sanitizeId(category)}-${this.sanitizeId(key)}`,
      {
        parameterName: paramPath,
        stringValue: value,
        type: options.secure
          ? ssm.ParameterType.SECURE_STRING
          : ssm.ParameterType.STRING,
        description: options.description || this.generateDescription(category, key, scope),
      }
    );
  }

  /**
   * Generate SSM parameter path for given scope
   *
   * @param category - Category path (e.g., 'auth', 'auth/cognito')
   * @param key - Parameter key
   * @param scope - Parameter scope
   * @returns Full SSM parameter path
   */
  path(category: string, key: string, scope: ParameterScope = 'project'): string {
    const { accountType, environment, project } = this.config;
    const fullKey = `${category}/${key}`;

    switch (scope) {
      case 'project':
        return `/${accountType}/${environment}/${project}/${fullKey}`;
      case 'environment':
        return `/${accountType}/${environment}/${fullKey}`;
      case 'account':
        return `/${accountType}/${fullKey}`;
      case 'shared':
        return `/shared/${fullKey}`;
    }
  }

  /**
   * Build fallback chain (most specific to most general)
   */
  private buildFallbackChain(category: string, key: string): string[] {
    return [
      this.path(category, key, 'project'),
      this.path(category, key, 'environment'),
      this.path(category, key, 'account'),
      this.path(category, key, 'shared'),
    ];
  }

  /**
   * Generate description for parameter
   */
  private generateDescription(category: string, key: string, scope: ParameterScope): string {
    const { accountType, environment, project } = this.config;
    return `[${accountType}/${environment}/${project}] ${category}/${key} (${scope})`;
  }

  /**
   * Sanitize category/key for CDK construct ID
   */
  private sanitizeId(input: string): string {
    return input.replace(/[^a-zA-Z0-9]/g, '-');
  }

  /**
   * Grant read access to parameter
   *
   * @param grantee - IAM principal (role, function, etc.)
   * @param category - Category path
   * @param key - Parameter key
   * @param scope - Parameter scope (default: 'project')
   */
  grantRead(
    grantee: any,
    category: string,
    key: string,
    scope: ParameterScope = 'project'
  ): void {
    const param = this.fromName(category, key, scope);
    param.grantRead(grantee);
  }

  /**
   * Get configuration for debugging
   */
  getConfig(): SSMResolverConfig {
    return { ...this.config };
  }
}

/**
 * Convenience function to create resolver
 */
export function createResolver(scope: Construct, config: SSMResolverConfig): SSMResolver {
  return new SSMResolver(scope, config);
}
