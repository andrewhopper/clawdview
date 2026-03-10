/**
 * Configuration loader with context/stage-specific YAML files.
 * Supports structure: config/{context}/{stage}.yml
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'yaml';
import { envConfigSchema, EnvConfig, Context, Stage } from './schema';

/**
 * Load and validate configuration for a context and stage.
 * @param context - Deployment context (e.g., 'work', 'personal')
 * @param stage - Deployment stage (e.g., 'dev', 'prod', 'blue')
 */
export function loadConfig(context?: Context, stage?: Stage): EnvConfig {
  const ctx = context ?? getContext();
  const stg = stage ?? getStage();
  const configPath = path.join(__dirname, ctx, `${stg}.yml`);

  if (!fs.existsSync(configPath)) {
    const availableConfigs = listAvailableConfigs();
    throw new Error(
      `Configuration file not found: ${configPath}\n` +
      `Available configs:\n${availableConfigs}`
    );
  }

  const fileContents = fs.readFileSync(configPath, 'utf8');
  const rawConfig = yaml.parse(fileContents);

  // Merge with context and stage
  const configWithMeta = { ...rawConfig, context: ctx, stage: stg };

  // Validate and return
  const result = envConfigSchema.safeParse(configWithMeta);

  if (!result.success) {
    console.error(`Configuration validation failed for ${ctx}/${stg}:`);
    console.error(result.error.format());
    throw new Error(`Invalid configuration for ${ctx}/${stg}`);
  }

  return result.data;
}

/**
 * Get current context from CONTEXT environment variable.
 */
export function getContext(): Context {
  const context = process.env.CONTEXT ?? process.env.CDK_CONTEXT ?? 'work';
  return context;
}

/**
 * Get current stage from STAGE environment variable.
 */
export function getStage(): Stage {
  const stage = process.env.STAGE ?? process.env.CDK_STAGE ?? 'dev';
  return stage;
}

/**
 * List all available config files.
 */
export function listAvailableConfigs(): string {
  const configDir = __dirname;
  const contexts: string[] = [];

  try {
    const entries = fs.readdirSync(configDir, { withFileTypes: true });

    for (const entry of entries) {
      if (entry.isDirectory()) {
        const contextPath = path.join(configDir, entry.name);
        const stages = fs.readdirSync(contextPath)
          .filter(f => f.endsWith('.yml'))
          .map(f => f.replace('.yml', ''));

        if (stages.length > 0) {
          contexts.push(`  ${entry.name}: ${stages.join(', ')}`);
        }
      }
    }
  } catch (err) {
    return '  No configs found';
  }

  return contexts.length > 0 ? contexts.join('\n') : '  No configs found';
}

/**
 * Get stack name with context and stage prefix.
 */
export function getStackName(config: EnvConfig, stackName: string): string {
  const prefix = config.stackPrefix ?? config.projectName;
  return `${prefix}-${config.context}-${config.stage}-${stackName}`;
}

/**
 * Get deployment identifier (context-stage).
 */
export function getDeploymentId(config: EnvConfig): string {
  return `${config.context}-${config.stage}`;
}

/**
 * Get full domain name.
 */
export function getFullDomain(config: EnvConfig): string | undefined {
  if (!config.domain) return undefined;

  const { rootDomain, subdomain } = config.domain;
  if (subdomain) {
    return `${subdomain}.${rootDomain}`;
  }
  return rootDomain;
}

/**
 * Check if stage is production-like.
 * Matches: prod, production, green, gamma
 */
export function isProduction(config: EnvConfig): boolean {
  const prodPatterns = ['prod', 'production', 'green', 'gamma'];
  return prodPatterns.includes(config.stage.toLowerCase());
}

/**
 * Get default tags for all resources.
 */
export function getDefaultTags(config: EnvConfig): Record<string, string> {
  return {
    Project: config.projectName,
    Context: config.context,
    Stage: config.stage,
    ManagedBy: 'CDK',
    ...config.tags,
  };
}
