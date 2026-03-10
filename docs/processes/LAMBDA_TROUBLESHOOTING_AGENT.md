<!-- File UUID: 8f4a2c7d-9e1b-4f3a-a8d6-5c9e3b7f1a2d -->

# AWS Lambda Troubleshooting Agent

## Overview

Specialized agent for diagnosing and resolving AWS Lambda function issues, with deep understanding of Lambda architecture, constraints, integrations, and common failure patterns.

## Agent Capabilities

### 1.0 Core Lambda Knowledge

**Lambda Architecture:**
- Execution environment lifecycle (INIT, INVOKE, SHUTDOWN)
- Cold start vs warm start behavior
- Container reuse patterns
- /tmp storage (512MB ephemeral, cleared on cold start)
- Memory/CPU allocation relationship (vCPU scales with memory)
- Timeout limits (max 15 minutes)
- Concurrent execution limits (1000 default, configurable)
- Reserved vs provisioned concurrency

**Lambda Layers:**
- Layer attachment (max 5 layers per function)
- Layer size limits (50MB zipped, 250MB unzipped total)
- Layer versioning and ARN resolution
- Common use cases: shared dependencies, runtime patches, custom runtimes
- Layer extraction path: `/opt` directory structure
- Python layers: `/opt/python/` for packages
- Node.js layers: `/opt/nodejs/node_modules/` for packages
- Troubleshooting layer conflicts and missing dependencies

**API Gateway Integration:**
- Lambda proxy integration vs custom integration
- Request/response transformation
- Payload format version 1.0 vs 2.0
- Event structure differences (REST vs HTTP API)
- Authorization: Lambda authorizers, IAM, Cognito, API keys
- Timeout constraints (29 seconds API Gateway max)
- Binary media type handling
- CORS configuration issues
- Resource policy requirements for API Gateway to invoke Lambda

### 2.0 Constraint Knowledge

**Size Limits:**
```
Deployment package:
  - Direct upload: 50MB (zipped)
  - S3: 250MB (unzipped)
  - Layers: 50MB each (zipped), 250MB total (unzipped)

Code + Layers:
  - Total unzipped: 250MB limit
  - /tmp storage: 512MB ephemeral

Request/Response:
  - Synchronous payload: 6MB (request + response)
  - Asynchronous payload: 256KB
  - API Gateway payload: 10MB (request + response combined)
```

**Execution Limits:**
```
Timeout: 1 second - 15 minutes (900s max)
Memory: 128MB - 10,240MB (10GB)
Ephemeral /tmp: 512MB - 10,240MB (configurable)
Concurrent executions: 1000 (default account limit)
Environment variables: 4KB total
```

**Network Constraints:**
```
VPC Lambda:
  - Requires ENI creation (cold start delay)
  - NAT Gateway for internet access
  - VPC endpoint for AWS service access
  - Security group rules apply

Non-VPC Lambda:
  - No VPC resources access by default
  - Internet access built-in
  - Faster cold starts
```

### 2.5 IAM Roles & Permissions

**Lambda Execution Role (REQUIRED):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Common IAM Policies by Service:**

**Bedrock Access:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-*",
        "arn:aws:bedrock:*::foundation-model/amazon.titan-*"
      ]
    }
  ]
}
```

**API Gateway Invocation (Resource Policy):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:region:account:function:function-name",
      "Condition": {
        "ArnLike": {
          "AWS:SourceArn": "arn:aws:execute-api:region:account:api-id/*/*"
        }
      }
    }
  ]
}
```

**DynamoDB Access:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:region:account:table/table-name"
    }
  ]
}
```

**S3 Access:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::bucket-name/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::bucket-name"
    }
  ]
}
```

**Secrets Manager Access:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:region:account:secret:secret-name-*"
    }
  ]
}
```

**CloudWatch Logs (ALWAYS REQUIRED):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:region:account:log-group:/aws/lambda/*"
    }
  ]
}
```

**VPC Access (if VPC-enabled):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface"
      ],
      "Resource": "*"
    }
  ]
}
```

### 2.6 API Gateway Authorization

**Authorization Methods:**

**1. API Keys (Simple rate limiting):**
```yaml
Usage:
  - Good for: Public APIs with rate limiting
  - NOT for: Security (keys visible in transit)
  - Setup: API Gateway → Usage Plans → API Keys
  - Header: x-api-key: {key}
```

**2. Lambda Authorizers (Custom auth logic):**
```yaml
Types:
  - TOKEN: Authorization header (JWT, OAuth)
  - REQUEST: Full request context (headers, query, etc.)

Response format:
  {
    "principalId": "user-id",
    "policyDocument": {
      "Version": "2012-10-17",
      "Statement": [{
        "Action": "execute-api:Invoke",
        "Effect": "Allow|Deny",
        "Resource": "arn:aws:execute-api:..."
      }]
    },
    "context": {
      "key": "value"  # Passed to backend Lambda
    }
  }

Cache: 0-3600 seconds (use wisely for performance)
```

**3. Cognito User Pools:**
```yaml
Setup:
  - API Gateway → Authorizers → Cognito
  - Requires: User Pool ID, App Client ID
  - Header: Authorization: Bearer {id_token}
  - Auto-validates: Token signature, expiration
```

**4. IAM Authorization:**
```yaml
Use case: Service-to-service, AWS SDK clients
Requires: AWS SigV4 signing
Good for: Internal APIs, no public access
```

**Common Authorization Issues:**

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Missing/invalid auth header | Check header name and value format |
| 403 Forbidden | Valid auth but no permission | Check IAM policy or authorizer response |
| {"message": "Forbidden"} | API Gateway resource policy | Add source ARN condition |
| Authorizer error | Lambda authorizer crashed | Check CloudWatch logs for authorizer function |
| Token expired | Cognito token TTL exceeded | Refresh token and retry |
| API key invalid | Wrong key or usage plan | Verify key in Usage Plan association |

**Security Best Practices:**
```
[1] ALWAYS use HTTPS (wss:// for WebSockets)
[2] NEVER put API keys in code (use Secrets Manager)
[3] ALWAYS use Lambda authorizers for custom auth logic
[4] ALWAYS validate tokens server-side (don't trust client)
[5] ALWAYS set appropriate CORS headers
[6] ALWAYS use least-privilege IAM policies
[7] ALWAYS enable CloudWatch logging for debugging
[8] ALWAYS cache authorizer responses (if stateless)
```

### 3.0 Common Issues & Diagnostics

**Issue Category Matrix:**

| Symptom | Common Causes | Investigation Path |
|---------|--------------|-------------------|
| Cold start timeouts | Large deployment package, VPC ENI creation, layer extraction | Check package size, VPC config, provisioned concurrency |
| Import errors | Missing layer, wrong layer path, version mismatch | Verify layer ARN, check `/opt` structure, test locally (Section 5.5) |
| Memory errors | Memory limit too low, memory leak | Check CloudWatch metrics, increase memory, profile code |
| Timeout errors | Long-running operation, external API delays, DB connection pooling | Increase timeout, async processing, connection reuse |
| Permission errors | Missing IAM policy, resource policy, VPC access | Check execution role (Section 2.5), resource policies, security groups |
| API Gateway 502/504 | Lambda timeout, large response, malformed response | Check Lambda duration, response size, response format |
| Throttling | Concurrent limit reached, burst limit exceeded | Check CloudWatch metrics, request reserved concurrency |
| Bedrock AccessDenied | Missing bedrock:InvokeModel permission | Add Bedrock policy to execution role (Section 2.5) |
| API Gateway 403 | Missing Lambda resource policy | Add execute-api:Invoke resource policy (Section 2.5) |
| API Gateway 401 | Authorization failure | Check authorizer config, token validity (Section 2.6) |
| Logs not appearing | Missing CloudWatch Logs permissions | Add logs:CreateLogGroup, logs:PutLogEvents to role (Section 2.5) |

**Diagnostic Checklist:**

```
1.0 CloudWatch Logs
    1.1 Check for START/END/REPORT lines
    1.2 Verify function execution duration
    1.3 Look for ERROR/Exception patterns
    1.4 Check memory usage (Max Memory Used vs Allocated)
    1.5 Identify cold start indicators (Init Duration)

2.0 CloudWatch Metrics
    2.1 Invocations - call volume
    2.2 Errors - function errors
    2.3 Throttles - rate limiting
    2.4 Duration - execution time percentiles
    2.5 ConcurrentExecutions - concurrency usage
    2.6 IteratorAge (for stream processors)

3.0 X-Ray Traces (if enabled)
    3.1 End-to-end latency breakdown
    3.2 Downstream service calls
    3.3 Cold start vs warm start comparison
    3.4 Bottleneck identification

4.0 Configuration Review
    4.1 Memory allocation vs actual usage
    4.2 Timeout setting vs actual duration
    4.3 Layer versions and compatibility
    4.4 VPC configuration (if applicable)
    4.5 Environment variables
    4.6 Execution role permissions
```

### 4.0 Troubleshooting Workflows

**4.1 Cold Start Investigation:**
```
Step 1: Enable X-Ray tracing
Step 2: Check Init Duration in CloudWatch logs
Step 3: Identify causes:
  - Package size > 50MB? → Reduce deps, use layers
  - VPC Lambda? → Consider Hyperplane ENI (newer runtimes auto)
  - Many layers? → Consolidate, remove unused
  - Large dependencies? → Lazy load, tree shake
Step 4: Mitigation:
  - Provisioned concurrency (if cost-justified)
  - Reduce package size
  - Remove VPC if not needed
  - Use ARM64 (Graviton2) for faster boot
```

**4.2 Memory/Performance Optimization:**
```
Step 1: Check Max Memory Used in CloudWatch logs
Step 2: Compare to allocated memory
Step 3: Tune memory allocation:
  - If Max < 50% allocated → Reduce memory (save cost)
  - If Max > 80% allocated → Increase memory (avoid OOM)
  - Test at different memory levels (CPU scales with memory)
Step 4: Profile memory usage:
  - Use memory profiling tools (memory-profiler, heapdump)
  - Identify memory leaks or inefficient patterns
```

**4.3 API Gateway Integration Issues:**
```
Step 1: Verify payload format version
  - Lambda proxy: event.requestContext, event.body (string)
  - HTTP API v2: event.version == "2.0"
Step 2: Check response format:
  - Must include: statusCode, headers, body
  - Body must be string (JSON.stringify if needed)
  - Headers must be object (not array)
Step 3: Verify CORS headers (if frontend):
  - Access-Control-Allow-Origin
  - Access-Control-Allow-Methods
  - Access-Control-Allow-Headers
Step 4: Check timeout alignment:
  - API Gateway: 29s max
  - Lambda: Configure ≤ 29s if synchronous
```

**4.4 Layer Dependency Issues:**
```
Step 1: List attached layers and versions
Step 2: Verify layer contents:
  - Python: /opt/python/lib/python3.X/site-packages/
  - Node.js: /opt/nodejs/node_modules/
Step 3: Test layer locally:
  - Download layer from console or aws lambda get-layer-version
  - Extract and verify file structure
  - Check for missing dependencies
Step 4: Rebuild layer if needed:
  - Use correct directory structure
  - Build on Amazon Linux 2 (or use Docker with public.ecr.aws/lambda/python:3.x)
  - Test import in Lambda console
```

**4.5 VPC Lambda Connectivity:**
```
Step 1: Verify VPC configuration:
  - Subnets: Use private subnets (not public)
  - Security groups: Allow outbound traffic
  - NAT Gateway: Required for internet access
Step 2: Test connectivity:
  - AWS services: Use VPC endpoints (S3, DynamoDB, etc.)
  - External APIs: Verify NAT Gateway route
  - Internal resources: Check security group rules
Step 3: Troubleshoot ENI issues:
  - Check for ENI creation errors in CloudWatch
  - Verify subnet has available IPs
  - Check IAM permissions for ENI creation
```

### 5.0 Common Anti-Patterns

**❌ Anti-Pattern 1: Initializing SDK clients inside handler**
```python
# BAD
def handler(event, context):
    s3 = boto3.client('s3')  # New client every invocation
    return s3.list_buckets()
```

**✅ Correct Pattern:**
```python
# GOOD - Connection reuse across invocations
s3 = boto3.client('s3')  # Initialize outside handler

def handler(event, context):
    return s3.list_buckets()
```

**❌ Anti-Pattern 2: Not handling cold starts gracefully**
```python
# BAD - Imports everything at once
import pandas as pd
import numpy as np
import sklearn
# 10+ seconds cold start
```

**✅ Correct Pattern:**
```python
# GOOD - Lazy imports for conditional paths
def handler(event, context):
    if event['operation'] == 'ml':
        import sklearn  # Only load if needed
        return sklearn_operation()
```

**❌ Anti-Pattern 3: Ignoring memory-CPU relationship**
```python
# BAD - CPU-bound task with minimal memory
# 128MB = 0.08 vCPU (very slow)
```

**✅ Correct Pattern:**
```python
# GOOD - Scale memory for CPU-bound tasks
# 1792MB = 1 full vCPU
# 3008MB = ~1.75 vCPU
# Test to find cost/performance sweet spot
```

**❌ Anti-Pattern 4: Large response payloads through API Gateway**
```python
# BAD - Returning 15MB JSON through API Gateway
return {
    'statusCode': 200,
    'body': json.dumps(huge_dataset)  # > 10MB = 502 error
}
```

**✅ Correct Pattern:**
```python
# GOOD - Upload to S3, return presigned URL
s3.put_object(Bucket='results', Key=key, Body=data)
url = s3.generate_presigned_url('get_object', Params={'Bucket': 'results', 'Key': key})
return {'statusCode': 200, 'body': json.dumps({'url': url})}
```

### 5.5 Local Development & Testing

**Local Testing Options:**

**1. SAM CLI (AWS recommended):**
```bash
# Install SAM CLI
brew install aws-sam-cli  # macOS
# or
pip install aws-sam-cli

# Create test event
cat > event.json <<EOF
{
  "body": "{\"key\": \"value\"}",
  "headers": {
    "Content-Type": "application/json"
  },
  "httpMethod": "POST",
  "path": "/api/endpoint"
}
EOF

# Invoke locally (no Docker, fast)
sam local invoke MyFunction --event event.json --no-event

# Start local API Gateway (with Docker)
sam local start-api --port 3000
# Test: curl http://localhost:3000/endpoint

# Start local Lambda endpoint (Docker)
sam local start-lambda --port 3001
aws lambda invoke --function-name MyFunction --endpoint-url http://localhost:3001 --payload file://event.json output.json
```

**2. Lambda Docker Images (native AWS runtimes):**
```bash
# Python example
docker run -p 9000:8080 \
  -v $(pwd):/var/task \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
  public.ecr.aws/lambda/python:3.11 \
  lambda_function.handler

# Invoke
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"key": "value"}'
```

**3. Python Local Testing (no Docker):**
```python
# test_lambda.py
import json
from lambda_function import handler

# Mock context object
class MockContext:
    function_name = 'test-function'
    function_version = '$LATEST'
    invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:test'
    memory_limit_in_mb = 128
    aws_request_id = 'test-request-id'
    log_group_name = '/aws/lambda/test'
    log_stream_name = 'test-stream'

    @staticmethod
    def get_remaining_time_in_millis():
        return 300000

# Test event
event = {
    'httpMethod': 'GET',
    'path': '/api/test',
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps({'key': 'value'})
}

# Invoke
result = handler(event, MockContext())
print(json.dumps(result, indent=2))
```

**4. Node.js Local Testing:**
```javascript
// test-lambda.js
const handler = require('./index').handler;

const event = {
  httpMethod: 'GET',
  path: '/api/test',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ key: 'value' })
};

const context = {
  functionName: 'test-function',
  functionVersion: '$LATEST',
  invokedFunctionArn: 'arn:aws:lambda:us-east-1:123456789012:function:test',
  memoryLimitInMB: 128,
  awsRequestId: 'test-request-id',
  logGroupName: '/aws/lambda/test',
  logStreamName: 'test-stream',
  getRemainingTimeInMillis: () => 300000
};

handler(event, context, (err, result) => {
  if (err) {
    console.error('Error:', err);
  } else {
    console.log('Result:', JSON.stringify(result, null, 2));
  }
});
```

**5. Testing with Layers Locally:**
```bash
# Download layer
aws lambda get-layer-version \
  --layer-name my-layer \
  --version-number 1 \
  --query 'Content.Location' \
  --output text | xargs curl -o layer.zip

# Extract layer
mkdir -p ./opt
unzip layer.zip -d ./opt

# Set PYTHONPATH (Python)
export PYTHONPATH="./opt/python:$PYTHONPATH"
python test_lambda.py

# Set NODE_PATH (Node.js)
export NODE_PATH="./opt/nodejs/node_modules:$NODE_PATH"
node test-lambda.js
```

**6. Environment Variables in Local Tests:**
```bash
# Load from .env file
export $(cat .env.local | xargs)

# Or inline
AWS_REGION=us-east-1 \
TABLE_NAME=my-table \
python test_lambda.py
```

### 5.6 Log Tailing & Real-Time Debugging

**CloudWatch Logs Tail Commands:**

**1. AWS CLI (built-in tail):**
```bash
# Tail logs in real-time (refreshes every 2s)
aws logs tail /aws/lambda/my-function --follow

# Tail with time filter
aws logs tail /aws/lambda/my-function --since 5m --follow

# Tail with grep filter
aws logs tail /aws/lambda/my-function --follow --filter-pattern "ERROR"

# Tail specific log stream
aws logs tail /aws/lambda/my-function --follow \
  --log-stream-names "2024/01/15/[$LATEST]abcd1234"
```

**2. SAM CLI Logs:**
```bash
# Tail logs for SAM deployed function
sam logs --name MyFunction --tail

# With time filter
sam logs --name MyFunction --tail --start-time "5 minutes ago"

# Filter errors only
sam logs --name MyFunction --tail --filter "ERROR"
```

**3. CloudWatch Insights (Real-Time Queries):**
```bash
# Start query
QUERY_ID=$(aws logs start-query \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -u -d '5 minutes ago' +%s) \
  --end-time $(date -u +%s) \
  --query-string 'fields @timestamp, @message | sort @timestamp desc | limit 20' \
  --query 'queryId' --output text)

# Poll for results
while true; do
  STATUS=$(aws logs get-query-results --query-id $QUERY_ID --query 'status' --output text)
  if [ "$STATUS" = "Complete" ]; then
    aws logs get-query-results --query-id $QUERY_ID
    break
  fi
  sleep 1
done
```

**4. Watch Command (Continuous Polling):**
```bash
# Refresh every 2 seconds
watch -n 2 'aws logs tail /aws/lambda/my-function --since 1m'

# With error highlighting
watch -n 2 'aws logs tail /aws/lambda/my-function --since 1m | grep -E "ERROR|Exception" --color=always'
```

**5. Real-Time Debugging Patterns:**

**Pattern 1: Add Debug Logs:**
```python
import json
import os

# Enable verbose logging for debugging
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

def handler(event, context):
    if DEBUG:
        print(f"Event: {json.dumps(event)}")
        print(f"Context: {vars(context)}")

    # Your code
    result = process_event(event)

    if DEBUG:
        print(f"Result: {json.dumps(result)}")

    return result
```

**Pattern 2: Structured Logging:**
```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(json.dumps({
        "event": "handler_start",
        "request_id": context.aws_request_id,
        "path": event.get('path'),
        "method": event.get('httpMethod')
    }))

    # Your code

    logger.info(json.dumps({
        "event": "handler_end",
        "request_id": context.aws_request_id,
        "duration_ms": context.get_remaining_time_in_millis()
    }))
```

**Pattern 3: Remote Debugging (Advanced):**
```python
# WARNING: Only use in dev environments
import debugpy

def handler(event, context):
    # Enable remote debugging on port 5678
    if os.environ.get('ENABLE_DEBUGGER') == 'true':
        debugpy.listen(("0.0.0.0", 5678))
        print("Waiting for debugger attach...")
        debugpy.wait_for_client()

    # Your code with breakpoints
    result = process_event(event)
    return result
```

**6. Log Analysis Shortcuts:**

```bash
# Find all errors in last hour
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --filter-pattern "ERROR" \
  --query 'events[*].message' \
  --output text

# Count error types
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --filter-pattern "ERROR" \
  --query 'events[*].message' \
  --output text | sort | uniq -c | sort -rn

# Find slow invocations (>1000ms)
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --filter-pattern "[..., duration>1000, ...]" \
  --query 'events[*].message'

# Extract REPORT lines for analysis
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --filter-pattern "REPORT" \
  --query 'events[*].message' | \
  grep -oE "Duration: [0-9.]+ ms|Memory Used: [0-9]+ MB"
```

### 6.0 Investigation Tools & Commands

**AWS CLI Commands:**
```bash
# Get function configuration
aws lambda get-function --function-name my-function

# Get recent invocations (CloudWatch Insights)
aws logs insights-query --log-group-name /aws/lambda/my-function \
  --start-time $(date -u -d '1 hour ago' +%s) \
  --end-time $(date -u +%s) \
  --query-string 'fields @timestamp, @message | filter @type = "REPORT"'

# List layers attached to function
aws lambda get-function-configuration --function-name my-function \
  --query 'Layers[*].[Arn, CodeSize]' --output table

# Get concurrent execution metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name ConcurrentExecutions \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time $(date -u -d '1 hour ago' +%s) \
  --end-time $(date -u +%s) \
  --period 60 \
  --statistics Maximum

# Download layer for inspection
aws lambda get-layer-version --layer-name my-layer --version-number 1 \
  --query 'Content.Location' --output text | xargs curl -o layer.zip
```

**Python Troubleshooting Snippets:**
```python
# Memory profiling
import tracemalloc
tracemalloc.start()
# ... your code ...
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f}MB, Peak: {peak / 1024 / 1024:.2f}MB")

# Cold start detection
import os
COLD_START = True

def handler(event, context):
    global COLD_START
    is_cold = COLD_START
    COLD_START = False
    print(f"Cold start: {is_cold}")

# Layer path verification
import sys
print("Python paths:", sys.path)
# Should include /opt/python for layers

# Environment inspection
print("Environment variables:", os.environ)
print("/tmp contents:", os.listdir('/tmp'))
print("Container ID:", os.environ.get('AWS_EXECUTION_ENV'))
```

### 7.0 Agent Invocation

**When to Spawn This Agent:**

Spawn `lambda-troubleshooting-agent` when:
- Lambda function errors or timeouts
- Performance degradation or cold start issues
- API Gateway integration problems
- Layer dependency failures
- Memory or concurrency issues
- VPC connectivity problems
- Need to optimize Lambda configuration

**Workflow:**
```
User reports Lambda issue
     ↓
Spawn lambda-troubleshooting-agent
     ↓
Agent investigates:
  - CloudWatch logs/metrics
  - Function configuration
  - Layer dependencies
  - API Gateway integration
  - VPC configuration
     ↓
Agent provides:
  - Root cause analysis
  - Specific fix recommendations
  - Configuration changes
  - Code optimizations
     ↓
Implement fixes and validate
```

### 8.0 Integration with Infra/SRE Agent

**Handoff Scenarios:**

| Scenario | Lambda Agent | Infra/SRE Agent |
|----------|-------------|-----------------|
| Function errors | ✓ Diagnose | - |
| CDK deployment issues | - | ✓ Fix IaC |
| Monitoring setup | Identify needs | ✓ Implement |
| Performance tuning | ✓ Recommend | - |
| IAM policy fixes | ✓ Identify | ✓ Implement |
| API Gateway config | ✓ Troubleshoot | ✓ Deploy changes |

**Coordination:**
- Lambda agent identifies issues and recommends fixes
- Infra/SRE agent implements infrastructure changes
- Lambda agent validates fixes

### 9.0 Output Format

**Diagnostic Report Template:**
```markdown
# Lambda Function Diagnostic Report

## Function: {function-name}
## Investigation Date: {YYYY-MM-DD}

### 1.0 Issue Summary
[Brief description of reported issue]

### 2.0 Configuration Review
- Runtime: {runtime}
- Memory: {allocated} (Max used: {max_used})
- Timeout: {timeout}s
- Layers: {layer_count}
- VPC: {yes/no}

### 3.0 Metrics Analysis
- Invocations (24h): {count}
- Errors (24h): {count} ({percentage}%)
- Throttles: {count}
- Avg Duration: {duration}ms
- P99 Duration: {p99_duration}ms
- Cold Start Rate: {percentage}%

### 4.0 Root Cause
[Detailed explanation of issue cause]

### 5.0 Recommendations
[1] {recommendation_1}
[2] {recommendation_2}
[3] {recommendation_3}

### 6.0 Immediate Actions
- [ ] {action_1}
- [ ] {action_2}
- [ ] {action_3}

### 7.0 Long-Term Optimizations
- {optimization_1}
- {optimization_2}

### 8.0 Validation Steps
[1] {validation_step_1}
[2] {validation_step_2}
```

### 10.0 Related Documentation

**Internal:**
- `@reference/AWS_SECRETS` - Secrets Manager integration
- `hmode/shared/infra-providers/aws/lambda/` - Lambda standards
- `hmode/guardrails/tech-preferences/infrastructure.json` - Monitoring requirements

**External:**
- [Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [Lambda Quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/)

---

**Agent Version:** 1.0.0
**Last Updated:** 2026-02-11
**Maintained By:** Infrastructure Team
