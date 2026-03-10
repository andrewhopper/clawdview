# Research Findings: Guardrail and Policy Enforcement Systems

<!-- File UUID: 7a9f2e4b-6c8d-4e3f-8a5b-9d7c3e6f1a2b -->

**Research Date:** 2026-01-15
**Status:** Phase 2 - In Progress

## 1.0 Overview

Research into existing guardrail, policy enforcement, and linting systems across multiple ecosystems to inform the design of Overwatch Guardrails.

## 2.0 Python Ecosystem

### 2.1 pre-commit Framework

**What it is:** Git hook framework for running checks before commits

**Enforcement Model:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
        stages: [commit, push]  # Context-based
```

**Key Insights:**
- Hooks run at specific stages (commit, push, merge)
- Binary enforcement: pass/fail (no warn mode)
- Can be bypassed with `--no-verify`
- Strong ecosystem integration

**Lessons for Overwatch:**
- ✅ Stage-based execution (phase-based in our case)
- ✅ Hook composition pattern
- ❌ No severity levels (we need LOG/WARN/etc)
- ❌ No ranking system

### 2.2 Pylint/Flake8

**Severity Levels:**
```ini
# pylint
# (C)onvention, (R)efactor, (W)arning, (E)rror, (F)atal

[MESSAGES CONTROL]
disable=C0111,R0903  # Can disable specific rules
```

**Key Insights:**
- 5 severity levels (C/R/W/E/F)
- Rules can be disabled per-file or globally
- Exit codes: 0 (success), non-zero (violations found)
- Can configure per-message category

**Lessons for Overwatch:**
- ✅ Severity hierarchy (maps to our modes)
- ✅ Per-rule configuration
- ✅ Disable/enable flexibility
- ❌ No approval workflow
- ❌ No ranking for alternatives

### 2.3 Safety (Dependency Security)

**Modes:**
```bash
safety check                    # Fail on vulnerabilities
safety check --continue-on-error  # Warn only
safety check --json             # Machine-readable output
```

**Key Insights:**
- Binary mode: fail or continue
- Severity levels for vulnerabilities (low/medium/high/critical)
- JSON output for tooling integration
- Ignore policies via .safety-policy.json

**Lessons for Overwatch:**
- ✅ Ignore/allowlist pattern
- ✅ Severity-based filtering
- ✅ Machine-readable output
- ❌ No graduated enforcement (just fail/continue)

### 2.4 Bandit (Security Linter)

**Severity System:**
```yaml
# .bandit
severity:
  LOW: [B201, B301]
  MEDIUM: [B501]
  HIGH: [B601, B602]

# Can set threshold
bandit -ll  # Only show high confidence issues
```

**Key Insights:**
- Confidence + Severity matrix
- Configurable threshold
- Can exclude tests, specific paths
- Machine-readable output (JSON, XML)

**Lessons for Overwatch:**
- ✅ Confidence scoring (could use for context)
- ✅ Threshold configuration
- ❌ No interactive approval

## 3.0 Rust Ecosystem

### 3.1 Clippy (Rust Linter)

**Lint Levels:**
```rust
#![allow(dead_code)]      // Disable warning
#![warn(missing_docs)]    // Enable warning
#![deny(unsafe_code)]     // Make it an error
#![forbid(unsafe_code)]   // Can't be overridden
```

**Hierarchy:**
```
allow   → Silenced
warn    → Warning (default for most lints)
deny    → Error (fails compilation)
forbid  → Error (can't be overridden with allow)
```

**Key Insights:**
- 4 levels: allow/warn/deny/forbid
- Can be set globally, per-module, per-function
- `forbid` is strongest (no local override)
- Part of compiler, not separate tool

**Lessons for Overwatch:**
- ✅ **4-level system matches our design!**
- ✅ allow=LOG, warn=WARN, deny=APPROVAL_REQUIRED, forbid=BLOCK
- ✅ Context-based overrides (global → module → function)
- ✅ "forbid" = BLOCK (no override)

**Best Match:** Clippy's model closely aligns with our design!

### 3.2 cargo-deny

**Dependency Policy Enforcement:**
```toml
[advisories]
vulnerability = "deny"  # Fail on vulnerabilities
unmaintained = "warn"   # Warn on unmaintained
unsound = "deny"

[bans]
multiple-versions = "warn"  # Warn on version conflicts

[licenses]
unlicensed = "deny"
copyleft = "warn"
allow = ["MIT", "Apache-2.0"]
```

**Levels:**
- `allow` - Permitted
- `warn` - Warning logged
- `deny` - Error, fails build

**Key Insights:**
- Policy as configuration
- Three levels: allow/warn/deny
- Category-based rules (advisories, licenses, bans)
- Clear allowlists

**Lessons for Overwatch:**
- ✅ Category-based configuration
- ✅ Allowlist pattern (rank 1 = allowed)
- ✅ 3-level enforcement
- ❌ No approval workflow
- ❌ No ranking within allowed items

## 4.0 Infrastructure & Policy Systems

### 4.1 OPA (Open Policy Agent)

**Policy as Code:**
```rego
package example

# Policy: deny requests without authentication
deny["Authentication required"] {
    not input.user
}

# Policy: warn about non-HTTPS
warn["Use HTTPS"] {
    input.protocol == "http"
}
```

**Key Insights:**
- Policies written in Rego language
- Returns: allow, deny, violations
- Decoupled from enforcement (decision vs. enforcement)
- Can return multiple violation reasons

**Lessons for Overwatch:**
- ✅ Separation: detection vs. enforcement
- ✅ Structured violation output
- ✅ Multiple violations per check
- ❌ Complex language (Rego)
- ✅ Decision + reason pattern

### 4.2 HashiCorp Sentinel

**Enforcement Levels:**
```hcl
policy "require-private-s3" {
  enforcement_level = "advisory"     # Log only
  enforcement_level = "soft-mandatory"  # Can override
  enforcement_level = "hard-mandatory"  # Cannot override
}
```

**Three Levels:**
- `advisory` - Warning, always passes
- `soft-mandatory` - Can be overridden with permissions
- `hard-mandatory` - Cannot be overridden

**Key Insights:**
- 3 enforcement levels
- Permission-based override for soft-mandatory
- Policy evaluation separate from enforcement
- Terraform/Vault integration

**Lessons for Overwatch:**
- ✅ **3-level model similar to ours!**
- ✅ advisory=LOG/WARN, soft=APPROVAL_REQUIRED, hard=BLOCK
- ✅ Override with justification (soft-mandatory)
- ✅ Named enforcement levels

**Good Match:** Sentinel's 3-level model maps well to our 4 modes!

### 4.3 Kubernetes Admission Controllers

**Modes:**
- **Validating:** Pass/fail decision
- **Mutating:** Modify resources (autofix)
- **Audit:** Log only, don't block

**Key Insights:**
- Three distinct modes of operation
- Can run multiple controllers
- Fail-open vs. fail-closed configuration
- Audit mode for monitoring

**Lessons for Overwatch:**
- ✅ Audit mode = LOG
- ✅ Validating mode = BLOCK/APPROVAL_REQUIRED
- ✅ Mutating mode = autofix capability
- ✅ Composable controllers

### 4.4 AWS Config Rules

**Compliance States:**
```
COMPLIANT
NON_COMPLIANT
NOT_APPLICABLE
INSUFFICIENT_DATA
```

**Enforcement:**
- Detection only (no blocking)
- Remediation actions (separate)
- Continuous evaluation
- Historical compliance tracking

**Key Insights:**
- Detection separate from remediation
- Temporal compliance tracking
- NOT_APPLICABLE = context-aware
- Audit-focused (no blocking)

**Lessons for Overwatch:**
- ✅ Historical tracking important
- ✅ Context awareness (NOT_APPLICABLE)
- ✅ Detection ≠ enforcement
- ❌ No real-time blocking

## 5.0 Common Patterns Across Systems

### 5.1 Enforcement Hierarchies

**2-Level Systems:**
- Pass/Fail (pre-commit, safety)
- Too simplistic for our needs

**3-Level Systems:**
- cargo-deny: allow/warn/deny
- Sentinel: advisory/soft-mandatory/hard-mandatory
- Good balance, maps well

**4-Level Systems:**
- Clippy: allow/warn/deny/forbid
- Pylint: C/R/W/E/F (5 actually)
- **Best match for our needs**

**5+ Level Systems:**
- Pylint (5 levels)
- Too many distinctions

### 5.2 Override Mechanisms

**No Override:**
- Clippy: `forbid`
- Sentinel: `hard-mandatory`
- Maps to our **BLOCK**

**Permission-Based Override:**
- Sentinel: `soft-mandatory` (requires permissions)
- Maps to our **APPROVAL_REQUIRED**

**Inline Override:**
- Pylint: `# pylint: disable=C0111`
- Clippy: `#[allow(dead_code)]`
- ESLint: `// eslint-disable-next-line`
- Could add to our system

### 5.3 Configuration Patterns

**File-Based Config:**
- YAML: pre-commit, GitHub Actions
- TOML: cargo-deny, Rust
- JSON: ESLint, TSConfig
- INI: pylint

**Inline Config:**
- Comments: `# noqa`, `// eslint-disable`
- Attributes: Rust `#[allow]`

**Lessons:**
- ✅ YAML is most readable for complex config
- ✅ JSON for machine generation
- ✅ Consider inline overrides for exceptions

### 5.4 Context Awareness

**By File/Path:**
- ESLint: Different rules per directory
- Clippy: Per-module configuration
- ✅ We have per-project config

**By Stage:**
- pre-commit: Different hooks per stage (commit/push)
- GitHub Actions: Different jobs per event
- ✅ We have phase-based overrides

**By Environment:**
- Terraform: workspace-specific policies
- ✅ We have environment overrides

## 6.0 Recommendations for Overwatch Guardrails

### 6.1 Keep 4-Mode System

**Validation:** Clippy's allow/warn/deny/forbid model is widely successful

```
LOG (allow)              → Silent, for metrics
WARN (warn)              → Show but proceed
APPROVAL_REQUIRED (deny) → Block until approved
BLOCK (forbid)           → Hard block, no override
```

### 6.2 Add Inline Override Support

```python
# guardrails: disable=unapproved-dependency
from create_react_app import something  # Spike only, remove later
```

Inspired by: ESLint, Pylint, Clippy

### 6.3 Separation of Concerns

Follow OPA model:
1. **Detection** - Identify violations
2. **Decision** - Determine severity/mode
3. **Enforcement** - Apply action (log/warn/block/ask)
4. **Logging** - Record decision

### 6.4 Historical Tracking

Like AWS Config:
- Track compliance over time
- Show trends (violations increasing/decreasing)
- Report: "Project had 45 violations in phase 1, now 5 in phase 8"

### 6.5 Autofix Support

Like Kubernetes Mutating Admission:
- Detect violation
- Offer autofix
- Apply with user consent
- Log what was changed

### 6.6 Machine-Readable Output

Support multiple formats:
- Human-readable (terminal)
- JSON (CI/CD integration)
- YAML (reporting)
- JUnit XML (test frameworks)

## 7.0 Design Validation

### 7.1 Our 4-Mode System vs. Industry

| System | Levels | Mapping to Ours |
|--------|--------|-----------------|
| Clippy | allow/warn/deny/forbid | ✅ Perfect match |
| Sentinel | advisory/soft/hard | ✅ Missing LOG, but close |
| cargo-deny | allow/warn/deny | ✅ Close, missing BLOCK distinction |
| pre-commit | pass/fail | ❌ Too simple |
| Pylint | C/R/W/E/F | ⚠️ More granular, but complex |

**Conclusion:** Our 4-mode system aligns with best-in-class tools (Clippy, Sentinel)

### 7.2 Ranking System Validation

**Finding:** Most systems don't have ranking/preference systems
- cargo-deny: binary allow/deny lists
- OPA: binary decisions
- **Gap in market:** Ranked preferences with graduated enforcement

**Our Innovation:** Mapping ranks to enforcement modes
- Rank 1 → LOG (preferred, silent)
- Rank 2-3 → WARN (acceptable alternatives)
- Unlisted → APPROVAL_REQUIRED (needs approval)

**Validation:** This is novel and valuable

## 8.0 References

### 8.1 Tools Researched
- pre-commit: https://pre-commit.com/
- Clippy: https://doc.rust-lang.org/clippy/
- cargo-deny: https://embarkstudios.github.io/cargo-deny/
- OPA: https://www.openpolicyagent.org/
- Sentinel: https://www.hashicorp.com/sentinel
- Pylint: https://pylint.pycqa.org/
- Bandit: https://bandit.readthedocs.io/

### 8.2 Key Takeaways
1. 4-level enforcement is proven (Clippy)
2. Context-based overrides are common
3. Separation of detection/enforcement is best practice
4. Historical tracking adds value
5. Machine-readable output is essential
6. Inline overrides are useful for exceptions

## 9.0 Next Steps for Phase 3

1. Define Python API based on research
2. Add inline override syntax (`# guardrails: disable`)
3. Design violation history tracking
4. Create autofix framework
5. Define JSON output schema
6. Write integration examples
