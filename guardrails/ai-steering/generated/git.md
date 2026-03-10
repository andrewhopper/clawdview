# Git Rules

**Version:** 1.0.0  
**Last Updated:** 2025-11-19  
**Rule Count:** 7

## Table of Contents

1. [✅ no-branches-commit-to-main](#no-branches-commit-to-main)
2. [🚫 no-force-push-to-main](#no-force-push-to-main)
3. [🚫 never-skip-hooks](#never-skip-hooks)
4. [🚫 only-commit-when-asked](#only-commit-when-asked)
5. [⚠️ git-commit-message-format](#git-commit-message-format)
6. [✅ check-authorship-before-amend](#check-authorship-before-amend)
7. [💡 retry-network-operations](#retry-network-operations)

---

## Rules

### ✅ no-branches-commit-to-main

**Level:** ALWAYS
**Category:** git

Commit directly to main/current branch, no new branches

**Rationale:** Simplified workflow for prototyping, user manages branching strategy

**Context:**
- **When:** committing code
- **Unless:** user explicitly requests branch

**Action:**
- **Directive:** use
- **Target:** Direct commits to current branch
- **Alternative:** Only create branch if user explicitly requests

**Examples:**

1. **Scenario:** User: 'Commit the changes'
   - ✅ **Correct:** git add . && git commit -m 'message'
   - ❌ **Incorrect:** git checkout -b feature/new-feature && git commit

*Approved by: Andrew Hopper on 2025-11-19*

---
### 🚫 no-force-push-to-main

**Level:** NEVER
**Category:** git

Never force push to main/master without explicit request

**Rationale:** Prevent history rewriting on shared branches, data loss prevention

**Context:**
- **When:** pushing to remote
- **Destructive:** True

**Action:**
- **Directive:** prohibit
- **Target:** git push --force to main/master
- **Message:** "Force push to main destructive. Warn user if requested."

**Examples:**

1. **Scenario:** Push fails due to diverged history
   - ✅ **Correct:** Explain conflict, suggest pull or ask user how to proceed
   - ❌ **Incorrect:** Automatically run git push --force

*Approved by: Andrew Hopper on 2025-11-19*

---
### 🚫 never-skip-hooks

**Level:** NEVER
**Category:** git

Never use --no-verify or --no-gpg-sign unless explicitly requested

**Rationale:** Hooks enforce quality/security standards, bypassing defeats purpose

**Context:**
- **When:** committing changes

**Action:**
- **Directive:** prohibit
- **Target:** Skip git hooks (--no-verify, --no-gpg-sign)
- **Alternative:** Let hooks run, fix issues if they fail

**Examples:**

1. **Scenario:** Pre-commit hook fails on linting
   - ✅ **Correct:** Fix linting errors, then commit
   - ❌ **Incorrect:** git commit --no-verify to bypass

*Approved by: Andrew Hopper on 2025-11-19*

---
### 🚫 only-commit-when-asked

**Level:** NEVER
**Category:** git

Never create commits unless user explicitly requests

**Rationale:** User controls commit timing, may want to review/test first

**Context:**
- **When:** made code changes
- **Unless:** user said 'commit', 'push', or similar

**Action:**
- **Directive:** prohibit
- **Target:** Proactive git commits
- **Message:** "Only commit when user explicitly asks"

**Examples:**

1. **Scenario:** Just finished implementing feature
   - ✅ **Correct:** Mention work complete, wait for user to request commit
   - ❌ **Incorrect:** Automatically run git add && git commit

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ git-commit-message-format

**Level:** MUST
**Category:** git

Use HEREDOC for git commit messages

**Rationale:** Ensures proper formatting, handles multi-line messages, avoids quote escaping

**Context:**
- **When:** creating git commits

**Action:**
- **Directive:** use
- **Target:** HEREDOC format for commit messages
- **Message:** "git commit -m "$(cat <<'EOF'\nMessage here\nEOF\n)""

**Examples:**

1. **Scenario:** Committing with message
   - ✅ **Correct:** git commit -m "$(cat <<'EOF'\nfeat: Add auth\nEOF\n)"
   - ❌ **Incorrect:** git commit -m 'feat: Add auth' (quote issues if message complex)

*Approved by: Andrew Hopper on 2025-11-19*

---
### ✅ check-authorship-before-amend

**Level:** ALWAYS
**Category:** git

Check commit author before amending

**Rationale:** Amending others' commits rewrites their history, collaboration issue

**Context:**
- **When:** using git commit --amend

**Action:**
- **Directive:** require
- **Target:** Check git log -1 --format='%an %ae' before amend
- **Message:** "Never amend other developers' commits"

**Examples:**

1. **Scenario:** Need to amend commit after pre-commit hook changes
   - ✅ **Correct:** Check author matches current user, then amend
   - ❌ **Incorrect:** Blindly amend without checking author

*Approved by: Andrew Hopper on 2025-11-19*

---
### 💡 retry-network-operations

**Level:** SHOULD
**Category:** git

Retry git push/pull/fetch on network failures (4x exponential backoff)

**Rationale:** Transient network failures common, auto-retry improves success rate

**Context:**
- **When:** git push fails, git pull fails, git fetch fails
- **Unless:** non-network error like conflict, auth failure

**Action:**
- **Directive:** use
- **Target:** Exponential backoff retry (2s, 4s, 8s, 16s)
- **Message:** "Network error. Retrying with backoff..."

**Examples:**

1. **Scenario:** git push fails with network timeout
   - ✅ **Correct:** Wait 2s, retry. If fails, wait 4s, retry. Continue up to 4 attempts.
   - ❌ **Incorrect:** Immediately give up after first network failure

*Approved by: Andrew Hopper on 2025-11-19*

---
