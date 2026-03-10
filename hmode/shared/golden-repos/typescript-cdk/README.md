# TypeScript CDK Template

Gold standard AWS CDK template with multi-context, multi-stage configuration.

## Features

- **Multi-Context**: Separate work, personal, and client infrastructure
- **Multi-Stage**: Support any naming pattern (dev/prod, blue/green, alpha/beta/gamma)
- **YAML Configuration**: Context and stage-specific config files
- **Zod Validation**: Type-safe configuration with runtime validation
- **Capistrano-style Deployments**: Release history with rollback support
- **Base Stack Pattern**: Consistent resource naming and tagging
- **Example Stacks**: API Gateway + Lambda, Monitoring
- **Secrets Management**: AWS Secrets Manager integration

## Quick Start

```bash
# Install dependencies
npm install

# List available configurations
make infra-list

# Bootstrap CDK (first time per account)
make infra-bootstrap CONTEXT=work STAGE=dev

# Deploy to work dev environment
make infra-deploy CONTEXT=work STAGE=dev

# Deploy to personal blue environment
make infra-deploy CONTEXT=personal STAGE=blue

# Check deployment status
make infra-status CONTEXT=work STAGE=dev

# View help
make help
```

## Configuration

Multi-context structure with separate configs per context and stage:

```
config/
├── work/               # Work context
│   ├── dev.yml         #   Development
│   ├── stage.yml       #   Staging
│   └── prod.yml        #   Production
├── personal/           # Personal context
│   ├── dev.yml         #   Development
│   ├── alpha.yml       #   Alpha testing
│   ├── blue.yml        #   Blue (prod A)
│   └── green.yml       #   Green (prod B)
├── schema.ts           # Zod validation
├── loader.ts           # Config loading
└── index.ts            # Exports
```

**See [MULTI_CONTEXT.md](docs/MULTI_CONTEXT.md) for complete documentation.**

### Creating a New Context

1. Create context directory:
   ```bash
   mkdir config/client-acme
   ```

2. Update values for the new environment

3. Deploy:
   ```bash
   ENV=integration cdk deploy --all
   ```

### Configuration Schema

```yaml
# Required
account: "123456789012"       # AWS Account ID
region: "us-east-1"           # AWS Region
projectName: "my-app"         # Project name (used in resource names)

# Notifications (required)
notifications:
  adminEmail: "admin@example.com"
  supportEmail: "support@example.com"

# Domain (optional)
domain:
  rootDomain: "example.com"
  subdomain: "api"

# Database (optional)
database:
  instanceClass: "t3.micro"
  multiAz: false

# Compute (optional, has defaults)
compute:
  lambdaMemory: 256
  lambdaTimeout: 30

# Monitoring (optional, has defaults)
monitoring:
  enableDashboards: true
  enableTracing: true
```

## Project Structure

```
typescript-cdk/
├── bin/
│   └── app.ts              # CDK app entry point
├── lib/
│   ├── constructs/
│   │   └── base-stack.ts   # Base stack with common config
│   └── stacks/
│       ├── api-stack.ts    # Example API stack
│       └── monitoring-stack.ts
├── config/
│   ├── schema.ts           # Zod validation
│   ├── loader.ts           # Config utilities
│   ├── dev.yml
│   ├── stage.yml
│   └── prod.yml
├── test/
│   └── config.test.ts
├── package.json
├── tsconfig.json
└── cdk.json
```

## Adding New Stacks

1. Create stack in `lib/stacks/`:

```typescript
import { BaseStack, BaseStackProps } from '../constructs/base-stack';

export class MyStack extends BaseStack {
  constructor(scope: Construct, id: string, props: BaseStackProps) {
    super(scope, id, props);

    // Access config
    const { compute, monitoring } = this.config;

    // Use helper methods
    const resourceName = this.resourceName('my-resource');
    const removalPolicy = this.removalPolicy;
  }
}
```

2. Add to `bin/app.ts`:

```typescript
import { MyStack } from '../lib/stacks/my-stack';

new MyStack(app, 'MyStack', { config });
```

## Environment-Specific Patterns

### Resource Sizing

```typescript
// Automatically uses config values
memorySize: this.config.compute.lambdaMemory,
timeout: cdk.Duration.seconds(this.config.compute.lambdaTimeout),
```

### Conditional Features

```typescript
// Enable tracing only when configured
tracing: this.config.monitoring.enableTracing
  ? lambda.Tracing.ACTIVE
  : lambda.Tracing.DISABLED,
```

### Removal Policies

```typescript
// Retain in prod, destroy elsewhere
removalPolicy: this.isProduction
  ? cdk.RemovalPolicy.RETAIN
  : cdk.RemovalPolicy.DESTROY,
```

## Testing

```bash
# Run tests
npm test

# Validate all config files
npm test -- --run
```

## Useful Commands

```bash
cdk diff          # Compare deployed stack with current state
cdk synth         # Emit synthesized CloudFormation template
cdk deploy        # Deploy this stack to your default AWS account/region
cdk destroy       # Destroy the stack
```
