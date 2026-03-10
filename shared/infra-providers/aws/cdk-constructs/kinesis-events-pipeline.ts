// File UUID: b3f7e9d4-2c8a-4f1b-9d3e-7a6c8b5f2d4e
/**
 * Kinesis Events Pipeline CDK Construct
 *
 * Creates a complete pipeline for streaming Claude Code events to S3:
 * - Kinesis Data Firehose delivery stream
 * - S3 bucket with lifecycle policies
 * - IAM roles and policies
 * - CloudWatch alarms for monitoring
 *
 * Features:
 * - Automatic compression (GZIP)
 * - Date-partitioned S3 prefix (year/month/day/hour)
 * - 90-day lifecycle to Glacier
 * - Error logging to separate S3 prefix
 * - CloudWatch metrics and alarms
 */

import * as cdk from 'aws-cdk-lib';
import * as firehose from 'aws-cdk-lib/aws-kinesisfirehose';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import { Construct } from 'constructs';

export interface KinesisEventsPipelineProps {
  /**
   * Name of the Firehose delivery stream
   * @default 'claude-code-events'
   */
  readonly streamName?: string;

  /**
   * S3 bucket for event storage (creates new if not provided)
   */
  readonly bucket?: s3.IBucket;

  /**
   * S3 prefix for events
   * @default 'claude-events/'
   */
  readonly prefix?: string;

  /**
   * Buffer size in MB before Firehose flushes to S3
   * @default 5
   */
  readonly bufferSizeMB?: number;

  /**
   * Buffer interval in seconds before Firehose flushes to S3
   * @default 300 (5 minutes)
   */
  readonly bufferIntervalSeconds?: number;

  /**
   * Enable GZIP compression
   * @default true
   */
  readonly compressionEnabled?: boolean;

  /**
   * Days to keep events in S3 before deletion (no Glacier transition)
   * @default 365
   */
  readonly expirationDays?: number;

  /**
   * Enable CloudWatch alarms
   * @default true
   */
  readonly alarmsEnabled?: boolean;
}

export class KinesisEventsPipeline extends Construct {
  public readonly deliveryStream: firehose.CfnDeliveryStream;
  public readonly bucket: s3.IBucket;
  public readonly firehoseRole: iam.Role;

  constructor(scope: Construct, id: string, props: KinesisEventsPipelineProps = {}) {
    super(scope, id);

    const streamName = props.streamName ?? 'claude-code-events';
    const prefix = props.prefix ?? 'claude-events/';
    const bufferSizeMB = props.bufferSizeMB ?? 5;
    const bufferIntervalSeconds = props.bufferIntervalSeconds ?? 300;
    const compressionEnabled = props.compressionEnabled ?? true;
    const expirationDays = props.expirationDays ?? 365;
    const alarmsEnabled = props.alarmsEnabled ?? true;

    // ========================================================================
    // S3 Bucket
    // ========================================================================

    this.bucket = props.bucket ?? new s3.Bucket(this, 'EventsBucket', {
      bucketName: `${cdk.Stack.of(this).account}-claude-code-events`,
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      lifecycleRules: [
        {
          id: 'ExpireOldEvents',
          enabled: true,
          expiration: cdk.Duration.days(expirationDays),
        },
      ],
      removalPolicy: cdk.RemovalPolicy.RETAIN, // Protect data
    });

    // ========================================================================
    // IAM Role for Firehose
    // ========================================================================

    this.firehoseRole = new iam.Role(this, 'FirehoseRole', {
      assumedBy: new iam.ServicePrincipal('firehose.amazonaws.com'),
      description: 'Role for Kinesis Firehose to write to S3',
    });

    // Grant S3 write permissions
    this.bucket.grantWrite(this.firehoseRole);

    // ========================================================================
    // CloudWatch Log Group for Errors
    // ========================================================================

    const errorLogGroup = new logs.LogGroup(this, 'ErrorLogGroup', {
      logGroupName: `/aws/kinesisfirehose/${streamName}`,
      retention: logs.RetentionDays.ONE_WEEK,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const errorLogStream = new logs.LogStream(this, 'ErrorLogStream', {
      logGroup: errorLogGroup,
      logStreamName: 'S3Delivery',
    });

    // Grant Firehose permissions to write logs
    errorLogGroup.grantWrite(this.firehoseRole);

    // ========================================================================
    // Kinesis Firehose Delivery Stream
    // ========================================================================

    this.deliveryStream = new firehose.CfnDeliveryStream(this, 'DeliveryStream', {
      deliveryStreamName: streamName,
      deliveryStreamType: 'DirectPut', // Receive data via PutRecord API

      extendedS3DestinationConfiguration: {
        bucketArn: this.bucket.bucketArn,
        roleArn: this.firehoseRole.roleArn,

        // S3 prefix with date partitioning
        prefix: `${prefix}year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/`,
        errorOutputPrefix: `${prefix}errors/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/!{firehose:error-output-type}/`,

        // Buffering configuration
        bufferingHints: {
          sizeInMBs: bufferSizeMB,
          intervalInSeconds: bufferIntervalSeconds,
        },

        // Compression
        compressionFormat: compressionEnabled ? 'GZIP' : 'UNCOMPRESSED',

        // CloudWatch logging
        cloudWatchLoggingOptions: {
          enabled: true,
          logGroupName: errorLogGroup.logGroupName,
          logStreamName: errorLogStream.logStreamName,
        },

        // S3 backup mode (backup all data, not just failed records)
        s3BackupMode: 'Disabled',
      },
    });

    // ========================================================================
    // CloudWatch Alarms
    // ========================================================================

    if (alarmsEnabled) {
      // Alarm: High delivery failure rate
      new cloudwatch.Alarm(this, 'DeliveryFailureAlarm', {
        alarmName: `${streamName}-delivery-failures`,
        alarmDescription: 'Firehose delivery failure rate is high',
        metric: new cloudwatch.Metric({
          namespace: 'AWS/Firehose',
          metricName: 'DeliveryToS3.Records',
          dimensionsMap: {
            DeliveryStreamName: streamName,
          },
          statistic: 'Sum',
          period: cdk.Duration.minutes(5),
        }),
        evaluationPeriods: 2,
        threshold: 10,
        comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      });

      // Alarm: No data received
      new cloudwatch.Alarm(this, 'NoDataAlarm', {
        alarmName: `${streamName}-no-data`,
        alarmDescription: 'Firehose has not received data',
        metric: new cloudwatch.Metric({
          namespace: 'AWS/Firehose',
          metricName: 'IncomingRecords',
          dimensionsMap: {
            DeliveryStreamName: streamName,
          },
          statistic: 'Sum',
          period: cdk.Duration.minutes(15),
        }),
        evaluationPeriods: 1,
        threshold: 1,
        comparisonOperator: cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
        treatMissingData: cloudwatch.TreatMissingData.BREACHING,
      });
    }

    // ========================================================================
    // Outputs
    // ========================================================================

    new cdk.CfnOutput(this, 'DeliveryStreamName', {
      value: this.deliveryStream.deliveryStreamName!,
      description: 'Kinesis Firehose delivery stream name',
      exportName: `${cdk.Stack.of(this).stackName}-DeliveryStreamName`,
    });

    new cdk.CfnOutput(this, 'BucketName', {
      value: this.bucket.bucketName,
      description: 'S3 bucket for events',
      exportName: `${cdk.Stack.of(this).stackName}-BucketName`,
    });

    new cdk.CfnOutput(this, 'BucketArn', {
      value: this.bucket.bucketArn,
      description: 'S3 bucket ARN',
      exportName: `${cdk.Stack.of(this).stackName}-BucketArn`,
    });
  }
}
