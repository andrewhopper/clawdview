/**
 * Base stack with common configuration.
 */

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { EnvConfig, getDefaultTags, getStackName } from '../../config';

export interface BaseStackProps extends cdk.StackProps {
  config: EnvConfig;
}

export class BaseStack extends cdk.Stack {
  protected readonly config: EnvConfig;

  constructor(scope: Construct, id: string, props: BaseStackProps) {
    const stackName = getStackName(props.config, id);

    super(scope, stackName, {
      ...props,
      stackName,
      env: {
        account: props.config.account,
        region: props.config.region,
      },
      tags: getDefaultTags(props.config),
    });

    this.config = props.config;
  }

  /**
   * Check if this is a production deployment.
   */
  protected get isProduction(): boolean {
    return this.config.env === 'prod';
  }

  /**
   * Get resource name with environment prefix.
   */
  protected resourceName(name: string): string {
    return `${this.config.projectName}-${this.config.env}-${name}`;
  }

  /**
   * Apply removal policy based on environment.
   */
  protected get removalPolicy(): cdk.RemovalPolicy {
    return this.isProduction
      ? cdk.RemovalPolicy.RETAIN
      : cdk.RemovalPolicy.DESTROY;
  }
}
