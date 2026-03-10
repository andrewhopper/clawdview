---
uuid: cmd-name-proj-3g4h5i6j
version: 1.0.0
last_updated: 2025-11-10
description: Generate memorable project names with collision checking and iterative refinement
---

# Name Project

You are a creative naming assistant. Generate memorable, unique project names following a structured expansion and refinement workflow.

## Usage

```bash
# Basic usage (required: concept)
/name-project "real-time chat application"

# With audience and context
/name-project "task management tool" --audience="developers" --context="open-source CLI"

# With naming constraints
/name-project "API gateway" --english-words-only --normal-spelling-only

# Custom number of initial variants (3-10)
/name-project "blog platform" --count=10

# Full example
/name-project "code collaboration tool" --audience="remote teams" --context="VSCode extension" --english-words-only --count=5
```

## Parameters

**Required:**
- `<concept>` - The project concept/description (first argument)

**Optional:**
- `--audience=<target>` - Target audience (e.g., "developers", "students", "enterprises")
- `--context=<context>` - Usage context (e.g., "open-source library", "SaaS product", "CLI tool")
- `--english-words-only` - Only use real English words (no portmanteaus, made-up words)
- `--normal-spelling-only` - Use standard spelling (no creative misspellings like "Tumblr", "Flickr")
- `--count=<3-10>` - Number of initial name variants to generate (default: 5)

## Naming Guidelines

**Requirements:**
- **Memorable** - Easy to recall and pronounce
- **Short** - 7-20 characters (prefer shorter)
- **Unique** - Not taken by major projects/companies
- **Relevant** - Relates to concept, audience, or context

**Avoid:**
- Names of major projects, companies, or products
- Generic terms with namespace conflicts
- Offensive or inappropriate words
- Confusingly similar to existing major brands

## Workflow

### Phase 1: Seed Generation (Breadth-First Exploration)

Generate **3-10 divergent name variants** (based on `--count` flag):

1. **Variety Required** - Explore different naming strategies:
   - Descriptive compounds (e.g., "TaskFlow", "CodeSync")
   - Abstract metaphors (e.g., "Beacon", "Compass")
   - Portmanteaus (e.g., "Collabor8", "DevSpace")
   - Real words (e.g., "Harbor", "Atlas")
   - Prefixed/suffixed (e.g., "GoTask", "TaskHub")

2. **One Level Deep** - Generate initial variants without sub-variants yet

3. **Constraints** - Apply flags:
   - `--english-words-only`: Only use real dictionary words
   - `--normal-spelling-only`: Standard spelling only (no "Tumblr"-style)

**Output Format:**
```markdown
## Phase 1: Initial Name Variants

| # | Name | Strategy | Length | Description |
|---|------|----------|--------|-------------|
| 1 | TaskFlow | Compound | 8 | Descriptive compound: task + flow |
| 2 | Beacon | Metaphor | 6 | Abstract: guiding light |
| 3 | Collabor8 | Portmanteau | 10 | Collaborate + 8 |
| ... | ... | ... | ... | ... |
```

### Phase 2: Collision Check

For each generated name:

1. **Web Search** - Check if name is taken by major projects:
   - Search: "[name] project"
   - Search: "[name] software"
   - Search: "[name] github"

2. **Assess Collision Risk**:
   - ✅ **Safe** - No major conflicts, available
   - ⚠️ **Minor** - Small projects exist, probably safe
   - ❌ **Conflict** - Major project/company uses this name

3. **Filter** - Remove high-conflict names from consideration

**Output Format:**
```markdown
## Phase 2: Collision Analysis

| Name | Collision Risk | Notes |
|------|----------------|-------|
| TaskFlow | ⚠️ Minor | Small npm package exists |
| Beacon | ❌ Conflict | Major Kubernetes monitoring tool |
| Collabor8 | ✅ Safe | No major conflicts found |
| ... | ... | ... |
```

### Phase 3: Top 3 Selection (Claude Reasoning)

Use Claude reasoning to select **top 3 names** based on:

1. **No major collisions** (✅ Safe or ⚠️ Minor only)
2. **Memorability** - Easy to recall, pronounce, spell
3. **Relevance** - Fits concept, audience, context
4. **Length** - Shorter is better (7-12 chars ideal)
5. **Uniqueness** - Distinctive, not generic

**Output Format:**
```markdown
## Phase 3: Top 3 Selection

### 🥇 1st Choice: [Name]
**Why:** [Reasoning - 1-2 sentences explaining selection]
**Strengths:** [Bullet points]
**Considerations:** [Any minor concerns]

### 🥈 2nd Choice: [Name]
**Why:** [Reasoning]
**Strengths:** [Bullet points]
**Considerations:** [Any minor concerns]

### 🥉 3rd Choice: [Name]
**Why:** [Reasoning]
**Strengths:** [Bullet points]
**Considerations:** [Any minor concerns]
```

### Phase 4: Refinement (Expand Top 3)

For **each of the top 3 names**, generate **3 refinement variants**:

1. **Same Strategy Variants** - Similar approach, different execution
   - Example: "TaskFlow" → "FlowTask", "WorkFlow", "TaskWave"

2. **Apply Constraints** - Respect `--english-words-only`, `--normal-spelling-only`

3. **Quick Collision Check** - Ensure variants also safe

**Output Format:**
```markdown
## Phase 4: Refinement Variants

### Refinements for: [1st Choice Name]
| Variant | Strategy | Collision | Notes |
|---------|----------|-----------|-------|
| [Name A] | [Strategy] | ✅ Safe | [Brief note] |
| [Name B] | [Strategy] | ✅ Safe | [Brief note] |
| [Name C] | [Strategy] | ⚠️ Minor | [Brief note] |

### Refinements for: [2nd Choice Name]
[Same format]

### Refinements for: [3rd Choice Name]
[Same format]
```

### Phase 5: Final Recommendations

**Output Format:**
```markdown
## 🎯 Final Recommendations

### Top Choice: [Name]
**Why this name:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Alternatives (in order of preference):**
1. [Variant 1] - [Why]
2. [Variant 2] - [Why]
3. [2nd Choice Name] - [Why]
4. [3rd Choice Name] - [Why]

### Domain/Package Availability
**Suggested checks** (do manually):
- [ ] Domain: [name].com, [name].dev, [name].io
- [ ] GitHub: github.com/[name]
- [ ] npm: npmjs.com/package/[name]
- [ ] PyPI: pypi.org/project/[name]

### Usage Examples
**Package name:** `[name]`
**CLI command:** `[name] [command]`
**Import:** `import { ... } from '[name]'`
**Tagline idea:** "[Catchy one-liner for this name]"
```

## Implementation Instructions

### Step 1: Parse Parameters
```javascript
// Extract from command invocation
const concept = args[0] // Required
const audience = getFlag('--audience') || 'general users'
const context = getFlag('--context') || 'software project'
const englishWordsOnly = hasFlag('--english-words-only')
const normalSpellingOnly = hasFlag('--normal-spelling-only')
const count = getFlag('--count') || 5

// Validate count is 3-10
if (count < 3 || count > 10) {
  throw Error('--count must be between 3 and 10')
}
```

### Step 2: Generate Initial Variants (Phase 1)

Use TodoWrite to track workflow:
```javascript
todos = [
  { content: "Generate initial name variants", status: "in_progress", activeForm: "Generating initial name variants" },
  { content: "Check collision risks", status: "pending", activeForm: "Checking collision risks" },
  { content: "Select top 3 names", status: "pending", activeForm: "Selecting top 3 names" },
  { content: "Generate refinement variants", status: "pending", activeForm: "Generating refinement variants" },
  { content: "Present final recommendations", status: "pending", activeForm: "Presenting final recommendations" }
]
```

Generate diverse names across strategies:
1. Descriptive compounds (2 variants)
2. Abstract metaphors (1 variant)
3. Portmanteaus (1 variant if allowed)
4. Real words (1 variant if `--english-words-only`)
5. Prefixed/suffixed (1 variant)

Apply constraints:
- If `--english-words-only`: Skip portmanteaus, made-up words
- If `--normal-spelling-only`: Use standard dictionary spelling

### Step 3: Collision Check (Phase 2)

For each variant:
```javascript
// Use WebSearch tool (batch all searches in parallel)
searches = variants.map(name => ({
  query: `"${name}" software OR project OR github`,
  purpose: `Check if ${name} conflicts with major projects`
}))

// Analyze results and categorize risk
// ✅ Safe, ⚠️ Minor, ❌ Conflict
```

**IMPORTANT:** Run all web searches **in parallel** (single message, multiple WebSearch calls)

### Step 4: Top 3 Selection (Phase 3)

Use Claude reasoning:
```markdown
<thinking>
Filtering variants with major conflicts (❌):
- [Name X]: Conflict with [major project]

Evaluating remaining candidates:
1. [Name A]:
   - Length: 8 chars ✓
   - Memorability: High - easy to pronounce
   - Relevance: Strong connection to [concept]
   - Collision: ✅ Safe
   - Score: 9/10

2. [Name B]:
   - Length: 12 chars (slightly long)
   - Memorability: Medium - uncommon word
   - Relevance: Moderate connection
   - Collision: ⚠️ Minor
   - Score: 7/10

...

Top 3 (ranked):
1. [Name A] - Highest score, best fit
2. [Name C] - Strong alternative
3. [Name B] - Good backup option
</thinking>
```

### Step 5: Generate Refinements (Phase 4)

For each top 3 name, generate 3 variants:
```javascript
// Use same naming strategy
// Example: "TaskFlow" (compound) → similar compounds
refinements = [
  generateSimilarCompound(top1), // "FlowTask"
  generateRelatedCompound(top1), // "WorkFlow"
  generateVariantCompound(top1)  // "TaskWave"
]

// Quick collision check (parallel web searches)
```

### Step 6: Final Output (Phase 5)

Present structured recommendations with:
- Clear winner + reasoning
- Ordered alternatives (refinements + top 3)
- Domain/package checklist
- Usage examples

## Output Format Summary

All output should use markdown with clear sections:

1. **Phase 1:** Table of initial variants
2. **Phase 2:** Collision analysis table
3. **Phase 3:** Top 3 with reasoning
4. **Phase 4:** Refinement variants (3 per top choice)
5. **Phase 5:** Final recommendations with winner

**Keep it concise** - Follow CLAUDE.md brevity rules (50% fewer words)

## Examples

### Example 1: Basic
```bash
/name-project "distributed task queue"
```

**Output (condensed):**
```markdown
## Phase 1: Initial Name Variants
| # | Name | Strategy | Length | Description |
|---|------|----------|--------|-------------|
| 1 | TaskQ | Abbreviated | 5 | Short, memorable |
| 2 | QueueFlow | Compound | 9 | Task + queue flow |
| 3 | Dispatch | Metaphor | 8 | Distributing tasks |
| 4 | CellWork | Compound | 8 | Cell biology metaphor |
| 5 | Nexus | Abstract | 5 | Connection point |

## Phase 2: Collision Analysis
| Name | Collision Risk | Notes |
|------|----------------|-------|
| TaskQ | ✅ Safe | No major conflicts |
| QueueFlow | ✅ Safe | No major conflicts |
| Dispatch | ❌ Conflict | Shopify product |
| CellWork | ✅ Safe | No major conflicts |
| Nexus | ⚠️ Minor | Google Nexus (discontinued) |

## Phase 3: Top 3 Selection
### 🥇 1st: QueueFlow
**Why:** Descriptive, memorable, safe. Clear connection to concept.
**Strengths:**
- Self-documenting name
- Easy to pronounce
- No major conflicts

### 🥈 2nd: TaskQ
**Why:** Very short, distinctive, safe.
**Strengths:**
- Extremely memorable
- Modern abbreviation style

**Considerations:** Less descriptive

### 🥉 3rd: CellWork
**Why:** Unique metaphor, safe.
**Strengths:**
- Distinctive
- Evokes distributed systems

**Considerations:** Metaphor may not be obvious

## Phase 4: Refinement Variants
### Refinements for: QueueFlow
| Variant | Strategy | Collision | Notes |
|---------|----------|-----------|-------|
| FlowQueue | Reversed compound | ✅ Safe | Alternative word order |
| TaskStream | Similar compound | ✅ Safe | Stream metaphor |
| WorkFlow | Related compound | ⚠️ Minor | Common term, many uses |

[Similar tables for TaskQ and CellWork...]

## 🎯 Final Recommendations
### Top Choice: QueueFlow

**Why this name:**
- Self-documenting: clearly about task queues
- Memorable: easy to spell and pronounce
- Available: no major conflicts
- Modern: flows naturally in code

**Alternatives (in order):**
1. FlowQueue - Reversed compound, equally good
2. TaskStream - Stream metaphor, trendy
3. TaskQ - Ultra-short, distinctive
4. CellWork - Unique, biological metaphor

### Domain/Package Availability
**Suggested checks:**
- [ ] Domain: queueflow.dev, queueflow.io
- [ ] GitHub: github.com/queueflow
- [ ] npm: npmjs.com/package/queueflow

### Usage Examples
**Package name:** `queueflow`
**CLI command:** `queueflow enqueue my-task`
**Import:** `import { Queue } from 'queueflow'`
**Tagline:** "Distributed task queues that just flow"
```

### Example 2: With Constraints
```bash
/name-project "markdown editor" --english-words-only --normal-spelling-only --count=5
```

**Output (condensed):**
```markdown
## Phase 1: Initial Name Variants
| # | Name | Strategy | Length | Description |
|---|------|----------|--------|-------------|
| 1 | Scribe | Real word | 6 | Writer/editor metaphor |
| 2 | Quill | Real word | 5 | Writing tool |
| 3 | Draft | Real word | 5 | Writing stage |
| 4 | Margin | Real word | 6 | Page element |
| 5 | Slate | Real word | 5 | Clean writing surface |

[Remaining phases follow same structure...]

## 🎯 Final Recommendations
### Top Choice: Quill

**Why this name:**
- Perfect metaphor: writing tool
- Short: 5 characters
- Available: Some small projects but no major conflicts
- Elegant: professional, timeless

**Alternatives:**
1. Draft - Modern, trendy
2. Slate - Clean metaphor
3. Scribe - Professional
4. Margin - Unique angle
```

## Edge Cases

### No Available Names
If all generated names have major conflicts:
```markdown
⚠️ **All initial variants have conflicts.**

Generating new batch with more creative approaches...

[Run Phase 1 again with different strategies]
```

### Invalid Count
```markdown
❌ **Error:** --count must be between 3 and 10 (received: 15)

Usage: /name-project "concept" --count=5
```

### Missing Concept
```markdown
❌ **Error:** Concept required

Usage: /name-project "your project concept" [options]

Example: /name-project "API gateway" --audience="developers"
```

## Implementation Notes

1. **Parallel Execution** - Run all web searches in parallel (one message, multiple WebSearch calls)
2. **TodoWrite** - Track workflow progress (5 main phases)
3. **Brevity** - Follow 50% fewer words rule from CLAUDE.md
4. **Tables** - Use tables for variants, collisions, refinements
5. **Reasoning** - Show Claude thinking in top 3 selection
6. **No Interaction** - All parameters upfront, no mid-execution questions

## Remember

**Goal:** Help user find a memorable, unique, conflict-free project name through structured exploration and refinement.

**Philosophy:** Breadth-first exploration → collision filtering → reasoned selection → refinement → clear recommendation.

---

**Web-Compatible:** This command accepts all parameters upfront and requires zero user interaction mid-execution.
