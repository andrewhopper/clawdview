# AI Steering Rules - Index

**Version:** 1.1.0  
**Last Updated:** 2025-11-19  
**Generated:** 2025-11-19 21:50:23

Combined index of all AI steering rules

## Summary

- **Total Rules:** 72
- **Total Categories:** 8

### Constraint Levels

- 🚫 **NEVER:** 15 rules
- ✅ **ALWAYS:** 16 rules
- ⚠️ **MUST:** 22 rules
- ❌ **MUST_NOT:** 0 rules
- 💡 **SHOULD:** 11 rules
- ⚡ **SHOULD_NOT:** 7 rules
- 👍 **PREFER:** 1 rules
- 👎 **AVOID:** 0 rules

## Categories

### 🟡 Tool Usage

**File:** `tool-usage.json`  
**Rules:** 8  
**Priority:** high  
Rules for selecting and using tools (Read, Grep, Glob, Edit, etc.)

[📄 View Generated Docs](./tool-usage.md)

### 🟡 File Operations

**File:** `file-operations.json`  
**Rules:** 7  
**Priority:** high  
Rules for file/directory operations (create, modify, delete)

[📄 View Generated Docs](./file-operations.md)

### 🔴 Workflow

**File:** `workflow.json`  
**Rules:** 8  
**Priority:** critical  
Rules for task execution, planning, progress tracking

[📄 View Generated Docs](./workflow.md)

### 🟢 Communication

**File:** `communication.json`  
**Rules:** 5  
**Priority:** medium  
Rules for AI responses, tone, formatting

[📄 View Generated Docs](./communication.md)

### 🟡 Git

**File:** `git.json`  
**Rules:** 7  
**Priority:** high  
Rules for git operations (commit, push, branches)

[📄 View Generated Docs](./git.md)

### 🔴 Sdlc

**File:** `sdlc-phases.json`  
**Rules:** 11  
**Priority:** critical  
Rules for SDLC phase transitions, deliverables, gates

[📄 View Generated Docs](./sdlc-phases.md)

### 🟢 Artifacts

**File:** `artifacts.json`  
**Rules:** 11  
**Priority:** medium  
Rules for creating documents, presentations, diagrams

[📄 View Generated Docs](./artifacts.md)

### 🟡 Anti-Patterns

**File:** `anti-patterns.json`  
**Rules:** 15  
**Priority:** high  
Common bad patterns to avoid (AI theater, fake limitations, etc.)

[📄 View Generated Docs](./anti-patterns.md)

## Usage

- **Loadall:** Load all rule files to get complete ruleset
- **Loadcategory:** Load specific category file for targeted rules
- **Matchcontext:** Filter rules by context (phase, taskType, filePattern, etc.)
- **Applyconstraints:** Enforce rules based on constraint level priority
- **Generatedocs:** Use generator to create markdown documentation from JSON

## Integration

- **claudeMd:** .claude/docs/core/CRITICAL_RULES.md references this system
- **intentDetection:** .claude/docs/core/INTENT_DETECTION.md uses rule matching
- **confirmationProtocol:** .claude/docs/core/CONFIRMATION_PROTOCOL.md enforces MUST/MUST_NOT
- **dynamicLoading:** Rules loaded on-demand based on detected context
- **generatedDocs:** Markdown guides generated from JSON source of truth
