# Headed Testing Strategy

**Version:** 1.0.0
**Created:** 2025-12-05
**Category:** Testing / CI/CD

## 1.0 Overview

Chrome extensions and certain browser features require a headed (non-headless) browser. This document describes strategies for running headed browser tests in environments without a physical display.

## 2.0 The Problem

```
┌─────────────────────────────────────────────────────────────┐
│ Chrome Extensions require headed mode because:              │
│ - Extension system is stripped from headless Chrome         │
│ - --load-extension flag is ignored in headless              │
│ - Service workers need the full Chrome UI infrastructure    │
└─────────────────────────────────────────────────────────────┘
```

**Error without display:**
```
Looks like you launched a headed browser without having a XServer running.
Set either 'headless: true' or use 'xvfb-run <your-playwright-app>'
```

## 3.0 Solution: Xvfb (X Virtual Framebuffer)

Xvfb provides a virtual display that allows headed browsers to run without a physical monitor.

### 3.1 Installation

```bash
# Ubuntu/Debian
apt-get install -y xvfb

# Alpine
apk add xvfb

# macOS (not needed - has display)
# Windows (not needed - has display)
```

### 3.2 Usage Patterns

**Pattern 1: xvfb-run wrapper (Recommended)**
```bash
xvfb-run --auto-servernum --server-args='-screen 0 1280x720x24' node test.js
```

**Pattern 2: Manual Xvfb management**
```bash
# Start Xvfb
Xvfb :99 -screen 0 1280x720x24 &
export DISPLAY=:99

# Run tests
node test.js

# Stop Xvfb
killall Xvfb
```

**Pattern 3: npm scripts**
```json
{
  "scripts": {
    "test": "node test/test.js",
    "test:xvfb": "xvfb-run --auto-servernum --server-args='-screen 0 1280x720x24' node test/test.js",
    "test:ci": "xvfb-run --auto-servernum --server-args='-screen 0 1280x720x24' node test/test.js --ci"
  }
}
```

### 3.3 xvfb-run Options

| Option | Description |
|--------|-------------|
| `--auto-servernum` | Auto-select display number (avoids conflicts) |
| `--server-args='-screen 0 WxHxD'` | Set virtual screen resolution and depth |
| `-a` | Short form of --auto-servernum |

**Common resolutions:**
- `1280x720x24` - 720p, 24-bit color (recommended)
- `1920x1080x24` - 1080p, 24-bit color
- `1024x768x24` - Legacy resolution

## 4.0 Playwright Configuration

### 4.1 Extension Testing Setup

```javascript
const { chromium } = require('playwright');
const path = require('path');

const EXTENSION_PATH = path.resolve(__dirname, '../extension');

async function testExtension() {
  const context = await chromium.launchPersistentContext('', {
    headless: false,  // MUST be false for extensions
    args: [
      `--disable-extensions-except=${EXTENSION_PATH}`,
      `--load-extension=${EXTENSION_PATH}`,
      '--no-sandbox',
      '--disable-setuid-sandbox',
    ],
  });

  // Get extension ID from service worker
  const serviceWorkers = context.serviceWorkers();
  let extensionId;
  for (const sw of serviceWorkers) {
    if (sw.url().includes('chrome-extension://')) {
      extensionId = sw.url().split('/')[2];
      break;
    }
  }

  // Open extension popup
  const popup = await context.newPage();
  await popup.goto(`chrome-extension://${extensionId}/popup.html`);

  // ... test logic

  await context.close();
}
```

### 4.2 CI Mode Detection

```javascript
const CI_MODE = process.env.CI === 'true' || process.argv.includes('--ci');

if (CI_MODE) {
  // Auto-close browser after test
  await context.close();
  process.exit(passed ? 0 : 1);
} else {
  // Keep open for manual inspection
  console.log('Browser open for inspection. Press Ctrl+C to close.');
  await new Promise(() => {});
}
```

## 5.0 CI/CD Integration

### 5.1 GitHub Actions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y xvfb
          npm install
          npx playwright install chromium

      - name: Run tests
        run: npm run test:ci
```

### 5.2 Docker

```dockerfile
FROM node:20

# Install Xvfb and Chrome dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    libgbm1 \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2

WORKDIR /app
COPY . .
RUN npm install
RUN npx playwright install chromium

CMD ["npm", "run", "test:ci"]
```

### 5.3 GitLab CI

```yaml
test:
  image: node:20
  before_script:
    - apt-get update && apt-get install -y xvfb
    - npm install
    - npx playwright install chromium
  script:
    - npm run test:ci
```

## 6.0 Troubleshooting

### 6.1 Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing X server or $DISPLAY` | No display available | Use xvfb-run |
| `Cannot find extension ID` | Extension not loaded | Check extension path, wait for service worker |
| `net::ERR_TUNNEL_CONNECTION_FAILED` | Network blocked | CI environment network restrictions |
| `Target page closed` | Browser crashed | Add `--no-sandbox` flag |

### 6.2 Debug Mode

```bash
# See Xvfb output
xvfb-run --auto-servernum node test.js 2>&1

# Check display variable
echo $DISPLAY

# Verify Xvfb is running
ps aux | grep Xvfb
```

## 7.0 Best Practices

1. **Always use --auto-servernum** - Prevents display number conflicts
2. **Set explicit screen size** - Ensures consistent screenshots
3. **Add --no-sandbox for CI** - Required in most CI environments
4. **Implement CI mode flag** - Auto-close vs manual inspection
5. **Take screenshots on failure** - Aids debugging
6. **Set reasonable timeouts** - Browser startup can be slow

## 8.0 Related Documents

- `PHASE_8.5_VALIDATION.md` - Testing phase in SDLC
- `MODULAR_QA_VALIDATION.md` - QA patterns

---

**Changelog:**
- 1.0.0 (2025-12-05): Initial version
