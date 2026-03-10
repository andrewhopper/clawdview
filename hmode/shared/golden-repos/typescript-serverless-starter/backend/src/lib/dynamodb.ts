import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand, PutCommand, QueryCommand, DeleteCommand, UpdateCommand } from '@aws-sdk/lib-dynamodb';
import AWSXRay from 'aws-xray-sdk-core';

// Create X-Ray traced DynamoDB client
const client = AWSXRay.captureAWSv3Client(new DynamoDBClient({}));
export const docClient = DynamoDBDocumentClient.from(client, {
  marshallOptions: {
    removeUndefinedValues: true,
    convertEmptyValues: true,
  },
});

const TABLE_NAME = process.env.TABLE_NAME;

if (!TABLE_NAME) {
  throw new Error('Missing required environment variable: TABLE_NAME');
}

export interface BaseEntity {
  pk: string;
  sk: string;
  gsi1pk?: string;
  gsi1sk?: string;
  createdAt: string;
  updatedAt: string;
  ttl?: number;
}

export async function getItem<T extends BaseEntity>(pk: string, sk: string): Promise<T | null> {
  const result = await docClient.send(new GetCommand({
    TableName: TABLE_NAME,
    Key: { pk, sk },
  }));
  return (result.Item as T) || null;
}

export async function putItem<T extends BaseEntity>(item: T): Promise<T> {
  await docClient.send(new PutCommand({
    TableName: TABLE_NAME,
    Item: item,
  }));
  return item;
}

export async function queryItems<T extends BaseEntity>(
  keyCondition: string,
  expressionValues: Record<string, unknown>,
  indexName?: string
): Promise<T[]> {
  const result = await docClient.send(new QueryCommand({
    TableName: TABLE_NAME,
    IndexName: indexName,
    KeyConditionExpression: keyCondition,
    ExpressionAttributeValues: expressionValues,
  }));
  return (result.Items as T[]) || [];
}

export async function deleteItem(pk: string, sk: string): Promise<void> {
  await docClient.send(new DeleteCommand({
    TableName: TABLE_NAME,
    Key: { pk, sk },
  }));
}

export async function updateItem(
  pk: string,
  sk: string,
  updateExpression: string,
  expressionValues: Record<string, unknown>,
  expressionNames?: Record<string, string>
): Promise<void> {
  await docClient.send(new UpdateCommand({
    TableName: TABLE_NAME,
    Key: { pk, sk },
    UpdateExpression: updateExpression,
    ExpressionAttributeValues: expressionValues,
    ExpressionAttributeNames: expressionNames,
  }));
}

// Generate a time-based sort key for ordering
export function generateSortKey(prefix: string = ''): string {
  const timestamp = new Date().toISOString();
  const random = Math.random().toString(36).substring(2, 8);
  return prefix ? `${prefix}#${timestamp}#${random}` : `${timestamp}#${random}`;
}

// Generate TTL value (seconds since epoch)
export function generateTTL(daysFromNow: number): number {
  return Math.floor(Date.now() / 1000) + (daysFromNow * 24 * 60 * 60);
}
