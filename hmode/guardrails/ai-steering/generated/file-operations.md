# File Operations Rules

**Version:** 1.0.0  
**Last Updated:** 2025-11-19  
**Rule Count:** 7

## Table of Contents

1. [⚠️ confirm-bulk-file-operations](#confirm-bulk-file-operations)
2. [💡 brief-summary-medium-file-operations](#brief-summary-medium-file-operations)
3. [👍 execute-small-file-operations](#execute-small-file-operations)
4. [⚠️ confirm-destructive-operations](#confirm-destructive-operations)
5. [✅ prefer-edit-over-write-existing](#prefer-edit-over-write-existing)
6. [⚠️ read-before-write-existing](#read-before-write-existing)
7. [🚫 no-proactive-documentation](#no-proactive-documentation)

---

## Rules

### ⚠️ confirm-bulk-file-operations

**Level:** MUST
**Category:** file_operations

Confirm before operating on 20+ files

**Rationale:** Prevent accidental large-scale changes, give user visibility and control

**Context:**
- **When:** modifying files, creating files, deleting files
- **Min Files:** 20
- **Task Types:** Chore, Task

**Action:**
- **Directive:** confirm
- **Target:** Bulk file operations (20+ files)
- **Message:** "Operating on {count} files. Time estimate: {estimate}. Confirm?"

**Examples:**

1. **Scenario:** User: 'Update all .project files with new field'
   - ✅ **Correct:** Count files (30), confirm with user before proceeding
   - ❌ **Incorrect:** Immediately update all 30 files without confirmation

*Approved by: Andrew Hopper on 2025-11-19*

---
### 💡 brief-summary-medium-file-operations

**Level:** SHOULD
**Category:** file_operations

Brief summary for 6-20 file operations

**Rationale:** Balance between visibility and efficiency

**Context:**
- **When:** modifying files, creating files
- **Min Files:** 6
- **Max Files:** 19

**Action:**
- **Directive:** paraphrase
- **Target:** Medium file operations (6-19 files)
- **Message:** "Updating {count} files: {brief_list}. Proceeding."

**Examples:**

1. **Scenario:** User: 'Add prettier config to all packages'
   - ✅ **Correct:** Brief: 'Adding prettier to 8 packages. Proceeding.'
   - ❌ **Incorrect:** Silently update all 8 without mention

*Approved by: Andrew Hopper on 2025-11-19*

---
### 👍 execute-small-file-operations

**Level:** PREFER
**Category:** file_operations

Execute immediately for 1-5 file operations

**Rationale:** Small operations obvious, don't need confirmation overhead

**Context:**
- **When:** modifying files, creating files
- **Max Files:** 5

**Action:**
- **Directive:** use
- **Target:** Immediate execution
- **Message:** "Updating {count} file(s). Done."

**Examples:**

1. **Scenario:** User: 'Fix the typo in README.md'
   - ✅ **Correct:** Immediately fix typo, mention completion
   - ❌ **Incorrect:** Ask for confirmation to fix 1 file

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ confirm-destructive-operations

**Level:** MUST
**Category:** file_operations

Always confirm destructive operations

**Rationale:** Prevent data loss, irreversible changes require explicit approval

**Context:**
- **When:** deleting files, force operations, major refactors
- **Destructive:** True

**Action:**
- **Directive:** confirm
- **Target:** Destructive file operations
- **Message:** "Destructive operation: {action} on {target}. Cannot undo. Confirm?"

**Examples:**

1. **Scenario:** User: 'Delete all old test files'
   - ✅ **Correct:** List files to delete, confirm before deletion
   - ❌ **Incorrect:** Immediately delete without showing what will be removed

*Approved by: Andrew Hopper on 2025-11-19*

---
### ✅ prefer-edit-over-write-existing

**Level:** ALWAYS
**Category:** file_operations

Use Edit instead of Write for existing files

**Rationale:** Edit safer for modifications, prevents accidental overwrites, preserves context

**Context:**
- **When:** modifying existing file content

**Action:**
- **Directive:** use
- **Target:** Edit tool for existing files
- **Alternative:** Write only for new files

**Examples:**

1. **Scenario:** User: 'Update the API endpoint in config.ts'
   - ✅ **Correct:** Use Edit with old_string/new_string
   - ❌ **Incorrect:** Use Write to overwrite entire file

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ read-before-write-existing

**Level:** MUST
**Category:** file_operations

Read existing file before using Write tool

**Rationale:** Write tool will error if file not read first, prevents accidental overwrites

**Context:**
- **When:** using Write tool, file exists

**Action:**
- **Directive:** require
- **Target:** Read file before Write
- **Message:** "Must read existing file before overwriting with Write tool"

**Examples:**

1. **Scenario:** User: 'Rewrite the entire config file'
   - ✅ **Correct:** Read config file first, then use Write
   - ❌ **Incorrect:** Use Write without reading (will error)

*Approved by: Andrew Hopper on 2025-11-19*

---
### 🚫 no-proactive-documentation

**Level:** NEVER
**Category:** file_operations

Never create documentation files unless explicitly requested

**Rationale:** Avoid cluttering codebase, user knows when docs needed

**Context:**
- **When:** creating files
- **File Pattern:** `**/*.md`

**Action:**
- **Directive:** prohibit
- **Target:** Proactive README/doc creation
- **Alternative:** Only create docs when user explicitly asks

**Examples:**

1. **Scenario:** Just created a new util function
   - ✅ **Correct:** Do not create README.md for the util
   - ❌ **Incorrect:** Proactively create README.md documenting the util

*Approved by: Andrew Hopper on 2025-11-19*

---
