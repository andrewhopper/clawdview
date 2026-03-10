// File UUID: 3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f
/**
 * Type-safe AWS Configuration Schemas
 *
 * Use these Zod schemas to validate configuration at runtime
 * and get TypeScript type inference.
 *
 * @example
 * import { deploymentConfigSchema, type DeploymentConfig } from '@shared/standards/config/aws-config-schemas';
 *
 * const config = deploymentConfigSchema.parse(rawConfig);
 * // config is now typed as DeploymentConfig
 */

import { z } from 'zod';

// ============================================
// AWS Resource ID Patterns
// ============================================

/**
 * AWS Account ID - exactly 12 digits
 * @example "507745175693"
 */
export const awsAccountIdSchema = z
  .string()
  .regex(/^\d{12}$/, 'AWS Account ID must be exactly 12 digits')
  .refine(
    (val) => !['000000000000', '111111111111', '123456789012'].includes(val),
    'Placeholder AWS account ID detected'
  );

/**
 * AWS Region
 * @example "us-east-1", "eu-west-2"
 */
export const awsRegionSchema = z
  .string()
  .regex(/^[a-z]{2}-[a-z]+-\d$/, 'Invalid AWS region format')
  .refine(
    (val) =>
      [
        'us-east-1',
        'us-east-2',
        'us-west-1',
        'us-west-2',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'eu-central-1',
        'eu-north-1',
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-southeast-1',
        'ap-southeast-2',
        'ap-south-1',
        'sa-east-1',
        'ca-central-1',
      ].includes(val),
    'Unknown AWS region'
  );

/**
 * AWS ARN - Amazon Resource Name
 * @example "arn:aws:s3:::my-bucket"
 */
export const awsArnSchema = z
  .string()
  .regex(
    /^arn:aws:[a-z0-9-]+:[a-z0-9-]*:\d{12}:[a-zA-Z0-9:/_-]+$/,
    'Invalid ARN format'
  )
  .refine(
    (val) => !val.includes('000000000000') && !val.includes('123456789012'),
    'Placeholder ARN detected'
  );

// ============================================
// Cognito Schemas
// ============================================

/**
 * Cognito User Pool ID
 * @example "us-east-1_AbcDefGhi"
 */
export const cognitoUserPoolIdSchema = z
  .string()
  .regex(
    /^[a-z]{2}-[a-z]+-\d_[A-Za-z0-9]{9}$/,
    'Invalid Cognito User Pool ID format (expected: us-east-1_AbcDefGhi)'
  )
  .refine(
    (val) => !val.includes('XXXXXXXXX') && !val.toLowerCase().includes('example'),
    'Placeholder Cognito User Pool ID detected'
  );

/**
 * Cognito App Client ID
 * @example "1234567890abcdefghijklmnop"
 */
export const cognitoClientIdSchema = z
  .string()
  .regex(
    /^[a-z0-9]{26}$/,
    'Invalid Cognito App Client ID format (expected: 26 lowercase alphanumeric characters)'
  );

/**
 * Full Cognito configuration
 */
export const cognitoConfigSchema = z.object({
  userPoolId: cognitoUserPoolIdSchema,
  clientId: cognitoClientIdSchema,
  region: awsRegionSchema.optional().default('us-east-1'),
  domain: z.string().optional(),
  identityPoolId: z.string().optional(),
});

// ============================================
// S3 Schemas
// ============================================

/**
 * S3 Bucket Name
 * @example "my-app-bucket-dev"
 */
export const s3BucketNameSchema = z
  .string()
  .min(3, 'S3 bucket name must be at least 3 characters')
  .max(63, 'S3 bucket name must be at most 63 characters')
  .regex(
    /^[a-z0-9][a-z0-9.-]*[a-z0-9]$/,
    'S3 bucket name must start and end with lowercase letter or number'
  )
  .refine(
    (val) =>
      !val.includes('example') &&
      !val.includes('placeholder') &&
      !val.includes('your-'),
    'Placeholder S3 bucket name detected'
  );

/**
 * S3 configuration
 */
export const s3ConfigSchema = z.object({
  bucketName: s3BucketNameSchema,
  region: awsRegionSchema.optional().default('us-east-1'),
  prefix: z.string().optional(),
});

// ============================================
// DynamoDB Schemas
// ============================================

/**
 * DynamoDB Table Name
 * @example "my-app-users-dev"
 */
export const dynamoDbTableNameSchema = z
  .string()
  .min(3, 'DynamoDB table name must be at least 3 characters')
  .max(255, 'DynamoDB table name must be at most 255 characters')
  .regex(
    /^[a-zA-Z0-9._-]+$/,
    'DynamoDB table name can only contain letters, numbers, dots, hyphens, and underscores'
  );

/**
 * DynamoDB Table ARN
 */
export const dynamoDbTableArnSchema = z
  .string()
  .regex(
    /^arn:aws:dynamodb:[a-z0-9-]+:\d{12}:table\/[a-zA-Z0-9._-]+$/,
    'Invalid DynamoDB table ARN format'
  );

/**
 * DynamoDB configuration
 */
export const dynamoDbConfigSchema = z.object({
  tableName: dynamoDbTableNameSchema,
  tableArn: dynamoDbTableArnSchema.optional(),
  region: awsRegionSchema.optional().default('us-east-1'),
});

// ============================================
// Lambda Schemas
// ============================================

/**
 * Lambda Function Name
 * @example "my-app-api-handler"
 */
export const lambdaFunctionNameSchema = z
  .string()
  .min(1, 'Lambda function name must be at least 1 character')
  .max(64, 'Lambda function name must be at most 64 characters')
  .regex(
    /^[a-zA-Z0-9-_]+$/,
    'Lambda function name can only contain letters, numbers, hyphens, and underscores'
  );

// ============================================
// API Gateway Schemas
// ============================================

/**
 * API Gateway REST API ID
 * @example "abcd123456"
 */
export const apiGatewayIdSchema = z
  .string()
  .regex(/^[a-z0-9]{10}$/, 'Invalid API Gateway ID format (expected: 10 lowercase alphanumeric)');

// ============================================
// CloudFront Schemas
// ============================================

/**
 * CloudFront Distribution ID
 * @example "E1234567890ABC"
 */
export const cloudFrontDistributionIdSchema = z
  .string()
  .regex(
    /^[A-Z0-9]{13,14}$/,
    'Invalid CloudFront Distribution ID format (expected: 13-14 uppercase alphanumeric)'
  );

// ============================================
// Placeholder Detection
// ============================================

/**
 * String that is not a placeholder
 * Rejects common placeholder patterns
 */
export const nonPlaceholderStringSchema = z
  .string()
  .refine(
    (val) => {
      const placeholderPatterns = [
        /^YOUR_/i,
        /^REPLACE_/i,
        /^CHANGEME/i,
        /^TODO/i,
        /^FIXME/i,
        /^XXX/i,
        /^placeholder/i,
        /^example/i,
        /^<.*>$/,
        /^\[.*\]$/,
        /^\{.*\}$/,
        /^___+$/,
        /^\.\.\.$/,
        /^null$/i,
        /^undefined$/i,
        /^N\/A$/i,
        /^TBD$/i,
      ];
      return !placeholderPatterns.some((pattern) => pattern.test(val));
    },
    'Placeholder value detected - replace with actual value'
  );

// ============================================
// Environment Configuration
// ============================================

export const environmentSchema = z.enum(['dev', 'staging', 'prod', 'test', 'local']);
export type Environment = z.infer<typeof environmentSchema>;

// ============================================
// Complete Deployment Configuration
// ============================================

/**
 * Full deployment configuration schema
 * Use this for complete infrastructure configs
 */
export const deploymentConfigSchema = z.object({
  // Basic info
  projectName: nonPlaceholderStringSchema,
  environment: environmentSchema,
  region: awsRegionSchema,
  accountId: awsAccountIdSchema,

  // Optional service configs
  cognito: cognitoConfigSchema.optional(),
  s3: z.array(s3ConfigSchema).optional(),
  dynamodb: z.array(dynamoDbConfigSchema).optional(),

  // URLs
  appUrl: z.string().url().optional(),
  apiUrl: z.string().url().optional(),

  // Tags
  tags: z.record(z.string()).optional(),
});

export type DeploymentConfig = z.infer<typeof deploymentConfigSchema>;

// ============================================
// Amplify Configuration
// ============================================

export const amplifyConfigSchema = z.object({
  appId: z.string().regex(/^[a-z0-9]{12,}$/, 'Invalid Amplify App ID'),
  branch: z.string().min(1),
  region: awsRegionSchema,
  domainName: z.string().optional(),
});

export type AmplifyConfig = z.infer<typeof amplifyConfigSchema>;

// ============================================
// Helper Functions
// ============================================

/**
 * Validate configuration and return typed result
 * Throws ZodError with detailed messages on failure
 */
export function validateConfig<T extends z.ZodType>(
  schema: T,
  config: unknown
): z.infer<T> {
  return schema.parse(config);
}

/**
 * Safe validation - returns result object instead of throwing
 */
export function safeValidateConfig<T extends z.ZodType>(
  schema: T,
  config: unknown
): { success: true; data: z.infer<T> } | { success: false; errors: z.ZodError } {
  const result = schema.safeParse(config);
  if (result.success) {
    return { success: true, data: result.data };
  }
  return { success: false, errors: result.error };
}

/**
 * Format Zod errors for human-readable output
 */
export function formatValidationErrors(errors: z.ZodError): string[] {
  return errors.errors.map((err) => {
    const path = err.path.join('.');
    return `${path}: ${err.message}`;
  });
}
