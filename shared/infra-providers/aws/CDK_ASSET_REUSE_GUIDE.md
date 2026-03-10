# AWS CDK Asset Decomposition & Reuse Guide

<!-- File UUID: 9c4b7f2e-8a1d-4e3f-b9c5-7d8e9f0a1b2c -->

## Overview

This guide documents patterns for decomposing CDK infrastructure into reusable constructs, optimizing asset bundling, and preventing duplicate assets across stacks.

---

## Problem Summary

| # | Problem | Impact | Solution |
|---|---------|--------|----------|
| 1 | Duplicate assets across stacks | S3 bloat, slow synth, wasted space | Shared construct library |
| 2 | Monolithic stack files (1000+ lines) | Hard to maintain, slow testing | Decompose into L3 constructs |
| 3 | Lambda code bundled separately per stack | Duplicate bundles, slow builds | Asset deduplication |
| 4 | Docker images rebuilt unnecessarily | Slow deployments, cache misses | ECR asset sharing |
| 5 | Custom resources copy-pasted | Drift, inconsistency | Extract to shared constructs |
| 6 | No construct versioning | Breaking changes, hard rollbacks | Semantic versioning pattern |

---

## Problem 1: Duplicate Assets Across Stacks

### Symptom
Multiple stacks deploying identical Lambda code or Docker images:
- S3 bucket contains 20+ copies of same bundle
- `cdk synth` takes 5+ minutes
- Asset hashes differ despite identical code

### Root Cause
Each stack creates its own `lambda.Function` with `code: lambda.Code.fromAsset()`, resulting in separate asset bundles even for identical source.

### Solution: Shared Asset Constructs

**Anti-Pattern:**
```typescript
// ❌ BAD: Each stack bundles its own copy
// api-stack.ts
const apiHandler = new lambda.Function(this, 'ApiHandler', {
  code: lambda.Code.fromAsset('src/handlers/api'),
  handler: 'index.handler',
  runtime: lambda.Runtime.NODEJS_20_X,
});

// auth-stack.ts
const authHandler = new lambda.Function(this, 'AuthHandler', {
  code: lambda.Code.fromAsset('src/handlers/api'),  // Same path!
  handler: 'index.handler',
  runtime: lambda.Runtime.NODEJS_20_X,
});
```

**Solution: Extract Asset to Shared Construct**

```typescript
// lib/constructs/shared-assets.ts
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export class SharedAssets extends Construct {
  public readonly apiHandlerCode: lambda.Code;
  public readonly utilsLayerCode: lambda.Code;

  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Bundle ONCE, reuse everywhere
    this.apiHandlerCode = lambda.Code.fromAsset('src/handlers/api', {
      bundling: {
        image: lambda.Runtime.NODEJS_20_X.bundlingImage,
        command: [
          'bash', '-c',
          'npm ci && npm run build && cp -r dist/* /asset-output/',
        ],
      },
    });

    this.utilsLayerCode = lambda.Code.fromAsset('src/layers/utils', {
      bundling: {
        image: lambda.Runtime.NODEJS_20_X.bundlingImage,
        command: [
          'bash', '-c',
          'mkdir -p /asset-output/nodejs && npm ci --production && cp -r node_modules /asset-output/nodejs/',
        ],
      },
    });
  }
}

// bin/app.ts
const sharedAssets = new SharedAssets(app, 'SharedAssets');

// lib/stacks/api-stack.ts
export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: ApiStackProps) {
    super(scope, id, props);

    // ✅ GOOD: Reuse pre-bundled asset
    const apiHandler = new lambda.Function(this, 'ApiHandler', {
      code: props.sharedAssets.apiHandlerCode,  // No re-bundling!
      handler: 'index.handler',
      runtime: lambda.Runtime.NODEJS_20_X,
    });
  }
}

// lib/stacks/auth-stack.ts
export class AuthStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: AuthStackProps) {
    super(scope, id, props);

    // ✅ GOOD: Same asset, no duplication
    const authHandler = new lambda.Function(this, 'AuthHandler', {
      code: props.sharedAssets.apiHandlerCode,  // Reuses asset hash!
      handler: 'index.handler',
      runtime: lambda.Runtime.NODEJS_20_X,
    });
  }
}
```

### Asset Deduplication Pattern

CDK uses content hashing to deduplicate assets. Ensure identical inputs:

```typescript
// ✅ GOOD: Deterministic bundling for deduplication
const code = lambda.Code.fromAsset('src/', {
  exclude: [
    'node_modules',
    '*.test.ts',
    'coverage',
    '.git',
  ],
  bundling: {
    image: lambda.Runtime.NODEJS_20_X.bundlingImage,
    environment: {
      NODE_ENV: 'production',  // Consistent env vars
    },
    command: [
      'bash', '-c', [
        'set -euo pipefail',  // Fail on errors
        'npm ci',             // Use package-lock for deterministic install
        'npm run build',
        'cp -r dist/* /asset-output/',
      ].join(' && '),
    ],
  },
});
```

**Key Principles for Deduplication:**
1. **Consistent paths**: Always use same source path for identical code
2. **Deterministic bundling**: Use `npm ci` (not `npm install`), lock files
3. **Exclude variability**: Exclude timestamps, logs, temp files
4. **Shared construct**: Create asset once, pass to multiple stacks
5. **Asset publishing**: CDK auto-deduplicates by content hash

---

## Problem 2: Monolithic Stack Files

### Symptom
Single stack file with 1000+ lines:
- Hard to navigate and maintain
- Slow unit tests
- Difficult to reuse patterns
- Merge conflicts

### Root Cause
All resources defined inline in stack constructor instead of decomposed into logical constructs.

### Solution: L3 Construct Decomposition

**Hierarchy:**
```
L1 (CloudFormation)  → CfnBucket
L2 (AWS CDK)         → s3.Bucket (adds methods, defaults)
L3 (Custom/Domain)   → StaticWebsiteBucket (opinionated pattern)
```

**Anti-Pattern:**
```typescript
// ❌ BAD: 800-line monolithic stack
export class MonolithStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    // 100 lines of S3 + CloudFront setup
    const bucket = new s3.Bucket(this, 'Bucket', { ... });
    const distribution = new cloudfront.Distribution(this, 'CDN', { ... });
    const originAccessIdentity = new cloudfront.OriginAccessIdentity(this, 'OAI', { ... });
    bucket.grantRead(originAccessIdentity);
    // ... 50 more lines

    // 100 lines of API Gateway + Lambda setup
    const api = new apigateway.RestApi(this, 'Api', { ... });
    const handler = new lambda.Function(this, 'Handler', { ... });
    const integration = new apigateway.LambdaIntegration(handler);
    // ... 50 more lines

    // 100 lines of database setup
    // ... and so on
  }
}
```

**Solution: Extract L3 Constructs**

```typescript
// lib/constructs/static-website.ts
export interface StaticWebsiteProps {
  domainName?: string;
  hostedZone?: route53.IHostedZone;
  certificateArn?: string;
  indexDocument?: string;
  errorDocument?: string;
}

export class StaticWebsite extends Construct {
  public readonly bucket: s3.Bucket;
  public readonly distribution: cloudfront.Distribution;
  public readonly url: string;

  constructor(scope: Construct, id: string, props: StaticWebsiteProps) {
    super(scope, id);

    // S3 bucket with website hosting
    this.bucket = new s3.Bucket(this, 'Bucket', {
      websiteIndexDocument: props.indexDocument ?? 'index.html',
      websiteErrorDocument: props.errorDocument ?? 'error.html',
      publicReadAccess: false,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    // Origin access identity for CloudFront
    const oai = new cloudfront.OriginAccessIdentity(this, 'OAI');
    this.bucket.grantRead(oai);

    // CloudFront distribution
    this.distribution = new cloudfront.Distribution(this, 'Distribution', {
      defaultBehavior: {
        origin: new origins.S3Origin(this.bucket, { originAccessIdentity: oai }),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
      },
      domainNames: props.domainName ? [props.domainName] : undefined,
      certificate: props.certificateArn
        ? acm.Certificate.fromCertificateArn(this, 'Cert', props.certificateArn)
        : undefined,
      defaultRootObject: props.indexDocument ?? 'index.html',
    });

    // DNS record if hosted zone provided
    if (props.hostedZone && props.domainName) {
      new route53.ARecord(this, 'AliasRecord', {
        zone: props.hostedZone,
        recordName: props.domainName,
        target: route53.RecordTarget.fromAlias(
          new targets.CloudFrontTarget(this.distribution)
        ),
      });
    }

    this.url = props.domainName ?? this.distribution.distributionDomainName;

    new cdk.CfnOutput(this, 'WebsiteUrl', {
      value: `https://${this.url}`,
      description: 'Website URL',
    });
  }
}

// lib/stacks/frontend-stack.ts - Now clean and focused
export class FrontendStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: FrontendStackProps) {
    super(scope, id, props);

    // ✅ GOOD: Simple, declarative, reusable
    const website = new StaticWebsite(this, 'Website', {
      domainName: props.config.domain.rootDomain,
      hostedZone: props.hostedZone,
      certificateArn: props.config.certificateArn,
    });

    // Deployment construct
    new s3deploy.BucketDeployment(this, 'Deploy', {
      sources: [s3deploy.Source.asset('./dist')],
      destinationBucket: website.bucket,
      distribution: website.distribution,
    });
  }
}
```

### Construct Organization Pattern

```
lib/
├── constructs/           # Reusable L3 constructs
│   ├── base-stack.ts     # Base with common config
│   ├── static-website.ts # S3 + CloudFront pattern
│   ├── api-service.ts    # API Gateway + Lambda pattern
│   ├── database.ts       # RDS/DynamoDB pattern
│   └── monitoring.ts     # CloudWatch + alarms pattern
├── stacks/               # Thin orchestration layers
│   ├── frontend-stack.ts # Composes StaticWebsite
│   ├── backend-stack.ts  # Composes ApiService + Database
│   └── cicd-stack.ts     # Composes CodePipeline
└── shared/               # Cross-project constructs
    └── auth-construct.ts # Shared Cognito pattern
```

---

## Problem 3: Lambda Code Bundled Separately Per Stack

### Symptom
- Same Lambda code bundled 5+ times
- Build takes 10+ minutes
- Identical bundles with different asset hashes

### Root Cause
Each stack invokes bundling independently, even for identical source.

### Solution: Centralized Bundling with Layers

```typescript
// lib/constructs/lambda-assets.ts
export class LambdaAssets extends Construct {
  public readonly commonLayer: lambda.LayerVersion;
  public readonly apiCode: lambda.Code;

  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Bundle dependencies as layer (ONCE)
    this.commonLayer = new lambda.LayerVersion(this, 'CommonLayer', {
      code: lambda.Code.fromAsset('src/layers/common', {
        bundling: {
          image: lambda.Runtime.NODEJS_20_X.bundlingImage,
          command: [
            'bash', '-c', [
              'mkdir -p /asset-output/nodejs',
              'cp package.json package-lock.json /asset-output/nodejs/',
              'cd /asset-output/nodejs',
              'npm ci --production',
            ].join(' && '),
          ],
        },
      }),
      compatibleRuntimes: [lambda.Runtime.NODEJS_20_X],
      description: 'Common dependencies layer',
    });

    // Bundle application code (ONCE)
    this.apiCode = lambda.Code.fromAsset('src/api', {
      bundling: {
        image: lambda.Runtime.NODEJS_20_X.bundlingImage,
        command: [
          'bash', '-c', [
            'npm ci',
            'npm run build',
            'cp -r dist/* /asset-output/',
          ].join(' && '),
        ],
      },
    });
  }
}

// In app.ts
const lambdaAssets = new LambdaAssets(app, 'LambdaAssets');

// In multiple stacks - no re-bundling
const createHandler = (scope: Construct, id: string, handler: string) =>
  new lambda.Function(scope, id, {
    code: lambdaAssets.apiCode,      // Shared asset
    layers: [lambdaAssets.commonLayer], // Shared layer
    handler,
    runtime: lambda.Runtime.NODEJS_20_X,
  });
```

### Asset Bundling Best Practices

```typescript
// ✅ GOOD: Optimized bundling with esbuild
const code = lambda.Code.fromAsset('src/', {
  bundling: {
    image: lambda.Runtime.NODEJS_20_X.bundlingImage,
    command: [
      'bash', '-c', [
        // Install esbuild
        'npm install -g esbuild',
        // Bundle with tree-shaking
        'esbuild src/index.ts',
        '  --bundle',
        '  --platform=node',
        '  --target=node20',
        '  --external:aws-sdk',  // AWS SDK included in runtime
        '  --external:@aws-sdk/*',
        '  --outfile=/asset-output/index.js',
        '  --minify',
        '  --sourcemap',
      ].join(' '),
    ],
  },
});
```

**Bundling Optimization Checklist:**
- [ ] External AWS SDK (included in Lambda runtime)
- [ ] Use esbuild/swc for fast bundling
- [ ] Enable minification and tree-shaking
- [ ] Separate dependencies into layers
- [ ] Cache node_modules in CI/CD
- [ ] Use Docker layer caching

---

## Problem 4: Docker Images Rebuilt Unnecessarily

### Symptom
- `cdk deploy` rebuilds same Docker image 5+ times
- 20-minute synth times
- ECR contains 50+ duplicate images

### Root Cause
Each stack that uses `DockerImageAsset` triggers separate build, even for identical Dockerfiles.

### Solution: Shared Docker Image Assets

```typescript
// lib/constructs/docker-assets.ts
import * as ecr_assets from 'aws-cdk-lib/aws-ecr-assets';

export class DockerAssets extends Construct {
  public readonly apiImage: ecr_assets.DockerImageAsset;
  public readonly workerImage: ecr_assets.DockerImageAsset;

  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Build ONCE, reuse across stacks
    this.apiImage = new ecr_assets.DockerImageAsset(this, 'ApiImage', {
      directory: 'src/api',
      file: 'Dockerfile',
      buildArgs: {
        NODE_ENV: 'production',
      },
      exclude: [
        'node_modules',
        '*.test.ts',
        'coverage',
      ],
      // Platform for cross-compilation
      platform: ecr_assets.Platform.LINUX_AMD64,
    });

    this.workerImage = new ecr_assets.DockerImageAsset(this, 'WorkerImage', {
      directory: 'src/worker',
      file: 'Dockerfile',
    });
  }
}

// In app.ts
const dockerAssets = new DockerAssets(app, 'DockerAssets');

// In ECS stack
const taskDef = new ecs.FargateTaskDefinition(this, 'TaskDef', {
  memoryLimitMiB: 512,
  cpu: 256,
});

taskDef.addContainer('Api', {
  image: ecs.ContainerImage.fromDockerImageAsset(dockerAssets.apiImage),
  logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'api' }),
});

// In Lambda container stack
const handler = new lambda.DockerImageFunction(this, 'Handler', {
  code: lambda.DockerImageCode.fromEcr(
    ecr.Repository.fromRepositoryArn(
      this,
      'Repo',
      dockerAssets.apiImage.repository.repositoryArn
    ),
    { tag: dockerAssets.apiImage.imageTag }
  ),
});
```

### Multi-Stage Dockerfile for CDK

```dockerfile
# Optimized for CDK asset caching
FROM node:20-alpine AS builder
WORKDIR /app

# Layer 1: Dependencies (cached unless package.json changes)
COPY package.json package-lock.json ./
RUN npm ci --production

# Layer 2: Source code (cached unless code changes)
COPY src ./src
RUN npm run build

# Layer 3: Runtime (minimal image)
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

# Non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs

CMD ["node", "dist/index.js"]
```

---

## Problem 5: Custom Resources Copy-Pasted

### Symptom
- Same custom resource Lambda duplicated across 10+ stacks
- Inconsistent implementations
- Hard to update (must touch all stacks)

### Root Cause
Custom resources copied instead of extracted to shared construct.

### Solution: Shared Custom Resource Construct

```typescript
// lib/constructs/custom-resources/cloudfront-invalidation.ts
export interface CloudFrontInvalidationProps {
  distributionId: string;
  paths: string[];
}

export class CloudFrontInvalidation extends Construct {
  constructor(scope: Construct, id: string, props: CloudFrontInvalidationProps) {
    super(scope, id);

    // Shared Lambda for custom resource (singleton pattern)
    const handler = this.getOrCreateHandler(scope);

    // Custom resource
    new cdk.CustomResource(this, 'Resource', {
      serviceToken: handler.functionArn,
      properties: {
        DistributionId: props.distributionId,
        Paths: props.paths,
        Timestamp: Date.now(), // Force update on every deploy
      },
    });
  }

  private getOrCreateHandler(scope: Construct): lambda.Function {
    const stack = cdk.Stack.of(scope);
    const id = 'CloudFrontInvalidationHandler';

    // Singleton: create once per stack, reuse for all custom resources
    const existing = stack.node.tryFindChild(id);
    if (existing) {
      return existing as lambda.Function;
    }

    return new lambda.Function(stack, id, {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
import boto3
import cfnresponse

cf = boto3.client('cloudfront')

def handler(event, context):
    try:
        if event['RequestType'] in ['Create', 'Update']:
            dist_id = event['ResourceProperties']['DistributionId']
            paths = event['ResourceProperties']['Paths']

            cf.create_invalidation(
                DistributionId=dist_id,
                InvalidationBatch={
                    'Paths': {'Quantity': len(paths), 'Items': paths},
                    'CallerReference': str(event['ResourceProperties']['Timestamp'])
                }
            )

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
      `),
      timeout: cdk.Duration.minutes(5),
      initialPolicy: [
        new iam.PolicyStatement({
          actions: ['cloudfront:CreateInvalidation'],
          resources: ['*'],
        }),
      ],
    });
  }
}

// Usage in any stack
new CloudFrontInvalidation(this, 'Invalidation', {
  distributionId: distribution.distributionId,
  paths: ['/*'],
});
```

---

## Problem 6: No Construct Versioning

### Symptom
- Breaking changes in shared constructs break all stacks
- No rollback capability
- Hard to coordinate updates across teams

### Root Cause
Shared constructs treated as mutable instead of versioned.

### Solution: Semantic Versioning Pattern

```typescript
// lib/constructs/v2/static-website.ts
/**
 * StaticWebsite construct v2.0.0
 *
 * Breaking changes from v1:
 * - Requires certificateArn (no longer optional)
 * - Removed `enableCloudFrontLogs` (always enabled)
 *
 * @version 2.0.0
 * @since 2025-01-15
 */
export class StaticWebsiteV2 extends Construct {
  // ... implementation
}

// lib/constructs/v1/static-website.ts (deprecated but maintained)
/**
 * @deprecated Use StaticWebsiteV2 instead
 * @version 1.5.0
 */
export class StaticWebsite extends Construct {
  // ... old implementation (frozen)
}
```

**Versioning Strategy:**
```
lib/constructs/
├── v1/
│   ├── static-website.ts    # Frozen (1.5.0)
│   └── api-service.ts       # Frozen (1.3.0)
├── v2/
│   ├── static-website.ts    # Active (2.1.0)
│   └── api-service.ts       # Active (2.0.0)
└── index.ts                 # Exports both versions
```

**Migration Path:**
```typescript
// Step 1: Old stacks continue using v1
import { StaticWebsite } from '../constructs/v1/static-website';

// Step 2: New stacks adopt v2
import { StaticWebsiteV2 } from '../constructs/v2/static-website';

// Step 3: Gradually migrate old stacks
// (v1 remains available, no forced breaking changes)
```

---

## Complete Example: Reusable Multi-Stack App

```typescript
// bin/app.ts
import { SharedAssets } from '../lib/constructs/shared-assets';
import { FrontendStack } from '../lib/stacks/frontend-stack';
import { BackendStack } from '../lib/stacks/backend-stack';
import { MonitoringStack } from '../lib/stacks/monitoring-stack';

const app = new cdk.App();
const config = loadConfig();

// Step 1: Create shared assets ONCE
const sharedAssets = new SharedAssets(app, 'SharedAssets', {
  lambdaCode: 'src/api',
  dockerImages: ['src/api', 'src/worker'],
});

// Step 2: Deploy stacks using shared assets
const backend = new BackendStack(app, 'Backend', {
  config,
  sharedAssets,
});

const frontend = new FrontendStack(app, 'Frontend', {
  config,
  apiUrl: backend.apiUrl,
});

const monitoring = new MonitoringStack(app, 'Monitoring', {
  config,
  targets: [backend.api, frontend.distribution],
});

app.synth();
```

```typescript
// lib/constructs/shared-assets.ts
export interface SharedAssetsProps {
  lambdaCode: string;
  dockerImages: string[];
}

export class SharedAssets extends Construct {
  public readonly lambdaCode: lambda.Code;
  public readonly dockerImages: Map<string, ecr_assets.DockerImageAsset>;
  public readonly layers: Map<string, lambda.LayerVersion>;

  constructor(scope: Construct, id: string, props: SharedAssetsProps) {
    super(scope, id);

    // Bundle Lambda code ONCE
    this.lambdaCode = lambda.Code.fromAsset(props.lambdaCode, {
      bundling: {
        image: lambda.Runtime.NODEJS_20_X.bundlingImage,
        command: [
          'bash', '-c',
          'npm ci && npm run build && cp -r dist/* /asset-output/',
        ],
      },
    });

    // Build Docker images ONCE
    this.dockerImages = new Map();
    props.dockerImages.forEach((dir) => {
      const name = dir.split('/').pop()!;
      this.dockerImages.set(
        name,
        new ecr_assets.DockerImageAsset(this, `${name}Image`, {
          directory: dir,
        })
      );
    });

    // Create layers ONCE
    this.layers = new Map([
      [
        'common',
        new lambda.LayerVersion(this, 'CommonLayer', {
          code: lambda.Code.fromAsset('src/layers/common'),
          compatibleRuntimes: [lambda.Runtime.NODEJS_20_X],
        }),
      ],
    ]);
  }
}
```

---

## Checklist

Before deploying multi-stack CDK apps:

- [ ] **Shared Assets**: Extract common Lambda code/Docker images to shared construct
- [ ] **L3 Constructs**: Decompose stacks into reusable L3 constructs (<300 lines per file)
- [ ] **Asset Deduplication**: Use consistent paths and bundling for identical code
- [ ] **Layer Strategy**: Separate dependencies into layers, bundle code separately
- [ ] **Docker Optimization**: Multi-stage Dockerfiles, single asset per image
- [ ] **Custom Resources**: Extract to shared constructs with singleton pattern
- [ ] **Versioning**: Use semantic versioning for breaking changes in shared constructs
- [ ] **Deterministic Builds**: Use `npm ci`, exclude variability, lock dependencies

---

## Related Documentation

- [typescript-cdk Golden Repo](../../golden-repos/typescript-cdk/) - Multi-context CDK template
- [Base Stack Pattern](../../golden-repos/typescript-cdk/lib/constructs/base-stack.ts) - Reusable base class
- [AMPLIFY_COGNITO_REUSE_SOP.md](./AMPLIFY_COGNITO_REUSE_SOP.md) - Resource reuse patterns
