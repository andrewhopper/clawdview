# Narrative Creation SOP

Standard operating procedure for creating future narratives that transform abstract concepts into concrete human stories.

## Overview

Future narratives make abstract ideas tangible by showing them through named protagonists in specific moments. This SOP guides the creation process from concept to publication.

**Skill Reference:** `hmode/skills/narratize.md`
**Domain Model:** `hmode/hmode/shared/semantic/domains/future-narrative/`
**Examples:** 9 narratives at `hmode/hmode/shared/semantic/domains/future-narrative/examples/`

---

## 1. Concept Extraction

### 1.1 Input Types

| Input | Example | Action |
|-------|---------|--------|
| Abstract concept | "AI-to-AI coordination" | Identify transformation type |
| Technology description | "Systems that talk to each other" | Find human impact angle |
| Problem statement | "People waste time on hold" | Show friction → resolution |
| Feature idea | "Proactive pitch deck generation" | Identify protagonist and context |

### 1.2 Transformation Type Selection

**Choose the core transformation:**

| Type | Question to Answer |
|------|-------------------|
| `operator_to_approver` | What did humans DO that they now JUDGE? |
| `interface_evolution` | How does the interface adapt TO the user? |
| `ai_to_ai_coordination` | What systems talk that required human middleware? |
| `personalization` | What becomes one-size-fits-one? |
| `cognitive_offload` | What mental load disappears? |
| `time_compression` | What takes weeks that now takes hours? |
| `proactive_ai` | What does AI do before being asked? |

---

## 2. Outline Creation

### 2.1 Protagonist Gate (REQUIRED)

**NEVER use generic references. ALWAYS create a named protagonist.**

```markdown
BAD:  "A user", "someone", "people", "they"
GOOD: "Ben, 5 years old", "Sarah, working mother in Austin", "Marcus, nuclear safety engineer"
```

**Protagonist Checklist:**
- [ ] Name
- [ ] Age (or approximate)
- [ ] Location
- [ ] Occupation or role
- [ ] One defining characteristic or constraint

### 2.2 Use the Outline Template

**Location:** `hmode/hmode/shared/semantic/domains/future-narrative/NARRATIVE_OUTLINE_TEMPLATE.md`

Fill out before writing:

```markdown
## 1. THE CONCEPT
Abstract idea: [e.g., "AI-to-AI scheduling coordination"]
Transformation type: [e.g., ai_to_ai_coordination]
The Shift (thesis): [e.g., "Humans set preferences. Systems handle logistics."]

## 2. THE PROTAGONIST
Name: [e.g., Sarah]
Demographics: [e.g., 34, working mother, Austin TX]
Occupation: [e.g., Marketing manager]
Key constraint: [e.g., Mornings sacred for deep work, kid pickup at 5 PM]
Current friction: [e.g., Wastes 20 min/week on hold scheduling appointments]

## 3. THE SETTING
Year: [e.g., 2030]
Location: [e.g., Austin, Texas]
Context: [e.g., Morning routine, unloading dishwasher]

## 4. THE MECHANISM
First principle: [e.g., AI knows her preferences and rhythms]
How shown: [e.g., AI claims cancellation slot within her 1-3 PM window]

## 5. THE PATTERN
Pattern: [e.g., AI-to-AI Coordination]
Key beats: [e.g., Mention need → AI negotiates → Cancellation broadcast → Instant claim]

## 6. THE SCENE
Timestamp: [e.g., "7:42 AM, making breakfast"]
Sensory detail: [e.g., phone buzzes, notification appears]
Dialogue: [e.g., daughter asks about haircut, Sarah smiles knowing AI is listening]

## 7. THE IMPLICATIONS
For protagonist: [e.g., Time back, no mental load]
For broader group: [e.g., Doctor's office fills cancelled slots instantly]
For society: [e.g., Humans stop being middleware between systems]
```

---

## 3. Writing the Narrative

### 3.1 Length Gate

**Target: 75-300 words (30 seconds to 2 minutes reading time)**

| Length | Use Case |
|--------|----------|
| 75-150 words | Single transformation, simple mechanism |
| 150-250 words | Standard narrative with scene and implications |
| 250-300 words | Dual protagonist or progressive interaction pattern |

### 3.2 Seven Elements Checklist

Write the narrative ensuring all seven elements appear:

1. **THE HOOK** - Opens with problem/friction
2. **THE SOLUTION** - Technology introduced naturally
3. **THE MECHANISM** - First principles through action
4. **THE MOMENT** - Concrete scene with dialogue
5. **THE WITNESS** - Someone observing (optional but powerful)
6. **THE IMPLICATIONS** - Three-part: protagonist, group, society
7. **THE SHIFT** - One-sentence thesis at end

### 3.3 Quality Gate

Before proceeding, verify:

- [ ] Named protagonist (not "a user")
- [ ] Specific year and location
- [ ] Hook shows friction BEFORE solution
- [ ] Mechanism shown through ACTION, not explanation
- [ ] At least one line of DIALOGUE
- [ ] Sensory detail present (see, hear, feel)
- [ ] Within 75-300 words
- [ ] "The Shift" is one clear sentence
- [ ] Implications include a tension/tradeoff

---

## 4. Review and Refinement

### 4.1 Anti-Pattern Checklist

| Don't | Do Instead |
|-------|------------|
| "The AI uses machine learning to..." | Show the AI doing something specific |
| "Users can now..." | Show Sarah doing something specific |
| Long exposition paragraphs | Short sentences, present tense action |
| Technical jargon | Sensory, human language |
| Multiple concepts in one story | One transformation per narrative |
| Utopian ending with no tradeoff | Acknowledge one tension in implications |

### 4.2 Revision Patterns

**If story feels flat:** Add more sensory detail to THE MOMENT
**If story feels preachy:** Cut THE IMPLICATIONS section, let action speak
**If story feels confusing:** Simplify THE MECHANISM, show one thing clearly
**If story feels rushed:** Expand the before state in THE HOOK

---

## 5. Audio Generation (Optional)

### 5.1 Pre-Audio Checklist

- [ ] Story finalized and approved
- [ ] No markdown formatting that sounds awkward read aloud
- [ ] Dialogue clearly attributed
- [ ] No URLs or technical notation

### 5.2 ElevenLabs Settings

| Setting | Value | Reason |
|---------|-------|--------|
| Voice | Adam (pNInz6obpgDQGcFmaJgB) | Neutral narrator |
| Model | eleven_multilingual_v2 | Best quality |
| Stability | 0.5 | Balanced |
| Similarity | 0.75 | Natural variation |
| Style | 0.4 | Slight expressiveness |

### 5.3 Text Cleaning

Remove before sending to TTS:
- `# ` and `## ` headers
- `**bold**` and `*italic*` markers
- `---` horizontal rules
- `- ` bullet points
- Code blocks

---

## 6. Publishing (Optional)

### 6.1 S3 Upload

**Audio location:** `future-narratives/audio/{filename}.mp3`
**HTML location:** `future-narratives/sites/{site-name}/index.html`

### 6.2 Microsite Generation

For collections of narratives, generate an HTML microsite:

**Template:** `projects/personal/active/motifs-microsite/index.html`

**Required elements:**
- Title and subtitle
- Story cards with title, meta, excerpt
- Audio player for each story
- Transformation type tags
- "The Shift" callout

### 6.3 Amplify Deployment

For custom domains:

```bash
python3 shared/scripts/amplify_deploy.py deploy ./site-folder \
  --framework static \
  --app-name site-name \
  --yes
```

---

## 7. Workflow Summary

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. EXTRACT CONCEPT                                               │
│    └─ Identify abstract idea and transformation type             │
├──────────────────────────────────────────────────────────────────┤
│ 2. CREATE OUTLINE                                                │
│    ├─ Name protagonist (REQUIRED GATE)                           │
│    └─ Fill NARRATIVE_OUTLINE_TEMPLATE.md                         │
├──────────────────────────────────────────────────────────────────┤
│ 3. WRITE NARRATIVE                                               │
│    ├─ Include all 7 elements                                     │
│    └─ Stay within 75-300 words                                   │
├──────────────────────────────────────────────────────────────────┤
│ 4. QUALITY GATE                                                  │
│    └─ Verify checklist before proceeding                         │
├──────────────────────────────────────────────────────────────────┤
│ 5. GENERATE AUDIO (optional)                                     │
│    ├─ Clean markdown                                             │
│    └─ Call ElevenLabs API                                        │
├──────────────────────────────────────────────────────────────────┤
│ 6. PUBLISH (optional)                                            │
│    ├─ Upload to S3                                               │
│    └─ Generate microsite if collection                           │
└──────────────────────────────────────────────────────────────────┘
```

---

## 8. Examples Reference

| Story | Transformation | Pattern | Read |
|-------|----------------|---------|------|
| Ben's Learning Game | personalization | Before/After | 2 min |
| Sarah's Last Hold Music | ai_to_ai_coordination | AI-to-AI | 2 min |
| Marcus Approves | operator_to_approver | Before/After | 1 min |
| The Pitch That Wrote Itself | proactive_ai | Progressive | 3 min |
| The Notification That Set Her Free | interface_evolution | Before/After | 1 min |
| The Interface That Knows You | interface_evolution | Dual Protagonist | 2 min |
| The System That Sees Your Work | cognitive_offload | Before/After | 3 min |
| The Idea That Built Itself | time_compression | Async Validation | 3 min |
| Five Clicks From Code | accessibility | Before/After | 2 min |

**Full examples:** `hmode/hmode/shared/semantic/domains/future-narrative/examples/`

---

## 9. Related Resources

| Resource | Location |
|----------|----------|
| Skill (automation) | `hmode/skills/narratize.md` |
| Command (trigger) | `hmode/commands/narratize.md` |
| Domain model | `hmode/hmode/shared/semantic/domains/future-narrative/` |
| Outline template | `NARRATIVE_OUTLINE_TEMPLATE.md` |
| Example microsite | `projects/personal/active/motifs-microsite/` |
| Live site | https://motifs.b.lfg.new |
