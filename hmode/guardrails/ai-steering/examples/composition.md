# Rule Composition Examples

## How Rules Combine

Multiple rules can apply simultaneously. Resolution follows:

1. **Constraint Level Precedence:** NEVER > ALWAYS > MUST > MUST_NOT > SHOULD > SHOULD_NOT > PREFER > AVOID
2. **Context Specificity:** More specific context wins over general
3. **Additive Application:** Non-conflicting rules all apply

---

## Example 1: Multiple MUST Rules (Additive)

**Scenario:**
```
User: "Delete 25 old test files"
```

**Rules Triggered:**

1. **`confirm-bulk-file-operations`** (MUST)
   - Context: fileCount >= 20
   - Action: confirm

2. **`confirm-destructive-operations`** (MUST)
   - Context: destructive = true
   - Action: confirm

**Resolution:** Both MUST level, non-conflicting, combine requirements

**AI Behavior:**
```
✓ CORRECT: Single comprehensive confirmation
  "Destructive operation: Delete 25 test files

   Files to delete:
   - test/old_spec_1.ts
   - test/old_spec_2.ts
   ... (showing all 25)

   Cannot undo. Time estimate: 30 seconds.
   Confirm? y/n"

✗ INCORRECT: Two separate confirmations
  First: "Confirm bulk operation on 25 files?"
  Then: "Confirm destructive delete?"
```

**Lesson:** Combine multiple MUST confirmations into one comprehensive prompt

---

## Example 2: NEVER Overrides ALWAYS

**Scenario:**
```
User: "Commit these changes"
AI made changes, ready to commit
AI not explicitly asked to commit
```

**Rules in Conflict:**

1. **`use-bash-for-git`** (ALWAYS - hypothetical)
   - Context: git operations
   - Action: use Bash

2. **`only-commit-when-asked`** (NEVER)
   - Context: made changes, user didn't say "commit"
   - Action: prohibit proactive commits

**Resolution:** NEVER > ALWAYS (constraint level precedence)

**AI Behavior:**
```
✓ CORRECT: Don't commit (NEVER rule wins)
  "Changes complete. Ready to commit when you are."

✗ INCORRECT: Auto-commit (ALWAYS rule would do this)
  Bash(command="git add . && git commit -m 'Update'")
```

**Lesson:** Higher constraint levels override lower ones

---

## Example 3: Specific Context Wins Over General

**Scenario:**
```
User: "Read the application logs to see latest entries"
Logs actively being written
```

**Rules:**

1. **`use-read-over-bash-cat`** (ALWAYS)
   - Context: when = ["reading file contents"]
   - Action: use Read tool

2. **`use-bash-for-streaming-logs`** (ALWAYS - hypothetical with more specific context)
   - Context: when = ["reading file contents", "real-time streaming"]
   - Action: use Bash for tail -f

**Resolution:** Rule 2 more specific (2 conditions vs 1), wins

**AI Behavior:**
```
✓ CORRECT: Use Bash for streaming (more specific)
  Bash(command="tail -f /var/log/app.log")

✗ INCORRECT: Use Read (less specific rule)
  Read(file_path="/var/log/app.log")  # Won't stream
```

**Lesson:** More specific context (more conditions) takes precedence

---

## Example 4: SHOULD + MUST Layering

**Scenario:**
```
User: "Create a comprehensive GenAI adoption framework presentation"
```

**Rules Triggered:**

1. **`progressive-content-complex-artifacts`** (MUST)
   - Context: taskType = ["New Artifact"], creating detailed presentation
   - Action: use /progressive-content

2. **`use-todo-list-complex-tasks`** (SHOULD)
   - Context: task has 3+ steps
   - Action: use TodoWrite

3. **`brevity-50-percent-fewer-words`** (SHOULD)
   - Context: communicating with user
   - Action: concise language

**Resolution:** All rules apply (different aspects, non-conflicting)

**AI Behavior:**
```
✓ CORRECT: Apply all 3 rules
  "Complex artifact: Detailed presentation.
   Using /progressive-content (6 stages).

   [Creates todo list]
   Todos:
   1. Stage 0: Seeding
   2. Stage 1: Structure
   ...

   Stage 0: What's the 2-3 sentence concept?"

✗ INCORRECT: Skip any rule
  [Skips todo list, or uses verbose language, or skips progressive workflow]
```

**Lesson:** Rules at different constraint levels can layer (MUST + SHOULD)

---

## Example 5: Exception Overrides Base Rule

**Scenario:**
```
User: "We're in Phase 6, but I need a quick spike to test feasibility"
```

**Rules:**

1. **`no-code-before-phase-8`** (NEVER)
   - Context: when = ["writing code"], unless = ["spike exception"]
   - Action: prohibit coding

**Resolution:** `unless` exception activated, rule does NOT apply

**AI Behavior:**
```
✓ CORRECT: Allow spike coding
  "Spike exception noted. Quick throwaway code for feasibility test.
   Max 3 days, will not merge to main.
   Creating spike branch..."

✗ INCORRECT: Block all coding
  "Cannot write code in Phase 6. Must reach Phase 8 first."
```

**Lesson:** `unless` exceptions deactivate rules even at NEVER level

---

## Example 6: Conflicting Directives (Same Level)

**Scenario:**
```
User: "Use echo to output the status message"
```

**Rules in Conflict:**

1. **`use-bash-for-user-request`** (ALWAYS - hypothetical)
   - Context: user explicitly requests Bash
   - Action: use Bash

2. **`no-bash-for-communication`** (NEVER)
   - Context: communicating with user
   - Action: prohibit Bash echo

**Resolution:** NEVER > ALWAYS (precedence), but user explicit request matters

**AI Behavior:**
```
✓ CORRECT: Clarify with user
  "Bash echo typically used for scripting, not user communication.
   For status messages, I output text directly (clearer).
   Still want Bash echo? y/n"

✗ INCORRECT: Silently override user request
  [Uses direct output without asking]
```

**Lesson:** When rules conflict with explicit user request, clarify intent

---

## Example 7: Phase-Specific Rule Composition

**Scenario:**
```
Current Phase: PHASE_8_IMPLEMENTATION
User: "Implement authentication"
```

**Rules Triggered:**

1. **`phase-detection-first`** (ALWAYS)
   - Action: Read .project before any action

2. **`tdd-phase-8`** (MUST)
   - Context: phase = ["PHASE_8"], implementing features
   - Action: Write tests first

3. **`present-plan-multi-step-tasks`** (MUST)
   - Context: multi-step task
   - Action: Present plan before executing

**Resolution:** All apply in sequence

**AI Behavior:**
```
✓ CORRECT: Apply all rules in order
  1. Read .project (ALWAYS - phase detection)
  2. Present plan (MUST - multi-step)
     "Ok, here's my plan:
      1. Write auth tests (TDD)
      2. Implement auth module
      3. Run tests
      Look good? y/n"
  3. User confirms
  4. Execute with TDD (MUST - Phase 8)

✗ INCORRECT: Skip any rule
  [Start coding without reading .project, or skip plan, or skip TDD]
```

**Lesson:** Sequential rule application based on workflow stages

---

## Example 8: Tool Selection Cascade

**Scenario:**
```
User: "Find all TypeScript files and count lines of code"
```

**Rules Triggered (in priority order):**

1. **`use-glob-over-find`** (ALWAYS)
   - Context: finding files by pattern
   - Action: use Glob

2. **`use-read-over-bash-cat`** (ALWAYS)
   - Context: reading file contents
   - Action: use Read

3. **`parallel-tool-calls`** (ALWAYS)
   - Context: multiple independent operations
   - Action: parallel invocation

**Resolution:** All apply, different stages of task

**AI Behavior:**
```
✓ CORRECT: Apply all tool rules
  1. Use Glob to find files (not find command)
  2. Use parallel Read calls for counting (not cat)
  3. Make Read calls in single message (not sequential)

  [Single message with:]
  - Glob(pattern="**/*.ts")
  - [After getting file list, in next message:]
  - Read(file1) + Read(file2) + ... [parallel]

✗ INCORRECT: Use Bash for everything
  Bash(command="find . -name '*.ts' -exec wc -l {} \\;")
```

**Lesson:** Tool selection rules cascade through task stages

---

## Example 9: Override with Rationale (SHOULD vs User Preference)

**Scenario:**
```
User: "Use lots of emojis in your response to make it fun! 🎉"
```

**Rules:**

1. **`no-emojis-default`** (SHOULD_NOT)
   - Context: communicating with user, unless = ["user requested emojis"]
   - Action: avoid emojis

**Resolution:** User explicit request activates `unless` exception

**AI Behavior:**
```
✓ CORRECT: Honor user preference (exception)
  "Got it! 🎉 I'll use emojis as requested. ✨
   Creating the feature now... 🚀"

✗ INCORRECT: Ignore user preference
  "Got it. I'll create the feature now."
```

**Lesson:** `unless` conditions allow user preferences to override defaults

---

## Example 10: Complex Multi-Rule Scenario

**Scenario:**
```
Current Phase: PHASE_8_IMPLEMENTATION
User: "Refactor all 30 API endpoints to use new middleware"
Task Type: Task (multi-step, complex)
Destructive: No (refactor, not delete)
```

**All Rules Triggered:**

1. **`phase-detection-first`** (ALWAYS) → Read .project
2. **`present-plan-multi-step-tasks`** (MUST) → Show plan
3. **`confirm-bulk-file-operations`** (MUST) → Confirm 30 files
4. **`use-todo-list-complex-tasks`** (SHOULD) → Track progress
5. **`tdd-phase-8`** (MUST) → Tests first
6. **`brevity-50-percent-fewer-words`** (SHOULD) → Concise language

**AI Behavior:**
```
✓ CORRECT: Apply all rules systematically
  [1. Read .project - ALWAYS]
  [2. Create todo list - SHOULD]
  Todos:
  1. Identify 30 endpoints
  2. Create middleware
  3. Write tests for middleware (TDD)
  4. Refactor endpoints
  5. Run full test suite

  [3. Present plan - MUST]
  Plan:
  1. Find endpoints (Grep API routes)
  2. Create error middleware
  3. Write middleware tests (TDD - Phase 8)
  4. Update 30 endpoints to use middleware
  5. Run tests, fix failures

  Btw, affecting 30 files, following TDD pattern.
  Time: 30-45 min.

  [4. Confirm bulk operation - MUST]
  Look good? y/n

✗ INCORRECT: Skip rules or apply out of order
  [Immediately starts refactoring without plan/confirmation]
```

**Lesson:** Complex scenarios require orchestrating multiple rules across constraint levels

---

## Rule Composition Principles

1. **Precedence:** NEVER > ALWAYS > MUST > MUST_NOT > SHOULD > SHOULD_NOT > PREFER > AVOID
2. **Specificity:** More context conditions = more specific = higher priority
3. **Exceptions:** `unless` conditions can override even high-precedence rules
4. **Layering:** Rules at different levels can combine (MUST + SHOULD both apply)
5. **User Override:** Explicit user requests can activate exception conditions
6. **Additive:** Non-conflicting rules all apply
7. **Clarification:** When rules conflict with user request, ask for clarification
