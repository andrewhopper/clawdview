# Ranking System

<!-- File UUID: 9b3e6f8a-2d7c-4e9f-8a1b-6c4d5e7f9a2b -->

## 1.0 Overview

Tech preferences already use `rank` fields (1, 2, 3, etc.). This system maps ranks to enforcement behavior.

## 2.0 Rank Meanings

```
┌──────┬─────────────────────┬────────────────────────────────────┐
│ Rank │ Status              │ Meaning                            │
├──────┼─────────────────────┼────────────────────────────────────┤
│ 1    │ Preferred           │ Optimal choice for use case        │
│ 2-3  │ Allowed Alternative │ Valid with acceptable tradeoffs    │
│ 4+   │ Discouraged         │ Consider better alternatives       │
│ N/A  │ Unlisted            │ Not in preferences, needs approval │
└──────┴─────────────────────┴────────────────────────────────────┘
```

## 3.0 Rank to Enforcement Mapping

### 3.1 Standard Strictness (Default)

```
Rank 1    →  LOG                 (silent, ideal choice)
Rank 2-3  →  WARN                (show preferred alternative)
Rank 4+   →  WARN                (discourage, suggest better options)
Unlisted  →  APPROVAL_REQUIRED   (block until approved)
```

### 3.2 Relaxed Strictness (Spike, Early Phases)

```
Rank 1    →  LOG
Rank 2-3  →  LOG                 (no warning)
Rank 4+   →  WARN
Unlisted  →  WARN                (allow with warning)
```

### 3.3 Strict Strictness (Production)

```
Rank 1    →  LOG
Rank 2-3  →  APPROVAL_REQUIRED   (even rank 2 needs justification)
Rank 4+   →  BLOCK
Unlisted  →  BLOCK
```

## 4.0 Example: Frontend Frameworks

From `.guardrails/tech-preferences/frontend.json`:

```json
{
  "frontend_frameworks": {
    "preferences": [
      {
        "rank": 1,
        "name": "Next.js",
        "version": "15.x",
        "rationale": "Full-stack React with App Router..."
      },
      {
        "rank": 2,
        "name": "Vite + React",
        "version": "6.x + React 19.x",
        "rationale": "Fast HMR, simple SPAs..."
      },
      {
        "rank": 3,
        "name": "Expo",
        "version": "SDK 51+",
        "rationale": "React Native for mobile..."
      }
    ]
  }
}
```

### Enforcement Scenarios

**Scenario 1: User chooses Next.js**
- Rank: 1
- Mode: LOG
- Message: (none)
- Action: Allowed, silently logged

**Scenario 2: User chooses Vite + React**
- Rank: 2
- Mode: WARN (standard strictness)
- Message: "⚠️  Using Vite + React (rank 2). Preferred: Next.js 15.x"
- Action: Allowed, warning shown

**Scenario 3: User chooses Create React App**
- Rank: Unlisted
- Mode: APPROVAL_REQUIRED (standard strictness)
- Message: "🔒 Package 'create-react-app' not in approved list"
- Alternatives shown: Next.js (1), Vite (2), Expo (3)
- Action: Blocked until approved

## 5.0 Strictness Profiles

### 5.1 Configuration

```yaml
# .guardrails/enforcement-config.yaml

strictness_profiles:
  relaxed:
    rank_1: LOG
    rank_2_3: LOG
    rank_4_plus: WARN
    not_listed: WARN

  standard:
    rank_1: LOG
    rank_2_3: WARN
    rank_4_plus: WARN
    not_listed: APPROVAL_REQUIRED

  strict:
    rank_1: LOG
    rank_2_3: APPROVAL_REQUIRED
    rank_4_plus: BLOCK
    not_listed: BLOCK
```

### 5.2 Context-Based Selection

```yaml
contexts:
  # By phase
  phase_1_to_3:
    strictness: relaxed
  phase_8_to_9:
    strictness: standard

  # By project type
  spike:
    strictness: relaxed
  production:
    strictness: strict

  # By environment
  development:
    strictness: relaxed
  staging:
    strictness: standard
  production:
    strictness: strict
```

## 6.0 Showing Alternatives

When ranks 2+ or unlisted are used, show preferred alternatives:

### 6.1 Rank 2-3 Detection

```
[WARN] Using Vite + React (rank 2)

Preferred option:
  1. Next.js 15.x
     Rationale: Full-stack React with App Router, Server Components,
                built-in API routes, excellent DX

Continue with Vite? Action will be logged.
```

### 6.2 Unlisted Detection

```
[APPROVAL_REQUIRED] Package 'angular' not in approved list

Approved frontend frameworks:
  1. Next.js 15.x (preferred)
     Use case: web apps, dashboards, marketing sites

  2. Vite + React 6.x
     Use case: simple SPAs, client-only apps

  3. Expo SDK 51+
     Use case: mobile apps, cross-platform

Reason for using 'angular': _____________________

Approve? [y/N]: _
```

## 7.0 Implementation Pseudocode

```python
def enforce_ranked_preference(package_name, category, context):
    # Find package in preferences
    rank, all_options = lookup_package(package_name, category)

    # Determine strictness from context
    strictness = get_strictness(context)

    # Map rank to mode
    if rank == 1:
        mode = LOG
    elif rank in [2, 3]:
        mode = strictness_profiles[strictness]["rank_2_3"]
    elif rank >= 4:
        mode = strictness_profiles[strictness]["rank_4_plus"]
    else:  # unlisted
        mode = strictness_profiles[strictness]["not_listed"]

    # Get preferred alternatives
    preferred = get_alternatives(category, max_rank=1)

    # Build violation
    violation = Violation(
        message=f"Using {package_name} (rank {rank})",
        alternatives=preferred,
        severity=classify_rank(rank)
    )

    # Enforce
    return enforce(mode, violation)
```

## 8.0 Benefits

1. **Reuses existing rankings** - No duplicate preference definitions
2. **Progressive guidance** - Rank 1 silent, higher ranks increasingly strict
3. **Context-aware** - Same package can be WARN in spike, BLOCK in production
4. **Clear alternatives** - Always show what's preferred and why
5. **Audit trail** - All decisions logged with rank and justification
