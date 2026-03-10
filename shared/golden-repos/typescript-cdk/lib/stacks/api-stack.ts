/**
 * Example API stack demonstrating patterns.
 */

import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as logs from 'aws-cdk-lib/aws-logs';
import { Construct } from 'constructs';
import { BaseStack, BaseStackProps } from '../constructs/base-stack';

export class ApiStack extends BaseStack {
  public readonly api: apigateway.RestApi;
  public readonly handler: lambda.Function;

  constructor(scope: Construct, id: string, props: BaseStackProps) {
    super(scope, id, props);

    const { compute, monitoring } = this.config;

    // Lambda function
    this.handler = new lambda.Function(this, 'Handler', {
      functionName: this.resourceName('api-handler'),
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
        exports.handler = async (event) => {
          return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Hello from ${this.config.env}!' }),
          };
        };
      `),
      memorySize: compute.lambdaMemory,
      timeout: cdk.Duration.seconds(compute.lambdaTimeout),
      tracing: monitoring.enableTracing
        ? lambda.Tracing.ACTIVE
        : lambda.Tracing.DISABLED,
      environment: {
        ENV: this.config.env,
        PROJECT_NAME: this.config.projectName,
      },
      logRetention: monitoring.logRetentionDays,
    });

    // API Gateway
    this.api = new apigateway.RestApi(this, 'Api', {
      restApiName: this.resourceName('api'),
      description: `${this.config.projectName} API (${this.config.env})`,
      deployOptions: {
        stageName: this.config.env,
        tracingEnabled: monitoring.enableTracing,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
      },
    });

    // Add Lambda integration
    const integration = new apigateway.LambdaIntegration(this.handler);
    this.api.root.addMethod('GET', integration);
    this.api.root.addResource('health').addMethod('GET', integration);

    // Outputs
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: this.api.url,
      description: 'API Gateway URL',
    });
  }
}
