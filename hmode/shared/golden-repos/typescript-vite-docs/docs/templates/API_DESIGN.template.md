---
title: API DESIGN - API Specifications
order: 7
description: Phase 6 - Detailed API endpoint specifications and contracts
date: YYYY-MM-DD
tags: [phase-6, design, api]
---

# API Design

## 1.0 API Overview

### 1.1 API Style
**[REST / GraphQL / gRPC / tRPC]**

### 1.2 Base URL Structure
```
Development:   https://api.dev.example.com/v1
Staging:       https://api.staging.example.com/v1
Production:    https://api.example.com/v1
```

### 1.3 Authentication
**Method:** [JWT / OAuth2 / API Key / Other]

**Header Format:**
```
Authorization: Bearer <token>
```

### 1.4 Versioning Strategy
[How API versions are managed]

## 2.0 Common Patterns

### 2.1 Request Format
```json
{
  "data": {
    // Request payload
  },
  "metadata": {
    "requestId": "uuid",
    "timestamp": "ISO-8601"
  }
}
```

### 2.2 Response Format
```json
{
  "data": {
    // Response payload
  },
  "metadata": {
    "requestId": "uuid",
    "timestamp": "ISO-8601"
  }
}
```

### 2.3 Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Additional context
    }
  },
  "metadata": {
    "requestId": "uuid",
    "timestamp": "ISO-8601"
  }
}
```

### 2.4 Pagination
```
GET /resources?page=1&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

## 3.0 Endpoints

### 3.1 [Resource Name] Endpoints

#### 3.1.1 Create [Resource]

**Endpoint:** `POST /resources`

**Description:** [What this endpoint does]

**Request Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "field1": "string",
  "field2": 123,
  "field3": {
    "nestedField": "value"
  }
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "uuid",
    "field1": "string",
    "field2": 123,
    "field3": {
      "nestedField": "value"
    },
    "createdAt": "2026-02-05T12:00:00Z",
    "updatedAt": "2026-02-05T12:00:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid auth
- `409 Conflict` - Resource already exists
- `500 Internal Server Error` - Server error

**Validation Rules:**
- `field1`: Required, max 255 characters
- `field2`: Required, integer, range 1-1000
- `field3.nestedField`: Optional, string

---

#### 3.1.2 Get [Resource]

**Endpoint:** `GET /resources/:id`

**Description:** [What this endpoint does]

**Request Headers:**
```
Authorization: Bearer <token>
```

**Path Parameters:**
- `id` (required): Resource UUID

**Response (200 OK):**
```json
{
  "data": {
    "id": "uuid",
    "field1": "string",
    "field2": 123,
    "createdAt": "2026-02-05T12:00:00Z",
    "updatedAt": "2026-02-05T12:00:00Z"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid auth
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server error

---

#### 3.1.3 List [Resources]

**Endpoint:** `GET /resources`

**Description:** [What this endpoint does]

**Request Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `sort` (optional): Sort field (e.g., `createdAt`, `-createdAt`)
- `filter[field]` (optional): Filter by field value

**Example:**
```
GET /resources?page=2&limit=10&sort=-createdAt&filter[status]=active
```

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "uuid",
      "field1": "string",
      "createdAt": "2026-02-05T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 2,
    "limit": 10,
    "total": 45,
    "totalPages": 5
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid auth
- `500 Internal Server Error` - Server error

---

#### 3.1.4 Update [Resource]

**Endpoint:** `PATCH /resources/:id`

**Description:** [What this endpoint does]

**Request Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Path Parameters:**
- `id` (required): Resource UUID

**Request Body:**
```json
{
  "field1": "updated value",
  "field2": 456
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "uuid",
    "field1": "updated value",
    "field2": 456,
    "updatedAt": "2026-02-05T13:00:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid auth
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server error

---

#### 3.1.5 Delete [Resource]

**Endpoint:** `DELETE /resources/:id`

**Description:** [What this endpoint does]

**Request Headers:**
```
Authorization: Bearer <token>
```

**Path Parameters:**
- `id` (required): Resource UUID

**Response (204 No Content):**
[Empty body]

**Error Responses:**
- `401 Unauthorized` - Missing or invalid auth
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server error

---

### 3.2 [Another Resource] Endpoints

[Repeat the same structure for each resource]

---

## 4.0 WebSocket Events (if applicable)

### 4.1 Connection

**Endpoint:** `wss://api.example.com/v1/ws`

**Authentication:**
```
wss://api.example.com/v1/ws?token=<jwt-token>
```

### 4.2 Client → Server Events

#### 4.2.1 [Event Name]

**Event Type:** `event.name`

**Payload:**
```json
{
  "type": "event.name",
  "data": {
    "field1": "value"
  }
}
```

**Description:** [What this event does]

---

### 4.3 Server → Client Events

#### 4.3.1 [Event Name]

**Event Type:** `event.name`

**Payload:**
```json
{
  "type": "event.name",
  "data": {
    "field1": "value"
  },
  "timestamp": "2026-02-05T12:00:00Z"
}
```

**Description:** [When this event is sent]

---

## 5.0 Rate Limiting

### 5.1 Rate Limits

| Tier | Requests/Hour | Burst |
|------|--------------|-------|
| Free | 100 | 10 |
| Pro | 1,000 | 50 |
| Enterprise | Unlimited | 200 |

### 5.2 Rate Limit Headers

**Response Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1675612800
```

### 5.3 Rate Limit Exceeded Response

**Status:** `429 Too Many Requests`

**Body:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 3600 seconds.",
    "details": {
      "retryAfter": 3600
    }
  }
}
```

## 6.0 Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input data |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

## 7.0 Data Types

### 7.1 Common Types

```typescript
type UUID = string;           // UUID v4
type Timestamp = string;      // ISO-8601 format
type Email = string;          // RFC 5322 compliant
type URL = string;            // Valid URL

interface Resource {
  id: UUID;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

### 7.2 Custom Types

```typescript
// Define custom types specific to your API
type [TypeName] = {
  field1: string;
  field2: number;
};
```

## 8.0 Testing Endpoints

### 8.1 Health Check

**Endpoint:** `GET /health`

**Description:** Service health status

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-05T12:00:00Z"
}
```

### 8.2 Readiness Check

**Endpoint:** `GET /ready`

**Description:** Service readiness (includes dependencies)

**Response (200 OK):**
```json
{
  "ready": true,
  "dependencies": {
    "database": "connected",
    "cache": "connected"
  }
}
```

## 9.0 OpenAPI Specification

**OpenAPI Spec:** `openapi.yaml`

[Link to generated OpenAPI/Swagger documentation]

## 10.0 SDK Support

### 10.1 Official SDKs

| Language | Package | Repository |
|----------|---------|------------|
| TypeScript | `@example/sdk` | [GitHub URL] |
| Python | `example-sdk` | [GitHub URL] |

### 10.2 Example Usage

**TypeScript:**
```typescript
import { ExampleAPI } from '@example/sdk';

const api = new ExampleAPI({ token: 'your-token' });
const resource = await api.resources.get('resource-id');
```

**Python:**
```python
from example_sdk import ExampleAPI

api = ExampleAPI(token='your-token')
resource = api.resources.get('resource-id')
```

---

**API Design Complete:** [Date]
**Next Document:** DATABASE_SCHEMA.md
