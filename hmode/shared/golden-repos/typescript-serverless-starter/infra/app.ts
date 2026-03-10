#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import * as ssm from 'aws-cdk-lib/aws-ssm';
import { ServerlessStack } from './stacks/serverless-stack';

const app = new cdk.App();

if (!process.env.CDK_DEFAULT_REGION && !process.env.AWS_REGION) {
  throw new Error('Missing required environment variable: CDK_DEFAULT_REGION or AWS_REGION');
}

if (!process.env.STAGE_NAME) {
  throw new Error('Missing required environment variable: STAGE_NAME (dev, stage, prod)');
}

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT || process.env.AWS_ACCOUNT_ID,
  region: process.env.CDK_DEFAULT_REGION || process.env.AWS_REGION,
};

const stageName = process.env.STAGE_NAME;

/**
 * Cognito User Pool Configuration
 *
 * Priority order:
 * 1. Environment variables (COGNITO_USER_POOL_ID, etc.)
 * 2. SSM Parameter Store (/shared/auth/*)
 * 3. Hardcoded defaults (auth.b.lfg.new)
 *
 * Set COGNITO_CREATE_NEW=true to create a new user pool instead.
 */

// SSM Parameter Store paths for shared Cognito config
// Must match shared/cdk-constructs/src/config/ssm-paths.ts
const SSM_COGNITO_USER_POOL_ID = '/protoflow/shared/cognito/user-pool-id';
const SSM_COGNITO_USER_POOL_ARN = '/protoflow/shared/cognito/user-pool-arn';
const SSM_COGNITO_DOMAIN = '/protoflow/shared/cognito/domain';

/**
 * Read from SSM at synth time.
 * Requires SSM parameters to be bootstrapped first via:
 *   python scripts/setup-cognito-ssm-params.py
 */
function getFromSsm(scope: cdk.App, ssmPath: string): string {
  return ssm.StringParameter.valueFromLookup(scope, ssmPath);
}

// Determine if we should create a new pool or use existing
const createNewPool = process.env.COGNITO_CREATE_NEW === 'true';

let existingUserPoolId: string | undefined;
let existingUserPoolArn: string | undefined;
let cognitoDomain: string | undefined;

if (!createNewPool) {
  // Priority: env var > SSM (no hardcoded defaults)
  existingUserPoolId = process.env.COGNITO_USER_POOL_ID ||
    getFromSsm(app, SSM_COGNITO_USER_POOL_ID);

  existingUserPoolArn = process.env.COGNITO_USER_POOL_ARN ||
    getFromSsm(app, SSM_COGNITO_USER_POOL_ARN);

  cognitoDomain = process.env.COGNITO_DOMAIN ||
    getFromSsm(app, SSM_COGNITO_DOMAIN);
}

const existingUserPoolClientId = process.env.COGNITO_USER_POOL_CLIENT_ID;

// Log configuration source
console.log('Auth Configuration:');
console.log(`  Create New Pool: ${createNewPool}`);
if (!createNewPool) {
  console.log(`  User Pool ID: ${existingUserPoolId}`);
  console.log(`  Domain: ${cognitoDomain}`);
  console.log(`  Source: ${process.env.COGNITO_USER_POOL_ID ? 'env' : 'SSM/default'}`);
}

new ServerlessStack(app, `ServerlessStarter-${stageName}`, {
  env,
  stageName,
  existingUserPoolId,
  existingUserPoolArn,
  existingUserPoolClientId,
  cognitoDomain,
  description: 'Serverless starter with API Gateway, Lambda, DynamoDB, Cognito (auth.b.lfg.new), CloudWatch, and X-Ray',
  tags: {
    Project: 'serverless-starter',
    Environment: stageName,
    ManagedBy: 'CDK',
    AuthProvider: cognitoDomain || (createNewPool ? 'new-pool' : 'undefined'),
  },
});

app.synth();
