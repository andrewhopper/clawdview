---
name: error-detection
description: Error tracking and prevention skill. Activate when user says error, bug, fail, failure, WTF, broke, broken, crash, crashed, something went wrong, or expresses frustration about something not working. Tracks workflow errors and prevents future occurrences.
version: 1.0.0
---

# Error Detection Skill

**Automatically activated on error-related keywords: error, bug, fail, WTF, broke, broken, crash, something went wrong**

This skill performs the same function as `/track-errors` - logging errors and preventing future occurrences.

## Trigger Keywords

This skill activates when the user mentions:
- "error" / "errors"
- "bug" / "bugs"
- "fail" / "failed" / "failure"
- "WTF" / "wtf"
- "broke" / "broken"
- "crash" / "crashed"
- "something went wrong"
- "not working"
- "doesn't work"

## Configuration

File paths are defined in `shared/config.yaml` under `error_tracking`:
- `log_dir`: Directory for all error logs
- `error_log_text`: Plain text error log file
- `error_log_yaml`: YAML structured error log file

## Execution Flow

### 1. Analyze the Error Context

- Review the recent conversation history to identify any errors, failures, or issues that occurred
- Extract error messages, stack traces, failed commands, or problematic operations
- Identify the root cause and contributing factors
- **Categorize the violation type**: Determine if it's SDLC, tech-standard, confirmation, data-grounding, etc.
- **Capture prior messages**: Extract the prior 10 messages from conversation history
- **Capture artifact URLs**: Extract any URLs for generated artifacts (S3 URLs, deployed sites, etc.)

### 2. Log the Error

Read `shared/config.yaml` to get `error_tracking.error_log_text` path. Create or append to the text error log:

```
================================================================================
Timestamp: [Current Date and Time]
UUID: [Universally unique identifier]
Error ID: [Human-readable identifier, e.g., ERR-YYYYMMDD-NNNN]
Error Type: [Brief classification]
Category: [Violation categories, comma-separated]

Description:
[Detailed description of what went wrong]

Root Cause:
[Analysis of why it happened]

Context:
[Relevant code, commands, or operations that led to the error]

Artifact URLs:
[List of URLs for any generated artifacts]

Prior Messages (Last 10):
[Excerpt of prior 10 messages from conversation history]

================================================================================
```

**Also log to YAML**: Read `shared/config.yaml` to get `error_tracking.error_log_yaml` path:

```yaml
errors:
  - uuid: 550e8400-e29b-41d4-a716-446655440000
    id: ERR-YYYYMMDD-NNNN
    date: "ISO 8601 timestamp"
    error: "Brief error description"
    error_type: "Classification"
    category:
      - violation-category
    context: |
      Detailed context including code/commands
    root_cause: |
      Analysis of why it happened
    status: new
    notes: []
    artifact_urls: []
    prior_messages: []
    created_at: "ISO 8601 timestamp"
    updated_at: "ISO 8601 timestamp"
```

### 3. Category Values

ALWAYS categorize violations (use array, can be multiple):

- `sdlc-violation` - Violated SDLC process (coded before Phase 8, skipped test design, no TDD)
- `confirmation-protocol` - Failed to use confirmation protocol for complex/ambiguous tasks
- `tech-standard` - Didn't follow tech standards (used pip vs uv, avoided AWS CDK, wrong tool)
- `guardrails` - Modified protected files or ignored guardrails without approval
- `data-grounding` - Invented data (contacts, library versions, technical details)
- `parallel-execution` - Failed to batch operations in single message
- `git-workflow` - Violated git rules (created branches, used disallowed commands)
- `tool-selection` - Wrong tool choice (bash for file ops, didn't delegate to sub-agents)
- `domain-model` - Didn't decompose domain models or check shared registry
- `file-size` - Created files exceeding 300-500 line limit
- `testing` - Failed to test after creating (APIs, UIs, S3 URLs)
- `documentation` - Missing source citations, no file paths/line numbers
- `asset-generation` - Didn't declare count upfront for multiple assets
- `brevity` - Used too many words, didn't densify writing
- `critical-rules` - Violated one of 27 CRITICAL RULES from CLAUDE.md
- `technical-error` - Actual code/runtime/logic error (not process violation)
- `other` - Other issues not fitting above categories

### 4. Analyze Prevention Strategies

- Determine what instructions or guidelines could prevent this error in the future
- Consider if this is a:
  - Coding pattern to avoid or follow
  - Tool usage issue
  - Missing validation or check
  - Documentation gap
  - Configuration issue

### 5. Update Prevention Documentation

- Propose specific additions or modifications to prevent this error class
- Create or update `.claude/CLAUDE.md` with new guidelines under an appropriate section
- If the error relates to specific files or patterns, consider creating/updating:
  - `.claude/patterns.md` - for code patterns to follow/avoid
  - `.claude/checklist.md` - for validation steps before operations

### 6. Summary Report

Provide a concise summary of:
- What error was logged
- Error UUID and ID for future reference
- What documentation was updated
- How this prevents future occurrences
- Any recommended immediate actions

## Important Notes

- Be specific in prevention guidelines, not generic
- Use code examples where applicable
- Cross-reference related guidelines if they exist
- Maintain consistency with existing documentation style
- Focus on actionable, concrete instructions
