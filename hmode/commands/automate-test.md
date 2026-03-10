---
version: 1.0.0
last_updated: 2025-11-13
description: Automated browser testing with natural language (URL, test description)
---

# Automate Test

Automated browser testing using natural language descriptions. Powered by Playwright with AI-driven test generation.

## Usage

```bash
# Natural language test description
/automate-test https://example.com "test user registration"

# More specific scenarios
/automate-test https://app.example.com "login with test@example.com and verify dashboard loads"

# E2E workflows
/automate-test https://shop.example.com "add product to cart, proceed to checkout, verify total price"

# Form validation
/automate-test https://example.com/signup "test signup form validation with invalid email"

# Accessibility testing
/automate-test https://example.com "navigate entire site using only keyboard"
```

## Instructions

### Step 1: Parse Arguments

**Extract URL and test description:**
```
args[0] = URL (required)
args[1+] = test description (natural language)
```

**Example:**
```
/automate-test https://example.com "test user registration"
→ url: https://example.com
→ test: "test user registration"
```

### Step 2: Analyze Test Description

**Break down the natural language description into steps:**

1. **Identify test type**:
   - User flow (registration, login, checkout)
   - Form validation (invalid inputs, required fields)
   - Navigation (menu, links, search)
   - Interaction (clicks, typing, scrolling)
   - Verification (content, state, error messages)

2. **Extract key actions**:
   - Navigate to page
   - Fill form fields
   - Click buttons/links
   - Verify elements/text
   - Check state/URL changes
   - Capture screenshots

3. **Infer test data**:
   - For "user registration": Generate test email, password
   - For "login": Use provided credentials or test data
   - For "checkout": Use test payment info
   - For "search": Use sample search terms

**Example breakdown:**
```
Test: "test user registration"

Steps inferred:
1. Navigate to https://example.com
2. Find registration link/button
3. Click to open registration form
4. Fill form fields:
   - Email: test_{timestamp}@example.com
   - Password: TestPass123!
   - Confirm password: TestPass123!
5. Submit form
6. Verify success message or redirect
7. Check for confirmation email reference
8. Capture screenshots at each step
```

### Step 3: Generate Playwright Test Script

**Create executable Playwright script:**

```javascript
const { chromium } = require('playwright');

(async () => {
  // Configuration
  const url = '{URL}';
  const testDescription = '{test description}';
  const screenshots = [];

  // Launch browser
  const browser = await chromium.launch({ headless: false }); // Show browser for visibility
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: { dir: './test-videos/' }
  });
  const page = await context.newPage();

  // Enable console logging
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));

  try {
    console.log(`🧪 Starting test: ${testDescription}`);
    console.log(`🌐 URL: ${url}`);

    // Step 1: Navigate to URL
    console.log('\n📍 Step 1: Navigate to page');
    await page.goto(url);
    await page.waitForLoadState('networkidle');
    screenshots.push(await page.screenshot({ path: 'step-1-navigate.png', fullPage: true }));

    // Step 2: Find registration link/button
    console.log('\n📍 Step 2: Find registration element');
    const registrationSelectors = [
      'text=/sign up/i',
      'text=/register/i',
      'text=/create account/i',
      'a[href*="register"]',
      'a[href*="signup"]',
      'button:has-text("Sign Up")',
      'button:has-text("Register")'
    ];

    let registrationElement = null;
    for (const selector of registrationSelectors) {
      try {
        registrationElement = await page.locator(selector).first();
        if (await registrationElement.isVisible({ timeout: 2000 })) {
          console.log(`✅ Found registration element: ${selector}`);
          break;
        }
      } catch (e) {
        // Continue trying next selector
      }
    }

    if (!registrationElement) {
      throw new Error('Could not find registration link/button');
    }

    await registrationElement.click();
    await page.waitForLoadState('networkidle');
    screenshots.push(await page.screenshot({ path: 'step-2-registration-page.png', fullPage: true }));

    // Step 3: Fill registration form
    console.log('\n📍 Step 3: Fill registration form');
    const timestamp = Date.now();
    const testData = {
      email: `test_${timestamp}@example.com`,
      password: 'TestPass123!',
      firstName: 'Test',
      lastName: 'User'
    };

    // Find and fill email field
    const emailSelectors = [
      'input[type="email"]',
      'input[name*="email"]',
      'input[id*="email"]',
      'input[placeholder*="email"]'
    ];

    for (const selector of emailSelectors) {
      try {
        const field = page.locator(selector).first();
        if (await field.isVisible({ timeout: 1000 })) {
          await field.fill(testData.email);
          console.log(`✅ Filled email: ${testData.email}`);
          break;
        }
      } catch (e) {
        // Try next selector
      }
    }

    // Find and fill password field
    const passwordSelectors = [
      'input[type="password"]',
      'input[name*="password"]',
      'input[id*="password"]'
    ];

    const passwordFields = await page.locator(passwordSelectors.join(',')).all();
    if (passwordFields.length >= 1) {
      await passwordFields[0].fill(testData.password);
      console.log('✅ Filled password');
    }
    if (passwordFields.length >= 2) {
      await passwordFields[1].fill(testData.password);
      console.log('✅ Filled password confirmation');
    }

    // Optional: First/Last name if present
    try {
      await page.locator('input[name*="first"], input[id*="first"]').first().fill(testData.firstName, { timeout: 1000 });
      await page.locator('input[name*="last"], input[id*="last"]').first().fill(testData.lastName, { timeout: 1000 });
      console.log('✅ Filled name fields');
    } catch (e) {
      console.log('ℹ️  Name fields not found (optional)');
    }

    screenshots.push(await page.screenshot({ path: 'step-3-form-filled.png', fullPage: true }));

    // Step 4: Submit form
    console.log('\n📍 Step 4: Submit form');
    const submitSelectors = [
      'button[type="submit"]',
      'input[type="submit"]',
      'button:has-text("Sign Up")',
      'button:has-text("Register")',
      'button:has-text("Create Account")'
    ];

    for (const selector of submitSelectors) {
      try {
        const button = page.locator(selector).first();
        if (await button.isVisible({ timeout: 1000 })) {
          await button.click();
          console.log(`✅ Clicked submit button: ${selector}`);
          break;
        }
      } catch (e) {
        // Try next selector
      }
    }

    // Wait for navigation or success message
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    await page.waitForTimeout(2000); // Allow for animations/messages

    screenshots.push(await page.screenshot({ path: 'step-4-submitted.png', fullPage: true }));

    // Step 5: Verify success
    console.log('\n📍 Step 5: Verify registration success');
    const currentUrl = page.url();
    const pageContent = await page.content();

    const successIndicators = [
      'success',
      'welcome',
      'confirm',
      'verification',
      'thank you',
      'account created',
      'check your email',
      'dashboard',
      'profile'
    ];

    let successFound = false;
    for (const indicator of successIndicators) {
      if (currentUrl.toLowerCase().includes(indicator) ||
          pageContent.toLowerCase().includes(indicator)) {
        console.log(`✅ Success indicator found: "${indicator}"`);
        successFound = true;
        break;
      }
    }

    // Check for error messages
    const errorSelectors = [
      '.error',
      '.alert-error',
      '[role="alert"]',
      '.text-danger',
      '.invalid-feedback'
    ];

    let errorFound = false;
    for (const selector of errorSelectors) {
      try {
        const errorElement = await page.locator(selector).first();
        if (await errorElement.isVisible({ timeout: 1000 })) {
          const errorText = await errorElement.textContent();
          console.log(`⚠️  Error message found: ${errorText}`);
          errorFound = true;
        }
      } catch (e) {
        // No error found
      }
    }

    screenshots.push(await page.screenshot({ path: 'step-5-result.png', fullPage: true }));

    // Generate report
    console.log('\n' + '='.repeat(60));
    console.log('📊 TEST REPORT');
    console.log('='.repeat(60));
    console.log(`Test: ${testDescription}`);
    console.log(`URL: ${url}`);
    console.log(`Status: ${successFound && !errorFound ? '✅ PASSED' : errorFound ? '❌ FAILED' : '⚠️  INCONCLUSIVE'}`);
    console.log(`Final URL: ${currentUrl}`);
    console.log(`Screenshots: ${screenshots.length} captured`);
    console.log('='.repeat(60));

    // Return results
    return {
      status: successFound && !errorFound ? 'PASSED' : errorFound ? 'FAILED' : 'INCONCLUSIVE',
      testDescription,
      url,
      finalUrl: currentUrl,
      testData,
      screenshots: screenshots.length,
      successFound,
      errorFound
    };

  } catch (error) {
    console.error('\n❌ Test failed with error:', error.message);
    await page.screenshot({ path: 'error-screenshot.png', fullPage: true });
    throw error;
  } finally {
    await context.close();
    await browser.close();
  }
})();
```

### Step 4: Execute Test

1. **Save Playwright script** to temporary file
2. **Run with Node.js**: `node test-script.js`
3. **Capture output** and parse results
4. **Collect screenshots** from generated files

### Step 5: Generate Report

```markdown
# Automated Test Report

**Test**: {test description}
**URL**: {url}
**Executed**: {timestamp}
**Status**: {✅ PASSED / ❌ FAILED / ⚠️ INCONCLUSIVE}

---

## Test Execution

**Test scenario**: {natural language description}

**Steps executed**:
1. ✅ Navigate to {url}
2. ✅ Find registration element
3. ✅ Fill registration form
   - Email: {test email}
   - Password: ********
   - Name: {test name}
4. ✅ Submit form
5. {✅/❌} Verify success

**Total duration**: {seconds}s

---

## Results

**Final URL**: {final url}
**URL changed**: {Yes/No}

**Success indicators found**:
- {indicator 1}
- {indicator 2}

**Errors detected**: {count}
{If errors found, list them}

**Outcome**: {description of what happened}

---

## Test Data Used

```json
{
  "email": "test_1699999999@example.com",
  "password": "TestPass123!",
  "firstName": "Test",
  "lastName": "User"
}
```

---

## Screenshots

**{count} screenshots captured:**

1. **step-1-navigate.png** - Initial page load
2. **step-2-registration-page.png** - Registration form opened
3. **step-3-form-filled.png** - Form filled with test data
4. **step-4-submitted.png** - After form submission
5. **step-5-result.png** - Final result

**Location**: `./test-screenshots/`

---

## Console Output

```
{Captured console logs from test execution}
```

---

## Recommendations

{If test failed}:
- **Issue detected**: {description}
- **Possible causes**: {list}
- **Suggested fixes**: {list}

{If test passed}:
- ✅ User registration flow working correctly
- ✅ Form validation functioning
- ✅ Success feedback provided

---

## Next Steps

**Regression testing**:
- Add to automated test suite
- Run on CI/CD pipeline
- Test with various data inputs

**Additional scenarios to test**:
- Invalid email format
- Weak password
- Duplicate email
- Missing required fields

---

*Generated by Automate Test v1.0.0*
*Powered by Playwright*
```

---

## Supported Test Scenarios

### User Flows
```bash
/automate-test https://example.com "test user registration"
/automate-test https://example.com "test login with existing user"
/automate-test https://example.com "test password reset flow"
/automate-test https://example.com "test logout"
```

### E-Commerce
```bash
/automate-test https://shop.com "add product to cart and checkout"
/automate-test https://shop.com "search for 'laptop' and view first result"
/automate-test https://shop.com "filter products by price range"
```

### Form Validation
```bash
/automate-test https://example.com "submit contact form with invalid email"
/automate-test https://example.com "test required field validation on signup"
/automate-test https://example.com "test password strength requirements"
```

### Navigation
```bash
/automate-test https://example.com "click all menu items and verify pages load"
/automate-test https://example.com "test search functionality"
/automate-test https://example.com "navigate using breadcrumbs"
```

### Accessibility
```bash
/automate-test https://example.com "navigate site using only Tab key"
/automate-test https://example.com "test screen reader announcements"
/automate-test https://example.com "verify all images have alt text"
```

---

## Advanced Features

### Custom Test Data

```bash
/automate-test https://example.com "login with user@example.com password SecurePass123"
```

**Parser extracts credentials from natural language**

### Multi-Step Workflows

```bash
/automate-test https://example.com "register new user, login, update profile, logout"
```

**Automatically chains multiple actions**

### Conditional Testing

```bash
/automate-test https://example.com "if login fails, verify error message shows"
```

**Handles conditional logic**

---

## Test Execution Modes

### Interactive Mode (Default)
- Browser window visible
- Slower execution for observation
- Easier debugging

### Headless Mode
```bash
# Modify script: headless: true
```
- Faster execution
- CI/CD friendly
- No browser window

### Record Mode
```bash
# Enables video recording
recordVideo: { dir: './test-videos/' }
```
- Captures full test execution
- Useful for debugging failures

---

## Error Handling

**Common issues:**

1. **Element not found**
   ```
   ❌ Could not find registration link/button

   Tried selectors:
   - text=/sign up/i
   - text=/register/i
   - a[href*="register"]

   Recommendation:
   - Provide more specific test description
   - Check if registration is behind login
   - Verify element exists on page
   ```

2. **Timeout**
   ```
   ❌ Test timed out waiting for page load

   Possible causes:
   - Slow network
   - Heavy page assets
   - Blocking requests

   Recommendation:
   - Increase timeout
   - Check network performance
   - Verify URL is accessible
   ```

3. **Verification failed**
   ```
   ⚠️  Could not verify test success

   No success indicators found
   No error messages detected

   Recommendation:
   - Check final URL for redirect
   - Look for specific success message
   - Verify expected outcome manually
   ```

---

## Integration with CI/CD

**Add to test suite:**

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install -D playwright
      - run: npx playwright install chromium
      - run: node test-registration.js
```

**Continuous testing:**
- Run on every commit
- Test against staging environment
- Notify on failures

---

## Playwright Installation

**If Playwright not installed:**

```bash
# Install Playwright
npm install -D @playwright/test

# Install Chromium browser
npx playwright install chromium

# Or all browsers
npx playwright install
```

**Docker (for CI/CD):**
```bash
docker run -it --rm \
  -v $(pwd):/work \
  -w /work \
  mcr.microsoft.com/playwright:latest \
  node test-script.js
```

---

## Browser-Use Integration (Future)

**For more complex scenarios**, can integrate browser-use library:

```python
from browser_use import Agent

agent = Agent(
    task="Register a new user on example.com",
    llm=your_llm
)

result = agent.run()
```

**Benefits:**
- AI-driven navigation
- Adaptive to layout changes
- Natural language control
- Self-healing tests

---

## Best Practices

1. **Use descriptive test descriptions**
   - ✅ "test user registration with valid email"
   - ❌ "test signup"

2. **Include verification steps**
   - ✅ "register user and verify confirmation email message"
   - ❌ "register user"

3. **Test both positive and negative cases**
   - Positive: "register with valid data"
   - Negative: "register with existing email and verify error"

4. **Keep tests atomic**
   - One test per user flow
   - Independent test data
   - No dependencies between tests

5. **Use stable selectors**
   - AI infers best selectors
   - Falls back to multiple strategies
   - Text-based selectors more resilient

---

## Troubleshooting

**Test keeps failing:**
1. Run in interactive mode (browser visible)
2. Check screenshots to see where it failed
3. Verify selectors match page structure
4. Increase timeouts for slow sites

**Can't find elements:**
1. Check if element is in iframe
2. Verify element is visible (not hidden)
3. Wait for page to fully load
4. Use more specific selectors

**Tests flaky:**
1. Add explicit waits
2. Wait for network idle
3. Use retry logic
4. Check for race conditions

---

Be adaptive, handle errors gracefully, provide detailed reports with actionable insights.
