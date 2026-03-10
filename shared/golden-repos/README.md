# Golden Repos - Project Templates

Gold standard project templates with logging, configuration, testing, and best practices built-in.

**Design System:** All TypeScript templates use shadcn/ui patterns. See `shared/design-system/` for:
- CSS variables and Tailwind config
- React components (Button, Card, Input, etc.)
- Layout components (Header, Sidebar, Footer)
- HTML mockup templates
- Storybook stories

## Quick Start

```bash
# Copy a template to start a new project
cp -r shared/golden-repos/python-fastapi/* prototypes/proto-my-api-xxxxx-001/
cd prototypes/proto-my-api-xxxxx-001/
uv sync  # or npm install for TypeScript projects
```

## Available Templates

### Python Templates

| Template | Use Case | Key Features |
|----------|----------|--------------|
| **[python-script](./python-script/)** | CLI tools, scripts, automation | Typer CLI, Rich output, structlog, pydantic-settings |
| **[python-fastapi](./python-fastapi/)** | REST APIs, backends | FastAPI, middleware, CORS, health checks, OpenAPI docs |
| **[python-general](./python-general/)** | Libraries, shared code | Pydantic models, Result pattern, custom exceptions |

### TypeScript Templates

| Template | Use Case | Key Features |
|----------|----------|--------------|
| **[typescript-nodejs](./typescript-nodejs/)** | Node.js backends, services | Pino logging, Zod config, Vitest, ESM |
| **[typescript-nextjs](./typescript-nextjs/)** | Full-stack web apps | Next.js 14, App Router, Tailwind, React Testing Library |
| **[typescript-react](./typescript-react/)** | Component libraries | Vite library mode, hooks, component patterns |
| **[typescript-vite](./typescript-vite/)** | Vanilla TS apps, SPAs | DOM utils, Result type, debounce/throttle |
| **[typescript-email](./typescript-email/)** | Email templates | React Email, Resend, preview server |
| **[typescript-cdk](./typescript-cdk/)** | AWS Infrastructure | CDK, YAML configs, multi-env, Zod validation |
| **[typescript-expo](./typescript-expo/)** | Mobile apps (iOS/Android) | Expo SDK 52, Expo Router, design system, dark mode |

## What's Included

Every template provides:

- **Multi-Environment Support** - local, dev, integration, stage, prod
- **Structured Logging** - structlog (Python) or Pino (Node.js)
- **Configuration Management** - pydantic-settings (Python) or Zod (TypeScript)
- **Test Setup** - pytest (Python) or Vitest (TypeScript)
- **Type Safety** - mypy strict (Python) or TypeScript strict mode
- **Linting** - ruff (Python) or ESLint (TypeScript)
- **Environment Management** - `.env.example` or YAML config files

## Template Details

### Python Script (`python-script/`)

For CLI tools and automation scripts.

```bash
cd python-script
uv sync
uv run main run --help
uv run pytest
```

**Structure:**
```
python-script/
├── src/
│   ├── config.py         # Pydantic Settings
│   ├── logging_config.py # structlog setup
│   └── main.py           # Typer CLI
├── tests/
├── pyproject.toml
└── .env.example
```

### Python FastAPI (`python-fastapi/`)

For REST APIs and web backends.

```bash
cd python-fastapi
uv sync
uv run uvicorn src.main:app --reload
# Open http://localhost:8000/api/v1/docs
```

**Structure:**
```
python-fastapi/
├── src/
│   ├── routers/          # API endpoints
│   ├── config.py         # Settings
│   ├── middleware.py     # Request logging
│   ├── models.py         # Pydantic models
│   └── main.py           # App factory
├── tests/
└── pyproject.toml
```

### Python General (`python-general/`)

For Python libraries and shared code.

```bash
cd python-general
uv pip install -e ".[dev]"
uv run pytest
```

**Features:**
- `Result[T]` wrapper for error handling
- `BaseEntity` with timestamps
- Utility functions (validation, formatting)

### TypeScript Node.js (`typescript-nodejs/`)

For Node.js backends and services.

```bash
cd typescript-nodejs
npm install
npm run dev
npm test
```

**Features:**
- ESM native with `"type": "module"`
- Pino structured logging
- Retry with exponential backoff

### TypeScript Next.js (`typescript-nextjs/`)

For full-stack web applications.

```bash
cd typescript-nextjs
npm install
npm run dev
# Open http://localhost:3000
```

**Features:**
- Next.js 14 App Router
- Tailwind CSS
- API routes with health check
- Reusable Button component

### TypeScript React (`typescript-react/`)

For React component libraries.

```bash
cd typescript-react
npm install
npm run build
npm test
```

**Features:**
- Vite library mode for npm publishing
- Button, Card, Input components
- useToggle, useDebounce, useLocalStorage hooks

### TypeScript Vite (`typescript-vite/`)

For vanilla TypeScript applications.

```bash
cd typescript-vite
npm install
npm run dev
# Open http://localhost:5173
```

**Features:**
- Type-safe DOM utilities
- Result type pattern
- Debounce/throttle helpers

### TypeScript Email (`typescript-email/`)

For email templates with React Email.

```bash
cd typescript-email
npm install
npm run dev
# Open http://localhost:3001 for preview
```

**Features:**
- React Email components
- Resend API integration
- Welcome, password reset, notification templates

### TypeScript CDK (`typescript-cdk/`)

For AWS infrastructure with CDK.

```bash
cd typescript-cdk
npm install
# Edit config/dev.yml with your settings
npm run deploy:dev
```

**Features:**
- YAML-based environment configs (dev, stage, prod)
- Zod validation for type-safe configuration
- BaseStack pattern with consistent naming/tagging
- Example API Gateway + Lambda stack
- Monitoring stack with SNS alerts

**Structure:**
```
typescript-cdk/
├── bin/
│   └── app.ts              # CDK app entry point
├── lib/
│   ├── constructs/
│   │   └── base-stack.ts   # Base stack pattern
│   └── stacks/
│       ├── api-stack.ts    # Example API stack
│       └── monitoring-stack.ts
├── config/
│   ├── schema.ts           # Zod validation
│   ├── loader.ts           # Config utilities
│   ├── dev.yml             # Development config
│   ├── stage.yml           # Staging config
│   └── prod.yml            # Production config
└── test/
```

### TypeScript Expo (`typescript-expo/`)

For React Native mobile apps with Expo.

```bash
cd typescript-expo
npm install
npm run start
# Press 'i' for iOS, 'a' for Android, 'w' for web
```

**Features:**
- Expo SDK 52 with New Architecture
- Expo Router file-based navigation
- Native design system (Button, Card, Input, Badge, Text)
- Dark mode with theme context
- Custom hooks (useDebounce, useToggle, useAsyncStorage)
- Jest + React Native Testing Library

**Structure:**
```
typescript-expo/
├── app/                    # Expo Router screens
│   ├── _layout.tsx         # Root layout
│   └── (tabs)/             # Tab navigation
├── src/
│   ├── components/
│   │   ├── ui/             # Design system
│   │   └── layout/         # Layout components
│   ├── hooks/              # Custom hooks
│   ├── lib/                # Theme system
│   ├── config/             # Zod-validated config
│   └── constants/          # App constants
├── tests/
└── app.json
```

## Best Practices

### Configuration

All templates use environment variables with validation:

```python
# Python (pydantic-settings)
from src.config import get_settings
settings = get_settings()
```

```typescript
// TypeScript (Zod)
import { getConfig } from './config';
const config = getConfig();
```

### Logging

Structured logging with context:

```python
# Python (structlog)
from src.logging_config import get_logger
log = get_logger("module_name")
log.info("Event happened", user_id=123, action="login")
```

```typescript
// TypeScript (Pino)
import { getLogger } from './logger';
const log = getLogger('module');
log.info({ userId: 123, action: 'login' }, 'Event happened');
```

### Testing

Run tests with coverage:

```bash
# Python
uv run pytest --cov=src --cov-report=term-missing

# TypeScript
npm run test:coverage
```

## Adding New Templates

1. Create directory in `shared/golden-repos/`
2. Include standard files:
   - `README.md` with quick start
   - Configuration with env validation
   - Structured logging setup
   - Test configuration
   - `.env.example`
   - `.gitignore`
3. Update this README with new template
4. Update `.claude/docs/processes/PHASE_8_IMPLEMENTATION.md` table

## Integration with SDLC

These templates are integrated into Phase 8 (Implementation) of the SDLC. When starting implementation:

1. Identify project type from design docs
2. Copy appropriate golden repo template
3. Customize for specific requirements
4. Run tests to verify setup works
5. Begin TDD implementation

See `.claude/docs/processes/PHASE_8_IMPLEMENTATION.md` for full workflow.
