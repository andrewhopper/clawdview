---
uuid: cmd-polish-8l9m0n1o
version: 1.0.0
last_updated: 2025-11-10
description: Skip write-to-top audit, only densify
---

# Polish Document

Comprehensive document improvement: audit/fix writing structure (write to top principles) then compress (densify). Two-pass optimization for maximum clarity and brevity.

## What This Does

**Pass 1: Write to Top** (unless `--skip-structure`)
- Audit document for BLUF, inverted pyramid, executive summaries
- Score 6 principles (0-10 each)
- If `--fix` flag: apply structural improvements
- If no `--fix`: show audit report only

**Pass 2: Densify**
- Compress verbose text → technical format
- Remove filler, use arrows, bullets over prose
- Target 60-70% reduction while preserving meaning

**Result:** Well-structured + concise document following best practices

## Modes

### Mode 1: Audit Only (no --fix)

```bash
/polish ./docs/design.md
```

**Output:**
1. Write-to-top audit scores + recommendations
2. Densification preview (shows what would be compressed)
3. No file modifications
4. Run `/polish ./docs/design.md --fix` to apply

### Mode 2: Full Polish (--fix)

```bash
/polish ./docs/design.md --fix
```

**Output:**
1. Apply write-to-top improvements (restructure)
2. Apply densification (compress)
3. Show before/after metrics for both passes
4. File modified with all improvements

### Mode 3: Densify Only (--skip-structure)

```bash
/polish ./docs/design.md --skip-structure
```

**Output:**
1. Skip write-to-top audit
2. Apply densification only
3. Useful when structure is already good

## Instructions

### Step 1: Parse Flags

1. **Check command arguments**:
   - `--fix` present? → Apply improvements
   - `--skip-structure` present? → Skip pass 1
   - No flags? → Audit-only mode

### Step 2: Write to Top Pass

2. **If NOT `--skip-structure`**:

   a. **Read document**: Use Read tool on `{file_path}`

   b. **Analyze structure**:
      - Score 6 principles (exec summary, BLUF, inverted pyramid, section BLUF, headings, hierarchy)
      - Identify specific issues with line numbers
      - Generate fix recommendations

   c. **If `--fix` flag present**:
      - Apply structural improvements:
        - Add executive summary if missing
        - Restructure intro with BLUF
        - Improve headings (front-load conclusions)
        - Add section summaries
        - Reorder sections (critical → details → background)
      - Track changes made

   d. **If `--fix` NOT present**:
      - Show audit report only
      - List recommendations
      - Skip to Step 4 (preview densification but don't apply)

### Step 3: Densify Pass

3. **Apply densification**:

   a. **Read current content** (post-restructuring if --fix was used)

   b. **Apply compression**:
      - Remove filler words (very, really, basically, essentially)
      - Convert prose → bullets
      - Use `→` instead of verbose connectors
      - Apply tech abbreviations (k8s, postgres, dynamo)
      - Preserve brand names and critical details

   c. **Calculate metrics**:
      - Original character count
      - Compressed character count
      - Reduction percentage

   d. **If `--fix` flag present**:
      - Apply densification using Edit tool
      - Save changes to file

   e. **If `--fix` NOT present**:
      - Show preview of densified content
      - Don't modify file

### Step 4: Report Results

4. **Output combined report**:

**Audit Mode (no --fix):**

```markdown
# Document Polish Audit: {filename}

## Pass 1: Write to Top Analysis

**Overall Score:** {score}/10
**Assessment:** {Excellent/Good/Needs Work/Poor}

### Scores by Principle

| Principle | Score | Issue |
|-----------|-------|-------|
| Executive summary | {score}/10 | {issue or ✅} |
| BLUF intro | {score}/10 | {issue or ✅} |
| Inverted pyramid | {score}/10 | {issue or ✅} |
| Section BLUF | {score}/10 | {issue or ✅} |
| Front-loaded headings | {score}/10 | {issue or ✅} |
| Clear hierarchy | {score}/10 | {issue or ✅} |

### Key Issues

🔴 **CRITICAL:** Missing executive summary
⚠️ **WARNING:** BLUF missing (recommendation at line 243)
💡 **SUGGESTION:** Improve 5 headings to front-load conclusions

### Recommendations

1. Add 2-3 sentence executive summary
2. Move recommendation to paragraph 1
3. Rewrite headings to include conclusions
4. Add section summaries

---

## Pass 2: Densification Preview

**Current:** {chars} chars
**Densified:** {chars} chars
**Potential Reduction:** {%}%

### Example Compression

**Before:**
```
We need to implement a comprehensive microservices architecture
with an API gateway for routing requests, a service mesh for
inter-service communication, and deploy everything to Kubernetes
with Istio for traffic management.
```

**After:**
```
Implement microservices: API gateway + service mesh, deploy to k8s+Istio
```

---

## Summary

**No changes made.** Run with `--fix` to apply improvements:

```bash
/polish {file_path} --fix
```

**Expected improvements:**
- Structure: {before}/10 → ~{estimated after}/10
- Length: {chars} → ~{estimated chars} ({%}% reduction)
```

**Fix Mode (--fix present):**

```markdown
# Document Polish Applied: {filename}

## Pass 1: Write to Top Improvements

### Changes Made

✅ Added executive summary (3 sentences, 287 chars)
✅ Restructured introduction with BLUF
✅ Improved 5 headings to front-load conclusions
✅ Added section BLUF to 3 sections
✅ Reordered sections (moved background to appendix)

### Score Improvement

| Principle | Before | After | Δ |
|-----------|--------|-------|---|
| Executive summary | 0/10 | 9/10 | +9 |
| BLUF intro | 2/10 | 8/10 | +6 |
| Inverted pyramid | 4/10 | 8/10 | +4 |
| Section BLUF | 3/10 | 7/10 | +4 |
| Front-loaded headings | 5/10 | 9/10 | +4 |
| Clear hierarchy | 6/10 | 8/10 | +2 |

**Overall:** 3.3/10 → 8.2/10 (+4.9)

---

## Pass 2: Densification Applied

### Compression Results

**Original:** 4,523 chars (post-restructuring)
**Densified:** 2,145 chars
**Reduction:** 52.6%

### Example Improvements

**Before (verbose):**
```
## Database Analysis and Selection Process

After conducting an extensive analysis of multiple database options
including PostgreSQL, MySQL, MongoDB, and DynamoDB, and considering
various factors such as scalability, operational complexity, and cost
implications, we have determined that PostgreSQL provides the best
balance for our requirements.
```

**After (BLUF + densified):**
```
## Database Selection: PostgreSQL for ACID + Scale

PostgreSQL recommended. Analysis of 4 options (postgres, mysql, mongo, dynamo)
shows best balance: ACID compliance, horizontal scaling, $2K/mo ops cost.
See comparison table below.
```

---

## Combined Metrics

**Structure:** 3.3/10 → 8.2/10 (+4.9)
**Length:** 6,789 chars → 2,145 chars (-68.4%)
**Readability:** Significantly improved

✅ File updated: {file_path}
```

**Skip Structure Mode (--skip-structure):**

```markdown
# Document Densified: {filename}

(Write to top audit skipped via --skip-structure flag)

## Densification Applied

**Original:** 4,523 chars
**Densified:** 2,145 chars
**Reduction:** 52.6%

### Example Compressions

[Show before/after examples]

✅ File updated: {file_path}
```

## Flag Combinations

| Command | Pass 1 (Structure) | Pass 2 (Densify) | File Modified? |
|---------|-------------------|------------------|----------------|
| `/polish file.md` | Audit only | Preview only | ❌ No |
| `/polish file.md --fix` | Apply fixes | Apply densify | ✅ Yes |
| `/polish file.md --skip-structure` | Skip | Preview only | ❌ No |
| `/polish file.md --skip-structure --fix` | Skip | Apply densify | ✅ Yes (densify only) |

## Use Cases

### Use Case 1: Quick Assessment

**Command:** `/polish ./docs/design.md`

**When:** Before sending doc to stakeholders, want to check quality
**Result:** Audit report + densification preview, no changes made
**Next:** Review recommendations, run with `--fix` if needed

### Use Case 2: Full Polish

**Command:** `/polish ./docs/design.md --fix`

**When:** Doc needs comprehensive improvement
**Result:** Restructured + compressed, significant quality boost
**Next:** Review changes, potentially run `/cite` to add references

### Use Case 3: Already Well-Structured

**Command:** `/polish ./docs/architecture.md --skip-structure --fix`

**When:** Structure is good, just needs compression
**Result:** Densified only (no restructuring)
**Next:** Done!

### Use Case 4: Iterative Review

**Command:**
```bash
/polish ./docs/proposal.md              # Initial audit
# Review recommendations, make manual edits
/polish ./docs/proposal.md --fix        # Apply remaining improvements
```

**When:** Want to make some manual adjustments before auto-polish
**Result:** Hybrid manual + automated improvement

## Integration Examples

### Pre-Commit Polish

```bash
# Before committing important docs
/polish ./docs/design.md --fix
git add docs/design.md
git commit -m "Polish design doc (structure + densify)"
```

### Documentation Pipeline

```bash
# Full documentation improvement pipeline
/polish ./docs/architecture.md --fix     # Structure + compress
/cite ./docs/architecture.md             # Add citations
git commit -m "Polish and cite architecture doc"
```

### Quick Cleanup

```bash
# Already structured well, just compress
/polish ./docs/*.md --skip-structure --fix
```

## Quality Metrics

**Good document after polish:**
- Write to top score: 8.0+/10
- Length reduction: 50-70%
- Executive summary present
- BLUF in introduction
- Front-loaded headings
- 60-70% fewer characters while preserving 95%+ meaning

**Excellent document after polish:**
- Write to top score: 9.0+/10
- Length reduction: 60-75%
- All 6 principles scoring 8+/10
- Clear hierarchical structure
- Dense but readable

## Error Handling

**File doesn't exist:**
```
Error: File not found: {file_path}
Check path and try again.
```

**Already optimal:**
```
# Document Polish Audit: {filename}

✅ Document already excellent!

**Write to top score:** 9.4/10
**Current length:** Already concise (minimal reduction possible)

No improvements needed. Document follows best practices.
```

**Only minor improvements possible:**
```
# Document Polish Audit: {filename}

**Write to top score:** 8.1/10 (good)
**Densification potential:** 15% reduction (moderate verbosity)

Minor improvements available. Run with --fix if desired, but document
already meets quality standards.
```

## Comparison with Individual Commands

| Scenario | Use `/polish` | Use Individual Commands |
|----------|--------------|------------------------|
| Need both structure + compression | ✅ Yes - one command | `/write-to-top --fix` then `/densify` |
| Only need structure audit | ❌ No | `/write-to-top` (no --fix) |
| Only need compression | Use `--skip-structure --fix` | `/densify` |
| Want granular control | ❌ No | Run individually |
| Quick quality check | ✅ Yes - audit mode | Run both audits separately |

## Key Principles

1. **Two-pass optimization**: Structure first, then compress
2. **Web-compatible**: Non-interactive, all flags upfront
3. **Audit before fix**: Default mode shows what would change
4. **Composable**: Can skip passes via flags
5. **Transparent**: Shows exactly what changed and why
6. **Metrics-driven**: Quantifies improvements (scores + percentages)

## Advanced Usage

### Batch Processing (Manual)

```bash
# Audit all docs first
/polish ./docs/design.md
/polish ./docs/architecture.md
/polish ./docs/api.md

# Review recommendations, then fix
/polish ./docs/design.md --fix
/polish ./docs/architecture.md --skip-structure --fix  # Structure already good
/polish ./docs/api.md --fix
```

### Pre-Publication Checklist

```bash
# 1. Polish structure + compress
/polish ./docs/whitepaper.md --fix

# 2. Add citations
/cite ./docs/whitepaper.md

# 3. Final review
# (Manual review)

# 4. Commit
git add docs/whitepaper.md
git commit -m "Polish whitepaper for publication"
```

## Success Criteria

**Command succeeds when:**
- Audit mode: Provides actionable scores + recommendations
- Fix mode: Applies improvements, file structurally sound + concise
- Metrics shown: Clear before/after comparison
- No meaning lost: 95%+ semantic preservation
- Respects flags: --skip-structure and --fix work as expected

**Output quality:**
- Write to top score improved by 3+ points (if --fix)
- Length reduced by 50-70% (if --fix)
- Executive summary present
- BLUF structure throughout
- Dense but readable

Be efficient, transparent, and improvement-focused.
