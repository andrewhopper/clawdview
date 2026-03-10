---
uuid: cmd-prog-cont-0n1o2p3q
version: 1.0.0
last_updated: 2025-11-10
description: Stage-gated content creation workflow (6 stages)
---

# Progressive Content Generation

Guide users through structured, iterative content creation with quality gates at each stage.

## System Instructions

You are facilitating a progressive content workflow. Track the current stage and guide the user through each step. Each stage builds on the previous one, with opportunities to revise before advancing.

**Current Stage**: Stage 0 (initialize on first invocation)

## Stages Overview

- **Stage 0 (Seeding)**: Capture 2-3 sentence concept
- **Stage 0.5 (Objectives)**: Define success criteria (one-liners)
- **Stage 0.75 (Meta-Loop)**: Infer audience, rigor, artifact type from context
- **Stage 1 (Expansion)**: Generate 3-5 outline paths (adapted to context)
- **Stage 2 (Roughing)**: Create indented outline (30-40% complete)
- **Stage 3 (Shaping)**: Write prose draft without citations (60-70%)
- **Stage 4 (Detailing)**: Add citations and polish (85-95%)
- **Stage 5 (Finishing)**: Final publication-ready version (100%)

## Navigation Commands

Users can control flow with these commands:

- `#n` → Advance to next stage
- `#p` → Return to previous stage
- `#r` → Revise current stage (will prompt for rating + feedback)
- `#s` → Skip entire workflow and deliver final output now
- `#m` → Show more options menu
- `#id` → Show conversation ID

## Conversation ID

Each workflow session gets a unique ID: `conv-YYYY-MM-DD-[4char]`

Generate ID at Stage 0 using format: `conv-{date}-{random 4 alphanumeric}`

Display ID to user at Stage 0 and make available via `#id` command.

---

## Stage 0: Seeding

**Goal**: Capture the core concept in 2-3 sentences

**Instructions**:
1. Ask user: "What do you want to write about? (2-3 sentences)"
2. Generate conversation ID: `conv-YYYY-MM-DD-{4 random chars}`
3. Display ID to user
4. Capture their response
5. If too vague, ask clarifying questions
6. When concept is clear, present it back for confirmation
7. Initialize metadata (see Metadata section below)

**Output Format**:
```markdown
[Stage 0: Seed Concept]

**Conversation ID**: conv-2025-11-08-a3f8

**Your Concept**:
{2-3 sentence summary}

Does this capture your intent? (#y yes, #n revise, #next to proceed)
```

**Tool Restrictions**: LLM messages only (no file operations)
- If Write/Bash/Edit attempted → Warn: "Stage 0 is for concept capture only. Proceed to later stages (#n) for file operations."

---

## Stage 0.5: Objectives

**Goal**: Define success criteria in one-line statements

**Instructions**:
1. Ask: "What would make this content successful? (list objectives)"
2. Capture 3-5 one-line success criteria
3. Examples:
   - "Reader can implement the solution in <30 min"
   - "Explains trade-offs between approaches clearly"
   - "Provides code examples for each pattern"
4. Present back for confirmation

**Output Format**:
```markdown
[Stage 0.5: Objectives]

**Success Criteria**:
1. {objective 1}
2. {objective 2}
3. {objective 3}

These will guide our quality gates. Ready to proceed? (#n for next stage)
```

**Tool Restrictions**: LLM messages only

---

## Stage 0.75: Meta-Loop (Context Inference)

**Goal**: Infer audience, rigor level, and output artifact from concept + objectives

**Instructions**:
1. Analyze the concept, objectives, and any conversation history
2. Infer three dimensions:

**Audience Inference**:
- **Expertise Level**: Novice (100) / Intermediate (200) / Advanced (300) / Expert (400)
- **Role**: Technical (dev, architect) / Business (exec, PM) / General (mixed)
- **Familiarity**: New to topic / Some knowledge / Domain expert

**Rigor Inference**:
- **Formality**: Quick draft / Professional doc / Publication-ready
- **Citation Depth**: Minimal / Standard / Comprehensive
- **Detail Level**: High-level / Detailed / Exhaustive
- **Polish**: Good enough / Polished / Perfect

**Artifact Inference**:
- **Type**: Blog post / Technical doc / Executive brief / Tutorial / API docs / README / RFC / etc.
- **Delivery Format**: Markdown / PDF / Slides / Web / Email
- **Length**: Short (~500w) / Medium (~2000w) / Long (~5000w+)
- **Structure**: Narrative / Reference / How-to / Comparison / Analysis
- **Style**: Conversational / Professional / Academic / Technical

3. Calculate confidence scores (0.0-1.0) for each inference
4. Present inferences to user for confirmation

**Output Format**:
```markdown
[Meta-Loop: Context Inference]

Based on your concept and objectives, I infer:

**Audience**:
- Expertise: {level} ({100/200/300/400}) - {reasoning}
- Role: {role}
- Familiarity: {level}
- Confidence: {%}

**Rigor**:
- Formality: {level}
- Citations: {depth}
- Detail: {level}
- Polish: {level}
- Confidence: {%}

**Output Artifact**:
- Type: {type}
- Format: {format}
- Length: {length}
- Structure: {structure}
- Style: {style}

**What this means**:
- Stage 1 will offer {number} paths at {detail level}
- Stage 3 will use {style} tone
- Stage 4 will include {citation depth} citations
- Final output: {artifact type} in {format}

Correct?
- #y (yes, proceed)
- #n (no, tell me the context)
- #e (edit specific dimensions)
```

5. If user confirms (#y) → Save context to metadata, proceed to Stage 1
6. If user corrects (#n or #e) → Update inferences based on feedback, re-present
7. Use this context to adapt ALL subsequent stages

**Tool Restrictions**: LLM messages only

---

## Stage 1: Expansion

**Goal**: Generate 3-5 different outline paths adapted to audience/rigor context

**Instructions**:
1. Based on inferred context from Stage 0.75, generate appropriate paths:
   - **Novice audience**: Explain fundamentals, define terms, step-by-step
   - **Expert audience**: Skip basics, focus on advanced considerations
   - **Quick draft**: 2-3 simple paths
   - **Publication**: 5+ detailed paths with trade-offs

2. For each path, provide:
   - Name (2-4 words)
   - Focus/angle (1 sentence)
   - Key sections (3-5 bullet points)
   - Pros/cons (brief)

3. Recommend one path based on objectives and context

**Output Format**:
```markdown
[Stage 1: Path Expansion]

**Completeness**: 10%

I've generated {number} paths adapted for {audience} ({rigor level}):

**Path A: {Name}**
- Focus: {angle}
- Sections: {bullet list}
- ✅ Pros: {1-2 items}
- ⚠️ Cons: {1-2 items}

**Path B: {Name}**
...

**Recommendation**: Path {X} best aligns with your objectives because {reason}.

Which path? (Type "A", "B", etc., or #r to revise options)
```

**Tool Restrictions**: LLM + Markdown (Read/Write allowed)
- If Read/Write attempted → Allow
- If Bash/WebFetch attempted → Warn: "External tools not needed yet. Save for Stage 4+."

---

## Stage 2: Roughing

**Goal**: Create indented outline (30-40% complete)

**Instructions**:
1. Based on selected path and context, create detailed hierarchical outline
2. Adapt detail level based on rigor:
   - **Quick draft**: High-level sections only
   - **Publication**: Detailed subsections with notes

3. Include:
   - Hierarchical structure (H1, H2, H3)
   - Key points under each section (bullets)
   - Notes on examples, data, citations needed (if publication-level)

**Output Format**:
```markdown
[Stage 2: Rough Outline]

**Completeness**: 35%

# {Title}

## 1.0 {Section 1}
- {Key point}
- {Key point}
- NOTE: {Add example here}

### 1.1 {Subsection}
- {Detail}

## 2.0 {Section 2}
...

This is {detail level} suitable for {audience}. Ready to proceed? (#n for next, #r to revise)
```

**Tool Restrictions**: LLM + Markdown + Search (Grep/Glob allowed)
- Can search existing files for reference
- If Edit attempted → Warn: "We're still outlining. Edits come in Stage 3+."

---

## Stage 3: Shaping

**Goal**: Write prose draft without citations (60-70% complete)

**Instructions**:
1. Convert outline to flowing prose adapted to context:
   - **Novice audience**: Define terms, explain concepts, use analogies
   - **Expert audience**: Assume knowledge, focus on insights
   - **Conversational style**: Personal tone, examples, contractions OK
   - **Academic style**: Formal tone, structured arguments

2. Write in full paragraphs and sentences
3. Leave citation placeholders: `[citation needed]` or `[1]` without URLs yet
4. Include code examples, diagrams descriptions if relevant

**Output Format**:
```markdown
[Stage 3: Prose Draft]

**Completeness**: 65%

{Full prose content in {style} style}

Draft complete. Citations to be added in Stage 4. Ready? (#n for next, #r to revise)
```

**Tool Restrictions**: LLM + Markdown + Search + Edit (allowed)
- Can edit files, search for info
- If Bash/WebFetch attempted → Warn: "Research and external calls available in Stage 4."

---

## Stage 4: Detailing

**Goal**: Add citations and polish (85-95% complete)

**Instructions**:
1. Add citations based on context:
   - **Minimal**: Key claims only
   - **Standard**: Major assertions
   - **Comprehensive**: Every fact, multiple sources

2. Use WebFetch or existing knowledge to find sources
3. Format citations: `[1]`, `[2]`, etc. with references section
4. Polish language, fix grammar, improve flow
5. Add missing examples or data

**Output Format**:
```markdown
[Stage 4: Detailed Draft]

**Completeness**: 90%

{Full content with citations}

## References

[1] {Source name} - {URL}
[2] {Source name} - {URL}

Nearly done. Final polish in Stage 5. (#n for final, #r to revise)
```

**Tool Restrictions**: All tools allowed (LLM + Markdown + Search + Edit + Bash + WebFetch)

---

## Stage 5: Finishing

**Goal**: Publication-ready final version (100%)

**Instructions**:
1. Final polish based on context:
   - **Quick draft**: Basic cleanup, good enough
   - **Professional**: Clean, consistent, well-formatted
   - **Publication**: Perfect grammar, style guide compliance, visual appeal

2. Check:
   - Formatting consistent
   - Links work
   - Code examples tested
   - No TODOs or placeholders
   - Meets success criteria from Stage 0.5

3. Generate final output

**Output Format**:
```markdown
[Stage 5: Final Output]

**Completeness**: 100% ✅

{Publication-ready content}

✅ All success criteria met:
- {criterion 1} ✓
- {criterion 2} ✓
- {criterion 3} ✓

Your content is ready!

Conversation ID: {conv-id} (use this to resume later)
```

**Tool Restrictions**: All tools allowed

---

## Revision Flow (#r command)

When user types `#r`:

1. **Prompt for rating**: "Rate current stage output (1-5 stars):"
2. **Prompt for feedback**: "What needs improvement?"
3. **Regenerate**: Create revised version incorporating feedback
4. **Present**: Show updated output, ask if better
5. **Iterate**: Can revise multiple times

**Example**:
```markdown
You chose to revise Stage 3.

Rate this draft (1-5 stars): _
What needs improvement? _

[After user responds]

[Stage 3: Revised Draft]

Changes made:
- {change 1}
- {change 2}

{Updated content}

Better? (#y to keep, #r to revise again, #p to go back, #n to continue)
```

---

## Quality Gates

Before advancing each stage, check:

**Stage 0 → 0.5**: Concept clear and scoped?
**Stage 0.5 → 0.75**: Objectives measurable?
**Stage 0.75 → 1**: Context confirmed by user?
**Stage 1 → 2**: Path selected?
**Stage 2 → 3**: Outline complete and logical?
**Stage 3 → 4**: Prose readable and structured?
**Stage 4 → 5**: Citations complete, content polished?
**Stage 5 → Done**: Success criteria met?

If gate fails, prompt user to revise current stage before advancing.

---

## Metadata Tracking

Track in conversation (invisible to user, for internal state):

```json
{
  "conversation_id": "conv-2025-11-08-a3f8",
  "artifact_id": "uuid",
  "title": "string",
  "current_stage": "Stage 3",
  "completeness_percent": 70,
  "success_criteria": ["criterion1", "criterion2"],
  "created_timestamp": "2025-11-08T10:00:00Z",
  "last_updated": "2025-11-08T10:30:00Z",
  "context": {
    "audience": {
      "expertise_level": 300,
      "role": "technical",
      "familiarity": "domain_expert",
      "confidence": 0.85
    },
    "rigor": {
      "formality": "professional",
      "citation_depth": "standard",
      "detail_level": "detailed",
      "polish": "polished",
      "confidence": 0.80
    },
    "artifact": {
      "type": "technical_documentation",
      "delivery_format": "markdown",
      "length": "medium",
      "structure": "reference",
      "style": "professional_technical"
    }
  },
  "stage_history": [
    {"stage": "Stage 0", "timestamp": "2025-11-08T10:00:00Z"},
    {"stage": "Stage 1", "timestamp": "2025-11-08T10:10:00Z"}
  ]
}
```

Update on every stage transition and revision.

---

## Error Handling

**Invalid command**: "Unknown command '{cmd}'. Valid: #n, #p, #r, #s, #m, #id"

**Already at first stage** (#p at Stage 0): "Already at first stage. Use #n to advance."

**Already at last stage** (#n at Stage 5): "Already at final stage. Content is complete!"

**Tool restriction violated**: "⚠️ {Tool} not recommended at Stage {X}. Best practices: {explanation}. Proceed anyway? (#y yes, #n no)"

---

## More Options Menu (#m)

When user types `#m`:

```markdown
[More Options]

**Navigation**:
- #n → Next stage
- #p → Previous stage
- #r → Revise current stage

**Actions**:
- #s → Skip to final output
- #id → Show conversation ID
- #save → Save current draft to file
- #status → Show progress summary

**Help**:
- #stages → Show all stages overview
- #help → Show this menu

Choose an option or continue with workflow.
```

---

## Implementation Notes

- **State management**: Track current stage in conversation memory (session-scoped)
- **Context carries forward**: Once inferred in Stage 0.75, context influences all subsequent stages
- **Stateful but session-limited**: State persists within conversation but resets on new session (resumption is future enhancement)
- **Progressive disclosure**: Users learn commands as they go; don't overwhelm with all options upfront
- **Flexible navigation**: Users can jump back, revise any stage, or skip ahead as needed

---

## Example Session Flow

```
User: /progressive-content
Assistant: [Stage 0 prompt]

User: "I want to write a technical guide for building REST APIs with FastAPI"
Assistant: [Stage 0 confirmation + conversation ID]

User: #n
Assistant: [Stage 0.5 - objectives prompt]

User: "Reader can build and deploy a FastAPI app in under 1 hour..."
Assistant: [Stage 0.5 confirmation]

User: #n
Assistant: [Stage 0.75 - context inference]
          Inferred: Expert (300), Technical, Professional, Medium length
          Correct?

User: #y
Assistant: [Stage 1 - 4 paths adapted for expert technical audience]

User: B
Assistant: [Stage 2 - detailed outline for Path B]

User: #n
Assistant: [Stage 3 - prose draft in professional technical style]

User: #r
Assistant: [Revision prompt]

User: 4 stars, add more code examples
Assistant: [Stage 3 revised with more examples]

User: #n
Assistant: [Stage 4 - adding citations via WebFetch]

User: #n
Assistant: [Stage 5 - final polished output]
```

---

End of Progressive Content specification.
