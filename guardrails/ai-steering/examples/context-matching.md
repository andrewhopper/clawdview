# Context Matching Examples

## Understanding Context Matching

Rules activate when **ALL** `when` conditions are met **AND** **NONE** of the `unless` conditions are met.

```
Rule applies IF:
  (when[0] AND when[1] AND ... when[n])
  AND NOT
  (unless[0] OR unless[1] OR ... unless[n])
```

---

## Example 1: Simple `when` Matching

**Rule:**
```json
{
  "id": "use-read-over-bash-cat",
  "context": {
    "when": ["reading file contents"]
  }
}
```

**Test Cases:**

| Scenario | `when` Match | Rule Applies |
|----------|--------------|--------------|
| User: "Show me config.json" | ✓ | YES |
| User: "What's in the logs?" | ✓ | YES |
| User: "Delete old files" | ✗ | NO |
| User: "Run the tests" | ✗ | NO |

---

## Example 2: Multiple `when` Conditions (AND Logic)

**Rule:**
```json
{
  "id": "tdd-phase-8",
  "context": {
    "when": ["implementing features", "in Phase 8"]
  }
}
```

**Test Cases:**

| Scenario | `when[0]` | `when[1]` | Rule Applies |
|----------|-----------|-----------|--------------|
| Phase 8, implementing auth | ✓ | ✓ | YES |
| Phase 6, implementing auth | ✓ | ✗ | NO |
| Phase 8, fixing bug | ✗ | ✓ | NO |
| Phase 9, refactoring | ✗ | ✗ | NO |

**Key:** ALL conditions must be true (AND logic)

---

## Example 3: `unless` Exception Handling

**Rule:**
```json
{
  "id": "no-code-before-phase-8",
  "context": {
    "when": ["writing production code"],
    "unless": ["spike exception", "phase is PHASE_8 or later"]
  }
}
```

**Test Cases:**

| Scenario | `when` | `unless[0]` | `unless[1]` | Rule Applies |
|----------|--------|-------------|-------------|--------------|
| Phase 6, regular coding | ✓ | ✗ | ✗ | YES (block) |
| Phase 8, regular coding | ✓ | ✗ | ✓ | NO (allowed) |
| Phase 6, spike coding | ✓ | ✓ | ✗ | NO (exception) |
| Phase 9, regular coding | ✓ | ✗ | ✓ | NO (allowed) |

**Key:** ANY `unless` condition being true deactivates the rule

---

## Example 4: Phase Matching

**Rule:**
```json
{
  "id": "tdd-enforcement",
  "context": {
    "phase": ["PHASE_8_IMPLEMENTATION", "PHASE_9_REFINEMENT"]
  }
}
```

**Test Cases:**

| Current Phase | Phase Match | Rule Applies |
|---------------|-------------|--------------|
| PHASE_8_IMPLEMENTATION | ✓ | YES |
| PHASE_9_REFINEMENT | ✓ | YES |
| PHASE_6_DESIGN | ✗ | NO |
| PHASE_7_TEST_DESIGN | ✗ | NO |

---

## Example 5: File Count Thresholds

**Rule:**
```json
{
  "id": "confirm-bulk-operations",
  "context": {
    "fileCount": {
      "min": 20
    }
  }
}
```

**Test Cases:**

| File Count | Threshold Check | Rule Applies |
|------------|-----------------|--------------|
| 5 files | 5 < 20 | NO |
| 19 files | 19 < 20 | NO |
| 20 files | 20 >= 20 | YES |
| 50 files | 50 >= 20 | YES |

---

## Example 6: File Pattern Matching

**Rule:**
```json
{
  "id": "no-proactive-docs",
  "context": {
    "when": ["creating files"],
    "filePattern": "**/*.md"
  }
}
```

**Test Cases:**

| File Being Created | Pattern Match | Rule Applies |
|-------------------|---------------|--------------|
| `README.md` | ✓ | YES |
| `docs/guide.md` | ✓ | YES |
| `src/app.ts` | ✗ | NO |
| `config.json` | ✗ | NO |

---

## Example 7: Task Type Matching

**Rule:**
```json
{
  "id": "progressive-content-complex",
  "context": {
    "when": ["creating detailed presentation"],
    "taskType": ["New Artifact"]
  }
}
```

**Test Cases:**

| User Request | Classified As | `when` | `taskType` | Rule Applies |
|--------------|---------------|--------|------------|--------------|
| "Create architecture deck" | New Artifact | ✓ | ✓ | YES |
| "Fix presentation typo" | Task | ✓ | ✗ | NO |
| "Brainstorm slide ideas" | Brainstorm | ✗ | ✗ | NO |

---

## Example 8: Tool Matching

**Rule:**
```json
{
  "id": "no-bash-for-communication",
  "context": {
    "when": ["communicating with user"],
    "toolInvolved": ["Bash"]
  }
}
```

**Test Cases:**

| AI Action | `when` | `toolInvolved` | Rule Applies |
|-----------|--------|----------------|--------------|
| Use Bash echo to explain | ✓ | ✓ | YES (prohibit) |
| Use Bash for git commit | ✗ | ✓ | NO |
| Use direct output to explain | ✓ | ✗ | NO |

---

## Example 9: Destructive Flag

**Rule:**
```json
{
  "id": "confirm-destructive",
  "context": {
    "destructive": true
  }
}
```

**Test Cases:**

| Operation | Destructive | Rule Applies |
|-----------|-------------|--------------|
| `git reset --hard` | ✓ | YES |
| `rm -rf build/` | ✓ | YES |
| `git add .` | ✗ | NO |
| `mkdir new-dir` | ✗ | NO |

---

## Example 10: Complex Multi-Condition

**Rule:**
```json
{
  "id": "complex-rule",
  "context": {
    "when": ["modifying files", "in production"],
    "unless": ["emergency hotfix", "approved by tech lead"],
    "phase": ["PHASE_8_IMPLEMENTATION"],
    "fileCount": {
      "min": 10
    },
    "destructive": false
  }
}
```

**Test Cases:**

| Scenario | `when[0]` | `when[1]` | `unless[0]` | `unless[1]` | `phase` | `fileCount` | `destructive` | **Result** |
|----------|-----------|-----------|-------------|-------------|---------|-------------|---------------|------------|
| Phase 8, modify 15 prod files | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ | ✓ | **YES** |
| Phase 8, emergency hotfix (3 files) | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ | **NO** (exception) |
| Phase 6, modify 15 prod files | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | ✓ | **NO** (wrong phase) |
| Phase 8, modify 5 prod files | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ | ✓ | **NO** (too few files) |
| Phase 8, tech lead approved change | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | **NO** (exception) |

**Explanation:**
- Rule applies ONLY when ALL `when` conditions AND phase AND fileCount AND destructive match
- Rule does NOT apply if ANY `unless` condition is true
- Most restrictive: All positive conditions must be true, any exception makes it false

---

## Context Matching Best Practices

1. **Keep `when` conditions specific:** Broad conditions trigger too often
2. **Use `unless` for exceptions:** Clear exception handling
3. **Combine context types:** Mix phase + fileCount + taskType for precision
4. **Test edge cases:** What happens at thresholds (19 vs 20 files)?
5. **Document intent:** Why does this context matter for this rule?

---

## AI Implementation Logic

```python
def rule_applies(rule, context):
    # Check all 'when' conditions (AND logic)
    if rule.context.when:
        if not all(matches(cond, context) for cond in rule.context.when):
            return False

    # Check 'unless' exceptions (OR logic for any exception)
    if rule.context.unless:
        if any(matches(exc, context) for exc in rule.context.unless):
            return False

    # Check phase
    if rule.context.phase:
        if context.current_phase not in rule.context.phase:
            return False

    # Check file count
    if rule.context.fileCount:
        if rule.context.fileCount.min and context.file_count < rule.context.fileCount.min:
            return False
        if rule.context.fileCount.max and context.file_count > rule.context.fileCount.max:
            return False

    # Check file pattern
    if rule.context.filePattern:
        if not glob_match(context.file_path, rule.context.filePattern):
            return False

    # Check task type
    if rule.context.taskType:
        if context.task_type not in rule.context.taskType:
            return False

    # Check tool involved
    if rule.context.toolInvolved:
        if context.tool_name not in rule.context.toolInvolved:
            return False

    # Check destructive flag
    if rule.context.destructive is not None:
        if context.is_destructive != rule.context.destructive:
            return False

    return True
```
