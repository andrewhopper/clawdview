# ClawdView Test Plan

## Overview

This document describes the end-to-end (e2e) test strategy for ClawdView using
[Playwright](https://playwright.dev). The goal is to ensure that every user-facing
feature and security constraint is automatically verified on every pull request.

---

## Test Architecture

```
clawdview-tool/
├── playwright.config.js          # Playwright configuration
├── TEST_PLAN.md                  # This document
└── tests/
    ├── test-server.js            # Launches a test server on port 3334
    ├── fixtures/                 # Static files used as test data
    │   ├── sample.html
    │   ├── sample.json
    │   ├── sample.py
    │   ├── sample.md
    │   └── sample.css
    └── e2e/                      # Playwright test suites
        ├── smoke.spec.js         # App load & basic UI
        ├── api.spec.js           # REST API correctness
        ├── security.spec.js      # Security enforcement
        ├── file-browser.spec.js  # Sidebar file navigation
        └── file-preview.spec.js  # Preview / Code / Output tabs
```

### Test Server

A dedicated test server (`tests/test-server.js`) starts on **port 3334** and
watches the `tests/fixtures/` directory. This keeps tests isolated from any
developer server running on the default port 3333.

---

## Test Suites

### 1. Smoke Tests (`smoke.spec.js`)

**Purpose:** Verify the app starts correctly and essential UI chrome is present.

| # | Test Case | Expected Result |
|---|-----------|----------------|
| S1 | Homepage loads | `<title>` contains "ClawdView" |
| S2 | File sidebar is visible | Sidebar element visible on load |
| S3 | Tab bar has Preview, Code, Output tabs | All three tab labels present |
| S4 | No uncaught JS errors on load | Zero pageerror events |

---

### 2. REST API Tests (`api.spec.js`)

**Purpose:** Verify each HTTP endpoint returns the correct status codes and
response shapes.

#### `GET /api/files`

| # | Test Case | Expected Result |
|---|-----------|----------------|
| A1 | Returns HTTP 200 | Status 200 |
| A2 | Response is an array | `Array.isArray(body) === true` |
| A3 | Fixture files present | `sample.html`, `sample.json`, etc. in list |
| A4 | File entries have correct shape | `name`, `type`, `path`, `extension` fields |

#### `GET /api/file/:path`

| # | Test Case | Expected Result |
|---|-----------|----------------|
| A5 | Returns HTML file content | 200, `content` includes `<!DOCTYPE html>` |
| A6 | Returns JSON file content | 200, content is valid JSON |
| A7 | Returns Markdown file content | 200, content includes heading text |
| A8 | Returns Python file content | 200, content includes function definition |
| A9 | 404 for missing file | 404 with `error` field |
| A10 | Does not leak system path | `path` field is relative, not absolute |

#### `POST /api/format`

| # | Test Case | Expected Result |
|---|-----------|----------------|
| A11 | Formats JSON file successfully | 200, `success: true` |
| A12 | Missing extension returns 400 | 400 |
| A13 | Unsupported file type returns 400 | 400, `success: false` |

---

### 3. Security Tests (`security.spec.js`)

**Purpose:** Ensure the server enforces all documented security rules.

#### Hidden file protection

| # | Test Case | Expected Result |
|---|-----------|----------------|
| SE1 | `.env` is blocked | 403, error mentions "hidden" |
| SE2 | `.ssh/id_rsa` path is blocked | 403 |

#### File type restrictions

| # | Test Case | Expected Result |
|---|-----------|----------------|
| SE3 | `.exe` file blocked | 403, error mentions "not supported" |
| SE4 | `.sh` file blocked | 403 |
| SE5 | `.bat` file blocked | 403 |
| SE6 | `.hidden.html` is allowed (edge case) | Not 403 (may be 404) |

#### Python execution safety

| # | Test Case | Expected Result |
|---|-----------|----------------|
| SE7 | Empty code rejected | 400, `success: false` |
| SE8 | Code > 50KB rejected | 400, error mentions "too large" |
| SE9 | Rate limit enforced after 5 calls | 6th call returns 429 |

---

### 4. File Browser Tests (`file-browser.spec.js`)

**Purpose:** Verify the sidebar file tree lists files and responds to selection.

| # | Test Case | Expected Result |
|---|-----------|----------------|
| FB1 | Fixture files appear in sidebar | All four fixture files visible |
| FB2 | Clicking a file selects it | Filename highlighted/shown |
| FB3 | Selecting `.py` file shows Run button | Run button visible |
| FB4 | Selecting non-Python file hides Run button | Run button not visible |

---

### 5. File Preview Tests (`file-preview.spec.js`)

**Purpose:** Verify the Preview, Code, and Output tabs render content correctly.

#### HTML preview

| # | Test Case | Expected Result |
|---|-----------|----------------|
| FP1 | HTML file renders in an `<iframe>` | `<iframe>` element visible |
| FP2 | iframe contains fixture heading | "Sample HTML File" text inside iframe |

#### Code tab

| # | Test Case | Expected Result |
|---|-----------|----------------|
| FP3 | Code tab shows raw JSON content | Fixture key visible in code panel |
| FP4 | Code tab shows Python source | `def greet` visible |

#### Markdown preview

| # | Test Case | Expected Result |
|---|-----------|----------------|
| FP5 | Markdown renders as formatted HTML | Heading text visible in preview area |

#### Python execution

| # | Test Case | Expected Result |
|---|-----------|----------------|
| FP6 | Run button executes script | Output panel shows "Hello, ClawdView!" |

---

## Running the Tests

### Prerequisites

```bash
cd clawdview-tool
npm install                        # installs @playwright/test
npx playwright install chromium    # installs browser binaries
```

### Commands

```bash
# Run all tests (headless, both browsers)
npm test

# Run with Playwright UI for interactive debugging
npm run test:ui

# Run in headed mode (see the browser)
npm run test:headed

# Open the HTML report after a run
npm run test:report
```

### CI/CD Integration

Add the following job to your GitHub Actions workflow:

```yaml
- name: Install dependencies
  run: npm ci
  working-directory: clawdview-tool

- name: Install Playwright browsers
  run: npx playwright install --with-deps chromium
  working-directory: clawdview-tool

- name: Run e2e tests
  run: npm test
  working-directory: clawdview-tool

- name: Upload Playwright report
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: playwright-report
    path: clawdview-tool/tests/playwright-report/
    retention-days: 30
```

---

## Future Test Areas

The following areas are not yet covered and should be added as the codebase grows:

| Area | Description |
|------|-------------|
| Live reload | Verify that editing a fixture file triggers a WebSocket `fileChange` event and the UI refreshes |
| React/JSX preview | Verify `.jsx` files are transpiled via Babel and rendered in the preview |
| SVG preview | Verify `.svg` files are rendered as vector graphics |
| File formatter accuracy | Unit-test the `formatJavaScript`, `formatHTML`, `formatCSS` methods in isolation |
| Python timeout | Verify a long-running script is killed after 30 seconds |
| Accessibility | Run `axe` accessibility checks on the main UI |
| Mobile viewports | Verify the UI is usable on smaller screens |

---

## Quality Gates

The following gates must pass before merging any PR:

- [ ] All Playwright tests pass in CI (chromium + firefox)
- [ ] Zero new console errors introduced
- [ ] Security tests pass (no regressions in access control)
- [ ] Screenshots captured on failure are reviewed

---

*Last updated: 2026-03-03*
