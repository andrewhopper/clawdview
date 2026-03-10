/**
 * Configuration schema with Zod validation.
 * Supports multi-context (work, personal, etc.) and flexible stage names.
 */

import { z } from 'zod';

/**
 * Deployment contexts - organizational boundaries.
 * Examples: work, personal, client-name, project-team
 */
export type Context = string;

/**
 * Deployment stages - any naming pattern you want.
 * Examples:
 * - Traditional: dev, stage, prod
 * - Blue/Green: blue, green
 * - Greek letters: alpha, beta, gamma
 * - Semantic: development, staging, production
 */
export type Stage = string;

/**
 * Domain configuration schema.
 */
const domainConfigSchema = z.object({
  /** Root domain (e.g., example.com) */
  rootDomain: z.string(),
  /** Subdomain prefix (e.g., api, app) */
  subdomain: z.string().optional(),
  /** Route53 hosted zone ID */
  hostedZoneId: z.string().optional(),
  /** ACM certificate ARN */
  certificateArn: z.string().optional(),
});

/**
 * Email/notification configuration schema.
 */
const notificationConfigSchema = z.object({
  /** Admin email for alerts */
  adminEmail: z.string().email(),
  /** Support email */
  supportEmail: z.string().email().optional(),
  /** SNS topic ARN for alerts (optional, created if not provided) */
  alertTopicArn: z.string().optional(),
  /** SES verified domain */
  sesDomain: z.string().optional(),
});

/**
 * Database configuration schema.
 */
const databaseConfigSchema = z.object({
  /** Instance class (e.g., t3.micro, r5.large) */
  instanceClass: z.string().default('t3.micro'),
  /** Allocated storage in GB */
  allocatedStorage: z.number().default(20),
  /** Enable multi-AZ deployment */
  multiAz: z.boolean().default(false),
  /** Enable deletion protection */
  deletionProtection: z.boolean().default(false),
  /** Backup retention days */
  backupRetentionDays: z.number().default(7),
});

/**
 * Compute configuration schema.
 */
const computeConfigSchema = z.object({
  /** Lambda memory size in MB */
  lambdaMemory: z.number().default(256),
  /** Lambda timeout in seconds */
  lambdaTimeout: z.number().default(30),
  /** ECS task CPU units */
  taskCpu: z.number().default(256),
  /** ECS task memory in MB */
  taskMemory: z.number().default(512),
  /** Desired task count */
  desiredCount: z.number().default(1),
  /** Min task count for autoscaling */
  minCount: z.number().default(1),
  /** Max task count for autoscaling */
  maxCount: z.number().default(4),
});

/**
 * Monitoring configuration schema.
 */
const monitoringConfigSchema = z.object({
  /** Enable CloudWatch dashboards */
  enableDashboards: z.boolean().default(false),
  /** Enable X-Ray tracing */
  enableTracing: z.boolean().default(false),
  /** Log retention in days */
  logRetentionDays: z.number().default(14),
  /** Alarm evaluation periods */
  alarmEvaluationPeriods: z.number().default(3),
});

/**
 * Complete environment configuration schema.
 */
export const envConfigSchema = z.object({
  /** Deployment context (e.g., work, personal) */
  context: z.string(),
  /** Deployment stage (e.g., dev, prod, blue, alpha) */
  stage: z.string(),
  /** AWS account ID */
  account: z.string(),
  /** AWS region */
  region: z.string().default('us-east-1'),
  /** Project/application name */
  projectName: z.string(),
  /** Stack name prefix */
  stackPrefix: z.string().optional(),

  /** Domain configuration */
  domain: domainConfigSchema.optional(),
  /** Notification configuration */
  notifications: notificationConfigSchema,
  /** Database configuration */
  database: databaseConfigSchema.optional(),
  /** Compute configuration */
  compute: computeConfigSchema.default({}),
  /** Monitoring configuration */
  monitoring: monitoringConfigSchema.default({}),

  /** Resource tags */
  tags: z.record(z.string()).default({}),
});

export type EnvConfig = z.infer<typeof envConfigSchema>;
export type DomainConfig = z.infer<typeof domainConfigSchema>;
export type NotificationConfig = z.infer<typeof notificationConfigSchema>;
export type DatabaseConfig = z.infer<typeof databaseConfigSchema>;
export type ComputeConfig = z.infer<typeof computeConfigSchema>;
export type MonitoringConfig = z.infer<typeof monitoringConfigSchema>;
