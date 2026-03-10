---
description: Comprehensive website QA checklist (design system, meta tags, mobile, a11y, performance)
version: 2.0.0
---

# Website QA Checklist

Comprehensive QA validation for websites covering design system compliance, mobile responsiveness, meta tags, accessibility, performance, SEO, and code quality.

## Arguments

```
$ARGUMENTS = [options] URL_or_file

Options:
  --sections=<list>   Comma-separated sections to run (meta,mobile,design,a11y,perf,seo,security)
  --cache             Use cached results for non-specified sections
  --no-cache          Force fresh run, ignore cache
  --cache-file=<path> Custom cache file path (default: .qa-cache/{url-hash}.json)
  --show-cache        Display cached results without running checks

Examples:
  /website-qa-checklist https://example.com
  /website-qa-checklist --sections=a11y,perf https://example.com
  /website-qa-checklist --cache --sections=meta https://example.com
  /website-qa-checklist --show-cache https://example.com
```

## Section Aliases

| Alias | Full Name | Checks |
|-------|-----------|--------|
| `meta` | Meta Tags | 8 |
| `mobile` | Mobile/Responsive | 5 |
| `design` | Design System | 6 |
| `a11y` | Accessibility | 7 |
| `perf` | Performance | 5 |
| `seo` | SEO | 4 |
| `security` | Security | 3 |
| `code` | Code Quality | 4 |
| `all` | All sections | 42 |

## Cache System

### Cache Location
```
.qa-cache/
├── {url-hash}.json          # Cached results per URL
├── {url-hash}.meta.json     # Cache metadata (timestamp, sections)
└── index.json               # Index of all cached URLs
```

### Cache File Format
```json
{
  "target": "https://example.com",
  "timestamp": "2025-11-27T10:00:00Z",
  "content_hash": "abc123...",
  "sections": {
    "meta": {
      "run_at": "2025-11-27T10:00:00Z",
      "passed": 7,
      "total": 8,
      "status": "WARN",
      "results": [
        {"id": "META-01", "name": "Title tag", "passed": true, "found": "My Page Title"},
        {"id": "META-02", "name": "Meta description", "passed": true, "found": "Description..."}
      ]
    },
    "mobile": { ... },
    "design": { ... },
    "a11y": { ... },
    "perf": { ... },
    "seo": { ... },
    "security": { ... }
  },
  "summary": {
    "passed": 33,
    "total": 38,
    "grade": "B",
    "percentage": 87
  }
}
```

### Cache Behavior

| Command | Behavior |
|---------|----------|
| No flags | Run all sections, save to cache |
| `--sections=X` | Run only X, don't use cache |
| `--cache --sections=X` | Run X, load others from cache |
| `--no-cache` | Run all, don't read/write cache |
| `--show-cache` | Display cached results only |

### Cache Instructions

**Step 0: Parse Arguments**
```python
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

args = "$ARGUMENTS"
sections_to_run = None  # None = all
use_cache = False
show_cache_only = False
cache_file = None

# Parse flags
if "--sections=" in args:
    sections_str = args.split("--sections=")[1].split()[0]
    sections_to_run = [s.strip() for s in sections_str.split(",")]
    args = args.replace(f"--sections={sections_str}", "").strip()

if "--cache" in args:
    use_cache = True
    args = args.replace("--cache", "").strip()

if "--no-cache" in args:
    use_cache = False
    args = args.replace("--no-cache", "").strip()

if "--show-cache" in args:
    show_cache_only = True
    args = args.replace("--show-cache", "").strip()

if "--cache-file=" in args:
    cache_file = args.split("--cache-file=")[1].split()[0]
    args = args.replace(f"--cache-file={cache_file}", "").strip()

TARGET = args.strip()

# Generate cache path
def get_cache_path(target):
    url_hash = hashlib.md5(target.encode()).hexdigest()[:12]
    return Path(".qa-cache") / f"{url_hash}.json"

CACHE_PATH = cache_file or get_cache_path(TARGET)
```

**Step 0.1: Load Cache (if applicable)**
```python
cached_data = None
if use_cache or show_cache_only:
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            cached_data = json.load(f)
        print(f"Loaded cache from {CACHE_PATH}")
        print(f"Cached at: {cached_data['timestamp']}")
    else:
        print(f"No cache found at {CACHE_PATH}")
        if show_cache_only:
            print("Run without --show-cache to generate cache")
            exit(0)
```

**Step 0.2: Show Cache Only (if requested)**
```python
if show_cache_only and cached_data:
    # Display cached results in report format
    print_report(cached_data)
    exit(0)
```

**Step 0.3: Determine Sections to Run**
```python
ALL_SECTIONS = ["meta", "mobile", "design", "a11y", "perf", "seo", "security", "code"]

if sections_to_run is None:
    sections_to_run = ALL_SECTIONS
else:
    # Validate section names
    for s in sections_to_run:
        if s not in ALL_SECTIONS and s != "all":
            print(f"Unknown section: {s}")
            print(f"Valid sections: {', '.join(ALL_SECTIONS)}")
            exit(1)
    if "all" in sections_to_run:
        sections_to_run = ALL_SECTIONS

# If using cache, only run specified sections
if use_cache and cached_data:
    cached_sections = set(cached_data.get("sections", {}).keys())
    sections_from_cache = [s for s in ALL_SECTIONS if s not in sections_to_run and s in cached_sections]
    print(f"Running: {', '.join(sections_to_run)}")
    print(f"From cache: {', '.join(sections_from_cache)}")
```

## Check Categories

| Category | Checks | Deterministic | LLM | Weight |
|----------|--------|---------------|-----|--------|
| Meta Tags | 8 | 8 | 0 | Critical |
| Mobile/Responsive | 5 | 4 | 1 | Critical |
| Design System | 6 | 3 | 3 | Important |
| Accessibility | 7 | 5 | 2 | Critical |
| Performance | 5 | 5 | 0 | Important |
| SEO | 4 | 3 | 1 | Important |
| Security | 3 | 3 | 0 | Critical |
| Code Quality | 4 | 3 | 1 | Important |

**Total: 42 checks (34 deterministic + 8 LLM)**

## Check Types

### Deterministic Checks (31)
Pattern-matching, regex, and rule-based checks that produce consistent, reproducible results.
- Fast execution
- Cacheable indefinitely (until content changes)
- Binary pass/fail

### LLM Checks (7)
AI-evaluated checks requiring semantic understanding or subjective assessment.
- Requires content analysis
- Cache with content hash (re-run if content changes)
- May include confidence score

| ID | Check | Type | Why LLM? |
|----|-------|------|----------|
| MOBILE-04 | Touch target sizing | LLM | Requires visual/semantic assessment |
| DS-01 | Class naming consistency | LLM | Pattern recognition across codebase |
| DS-04 | Color palette coherence | LLM | Aesthetic judgment |
| DS-05 | Typography scale | LLM | Design system comprehension |
| A11Y-06 | Focus visible adequacy | LLM | Requires CSS analysis |
| A11Y-07 | Color contrast | LLM | Requires color extraction + math |
| SEO-04 | Descriptive link text | LLM | Semantic quality of anchor text |
| CODE-04 | Config completeness | LLM | Requires understanding of what should be configurable |

## Instructions

### Step 1: Fetch Content

```bash
TARGET="$ARGUMENTS"

# URL or local file
if [[ "$TARGET" =~ ^https?:// ]]; then
  CONTENT=$(curl -sL "$TARGET" --max-time 30)
  HEADERS=$(curl -sI "$TARGET" --max-time 10)
else
  CONTENT=$(cat "$TARGET")
  HEADERS=""
fi
```

### Step 2: Meta Tags (8 checks)

| ID | Check | Pattern | Severity |
|----|-------|---------|----------|
| META-01 | Title tag | `<title>.+</title>` | error |
| META-02 | Meta description | `<meta name="description"` | error |
| META-03 | Viewport | `<meta name="viewport"` | error |
| META-04 | OG Title | `<meta property="og:title"` | warning |
| META-05 | OG Description | `<meta property="og:description"` | warning |
| META-06 | OG Image | `<meta property="og:image"` | warning |
| META-07 | Twitter Card | `<meta name="twitter:card"` | warning |
| META-08 | Canonical URL | `<link rel="canonical"` | warning |

**Validation:**
```bash
# Check each meta tag
echo "$CONTENT" | grep -iE '<title>.+</title>'
echo "$CONTENT" | grep -i 'name="description"'
echo "$CONTENT" | grep -i 'name="viewport"'
echo "$CONTENT" | grep -i 'property="og:title"'
echo "$CONTENT" | grep -i 'property="og:description"'
echo "$CONTENT" | grep -i 'property="og:image"'
echo "$CONTENT" | grep -i 'name="twitter:card"'
echo "$CONTENT" | grep -i 'rel="canonical"'
```

### Step 3: Mobile/Responsive (5 checks)

| ID | Check | Type | Pattern | Severity |
|----|-------|------|---------|----------|
| MOBILE-01 | Viewport meta | DET | `width=device-width` | error |
| MOBILE-02 | Media queries | DET | `@media` in CSS | warning |
| MOBILE-03 | No fixed widths | DET | Absence of `width:\s*\d{4,}px` | warning |
| MOBILE-04 | Touch targets | **LLM** | Links/buttons sized adequately | info |
| MOBILE-05 | Responsive images | DET | `srcset` or `max-width: 100%` | warning |

**Deterministic Validation:**
```bash
# MOBILE-01: Viewport with device-width
echo "$CONTENT" | grep -i 'width=device-width'

# MOBILE-02: Media queries present
echo "$CONTENT" | grep -E '@media.*\(' | head -5

# MOBILE-03: Check for problematic fixed widths (>999px)
FIXED_WIDTH=$(echo "$CONTENT" | grep -oE 'width:\s*[0-9]{4,}px' | head -3)

# MOBILE-05: Responsive images
echo "$CONTENT" | grep -iE '(srcset=|max-width:\s*100%)'
```

**LLM Validation (MOBILE-04):**
```
Analyze the HTML/CSS for touch target sizing:

1. Extract all clickable elements (<a>, <button>, elements with onclick)
2. Check for explicit sizing (min-height, min-width, padding)
3. Look for touch-friendly CSS (min-height: 44px, padding patterns)

Evaluate:
- PASS: Most interactive elements appear to have adequate touch targets (44x44px minimum)
- WARN: Some elements may be too small for comfortable touch
- FAIL: Many elements appear too small for touch interaction

Respond with: {status: "PASS|WARN|FAIL", confidence: 0.0-1.0, details: "..."}
```

### Step 4: Design System (6 checks)

| ID | Check | Type | Pattern | Severity |
|----|-------|------|---------|----------|
| DS-01 | Consistent class naming | **LLM** | BEM, Tailwind, or semantic patterns | info |
| DS-02 | CSS variables | DET | `var(--` present | info |
| DS-03 | Font loading | DET | `<link.*font` or `@font-face` | info |
| DS-04 | Color consistency | **LLM** | Limited color palette | info |
| DS-05 | Typography scale | **LLM** | Consistent heading sizes | info |
| DS-06 | Component patterns | DET | Recognizable UI framework | info |

**Deterministic Validation:**
```bash
# DS-02: CSS Variables
CSS_VARS=$(echo "$CONTENT" | grep -oE 'var\(--[a-zA-Z0-9-]+\)' | sort -u | wc -l)

# DS-03: Font loading
echo "$CONTENT" | grep -iE '(fonts\.googleapis|@font-face|rel="preconnect".*fonts)'

# DS-06: Detect design framework
echo "$CONTENT" | grep -iE '(tailwind|shadcn|bootstrap|mui-|chakra|bulma)' | head -3

# Extract color variables for LLM analysis
echo "$CONTENT" | grep -oE 'var\(--[a-zA-Z]*color[a-zA-Z0-9-]*\)' | sort -u | head -10
```

**LLM Validation (DS-01, DS-04, DS-05):**
```
Analyze the HTML/CSS for design system coherence:

## DS-01: Class Naming Consistency
Extract class attributes and evaluate:
- Is there a consistent naming convention? (BEM: block__element--modifier, Tailwind: utility-first, semantic: descriptive)
- Are class names self-documenting?
- Is there mixing of conventions (bad) or consistent pattern (good)?

## DS-04: Color Palette Coherence
Extract all color values (hex, rgb, hsl, CSS vars):
- Count unique colors
- Are colors from a limited, intentional palette (<20 unique)?
- Are there near-duplicates that suggest inconsistency?

## DS-05: Typography Scale
Extract font-size declarations:
- Is there a consistent scale (e.g., 12, 14, 16, 20, 24, 32)?
- Are heading sizes proportional (h1 > h2 > h3)?
- Is there a clear hierarchy?

Respond with:
{
  "DS-01": {status: "PASS|WARN|INFO", confidence: 0.0-1.0, pattern: "BEM|Tailwind|semantic|mixed|none"},
  "DS-04": {status: "PASS|WARN|INFO", confidence: 0.0-1.0, unique_colors: N, assessment: "..."},
  "DS-05": {status: "PASS|WARN|INFO", confidence: 0.0-1.0, scale: [...], assessment: "..."}
}
```

### Step 5: Accessibility (7 checks)

| ID | Check | Type | Pattern | Severity |
|----|-------|------|---------|----------|
| A11Y-01 | Lang attribute | DET | `<html lang=` | error |
| A11Y-02 | Alt attributes | DET | All `<img` have `alt=` | error |
| A11Y-03 | Skip navigation | DET | Skip-to-content link | warning |
| A11Y-04 | Heading hierarchy | DET | h1 → h2 → h3 proper order | warning |
| A11Y-05 | ARIA landmarks | DET | `role=` or landmark elements | info |
| A11Y-06 | Focus visible | **LLM** | `:focus` styles adequate | warning |
| A11Y-07 | Color contrast | **LLM** | Text colors vs background | warning |

**Deterministic Validation:**
```bash
# A11Y-01: Lang attribute
echo "$CONTENT" | grep -iE '<html[^>]*lang='

# A11Y-02: Images without alt
IMAGES_TOTAL=$(echo "$CONTENT" | grep -oE '<img[^>]+>' | wc -l)
IMAGES_WITH_ALT=$(echo "$CONTENT" | grep -oE '<img[^>]+alt=' | wc -l)

# A11Y-03: Skip navigation
echo "$CONTENT" | grep -iE '(skip.*(nav|content|main)|#main-content)'

# A11Y-04: Heading hierarchy (extract all headings in order)
echo "$CONTENT" | grep -oE '<h[1-6][^>]*>' | head -10

# A11Y-05: ARIA landmarks
echo "$CONTENT" | grep -oE '(role="[^"]+"|<(main|nav|header|footer|aside|article)[^>]*>)' | head -5

# Extract focus styles for LLM
echo "$CONTENT" | grep -iE ':focus|focus-visible|outline:' | head -5
```

**LLM Validation (A11Y-06, A11Y-07):**
```
Analyze accessibility concerns requiring judgment:

## A11Y-06: Focus Visible Adequacy
Extract :focus and :focus-visible styles:
- Are focus states defined for interactive elements?
- Is outline preserved or appropriately replaced?
- Would keyboard users be able to track focus?

## A11Y-07: Color Contrast
This requires extracting color pairs and evaluating contrast:
1. Find text color declarations
2. Find corresponding background colors
3. Estimate if contrast ratio meets WCAG AA (4.5:1 for normal text, 3:1 for large)

Note: For accurate contrast, recommend running through automated tool (Lighthouse, axe).
Provide best-effort assessment based on visible color values.

Respond with:
{
  "A11Y-06": {status: "PASS|WARN|FAIL", confidence: 0.0-1.0, details: "..."},
  "A11Y-07": {status: "PASS|WARN|FAIL", confidence: 0.0-1.0, details: "...", recommendation: "Run Lighthouse for accurate contrast ratios"}
}
```

### Step 6: Performance (5 checks)

| ID | Check | Pattern | Severity |
|----|-------|---------|----------|
| PERF-01 | Async/defer scripts | `<script.*(async|defer)` | warning |
| PERF-02 | Image optimization | webp, avif, or lazy loading | info |
| PERF-03 | Critical CSS | Inline critical styles | info |
| PERF-04 | Resource hints | preload, prefetch, preconnect | info |
| PERF-05 | Minified assets | .min.js, .min.css | info |

**Validation:**
```bash
# Scripts with async/defer
SCRIPTS_TOTAL=$(echo "$CONTENT" | grep -oE '<script[^>]+src=' | wc -l)
SCRIPTS_OPTIMIZED=$(echo "$CONTENT" | grep -oE '<script[^>]*(async|defer)[^>]*src=' | wc -l)

# Lazy loading
echo "$CONTENT" | grep -iE '(loading="lazy"|data-src=|lazyload)'

# Resource hints
echo "$CONTENT" | grep -iE 'rel="(preload|prefetch|preconnect)"' | head -3

# WebP/AVIF images
echo "$CONTENT" | grep -oE '\.(webp|avif)"' | sort -u
```

### Step 7: SEO (4 checks)

| ID | Check | Type | Pattern | Severity |
|----|-------|------|---------|----------|
| SEO-01 | Robots meta | DET | `<meta name="robots"` or allowed | info |
| SEO-02 | Structured data | DET | `application/ld+json` | info |
| SEO-03 | Sitemap reference | DET | `sitemap.xml` | info |
| SEO-04 | Descriptive links | **LLM** | Links with meaningful text | warning |

**Deterministic Validation:**
```bash
# SEO-01: Robots meta
echo "$CONTENT" | grep -iE 'name="robots"'

# SEO-02: Structured data (JSON-LD)
echo "$CONTENT" | grep -i 'application/ld+json'

# SEO-03: Sitemap reference
echo "$CONTENT" | grep -iE 'sitemap\.xml'

# Extract links for LLM analysis
echo "$CONTENT" | grep -oE '<a[^>]*>[^<]+</a>' | head -20
```

**LLM Validation (SEO-04):**
```
Analyze anchor text quality for SEO:

Extract all <a> elements with their visible text.
Evaluate link text quality:

BAD patterns (flag these):
- "click here", "here", "read more", "learn more" (without context)
- "link", "this", "page"
- Single characters or numbers only
- URLs as link text

GOOD patterns:
- Descriptive text explaining destination
- Action-oriented text with context
- Product/page names

Count:
- Total links with text
- Links with generic/poor anchor text
- Percentage of quality links

Respond with:
{
  "SEO-04": {
    status: "PASS|WARN|FAIL",
    confidence: 0.0-1.0,
    total_links: N,
    generic_links: N,
    examples: ["bad example 1", "bad example 2"],
    percentage_good: N%
  }
}

Thresholds:
- PASS: >90% descriptive links
- WARN: 70-90% descriptive links
- FAIL: <70% descriptive links
```

### Step 8: Security (3 checks)

| ID | Check | Type | Pattern | Severity |
|----|-------|------|---------|----------|
| SEC-01 | HTTPS | DET | URL uses https:// | error |
| SEC-02 | No mixed content | DET | No http:// in https page | warning |
| SEC-03 | CSP header | DET | Content-Security-Policy | info |

**Deterministic Validation:**
```bash
# SEC-01: HTTPS check
if [[ "$TARGET" =~ ^https:// ]]; then
  echo "PASS: Using HTTPS"
elif [[ "$TARGET" =~ ^http:// ]]; then
  echo "FAIL: Using HTTP (insecure)"
else
  echo "INFO: Local file, HTTPS not applicable"
fi

# SEC-02: Mixed content check (http:// resources on https page)
if [[ "$TARGET" =~ ^https:// ]]; then
  MIXED=$(echo "$CONTENT" | grep -oE '(src|href)="http://[^"]+' | wc -l)
  echo "Mixed content resources: $MIXED"
fi

# SEC-03: CSP header (if URL)
if [[ -n "$HEADERS" ]]; then
  echo "$HEADERS" | grep -i 'content-security-policy'
fi
```



### Step 8.5: Code Quality (4 checks)

| ID | Check | Type | Pattern | Severity |
|----|-------|------|---------|----------|
| CODE-01 | Centralized config | DET | `site-config` or `siteConfig` file exists | warning |
| CODE-02 | No hardcoded site name | DET | Site name comes from config, not literals | warning |
| CODE-03 | No hardcoded URLs | DET | URLs come from config or env vars | warning |
| CODE-04 | Config completeness | **LLM** | Config covers all site metadata | info |

**Deterministic Validation:**
```bash
# CODE-01: Centralized config file exists
CONFIG_FILE=$(find src lib -name "*site*config*" -o -name "*siteConfig*" 2>/dev/null | head -1)
if [[ -n "$CONFIG_FILE" ]]; then
  echo "PASS: Config file found at $CONFIG_FILE"
else
  echo "WARN: No centralized site config file found"
fi

# CODE-02: Check for hardcoded site names in components
# Look for literal site name in layout/header/footer
HARDCODED_NAME=$(grep -rE '"(My Site|Portfolio|My Portfolio|Site Name)"' src/components src/app --include="*.tsx" --include="*.ts" 2>/dev/null | grep -v "config" | head -5)
if [[ -z "$HARDCODED_NAME" ]]; then
  echo "PASS: No obvious hardcoded site names"
else
  echo "WARN: Potential hardcoded site names found"
fi

# CODE-03: Check for hardcoded URLs
HARDCODED_URLS=$(grep -rE 'https?://[^"]+\.(com|io|dev|org)"' src/components src/app --include="*.tsx" --include="*.ts" 2>/dev/null | grep -v "config\|schema\.org\|googleapis\|cdn\." | head -5)
```

**LLM Validation (CODE-04):**
```
Analyze the site configuration file for completeness:

## CODE-04: Config Completeness
A well-organized site config should include:

REQUIRED fields (check all present):
- Site name/title
- Site description
- Site URL (from env var or default)
- Author name

RECOMMENDED fields (nice to have):
- Author email/contact
- Social links (GitHub, LinkedIn, Twitter)
- Navigation items array
- Footer content/copyright
- SEO defaults (OG image, locale)

BONUS fields (for advanced sites):
- Hero/landing page content
- Resume/about data
- Theme configuration
- Feature flags

Evaluate:
- PASS: All REQUIRED + most RECOMMENDED fields present
- WARN: All REQUIRED present, missing some RECOMMENDED
- FAIL: Missing REQUIRED fields
- INFO: Basic config exists but could be expanded

Respond with:
{
  "CODE-04": {
    status: "PASS|WARN|FAIL|INFO",
    confidence: 0.0-1.0,
    required_present: ["name", "description", ...],
    required_missing: [],
    recommended_present: [...],
    recommended_missing: [...],
    suggestion: "Consider adding X, Y, Z to config"
  }
}
```

**Config File Best Practices:**

A good site config file (`src/lib/site-config.ts`) should look like:

```typescript
export const siteConfig = {
  // Site metadata (REQUIRED)
  name: "Site Name",
  title: "Site Title",
  description: "Site description for SEO",
  url: process.env.NEXT_PUBLIC_SITE_URL || "https://example.com",

  // Author info (REQUIRED)
  author: {
    name: "Author Name",
    email: "email@example.com",
    // Optional extended info
    title: "Job Title",
    location: "City, Country",
    bio: "Short bio text",
  },

  // Social links (RECOMMENDED)
  social: {
    github: "github.com/username",
    linkedin: "linkedin.com/in/username",
    twitter: "@username",
  },

  // Navigation (RECOMMENDED)
  nav: [
    { label: "Blog", href: "/blog" },
    { label: "Projects", href: "/projects" },
    { label: "About", href: "/about" },
  ],

  // Footer (RECOMMENDED)
  footer: {
    copyright: "Built with Next.js",
  },

  // Hero section (BONUS)
  hero: {
    greeting: "Hello",
    headline: "Welcome to my site",
    cta: { label: "Learn More", href: "/about" },
  },
} as const;
```

**Why Config Abstraction Matters:**
1. **Single source of truth** - Change site name in one place, updates everywhere
2. **Environment flexibility** - Easy to configure for dev/staging/prod
3. **Maintainability** - New developers can find all site settings in one file
4. **Consistency** - Prevents typos and inconsistencies across pages
5. **Testability** - Easy to mock config in tests

### Step 9: Generate Report

```markdown
# Website QA Report

**Target**: {url_or_file}
**Tested**: {timestamp}
**Framework Detected**: {Tailwind/Bootstrap/shadcn/None}

## Summary

| Category | Passed | Total | Status |
|----------|--------|-------|--------|
| Meta Tags | X | 8 | {status} |
| Mobile/Responsive | X | 5 | {status} |
| Design System | X | 6 | {status} |
| Accessibility | X | 7 | {status} |
| Performance | X | 5 | {status} |
| SEO | X | 4 | {status} |
| Security | X | 3 | {status} |
| Code Quality | X | 4 | {status} |
| **TOTAL** | **X** | **42** | **{status}** |

## Detailed Results

### Meta Tags {emoji}

| Check | Status | Found |
|-------|--------|-------|
| Title | {PASS/FAIL} | {extracted title} |
| Description | {PASS/FAIL} | {first 60 chars} |
| Viewport | {PASS/FAIL} | {value} |
| OG Title | {PASS/FAIL} | {value} |
| OG Description | {PASS/FAIL} | {value} |
| OG Image | {PASS/FAIL} | {URL} |
| Twitter Card | {PASS/FAIL} | {type} |
| Canonical | {PASS/FAIL} | {URL} |

### Mobile/Responsive {emoji}

| Check | Status | Notes |
|-------|--------|-------|
| Viewport width | {PASS/FAIL} | {device-width or missing} |
| Media queries | {PASS/FAIL} | {count found} |
| Fixed widths | {PASS/WARN} | {issues if any} |
| Touch targets | {PASS/INFO} | {assessment} |
| Responsive images | {PASS/FAIL} | {srcset/max-width found} |

### Design System {emoji}

| Check | Status | Notes |
|-------|--------|-------|
| Class naming | {INFO} | {pattern detected} |
| CSS variables | {PASS/FAIL} | {count} custom properties |
| Font loading | {PASS/FAIL} | {fonts found} |
| Color palette | {INFO} | {count} colors detected |
| Typography | {INFO} | {assessment} |
| UI Framework | {INFO} | {detected or None} |

### Accessibility {emoji}

| Check | Status | Notes |
|-------|--------|-------|
| Lang attribute | {PASS/FAIL} | {lang value} |
| Image alt text | {PASS/FAIL} | {X}/{Y} images have alt |
| Skip navigation | {PASS/WARN} | {found or missing} |
| Heading hierarchy | {PASS/WARN} | {assessment} |
| ARIA landmarks | {PASS/INFO} | {count} landmarks |
| Focus visible | {PASS/WARN} | {assessment} |
| Color contrast | {PASS/WARN} | {assessment} |

### Performance {emoji}

| Check | Status | Notes |
|-------|--------|-------|
| Script loading | {PASS/WARN} | {X}/{Y} optimized |
| Image format | {PASS/INFO} | {webp/avif usage} |
| Critical CSS | {PASS/INFO} | {inline styles found} |
| Resource hints | {PASS/INFO} | {preload/prefetch count} |
| Minified assets | {PASS/INFO} | {assessment} |

### SEO {emoji}

| Check | Status | Notes |
|-------|--------|-------|
| Robots meta | {PASS/INFO} | {directive} |
| Structured data | {PASS/INFO} | {type found} |
| Sitemap | {PASS/INFO} | {reference found} |
| Link text | {PASS/WARN} | {generic links count} |

### Security {emoji}

| Check | Status | Notes |
|-------|--------|-------|
| HTTPS | {PASS/FAIL} | {protocol} |
| Mixed content | {PASS/FAIL} | {issues count} |
| CSP header | {PASS/INFO} | {present or missing} |



### Code Quality {emoji}

| Check | Status | Notes |
|-------|--------|-------|
| Config file | {PASS/WARN} | {path or missing} |
| Site name | {PASS/WARN} | {from config or hardcoded} |
| URLs | {PASS/WARN} | {from config/env or hardcoded} |
| Config completeness | {PASS/INFO} | {assessment} |

## Recommendations

### Critical (Must Fix)
{List any error-severity failures}

### Important (Should Fix)
{List any warning-severity failures}

### Suggestions (Nice to Have)
{List any info-severity improvements}

## Quick Fixes

{For each critical/important issue, provide copy-paste fix}
```

## Scoring

**Status Calculation:**
- **PASS**: All errors pass, <2 warnings fail
- **WARN**: All errors pass, 2+ warnings fail
- **FAIL**: Any error-severity check fails

**Grade Scale:**
- A: 35-38 checks pass (90%+)
- B: 30-34 checks pass (79-89%)
- C: 23-29 checks pass (60-78%)
- D: 15-22 checks pass (40-59%)
- F: <15 checks pass (<40%)

## Example Output

```
# Website QA Report

**Target**: https://example.com
**Tested**: 2025-11-27T10:00:00Z
**Framework Detected**: Tailwind CSS + shadcn/ui

## Summary

| Category | Passed | Total | Status |
|----------|--------|-------|--------|
| Meta Tags | 7 | 8 | WARN |
| Mobile/Responsive | 5 | 5 | PASS |
| Design System | 6 | 6 | PASS |
| Accessibility | 5 | 7 | WARN |
| Performance | 4 | 5 | PASS |
| SEO | 3 | 4 | PASS |
| Security | 3 | 3 | PASS |
| Code Quality | 4 | 4 | PASS |
| **TOTAL** | **37** | **42** | **B (88%)** |



### Code Quality {emoji}

| Check | Status | Notes |
|-------|--------|-------|
| Config file | {PASS/WARN} | {path or missing} |
| Site name | {PASS/WARN} | {from config or hardcoded} |
| URLs | {PASS/WARN} | {from config/env or hardcoded} |
| Config completeness | {PASS/INFO} | {assessment} |

## Recommendations

### Critical (Must Fix)
None

### Important (Should Fix)
1. META-08: Add canonical URL
2. A11Y-03: Add skip navigation link
3. A11Y-05: Add more ARIA landmarks

### Quick Fixes

**Canonical URL:**
<link rel="canonical" href="https://example.com/page">

**Skip Navigation:**
<a href="#main" class="sr-only focus:not-sr-only">Skip to content</a>
```

## Integration with /qa-microsite

This command complements `/qa-microsite`:
- `/qa-microsite` - Checks branding requirements (copyright, email, git info)
- `/website-qa-checklist` - Checks technical quality (meta, a11y, performance)

**Full QA Workflow:**
```bash
# Step 1: Deploy
/publish path/to/site

# Step 2: Brand QA
/qa-microsite https://deployed-url.com

# Step 3: Technical QA
/website-qa-checklist https://deployed-url.com
```

### Step 10: Save Cache

After running checks, save results to cache:

```python
import json
import hashlib
from pathlib import Path
from datetime import datetime

def save_cache(target, results, sections_run):
    """Save QA results to cache file."""
    cache_dir = Path(".qa-cache")
    cache_dir.mkdir(exist_ok=True)

    url_hash = hashlib.md5(target.encode()).hexdigest()[:12]
    cache_path = cache_dir / f"{url_hash}.json"

    # Load existing cache if present
    existing = {}
    if cache_path.exists():
        with open(cache_path) as f:
            existing = json.load(f)

    # Merge new results with existing
    timestamp = datetime.utcnow().isoformat() + "Z"
    content_hash = hashlib.md5(CONTENT.encode()).hexdigest()[:16]

    cache_data = {
        "target": target,
        "timestamp": timestamp,
        "content_hash": content_hash,
        "sections": existing.get("sections", {})
    }

    # Update sections that were run
    for section in sections_run:
        cache_data["sections"][section] = {
            "run_at": timestamp,
            "content_hash": content_hash,
            **results[section]
        }

    # Calculate summary
    total_passed = sum(s.get("passed", 0) for s in cache_data["sections"].values())
    total_checks = sum(s.get("total", 0) for s in cache_data["sections"].values())
    percentage = int((total_passed / total_checks) * 100) if total_checks > 0 else 0

    grade = "A" if percentage >= 90 else "B" if percentage >= 79 else "C" if percentage >= 60 else "D" if percentage >= 40 else "F"

    cache_data["summary"] = {
        "passed": total_passed,
        "total": total_checks,
        "grade": grade,
        "percentage": percentage
    }

    # Save cache
    with open(cache_path, "w") as f:
        json.dump(cache_data, f, indent=2)

    print(f"Cache saved to {cache_path}")

    # Update index
    index_path = cache_dir / "index.json"
    index = {}
    if index_path.exists():
        with open(index_path) as f:
            index = json.load(f)

    index[url_hash] = {
        "target": target,
        "last_run": timestamp,
        "grade": grade
    }

    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)

# Call after generating report
if not show_cache_only:
    save_cache(TARGET, results, sections_run)
```

### Step 11: Display Cache Info in Report

When using cached results, indicate which sections are from cache:

```markdown
## Summary

| Category | Passed | Total | Status | Source |
|----------|--------|-------|--------|--------|
| Meta Tags | 7 | 8 | WARN | **FRESH** |
| Mobile/Responsive | 5 | 5 | PASS | cached (2h ago) |
| Design System | 6 | 6 | PASS | cached (2h ago) |
| Accessibility | 5 | 7 | WARN | **FRESH** |
| Performance | 4 | 5 | PASS | cached (2h ago) |
| SEO | 3 | 4 | PASS | cached (2h ago) |
| Security | 3 | 3 | PASS | cached (2h ago) |
```

## Cache Management Commands

```bash
# Show all cached URLs
/website-qa-checklist --list-cache

# Clear cache for specific URL
/website-qa-checklist --clear-cache https://example.com

# Clear all cache
/website-qa-checklist --clear-all-cache

# Show cache age
/website-qa-checklist --cache-info https://example.com
```

## LLM Check Execution

When running LLM checks, use this execution pattern:

```python
def run_llm_checks(content, sections_to_run):
    """Execute LLM-based checks."""
    llm_checks = {
        "mobile": ["MOBILE-04"],
        "design": ["DS-01", "DS-04", "DS-05"],
        "a11y": ["A11Y-06", "A11Y-07"],
        "seo": ["SEO-04"]
    }

    results = {}

    for section in sections_to_run:
        if section in llm_checks:
            # Prepare context for LLM
            context = extract_relevant_content(content, section)

            # Call LLM with section-specific prompt
            llm_result = evaluate_with_llm(context, section)

            # Parse and validate response
            for check_id in llm_checks[section]:
                results[check_id] = {
                    "passed": llm_result[check_id]["status"] in ["PASS", "INFO"],
                    "status": llm_result[check_id]["status"],
                    "confidence": llm_result[check_id]["confidence"],
                    "details": llm_result[check_id].get("details", ""),
                    "type": "LLM"
                }

    return results
```

## Rerun Workflow Examples

**Full run (first time):**
```bash
/website-qa-checklist https://example.com
# Runs all 38 checks, saves to cache
```

**Quick recheck of failed sections:**
```bash
/website-qa-checklist --cache --sections=meta,a11y https://example.com
# Only runs meta (8) + a11y (7) = 15 checks
# Uses cached results for other 23 checks
```

**Rerun only LLM checks:**
```bash
/website-qa-checklist --cache --sections=mobile,design,a11y,seo --llm-only https://example.com
# Only runs 7 LLM checks, uses cache for 31 deterministic
```

**Force fresh run ignoring cache:**
```bash
/website-qa-checklist --no-cache https://example.com
# Runs all 38 checks fresh
```

## Notes

- All severity levels are recommendations; adjust based on project needs
- Design system checks are informational (no strict pass/fail)
- LLM checks include confidence scores - low confidence suggests manual review
- Deterministic checks are cached until content changes
- LLM checks are re-cached when content hash changes
- Run both local (pre-deploy) and remote (post-deploy) for complete coverage
