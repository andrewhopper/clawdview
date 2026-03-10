/**
 * Monitoring and alerting stack.
 */

import * as cdk from 'aws-cdk-lib';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import { Construct } from 'constructs';
import { BaseStack, BaseStackProps } from '../constructs/base-stack';

export class MonitoringStack extends BaseStack {
  public readonly alertTopic: sns.Topic;

  constructor(scope: Construct, id: string, props: BaseStackProps) {
    super(scope, id, props);

    const { notifications, monitoring } = this.config;

    // SNS Topic for alerts
    this.alertTopic = new sns.Topic(this, 'AlertTopic', {
      topicName: this.resourceName('alerts'),
      displayName: `${this.config.projectName} Alerts (${this.config.env})`,
    });

    // Subscribe admin email
    this.alertTopic.addSubscription(
      new subscriptions.EmailSubscription(notifications.adminEmail)
    );

    // Optional: Subscribe support email
    if (notifications.supportEmail) {
      this.alertTopic.addSubscription(
        new subscriptions.EmailSubscription(notifications.supportEmail)
      );
    }

    // Create dashboard if enabled
    if (monitoring.enableDashboards) {
      new cloudwatch.Dashboard(this, 'Dashboard', {
        dashboardName: this.resourceName('dashboard'),
        widgets: [
          [
            new cloudwatch.TextWidget({
              markdown: `# ${this.config.projectName} - ${this.config.env.toUpperCase()}`,
              width: 24,
              height: 1,
            }),
          ],
          // Add more widgets based on your needs
        ],
      });
    }

    // Outputs
    new cdk.CfnOutput(this, 'AlertTopicArn', {
      value: this.alertTopic.topicArn,
      description: 'SNS Topic ARN for alerts',
    });
  }
}
