# Testing SOP: pytest, Vitest, Playwright

Simple, standard approach to testing across the monorepo.

## 1.0 Framework Selection

```
┌─────────────────────┬──────────────────────────────────────┐
│ Project Type        │ Testing Framework                    │
├─────────────────────┼──────────────────────────────────────┤
│ Python              │ pytest                               │
│ TypeScript/React    │ Vitest                               │
│ E2E (any language)  │ Playwright                           │
│ BDD (stakeholders)  │ Cucumber + Playwright                │
└─────────────────────┴──────────────────────────────────────┘
```

## 2.0 Python: pytest

### 2.1 Setup

```bash
# Install
pip install pytest pytest-cov pytest-asyncio

# Create pytest.ini at project root
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --cov=.
    --cov-report=term-missing
    --cov-report=html:coverage
EOF
```

### 2.2 Test Structure

```
project/
├── src/
│   └── mymodule/
│       └── calculator.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py       # Unit tests
│   └── integration/
│       └── test_api.py          # Integration tests
└── pytest.ini
```

### 2.3 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_calculator.py

# Run specific test
pytest tests/test_calculator.py::test_add

# Watch mode (install pytest-watch)
pip install pytest-watch
ptw

# HTML coverage report
pytest --cov --cov-report=html
open coverage/index.html
```

### 2.4 Example Test

```python
# tests/test_calculator.py
import pytest
from mymodule.calculator import add, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected_value
```

## 3.0 TypeScript: Vitest

### 3.1 Setup

```bash
# Install
npm install -D vitest @vitest/ui

# Add to package.json
cat > package.json << 'EOF'
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
EOF
```

### 3.2 Configuration

Create `vitest.config.ts`:

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node', // or 'jsdom' for React
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json'],
      exclude: ['node_modules/', 'dist/']
    }
  }
})
```

### 3.3 Test Structure

```
project/
├── src/
│   └── calculator.ts
├── tests/
│   ├── calculator.test.ts       # Unit tests
│   └── integration/
│       └── api.test.ts          # Integration tests
├── vitest.config.ts
└── package.json
```

### 3.4 Running Tests

```bash
# Run all tests
npm test

# Watch mode (default)
npm test

# UI mode (web dashboard)
npm run test:ui
# Opens http://localhost:51204

# Coverage
npm run test:coverage

# Run specific test file
npm test calculator.test.ts
```

### 3.5 Example Test

```typescript
// tests/calculator.test.ts
import { describe, it, expect } from 'vitest'
import { add, divide } from '../src/calculator'

describe('Calculator', () => {
  it('adds two numbers', () => {
    expect(add(2, 3)).toBe(5)
    expect(add(-1, 1)).toBe(0)
  })

  it('divides two numbers', () => {
    expect(divide(10, 2)).toBe(5)
  })

  it('throws on divide by zero', () => {
    expect(() => divide(10, 0)).toThrow()
  })
})
```

## 4.0 E2E: Playwright

### 4.1 Setup

```bash
# Install
npm init playwright@latest

# This creates:
# - playwright.config.ts
# - tests/ directory
# - .github/workflows/playwright.yml
```

### 4.2 Configuration

Edit `playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://127.0.0.1:3000',
    trace: 'on-first-retry',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://127.0.0.1:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

### 4.3 Test Structure

```
project/
├── tests/
│   ├── example.spec.ts          # E2E tests
│   └── auth.setup.ts            # Shared auth setup
├── playwright.config.ts
└── package.json
```

### 4.4 Running Tests

```bash
# Run all tests
npx playwright test

# UI mode (interactive)
npx playwright test --ui

# Run specific test
npx playwright test tests/example.spec.ts

# Debug mode
npx playwright test --debug

# Run in headed mode (see browser)
npx playwright test --headed

# Show report
npx playwright show-report
```

### 4.5 Example Test

```typescript
// tests/example.spec.ts
import { test, expect } from '@playwright/test'

test('homepage has title', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveTitle(/My App/)
})

test('login flow', async ({ page }) => {
  await page.goto('/login')
  await page.fill('input[name="email"]', 'user@example.com')
  await page.fill('input[name="password"]', 'password123')
  await page.click('button[type="submit"]')

  await expect(page).toHaveURL('/dashboard')
  await expect(page.locator('h1')).toContainText('Welcome')
})
```

## 5.0 Running Tests Locally

### 5.1 Quick Commands

```bash
# Python project
cd projects/path/to/python-project
pytest

# TypeScript project
cd projects/path/to/typescript-project
npm test

# E2E tests
cd projects/path/to/web-app
npx playwright test --ui
```

### 5.2 Watch Mode for Development

**Python:**
```bash
pip install pytest-watch
ptw  # Auto-runs tests on file changes
```

**TypeScript:**
```bash
npm test  # Vitest runs in watch mode by default
```

**Playwright:**
```bash
npx playwright test --ui  # Interactive UI with live preview
```

## 6.0 Test Organization Rules

### 6.1 File Naming

```
pytest:      test_*.py or *_test.py
vitest:      *.test.ts or *.spec.ts
playwright:  *.spec.ts
```

### 6.2 Directory Structure

```
Option A (separate tests dir):
project/
├── src/
└── tests/

Option B (colocated):
project/
└── src/
    ├── calculator.ts
    └── calculator.test.ts
```

Use Option A for this monorepo (consistent with existing projects).

### 6.3 Test Categories

1. **Unit tests** - Test individual functions/classes
2. **Integration tests** - Test multiple components together
3. **E2E tests** - Test full user workflows

## 7.0 CI/CD Integration

All three frameworks generate standard reports:

```bash
# pytest
pytest --junitxml=junit.xml

# vitest
vitest --reporter=junit --outputFile=junit.xml

# playwright
npx playwright test --reporter=junit
```

## 8.0 Coverage Targets

- **Minimum:** 70% coverage
- **Recommended:** 80% coverage
- **Exclude:** Config files, test files, generated code

## 9.0 Common Patterns

### 9.1 Fixtures/Setup

**pytest:**
```python
@pytest.fixture
def client():
    return TestClient(app)

def test_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
```

**vitest:**
```typescript
import { beforeEach, afterEach } from 'vitest'

beforeEach(() => {
  // Setup before each test
})

afterEach(() => {
  // Cleanup after each test
})
```

**playwright:**
```typescript
test.beforeEach(async ({ page }) => {
  await page.goto('/dashboard')
})
```

### 9.2 Mocking

**pytest:**
```python
from unittest.mock import Mock, patch

@patch('mymodule.external_api')
def test_with_mock(mock_api):
    mock_api.return_value = {"status": "ok"}
    result = my_function()
    assert result == expected
```

**vitest:**
```typescript
import { vi } from 'vitest'

vi.mock('../src/api', () => ({
  fetchData: vi.fn(() => Promise.resolve({ status: 'ok' }))
}))
```

**playwright:**
```typescript
await page.route('**/api/data', route => {
  route.fulfill({ json: { status: 'ok' } })
})
```

## 10.0 Troubleshooting

### 10.1 Common Issues

**pytest not finding tests:**
```bash
# Check pytest.ini testpaths setting
# Ensure __init__.py exists in tests/
```

**Vitest import errors:**
```bash
# Check tsconfig.json paths
# Ensure vitest.config.ts environment is set correctly
```

**Playwright timeouts:**
```bash
# Increase timeout in test
test('slow test', async ({ page }) => {
  test.setTimeout(60000) // 60 seconds
  // ... test code
})
```

### 10.2 Debug Commands

```bash
# pytest with print statements visible
pytest -s

# vitest with console output
npm test -- --reporter=verbose

# playwright debug mode
npx playwright test --debug
```

## 11.0 BDD: Cucumber + Playwright

For stakeholder-readable tests using natural language (Gherkin syntax).

### 11.1 When to Use Cucumber

Use when:
- Stakeholders need to read/review test scenarios
- Product managers want to validate requirements
- Tests serve as living documentation
- Need shareable HTML reports

### 11.2 Quick Start

```bash
# Install
npm install -D @cucumber/cucumber @cucumber/html-formatter @playwright/test

# Add to package.json
{
  "scripts": {
    "test:bdd": "cucumber-js",
    "test:bdd:report": "cucumber-js && node cucumber-report.js"
  }
}
```

### 11.3 File Structure

```
project/
├── features/
│   ├── login.feature           # Gherkin scenarios
│   └── step_definitions/
│       └── login.steps.ts      # Step implementations
├── cucumber.cjs                 # Configuration
└── package.json
```

### 11.4 Example Feature

```gherkin
# features/login.feature
Feature: User Login

  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    And I click the login button
    Then I should see the dashboard
    And I should see "Welcome back"
```

### 11.5 Example Steps

```typescript
// features/step_definitions/login.steps.ts
import { Given, When, Then } from '@cucumber/cucumber'
import { expect } from '@playwright/test'

Given('I am on the login page', async function () {
  await this.page.goto('/login')
})

When('I enter valid credentials', async function () {
  await this.page.fill('input[name="email"]', 'user@example.com')
  await this.page.fill('input[name="password"]', 'password123')
})

When('I click the login button', async function () {
  await this.page.click('button[type="submit"]')
})

Then('I should see the dashboard', async function () {
  await expect(this.page).toHaveURL('/dashboard')
})

Then('I should see {string}', async function (text: string) {
  await expect(this.page.locator('body')).toContainText(text)
})
```

### 11.6 Running Cucumber Tests

```bash
# Run all scenarios
npm run test:bdd

# Run specific feature
npx cucumber-js features/login.feature

# Generate HTML report
npm run test:bdd:report
```

### 11.7 Full Documentation

See `shared/standards/testing/BDD_TESTING_GUIDE.md` for:
- Complete setup instructions
- Configuration examples
- Report generation
- S3 upload for sharing with stakeholders

## 12.0 Related Documentation

- BDD Testing: `shared/standards/testing/BDD_TESTING_GUIDE.md`
- Test accounts: `shared/standards/testing/test-accounts.json`
- Golden repos with test examples: `shared/golden-repos/*/tests/`
