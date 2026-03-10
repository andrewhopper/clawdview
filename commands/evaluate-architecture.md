---
version: 1.0.0
last_updated: 2026-02-19
description: Evaluate code modularity, decoupling, and DRY principles
args:
  path: Path to project directory or specific files to evaluate
  mode: Analysis depth - quick, standard (default), deep
---

# Evaluate Architecture

Assess code quality for modularity, decoupling, and DRY (Don't Repeat Yourself) principles. Get actionable refactoring recommendations.

## Usage

**Option 1: Evaluate entire project**
```
/evaluate-architecture .
```

**Option 2: Evaluate specific directory**
```
/evaluate-architecture src/
```

**Option 3: Evaluate specific files**
```
/evaluate-architecture src/server.py src/filters.py
```

**Option 4: Quick scan**
```
/evaluate-architecture . quick
```

---

## What It Evaluates

### 1. Modularity (0-100)
- Single Responsibility Principle
- File size (>500 lines = warning)
- Module cohesion
- Clear boundaries

### 2. Decoupling (0-100)
- Dependency on abstractions vs implementations
- Hardcoded dependencies vs dependency injection
- Global state usage
- Interface/protocol usage

### 3. DRY Compliance (0-100)
- Code duplication (exact, structural, semantic)
- Magic numbers/strings
- Repeated error handling patterns
- Copy-paste code

### 4. Testability (0-100)
- Can components be unit tested?
- Are dependencies mockable?
- Requires full environment to test?

---

## Output

You'll receive:

1. **Overall Architecture Score** (0-100)
2. **Dimension Scores** (Modularity, Decoupling, DRY, Testability)
3. **Architecture Smells** (God objects, tight coupling, duplication)
4. **Before/After Examples** (how to refactor)
5. **Refactoring Roadmap** (phased improvements)
6. **Priority Actions** (what to fix first)

---

## Analysis Modes

**Quick (5 minutes):**
- File count and sizes
- Top 3 smells
- Overall score
- Critical issues only

**Standard (15 minutes) - Default:**
- Full analysis
- All smells
- Refactoring roadmap
- Code examples

**Deep (30+ minutes):**
- Line-by-line duplication
- Dependency graphs
- Per-component testability
- Detailed refactoring per file

---

## When to Use

- **Before refactoring:** Understand current state and prioritize improvements
- **Code review:** Identify architectural issues before merge
- **Phase 8.5 (Web Apps):** Architecture quality gate
- **Brownfield assessment:** Evaluate existing codebase before changes
- **After spike:** Convert POC code to production-ready architecture

---

## Examples

### Example 1: Single File Evaluation
```
/evaluate-architecture src/server.py
```

**Result:**
```
# Architecture Evaluation Report

**File:** src/server.py (450 lines)
**Score:** 30/100 🔴 Critical Issues

## Issues
🔴 God Object - File contains server + filters + config + logging
🔴 Tight Coupling - Server hardcodes filter logic
🟡 Duplication - Validation logic repeated 12 times

## Refactoring Roadmap
Phase 1: Extract filters to filters/ directory
Phase 2: Extract config to config/loader.py
Phase 3: Eliminate duplication (validation.py)
```

### Example 2: Project-Wide Evaluation
```
/evaluate-architecture . standard
```

**Result:**
```
# Architecture Evaluation Report

**Project:** dns-filter-system
**Files:** 2
**Lines of Code:** 550
**Overall Score:** 35/100 🔴 Requires Refactoring

| Dimension | Score | Status |
|-----------|-------|--------|
| Modularity | 35/100 | 🔴 Poor |
| Decoupling | 25/100 | 🔴 Poor |
| DRY | 40/100 | 🔴 Poor |
| Testability | 20/100 | 🔴 Poor |

## Critical Issues
1. server.py is a god object (450 lines, mixed concerns)
2. Filters tightly coupled to server
3. 12 instances of duplicated validation logic

## Expected After Refactoring
Modularity: 35 → 85 (+143%)
Decoupling: 25 → 80 (+220%)
Overall: 35 → 85 (+183%)
```

### Example 3: Quick Scan
```
/evaluate-architecture . quick
```

**Result:**
```
# Quick Architecture Scan

**Score:** 35/100 🔴

**Top 3 Issues:**
1. 🔴 God object in server.py (450 lines)
2. 🔴 DNS server + filters in one file (tight coupling)
3. 🟡 Validation logic duplicated 12 times

**Recommendation:** Split server.py into 5 modules
**Estimated Effort:** 4-6 hours
```

---

## Behind the Scenes

This skill spawns the **architecture-evaluator** agent which:
1. Analyzes file structure and module organization
2. Detects coupling patterns (hardcoded dependencies, global state)
3. Identifies code duplication (exact, structural, semantic)
4. Finds architecture smells (god objects, long methods, feature envy)
5. Assesses testability (can components be unit tested?)
6. Generates refactoring roadmap with before/after examples
7. Prioritizes improvements (must-do, should-do, could-do)

---

## Integration with SDLC

### Phase 8.5 (Web Apps) - Quality Gate
For web applications, architecture evaluation is **mandatory** before Phase 9:

```
Phase 8 (IMPL) → Phase 8.5 (QA) → /evaluate-architecture → Fix issues → Phase 9
```

**Quality Gate Criteria:**
- Overall score ≥ 70/100
- No critical smells (god objects, tight coupling)
- Modularity ≥ 70/100
- Testability ≥ 60/100

### Brownfield Projects
Before adding features or fixing bugs, run architecture evaluation:
```
/evaluate-architecture . → Understand current state → Plan improvements
```

### Post-Spike Cleanup
After throwaway POC code, convert to production-ready:
```
/evaluate-architecture . → Refactoring roadmap → Apply phases → Re-validate
```

---

## Related

- `/audit-proposal` - Validate technical proposals
- `/validate-requirements` - Validate product requirements
- Phase 8.5 (QA/Validation) - Quality gate for web apps
- Brownfield workflow - Existing codebase maintenance

---

## Instructions for Claude

When user invokes `/evaluate-architecture [path] [mode]`:

1. **Parse arguments:**
   - path: Directory or file(s) to evaluate (default: current directory)
   - mode: quick | standard | deep (default: standard)

2. **Spawn architecture-evaluator agent:**
   ```python
   Task(
       subagent_type="general-purpose",
       prompt=f"""
       You are an architecture evaluation specialist. Your task is to evaluate code quality for modularity, decoupling, and DRY principles.

       Load and follow the agent definition: hmode/agents/architecture-evaluator.md

       PROJECT PATH: {path}
       ANALYSIS MODE: {mode}

       Provide:
       1. Overall architecture score (0-100)
       2. Dimension scores (modularity, decoupling, DRY, testability)
       3. Architecture smells detected
       4. Before/after refactoring examples
       5. Phased refactoring roadmap
       6. Priority actions (must-do, should-do, could-do)
       """,
       description="Evaluate architecture"
   )
   ```

3. **Present results to user:**
   - Show overall score and dimension breakdown
   - Highlight critical issues
   - Provide before/after examples
   - Offer refactoring roadmap

4. **Quality gate check (if Phase 8.5):**
   - If overall score < 70 → Block Phase 9, require improvements
   - If score ≥ 70 → Allow Phase 9 transition

5. **Follow-up:**
   - Ask if user wants detailed refactoring plan
   - Offer to start Phase 1 refactoring
   - Suggest next actions based on score

---

**Skill Version:** 1.0.0
**Agent:** architecture-evaluator
