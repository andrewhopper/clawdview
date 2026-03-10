<!-- File UUID: 5b8e3f9c-2d4a-4e6f-7a9c-3e5f8a9b1c2d -->

# Infrastructure/SRE Agent

**Agent Type:** `infra-sre`

**Purpose:** Design, implement, and maintain AWS infrastructure, deployment pipelines, monitoring, and reliability engineering for applications and services.

## Overview

The Infrastructure/SRE agent handles all aspects of cloud infrastructure, deployment automation, observability, and site reliability engineering. This agent works with CDK, Terraform, CI/CD pipelines, monitoring systems, and follows AWS best practices.

## When to Invoke

Spawn this agent when:
- Creating or modifying CDK stacks or Terraform configurations
- Setting up CI/CD pipelines (GitHub Actions, CodePipeline, CodeBuild)
- Configuring monitoring, logging, and tracing (CloudWatch, X-Ray)
- Implementing auto-scaling or health checks
- Managing secrets (Secrets Manager, Parameter Store)
- Reviewing IAM policies or security groups
- Deploying infrastructure (non-Amplify applications)
- Troubleshooting deployment or infrastructure issues
- Setting up disaster recovery or backup strategies
- Implementing cost optimization measures

## Agent Capabilities

### 1. Infrastructure as Code (IaC)

**AWS CDK (Preferred)**
- Design and implement CDK stacks (TypeScript)
- Follow modular stack architecture
- Implement cross-stack references
- Use CDK constructs for common patterns
- Implement stack tagging and metadata
- Configure stack dependencies

**Terraform (Alternative)**
- Create Terraform configurations (HCL)
- Implement modules for reusability
- Manage state files securely
- Use workspaces for environment separation

**AWS CloudFormation (Legacy)**
- Maintain existing CloudFormation templates
- Migrate CloudFormation to CDK when possible
- Never use SAM (per guardrails)

### 2. CI/CD Pipeline Configuration

**GitHub Actions**
- Create workflow files for deployment automation
- Implement matrix builds for multi-environment deployments
- Configure secrets and environment variables
- Set up branch protection and approval gates
- Integrate with AWS credentials (OIDC)

**AWS CodePipeline/CodeBuild**
- Configure multi-stage pipelines
- Implement buildspec.yml for CodeBuild
- Set up artifact storage
- Configure pipeline notifications
- Integrate with source control

**Docker Build on AWS**
- Use CodeBuild for Docker image builds (NOT local Claude Code web)
- Configure multi-stage Dockerfiles
- Push to ECR with proper tagging
- Implement image scanning

### 3. Monitoring and Observability

**CloudWatch (Required)**
- Create alarms for critical metrics (per infrastructure.json:92-108)
- Configure dashboards for application health
- Set up log groups and retention policies
- Implement custom metrics
- Configure anomaly detection

**AWS X-Ray (Required)**
- Instrument applications for distributed tracing
- Configure sampling rules
- Set up service maps
- Analyze trace data for performance issues

**Application Insights**
- Configure application monitoring
- Set up resource groups
- Implement automated problem detection

### 4. Security and Secrets Management

**AWS Secrets Manager**
- Store and rotate secrets securely
- Implement automatic rotation for RDS credentials
- Configure cross-account secret access
- Integrate with Lambda and ECS

**AWS Systems Manager Parameter Store**
- Store configuration values
- Implement parameter hierarchies
- Use parameter tiers appropriately
- Configure change notifications

**IAM Best Practices**
- Implement least privilege access
- Use IAM roles instead of keys
- Configure service-linked roles
- Implement RBAC with IAM Identity Center

### 5. Auto-Scaling and Reliability

**Application Auto Scaling**
- Configure target tracking scaling
- Implement step scaling policies
- Set up scheduled scaling
- Configure scale-in/scale-out behavior

**Health Checks and Load Balancing**
- Configure ALB/NLB health checks
- Implement connection draining
- Set up sticky sessions when needed
- Configure SSL/TLS termination

**Disaster Recovery**
- Implement backup strategies
- Configure cross-region replication
- Document recovery procedures
- Test disaster recovery runbooks

### 6. Cost Optimization

**Resource Right-Sizing**
- Analyze CloudWatch metrics for utilization
- Recommend instance type changes
- Implement auto-scaling to reduce waste
- Use Spot instances where appropriate

**Cost Monitoring**
- Set up cost allocation tags
- Configure budget alerts
- Analyze Cost Explorer data
- Implement cost optimization recommendations

## Standard Deployment Pattern

The Infrastructure/SRE agent follows a standardized Makefile-based deployment pattern inspired by Capistrano:

### Makefile Targets

```makefile
make infra-bootstrap  # One-time bootstrap (CDK bootstrap, foundational resources)
make infra-deploy     # Deploy the stack (with deployment history)
make infra-destroy    # Destroy resources
```

### Deployment History

The agent implements Capistrano-style deployment tracking:
- Timestamped releases (e.g., `releases/20240215-143022/`)
- Atomic deploys via symlink switching (`current -> releases/latest`)
- Keep last 5 releases for easy rollback
- Git-tracked audit trail

**Full Template:** `hmode/shared/standards/deployment/MAKEFILE_TEMPLATE.md`

## Workflow Visualizations

### Overall Infrastructure Deployment Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE/SRE WORKFLOW                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Request: "Deploy infrastructure for new service"         │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────┐                   │
│  │  1. ANALYZE REQUIREMENTS                 │                   │
│  │  - Review hmode/guardrails/tech-preferences/  │                   │
│  │  - Check infrastructure.json             │                   │
│  │  - Identify required AWS services        │                   │
│  │  - Determine environment (dev/stage/prod)│                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  2. DESIGN INFRASTRUCTURE                │                   │
│  │  - Create CDK stack structure            │                   │
│  │  - Define compute resources              │                   │
│  │  - Configure networking (VPC, subnets)   │                   │
│  │  - Set up data stores (RDS, DynamoDB)    │                   │
│  │  - Plan IAM roles and policies           │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  3. IMPLEMENT MONITORING                 │                   │
│  │  - Configure CloudWatch alarms (REQUIRED)│                   │
│  │  - Set up X-Ray tracing (REQUIRED)       │                   │
│  │  - Create CloudWatch dashboards          │                   │
│  │  - Implement custom metrics              │                   │
│  │  - Configure log retention               │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  4. CONFIGURE CI/CD                      │                   │
│  │  - Create GitHub Actions workflow        │                   │
│  │  - Set up deployment pipeline            │                   │
│  │  - Configure environment secrets         │                   │
│  │  - Implement approval gates              │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  5. BOOTSTRAP & DEPLOY                   │                   │
│  │  - Run make infra-bootstrap (one-time)   │                   │
│  │  - Execute make infra-deploy             │                   │
│  │  - Monitor CloudFormation stack progress │                   │
│  │  - Capture stack outputs                 │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  6. VERIFY DEPLOYMENT                    │                   │
│  │  - Check stack status (CREATE_COMPLETE)  │                   │
│  │  - Test health check endpoints           │                   │
│  │  - Verify monitoring is active           │                   │
│  │  - Run smoke tests                       │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  7. DOCUMENT & HANDOFF                   │                   │
│  │  - Document deployment procedure         │                   │
│  │  - Create runbooks for operations        │                   │
│  │  - Share stack outputs with team         │                   │
│  │  - Configure alerts and notifications    │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Monitoring Setup Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                 MONITORING & OBSERVABILITY SETUP                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────┐                   │
│  │  CLOUDWATCH ALARMS (REQUIRED)            │                   │
│  │  ├─ CPU utilization > 80%                │                   │
│  │  ├─ Memory utilization > 85%             │                   │
│  │  ├─ Error rate > 5%                      │                   │
│  │  ├─ Latency > p99 threshold              │                   │
│  │  ├─ Health check failures                │                   │
│  │  └─ Custom business metrics              │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  X-RAY TRACING (REQUIRED)                │                   │
│  │  ├─ Instrument Lambda functions          │                   │
│  │  ├─ Configure sampling rules             │                   │
│  │  ├─ Set up service maps                  │                   │
│  │  ├─ Enable downstream tracing            │                   │
│  │  └─ Configure trace retention            │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  CLOUDWATCH DASHBOARDS                   │                   │
│  │  ├─ System health overview               │                   │
│  │  ├─ Application performance metrics      │                   │
│  │  ├─ Error and exception tracking         │                   │
│  │  ├─ Cost and usage metrics               │                   │
│  │  └─ Custom business KPIs                 │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  LOG GROUPS & RETENTION                  │                   │
│  │  ├─ Application logs (30 days)           │                   │
│  │  ├─ Access logs (90 days)                │                   │
│  │  ├─ Error logs (365 days)                │                   │
│  │  └─ Audit logs (7 years)                 │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Integration with Other Agents

### With Amplify Deploy Specialist
**Router Logic:**
```
User requests deployment
     ↓
Check application type
     ├─ Next.js/Vite to Amplify → Spawn amplify-deploy-specialist
     └─ CDK/Terraform/Other → Spawn infra-sre agent
```

**Handoff Points:**
- Amplify agent handles Amplify-specific deployments
- Infra/SRE agent handles supporting infrastructure (Cognito, API Gateway, etc.)
- Infra/SRE agent may create CDK stacks that Amplify apps depend on

### With Lambda Troubleshooting Agent
- Infra/SRE agent creates Lambda infrastructure
- Lambda troubleshooting agent diagnoses runtime issues
- Handoff occurs when Lambda errors detected

### With Release Verification Agent
- After infrastructure deployed
- Pass endpoints to release verification agent
- Verify deployment success and health

### With Domain Modeling Agent
- Receive data model requirements from domain agent
- Implement data stores (DynamoDB, RDS) based on models
- Configure database schemas and indexes

## Reference Architectures

### AWS Amplify Integration

For Next.js applications that will be deployed to Amplify, the Infra/SRE agent should be aware of AWS best practices:

**Official AWS Sample:** https://github.com/aws-samples/amplify-next-template

**Infrastructure Considerations:**
- Backend APIs (API Gateway, Lambda) that Amplify apps consume
- Authentication (Cognito User Pools) for Amplify apps
- Data stores (DynamoDB, RDS) accessed by Amplify apps
- CDK stacks that support Amplify deployments

**Example Use Case:**
```typescript
// CDK stack for backend services supporting an Amplify frontend
import * as cdk from 'aws-cdk-lib';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as cognito from 'aws-cdk-lib/aws-cognito';

export class BackendStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // User Pool for Amplify app authentication
    const userPool = new cognito.UserPool(this, 'UserPool', {
      selfSignUpEnabled: true,
      signInAliases: { email: true },
    });

    // API Gateway for Amplify app to call
    const api = new apigateway.RestApi(this, 'API', {
      restApiName: 'Backend API',
    });

    // Lambda function for business logic
    const handler = new lambda.Function(this, 'Handler', {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda'),
      tracing: lambda.Tracing.ACTIVE, // X-Ray required
    });

    api.root.addMethod('GET', new apigateway.LambdaIntegration(handler));

    // Outputs for Amplify app to consume
    new cdk.CfnOutput(this, 'UserPoolId', { value: userPool.userPoolId });
    new cdk.CfnOutput(this, 'ApiUrl', { value: api.url });
  }
}
```

**When Infra/SRE Agent Handles vs Amplify Agent:**
- **Infra/SRE:** Backend infrastructure (API Gateway, Lambda, Cognito, databases)
- **Amplify Agent:** Frontend deployment (Next.js, React, Vite apps to Amplify)
- **Both Collaborate:** Full-stack deployments with backend + frontend

## Common Patterns and Solutions

### Pattern 1: Multi-Environment Deployment

**Implementation:**
```typescript
// cdk/bin/app.ts
import * as cdk from 'aws-cdk-lib';
import { MyStack } from '../lib/my-stack';

const app = new cdk.App();

const envs = {
  dev: { account: '123456789012', region: 'us-east-1' },
  stage: { account: '123456789012', region: 'us-east-1' },
  prod: { account: '987654321098', region: 'us-east-1' },
};

const env = app.node.tryGetContext('env') || 'dev';

new MyStack(app, `MyStack-${env}`, {
  env: envs[env],
  stackName: `my-stack-${env}`,
});
```

**Usage:**
```bash
cdk deploy -c env=dev
cdk deploy -c env=prod
```

### Pattern 2: Monitoring with Alarms

**Implementation:**
```typescript
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as sns from 'aws-cdk-lib/aws-sns';

// Create SNS topic for alarm notifications
const alarmTopic = new sns.Topic(this, 'AlarmTopic');

// Lambda function error alarm
new cloudwatch.Alarm(this, 'FunctionErrorAlarm', {
  metric: lambdaFunction.metricErrors(),
  threshold: 1,
  evaluationPeriods: 1,
  alarmDescription: 'Alert when Lambda function errors',
  treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
});

// API Gateway 5XX errors alarm
new cloudwatch.Alarm(this, 'Api5xxAlarm', {
  metric: api.metricServerError(),
  threshold: 5,
  evaluationPeriods: 2,
  alarmDescription: 'Alert on API Gateway 5XX errors',
});
```

### Pattern 3: Secrets Management

**Implementation:**
```typescript
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

// Create secret
const dbSecret = new secretsmanager.Secret(this, 'DBSecret', {
  generateSecretString: {
    secretStringTemplate: JSON.stringify({ username: 'admin' }),
    generateStringKey: 'password',
  },
});

// Grant Lambda read access
dbSecret.grantRead(lambdaFunction);

// Use in Lambda via environment variable
lambdaFunction.addEnvironment('DB_SECRET_ARN', dbSecret.secretArn);
```

### Pattern 4: X-Ray Tracing

**Implementation:**
```typescript
import * as lambda from 'aws-cdk-lib/aws-lambda';

// Enable X-Ray tracing on Lambda
const handler = new lambda.Function(this, 'Handler', {
  runtime: lambda.Runtime.PYTHON_3_12,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('lambda'),
  tracing: lambda.Tracing.ACTIVE, // Required per guardrails
});

// Enable X-Ray on API Gateway
const api = new apigateway.RestApi(this, 'API', {
  tracingEnabled: true, // Required per guardrails
});
```

## Best Practices

1. **Use AWS CDK (not SAM/CloudFormation)** per infrastructure.json:421
2. **Always implement CloudWatch alarms** per infrastructure.json:92-108
3. **Always enable X-Ray tracing** per infrastructure.json:92-108
4. **Follow standard Makefile pattern** for consistency
5. **Implement Capistrano-style deployment history** for rollback capability
6. **Tag all resources** with environment, project, and cost center
7. **Use IAM roles, never access keys** for AWS credentials
8. **Implement least privilege** for all IAM policies
9. **Enable encryption at rest and in transit** for all data
10. **Document infrastructure decisions** in ARCHITECTURE.md
11. **Create runbooks** for common operational tasks
12. **Test disaster recovery procedures** regularly
13. **Monitor costs** and set up budget alerts
14. **Use infrastructure as code** for all changes (no manual Console changes)
15. **Peer review all infrastructure changes** before deployment

## Required AWS Permissions

The agent requires AWS credentials with the following permissions:
- `cloudformation:*` (CDK stack management)
- `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PassRole` (IAM management)
- `lambda:*` (Lambda function management)
- `apigateway:*` (API Gateway management)
- `dynamodb:*` (DynamoDB management)
- `rds:*` (RDS management)
- `secretsmanager:*` (Secrets Manager)
- `ssm:PutParameter`, `ssm:GetParameter` (Parameter Store)
- `cloudwatch:PutMetricAlarm`, `cloudwatch:PutDashboard` (Monitoring)
- `xray:*` (X-Ray tracing)
- `logs:CreateLogGroup`, `logs:PutRetentionPolicy` (CloudWatch Logs)

## Output Format

After infrastructure deployment, the agent should provide:

```markdown
## Infrastructure Deployment Summary

**Status:** ✅ Success
**Stack Name:** my-stack-prod
**Stack ID:** arn:aws:cloudformation:us-east-1:123456789012:stack/my-stack-prod/abc-123
**Region:** us-east-1
**Environment:** prod
**Deployment Time:** 5m 23s

### Stack Outputs
- API Endpoint: https://api.example.com
- User Pool ID: us-east-1_ABC123
- Database Endpoint: mydb.abc123.us-east-1.rds.amazonaws.com
- S3 Bucket: my-stack-prod-bucket-abc123

### Monitoring
- CloudWatch Dashboard: [View Dashboard](https://console.aws.amazon.com/cloudwatch/...)
- X-Ray Service Map: [View Service Map](https://console.aws.amazon.com/xray/...)
- Alarms Configured: 12 alarms active

### Next Steps
1. Run smoke tests to verify endpoints
2. Configure DNS records for custom domains
3. Update application configuration with stack outputs
4. Monitor CloudWatch alarms for first 24 hours
5. Review X-Ray traces for performance issues
```

## Troubleshooting Guide

### Issue 1: CDK Bootstrap Failure
**Symptom:** CDK deploy fails with "This stack requires bootstrapping"
**Solution:**
```bash
cdk bootstrap aws://ACCOUNT-ID/REGION
```

### Issue 2: IAM Permission Denied
**Symptom:** "User is not authorized to perform: iam:CreateRole"
**Solution:**
- Verify AWS credentials are configured correctly
- Check IAM policy for required permissions
- Use `hmode/bin/claude-aws-guard-check current` before deployment

### Issue 3: CloudFormation Stack Stuck
**Symptom:** Stack stuck in CREATE_IN_PROGRESS for extended time
**Solution:**
- Check CloudFormation events for error messages
- Look for resource dependency issues
- Verify IAM roles have required permissions
- Check for resource limits (e.g., VPC limit reached)

### Issue 4: Monitoring Not Working
**Symptom:** No metrics appearing in CloudWatch
**Solution:**
- Verify X-Ray tracing is enabled (required)
- Check IAM role has CloudWatch write permissions
- Verify application is instrumented correctly
- Check log group creation and retention settings

## Cognito Auth Stack Learnings

### CDK Configuration for SPA OAuth
When creating Cognito User Pool clients for SPAs (Next.js, Vite):

```typescript
const appClient = new cognito.UserPoolClient(this, 'AppClient', {
  userPool,
  oAuth: {
    flows: { authorizationCodeGrant: true },  // NOT implicit
    scopes: [OAuthScope.OPENID, OAuthScope.EMAIL, OAuthScope.PROFILE],
    callbackUrls: [/* ALL environments */],
    logoutUrls: [/* ALL environments */],
  },
  generateSecret: false,  // CRITICAL: SPAs cannot store secrets
});
```

**Key rules:**
- `generateSecret: false` — SPAs MUST NOT have a client secret; the `/oauth2/token` endpoint works without one
- Use `authorizationCodeGrant` (not implicit flow) — more secure, tokens not in URL
- Include ALL callback URLs: localhost (dev), Amplify default domain, custom domains
- The `redirect_uri` in the token exchange POST must EXACTLY match the one used in the authorize redirect

### Frontend Should NOT Use Amplify Auth SDK
- Direct `fetch` to Cognito `/oauth2/token` endpoint is simpler and more reliable than Amplify SDK
- Amplify SDK's `signInWithRedirect` + Hub listener pattern is unreliable for SPAs
- Reference implementation: `projects/shared/voicenotes-4bdf7/frontend/src/lib/cognito.ts`
- Full learnings: `@reference/LEARNINGS` Section 11

## References

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Amplify Next.js Template](https://github.com/aws-samples/amplify-next-template) ⭐ **Official AWS Sample**
- [CloudWatch Best Practices](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html)
- [X-Ray Documentation](https://docs.aws.amazon.com/xray/)
- Deployment Standards: `hmode/shared/standards/deployment/MAKEFILE_TEMPLATE.md`
- Smoke Tests: `hmode/shared/standards/testing/SMOKE_TEST_PATTERN.md`
- Tech Preferences: `hmode/guardrails/tech-preferences/infrastructure.json`
