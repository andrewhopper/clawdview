<!-- File UUID: 7c9f3a2e-1d5b-4e8f-9a3c-6f2d8e4b7a1c -->

# Local Development Environment Agent

**Agent Type:** `local-dev`

**Purpose:** Manage local development environments using Docker, Docker Compose, and AWS SAM CLI for running Lambda functions and services locally during development.

## Overview

The Local Dev Environment agent helps developers run applications locally before deploying to AWS. It supports two primary approaches:
1. **AWS SAM CLI** - Official AWS tool for local Lambda development, API Gateway simulation, and event-driven testing
2. **Docker/Docker Compose** - Container-based local development for any application type

## When to Invoke

Spawn this agent when:
- Running Lambda functions locally for testing
- Starting a local API Gateway to test HTTP-triggered functions
- Generating sample events for Lambda invocations
- Managing Docker containers for local development
- Setting up local development environments with multiple services
- Debugging Lambda functions with step-through debugging
- Hot-reloading code during development
- Managing environment variables and secrets for local testing
- Simulating AWS services locally (DynamoDB Local, LocalStack)

## Agent Capabilities

### 1. AWS SAM CLI Operations

**Building and Packaging**
```bash
# Build SAM application (creates .aws-sam/build directory)
sam build

# Build with specific container image (for native dependencies)
sam build --use-container

# Build specific function only
sam build FunctionName

# Build with parallel builds (faster for multi-function stacks)
sam build --parallel
```

**Local Function Invocation**
```bash
# Invoke function once with event file
sam local invoke "FunctionName" -e event.json

# Invoke with inline JSON event
sam local invoke "FunctionName" -e '{"key": "value"}'

# Invoke with environment variables
sam local invoke "FunctionName" -e event.json --env-vars env.json

# Invoke with specific AWS profile
sam local invoke "FunctionName" -e event.json --profile my-profile

# Invoke with debug mode (step-through debugging)
sam local invoke "FunctionName" -e event.json -d 5858
```

**Local API Gateway**
```bash
# Start local API Gateway server
sam local start-api

# Start on specific port
sam local start-api --port 3000

# Start with hot reload (watch for code changes)
sam local start-api --warm-containers EAGER

# Start with specific template
sam local start-api --template template.yaml

# Start with environment variables
sam local start-api --env-vars env.json
```

**Local Lambda Endpoint**
```bash
# Start Lambda endpoint (for direct invocations without API Gateway)
sam local start-lambda

# Start on specific port
sam local start-lambda --port 3001
```

**Generate Sample Events**
```bash
# List all available event types
sam local generate-event --help

# Generate API Gateway event
sam local generate-event apigateway aws-proxy > event.json

# Generate S3 put event
sam local generate-event s3 put > event.json

# Generate DynamoDB stream event
sam local generate-event dynamodb update > event.json

# Generate SQS event
sam local generate-event sqs receive-message > event.json

# Generate CloudWatch scheduled event
sam local generate-event cloudwatch scheduled-event > event.json

# Generate SNS notification
sam local generate-event sns notification > event.json

# Generate Cognito event
sam local generate-event cognito-idp create-auth-challenge > event.json
```

**Viewing Logs**
```bash
# View Lambda logs from CloudWatch (deployed functions)
sam logs -n FunctionName --stack-name my-stack

# Tail logs in real-time
sam logs -n FunctionName --stack-name my-stack --tail

# Filter logs by time
sam logs -n FunctionName --stack-name my-stack --start-time "5 minutes ago"
```

### 2. Docker Operations

**Container Management**
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Start a container
docker start container_name

# Stop a container
docker stop container_name

# Remove a container
docker rm container_name

# View container logs
docker logs container_name

# Follow container logs
docker logs -f container_name

# Execute command in running container
docker exec -it container_name bash
```

**Image Management**
```bash
# List images
docker images

# Build image from Dockerfile
docker build -t image_name .

# Build with no cache
docker build --no-cache -t image_name .

# Remove image
docker rmi image_name

# Pull image from registry
docker pull image_name:tag
```

### 3. Docker Compose Operations

**Service Lifecycle**
```bash
# Start all services in background
docker-compose up -d

# Start specific services
docker-compose up -d service1 service2

# Start with build (rebuild images)
docker-compose up -d --build

# Start and remove orphan containers
docker-compose up -d --remove-orphans

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all

# Restart specific service
docker-compose restart service_name
```

**Monitoring and Debugging**
```bash
# View logs for all services
docker-compose logs

# Follow logs for specific service
docker-compose logs -f service_name

# View running services
docker-compose ps

# Execute command in service container
docker-compose exec service_name bash

# View service resource usage
docker stats
```

**Configuration**
```bash
# Validate compose file
docker-compose config

# Use specific compose file
docker-compose -f docker-compose.dev.yml up -d

# Use multiple compose files (merged)
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### 4. Local AWS Service Simulation

**DynamoDB Local**
```bash
# Start DynamoDB Local with Docker
docker run -p 8000:8000 amazon/dynamodb-local

# Create table on DynamoDB Local
aws dynamodb create-table \
  --endpoint-url http://localhost:8000 \
  --table-name my-table \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

**LocalStack (Multiple AWS Services)**
```bash
# Start LocalStack with Docker Compose
# docker-compose.yml:
services:
  localstack:
    image: localstack/localstack
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3,sqs,dynamodb,lambda
      - DEBUG=1
    volumes:
      - "./localstack:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"

# Use LocalStack endpoints
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-bucket
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name my-queue
```

### 5. Environment Management

**Environment Variables File (env.json)**
```json
{
  "FunctionName": {
    "TABLE_NAME": "my-table",
    "STAGE": "local",
    "AWS_REGION": "us-east-1",
    "LOG_LEVEL": "DEBUG"
  }
}
```

**.env File for Docker Compose**
```env
# .env
DATABASE_URL=postgres://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379
API_KEY=local-dev-key
DEBUG=true
```

**Secrets Management for Local Dev**
```bash
# Create local secrets file (NOT committed to git)
cat > .env.local << EOF
AWS_ACCESS_KEY_ID=local-key
AWS_SECRET_ACCESS_KEY=local-secret
DATABASE_PASSWORD=local-password
EOF

# Reference in docker-compose
# docker-compose.yml:
services:
  app:
    env_file:
      - .env
      - .env.local
```

## Workflow Visualizations

### SAM Local Development Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  SAM LOCAL DEVELOPMENT WORKFLOW                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Developer Request: "Test Lambda function locally"              │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────┐                   │
│  │  1. VERIFY PREREQUISITES                 │                   │
│  │  - Docker running                        │                   │
│  │  - SAM CLI installed                     │                   │
│  │  - template.yaml exists                  │                   │
│  │  - AWS credentials configured            │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  2. BUILD APPLICATION                    │                   │
│  │  - sam build                             │                   │
│  │  - Creates .aws-sam/build directory      │                   │
│  │  - Downloads dependencies                │                   │
│  │  - Packages code                         │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  3. GENERATE TEST EVENT                  │                   │
│  │  - sam local generate-event [type]       │                   │
│  │  - Customize event payload               │                   │
│  │  - Save to event.json                    │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ├────────────────────────────────────┐                  │
│         │                                    │                  │
│         ▼                                    ▼                  │
│  ┌─────────────────────┐      ┌─────────────────────────┐      │
│  │  4A. INVOKE ONCE    │  OR  │  4B. START LOCAL API    │      │
│  │  sam local invoke   │      │  sam local start-api    │      │
│  │  -e event.json      │      │  --warm-containers      │      │
│  │                     │      │  (hot reload enabled)   │      │
│  └──────┬──────────────┘      └──────┬──────────────────┘      │
│         │                            │                          │
│         ▼                            ▼                          │
│  ┌─────────────────────────────────────────┐                   │
│  │  5. TEST AND ITERATE                     │                   │
│  │  - View function output                  │                   │
│  │  - Check logs for errors                 │                   │
│  │  - Modify code (hot reload active)       │                   │
│  │  - Re-test until working                 │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  6. READY FOR DEPLOYMENT                 │                   │
│  │  - Local testing complete                │                   │
│  │  - Hand off to infra-sre agent           │                   │
│  │  - or: sam deploy --guided               │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Docker Compose Development Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                DOCKER COMPOSE DEVELOPMENT WORKFLOW               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Developer Request: "Run services locally"                      │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────┐                   │
│  │  1. REVIEW COMPOSE FILE                  │                   │
│  │  - docker-compose.yml                    │                   │
│  │  - docker-compose.override.yml (local)   │                   │
│  │  - Environment files (.env)              │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  2. START DEPENDENCIES                   │                   │
│  │  - Database (Postgres, MySQL, etc.)      │                   │
│  │  - Cache (Redis, Memcached)              │                   │
│  │  - Message Queue (RabbitMQ, LocalStack)  │                   │
│  │  - docker-compose up -d db redis         │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  3. WAIT FOR HEALTHY STATE               │                   │
│  │  - Health checks pass                    │                   │
│  │  - Services accepting connections        │                   │
│  │  - docker-compose ps                     │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  4. START APPLICATION                    │                   │
│  │  - docker-compose up -d app              │                   │
│  │  - OR run locally with hot reload        │                   │
│  │  - Connect to containerized deps         │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  5. MONITOR AND DEBUG                    │                   │
│  │  - docker-compose logs -f app            │                   │
│  │  - docker-compose exec app bash          │                   │
│  │  - docker stats                          │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  6. CLEANUP                              │                   │
│  │  - docker-compose down                   │                   │
│  │  - docker-compose down -v (with volumes) │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Common Development Scenarios

### Scenario 1: Testing Lambda with API Gateway

**Goal:** Test an HTTP-triggered Lambda function locally

```bash
# Step 1: Build the SAM application
sam build

# Step 2: Start local API Gateway
sam local start-api --port 3000 --warm-containers EAGER

# Step 3: Test with curl (in another terminal)
curl http://localhost:3000/hello
curl -X POST http://localhost:3000/items -d '{"name": "test"}'

# Step 4: View logs in the SAM terminal
# Hot reload: edit code, save, make another request
```

### Scenario 2: Testing Lambda with S3 Events

**Goal:** Test a Lambda triggered by S3 uploads

```bash
# Step 1: Generate S3 event
sam local generate-event s3 put \
  --bucket my-bucket \
  --key uploads/test.json > event.json

# Step 2: Customize event payload if needed
# Edit event.json to match your test case

# Step 3: Invoke function
sam local invoke "ProcessS3Upload" -e event.json

# Step 4: Check output and logs
```

### Scenario 3: Testing Lambda with DynamoDB Streams

**Goal:** Test a Lambda triggered by DynamoDB changes

```bash
# Step 1: Generate DynamoDB stream event
sam local generate-event dynamodb update > event.json

# Step 2: Customize the record
# Edit event.json to match your table schema

# Step 3: Invoke function
sam local invoke "ProcessDynamoDBStream" -e event.json
```

### Scenario 4: Full Stack with Docker Compose

**Goal:** Run full application stack locally

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./api/src:/app/src  # Hot reload

  db:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Stop everything
docker-compose down
```

### Scenario 5: Debugging Lambda with Step-Through

**Goal:** Debug Lambda function with breakpoints

```bash
# Step 1: Start function in debug mode
sam local invoke "FunctionName" -e event.json -d 5858

# Step 2: Connect debugger
# VS Code: Create launch.json with:
{
  "type": "node",
  "request": "attach",
  "name": "Attach to SAM CLI",
  "port": 5858,
  "localRoot": "${workspaceFolder}/src",
  "remoteRoot": "/var/task"
}

# For Python:
sam local invoke "FunctionName" -e event.json -d 5890 --debugger-path ~/.pyenv/versions/3.11.0/lib/python3.11/site-packages
```

## Integration with Other Agents

### With Infra/SRE Agent
- Local Dev agent tests locally
- Infra/SRE agent deploys to AWS
- Handoff: "Local testing complete, ready for deployment"

### With Lambda Troubleshooting Agent
- Local Dev agent for pre-deployment testing
- Lambda Troubleshooting agent for production issues
- Share event payloads for reproducing production issues locally

### With Domain Modeling Agent
- Domain agent defines data models
- Local Dev agent sets up local databases matching production schema
- Test with realistic data structures

## Sample template.yaml

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: SAM application for local development

Globals:
  Function:
    Timeout: 30
    MemorySize: 256
    Runtime: python3.12
    Architectures:
      - x86_64
    Environment:
      Variables:
        LOG_LEVEL: DEBUG
        STAGE: local

Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      CodeUri: src/
      Description: Hello World function
      Events:
        HelloApi:
          Type: Api
          Properties:
            Path: /hello
            Method: get
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref ItemsTable

  ItemsFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: items.lambda_handler
      CodeUri: src/
      Description: Items CRUD function
      Events:
        GetItems:
          Type: Api
          Properties:
            Path: /items
            Method: get
        CreateItem:
          Type: Api
          Properties:
            Path: /items
            Method: post
      Environment:
        Variables:
          TABLE_NAME: !Ref ItemsTable

  ItemsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: items-local
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST

Outputs:
  HelloApi:
    Description: API Gateway endpoint URL
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/hello/"
```

## Troubleshooting Guide

### Issue 1: SAM Build Fails

**Symptom:** `sam build` fails with dependency errors

**Solutions:**
```bash
# Use container for native dependencies
sam build --use-container

# Clear build cache
rm -rf .aws-sam/build
sam build

# Check runtime compatibility
sam build --parameter-overrides Runtime=python3.12
```

### Issue 2: Docker Not Running

**Symptom:** SAM commands fail with Docker errors

**Solution:**
```bash
# Check Docker status
docker info

# Start Docker Desktop (macOS)
open -a Docker

# Wait for Docker to be ready
until docker info > /dev/null 2>&1; do sleep 1; done
```

### Issue 3: Port Already in Use

**Symptom:** `sam local start-api` fails with port binding error

**Solution:**
```bash
# Find process using port
lsof -i :3000

# Kill process
kill -9 <PID>

# Or use different port
sam local start-api --port 3001
```

### Issue 4: Hot Reload Not Working

**Symptom:** Code changes not reflected in local API

**Solution:**
```bash
# Restart with warm containers
sam local start-api --warm-containers EAGER

# Or rebuild and restart
sam build && sam local start-api
```

### Issue 5: Environment Variables Not Set

**Symptom:** Function fails due to missing environment variables

**Solution:**
```bash
# Create env.json file
cat > env.json << EOF
{
  "FunctionName": {
    "TABLE_NAME": "items-local",
    "LOG_LEVEL": "DEBUG"
  }
}
EOF

# Use with invoke
sam local invoke "FunctionName" -e event.json --env-vars env.json

# Use with start-api
sam local start-api --env-vars env.json
```

### Issue 6: DynamoDB Local Connection

**Symptom:** Function can't connect to DynamoDB Local

**Solution:**
```bash
# Start DynamoDB Local in Docker network
docker network create sam-local
docker run -d --network sam-local --name dynamodb -p 8000:8000 amazon/dynamodb-local

# Configure SAM to use Docker network
sam local start-api --docker-network sam-local

# Set endpoint in function
# AWS_SAM_LOCAL=true -> detect and use http://dynamodb:8000
```

## Best Practices

1. **Always test locally before deploying** - Catch errors early
2. **Use `--warm-containers EAGER`** for faster iteration during development
3. **Generate events for accurate testing** - Use `sam local generate-event`
4. **Match production environment** - Use same runtime versions, memory settings
5. **Use environment files** - Separate local config from production
6. **Don't commit secrets** - Use `.env.local` files in `.gitignore`
7. **Use Docker Compose for dependencies** - Database, Redis, etc.
8. **Implement health checks** - Ensure services are ready before testing
9. **Clean up regularly** - `docker-compose down -v` to remove volumes
10. **Document local setup** - README.md with quick start instructions

## Required Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| Docker | Container runtime | `brew install --cask docker` |
| Docker Compose | Multi-container orchestration | Included with Docker Desktop |
| AWS SAM CLI | Lambda local development | `brew install aws-sam-cli` |
| AWS CLI | AWS service interaction | `brew install awscli` |

## References

- [AWS SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)
- [SAM Local Testing Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-invoke.html)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [DynamoDB Local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
- [LocalStack](https://localstack.cloud/)
