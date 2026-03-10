# Testing Standards

<!-- File UUID: 1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d -->

Standard configurations and stub tests for Protoflow projects.

## Quick Start

1. **→ [TESTING_SOP.md](./TESTING_SOP.md)** - Framework setup (pytest, Vitest, Playwright, Cucumber)
2. **→ [CICD_TESTING_GUIDE.md](./CICD_TESTING_GUIDE.md)** - CI/CD integration & Makefile targets
3. **→ [SMOKE_TEST_PATTERN.md](./SMOKE_TEST_PATTERN.md)** - Post-deploy verification

## Contents

```
testing/
├── README.md                    # This file
├── TESTING_SOP.md               # ⭐ Framework setup (pytest, Vitest, Playwright)
├── CICD_TESTING_GUIDE.md        # ⭐ CI/CD integration & Makefile targets
├── SMOKE_TEST_PATTERN.md        # Post-deploy smoke test pattern
├── BDD_TESTING_GUIDE.md         # Cucumber + Playwright BDD testing
├── test-accounts.json           # Test account configuration
├── templates/                   # Ready-to-use templates
│   ├── Makefile.testing.mk      # Makefile test targets (include or copy)
│   ├── github-actions.yml       # GitHub Actions workflow
│   ├── gitlab-ci.yml            # GitLab CI configuration
│   └── buildspec.yml            # AWS CodeBuild specification
└── e2e/
    └── observability/
        ├── README.md            # Observability testing guide
        ├── cloudwatch.spec.ts   # CloudWatch E2E stub tests
        └── xray.spec.ts         # X-Ray E2E stub tests
```

## Required Makefile Targets

Every project MUST have these test targets in their Makefile:

```bash
make test           # Run ALL tests (unit + e2e)
make test-unit      # Run unit tests only
make test-e2e       # Run E2E tests
make test-smoke     # Run post-deploy smoke tests
make test-coverage  # Run tests with coverage report
make test-ci        # Run CI tests (lint + coverage + e2e)
make lint           # Run linter
```

Use `templates/Makefile.testing.mk` as a starting point.

## Required CI/CD Build File

Every project MUST include a CI/CD build file for at least one platform:

| Platform | Template | Copy To |
|----------|----------|---------|
| GitHub Actions | `templates/github-actions.yml` | `.github/workflows/test.yml` |
| GitLab CI | `templates/gitlab-ci.yml` | `.gitlab-ci.yml` |
| AWS CodeBuild | `templates/buildspec.yml` | `buildspec.yml` |

## Parameterization (MANDATORY)

All test values MUST be parameterized via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `TEST_BASE_URL` | `http://localhost:3000` | App URL for E2E tests |
| `TEST_COVERAGE_THRESHOLD` | `70` | Minimum coverage % |
| `TEST_TIMEOUT` | `30000` | Timeout in ms |
| `TEST_FAIL_FAST` | `true` | Stop on first failure |
| `EXPECTED_GIT_HASH` | Current HEAD | For smoke test verification |

See **[CICD_TESTING_GUIDE.md](./CICD_TESTING_GUIDE.md)** for full details.

## Testing SOP

See **[TESTING_SOP.md](./TESTING_SOP.md)** for:
- pytest setup and examples (Python)
- Vitest setup and examples (TypeScript)
- Playwright E2E testing
- Cucumber BDD testing
- Watch modes and UI tools
- Common patterns and troubleshooting

## BDD Testing (Natural Language)

For stakeholder-readable tests with shareable HTML reports, see **[BDD_TESTING_GUIDE.md](./BDD_TESTING_GUIDE.md)**.

Uses:
- **Cucumber** - Gherkin natural language syntax
- **Playwright** - Browser automation
- **S3** - Report hosting for stakeholders

## Test Accounts

The `test-accounts.json` file defines standard test accounts and environments:

- **AWS Accounts** - IAM roles for E2E testing with appropriate permissions
- **Application Users** - Test users for different access levels (admin, user, readonly)
- **Environments** - Local, dev, staging configuration

### Usage

```typescript
import testAccounts from '@shared/standards/testing/test-accounts.json';

const adminUser = testAccounts.accounts.application.users.admin;
const username = process.env[adminUser.username_env];
const password = process.env[adminUser.password_env];
```

## E2E Testing Requirements

All projects with AWS infrastructure MUST include:

1. **Observability Tests** - Verify CloudWatch and X-Ray integration
2. **Smoke Tests** - Basic application health checks
3. **User Journey Tests** - Critical path testing

## Framework Preference

Per `.guardrails/tech-preferences/testing.json`:

1. **Playwright** (rank 1) - All E2E testing
2. **Jest** (rank 1) - Unit and integration testing
3. **pytest** (rank 3) - Python projects

## Related Documentation

- `/.guardrails/tech-preferences/testing.json` - Testing framework preferences
- `/.guardrails/tech-preferences/infrastructure.json` - Observability requirements
- `/shared/golden-repos/*/e2e/` - Example E2E tests per framework
