# Serverless Starter

A full-stack serverless starter template with AWS CDK infrastructure, featuring:

- **React 19** with Vite frontend
- **Tailwind CSS** with shadcn/ui components
- **auth.b.lfg.new** Cognito integration (shared user pool)
- **API Gateway** with CloudWatch logging and X-Ray tracing
- **Lambda Functions** (TypeScript + Python)
- **DynamoDB** with single-table design
- **Bedrock AI** integration with Claude
- **Light/Dark mode** toggle

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (Vite + React 19)                   │
│  Tailwind CSS + shadcn/ui + AWS Amplify Auth (auth.b.lfg.new)   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API Gateway (REST)                           │
│  CloudWatch Logs │ X-Ray Tracing │ Cognito Authorizer           │
└─────────────────────────────────────────────────────────────────┘
                    │                   │
                    ▼                   ▼
┌──────────────────────────┐ ┌──────────────────────────────────┐
│   Lambda (TypeScript)    │ │      Lambda (Python)             │
│  - /hello                │ │  - /ai/chat (Bedrock Claude)     │
│  - /items CRUD           │ │  - /ai/embeddings (Titan)        │
│  - /health               │ │  - Powertools (Logs/Metrics)     │
└──────────────────────────┘ └──────────────────────────────────┘
            │                            │
            └────────────┬───────────────┘
                         ▼
              ┌─────────────────────┐
              │      DynamoDB       │
              │  Single-table design│
              └─────────────────────┘
```

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- AWS CLI configured
- AWS CDK CLI (`npm install -g aws-cdk`)

### Installation

```bash
# Clone/copy this template
cp -r shared/golden-repos/typescript-serverless-starter my-project
cd my-project

# Install dependencies
make install

# Copy environment template
cp .env.example .env
# Edit .env with your AWS settings
```

### Development

```bash
# Start frontend dev server
make dev

# Build backend (in another terminal)
make build-backend
```

### Deployment

```bash
# First time: Bootstrap CDK
make infra-bootstrap

# Deploy infrastructure (uses auth.b.lfg.new by default)
make infra-deploy

# Update frontend environment from CDK outputs
make update-frontend-env

# Start frontend with API connection
make dev
```

## Authentication

### Default: Shared auth.b.lfg.new User Pool

By default, this starter integrates with the shared `auth.b.lfg.new` Cognito user pool:

- **User Pool ID**: `us-east-1_p0fQSZLEG`
- **Domain**: `auth.b.lfg.new`
- **Region**: `us-east-1`

This allows you to share authentication across multiple applications.

### Creating a New User Pool

To create a dedicated user pool instead:

```bash
export COGNITO_CREATE_NEW=true
make infra-deploy
```

### Using a Different Existing Pool

```bash
export COGNITO_USER_POOL_ID=us-east-1_xxxxxxxxx
export COGNITO_USER_POOL_ARN=arn:aws:cognito-idp:us-east-1:123456789012:userpool/us-east-1_xxxxxxxxx
make infra-deploy
```

## Project Structure

```
.
├── Makefile                 # Build and deployment commands
├── package.json             # Root workspace configuration
├── .env.example             # Environment template
│
├── infra/                   # AWS CDK Infrastructure
│   ├── app.ts               # CDK app entry point
│   ├── stacks/
│   │   └── serverless-stack.ts  # Main stack definition
│   └── deploys/             # Deployment history (Capistrano-style)
│       ├── releases/        # Timestamped releases
│       └── current -> ...   # Symlink to active release
│
├── backend/                 # TypeScript Lambda
│   └── src/
│       ├── handlers/
│       │   └── hello.ts     # Main handler
│       └── lib/
│           └── dynamodb.ts  # DynamoDB utilities
│
├── backend-python/          # Python Lambda
│   └── src/
│       ├── handlers/
│       │   └── bedrock_handler.py  # AI endpoints
│       ├── lib/
│       │   └── secrets.py   # Secrets Manager utilities
│       └── models/
│           └── requests.py  # Pydantic models
│
└── frontend/                # Vite + React 19
    └── src/
        ├── components/
        │   ├── ui/          # shadcn/ui components
        │   ├── ThemeToggle.tsx
        │   └── AuthForms.tsx
        ├── hooks/
        │   ├── useAuth.ts
        │   └── useTheme.ts
        ├── lib/
        │   ├── amplify.ts   # Cognito configuration (auth.b.lfg.new)
        │   ├── api.ts       # API client
        │   └── utils.ts     # Tailwind utilities
        ├── pages/
        │   └── HomePage.tsx
        └── styles/
            └── globals.css  # Tailwind + CSS variables
```

## API Endpoints

### Public (No Auth)
- `GET /health` - Health check
- `GET /hello` - Hello world
- `GET /ai/health` - AI service health

### Protected (Cognito Auth)
- `POST /hello` - Personalized hello
- `GET /items` - List items
- `POST /items` - Create item
- `GET /items/{id}` - Get item
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item
- `POST /ai/chat` - Chat with Claude
- `POST /ai/embeddings` - Generate embeddings

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `AWS_PROFILE` | AWS CLI profile to use |
| `AWS_REGION` | AWS region (default: us-east-1) |
| `STAGE_NAME` | Deployment stage (dev/staging/prod) |
| `COGNITO_CREATE_NEW` | Set to `true` to create new user pool |
| `COGNITO_USER_POOL_ID` | User pool ID (default: auth.b.lfg.new) |
| `COGNITO_USER_POOL_ARN` | User pool ARN |
| `COGNITO_USER_POOL_CLIENT_ID` | App client ID |

### Frontend Environment

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | API Gateway URL |
| `VITE_USER_POOL_ID` | Cognito User Pool ID (default: us-east-1_p0fQSZLEG) |
| `VITE_USER_POOL_CLIENT_ID` | Cognito Client ID (required) |
| `VITE_COGNITO_DOMAIN` | Hosted UI domain (default: auth.b.lfg.new) |

## Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Install all dependencies |
| `make dev` | Start frontend dev server |
| `make build` | Build all packages |
| `make test` | Run all tests |
| `make lint` | Run linters |
| `make infra-bootstrap` | Bootstrap CDK |
| `make infra-deploy` | Deploy to AWS |
| `make infra-destroy` | Destroy infrastructure |
| `make infra-diff` | Show pending changes |
| `make outputs` | Show deployment outputs |
| `make update-frontend-env` | Update frontend .env |

## Tech Stack

### Frontend
- **React 19** - Latest React with concurrent features
- **Vite 6** - Fast build tool
- **Tailwind CSS 3.4** - Utility-first CSS
- **shadcn/ui** - Accessible component library
- **AWS Amplify** - Cognito authentication

### Backend
- **TypeScript Lambda** - Node.js 20 runtime
- **Python Lambda** - Python 3.11 with Powertools
- **API Gateway** - REST API with X-Ray
- **DynamoDB** - Single-table design
- **Secrets Manager** - Secure credential storage

### Infrastructure
- **AWS CDK** - Infrastructure as code
- **CloudWatch** - Logging and metrics
- **X-Ray** - Distributed tracing
- **Cognito** - Authentication (auth.b.lfg.new)

## Extending

### Adding New Lambda Endpoints

1. Add handler in `backend/src/handlers/`
2. Update API Gateway routes in `infra/stacks/serverless-stack.ts`
3. Add API client method in `frontend/src/lib/api.ts`

### Adding shadcn/ui Components

Components are manually added following the shadcn/ui patterns. Add new components to `frontend/src/components/ui/`.

### Python Lambda Dependencies

Add to `backend-python/requirements.txt` and rebuild.

## License

MIT
