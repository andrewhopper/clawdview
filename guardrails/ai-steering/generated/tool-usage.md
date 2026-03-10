# Tool Usage Rules

**Version:** 1.0.0  
**Last Updated:** 2025-11-19  
**Rule Count:** 8

## Table of Contents

1. [✅ use-read-over-bash-cat](#use-read-over-bash-cat)
2. [✅ use-grep-over-bash-grep](#use-grep-over-bash-grep)
3. [✅ use-glob-over-find](#use-glob-over-find)
4. [✅ use-edit-over-sed](#use-edit-over-sed)
5. [✅ use-write-over-echo](#use-write-over-echo)
6. [🚫 no-bash-for-communication](#no-bash-for-communication)
7. [⚠️ use-task-for-codebase-exploration](#use-task-for-codebase-exploration)
8. [✅ parallel-tool-calls](#parallel-tool-calls)

---

## Rules

### ✅ use-read-over-bash-cat

**Level:** ALWAYS
**Category:** tool_usage

Use Read tool instead of bash cat/head/tail for file reading

**Rationale:** Read tool optimized for file viewing, better UX, handles large files, shows line numbers

**Context:**
- **When:** reading file contents, viewing files
- **Unless:** streaming logs in real-time, monitoring active processes

**Action:**
- **Directive:** use
- **Target:** Read tool
- **Alternative:** Only use Bash for streaming/real-time scenarios (tail -f, live logs)

**Examples:**

1. **Scenario:** User: 'Show me the contents of config.json'
   - ✅ **Correct:** Use Read tool to read config.json
   - ❌ **Incorrect:** Use Bash with 'cat config.json'

*Approved by: Andrew Hopper on 2025-11-19*

---
### ✅ use-grep-over-bash-grep

**Level:** ALWAYS
**Category:** tool_usage

Use Grep tool instead of bash grep/rg for code search

**Rationale:** Grep tool optimized for search, supports output modes, better performance

**Context:**
- **When:** searching code, finding patterns in files
- **Unless:** complex shell pipeline required

**Action:**
- **Directive:** use
- **Target:** Grep tool
- **Alternative:** Only use Bash grep for complex pipelines

**Examples:**

1. **Scenario:** User: 'Find all TODO comments'
   - ✅ **Correct:** Use Grep tool with pattern 'TODO'
   - ❌ **Incorrect:** Use Bash with 'grep -r TODO .'

*Approved by: Andrew Hopper on 2025-11-19*

---
### ✅ use-glob-over-find

**Level:** ALWAYS
**Category:** tool_usage

Use Glob tool instead of bash find/ls for file discovery

**Rationale:** Glob tool optimized for pattern matching, faster, cleaner results

**Context:**
- **When:** finding files by pattern, listing files
- **Unless:** complex find predicates needed

**Action:**
- **Directive:** use
- **Target:** Glob tool
- **Alternative:** Only use Bash find for complex predicates (mtime, size, etc.)

**Examples:**

1. **Scenario:** User: 'List all TypeScript files'
   - ✅ **Correct:** Use Glob with pattern '**/*.ts'
   - ❌ **Incorrect:** Use Bash with 'find . -name "*.ts"'

*Approved by: Andrew Hopper on 2025-11-19*

---
### ✅ use-edit-over-sed

**Level:** ALWAYS
**Category:** tool_usage

Use Edit tool instead of bash sed/awk for file editing

**Rationale:** Edit tool ensures exact matching, prevents errors, preserves formatting

**Context:**
- **When:** modifying files, replacing text
- **Unless:** streaming edits on large files

**Action:**
- **Directive:** use
- **Target:** Edit tool
- **Alternative:** Only use Bash sed/awk for streaming scenarios

**Examples:**

1. **Scenario:** User: 'Update the API endpoint URL'
   - ✅ **Correct:** Use Edit tool with old_string/new_string
   - ❌ **Incorrect:** Use Bash with 'sed -i ...'

*Approved by: Andrew Hopper on 2025-11-19*

---
### ✅ use-write-over-echo

**Level:** ALWAYS
**Category:** tool_usage

Use Write tool instead of bash echo/cat for file creation

**Rationale:** Write tool safer, handles special characters, clear intent

**Context:**
- **When:** creating new files, writing file contents

**Action:**
- **Directive:** use
- **Target:** Write tool

**Examples:**

1. **Scenario:** User: 'Create a config file'
   - ✅ **Correct:** Use Write tool with file_path and content
   - ❌ **Incorrect:** Use Bash with 'echo ... > config.json'

*Approved by: Andrew Hopper on 2025-11-19*

---
### 🚫 no-bash-for-communication

**Level:** NEVER
**Category:** tool_usage

Never use Bash echo to communicate with user

**Rationale:** Bash is for system operations, not communication. Direct output clearer.

**Context:**
- **When:** communicating thoughts, explaining to user

**Action:**
- **Directive:** prohibit
- **Target:** Bash echo for user communication
- **Alternative:** Output text directly in response

**Examples:**

1. **Scenario:** AI wants to explain next steps
   - ✅ **Correct:** Output explanation text directly
   - ❌ **Incorrect:** Use 'echo "Next steps are..."'

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ use-task-for-codebase-exploration

**Level:** MUST
**Category:** tool_usage

Use Task tool with Explore subagent for non-needle codebase exploration

**Rationale:** Explore agent optimized for broad codebase understanding, reduces token usage

**Context:**
- **When:** exploring codebase structure, understanding architecture, finding related code
- **Unless:** searching for specific class/function name, reading specific known file

**Action:**
- **Directive:** use
- **Target:** Task tool (Explore subagent)
- **Alternative:** Direct Glob/Grep only for needle queries (specific class/function)

**Examples:**

1. **Scenario:** User: 'Where are errors from the client handled?'
   - ✅ **Correct:** Use Task tool with Explore subagent
   - ❌ **Incorrect:** Use Grep directly to search for 'error' everywhere

2. **Scenario:** User: 'Find the ErrorHandler class'
   - ✅ **Correct:** Use Grep to find 'class ErrorHandler' (needle query)
   - ❌ **Incorrect:** Use Task tool for simple class search

*Approved by: Andrew Hopper on 2025-11-19*

---
### ✅ parallel-tool-calls

**Level:** ALWAYS
**Category:** tool_usage

Make independent tool calls in parallel within single message

**Rationale:** Maximize performance, reduce latency, follow Claude Code best practices

**Context:**
- **When:** multiple independent operations needed
- **Unless:** operations depend on previous results

**Action:**
- **Directive:** use
- **Target:** Parallel tool invocation pattern
- **Alternative:** Sequential calls only when dependencies exist

**Examples:**

1. **Scenario:** Need to read 3 unrelated files
   - ✅ **Correct:** Single message with 3 Read tool calls
   - ❌ **Incorrect:** 3 separate messages with 1 Read call each

2. **Scenario:** Read file A, then use contents to search file B
   - ✅ **Correct:** Sequential: Read A, then search B with results
   - ❌ **Incorrect:** Parallel calls (would fail, B search needs A contents)

*Approved by: Andrew Hopper on 2025-11-19*

---
