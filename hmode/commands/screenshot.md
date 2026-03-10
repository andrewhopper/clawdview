---
version: 1.0.0
last_updated: 2025-12-02
description: Capture screenshots of URLs with viewport presets (desktop, mobile, tablet)
---

# Screenshot

Capture screenshots of web pages using Playwright with viewport presets.

## Usage

```bash
# Single URL
/screenshot example.com

# Multiple URLs (comma-separated)
/screenshot example.com,google.com,github.com

# With viewport preset
/screenshot example.com mobile

# All viewports (desktop, tablet, mobile)
/screenshot example.com all

# With output directory
/screenshot example.com -o ./my-screenshots

# With scrolling (for lazy-loaded content)
/screenshot example.com --scroll
```

## Instructions

Parse the arguments from: $ARGUMENTS

### Step 1: Parse Arguments

**Extract from arguments:**
- URLs: First argument (required) - comma-separated or space-separated
- Viewport: `desktop` | `tablet` | `mobile` | `all` (default: desktop)
- Output: `-o <dir>` or use `./screenshots`
- Scroll: `--scroll` or `-s` flag
- Full page: `--full-page` (default) or `--no-full-page`

**Examples:**
```
/screenshot foo.com
→ urls: ["foo.com"], viewport: desktop

/screenshot foo.com,bar.com mobile
→ urls: ["foo.com", "bar.com"], viewport: mobile

/screenshot example.com all -o ./captures
→ urls: ["example.com"], viewport: [desktop, tablet, mobile], output: ./captures

/screenshot example.com --scroll
→ urls: ["example.com"], viewport: desktop, scroll: true
```

### Step 2: Run Screenshot Tool

Navigate to the screenshot tool directory and execute:

```bash
cd hmode/shared/tools/screenshot

# Install dependencies if needed
npm install 2>/dev/null || true

# Run the screenshot command
npx tsx src/screenshot.ts <urls> -v <viewport> -o <output> [--scroll] [--full-page|--no-full-page]
```

**Viewport options:**
- `desktop`: 1280x720
- `tablet`: 768x1024
- `mobile`: 375x667
- `all`: all three viewports

### Step 3: Report Results

After capture, report:

1. **Files generated** - list each screenshot path
2. **Viewport info** - dimensions used
3. **Any errors** - failed captures with reasons

**Output format:**
```
Screenshots captured:

[1] ./screenshots/example_com_desktop.png (1280x720)
[2] ./screenshots/example_com_mobile.png (375x667)

Open: [1] desktop [2] mobile [3] all [4] skip
```

### Step 4: Offer to Open

Use the Read tool to display the screenshots to the user if they select an option.

---

## Viewport Presets

| Preset  | Width | Height | Description        |
|---------|-------|--------|--------------------|
| desktop | 1280  | 720    | Standard laptop    |
| tablet  | 768   | 1024   | iPad portrait      |
| mobile  | 375   | 667    | iPhone SE          |

---

## Advanced Options

### Full Page vs Viewport Only

```bash
# Capture entire page (default)
/screenshot example.com --full-page

# Capture only visible viewport
/screenshot example.com --no-full-page
```

### Scrolling for Lazy Content

```bash
# Scroll page before capture (triggers lazy loading)
/screenshot example.com --scroll

# Custom scroll delay (ms between scroll steps)
/screenshot example.com --scroll --scroll-delay 1000
```

### Wait Time

```bash
# Wait longer for dynamic content (default: 2000ms)
/screenshot example.com -w 5000
```

### Output Format

```bash
# JPEG with quality
/screenshot example.com -f jpeg -q 90
```

---

## Examples

### Responsive Testing
```bash
/screenshot mysite.com all -o ./responsive-test
```
Captures desktop, tablet, and mobile versions.

### Multiple Pages
```bash
/screenshot mysite.com/,mysite.com/about,mysite.com/contact all
```
Captures all pages in all viewports.

### Before/After Comparison
```bash
/screenshot staging.mysite.com,production.mysite.com -o ./comparison
```

---

## Troubleshooting

**Page timeout:**
- Site may be slow - try increasing wait time: `-w 10000`
- Check if URL is accessible

**Missing content:**
- Use `--scroll` flag for lazy-loaded content
- Increase `--scroll-delay` for slower sites

**Blank screenshots:**
- Ensure URL includes protocol or will default to https
- Some sites block headless browsers

---

## Dependencies

The tool uses:
- Playwright (Chromium)
- TypeScript

First run will install Chromium automatically via Playwright.
