<!-- File UUID: 9c4e5f6a-7b8d-4e2f-a1b3-c5d6e7f8a9b0 -->

# Buildinfo Pattern

Generate `buildinfo.json` for frontend deployments to track git metadata and infrastructure ARNs.

## Quick Start

```bash
# Basic - just git info
python3 shared/tools/generate-buildinfo.py --output dist/buildinfo.json

# With CDK outputs (CloudFront, S3, Cognito ARNs)
python3 shared/tools/generate-buildinfo.py \
    --output dist/buildinfo.json \
    --cdk-outputs infra/deploys/current/outputs.json \
    --project-id my-app-12345 \
    --environment prod
```

## Output Format

```json
{
  "build": {
    "gitHash": "a1b2c3d",
    "gitHashFull": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
    "gitBranch": "main",
    "gitDirty": false,
    "buildDate": "2025-01-15T10:30:00+00:00",
    "projectId": "my-app-12345"
  },
  "infrastructure": {
    "cloudfrontDistributionId": "E2ABCD123",
    "cloudfrontDomain": "d123.cloudfront.net",
    "s3BucketName": "my-app-assets-123456",
    "s3BucketArn": "arn:aws:s3:::my-app-assets-123456",
    "cognitoUserPoolId": "us-east-1_abc123",
    "cognitoUserPoolArn": "arn:aws:cognito-idp:us-east-1:123456:userpool/us-east-1_abc123",
    "apiUrl": "https://api.example.com"
  },
  "deployment": {
    "releaseId": "20250115-103000",
    "environment": "prod"
  }
}
```

## Usage by Framework

### Vite / React (Golden Repo Pattern)

The golden repos include a `buildinfo` Makefile target:

```bash
# Generate after build
make build
make buildinfo

# Or combined
make build-with-info
```

Output location: `dist/buildinfo.json`

### Next.js

For Next.js, generate to `public/` before build so it's included in the static export:

```bash
make buildinfo  # Outputs to public/buildinfo.json
make build      # Includes buildinfo.json in build

# Or combined
make build-with-info
```

Output location: `public/buildinfo.json` → accessible at `/buildinfo.json`

### Static HTML

For static HTML sites without a build system:

```bash
# Generate directly to the site root
python3 shared/tools/generate-buildinfo.py \
    --output ./buildinfo.json \
    --cdk-outputs infra/deploys/current/outputs.json \
    --project-id my-static-site
```

### Amplify Integration

Add to your `amplify.yml`:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
        - python3 ../../shared/tools/generate-buildinfo.py \
            --output dist/buildinfo.json \
            --project-id $AWS_APP_ID \
            --environment $AWS_BRANCH
  artifacts:
    baseDirectory: dist
    files:
      - '**/*'
```

## CDK Output Key Mappings

The script automatically maps common CDK output keys to normalized names:

| CDK Output Pattern | Normalized Key |
|-------------------|----------------|
| `CloudFrontDistributionId`, `DistributionId` | `cloudfrontDistributionId` |
| `CloudFrontDomain`, `DistributionDomain` | `cloudfrontDomain` |
| `BucketName`, `AssetsBucket`, `WebsiteBucket` | `s3BucketName` |
| `BucketArn` | `s3BucketArn` |
| `UserPoolId`, `CognitoUserPoolId` | `cognitoUserPoolId` |
| `UserPoolArn` | `cognitoUserPoolArn` |
| `UserPoolClientId`, `CognitoClientId` | `cognitoUserPoolClientId` |
| `IdentityPoolId` | `cognitoIdentityPoolId` |
| `ApiUrl`, `ApiEndpoint`, `RestApiUrl`, `HttpApiUrl` | `apiUrl` |
| `WebSocketUrl`, `WssUrl` | `websocketUrl` |
| `TableArn`, `DynamoDbTableArn` | `dynamoDbTableArn` |
| `QueueUrl`, `QueueArn` | `sqsQueueUrl`, `sqsQueueArn` |
| `TopicArn` | `snsTopicArn` |
| `GraphqlUrl`, `AppSyncUrl` | `graphqlUrl` |

## CLI Options

```
--output, -o       Output path (default: dist/buildinfo.json)
--cdk-outputs      Path to CDK outputs.json file
--stack            Filter to specific CDK stack name
--project-id       Project identifier
--environment, -e  Deployment environment (dev, staging, prod)
--release-id       Release identifier (defaults to timestamp)
--quiet, -q        Suppress output
```

## Makefile Variables

The golden repo Makefiles support these variables:

```makefile
# Override shared tools path
SHARED_TOOLS=/path/to/shared/tools make buildinfo

# Override project ID
PROJECT_ID=custom-name make buildinfo

# Override environment
ENVIRONMENT=prod make buildinfo

# Override CDK outputs path
CDK_OUTPUTS=./outputs.json make buildinfo
```

## Accessing at Runtime

The file is accessible at `/buildinfo.json` from the deployed site:

```javascript
// Fetch buildinfo at runtime (if needed)
const response = await fetch('/buildinfo.json');
const buildinfo = await response.json();
console.log('Deployed from:', buildinfo.build.gitHash);
console.log('CloudFront:', buildinfo.infrastructure.cloudfrontDistributionId);
```

## Displaying in Footer

Use the standard footer template to display buildinfo in your app:

**Template Location:** `shared/design-system/templates/footer-component.tsx`

**Footer displays:**
- Project ID (e.g., `ppm-p1m2n`)
- Environment badge (dev/stage/prod)
- Git commit hash (clickable → GitHub commit page)

**Usage:**
1. Copy `shared/design-system/templates/footer-component.tsx` to your project
2. Update copyright text
3. Update GitHub repo URL in the commit link
4. Import and render in your layout:

```tsx
import { Footer } from '@/components/layout/footer';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Footer />
      </body>
    </html>
  );
}
```

## Security Considerations

- `buildinfo.json` exposes infrastructure identifiers (not secrets)
- ARNs and IDs are not sensitive but reveal infrastructure structure
- If concerned, use `.htaccess` or CloudFront functions to restrict access
- Alternative: Generate to a non-public path and access via API
