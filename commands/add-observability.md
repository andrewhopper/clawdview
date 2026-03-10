---
description: Add observability stack (CloudWatch, X-Ray, RUM, error tracker)
version: 1.0.0
---

# Add Observability

Add comprehensive observability to any web project. Installs CloudWatch logging, X-Ray distributed tracing, CloudWatch RUM (Real User Monitoring), and our lightweight JavaScript error tracker.

## Arguments

```
$ARGUMENTS = [options] [path]

Options:
  --components=<list>   Comma-separated components (cloudwatch,xray,rum,tracker,all)
  --project=<name>      Project identifier for tracking
  --env=<environment>   Environment name (dev,staging,prod) - default: dev
  --dry-run             Show what would be installed without making changes

Path:
  Project directory (default: current directory)

Examples:
  /add-observability
  /add-observability ./projects/my-app
  /add-observability --components=tracker,rum
  /add-observability --project=my-app --env=prod
  /add-observability --dry-run
```

## Components Overview

| Component | Purpose | Cost | Complexity |
|-----------|---------|------|------------|
| CloudWatch | Server-side logs & metrics | ~$0.50/GB logs | Low |
| X-Ray | Distributed tracing | ~$0.50/1M traces | Medium |
| RUM | Real user performance monitoring | ~$1/100K sessions | Low |
| Error Tracker | Lightweight error capture | < $1/month | Low |

## Prerequisites

| Requirement | Check |
|-------------|-------|
| AWS credentials configured | `aws sts get-caller-identity` |
| Node.js project | `package.json` exists |
| CDK installed (for infra) | `cdk --version` |

---

## Instructions

### Step 0: Parse Arguments & Detect Project

```python
import os
from pathlib import Path

args = "$ARGUMENTS"
components = ["cloudwatch", "xray", "rum", "tracker"]  # all by default
project_name = None
environment = "dev"
dry_run = False
target_path = "."

# Parse flags
if "--components=" in args:
    components_str = args.split("--components=")[1].split()[0]
    if components_str == "all":
        components = ["cloudwatch", "xray", "rum", "tracker"]
    else:
        components = [c.strip() for c in components_str.split(",")]
    args = args.replace(f"--components={components_str}", "").strip()

if "--project=" in args:
    project_name = args.split("--project=")[1].split()[0]
    args = args.replace(f"--project={project_name}", "").strip()

if "--env=" in args:
    environment = args.split("--env=")[1].split()[0]
    args = args.replace(f"--env={environment}", "").strip()

if "--dry-run" in args:
    dry_run = True
    args = args.replace("--dry-run", "").strip()

# Remaining arg is path
remaining = args.strip()
if remaining and not remaining.startswith("--"):
    target_path = remaining

TARGET = Path(target_path).resolve()
```

### Step 1: Detect Project Type

```bash
cd "$TARGET"

# Detect framework
PROJECT_TYPE="unknown"

if [ -f "package.json" ]; then
    if grep -q '"next"' package.json; then
        PROJECT_TYPE="nextjs"
    elif grep -q '"vite"' package.json || grep -q '"@vitejs"' package.json; then
        PROJECT_TYPE="vite"
    elif grep -q '"react-scripts"' package.json; then
        PROJECT_TYPE="cra"
    elif grep -q '"express"' package.json; then
        PROJECT_TYPE="express"
    else
        PROJECT_TYPE="nodejs"
    fi
fi

# Get project name from package.json if not specified
if [ -z "$PROJECT_NAME" ] && [ -f "package.json" ]; then
    PROJECT_NAME=$(grep '"name"' package.json | head -1 | sed 's/.*"name".*"\([^"]*\)".*/\1/')
fi

echo "Project type: $PROJECT_TYPE"
echo "Project name: $PROJECT_NAME"
echo "Environment: $ENVIRONMENT"
```

---

## Component: CloudWatch

### CW-01: Install AWS SDK (if needed)

```bash
# Check if AWS SDK is already installed
if ! grep -q '"@aws-sdk/client-cloudwatch-logs"' package.json 2>/dev/null; then
    npm install @aws-sdk/client-cloudwatch-logs
fi
```

### CW-02: Create CloudWatch Logger Utility

Create `src/lib/cloudwatch.ts`:

```typescript
/**
 * CloudWatch Logger
 *
 * Structured logging with CloudWatch integration.
 * Falls back to console in development.
 */
import {
  CloudWatchLogsClient,
  CreateLogStreamCommand,
  PutLogEventsCommand,
} from '@aws-sdk/client-cloudwatch-logs';

const LOG_GROUP = process.env.CLOUDWATCH_LOG_GROUP || `/apps/${process.env.APP_NAME || 'app'}/${process.env.NODE_ENV || 'dev'}`;
const LOG_STREAM = `${new Date().toISOString().split('T')[0]}-${process.env.HOSTNAME || 'local'}`;

let client: CloudWatchLogsClient | null = null;
let sequenceToken: string | undefined;
let buffer: { timestamp: number; message: string }[] = [];
let flushTimeout: NodeJS.Timeout | null = null;

const FLUSH_INTERVAL = 5000;
const MAX_BUFFER = 100;

function getClient() {
  if (!client && process.env.AWS_REGION) {
    client = new CloudWatchLogsClient({ region: process.env.AWS_REGION });
  }
  return client;
}

async function ensureLogStream() {
  const cwClient = getClient();
  if (!cwClient) return;

  try {
    await cwClient.send(new CreateLogStreamCommand({
      logGroupName: LOG_GROUP,
      logStreamName: LOG_STREAM,
    }));
  } catch (err: any) {
    if (err.name !== 'ResourceAlreadyExistsException') {
      console.warn('[CloudWatch] Failed to create log stream:', err.message);
    }
  }
}

async function flush() {
  if (buffer.length === 0) return;

  const cwClient = getClient();
  if (!cwClient) {
    buffer = [];
    return;
  }

  const events = buffer.splice(0, MAX_BUFFER);

  try {
    const result = await cwClient.send(new PutLogEventsCommand({
      logGroupName: LOG_GROUP,
      logStreamName: LOG_STREAM,
      logEvents: events,
      sequenceToken,
    }));
    sequenceToken = result.nextSequenceToken;
  } catch (err: any) {
    console.warn('[CloudWatch] Failed to send logs:', err.message);
    buffer = events.concat(buffer);
  }
}

function scheduleFlush() {
  if (flushTimeout) return;
  flushTimeout = setTimeout(() => {
    flushTimeout = null;
    flush();
  }, FLUSH_INTERVAL);
}

interface LogContext {
  [key: string]: unknown;
}

export const logger = {
  _log(level: string, message: string, context?: LogContext) {
    const timestamp = Date.now();
    const logEntry = {
      level,
      message,
      timestamp: new Date(timestamp).toISOString(),
      ...context,
    };

    // Always log to console
    const consoleFn = level === 'error' ? console.error : level === 'warn' ? console.warn : console.log;
    consoleFn(JSON.stringify(logEntry));

    // Buffer for CloudWatch
    if (process.env.NODE_ENV === 'production') {
      buffer.push({
        timestamp,
        message: JSON.stringify(logEntry),
      });

      if (buffer.length >= MAX_BUFFER) {
        flush();
      } else {
        scheduleFlush();
      }
    }
  },

  info(message: string, context?: LogContext) {
    this._log('info', message, context);
  },

  warn(message: string, context?: LogContext) {
    this._log('warn', message, context);
  },

  error(message: string, context?: LogContext) {
    this._log('error', message, context);
  },

  debug(message: string, context?: LogContext) {
    if (process.env.LOG_LEVEL === 'debug') {
      this._log('debug', message, context);
    }
  },
};

// Initialize on import
ensureLogStream();

export default logger;
```

### CW-03: Add Environment Variables

Add to `.env.example`:

```bash
# CloudWatch Logging
CLOUDWATCH_LOG_GROUP=/apps/my-app/dev
AWS_REGION=us-east-1
LOG_LEVEL=info
```

---

## Component: X-Ray

### XRAY-01: Install X-Ray SDK

```bash
# For Node.js/Express
npm install aws-xray-sdk

# For Lambda (already included in runtime)
```

### XRAY-02: Create X-Ray Middleware

Create `src/lib/xray.ts`:

```typescript
/**
 * X-Ray Tracing Middleware
 *
 * Wraps HTTP requests with X-Ray tracing for distributed tracing.
 */
import AWSXRay from 'aws-xray-sdk';
import { Express, Request, Response, NextFunction } from 'express';

const APP_NAME = process.env.APP_NAME || 'app';

/**
 * Configure X-Ray for Express
 */
export function configureXRay(app: Express) {
  // Only enable in production
  if (process.env.NODE_ENV !== 'production') {
    console.log('[X-Ray] Disabled in development');
    return;
  }

  // Set daemon address (default: 127.0.0.1:2000)
  if (process.env.AWS_XRAY_DAEMON_ADDRESS) {
    AWSXRay.setDaemonAddress(process.env.AWS_XRAY_DAEMON_ADDRESS);
  }

  // Open segment at start of request
  app.use(AWSXRay.express.openSegment(APP_NAME));

  // Add custom annotations
  app.use((req: Request, res: Response, next: NextFunction) => {
    const segment = AWSXRay.getSegment();
    if (segment) {
      // Add standard annotations
      segment.addAnnotation('environment', process.env.NODE_ENV || 'dev');
      segment.addAnnotation('request_path', req.path);

      // Add user ID if authenticated
      if ((req as any).user?.id) {
        segment.addAnnotation('user_id', (req as any).user.id);
      }

      // Add metadata
      segment.addMetadata('request', {
        method: req.method,
        url: req.originalUrl,
        query: req.query,
        headers: {
          'user-agent': req.headers['user-agent'],
          'content-type': req.headers['content-type'],
        },
      });
    }
    next();
  });

  console.log('[X-Ray] Tracing enabled');
}

/**
 * Close segment at end of request (use at end of middleware chain)
 */
export function closeXRaySegment() {
  return AWSXRay.express.closeSegment();
}

/**
 * Capture AWS SDK calls
 */
export function captureAWS<T>(client: T): T {
  if (process.env.NODE_ENV !== 'production') return client;
  return AWSXRay.captureAWSClient(client as any);
}

/**
 * Capture HTTP/HTTPS calls
 */
export function captureHTTP() {
  if (process.env.NODE_ENV !== 'production') return;
  AWSXRay.captureHTTPsGlobal(require('http'));
  AWSXRay.captureHTTPsGlobal(require('https'));
}

/**
 * Create a subsegment for custom operations
 */
export async function traceOperation<T>(
  name: string,
  operation: () => Promise<T>,
  annotations?: Record<string, string | number | boolean>,
): Promise<T> {
  if (process.env.NODE_ENV !== 'production') {
    return operation();
  }

  const segment = AWSXRay.getSegment();
  if (!segment) return operation();

  const subsegment = segment.addNewSubsegment(name);

  if (annotations) {
    Object.entries(annotations).forEach(([key, value]) => {
      subsegment.addAnnotation(key, value);
    });
  }

  try {
    const result = await operation();
    subsegment.close();
    return result;
  } catch (error) {
    subsegment.addError(error as Error);
    subsegment.close();
    throw error;
  }
}

export default {
  configureXRay,
  closeXRaySegment,
  captureAWS,
  captureHTTP,
  traceOperation,
};
```

### XRAY-03: Express Integration Example

```typescript
import express from 'express';
import { configureXRay, closeXRaySegment, captureHTTP } from './lib/xray';

const app = express();

// Capture outbound HTTP calls
captureHTTP();

// Start X-Ray tracing (first middleware)
configureXRay(app);

// ... your routes ...

// Close X-Ray segment (last middleware before error handler)
app.use(closeXRaySegment());
```

### XRAY-04: Lambda Integration

```typescript
import AWSXRay from 'aws-xray-sdk';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';

// Capture DynamoDB calls
const ddb = AWSXRay.captureAWSv3Client(new DynamoDBClient({}));
```

### XRAY-05: Add Environment Variables

```bash
# X-Ray Tracing
AWS_XRAY_DAEMON_ADDRESS=127.0.0.1:2000
AWS_XRAY_CONTEXT_MISSING=LOG_ERROR
```

---

## Component: CloudWatch RUM

### RUM-01: Create RUM App Monitor (CDK)

Add to `infra/lib/observability-stack.ts`:

```typescript
import * as cdk from 'aws-cdk-lib';
import * as rum from 'aws-cdk-lib/aws-rum';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import { Construct } from 'constructs';

export interface RUMProps {
  appName: string;
  domain: string;
  environment: string;
}

export class CloudWatchRUM extends Construct {
  public readonly appMonitorId: string;
  public readonly identityPoolId: string;
  public readonly guestRoleArn: string;

  constructor(scope: Construct, id: string, props: RUMProps) {
    super(scope, id);

    // Create identity pool for unauthenticated RUM access
    const identityPool = new cognito.CfnIdentityPool(this, 'RUMIdentityPool', {
      identityPoolName: `${props.appName}-rum-${props.environment}`,
      allowUnauthenticatedIdentities: true,
    });

    // Create guest role
    const guestRole = new cdk.aws_iam.Role(this, 'RUMGuestRole', {
      assumedBy: new cdk.aws_iam.FederatedPrincipal(
        'cognito-identity.amazonaws.com',
        {
          StringEquals: {
            'cognito-identity.amazonaws.com:aud': identityPool.ref,
          },
          'ForAnyValue:StringLike': {
            'cognito-identity.amazonaws.com:amr': 'unauthenticated',
          },
        },
        'sts:AssumeRoleWithWebIdentity',
      ),
    });

    guestRole.addToPolicy(
      new cdk.aws_iam.PolicyStatement({
        actions: ['rum:PutRumEvents'],
        resources: [`arn:aws:rum:${cdk.Aws.REGION}:${cdk.Aws.ACCOUNT_ID}:appmonitor/${props.appName}-${props.environment}`],
      }),
    );

    // Attach role to identity pool
    new cognito.CfnIdentityPoolRoleAttachment(this, 'RUMRoleAttachment', {
      identityPoolId: identityPool.ref,
      roles: {
        unauthenticated: guestRole.roleArn,
      },
    });

    // Create RUM App Monitor
    const appMonitor = new rum.CfnAppMonitor(this, 'AppMonitor', {
      name: `${props.appName}-${props.environment}`,
      domain: props.domain,
      cwLogEnabled: true,
      appMonitorConfiguration: {
        allowCookies: true,
        enableXRay: true,
        sessionSampleRate: 1.0,  // 100% sampling, adjust for production
        telemetries: ['errors', 'performance', 'http'],
        identityPoolId: identityPool.ref,
        guestRoleArn: guestRole.roleArn,
      },
    });

    this.appMonitorId = appMonitor.attrId;
    this.identityPoolId = identityPool.ref;
    this.guestRoleArn = guestRole.roleArn;

    // Output values
    new cdk.CfnOutput(this, 'RUMAppMonitorId', { value: this.appMonitorId });
    new cdk.CfnOutput(this, 'RUMIdentityPoolId', { value: this.identityPoolId });
  }
}
```

### RUM-02: Create RUM Client Utility

Create `src/lib/rum.ts`:

```typescript
/**
 * CloudWatch RUM Client
 *
 * Real User Monitoring for frontend performance and errors.
 * Automatically tracks page views, web vitals, and JS errors.
 */

interface RUMConfig {
  appId: string;
  identityPoolId: string;
  region: string;
  sessionSampleRate?: number;
  guestRoleArn?: string;
  endpoint?: string;
}

let rumClient: any = null;

/**
 * Initialize CloudWatch RUM
 */
export async function initRUM(config: RUMConfig): Promise<void> {
  // Only run in browser
  if (typeof window === 'undefined') return;

  // Only enable in production
  if (process.env.NODE_ENV !== 'production') {
    console.log('[RUM] Disabled in development');
    return;
  }

  try {
    // Dynamically import the RUM client
    const { AwsRum, AwsRumConfig } = await import('aws-rum-web');

    const rumConfig: AwsRumConfig = {
      sessionSampleRate: config.sessionSampleRate ?? 1.0,
      guestRoleArn: config.guestRoleArn,
      identityPoolId: config.identityPoolId,
      endpoint: config.endpoint,
      telemetries: ['errors', 'performance', 'http'],
      allowCookies: true,
      enableXRay: true,
    };

    rumClient = new AwsRum(
      config.appId,
      '1.0.0',
      config.region,
      rumConfig,
    );

    console.log('[RUM] Initialized');
  } catch (err) {
    console.warn('[RUM] Failed to initialize:', err);
  }
}

/**
 * Record a custom event
 */
export function recordEvent(eventType: string, eventData: Record<string, unknown>): void {
  if (!rumClient) return;
  rumClient.recordEvent(eventType, eventData);
}

/**
 * Record an error
 */
export function recordError(error: Error): void {
  if (!rumClient) return;
  rumClient.recordError(error);
}

/**
 * Set user ID for authenticated users
 */
export function setUser(userId: string): void {
  if (!rumClient) return;
  rumClient.addSessionAttributes({ userId });
}

/**
 * Add custom page attributes
 */
export function setPageAttributes(attributes: Record<string, string>): void {
  if (!rumClient) return;
  rumClient.addSessionAttributes(attributes);
}

export default {
  initRUM,
  recordEvent,
  recordError,
  setUser,
  setPageAttributes,
};
```

### RUM-03: Install RUM Web Package

```bash
npm install aws-rum-web
```

### RUM-04: Frontend Integration (React/Next.js)

Create `src/components/RUMProvider.tsx`:

```tsx
'use client';

import { useEffect } from 'react';
import { initRUM } from '@/lib/rum';

const RUM_CONFIG = {
  appId: process.env.NEXT_PUBLIC_RUM_APP_ID!,
  identityPoolId: process.env.NEXT_PUBLIC_RUM_IDENTITY_POOL_ID!,
  region: process.env.NEXT_PUBLIC_AWS_REGION || 'us-east-1',
  guestRoleArn: process.env.NEXT_PUBLIC_RUM_GUEST_ROLE_ARN,
};

export function RUMProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    if (RUM_CONFIG.appId && RUM_CONFIG.identityPoolId) {
      initRUM(RUM_CONFIG);
    }
  }, []);

  return <>{children}</>;
}
```

### RUM-05: Add Environment Variables

```bash
# CloudWatch RUM
NEXT_PUBLIC_RUM_APP_ID=your-app-monitor-id
NEXT_PUBLIC_RUM_IDENTITY_POOL_ID=us-east-1:xxxx-xxxx-xxxx
NEXT_PUBLIC_RUM_GUEST_ROLE_ARN=arn:aws:iam::123456789:role/RUMGuestRole
NEXT_PUBLIC_AWS_REGION=us-east-1
```

---

## Component: Error Tracker

### ET-01: Add Error Tracker Script

Copy or install the lightweight error tracker:

**Option A: Script tag (simplest)**

```html
<script
  src="https://cdn.b.lfg.new/tracker.min.js"
  data-project="your-project-id"
  data-endpoint="https://e.b.lfg.new/errors"
></script>
```

**Option B: Copy from shared**

```bash
cp /home/user/protoflow/shared/error-tracker/tracker.min.js public/
```

Then add to your HTML:

```html
<script src="/tracker.min.js" data-project="your-project-id" data-endpoint="https://e.b.lfg.new/errors"></script>
```

**Option C: Programmatic initialization**

```typescript
import { ErrorTracker } from '@/lib/error-tracker';

ErrorTracker.init({
  projectId: 'your-project-id',
  endpoint: 'https://e.b.lfg.new/errors',
  environment: process.env.NODE_ENV,
  release: process.env.NEXT_PUBLIC_VERSION,
});
```

### ET-02: Create Error Tracker Wrapper (TypeScript)

Create `src/lib/error-tracker.ts`:

```typescript
/**
 * Error Tracker Client
 *
 * Lightweight frontend error tracking.
 * @see shared/error-tracker/README.md
 */

interface ErrorTrackerConfig {
  projectId: string;
  endpoint: string;
  environment?: string;
  release?: string;
  userId?: string;
}

interface ErrorContext {
  type?: string;
  level?: 'error' | 'warning' | 'info';
  tags?: Record<string, string>;
  extra?: Record<string, unknown>;
}

declare global {
  interface Window {
    ErrorTracker?: {
      init: (config: ErrorTrackerConfig) => void;
      capture: (error: Error | string, context?: ErrorContext) => void;
      setUser: (userId: string) => void;
      setTags: (tags: Record<string, string>) => void;
      addBreadcrumb: (crumb: {
        type?: string;
        category?: string;
        message: string;
        data?: Record<string, unknown>;
      }) => void;
    };
  }
}

/**
 * Initialize error tracking
 */
export function initErrorTracker(config: ErrorTrackerConfig): void {
  if (typeof window === 'undefined') return;

  // Load script if not already loaded
  if (!window.ErrorTracker) {
    const script = document.createElement('script');
    script.src = '/tracker.min.js';
    script.dataset.project = config.projectId;
    script.dataset.endpoint = config.endpoint;
    if (config.environment) script.dataset.environment = config.environment;
    if (config.release) script.dataset.release = config.release;
    document.head.appendChild(script);
  } else {
    window.ErrorTracker.init(config);
  }
}

/**
 * Capture an error manually
 */
export function captureError(error: Error | string, context?: ErrorContext): void {
  window.ErrorTracker?.capture(error, context);
}

/**
 * Set the current user
 */
export function setUser(userId: string): void {
  window.ErrorTracker?.setUser(userId);
}

/**
 * Add breadcrumb for debugging
 */
export function addBreadcrumb(
  message: string,
  data?: Record<string, unknown>,
): void {
  window.ErrorTracker?.addBreadcrumb({
    category: 'custom',
    message,
    data,
  });
}

export const ErrorTracker = {
  init: initErrorTracker,
  capture: captureError,
  setUser,
  addBreadcrumb,
};

export default ErrorTracker;
```

### ET-03: React Error Boundary Integration

Create `src/components/ErrorBoundary.tsx`:

```tsx
'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { captureError, addBreadcrumb } from '@/lib/error-tracker';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    addBreadcrumb('React Error Boundary', {
      componentStack: errorInfo.componentStack,
    });

    captureError(error, {
      type: 'react_error_boundary',
      extra: {
        componentStack: errorInfo.componentStack,
      },
    });
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### ET-04: Add Environment Variables

```bash
# Error Tracker
NEXT_PUBLIC_ERROR_TRACKER_PROJECT=your-project-id
NEXT_PUBLIC_ERROR_TRACKER_ENDPOINT=https://e.b.lfg.new/errors
```

---

## Full Integration Example

### Next.js App Router

Create `src/app/providers.tsx`:

```tsx
'use client';

import { useEffect } from 'react';
import { RUMProvider } from '@/components/RUMProvider';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { initErrorTracker } from '@/lib/error-tracker';

export function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize error tracker
    initErrorTracker({
      projectId: process.env.NEXT_PUBLIC_ERROR_TRACKER_PROJECT!,
      endpoint: process.env.NEXT_PUBLIC_ERROR_TRACKER_ENDPOINT!,
      environment: process.env.NODE_ENV,
    });
  }, []);

  return (
    <ErrorBoundary>
      <RUMProvider>
        {children}
      </RUMProvider>
    </ErrorBoundary>
  );
}
```

Update `src/app/layout.tsx`:

```tsx
import { Providers } from './providers';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

---

## Verification Checklist

After installation, verify each component:

### CloudWatch
- [ ] Log group created: `/apps/{project}/{env}`
- [ ] Logs appearing in CloudWatch console
- [ ] Structured JSON format

### X-Ray
- [ ] Traces appearing in X-Ray console
- [ ] Service map shows application
- [ ] Subsegments for DB/HTTP calls

### RUM
- [ ] App Monitor active in console
- [ ] Page views being recorded
- [ ] Web Vitals (LCP, FID, CLS) tracked
- [ ] JS errors captured

### Error Tracker
- [ ] Endpoint responding: `curl https://e.b.lfg.new/errors`
- [ ] Test error captured: `throw new Error('Test')`
- [ ] Breadcrumbs recording

---

## Environment Variables Summary

Add all to `.env.example`:

```bash
# =============================
# Observability Configuration
# =============================

# CloudWatch Logging
CLOUDWATCH_LOG_GROUP=/apps/my-app/dev
AWS_REGION=us-east-1
LOG_LEVEL=info

# X-Ray Tracing
AWS_XRAY_DAEMON_ADDRESS=127.0.0.1:2000
AWS_XRAY_CONTEXT_MISSING=LOG_ERROR

# CloudWatch RUM (client-side, use NEXT_PUBLIC_ prefix)
NEXT_PUBLIC_RUM_APP_ID=
NEXT_PUBLIC_RUM_IDENTITY_POOL_ID=
NEXT_PUBLIC_RUM_GUEST_ROLE_ARN=
NEXT_PUBLIC_AWS_REGION=us-east-1

# Error Tracker (client-side)
NEXT_PUBLIC_ERROR_TRACKER_PROJECT=my-app
NEXT_PUBLIC_ERROR_TRACKER_ENDPOINT=https://e.b.lfg.new/errors
```

---

## Related Commands

- `/brownfield-audit` - Audit existing codebase for issues
- `/website-qa-checklist` - Comprehensive QA for web apps
- `/track-errors` - Track workflow errors in conversation

## Related Resources

- Error Tracker: `shared/error-tracker/`
- Production Error Tracker: `projects/shared/tool-error-tracker-js-et001/`
- X-Ray Tests: `hmode/shared/standards/testing/e2e/observability/xray.spec.ts`
- Design System: `hmode/shared/design-system/`
