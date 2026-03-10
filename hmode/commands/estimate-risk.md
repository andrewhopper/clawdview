---
uuid: cmd-risk-5o6p7q8r
---

# Estimate Operation Risk and Cost

Estimate the risk, token usage, cost, and time for a proposed operation or change.

## Usage

```bash
/estimate-risk <operation> [--context=<file/module>] [--output=json]
```

## Arguments

- `<operation>` (required) - Description of the operation/change
- `--context` (optional) - File, module, or component context
- `--output` (optional) - Output format: `json` or `markdown` (default)

## Examples

```bash
# Simple CSS change
/estimate-risk "Change button color from blue to red" --context="src/components/Button.tsx"

# High-risk refactor
/estimate-risk "Refactor authentication middleware" --context="src/middleware/auth.ts" --output=json

# Architecture change
/estimate-risk "Migrate from REST to GraphQL" --context="entire API layer"
```

## What It Does

1. **Analyzes the operation** based on:
   - Blast radius (files affected)
   - Reversibility (can it be rolled back?)
   - Data impact (does it modify data?)
   - Security surface (auth/secrets?)
   - Dependency impact (breaking changes?)
   - Test coverage

2. **Calculates risk score** (0-100):
   - 0-20: TRIVIAL
   - 21-40: LOW
   - 41-60: MEDIUM
   - 61-80: HIGH
   - 81-100: CRITICAL

3. **Estimates costs**:
   - Token usage (input + output)
   - Dollar cost (based on model pricing)
   - Time (AI + human review)

4. **Provides recommendations**:
   - Risk mitigation strategies
   - Cost reduction options
   - Best practices

5. **Records estimate** for tracking:
   - Generates unique estimate_id
   - Stores projection in .claude/risk-estimates/
   - Later compares actual vs projected

## Output Format

**Markdown (default):**
- Risk breakdown table
- Cost breakdown
- Time estimate
- Recommendations
- Mitigation strategies

**JSON (--output=json):**
- Structured data for programmatic use
- All numeric values for calculations
- Full breakdown of factors

## See Also

- [Operation Risk Estimator Documentation](../../docs/operation-risk-estimator.md)
- [Risk Estimator Examples](../../docs/risk-estimator-examples.md)
