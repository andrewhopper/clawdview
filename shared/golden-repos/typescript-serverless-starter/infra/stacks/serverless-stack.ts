import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as lambdaPython from 'aws-cdk-lib/aws-lambda-python-alpha';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';
import * as path from 'path';

export interface ServerlessStackProps extends cdk.StackProps {
  stageName: string;
  existingUserPoolId?: string;
  existingUserPoolArn?: string;
  existingUserPoolClientId?: string;
  cognitoDomain?: string;
}

export class ServerlessStack extends cdk.Stack {
  public readonly api: apigateway.RestApi;
  public readonly table: dynamodb.Table;
  public readonly helloFunction: lambda.Function;
  public readonly bedrockFunction: lambda.Function;
  public readonly userPool: cognito.IUserPool;
  public readonly userPoolClient: cognito.IUserPoolClient;
  public readonly secret: secretsmanager.Secret;

  constructor(scope: Construct, id: string, props: ServerlessStackProps) {
    super(scope, id, props);

    const { stageName, existingUserPoolId, existingUserPoolArn, existingUserPoolClientId, cognitoDomain } = props;

    // === COGNITO ===
    // Use existing user pool (auth.b.lfg.new) or create new one
    if (existingUserPoolId || existingUserPoolArn) {
      // Import existing user pool
      if (existingUserPoolArn) {
        this.userPool = cognito.UserPool.fromUserPoolArn(
          this, 'ExistingUserPool', existingUserPoolArn
        );
      } else {
        this.userPool = cognito.UserPool.fromUserPoolId(
          this, 'ExistingUserPool', existingUserPoolId!
        );
      }

      if (existingUserPoolClientId) {
        // Use existing client
        this.userPoolClient = cognito.UserPoolClient.fromUserPoolClientId(
          this, 'ExistingUserPoolClient', existingUserPoolClientId
        );
      } else {
        // Create a new client for the existing pool (auth.b.lfg.new)
        // Note: This requires the user pool to support client creation
        // For shared pools, you may need to create the client manually
        this.userPoolClient = new cognito.UserPoolClient(this, 'UserPoolClient', {
          userPool: this.userPool as cognito.UserPool,
          userPoolClientName: `serverless-starter-${stageName}`,
          authFlows: {
            userPassword: true,
            userSrp: true,
          },
          oAuth: {
            flows: { authorizationCodeGrant: true },
            scopes: [cognito.OAuthScope.OPENID, cognito.OAuthScope.EMAIL, cognito.OAuthScope.PROFILE],
            callbackUrls: [
              'http://localhost:5173/callback',
              'http://localhost:3000/callback',
            ],
            logoutUrls: [
              'http://localhost:5173/',
              'http://localhost:3000/',
            ],
          },
        });
      }

      // Output info about using existing pool
      new cdk.CfnOutput(this, 'AuthPoolInfo', {
        value: 'Using existing auth.b.lfg.new user pool',
        description: 'Cognito configuration source',
      });
    } else {
      // Create new user pool (only if COGNITO_CREATE_NEW=true)
      const newUserPool = new cognito.UserPool(this, 'UserPool', {
        userPoolName: `serverless-starter-${stageName}`,
        selfSignUpEnabled: true,
        signInAliases: { email: true },
        autoVerify: { email: true },
        standardAttributes: {
          email: { required: true, mutable: true },
        },
        passwordPolicy: {
          minLength: 8,
          requireLowercase: true,
          requireUppercase: true,
          requireDigits: true,
          requireSymbols: false,
        },
        accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
        removalPolicy: stageName === 'prod'
          ? cdk.RemovalPolicy.RETAIN
          : cdk.RemovalPolicy.DESTROY,
      });
      this.userPool = newUserPool;

      this.userPoolClient = new cognito.UserPoolClient(this, 'UserPoolClient', {
        userPool: newUserPool,
        userPoolClientName: `serverless-starter-${stageName}`,
        authFlows: {
          userPassword: true,
          userSrp: true,
        },
        oAuth: {
          flows: { authorizationCodeGrant: true },
          scopes: [cognito.OAuthScope.OPENID, cognito.OAuthScope.EMAIL, cognito.OAuthScope.PROFILE],
          callbackUrls: ['http://localhost:5173/callback'],
          logoutUrls: ['http://localhost:5173/'],
        },
      });

      // Add domain for hosted UI
      newUserPool.addDomain('CognitoDomain', {
        cognitoDomain: {
          domainPrefix: `serverless-starter-${stageName}-${cdk.Aws.ACCOUNT_ID}`,
        },
      });
    }

    // === SECRETS MANAGER ===
    this.secret = new secretsmanager.Secret(this, 'AppSecrets', {
      secretName: `serverless-starter/${stageName}/config`,
      description: 'Configuration secrets for serverless starter',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({
          api_key: 'placeholder-update-me',
        }),
        generateStringKey: 'generated_key',
      },
    });

    // === DYNAMODB ===
    this.table = new dynamodb.Table(this, 'MainTable', {
      tableName: `serverless-starter-${stageName}`,
      partitionKey: { name: 'pk', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'sk', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: stageName === 'prod'
        ? cdk.RemovalPolicy.RETAIN
        : cdk.RemovalPolicy.DESTROY,
      pointInTimeRecovery: stageName === 'prod',
      timeToLiveAttribute: 'ttl',
    });

    this.table.addGlobalSecondaryIndex({
      indexName: 'gsi1',
      partitionKey: { name: 'gsi1pk', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'gsi1sk', type: dynamodb.AttributeType.STRING },
      projectionType: dynamodb.ProjectionType.ALL,
    });

    // === LAMBDA ROLES ===
    // TypeScript Lambda role
    const nodeLambdaRole = new iam.Role(this, 'NodeLambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSXRayDaemonWriteAccess'),
      ],
    });

    // Python Lambda role with Bedrock permissions
    const pythonLambdaRole = new iam.Role(this, 'PythonLambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSXRayDaemonWriteAccess'),
      ],
    });

    // Bedrock permissions
    pythonLambdaRole.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'bedrock:InvokeModel',
        'bedrock:InvokeModelWithResponseStream',
      ],
      resources: ['*'],
    }));

    // === TYPESCRIPT LAMBDA ===
    this.helloFunction = new lambda.Function(this, 'HelloFunction', {
      functionName: `serverless-starter-hello-${stageName}`,
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: 'hello.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../../backend/dist')),
      role: nodeLambdaRole,
      timeout: cdk.Duration.seconds(30),
      memorySize: 256,
      environment: {
        TABLE_NAME: this.table.tableName,
        STAGE: stageName,
        NODE_OPTIONS: '--enable-source-maps',
      },
      tracing: lambda.Tracing.ACTIVE,
      logRetention: logs.RetentionDays.TWO_WEEKS,
    });

    this.table.grantReadWriteData(this.helloFunction);

    // === PYTHON LAMBDA (Bedrock) ===
    this.bedrockFunction = new lambdaPython.PythonFunction(this, 'BedrockFunction', {
      functionName: `serverless-starter-bedrock-${stageName}`,
      entry: path.join(__dirname, '../../backend-python/src'),
      runtime: lambda.Runtime.PYTHON_3_11,
      handler: 'handler',
      index: 'handlers/bedrock_handler.py',
      role: pythonLambdaRole,
      timeout: cdk.Duration.seconds(60),
      memorySize: 512,
      environment: {
        TABLE_NAME: this.table.tableName,
        SECRETS_ARN: this.secret.secretArn,
        STAGE: stageName,
        POWERTOOLS_SERVICE_NAME: 'bedrock-handler',
        POWERTOOLS_METRICS_NAMESPACE: 'ServerlessStarter',
        LOG_LEVEL: 'INFO',
      },
      tracing: lambda.Tracing.ACTIVE,
      logRetention: logs.RetentionDays.TWO_WEEKS,
    });

    this.table.grantReadWriteData(this.bedrockFunction);
    this.secret.grantRead(this.bedrockFunction);

    // === API GATEWAY ===
    const logGroup = new logs.LogGroup(this, 'ApiAccessLogs', {
      logGroupName: `/aws/apigateway/serverless-starter-${stageName}`,
      retention: logs.RetentionDays.TWO_WEEKS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    this.api = new apigateway.RestApi(this, 'ServerlessApi', {
      restApiName: `serverless-starter-${stageName}`,
      description: 'Serverless Starter API with Cognito auth (auth.b.lfg.new)',
      deployOptions: {
        stageName: stageName,
        tracingEnabled: true,
        dataTraceEnabled: true,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        accessLogDestination: new apigateway.LogGroupLogDestination(logGroup),
        accessLogFormat: apigateway.AccessLogFormat.jsonWithStandardFields({
          caller: true,
          httpMethod: true,
          ip: true,
          protocol: true,
          requestTime: true,
          resourcePath: true,
          responseLength: true,
          status: true,
          user: true,
        }),
        metricsEnabled: true,
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
          'X-Amz-Security-Token',
        ],
      },
    });

    // Cognito Authorizer
    const authorizer = new apigateway.CognitoUserPoolsAuthorizer(this, 'CognitoAuthorizer', {
      cognitoUserPools: [this.userPool as cognito.UserPool],
      authorizerName: 'CognitoAuthorizer',
      identitySource: 'method.request.header.Authorization',
    });

    const authMethodOptions: apigateway.MethodOptions = {
      authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
    };

    // Lambda integrations
    const helloIntegration = new apigateway.LambdaIntegration(this.helloFunction);
    const bedrockIntegration = new apigateway.LambdaIntegration(this.bedrockFunction);

    // Public endpoints (no auth)
    const healthResource = this.api.root.addResource('health');
    healthResource.addMethod('GET', helloIntegration);

    const helloResource = this.api.root.addResource('hello');
    helloResource.addMethod('GET', helloIntegration);

    // Protected endpoints (require auth)
    helloResource.addMethod('POST', helloIntegration, authMethodOptions);

    const itemsResource = this.api.root.addResource('items');
    itemsResource.addMethod('GET', helloIntegration, authMethodOptions);
    itemsResource.addMethod('POST', helloIntegration, authMethodOptions);

    const itemResource = itemsResource.addResource('{id}');
    itemResource.addMethod('GET', helloIntegration, authMethodOptions);
    itemResource.addMethod('PUT', helloIntegration, authMethodOptions);
    itemResource.addMethod('DELETE', helloIntegration, authMethodOptions);

    // AI endpoints (protected)
    const aiResource = this.api.root.addResource('ai');
    const aiHealthResource = aiResource.addResource('health');
    aiHealthResource.addMethod('GET', bedrockIntegration);

    const chatResource = aiResource.addResource('chat');
    chatResource.addMethod('POST', bedrockIntegration, authMethodOptions);

    const embeddingsResource = aiResource.addResource('embeddings');
    embeddingsResource.addMethod('POST', bedrockIntegration, authMethodOptions);

    // === OUTPUTS ===
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: this.api.url,
      description: 'API Gateway URL',
      exportName: `${id}-ApiUrl`,
    });

    new cdk.CfnOutput(this, 'TableName', {
      value: this.table.tableName,
      description: 'DynamoDB Table Name',
      exportName: `${id}-TableName`,
    });

    new cdk.CfnOutput(this, 'UserPoolId', {
      value: this.userPool.userPoolId,
      description: 'Cognito User Pool ID',
      exportName: `${id}-UserPoolId`,
    });

    new cdk.CfnOutput(this, 'UserPoolClientId', {
      value: this.userPoolClient.userPoolClientId,
      description: 'Cognito User Pool Client ID',
      exportName: `${id}-UserPoolClientId`,
    });

    if (!cognitoDomain) {
      throw new Error('cognitoDomain prop is required but was not provided. Check stack props in bin/app.ts');
    }

    new cdk.CfnOutput(this, 'CognitoDomain', {
      value: cognitoDomain,
      description: 'Cognito Hosted UI Domain',
      exportName: `${id}-CognitoDomain`,
    });

    new cdk.CfnOutput(this, 'SecretsArn', {
      value: this.secret.secretArn,
      description: 'Secrets Manager ARN',
      exportName: `${id}-SecretsArn`,
    });

    new cdk.CfnOutput(this, 'HelloFunctionArn', {
      value: this.helloFunction.functionArn,
      description: 'Hello Lambda Function ARN',
      exportName: `${id}-HelloFunctionArn`,
    });

    new cdk.CfnOutput(this, 'BedrockFunctionArn', {
      value: this.bedrockFunction.functionArn,
      description: 'Bedrock Lambda Function ARN',
      exportName: `${id}-BedrockFunctionArn`,
    });
  }
}
