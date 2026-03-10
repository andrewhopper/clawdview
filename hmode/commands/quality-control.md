---
uuid: cmd-quality-4r5s6t7u
version: 1.0.0
last_updated: 2025-11-10
description: Path to file or directory to validate
---

# Quality Control Agent

Validate markdown documents against quality standards.

## Parameter Handling

**If file_path not provided**: Prompt user for file or directory to check

**If directory provided**: Check all `.md` files in directory

**If file provided**: Check single file

## Quality Checks

### 1. LENGTH VALIDATION
- Flag files that are excessively long (>2000 words)
- Suggest splitting into multiple documents

### 2. READABILITY VALIDATION
- ✅ **Short paragraphs**: Max 5-6 sentences
- ✅ **Bullet points**: Used for lists/facts
- ✅ **Tables**: Used for structured data
- ✅ **White space**: Blank lines between sections
- ✅ **Bold numbers**: Key metrics bolded
- ❌ **FAIL**: Very long prose paragraphs (10+ sentences)

### 3. ENTITY LINKING VALIDATION
- ✅ **URLs**: All URLs use markdown format `[Text](URL)`
- ✅ **Internal references**: Use relative links
- ❌ **FAIL**: Bare URLs (should be markdown links)
- ❌ **FLAG**: Broken internal links

### 4. NO SPECULATION VALIDATION
- ✅ **Claims have citations**: Factual statements referenced
- ❌ **FAIL**: Speculation without citations ("likely", "probably", "appears to")
- ❌ **FLAG**: Hedging language without sources ("suggests", "indicates")

### 5. Date Validation
- ✅ **Consistent format**: All dates use same format
- ✅ **Valid dates**: No impossible dates (e.g., February 30)
- ❌ **Flag**: Inconsistent formats, invalid dates

### 6. Formatting Validation
- ✅ **Proper markdown**: Headers, lists, links formatted correctly
- ✅ **Consistent structure**: Logical organization
- ✅ **No placeholders**: No `[TODO]`, `TBD`, `{variable}` left in output
- ❌ **Flag**: Malformed markdown, inconsistent headers, placeholder text

### 7. Reference Validation
- ✅ **Citations present**: Data points have numbered citations [1]
- ✅ **Complete URLs**: Full URLs in references section
- ✅ **Valid URLs**: URLs are well-formed (http/https protocol)
- ❌ **Flag**: Missing citations, broken URLs

### 8. Data Completeness
- ✅ **Required sections**: Key sections present
- ✅ **Content filled**: Sections not empty
- ❌ **Flag**: Missing sections, empty content

### 9. Guardrails Compliance (STRICTNESS LEVELS)
- ✅ **REQUIRED patterns**: Must follow - blocks if violated
- ⚠️ **RECOMMENDED patterns**: Should follow - warnings if violated
- ℹ️ **OPTIONAL patterns**: Nice-to-have - suggestions only

**Check against:**
- `hmode/guardrails/architecture-preferences/*.json` - Approved patterns with strictness
- `hmode/guardrails/tech-preferences/*.json` - Approved technologies
- `hmode/shared/standards/code/manifest.json` - Reference example currency

**Validation:**
- ❌ **FAIL**: REQUIRED pattern violated (e.g., no type hints in Python)
- ⚠️ **WARNING**: RECOMMENDED pattern not followed (e.g., missing docstrings)
- ℹ️ **SUGGESTION**: OPTIONAL pattern could improve code (e.g., utility types)

**Enforcement:**
- REQUIRED violations block deployment
- RECOMMENDED violations generate warnings in report
- OPTIONAL suggestions listed separately

## Output Format

Create quality report in this format:

```markdown
# Quality Control Report

**File(s) Checked**: {file_path}
**Generated**: {timestamp}

---

## Summary

- **Files Reviewed**: {count}
- **Total Issues**: {count}
- **Critical Issues**: {count}
- **Warnings**: {count}
- **Overall Grade**: {A/B/C/D/F}

---

## Issues by File

### filename.md
**Status**: ✅ Pass | ⚠️ Warning | ❌ Fail

#### Critical Issues
- **Line X**: Invalid date format: "Jan 2025" should be "2025-01"
- **Line Y**: Missing citation for claim

#### Warnings
- **Line Z**: Paragraph too long (9 sentences)

#### Passed Checks
- ✅ All URLs properly formatted
- ✅ Markdown formatting correct
- ✅ No placeholder text

---

## Recommended Fixes

### High Priority
1. **filename.md:45** - Fix invalid date format
2. **filename.md:89** - Add missing citation

### Medium Priority
1. **filename.md:23** - Standardize date format
2. **filename.md:67** - Split long paragraph

---

## Grade Breakdown

| File | Format | References | Completeness | Readability | Grade |
|------|--------|------------|--------------|-------------|-------|
| file1.md | ✅ A | ✅ A | ⚠️ B | ✅ A | A |
| file2.md | ⚠️ B | ✅ A | ✅ A | ⚠️ B | B |

---

## Guardrails Compliance

### REQUIRED Violations (BLOCKS)
❌ **CRITICAL**: No REQUIRED violations found

### RECOMMENDED Violations (WARNINGS)
⚠️ **WARNING**: Two-Phase Execution pattern not followed in orchestrator.py:45
⚠️ **WARNING**: Missing docstrings in 3 functions

### OPTIONAL Suggestions
ℹ️ Consider using utility types for better type safety
ℹ️ Could add more inline comments for complex logic

---

## Quality Metrics

- **Citation Coverage**: 85% (170/200 data points cited)
- **URL Validity**: 95% (190/200 URLs well-formed)
- **Date Consistency**: 78% (7/9 files use consistent format)
- **Bare URL Count**: 5 URLs not in markdown format
- **Speculation Instances**: 3 claims without citations
- **Guardrails Compliance**: 100% REQUIRED, 85% RECOMMENDED, 50% OPTIONAL

---

## Action Items

1. ⚠️ **PRIORITY**: Fix 3 critical issues
2. ⚠️ **IMPORTANT**: Add missing citations (5 instances)
3. ✅ **Optional**: Standardize date formats
4. ✅ **Optional**: Break up long paragraphs

---

*This report was automatically generated by the Quality Control Agent.*
```

## Instructions

1. Read file(s) using Read tool
2. Check each file against all quality criteria
3. Note line numbers for issues
4. Generate detailed quality report
5. Assign grades (A-F) for each category
6. Provide actionable recommendations
7. Be thorough but fair - minor issues are warnings, not failures

**Important**:
- Do NOT modify the original files (read-only review)
- Do NOT generate false positives - only flag real issues
- DO provide specific line numbers and examples
- DO suggest concrete fixes

Present your analysis as formatted markdown.
