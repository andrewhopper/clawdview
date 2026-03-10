// File UUID: 4e9f7c3a-2b1d-4e8f-9c2a-5d6e7f8a9b0c

/**
 * Example: Using SSMResolver in AWS CDK Auth Stack
 *
 * This example shows how to migrate from hardcoded SSM paths
 * to hierarchical resolver with automatic fallback.
 */

import * as cdk from 'aws-cdk-lib';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as iot from 'aws-cdk-lib/aws-iot';
import { Construct } from 'constructs';
import { SSMResolver } from '@protoflow/ssm-resolver';

interface AuthStackProps extends cdk.StackProps {
  environment: 'dev' | 'prod' | 'beta';
}

export class AuthStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: AuthStackProps) {
    super(scope, id, props);

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // BEFORE (hardcoded paths)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    // const userPoolId = ssm.StringParameter.valueFromLookup(
    //   this,
    //   '/protoflow/shared/cognito/user-pool-id'
    // );

    // const googleClientId = ssm.StringParameter.valueFromLookup(
    //   this,
    //   '/gocoder/auth/google/client-id'
    // );

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // AFTER (hierarchical resolver with fallback)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    const ssm = new SSMResolver(this, {
      accountType: 'work',
      environment: props.environment,
      project: 'gocoder',
    });

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // 1. Read shared Cognito pool (account-level, inherited by all)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    // Resolves with fallback:
    // 1. /work/dev/gocoder/auth/cognito/user-pool-id (project override)
    // 2. /work/dev/auth/cognito/user-pool-id (environment default)
    // 3. /work/auth/cognito/user-pool-id (account default) ✓ FOUND
    // 4. /shared/auth/cognito/user-pool-id (global default)
    const userPoolId = ssm.resolve('auth/cognito', 'user-pool-id', {
      required: true,
      debug: true,
    });

    const userPoolArn = ssm.resolve('auth/cognito', 'user-pool-arn', {
      required: true,
    });

    const cognitoDomain = ssm.resolve('auth/cognito', 'domain', {
      required: true,
    });

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // 2. Read Google OAuth client ID (can override at project level)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    // Dev environment might override with test credentials
    // Prod inherits from account default
    const googleClientId = ssm.resolve('auth/google', 'client-id');
    const googleClientSecret = ssm.resolve('auth/google', 'client-secret');

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // 3. Create Cognito resources
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    const userPool = cognito.UserPool.fromUserPoolId(
      this,
      'UserPool',
      userPoolId
    );

    const appClient = new cognito.UserPoolClient(this, 'AppClient', {
      userPool,
      authFlows: {
        userPassword: true,
        userSrp: true,
      },
      oAuth: {
        flows: {
          authorizationCodeGrant: true,
        },
        scopes: [cognito.OAuthScope.OPENID, cognito.OAuthScope.EMAIL],
        callbackUrls: [
          `https://gocoder-${props.environment}.b.lfg.new/auth/callback`,
        ],
      },
    });

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // 4. Write generated values back to SSM (project-specific)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    // Frontend needs to know the client ID
    ssm.write('auth', 'cognito-client-id', appClient.userPoolClientId, {
      description: 'Cognito app client ID for GoCoder frontend',
    });

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // 5. IoT endpoint (environment-shared for all projects in env)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    const iotEndpoint = ssm.resolve('iot', 'endpoint');

    if (iotEndpoint) {
      // Use existing IoT endpoint
      new cdk.CfnOutput(this, 'IoTEndpoint', {
        value: iotEndpoint,
        description: 'IoT Core endpoint (inherited from environment)',
      });
    } else {
      // Create new IoT endpoint and store at environment level
      const endpoint = `${cdk.Aws.ACCOUNT_ID}.iot.${cdk.Aws.REGION}.amazonaws.com`;

      ssm.write('iot', 'endpoint', endpoint, {
        scope: 'environment',
        description: `IoT endpoint for ${props.environment} environment`,
      });
    }

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // 6. Feature flags (environment-specific)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    const enableGoogleOAuth = ssm.resolve('features', 'enable-google-oauth');
    const enableCodeExecution = ssm.resolve('features', 'enable-code-execution');

    new cdk.CfnOutput(this, 'GoogleOAuthEnabled', {
      value: enableGoogleOAuth || 'false',
    });

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // 7. Runtime parameter access (for Lambda)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    // If you need to pass parameter to Lambda at runtime:
    const clientIdParam = ssm.fromName('auth', 'cognito-client-id', 'project');

    // Use in Lambda environment variable
    // myLambda.addEnvironment('COGNITO_CLIENT_ID', clientIdParam.stringValue);

    // Grant Lambda read access
    // ssm.grantRead(myLambda, 'auth', 'cognito-client-id');

    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // 8. Secure parameters (secrets)
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    // Write test user password (SecureString)
    if (props.environment === 'dev') {
      ssm.write('secrets', 'test-user-password', 'TestPassword123!', {
        scope: 'environment',
        secure: true,
        description: 'Test user password for dev environment',
      });
    }
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Benefits of This Approach:
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// 1. DRY: Cognito user pool ID stored once at /work/auth/cognito/user-pool-id
//    All projects in work account inherit it automatically

// 2. Easy Override: Dev can use test Google OAuth credentials
//    Create: /work/dev/auth/google/client-id (overrides account default)

// 3. Environment Isolation: IoT endpoints unique per environment
//    Store at: /work/dev/iot/endpoint vs /work/prod/iot/endpoint

// 4. Clear Ownership: Path shows scope immediately
//    /work/dev/gocoder/* = project-specific
//    /work/dev/* = environment-shared
//    /work/* = account-shared
//    /shared/* = global

// 5. No CloudFormation Exports: Cross-stack coupling via SSM instead
//    More flexible, can deploy stacks independently
