---
description: Track workflow errors and prevent future occurrences
---

# Error Tracking and Prevention

You are tasked with tracking workflow errors and preventing future occurrences.

**Configuration:** File paths are defined in `shared/config.yaml` under `error_tracking`:
- `log_dir`: Directory for all error logs
- `error_log_text`: Plain text error log file
- `error_log_yaml`: YAML structured error log file

Logs errors to both text and YAML formats with status tracking.

## Your Tasks:

1. **Analyze the Error Context**
   - Review the recent conversation history to identify any errors, failures, or issues that occurred
   - Extract error messages, stack traces, failed commands, or problematic operations
   - Identify the root cause and contributing factors
   - **Categorize the violation type**: Determine if it's SDLC, tech-standard, confirmation, data-grounding, etc.
   - **Capture prior messages**: Extract the prior 10 messages from conversation history (if relevant)
   - **Capture artifact URLs**: Extract any URLs for generated artifacts (S3 URLs, deployed sites, etc.)

2. **Create Error Entry Using CLI Tool**
   - Use `hmode/shared/tools/rlhf-reward-punishment-tracker.py` to quickly generate error file:
     ```bash
     hmode/shared/tools/rlhf-reward-punishment-tracker.py new "Brief description" \
       --category cat1,cat2 \
       --type "Error classification"
     ```
   - **Category values** - ALWAYS categorize violations (comma-separated, can be multiple):
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
   - The tool will return UUID, ID, and filename
   - This creates a YAML file in `data/rlhf/signals/punishments/` with basic structure

3. **Enrich the Error Entry**
   - Read the generated YAML file
   - Update the following fields with detailed analysis:
     - `description`: Expand with full details of what went wrong
     - `context`: Add relevant code, commands, or operations that led to the error
     - `root_cause`: Your analysis of why it happened
     - `prevention`: Specific guidelines to prevent this in the future
     - `prior_messages`: Add relevant conversation excerpts (if applicable)
     - `artifact_urls`: Add any S3 URLs or deployed site URLs (if applicable)
     - `severity`: Update if needed (low/medium/high/critical)
   - Write the updated YAML back to the file

4. **Analyze Prevention Strategies**
   - Determine what instructions or guidelines could prevent this error in the future
   - Consider if this is a:
     - Coding pattern to avoid or follow
     - Tool usage issue
     - Missing validation or check
     - Documentation gap
     - Configuration issue

5. **Update Prevention Documentation**
   - Read the current CLAUDE.md file (if it exists in this project: `.claude/CLAUDE.md`, or globally: `~/.claude/CLAUDE.md`)
   - Propose specific additions or modifications to prevent this error class
   - Create or update `.claude/CLAUDE.md` with new guidelines under an appropriate section
   - If the error relates to specific files or patterns, consider creating/updating:
     - `.claude/patterns.md` - for code patterns to follow/avoid
     - `.claude/checklist.md` - for validation steps before operations

6. **Summary Report**
   - Provide a concise summary of:
     - What error was logged (or updated)
     - Error UUID and ID for future reference
     - What documentation was updated
     - How this prevents future occurrences
     - Any recommended immediate actions

## Important Notes:
- Be specific in your prevention guidelines, not generic
- Use code examples where applicable
- Cross-reference related guidelines if they exist
- Maintain consistency with existing documentation style
- Focus on actionable, concrete instructions

Now proceed with error tracking and prevention based on the recent conversation context.
