# BDD Testing with Cucumber + Playwright

Natural language test definitions using Gherkin syntax with Playwright execution.

## Why Cucumber BDD?

| Need | Solution |
|------|----------|
| Stakeholder-readable tests | Gherkin natural language syntax |
| Shareable reports | HTML reports uploadable to S3 |
| Existing infrastructure | Integrates with Playwright (already in use) |
| TypeScript support | tsx loader for step definitions |

## Quick Start

### 1. Install Dependencies

Add to `package.json`:

```json
{
  "devDependencies": {
    "@cucumber/cucumber": "^11.2.0",
    "@cucumber/html-formatter": "^21.9.0",
    "@playwright/test": "^1.57.0",
    "multiple-cucumber-html-reporter": "^3.8.0",
    "tsx": "^4.21.0"
  },
  "scripts": {
    "test:bdd": "cucumber-js --config cucumber.cjs",
    "test:bdd:report": "cucumber-js --config cucumber.cjs && node cucumber-report.js",
    "test:bdd:upload": "cucumber-js --config cucumber.cjs && node cucumber-report.js && node upload-report.js"
  }
}
```

Run:
```bash
npm install
npx playwright install chromium
```

### 2. Create Configuration

Create `cucumber.cjs`:

```javascript
module.exports = {
  default: {
    paths: ['features/**/*.feature'],
    require: [
      './features/support/world.ts',
      './features/support/hooks.ts',
      './features/step-definitions/*.ts',
    ],
    requireModule: ['tsx'],
    format: [
      'progress-bar',
      'json:cucumber-report/cucumber-report.json',
      'html:cucumber-report/cucumber-report.html',
    ],
    parallel: 1,
    timeout: 60000,
    worldParameters: {
      baseUrl: process.env.TEST_URL || 'http://localhost:5173',
      headless: process.env.HEADLESS !== 'false',
      slowMo: process.env.SLOW_MO ? parseInt(process.env.SLOW_MO) : 0,
    },
  },
};
```

### 3. Create Directory Structure

```
project/
├── cucumber.cjs
├── cucumber-report.js
├── upload-report.js
└── features/
    ├── example.feature          # Gherkin test specs
    ├── support/
    │   ├── world.ts             # Playwright browser setup
    │   └── hooks.ts             # Before/After lifecycle
    └── step-definitions/
        └── example.steps.ts     # Step implementations
```

### 4. Write Feature Files (Gherkin)

Create `features/example.feature`:

```gherkin
@smoke
Feature: User Authentication
  As a user
  I want to log in to the application
  So that I can access my dashboard

  Scenario: Successful login
    Given I am on the login page
    When I enter "user@example.com" as email
    And I enter "password123" as password
    And I click the login button
    Then I should see the dashboard
    And I should see "Welcome back" in the header
```

### 5. Create World (Playwright Setup)

Create `features/support/world.ts`:

```typescript
import { World, IWorldOptions, setWorldConstructor } from '@cucumber/cucumber';
import { Browser, BrowserContext, Page, chromium, devices } from '@playwright/test';

export interface ICustomWorld extends World {
  browser?: Browser;
  context?: BrowserContext;
  page?: Page;
  baseUrl: string;
  headless: boolean;
  slowMo: number;
  isMobile: boolean;
}

export class CustomWorld extends World implements ICustomWorld {
  browser?: Browser;
  context?: BrowserContext;
  page?: Page;
  baseUrl: string;
  headless: boolean;
  slowMo: number;
  isMobile: boolean = false;

  constructor(options: IWorldOptions) {
    super(options);
    this.baseUrl = options.parameters.baseUrl || 'http://localhost:3000';
    this.headless = options.parameters.headless !== false;
    this.slowMo = options.parameters.slowMo || 0;
  }

  async launchBrowser(mobile: boolean = false): Promise<void> {
    this.isMobile = mobile;
    this.browser = await chromium.launch({
      headless: this.headless,
      slowMo: this.slowMo,
    });

    const contextOptions = mobile
      ? { ...devices['iPhone 12'] }
      : { viewport: { width: 1280, height: 720 } };

    this.context = await this.browser.newContext(contextOptions);
    this.page = await this.context.newPage();
  }

  async closeBrowser(): Promise<void> {
    await this.page?.close();
    await this.context?.close();
    await this.browser?.close();
  }
}

setWorldConstructor(CustomWorld);
```

### 6. Create Hooks

Create `features/support/hooks.ts`:

```typescript
import { Before, After, BeforeAll, AfterAll, Status } from '@cucumber/cucumber';
import { ICustomWorld } from './world';
import * as fs from 'fs';

BeforeAll(async function () {
  const dirs = ['cucumber-report', 'cucumber-report/screenshots'];
  dirs.forEach((dir) => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  });
});

Before(async function (this: ICustomWorld, { pickle }) {
  const tags = pickle.tags.map((t) => t.name);
  const isMobile = tags.includes('@mobile');
  await this.launchBrowser(isMobile);
});

After(async function (this: ICustomWorld, { pickle, result }) {
  if (result?.status === Status.FAILED && this.page) {
    const screenshot = await this.page.screenshot({ fullPage: true });
    this.attach(screenshot, 'image/png');
  }
  await this.closeBrowser();
});
```

### 7. Write Step Definitions

Create `features/step-definitions/example.steps.ts`:

```typescript
import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { ICustomWorld } from '../support/world';

Given('I am on the login page', async function (this: ICustomWorld) {
  await this.page!.goto(`${this.baseUrl}/login`);
});

When('I enter {string} as email', async function (this: ICustomWorld, email: string) {
  await this.page!.fill('input[name="email"]', email);
});

When('I enter {string} as password', async function (this: ICustomWorld, password: string) {
  await this.page!.fill('input[name="password"]', password);
});

When('I click the login button', async function (this: ICustomWorld) {
  await this.page!.click('button[type="submit"]');
});

Then('I should see the dashboard', async function (this: ICustomWorld) {
  await expect(this.page!).toHaveURL(/dashboard/);
});

Then('I should see {string} in the header', async function (this: ICustomWorld, text: string) {
  const header = this.page!.locator('header');
  await expect(header).toContainText(text);
});
```

### 8. Create Report Generator

Create `cucumber-report.js`:

```javascript
const report = require('multiple-cucumber-html-reporter');
const fs = require('fs');
const path = require('path');

const reportDir = 'cucumber-report';
const jsonReportPath = path.join(reportDir, 'cucumber-report.json');

if (!fs.existsSync(jsonReportPath)) {
  console.error('No cucumber-report.json found. Run tests first.');
  process.exit(1);
}

report.generate({
  jsonDir: reportDir,
  reportPath: path.join(reportDir, 'html'),
  reportName: 'BDD Test Report',
  pageTitle: 'E2E Tests',
  displayDuration: true,
  displayReportTime: true,
  metadata: {
    browser: { name: 'chromium', version: 'latest' },
    device: 'Desktop & Mobile',
    platform: { name: process.platform, version: process.version },
  },
});

console.log(`Report: ${path.resolve(reportDir, 'html', 'index.html')}`);
```

### 9. Create S3 Upload Script

Create `upload-report.js`:

```javascript
#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const REPORT_DIR = 'cucumber-report/html';
const PROJECT_NAME = process.env.PROJECT_NAME || path.basename(process.cwd());

// Path to shared s3publish.py (adjust based on project location)
const S3PUBLISH_PATH = path.resolve(__dirname, '../../shared/tools/s3publish.py');

// Check environment
const required = ['ASSET_DIST_AWS_BUCKET', 'ASSET_DIST_AWS_ACCESS_KEY_ID', 'ASSET_DIST_AWS_ACCESS_KEY_SECRET'];
const missing = required.filter((v) => !process.env[v]);
if (missing.length > 0) {
  console.log(`Missing: ${missing.join(', ')}`);
  console.log(`Local report: ${path.resolve(REPORT_DIR, 'index.html')}`);
  process.exit(0);
}

// Get all files recursively
function getAllFiles(dir, files = []) {
  fs.readdirSync(dir).forEach((file) => {
    const fp = path.join(dir, file);
    fs.statSync(fp).isDirectory() ? getAllFiles(fp, files) : files.push(fp);
  });
  return files;
}

// Upload
const files = getAllFiles(REPORT_DIR);
const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
const reportPath = `test-reports/${PROJECT_NAME}/${timestamp}`;

files.forEach((localPath) => {
  const s3Key = `${reportPath}/${path.relative(REPORT_DIR, localPath)}`;
  spawnSync('python3', [S3PUBLISH_PATH, localPath, s3Key], { env: process.env });
});

console.log(`Report: https://${process.env.ASSET_DIST_AWS_BUCKET}.s3.us-east-1.amazonaws.com/${reportPath}/index.html`);
```

### 10. Add to .gitignore

```
cucumber-report/
dist-features/
```

## Commands

| Command | Description |
|---------|-------------|
| `npm run test:bdd` | Run all BDD tests |
| `npm run test:bdd:report` | Run tests + generate HTML report |
| `npm run test:bdd:upload` | Run tests + upload report to S3 |
| `npx cucumber-js --config cucumber.cjs --tags @smoke` | Run smoke tests only |
| `npx cucumber-js --config cucumber.cjs --tags @mobile` | Run mobile tests only |
| `HEADLESS=false npm run test:bdd` | Run with visible browser |

## Tagging Strategy

Use tags to organize and filter tests:

```gherkin
@smoke           # Quick verification tests
@mobile          # Mobile device tests
@regression      # Full regression suite
@wip             # Work in progress (skip in CI)
@skip            # Temporarily disabled
```

Run specific tags:
```bash
npx cucumber-js --config cucumber.cjs --tags "@smoke and not @mobile"
```

## Best Practices

1. **Feature files are documentation** - Write for non-technical stakeholders
2. **One scenario = one behavior** - Keep scenarios focused
3. **Reuse step definitions** - Create generic steps for common actions
4. **Use Background** - Factor out common Given steps
5. **Tag strategically** - Enable flexible test selection
6. **Screenshot on failure** - Already configured in hooks

## Reference Implementation

See GoCoder frontend for a complete working example:
`projects/personal/active/tool-gocoder-web-agentic-coding-ui-like-claude-code-web-t9x2k/frontend/`

Files:
- `cucumber.cjs` - Configuration
- `features/terminal.feature` - Gherkin specs
- `features/support/world.ts` - Playwright setup
- `features/step-definitions/terminal.steps.ts` - Step implementations
