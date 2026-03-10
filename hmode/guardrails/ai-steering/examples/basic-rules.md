# Basic AI Steering Rules - Examples

## Example 1: ALWAYS Rule (Tool Selection)

**Rule:** `use-read-over-bash-cat` (ALWAYS level)

**Scenario:**
```
User: "Show me the contents of config.json"
```

**Context Matching:**
- `when`: ["reading file contents"] ✓
- `unless`: ["streaming logs"] ✗

**Rule Applies:** YES

**AI Behavior:**
```
✓ CORRECT: Use Read tool
  Read(file_path="/path/to/config.json")

✗ INCORRECT: Use Bash
  Bash(command="cat config.json")
```

**Rationale:** Read tool optimized for file viewing, better UX

---

## Example 2: NEVER Rule (Proactive Actions)

**Rule:** `only-commit-when-asked` (NEVER level)

**Scenario:**
```
AI just finished implementing authentication feature
User hasn't mentioned committing
```

**Context Matching:**
- `when`: ["made code changes"] ✓
- `unless`: ["user said commit"] ✗

**Rule Applies:** YES

**AI Behavior:**
```
✓ CORRECT: Mention completion, wait for user
  "Authentication feature complete. Tests passing."

✗ INCORRECT: Auto-commit
  git add . && git commit -m "Add authentication"
```

**Rationale:** User controls commit timing, may want to review first

---

## Example 3: MUST Rule (Confirmation Required)

**Rule:** `confirm-bulk-file-operations` (MUST level)

**Scenario:**
```
User: "Update all .project files with new field"
File count: 30 files
```

**Context Matching:**
- `when`: ["modifying files"] ✓
- `fileCount.min`: 20 ✓ (30 >= 20)

**Rule Applies:** YES

**AI Behavior:**
```
✓ CORRECT: Confirm first
  "Updating 30 .project files with 'new_field'.
   Time estimate: 10-15 min.
   Confirm?"

   [Wait for user response]

✗ INCORRECT: Execute immediately
  [Starts modifying all 30 files without confirmation]
```

**Rationale:** Prevent accidental large-scale changes

---

## Example 4: SHOULD Rule (Strong Recommendation)

**Rule:** `brevity-50-percent-fewer-words` (SHOULD level)

**Scenario:**
```
AI explaining what was done
```

**Context Matching:**
- `when`: ["communicating with user"] ✓

**Rule Applies:** YES

**AI Behavior:**
```
✓ CORRECT: Concise
  "Updated 3 files with new error handling."

✗ INCORRECT: Verbose
  "I have successfully updated three files in your codebase
   with the new error handling pattern that we previously
   discussed and agreed upon."
```

**Rationale:** Respect user time, CLI favors brevity

---

## Example 5: Context Matching with `unless`

**Rule:** `no-code-before-phase-8` (NEVER level)

**Scenario:**
```
User: "Start implementing the API"
Current phase: PHASE_6_DESIGN
```

**Context Matching:**
- `when`: ["writing production code"] ✓
- `unless`: ["spike exception", "phase is PHASE_8 or later"] ✗

**Rule Applies:** YES (unless conditions NOT met)

**AI Behavior:**
```
✓ CORRECT: Explain phase constraint
  "Cannot write code in PHASE_6_DESIGN. Must complete:
   - Phase 6: Design (current)
   - Phase 7: Test design
   Then proceed to Phase 8 for implementation."

✗ INCORRECT: Start coding
  "Sure, let me start coding the API endpoints..."
```

**Rationale:** 9-phase SDLC ensures design-first

---

## Example 6: Rule Override (Exception Handling)

**Rule:** `use-read-over-bash-cat` (ALWAYS level)

**Scenario:**
```
User: "Monitor the application logs in real-time"
```

**Context Matching:**
- `when`: ["reading file contents"] ✓
- `unless`: ["streaming logs in real-time"] ✓ ← EXCEPTION

**Rule Applies:** NO (exception condition met)

**AI Behavior:**
```
✓ CORRECT: Use Bash for streaming
  Bash(command="tail -f /var/log/app.log")

✗ INCORRECT: Try to use Read (not suitable for streaming)
  Read(file_path="/var/log/app.log")  # Won't stream updates
```

**Rationale:** Exception condition overrides base rule

---

## Example 7: Multi-Rule Composition

**Scenario:**
```
User: "Delete all old test files"
File count: 25 files
Destructive: true
```

**Rules That Apply:**

1. `confirm-bulk-file-operations` (MUST)
   - `fileCount`: 25 >= 20 ✓

2. `confirm-destructive-operations` (MUST)
   - `destructive`: true ✓

**Conflict Resolution:** Both MUST level, both require confirmation

**AI Behavior:**
```
✓ CORRECT: Combine confirmations
  "Destructive operation: Delete 25 test files.
   Files to delete:
   - test/old_spec_1.ts
   - test/old_spec_2.ts
   ... (full list)

   Cannot undo. Confirm? y/n"

✗ INCORRECT: Skip confirmation
  [Immediately deletes all 25 files]
```

**Rationale:** Multiple MUST rules all must be satisfied

---

## Example 8: Precedence Override

**Scenario:**
```
User: "Use git reset --hard to undo changes"
```

**Rules That Apply:**

1. Rule A: `ALWAYS use Bash for git operations` (hypothetical)
2. Rule B: `confirm-destructive-operations` (MUST)
   - `destructive`: true ✓

**Precedence:** NEVER/ALWAYS > MUST > SHOULD > PREFER

**Conflict Resolution:** Both ALWAYS and MUST require action, but destructive nature triggers confirmation

**AI Behavior:**
```
✓ CORRECT: Confirm destructive git operation
  "Destructive operation: git reset --hard
   This will permanently discard all uncommitted changes.
   Cannot undo. Confirm? y/n"

✗ INCORRECT: Execute immediately
  Bash(command="git reset --hard")
```

**Rationale:** Destructive operations always require confirmation regardless of other rules

---

## Example 9: Progressive Rule Application

**Scenario:**
```
User: "Create a comprehensive architecture presentation"
```

**Rules That Apply (in order):**

1. Intent Detection: Classify as "New Artifact" (complex)
2. `progressive-content-complex-artifacts` (MUST)
   - `when`: ["creating detailed presentation"] ✓
3. `use-todo-list-complex-tasks` (SHOULD)
   - `when`: ["task has 3+ steps"] ✓

**AI Behavior:**
```
✓ CORRECT: Apply both rules
  "Complex artifact detected: Detailed presentation.
   Using /progressive-content (6-stage workflow).

   [Creates todo list for stages]
   1. Stage 0: Seeding
   2. Stage 1: Structure
   3. Stage 2: Substance
   ...

   Starting Stage 0: What's the 2-3 sentence concept?"

✗ INCORRECT: Skip progressive workflow
  [Immediately generates full 20-slide presentation]
```

**Rationale:** Layer MUST rules with SHOULD rules for comprehensive guidance
