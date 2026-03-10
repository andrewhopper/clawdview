# Research Person Command

Research a person across multiple sources and generate a comprehensive, cited dossier with a Vite microsite.

## Arguments
- `$ARGUMENTS` - Person's name and optional company (e.g., "John Smith at Acme Corp")

## Instructions

You are researching **$ARGUMENTS** to build a comprehensive dossier.

---

## PHASE 0: Check Prior Targets

### Step 0.1: Load Prior Targets
Check if person was previously researched:

```bash
# Read prior_targets.json
cat projects/shared/active/claude-person-searcher-iyauu-209/prior_targets.json
```

### Step 0.2: Auto-Selection Logic
Search for matching name (case-insensitive, partial match OK):

**If match found:**
```
## Prior Research Found

Found existing dossier for "[Name]":
- **Role:** [Title] at [Company]
- **Location:** [Location]
- **Last Researched:** [Date]
- **Dossier URL:** [Published URL]

Options:
1. **View existing** - Open published dossier
2. **Re-research** - Update with fresh data
3. **New search** - Search for different person

Select option: _
```

**If no match:** Proceed to Phase 1 (Target Confirmation)

---

## PHASE 1: Target Confirmation

### Step 1.1: Initial Search
Search for the person to identify potential matches:
```
"[Name]" LinkedIn profile
"[Name]" [Company if provided]
```

### Step 1.2: Present Candidates
Display a numbered list of potential matches:

```
## Target Confirmation

Found potential matches for "[Name]":

1. **[Full Name]**
   - Current: [Title] at [Company]
   - Location: [City, State/Country]
   - Profiles: [LinkedIn](url) | [GitHub](url) | [Twitter](url)

2. **[Full Name]**
   - Current: [Title] at [Company]
   - Location: [City, State/Country]
   - Profiles: [LinkedIn](url) | [Twitter](url)

---
**Confirm who you want to research:** Enter number(s) or "all"
```

### Step 1.3: Wait for Confirmation
**STOP and wait for user to confirm which target(s) to research.**

Do NOT proceed until the user confirms by selecting 1, 2, etc.

---

## PHASE 2: Deep Research (After Confirmation)

### Step 2.1: Parallel Source Search
Search ALL sources in parallel for the confirmed target:

| # | Source | Search Query | Data to Extract |
|---|--------|--------------|-----------------|
| 1 | LinkedIn | "[Name]" "[Company]" site:linkedin.com | Title, company, location, history, **photo** |
| 2 | GitHub | "[Name]" OR "[username]" site:github.com | Username, repos, bio, contributions |
| 3 | Twitter/X | "[Name]" site:twitter.com OR site:x.com | Handle, bio, followers, **recent tweets** |
| 4 | YouTube | site:youtube.com "[Name]" [Company] talk | **Videos, conference talks** |
| 5 | Medium | "[Name]" site:medium.com | **Blog posts, articles** |
| 6 | Substack | "[Name]" site:substack.com | **Newsletter, articles** |
| 7 | Crunchbase | "[Name]" site:crunchbase.com | Investments, founded companies |
| 8 | AngelList | "[Name]" site:wellfound.com OR site:angel.co | Startup activity, investments |
| 9 | Company | "[Company]" team OR about page | Bio, **photo**, role |
| 10 | Podcast | "[Name]" podcast interview episode | **Podcast appearances** |
| 11 | Conference | "[Name]" conference talk presentation | **Speaking engagements** |
| 12 | LinkedIn Posts | "[Name]" LinkedIn recent post 2024 2025 | **Recent activity** |
| 13 | Stack Overflow | "[Name]" site:stackoverflow.com | Developer profile |
| 14 | Personal Site | "[Name]" personal website blog | **Blog, about page** |

**IMPORTANT:** Track ALL sources checked, even if no data found.

### Step 2.2: Citation Requirements

**CRITICAL: Every data point MUST have a source citation.**

Use inline citation format: `[fact]^[N]` where N links to Sources section.

Example:
```
- **Current Role:** AI Team Leader at AWS^[1]
- **Location:** Boston, MA^[1]
- **Education:** Eckerd College, Computer Science^[2]
```

Sources section:
```
## Sources
1. [LinkedIn Profile](https://linkedin.com/in/...) - Retrieved 2025-11-22
2. [Crunchbase](https://crunchbase.com/person/...) - Retrieved 2025-11-22
```

---

## PHASE 3: Build Cited Dossier

### Step 3.1: Dossier Structure

```markdown
# Dossier: [Name]
> Generated: [ISO Date] | Sources: [N] verified | Platforms Checked: [M]

## Overview
| Field | Value | Source |
|-------|-------|--------|
| **Photo** | ![Photo](url) or "Not found" | ^[N] |
| **Current Title** | [Role]^[1] | ^[1] |
| **Company** | [Company]^[1] | ^[1] |
| **Location** | [City, Country]^[1] | ^[1] |

## Professional Summary
[2-3 sentences with inline citations^[N]]

## Work Experience
1. **[Title]** at [Company] ([dates])^[N]
   - [Achievement or responsibility]^[N]
2. **[Title]** at [Company] ([dates])^[N]
...

## Education
- **[School]** - [Degree], [Year]^[N]

## Social Profiles
| Platform | URL | Verified |
|----------|-----|----------|
| LinkedIn | [URL]^[1] | ✓ |
| GitHub | [URL]^[2] | ✓ |
| Twitter | [URL]^[3] | ✓ |

## Personality Analysis
*Estimated from public content - speculative*

### MBTI Estimate: [TYPE]
- **Confidence:** [low/medium/high]
- **Evidence:** [Specific behaviors observed]^[N]

### Scores
| Dimension | Score | Evidence |
|-----------|-------|----------|
| Innovation | X/10 | [Why]^[N] |
| Adaptiveness | X/10 | [Why]^[N] |

### Key Traits (with evidence)
- [Trait]: [Evidence]^[N]

## Content & Media

### Videos & Talks
- [Title] - [Event] ([URL])^[N]

### Articles
- [Title] - [Publication] ([URL])^[N]

## Media & Content

### Podcasts
- [Title] - [Show] Ep [N] ([URL])^[N]

### YouTube
- [Title] - [Channel] ([URL])^[N]

### Conference Talks
- [Event] - [Topic] ([Year])^[N]

### Blog Posts
- [Title] - [Platform] ([URL])^[N]

## Recent Activity
| Date | Platform | Content |
|------|----------|---------|
| [Date] | LinkedIn | [Post summary] |
| [Date] | Twitter | [Tweet summary] |

## Cited Sources
| # | Type | URL | Retrieved |
|---|------|-----|-----------|
| 1 | LinkedIn | [URL] | [Date] |
| 2 | GitHub | [URL] | [Date] |
| 3 | Twitter | [URL] | [Date] |
...

## All Sources Checked
| Platform | Found | URL |
|----------|-------|-----|
| LinkedIn | ✓ | [URL] |
| GitHub | ✗ | - |
| Twitter/X | ✗ | - |
| Crunchbase | ✓ | [URL] |
| AngelList | ✗ | - |
| YouTube | ✗ | - |
| Medium | ✗ | - |
| Substack | ✗ | - |
| Stack Overflow | ✓ | [URL] |
| Podcast | ✓ | [URL] |
| Personal Website | ✗ | - |
```

---

## PHASE 4: Generate Vite Microsite

### Step 4.1: Create Vite Project
After completing research, generate a single-page Vite microsite:

```bash
# Create in prototype directory
cd projects/shared/active/claude-person-searcher-iyauu-209/microsites
mkdir -p [safe-name]
cd [safe-name]

# Initialize minimal Vite project
cat > package.json << 'PACKAGE'
{
  "name": "dossier-[safe-name]",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
PACKAGE

# Create vite.config.js
cat > vite.config.js << 'VITE'
import { defineConfig } from 'vite'
export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    assetsInlineLimit: 100000
  }
})
VITE
```

### Step 4.2: Generate index.html
Create a styled single-page dossier with all data embedded:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dossier: [Name]</title>
  <style>
    /* Modern, professional styling */
    :root {
      --primary: #2563eb;
      --primary-dark: #1d4ed8;
      --bg: #f8fafc;
      --card: #ffffff;
      --text: #1e293b;
      --text-muted: #64748b;
      --border: #e2e8f0;
    }
    /* ... full styles ... */
  </style>
</head>
<body>
  <div id="app">
    <!-- Dossier content with citations -->
  </div>
  <script type="module">
    // Dossier data embedded as JSON
    const dossier = { /* ... */ };
    // Render logic
  </script>
</body>
</html>
```

### Step 4.3: Build Static Site
```bash
npm install
npm run build
```

Output: `dist/index.html` (single file with inlined assets)

---

## PHASE 5: Auto-Publish & Verify

### Step 5.1: Generate, Publish, and Verify
Use the microsite generator with publish and verify flags:

```bash
cd projects/shared/active/claude-person-searcher-iyauu-209

# Save dossier JSON first
cat > microsites/[safe-name]/dossier.json << 'DOSSIER'
{
  "name": "[Full Name]",
  "headline": "[Title at Company]",
  ...
}
DOSSIER

# Generate, build, publish, and verify in one command
python3 generate_microsite.py microsites/[safe-name]/dossier.json --publish --verify
```

### Step 5.2: Verification Check
The script automatically:
1. Uploads to S3
2. Generates presigned URL
3. Makes HEAD request to verify:
   - HTTP 200 status
   - Content-Type: text/html
4. Reports PASSED or FAILED

If verification fails, investigate and retry.

### Step 5.3: Return Results
Present to user:

```
## Research Complete

**Subject:** [Full Name]
**Sources:** [N] verified citations
**Generated:** [ISO Date]

### Microsite Published
🔗 **[Click to view dossier](presigned-url)**
*(Link valid for 7 days)*

### Files Generated
- `microsites/[name]/dist/index.html` - Static site
- `microsites/[name]/dossier.json` - Raw data
- `microsites/[name]/dossier.md` - Markdown version
```

---

## PHASE 6: Update Target Registry & Index

### Step 6.1: Update prior_targets.json
After successful publish, add/update target in registry:

```python
# Add to prior_targets.json
new_target = {
    "name": "[Full Name]",
    "slug": "[safe-name]",
    "company": "[Company]",
    "role": "[Title]",
    "location": "[Location]",
    "linkedin_url": "[LinkedIn URL]",
    "researched_date": "[YYYY-MM-DD]",
    "dossier_path": "microsites/[safe-name]/dossier.json",
    "published_url": "[S3 Presigned URL]"
}
```

### Step 6.2: Generate Index Page (if multiple targets)
When `prior_targets.json` has 2+ entries, generate index:

```bash
cd projects/shared/active/claude-person-searcher-iyauu-209
python3 generate_index.py
```

This creates `index.html` with:
- List of all researched people
- Photos (if available)
- Quick links to dossiers
- Search/filter functionality

### Step 6.3: Publish Index
```bash
python3 generate_index.py --publish --verify
```

---

## Quality Checklist

Before publishing, verify:
- [ ] Every fact has a citation^[N]
- [ ] All source URLs are valid
- [ ] Personality analysis marked as speculative
- [ ] No private/non-public information included
- [ ] Vite build succeeded
- [ ] S3 upload returned presigned URL

---

## Example Flow

**Input:** "Satya Nadella"

**Phase 1 Output:**
```
Found potential matches for "Satya Nadella":

1. **Satya Nadella**
   - Current: CEO at Microsoft
   - Location: Bellevue, WA
   - Profiles: [LinkedIn](url) | [Twitter](url)

Confirm who you want to research: _
```

**User:** "1"

**Phase 2-5:** Deep research → Cited dossier → Vite build → Publish

**Final Output:**
```
## Research Complete

**Subject:** Satya Nadella
**Sources:** 12 verified citations
**Generated:** 2025-11-22T13:45:00Z

### Microsite Published
🔗 **[Click to view dossier](https://...s3.amazonaws.com/dossiers/satya-nadella/...)**
*(Link valid for 7 days)*
```
