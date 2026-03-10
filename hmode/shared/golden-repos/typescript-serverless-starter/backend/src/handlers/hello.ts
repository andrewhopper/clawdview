import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand, PutCommand, QueryCommand, DeleteCommand } from '@aws-sdk/lib-dynamodb';

// X-Ray tracing
import AWSXRay from 'aws-xray-sdk-core';

const client = AWSXRay.captureAWSv3Client(new DynamoDBClient({}));
const docClient = DynamoDBDocumentClient.from(client);

const TABLE_NAME = process.env.TABLE_NAME || '';

interface Item {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

const headers = {
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token',
  'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
};

function response(statusCode: number, body: object): APIGatewayProxyResult {
  return {
    statusCode,
    headers,
    body: JSON.stringify(body),
  };
}

export async function handler(event: APIGatewayProxyEvent, context: Context): Promise<APIGatewayProxyResult> {
  console.log('Event:', JSON.stringify(event, null, 2));

  const { httpMethod, path, pathParameters, body } = event;

  try {
    // Health check
    if (path === '/health') {
      return response(200, {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        requestId: context.awsRequestId,
      });
    }

    // Hello endpoint
    if (path === '/hello') {
      if (httpMethod === 'GET') {
        return response(200, {
          message: 'Hello, World!',
          timestamp: new Date().toISOString(),
          stage: process.env.STAGE,
        });
      }

      if (httpMethod === 'POST') {
        const payload = body ? JSON.parse(body) : {};
        return response(200, {
          message: `Hello, ${payload.name || 'World'}!`,
          timestamp: new Date().toISOString(),
          echo: payload,
        });
      }
    }

    // Items CRUD
    if (path.startsWith('/items')) {
      const id = pathParameters?.id;

      // GET /items - List all items
      if (httpMethod === 'GET' && !id) {
        const result = await docClient.send(new QueryCommand({
          TableName: TABLE_NAME,
          IndexName: 'gsi1',
          KeyConditionExpression: 'gsi1pk = :pk',
          ExpressionAttributeValues: {
            ':pk': 'ITEM',
          },
        }));

        return response(200, {
          items: result.Items || [],
          count: result.Count || 0,
        });
      }

      // GET /items/:id - Get single item
      if (httpMethod === 'GET' && id) {
        const result = await docClient.send(new GetCommand({
          TableName: TABLE_NAME,
          Key: { pk: `ITEM#${id}`, sk: `ITEM#${id}` },
        }));

        if (!result.Item) {
          return response(404, { error: 'Item not found' });
        }

        return response(200, { item: result.Item });
      }

      // POST /items - Create item
      if (httpMethod === 'POST') {
        const payload = body ? JSON.parse(body) : {};
        const itemId = crypto.randomUUID();
        const now = new Date().toISOString();

        const item: Item & { pk: string; sk: string; gsi1pk: string; gsi1sk: string } = {
          pk: `ITEM#${itemId}`,
          sk: `ITEM#${itemId}`,
          gsi1pk: 'ITEM',
          gsi1sk: now,
          id: itemId,
          name: payload.name || 'Unnamed',
          description: payload.description,
          createdAt: now,
          updatedAt: now,
        };

        await docClient.send(new PutCommand({
          TableName: TABLE_NAME,
          Item: item,
        }));

        return response(201, { item });
      }

      // PUT /items/:id - Update item
      if (httpMethod === 'PUT' && id) {
        const payload = body ? JSON.parse(body) : {};
        const now = new Date().toISOString();

        // Get existing item
        const existing = await docClient.send(new GetCommand({
          TableName: TABLE_NAME,
          Key: { pk: `ITEM#${id}`, sk: `ITEM#${id}` },
        }));

        if (!existing.Item) {
          return response(404, { error: 'Item not found' });
        }

        const updatedItem = {
          ...existing.Item,
          name: payload.name || existing.Item.name,
          description: payload.description ?? existing.Item.description,
          updatedAt: now,
        };

        await docClient.send(new PutCommand({
          TableName: TABLE_NAME,
          Item: updatedItem,
        }));

        return response(200, { item: updatedItem });
      }

      // DELETE /items/:id - Delete item
      if (httpMethod === 'DELETE' && id) {
        await docClient.send(new DeleteCommand({
          TableName: TABLE_NAME,
          Key: { pk: `ITEM#${id}`, sk: `ITEM#${id}` },
        }));

        return response(204, {});
      }
    }

    return response(404, { error: 'Not found' });
  } catch (error) {
    console.error('Error:', error);
    return response(500, {
      error: 'Internal server error',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
}
