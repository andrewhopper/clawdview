# AI Steering Semantic Layer

## Overview

Structured framework for expressing AI behavior constraints using semantic rules. Maps natural language directives ("always use X", "never do Y") to machine-readable policies that guide AI actions.

## Purpose

**Problem:** AI behavior rules scattered across documentation, hard to discover, inconsistent enforcement
**Solution:** Centralized semantic layer defining "always/never/must/should" rules with context matching

**Inspired by:**
- Semantic layers as "API for agentic world" (see `proto-semantic-layer-domain-model-65jge-035`)
- Guardrails tech/architecture preferences (`.guardrails/*.json`)
- CLAUDE.md enforcement rules

## Domain Model

```
┌────────────────────────────────────────────────────────────────┐
│                    AI STEERING SEMANTIC LAYER                   │
└────────────────────────────────────────────────────────────────┘

Core Entities:

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Rule     │────▶│   Context   │────▶│   Action    │
└─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │
      │                    │                    │
      ▼                    ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Constraint  │     │  Trigger    │     │  Outcome    │
│   Level     │     │  Condition  │     │  Behavior   │
└─────────────┘     └─────────────┘     └─────────────┘

Constraint Levels (descending priority):
1. NEVER     - Absolute prohibition, cannot override
2. ALWAYS    - Absolute requirement, cannot skip
3. MUST      - Required unless explicitly approved
4. MUST_NOT  - Prohibited unless explicitly approved
5. SHOULD    - Strong recommendation, can override with reason
6. SHOULD_NOT- Discouraged, can override with reason
7. PREFER    - Suggestion, lower priority
8. AVOID     - Mild discouragement
```

## Rule Schema

```json
{
  "rule": {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "id": "unique-rule-id",
    "version": "1.2.3",
    "level": "ALWAYS | NEVER | MUST | MUST_NOT | SHOULD | SHOULD_NOT | PREFER | AVOID",
    "category": "tool_usage | code_generation | file_operations | communication | workflow",
    "description": "Human-readable rule description",
    "context": {
      "when": ["condition1", "condition2"],
      "unless": ["exception1"],
      "phase": ["PHASE_8", "PHASE_9"],
      "filePattern": "**/*.ts",
      "taskType": ["Chore", "Task"]
    },
    "action": {
      "directive": "use | avoid | confirm | require | prohibit",
      "target": "specific tool/pattern/behavior",
      "alternative": "suggested alternative if avoided"
    },
    "rationale": "Why this rule exists",
    "examples": [
      {
        "scenario": "User asks to...",
        "correct": "AI should...",
        "incorrect": "AI should NOT..."
      }
    ],
    "metadata": {
      "status": "approved",
      "approvedBy": "User Name",
      "approvedDate": "2025-01-15",
      "namespace": "@protoflow/core",
      "source": "https://github.com/org/rules-repo",
      "deprecatedBy": "uuid-of-replacement-rule",
      "relatedRules": ["uuid1", "uuid2"],
      "changelog": [
        {
          "version": "1.2.3",
          "date": "2025-01-15",
          "changes": ["Fixed context matching bug", "Added new example"],
          "author": "User Name",
          "breaking": false
        }
      ]
    }
  }
}
```

## Rule Identity & Versioning

**UUID System:**
- Every rule has a **UUID v4** (globally unique identifier)
- UUID is **immutable** - never changes across rule versions
- Enables: rule references, deprecation chains, dependency tracking
- Format: `550e8400-e29b-41d4-a716-446655440000`

**Human-Readable ID:**
- `id` field uses kebab-case (e.g., `use-read-over-bash-cat`)
- Can change across versions (UUID remains stable)
- Used for documentation, human communication

**Semantic Versioning (per rule):**
```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (constraint level change, context breaking)
MINOR: New features (new examples, expanded context)
PATCH: Bug fixes (typos, clarifications)
```

**Examples:**
- `1.0.0` → `1.0.1`: Fixed typo in rationale (PATCH)
- `1.0.1` → `1.1.0`: Added new context trigger (MINOR)
- `1.1.0` → `2.0.0`: Changed SHOULD to MUST (MAJOR - breaking)

## Rule Lifecycle

**Status Progression:**
```
draft → experimental → approved → deprecated
   │         │            │           │
   └─────────┴────────────┴───────────┘
         (any status can transition)
```

**Status Meanings:**
- **draft:** Under development, not enforced
- **experimental:** Testing in limited contexts
- **approved:** Production-ready, enforced
- **deprecated:** Replaced by newer rule (see `deprecatedBy` UUID)

**Deprecation Example:**
```json
{
  "uuid": "old-rule-uuid",
  "id": "old-rule-name",
  "version": "3.0.0",
  "status": "deprecated",
  "deprecatedBy": "new-rule-uuid",
  "changelog": [
    {
      "version": "3.0.0",
      "changes": ["Deprecated in favor of new-rule-uuid"],
      "breaking": true
    }
  ]
}
```

## Changelog Tracking

Each rule maintains version history:

```json
{
  "changelog": [
    {
      "version": "1.2.0",
      "date": "2025-01-20",
      "changes": [
        "Added fileCount context",
        "Expanded examples with edge cases"
      ],
      "author": "Jane Developer",
      "breaking": false
    },
    {
      "version": "1.1.0",
      "date": "2025-01-10",
      "changes": ["Added unless condition for spikes"],
      "author": "John Engineer",
      "breaking": false
    },
    {
      "version": "1.0.0",
      "date": "2025-01-01",
      "changes": ["Initial rule creation"],
      "author": "Jane Developer",
      "breaking": false
    }
  ]
}
```

**Changelog Best Practices:**
- Always add entry when updating rule
- Mark `breaking: true` for MAJOR version bumps
- Be specific: "Added X" not "Updated rule"
- Include author for accountability

## Rule Composition

**Precedence (highest to lowest):**
1. NEVER/ALWAYS (absolute)
2. MUST/MUST_NOT (requires approval override)
3. SHOULD/SHOULD_NOT (strong recommendation)
4. PREFER/AVOID (weak recommendation)

**Context Matching:**
- Rules activate when ALL `when` conditions met
- Rules deactivate if ANY `unless` condition met
- More specific context wins over general rules

**Conflict Resolution:**
```
Rule A: ALWAYS use Bash for git operations
Rule B: NEVER use Bash without confirmation for destructive operations
Context: git reset --hard

Resolution: Rule B (NEVER) overrides Rule A (ALWAYS) because NEVER > ALWAYS
Action: Confirm before executing
```

## File Structure

```
.guardrails/ai-steering/
├── README.md                    # This file
├── schema.json                  # JSON schema for rule definitions
├── rules/
│   ├── tool-usage.json         # Rules for tool selection/usage
│   ├── code-generation.json    # Rules for code creation
│   ├── file-operations.json    # Rules for file/directory ops
│   ├── communication.json      # Rules for AI responses
│   ├── workflow.json           # Rules for task execution
│   └── index.json              # Combined rule index
└── examples/
    ├── basic-rules.md          # Simple rule examples
    ├── context-matching.md     # Context trigger examples
    └── composition.md          # Rule combination examples
```

## Integration with CLAUDE.md

**CLAUDE.md orchestrator** → Load `.guardrails/ai-steering/rules/*.json`
**Intent detection** → Match rule contexts
**Confirmation protocol** → Enforce MUST/MUST_NOT
**Task execution** → Apply ALWAYS/NEVER constraints

**Dynamic Loading:**
```
User request → Classify intent → Load relevant rule category → Match context → Apply constraints → Execute or confirm
```

## Example Rules

**Tool Usage:**
```json
{
  "id": "use-read-over-bash-cat",
  "level": "ALWAYS",
  "category": "tool_usage",
  "description": "Use Read tool instead of bash cat for file reading",
  "context": {
    "when": ["reading file contents"],
    "unless": ["streaming logs", "monitoring real-time output"]
  },
  "action": {
    "directive": "use",
    "target": "Read tool",
    "alternative": "Use Bash only for streaming/real-time scenarios"
  },
  "rationale": "Read tool optimized for file viewing, better UX, handles large files"
}
```

**Code Generation:**
```json
{
  "id": "tdd-phase-8",
  "level": "MUST",
  "category": "code_generation",
  "description": "Write tests before implementation code in Phase 8",
  "context": {
    "when": ["implementing new features"],
    "phase": ["PHASE_8_IMPLEMENTATION"]
  },
  "action": {
    "directive": "require",
    "target": "Test-first development",
    "alternative": null
  },
  "rationale": "TDD ensures quality, prevents regressions, documents expected behavior"
}
```

**File Operations:**
```json
{
  "id": "confirm-bulk-operations",
  "level": "MUST",
  "category": "file_operations",
  "description": "Confirm before operating on 20+ files",
  "context": {
    "when": ["file count >= 20"],
    "taskType": ["Chore", "Task"]
  },
  "action": {
    "directive": "confirm",
    "target": "Bulk file operations",
    "alternative": "Execute immediately for <20 files"
  },
  "rationale": "Prevent accidental large-scale changes, give user visibility"
}
```

**Communication:**
```json
{
  "id": "no-emojis-default",
  "level": "SHOULD_NOT",
  "category": "communication",
  "description": "Avoid emojis unless user explicitly requests",
  "context": {
    "when": ["communicating with user"],
    "unless": ["user requested emojis", "slash command output uses emojis"]
  },
  "action": {
    "directive": "avoid",
    "target": "Emoji usage",
    "alternative": "Plain text communication"
  },
  "rationale": "Professional tone, CLI-appropriate formatting"
}
```

**Workflow:**
```json
{
  "id": "progressive-content-complex-artifacts",
  "level": "MUST",
  "category": "workflow",
  "description": "Use progressive content flow for complex artifacts",
  "context": {
    "when": ["creating detailed presentation", "comprehensive documentation", "strategic documents"],
    "taskType": ["New Artifact"]
  },
  "action": {
    "directive": "use",
    "target": "/progressive-content workflow",
    "alternative": null
  },
  "rationale": "Stage-gated creation ensures quality, enables user feedback, prevents wasted effort"
}
```

## Usage Patterns

**AI reads rules at startup:**
```python
# Load all steering rules
rules = load_rules(".guardrails/ai-steering/rules/*.json")

# Match rules to current context
active_rules = match_context(rules, {
    "phase": current_phase,
    "taskType": detected_task_type,
    "fileCount": len(files_to_modify)
})

# Apply constraints
for rule in active_rules:
    if rule.level == "NEVER" and rule.matches(action):
        raise ConstraintViolation(rule)
    elif rule.level == "MUST" and not rule.satisfied(action):
        request_approval(rule, action)
```

**User overrides:**
```
User: "Skip confirmation for this file operation"
AI: Checking steering rules...
    - Rule: confirm-bulk-operations (MUST level)
    - User override requested
    - Logging override for audit
    - Proceeding without confirmation
```

## Benefits

1. **Discoverability:** All rules in one place, structured format
2. **Consistency:** Same enforcement across sessions
3. **Composability:** Rules combine predictably via precedence
4. **Explainability:** AI can cite rule when explaining behavior
5. **Evolvability:** Add rules without modifying CLAUDE.md
6. **Auditability:** Track rule applications and overrides

## Relationship to Other Systems

**Semantic Schema Mapper** (`proto-semantic-schema-mapper-v6mbz-027`):
- Three-tier inference (LLM, rule-based, fuzzy)
- Confidence scoring
- Human-in-the-loop approval
- **Semantic steering** uses similar concepts for behavior mapping

**Guardrails Tech/Arch Preferences**:
- Ranked preferences with rationale
- Use cases and examples
- Approval tracking
- **Semantic steering** extends this to behavior rules

**CLAUDE.md Orchestration**:
- Dynamic loading of documentation
- Phase detection
- Intent classification
- **Semantic steering** adds structured rule enforcement

## Future Enhancements

### 1. Remote Rules Repository (npm-like)

**Concept:** Centralized registry for sharing/distributing rules

**Package Manager Pattern:**
```bash
# Install rules from remote registry
ai-rules install @protoflow/core
ai-rules install @company/custom-rules@2.1.0

# Update to latest versions
ai-rules update

# List installed rules
ai-rules list

# Search registry
ai-rules search "file operations"
```

**Registry Structure:**
```
rules-registry/
├── @protoflow/
│   ├── core/              # Base rules (tool usage, workflow, etc.)
│   ├── sdlc/              # SDLC-specific rules
│   └── anti-patterns/     # Common anti-patterns
├── @anthropic/
│   ├── claude-code/       # Claude Code CLI rules
│   └── prompt-eng/        # Prompt engineering best practices
├── @company/
│   └── custom/            # Company-specific rules
```

**Namespace Format:**
- `@org/package` (e.g., `@protoflow/core`, `@anthropic/claude-code`)
- Enables: ownership, discoverability, conflict prevention
- Each package has own versioning (semver)

**Version Resolution:**
```json
{
  "dependencies": {
    "@protoflow/core": "^2.0.0",
    "@company/custom": "1.5.3"
  },
  "conflicts": {
    "resolve": "latest",
    "strategy": "merge"
  }
}
```

**Metadata in package.json:**
```json
{
  "name": "@protoflow/core",
  "version": "2.3.1",
  "description": "Core AI steering rules",
  "author": "Protoflow",
  "license": "MIT",
  "repository": "https://github.com/protoflow/ai-rules",
  "keywords": ["ai", "steering", "rules", "claude"],
  "rules": [
    {
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "id": "use-read-over-bash-cat",
      "version": "1.2.3",
      "category": "tool_usage"
    }
  ]
}
```

**Benefits:**
- **Sharing:** Teams/organizations share rule sets
- **Versioning:** Semantic versioning for packages + individual rules
- **Discovery:** Search registry for rules by category/keyword
- **Updates:** `ai-rules update` pulls latest approved rules
- **Conflict resolution:** Handle overlapping rules from multiple packages
- **Offline support:** Cache rules locally, work without network

**Implementation Phases:**
1. **Phase 1:** Local file system (current)
2. **Phase 2:** Git-based distribution (clone repos)
3. **Phase 3:** HTTP-based registry (npm-like)
4. **Phase 4:** CDN distribution for global availability

**Use Cases:**
- **Open source:** Community-curated rules (`@community/best-practices`)
- **Enterprise:** Company-wide standards (`@acme-corp/ai-policies`)
- **Tool-specific:** Claude Code rules (`@anthropic/claude-code`)
- **Domain-specific:** Healthcare, finance, legal rules

---

### 2. Learning & Analytics

**Track rule violations → suggest new rules:**
- Monitor rule override patterns
- Identify gaps in coverage
- Auto-generate draft rules from behavior

**A/B testing:**
- Compare rule sets for effectiveness
- Measure: task completion, error rates, user satisfaction
- Optimize rules based on data

---

### 3. Advanced Conflict Resolution

**Automatic detection:**
- Find overlapping/contradictory rules
- Suggest merge strategies
- Visualize rule dependencies

**Resolution strategies:**
- Most specific context wins
- Latest version wins
- User-defined precedence

---

### 4. Natural Language Interface

**Query examples:**
```
User: "What are the rules for file operations?"
AI: Loads file-operations.json, displays 7 rules

User: "Why can't I skip phase 6?"
AI: Cites rule uuid 550e8400... (never-skip-phases)

User: "Show deprecated rules"
AI: Filters by status=deprecated, shows migration paths
```

---

### 5. LLM-Powered Inference

**AI infers implicit rules from behavior patterns:**
- Analyze conversation history
- Detect consistent patterns (e.g., "always uses Edit after Read")
- Suggest codifying as explicit rules

**Rule mining:**
- Extract rules from CLAUDE.md, docs, conversations
- Generate draft rules with examples
- Human reviews/approves before activation

---

### 6. IDE/Tool Integration

**Editor plugins:**
- VS Code extension: Highlight rule violations in real-time
- CLI tools: `ai-rules check` validates behavior
- Git hooks: Pre-commit rule compliance

**Dashboards:**
- Rule coverage metrics
- Violation trends over time
- Most/least effective rules
