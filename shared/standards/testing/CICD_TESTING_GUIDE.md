# CI/CD Testing Integration Guide

<!-- File UUID: 8f3a2c1e-4b7d-4e9a-b5c8-1d2e3f4a5b6c -->

Every project MUST include a CI/CD build file and Makefile targets for testing. This ensures consistent test execution across local development and CI environments.

## 1.0 Core Principles

### 1.1 Parameterization (MANDATORY)

**All test configuration values MUST be parameterized.** No hardcoded values.

```bash
# WRONG - hardcoded values
BASE_URL="https://myapp.example.com"
COVERAGE_THRESHOLD=70

# CORRECT - parameterized with defaults
BASE_URL="${TEST_BASE_URL:-http://localhost:3000}"
COVERAGE_THRESHOLD="${TEST_COVERAGE_THRESHOLD:-70}"
```

### 1.2 Required Parameters

Every project must support these environment variables:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `TEST_BASE_URL` | Application URL for E2E tests | `http://localhost:3000` |
| `TEST_COVERAGE_THRESHOLD` | Minimum coverage percentage | `70` |
| `TEST_TIMEOUT` | Test timeout in milliseconds | `30000` |
| `TEST_RETRIES` | Number of retries on failure (CI only) | `2` |
| `TEST_PARALLEL` | Run tests in parallel | `true` |
| `TEST_FAIL_FAST` | Stop on first failure | `true` |
| `TEST_REPORT_DIR` | Directory for test reports | `./test-reports` |
| `EXPECTED_GIT_HASH` | Expected deployed git hash (smoke tests) | Current HEAD |

### 1.3 Makefile as Single Interface

CI/CD pipelines MUST call Makefile targets, not raw test commands. This ensures:
- Same commands work locally and in CI
- Single source of truth for test execution
- Easy to update test commands without changing CI config

## 2.0 Required Makefile Targets

Every project MUST implement these targets:

```makefile
# ============================================================================
# TESTING TARGETS (Required)
# ============================================================================

# Run ALL tests (unit + integration + e2e)
test: test-unit test-e2e
	@echo "All tests passed"

# Run unit tests only
test-unit:
	@echo "Running unit tests..."
	# Framework-specific command here

# Run end-to-end/integration tests
test-e2e:
	@echo "Running E2E tests..."
	# Framework-specific command here

# Run post-deploy smoke tests (requires TEST_BASE_URL)
test-smoke:
	@echo "Running smoke tests against $(TEST_BASE_URL)..."
	# Smoke test command here

# Run tests with coverage report
test-coverage:
	@echo "Running tests with coverage..."
	# Coverage command here

# Run tests in CI mode (stricter settings)
test-ci: lint test-coverage
	@echo "CI tests complete"

# Linting (runs before test-ci)
lint:
	@echo "Running linter..."
	# Lint command here
```

## 3.0 CI/CD Platform Templates

### 3.1 Supported Platforms

| Platform | Config File | Runner |
|----------|-------------|--------|
| GitHub Actions | `.github/workflows/test.yml` | GitHub-hosted or self-hosted |
| GitLab CI | `.gitlab-ci.yml` | GitLab runners |
| AWS CodeBuild | `buildspec.yml` | CodeBuild compute |

### 3.2 Platform Selection

Choose based on:
- **GitHub Actions** - Default for GitHub-hosted repos (most projects)
- **GitLab CI** - GitLab-hosted repos
- **AWS CodeBuild** - AWS-native deployments, complex build requirements

## 4.0 GitHub Actions Template

Location: `.github/workflows/test.yml`

```yaml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  TEST_COVERAGE_THRESHOLD: ${{ vars.TEST_COVERAGE_THRESHOLD || '70' }}
  TEST_TIMEOUT: ${{ vars.TEST_TIMEOUT || '30000' }}
  TEST_RETRIES: ${{ vars.TEST_RETRIES || '2' }}
  TEST_FAIL_FAST: ${{ vars.TEST_FAIL_FAST || 'true' }}

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: make lint

      - name: Run tests with coverage
        run: make test-ci
        env:
          CI: true

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-report
          path: ${{ env.TEST_REPORT_DIR || './test-reports' }}

  smoke-test:
    needs: [test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run smoke tests
        run: make test-smoke
        env:
          TEST_BASE_URL: ${{ vars.PRODUCTION_URL }}
          EXPECTED_GIT_HASH: ${{ github.sha }}
```

## 5.0 GitLab CI Template

Location: `.gitlab-ci.yml`

```yaml
stages:
  - lint
  - test
  - smoke

variables:
  TEST_COVERAGE_THRESHOLD: ${TEST_COVERAGE_THRESHOLD:-70}
  TEST_TIMEOUT: ${TEST_TIMEOUT:-30000}
  TEST_RETRIES: ${TEST_RETRIES:-2}
  TEST_FAIL_FAST: ${TEST_FAIL_FAST:-true}
  TEST_REPORT_DIR: ${TEST_REPORT_DIR:-./test-reports}

.node-setup:
  image: node:20
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - npm ci

lint:
  extends: .node-setup
  stage: lint
  script:
    - make lint

test-unit:
  extends: .node-setup
  stage: test
  script:
    - make test-unit
  artifacts:
    when: always
    reports:
      junit: $TEST_REPORT_DIR/junit.xml
    paths:
      - $TEST_REPORT_DIR/

test-coverage:
  extends: .node-setup
  stage: test
  script:
    - make test-coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    when: always
    paths:
      - $TEST_REPORT_DIR/coverage/

smoke-test:
  extends: .node-setup
  stage: smoke
  only:
    - main
  script:
    - make test-smoke
  variables:
    TEST_BASE_URL: $PRODUCTION_URL
    EXPECTED_GIT_HASH: $CI_COMMIT_SHA
```

## 6.0 AWS CodeBuild Template

Location: `buildspec.yml`

```yaml
version: 0.2

env:
  variables:
    TEST_COVERAGE_THRESHOLD: "70"
    TEST_TIMEOUT: "30000"
    TEST_RETRIES: "2"
    TEST_FAIL_FAST: "true"
    TEST_REPORT_DIR: "./test-reports"
  parameter-store:
    PRODUCTION_URL: "/app/production-url"

phases:
  install:
    runtime-versions:
      nodejs: 20
    commands:
      - npm ci

  pre_build:
    commands:
      - echo "Running linter..."
      - make lint

  build:
    commands:
      - echo "Running tests..."
      - make test-ci

  post_build:
    commands:
      - |
        if [ "$CODEBUILD_BUILD_SUCCEEDING" = "1" ] && [ "$CODEBUILD_WEBHOOK_TRIGGER" = "branch/main" ]; then
          echo "Running smoke tests..."
          export TEST_BASE_URL=$PRODUCTION_URL
          export EXPECTED_GIT_HASH=$CODEBUILD_RESOLVED_SOURCE_VERSION
          make test-smoke
        fi

reports:
  test-reports:
    files:
      - "**/*"
    base-directory: $TEST_REPORT_DIR
    file-format: JUNITXML

artifacts:
  files:
    - $TEST_REPORT_DIR/**/*
  name: test-reports-$CODEBUILD_BUILD_NUMBER

cache:
  paths:
    - node_modules/**/*
```

## 7.0 Framework-Specific Makefiles

### 7.1 TypeScript/Node.js (Vitest + Playwright)

```makefile
# Configuration (all parameterized)
TEST_BASE_URL ?= http://localhost:3000
TEST_COVERAGE_THRESHOLD ?= 70
TEST_TIMEOUT ?= 30000
TEST_RETRIES ?= 2
TEST_FAIL_FAST ?= true
TEST_REPORT_DIR ?= ./test-reports
EXPECTED_GIT_HASH ?= $(shell git rev-parse --short HEAD)

# Derived settings
VITEST_FLAGS := --reporter=verbose
PLAYWRIGHT_FLAGS := --reporter=junit

ifeq ($(TEST_FAIL_FAST),true)
  VITEST_FLAGS += --bail=1
endif

ifdef CI
  VITEST_FLAGS += --coverage --coverage.reporter=json --coverage.reporter=html
  PLAYWRIGHT_FLAGS += --retries=$(TEST_RETRIES)
endif

# ============================================================================
# TESTING TARGETS
# ============================================================================

.PHONY: test test-unit test-e2e test-smoke test-coverage test-ci lint

test: test-unit test-e2e
	@echo "All tests passed"

test-unit:
	@echo "Running unit tests..."
	@mkdir -p $(TEST_REPORT_DIR)
	npx vitest run $(VITEST_FLAGS)

test-e2e:
	@echo "Running E2E tests..."
	@mkdir -p $(TEST_REPORT_DIR)
	npx playwright test $(PLAYWRIGHT_FLAGS) --output=$(TEST_REPORT_DIR)/playwright

test-smoke:
	@echo "Running smoke tests against $(TEST_BASE_URL)..."
	@mkdir -p $(TEST_REPORT_DIR)
	EXPECTED_GIT_HASH=$(EXPECTED_GIT_HASH) \
	BASE_URL=$(TEST_BASE_URL) \
	npx playwright test tests/smoke.spec.ts $(PLAYWRIGHT_FLAGS)

test-coverage:
	@echo "Running tests with coverage (threshold: $(TEST_COVERAGE_THRESHOLD)%)..."
	@mkdir -p $(TEST_REPORT_DIR)
	npx vitest run --coverage --coverage.thresholds.lines=$(TEST_COVERAGE_THRESHOLD)

test-ci: lint test-coverage test-e2e
	@echo "CI tests complete"

lint:
	@echo "Running linter..."
	npx eslint . --max-warnings=0
	npx tsc --noEmit
```

### 7.2 Python (pytest + Playwright)

```makefile
# Configuration (all parameterized)
TEST_BASE_URL ?= http://localhost:8000
TEST_COVERAGE_THRESHOLD ?= 70
TEST_TIMEOUT ?= 30000
TEST_RETRIES ?= 2
TEST_FAIL_FAST ?= true
TEST_REPORT_DIR ?= ./test-reports
EXPECTED_GIT_HASH ?= $(shell git rev-parse --short HEAD)

# Derived settings
PYTEST_FLAGS := -v

ifeq ($(TEST_FAIL_FAST),true)
  PYTEST_FLAGS += -x
endif

ifdef CI
  PYTEST_FLAGS += --cov --cov-report=xml --cov-report=html --cov-fail-under=$(TEST_COVERAGE_THRESHOLD)
  PYTEST_FLAGS += --junitxml=$(TEST_REPORT_DIR)/junit.xml
endif

# ============================================================================
# TESTING TARGETS
# ============================================================================

.PHONY: test test-unit test-e2e test-smoke test-coverage test-ci lint

test: test-unit test-e2e
	@echo "All tests passed"

test-unit:
	@echo "Running unit tests..."
	@mkdir -p $(TEST_REPORT_DIR)
	pytest tests/unit $(PYTEST_FLAGS)

test-e2e:
	@echo "Running E2E tests..."
	@mkdir -p $(TEST_REPORT_DIR)
	pytest tests/e2e $(PYTEST_FLAGS)

test-smoke:
	@echo "Running smoke tests against $(TEST_BASE_URL)..."
	@mkdir -p $(TEST_REPORT_DIR)
	TEST_BASE_URL=$(TEST_BASE_URL) \
	EXPECTED_GIT_HASH=$(EXPECTED_GIT_HASH) \
	pytest tests/smoke $(PYTEST_FLAGS)

test-coverage:
	@echo "Running tests with coverage (threshold: $(TEST_COVERAGE_THRESHOLD)%)..."
	@mkdir -p $(TEST_REPORT_DIR)
	pytest --cov --cov-fail-under=$(TEST_COVERAGE_THRESHOLD) \
		--cov-report=html:$(TEST_REPORT_DIR)/coverage \
		--cov-report=xml:$(TEST_REPORT_DIR)/coverage.xml

test-ci: lint test-coverage test-e2e
	@echo "CI tests complete"

lint:
	@echo "Running linter..."
	ruff check .
	mypy .
```

## 8.0 Smoke Test Implementation

### 8.1 Required Smoke Test Pattern

Every project with deployments MUST have `tests/smoke.spec.ts`:

```typescript
// tests/smoke.spec.ts
import { test, expect } from '@playwright/test';

// All values from environment - NO hardcoded values
const BASE_URL = process.env.BASE_URL || process.env.TEST_BASE_URL;
const EXPECTED_GIT_HASH = process.env.EXPECTED_GIT_HASH;
const TIMEOUT = parseInt(process.env.TEST_TIMEOUT || '30000', 10);

test.describe('Smoke Tests', () => {
  test.setTimeout(TIMEOUT);

  test('page loads without errors', async ({ page }) => {
    const response = await page.goto(BASE_URL!);
    expect(response?.status()).toBeLessThan(400);
    await expect(page.locator('body')).toBeVisible();
  });

  test('git hash matches deployed version', async ({ page }) => {
    if (!EXPECTED_GIT_HASH) {
      test.skip();
      return;
    }

    await page.goto(BASE_URL!);

    // Check meta tag OR health endpoint
    const metaHash = await page.getAttribute('meta[name="git-hash"]', 'content');

    if (metaHash) {
      expect(metaHash).toBe(EXPECTED_GIT_HASH);
    } else {
      // Fallback to health endpoint
      const response = await page.request.get(`${BASE_URL}/health`);
      const data = await response.json();
      expect(data.gitHash).toBe(EXPECTED_GIT_HASH);
    }
  });

  test('no console errors on page load', async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    await page.goto(BASE_URL!);
    await page.waitForLoadState('networkidle');

    expect(errors).toHaveLength(0);
  });
});
```

## 9.0 Test Configuration Files

### 9.1 Playwright Config (Parameterized)

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

const BASE_URL = process.env.TEST_BASE_URL || 'http://localhost:3000';
const TIMEOUT = parseInt(process.env.TEST_TIMEOUT || '30000', 10);
const RETRIES = parseInt(process.env.TEST_RETRIES || '0', 10);
const PARALLEL = process.env.TEST_PARALLEL !== 'false';
const REPORT_DIR = process.env.TEST_REPORT_DIR || './test-reports';

export default defineConfig({
  testDir: './tests',
  timeout: TIMEOUT,
  fullyParallel: PARALLEL,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? RETRIES : 0,
  workers: PARALLEL ? undefined : 1,

  reporter: [
    ['list'],
    ['junit', { outputFile: `${REPORT_DIR}/junit.xml` }],
    ['html', { outputFolder: `${REPORT_DIR}/html` }],
  ],

  use: {
    baseURL: BASE_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

### 9.2 Vitest Config (Parameterized)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

const COVERAGE_THRESHOLD = parseInt(process.env.TEST_COVERAGE_THRESHOLD || '70', 10);
const REPORT_DIR = process.env.TEST_REPORT_DIR || './test-reports';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.test.ts'],

    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json', 'lcov'],
      reportsDirectory: `${REPORT_DIR}/coverage`,
      exclude: ['node_modules/', 'dist/', 'tests/'],
      thresholds: {
        lines: COVERAGE_THRESHOLD,
        branches: COVERAGE_THRESHOLD,
        functions: COVERAGE_THRESHOLD,
        statements: COVERAGE_THRESHOLD,
      },
    },

    reporters: ['verbose', 'junit'],
    outputFile: {
      junit: `${REPORT_DIR}/junit.xml`,
    },
  },
});
```

## 10.0 Checklist for New Projects

Every project MUST have:

- [ ] **Makefile** with all required test targets (Section 2.0)
- [ ] **CI/CD config** for at least one platform (Sections 4-6)
- [ ] **Smoke test** file at `tests/smoke.spec.ts` (Section 8.1)
- [ ] **Parameterized config** - no hardcoded values anywhere
- [ ] **Coverage threshold** enforced in CI (default 70%)
- [ ] **Lint step** runs before tests in CI

## 11.0 Related Documentation

- Testing SOP: `shared/standards/testing/TESTING_SOP.md`
- Smoke Test Pattern: `shared/standards/testing/SMOKE_TEST_PATTERN.md`
- BDD Testing: `shared/standards/testing/BDD_TESTING_GUIDE.md`
- Deployment Pattern: `shared/standards/deployment/MAKEFILE_TEMPLATE.md`
