---
version: 2.0.0
last_updated: 2025-11-21
description: Brainstorm creative names for projects, blogs, papers, and presentations
---

# Name Brainstorm

Generate creative name ideas for projects, blogs, papers, and presentations through rapid ideation and exploration of multiple naming styles. Includes genetic generation mode for evolutionary name refinement.

## Usage

```bash
# Basic usage - shows all names at once
/name-brainstorm "topic or concept"

# GENETIC MODE - Interactive evolutionary refinement (10 names per generation)
/name-brainstorm "AI safety research" --genetic
/name-brainstorm "developer tools" --genetic --type=project
/name-brainstorm "tech blog" --genetic --tone=playful

# Standard mode options
/name-brainstorm "AI safety research" --type=paper
/name-brainstorm "developer productivity tools" --type=project
/name-brainstorm "startup journey stories" --type=blog
/name-brainstorm "cloud architecture patterns" --type=presentation

# Control number of ideas (standard mode only)
/name-brainstorm "serverless applications" --count=20

# Specify tone/style
/name-brainstorm "data visualization" --tone=professional
/name-brainstorm "tech humor" --tone=playful

# Combine options
/name-brainstorm "machine learning tutorial series" --type=blog --tone=friendly --count=15
```

## Parameters

**Required:**
- `<topic>` - The subject/concept to name (first argument)

**Optional:**
- `--genetic` - Enable genetic generation mode (interactive, 10 per generation)
- `--type=<type>` - Content type: `project`, `blog`, `paper`, `presentation` (default: auto-detect or ask)
- `--count=<n>` - Number of name ideas (standard mode only): 10-30 (default: 15)
- `--tone=<tone>` - Naming tone: `professional`, `playful`, `technical`, `creative`, `academic`, `friendly` (default: matches type)
- `--style=<styles>` - Comma-separated naming styles to explore (see Naming Styles below)

## Naming Styles

The command explores these naming strategies:

1. **Descriptive** - Clear, literal names (e.g., "Cloud Migration Guide")
2. **Metaphorical** - Creative metaphors (e.g., "Navigating the Cloud")
3. **Portmanteau** - Blended words (e.g., "DevOpsify", "Cloudify")
4. **Alliterative** - Repeating sounds (e.g., "Practical Python Patterns")
5. **Acronym** - Letter-based (e.g., "SMART", "RAPID")
6. **Abstract** - Single evocative word (e.g., "Catalyst", "Nexus")
7. **Question** - Inquiry format (e.g., "Why Cloud?", "What's Next?")
8. **Numbered** - Quantified titles (e.g., "7 Patterns for...", "The 3 Laws of...")
9. **Action-Oriented** - Verb-led (e.g., "Building Scalable Systems")
10. **Playful** - Puns and wordplay (e.g., "Git Happens", "Function Junction")

Use `--style=metaphorical,abstract` to focus on specific styles only.

## Genetic Generation Mode

When `--genetic` flag is enabled, the command uses evolutionary algorithms to refine names through interactive selection.

### How Genetic Mode Works

**Generation 0 (Initial Population):**
1. Generate 10 highly diverse names across different styles
2. Maximize variety in length, tone, structure, and approach
3. Present numbered list with brief descriptions
4. User selects 2-3 favorites OR picks a winner

**Generation N (Evolution):**
1. **Mutations** - Modify selected names:
   - Character swaps (TaskFlow → TaskFlux)
   - Word replacements (Task → Work)
   - Prefix/suffix additions (Flow → FlowHub)
   - Style shifts (literal → metaphorical)
2. **Crossover** - Blend selected names:
   - Combine parts (TaskFlow + WorkHub → TaskHub)
   - Merge concepts (Cloud + Nexus → CloudNexus)
3. **Random variants** - Inject 2-3 completely new ideas for diversity
4. Present new generation of 10 names
5. Repeat until user selects winner

### Genetic Mode Output Format

```markdown
## Generation {N}: "{topic}"
**Type:** {type} | **Tone:** {tone}

1. **NameOne** - Descriptive note (Parent: seed)
2. **NameTwo** - Brief description (Mutation of #1)
3. **NameThree** - What makes it interesting (Crossover: #1 + #2)
4. **NameFour** - Key characteristic (New variant)
5. **NameFive** - Why it works (Mutation of #3)
6. **NameSix** - Unique angle (Parent: seed)
7. **NameSeven** - Brief note (Crossover: #4 + #5)
8. **NameEight** - What it conveys (Mutation of #6)
9. **NameNine** - Style description (New variant)
10. **NameTen** - Key benefit (Mutation of #2)

**Your choice:**
- Select favorites: Enter numbers (e.g., "1, 3, 7")
- Pick winner: Enter "winner: 5"
- More diversity: Enter "diverge"
- Start over: Enter "reset"
```

### User Input Options

**Select favorites (evolve further):**
```
1, 3, 7
```
Next generation bred from these three names.

**Pick winner (done):**
```
winner: 5
```
Ends session, shows final recommendation.

**Request more diversity:**
```
diverge
```
Reduces selection pressure, adds more random variants.

**Start over:**
```
reset
```
Generate completely new initial population.

### Genetic Operators

**Mutation Types:**
1. **Character-level:**
   - Swap letters: FlowTask → FluxTask
   - Add/remove chars: Task → Taski, Tasks
   - Change case: TaskFlow → taskflow, TASKFLOW

2. **Word-level:**
   - Synonym swap: Task → Work, Job, Quest
   - Related terms: Flow → Stream, Current, Flux
   - Domain terms: Cloud → Sky, Nimbus, Ether

3. **Structure-level:**
   - Reverse words: TaskFlow → FlowTask
   - Add prefix: Flow → ProFlow, ReFlow
   - Add suffix: Task → Taskly, Taskify
   - Remove words: Task Management Tool → TaskTool

4. **Style-level:**
   - Shift tone: Professional → Playful
   - Change style: Descriptive → Metaphorical
   - Adjust length: Expand or compress

**Crossover Types:**
1. **Simple blend:**
   - TaskFlow + WorkHub → TaskHub, WorkFlow
   - Cloud + Nexus → CloudNexus, NexusCloud

2. **Concept merge:**
   - Extract concepts from both parents
   - Combine in new way
   - Example: "Quick Deploy" + "Easy Launch" → "QuickLaunch"

3. **Structural mix:**
   - Take structure from one, words from another
   - Example: [Verb][Noun] from A + vocabulary from B

**Diversity Injection:**
- Every generation includes 2-3 completely random names
- Prevents premature convergence
- Explores new areas of solution space
- Higher diversity when user requests "diverge"

### Genetic Mode Philosophy

**Goal:** Interactive refinement toward perfect name through natural selection.

**Strategy:**
- Generation 0: Maximize diversity
- Generations 1-N: Balance exploitation (refine good names) with exploration (try new ideas)
- User = fitness function (selected names = high fitness)
- Converge toward names user loves

**Stopping criteria:**
- User selects winner
- OR 5+ generations without new favorites
- OR user explicitly ends session

## Instructions

You are a creative naming assistant specializing in rapid brainstorming. Generate diverse, memorable names across multiple styles.

### Mode Detection

**First step:** Check for `--genetic` flag
- If present: Use Genetic Mode Workflow (below)
- If absent: Use Standard Mode Workflow (below)

### Genetic Mode Workflow

#### Phase 1: Initial Context

1. **Parse parameters**: topic, type, tone, styles
2. **Set defaults**: tone matches type, all styles enabled
3. **Analyze topic**: key concepts, themes, domain

#### Phase 2: Generation 0 (Initial Population)

1. **Maximize diversity** across all dimensions:
   - Length: 5-20 characters (mix short, medium, long)
   - Style: All 10 naming styles represented
   - Structure: Single words, compounds, phrases
   - Tone: Variations on requested tone
   - Origin: Different conceptual starting points

2. **Generate 10 names** with clear numbering:
   ```markdown
   ## Generation 0: "{topic}"
   **Type:** {type} | **Tone:** {tone}

   1. **ShortName** - Abstract, single word (5 chars)
   2. **DescriptiveCompound** - Two words combined (19 chars)
   3. **The Long Phrase Name** - Full phrase (18 chars)
   4. **Portman** - Blended word (7 chars)
   5. **Question Format?** - Interrogative (15 chars)
   6. **ActionVerb** - Imperative form (10 chars)
   7. **MetaphorName** - Evocative imagery (12 chars)
   8. **PlayfulPun** - Wordplay (10 chars)
   9. **ACRONYM** - Letter-based (7 chars)
   10. **Number7Pattern** - Quantified (14 chars)
   ```

3. **Add brief descriptions** - One line per name explaining concept

4. **Present user options**:
   ```markdown
   **Your choice:**
   - Select favorites: Enter numbers (e.g., "1, 3, 7")
   - Pick winner: Enter "winner: 5"
   - More diversity: Enter "diverge"
   - Start over: Enter "reset"
   ```

5. **Wait for user input** - This is an interactive command in genetic mode

#### Phase 3: Evolution (Generations 1-N)

1. **Parse user selection**:
   - If "winner: N": Jump to Phase 4 (Finalization)
   - If "reset": Return to Phase 2 (new Gen 0)
   - If "diverge": Increase random variant ratio to 50%
   - If numbers: Use as parent selection

2. **Breed new generation**:
   - **From selected parents (40%)**: 4 names via mutation
   - **From crossover (30%)**: 3 names blending parents
   - **Random variants (30%)**: 3 completely new names
   - If "diverge" mode: 5 mutated, 5 random

3. **Apply genetic operators**:
   - **Mutations**: Character, word, structure, style-level changes
   - **Crossover**: Blend concepts, merge parts, structural mix
   - **Random**: New styles, new concepts, new approaches

4. **Generate 10 names** with ancestry tracking:
   ```markdown
   ## Generation {N}: "{topic}"
   **Type:** {type} | **Tone:** {tone} | **Parents:** Names from Gen {N-1}

   1. **NewName** - Description (Mutation of Gen{N-1} #3)
   2. **Another** - Description (Crossover: #{1} + #{5})
   3. **Different** - Description (New variant)
   4. **Modified** - Description (Mutation of Gen{N-1} #1)
   ...
   ```

5. **Present options and wait for input** - Repeat Phase 3 until winner selected

#### Phase 4: Finalization

When user selects winner:

1. **Confirm selection**:
   ```markdown
   ## 🎯 Final Selection: **{WinningName}**

   **Origin:** Generation {N}, evolved from: [ancestry chain]
   **Style:** {style type}
   **Why it works:**
   - [Reason 1]
   - [Reason 2]
   - [Reason 3]
   ```

2. **Show evolutionary lineage**:
   ```markdown
   **Evolution path:**
   Gen 0: "{seed name}" (initial)
    ↓ (mutation: word swap)
   Gen 1: "{mutated name}" (selected)
    ↓ (crossover with "{other name}")
   Gen 2: "{winner}" ← Final choice
   ```

3. **Provide usage examples**:
   - Package name, CLI command, import statement
   - Domain suggestions
   - Tagline ideas

4. **Next steps**:
   - Domain/package availability checks
   - Memorability testing suggestions
   - Link to `/name-project` for collision analysis

### Standard Mode Workflow

#### Phase 1: Context Analysis

1. **Parse parameters**:
   - Extract topic, type, count, tone, styles
   - If type not specified: detect from topic or present menu:
     ```
     What type of name?
     [1] Project (software/tool)
     [2] Blog (publication/series)
     [3] Paper (research/article)
     [4] Presentation (talk/deck)
     [5] Auto-detect
     ```

2. **Set defaults**:
   - Count: 15 (range 10-30)
   - Tone: Match type (professional for paper, friendly for blog, etc.)
   - Styles: All 10 styles unless specified

3. **Analyze topic**:
   - Key concepts and themes
   - Target audience
   - Domain/industry context
   - Emotional tone

#### Phase 2: Name Generation

Generate `count` name ideas distributed across selected styles:

**Distribution strategy:**
- For 15 names: ~2 per style (rotate through 10 styles)
- For 20 names: ~2 per style
- For 30 names: ~3 per style

**Quality guidelines:**
- **Projects**: 5-20 characters, memorable, brandable
- **Blogs**: 2-6 words, catchy, searchable
- **Papers**: 5-12 words, descriptive, academic
- **Presentations**: 2-8 words, attention-grabbing

**Output format:**
```markdown
## Name Brainstorm: "{topic}"
**Type:** {type} | **Tone:** {tone} | **Generated:** {count} ideas

### Descriptive (Clear & Literal)
1. [Name] - [Brief note on why/when to use]
2. [Name] - [Brief note]

### Metaphorical (Creative Imagery)
3. [Name] - [Brief note]
4. [Name] - [Brief note]

### Portmanteau (Blended Words)
5. [Name] - [Brief note]
6. [Name] - [Brief note]

[Continue through selected styles...]

### Quick Picks
**Most Professional:** [Name]
**Most Creative:** [Name]
**Most Memorable:** [Name]
**Most Descriptive:** [Name]
**Best for SEO:** [Name] (for blogs/presentations)
**Best for Branding:** [Name] (for projects/blogs)
```

#### Phase 3: Curated Suggestions

After presenting all ideas, provide curated recommendations:

```markdown
## Recommendations by Use Case

### If you want something safe and clear:
- [Name 1]
- [Name 2]
- [Name 3]

### If you want to stand out:
- [Name 1]
- [Name 2]
- [Name 3]

### If you want technical credibility:
- [Name 1]
- [Name 2]
- [Name 3]

## Next Steps
1. **Check availability** (for projects/blogs):
   - Domain: [suggested searches]
   - GitHub/npm/PyPI: [suggested checks]
   - Google search: "[name] [topic]"

2. **Test memorability**:
   - Say it out loud 3 times
   - Share with colleague - can they spell it?
   - Wait 5 minutes and see if you remember it

3. **Refine**: Want more ideas? Try:
   - `/name-brainstorm "[topic]" --style=metaphorical --count=20`
   - `/name-project "[chosen name]"` (for detailed collision check)
```

### Type-Specific Guidance

#### Projects
- Favor: Short (5-12 chars), pronounceable, no hyphens
- Styles: Abstract, Portmanteau, Descriptive, Metaphorical
- Examples: "Nexus", "FlowDev", "CodeSync", "Harbor"
- Check: GitHub, npm, PyPI, domain availability

#### Blogs
- Favor: Memorable phrases, 2-4 words, SEO-friendly
- Styles: Metaphorical, Question, Alliterative, Action-Oriented
- Examples: "The Daily Deploy", "Why It Matters", "Code & Coffee"
- Check: Domain, social handles, Google search

#### Papers
- Favor: Descriptive, academic, 6-10 words
- Styles: Descriptive, Numbered, Question, Action-Oriented
- Examples: "A Survey of...", "Toward Scalable...", "Understanding the Impact of..."
- Check: Google Scholar, arXiv for similar titles

#### Presentations
- Favor: Punchy, 2-6 words, intrigue/value proposition
- Styles: Question, Numbered, Metaphorical, Action-Oriented
- Examples: "The Future of Cloud", "7 Secrets to...", "Scaling Beyond Limits"
- Check: Conference archives, SlideShare

### Tone Calibration

**Professional:**
- Avoid: Puns, slang, overly casual language
- Favor: Clear value proposition, industry terms
- Examples: "Enterprise Cloud Patterns", "Strategic API Design"

**Playful:**
- Embrace: Puns, wordplay, humor
- Favor: Memorable over precise
- Examples: "Git Gud", "Deploy & Pray", "Ctrl+Alt+Elite"

**Technical:**
- Use: Precise terminology, acronyms, jargon
- Favor: Accuracy and specificity
- Examples: "Kubernetes Operators Explained", "WASM Runtime Optimization"

**Creative:**
- Explore: Metaphors, imagery, unexpected connections
- Favor: Evocative over literal
- Examples: "Digital Alchemy", "The Architecture of Dreams"

**Academic:**
- Follow: Paper title conventions (article + colon + description)
- Favor: Clarity and searchability
- Examples: "Deep Learning for NLP: A Survey", "Toward Efficient Graph Processing"

**Friendly:**
- Use: Conversational language, approachability
- Favor: Warm, inviting tone
- Examples: "Your Guide to React Hooks", "Let's Talk About Testing"

## Implementation Notes

### Genetic Mode
1. **Interactive session** - Wait for user input after each generation
2. **Track ancestry** - Record parent names and genetic operations
3. **Use TodoWrite** - Track generations (Gen 0 → Gen N → Finalization)
4. **Numbered lists** - Always 1-10 with bold names and brief descriptions
5. **Apply genetic operators** - Mutations, crossover, random variants per ratios
6. **No web searches** - Pure creative evolution, no collision checking

### Standard Mode
1. **No web searches** - Rapid ideation, not collision checking
2. **Use TodoWrite** - Track phases (context → generation → recommendations)
3. **Parallel thinking** - Generate names across styles simultaneously
4. **Brevity** - Keep notes concise (5-10 words per name)
5. **Interactive menu** - If type not specified, present selection menu
6. **No mid-execution questions** - All parameters upfront or menu at start

## Examples

### Example 1: Genetic Mode (Interactive)

```bash
/name-brainstorm "distributed task queue" --genetic --type=project
```

**Output (Generation 0):**
```markdown
## Generation 0: "distributed task queue"
**Type:** project | **Tone:** professional

1. **Flux** - Abstract metaphor, flow of tasks (4 chars)
2. **TaskDistributor** - Descriptive compound, self-explanatory (15 chars)
3. **Queue & Conquer** - Playful phrase with pun (14 chars)
4. **Qwerk** - Portmanteau: Queue + Work (5 chars)
5. **Orchestrate** - Action-oriented, conducting tasks (11 chars)
6. **DTQ** - Acronym, technical abbreviation (3 chars)
7. **Nexus** - Abstract, connection point metaphor (5 chars)
8. **WorkFlow Hub** - Descriptive phrase (12 chars)
9. **How Does It Queue?** - Question format (17 chars)
10. **TaskStream** - Metaphorical compound, flowing tasks (10 chars)

**Your choice:**
- Select favorites: Enter numbers (e.g., "1, 3, 7")
- Pick winner: Enter "winner: 5"
- More diversity: Enter "diverge"
- Start over: Enter "reset"
```

**User input:** `1, 7, 10`

**Output (Generation 1):**
```markdown
## Generation 1: "distributed task queue"
**Type:** project | **Tone:** professional | **Parents:** Flux (#1), Nexus (#7), TaskStream (#10)

1. **Fluxus** - Latin-inspired evolution, flow concept (6 chars) (Mutation of #1)
2. **StreamNexus** - Merging flow with connection (11 chars) (Crossover: #10 + #7)
3. **Torrent** - Random: Fast-moving stream metaphor (7 chars) (New variant)
4. **TaskNexus** - Task-focused connection point (9 chars) (Crossover: #10 + #7)
5. **Influx** - Inward flow, receiving tasks (6 chars) (Mutation of #1)
6. **NexusFlow** - Reversed crossover combination (9 chars) (Crossover: #7 + #10)
7. **Current** - Random: Electrical/water flow metaphor (7 chars) (New variant)
8. **Reflux** - Backward flow, task recycling (6 chars) (Mutation of #1)
9. **StreamHub** - Stream with central point (9 chars) (Mutation of #10)
10. **Catalyst** - Random: Enabling action metaphor (8 chars) (New variant)

**Your choice:**
- Select favorites: Enter numbers (e.g., "2, 4, 6")
- Pick winner: Enter "winner: 4"
- More diversity: Enter "diverge"
- Start over: Enter "reset"
```

**User input:** `winner: 4`

**Output (Final):**
```markdown
## 🎯 Final Selection: **TaskNexus**

**Origin:** Generation 1, evolved from TaskStream (#10) + Nexus (#7)
**Style:** Crossover - Descriptive + Abstract metaphor
**Length:** 9 characters

**Why it works:**
- Clear task-focused naming (immediately understandable)
- "Nexus" conveys connection/distribution concept
- Short, memorable, pronounceable
- Professional tone suitable for infrastructure tool
- Brandable - works as package name, CLI, domain

**Evolution path:**
Gen 0: "TaskStream" (initial - #10, selected)
Gen 0: "Nexus" (initial - #7, selected)
 ↓ (crossover: task focus + connection metaphor)
Gen 1: "TaskNexus" ← Final choice

**Usage examples:**
- **Package name:** `tasknexus`
- **CLI command:** `tasknexus enqueue my-job`
- **Import:** `from tasknexus import Queue`
- **Domain:** tasknexus.io, tasknexus.dev
- **Tagline:** "The nexus of distributed task processing"

**Next steps:**
1. Check availability:
   - Domain: tasknexus.com, tasknexus.io, tasknexus.dev
   - GitHub: github.com/tasknexus
   - npm: npmjs.com/package/tasknexus
   - PyPI: pypi.org/project/tasknexus

2. Test memorability:
   - Say it 3 times out loud
   - Share with colleague - can they spell it?
   - Wait 5 minutes, recall the name

3. Detailed collision check:
   - Run: `/name-project "TaskNexus"`
```

### Example 2: Standard Mode - Project Name Brainstorm

```bash
/name-brainstorm "distributed task queue" --type=project --count=15
```

**Output (condensed):**
```markdown
## Name Brainstorm: "distributed task queue"
**Type:** project | **Tone:** professional | **Generated:** 15 ideas

### Descriptive
1. TaskFlow - Direct reference to task movement
2. QueueHub - Central queue management

### Metaphorical
3. Dispatch - Sending tasks out
4. Conductor - Orchestrating work

### Portmanteau
5. Taskify - Task + simplify
6. Queuely - Queue + friendly suffix

### Abstract
7. Nexus - Connection point
8. Catalyst - Enabling action

### Alliterative
9. Task Tracker
10. Queue Quest

### Action-Oriented
11. Distribute
12. Orchestrate

### Playful
13. WorkHorse - Reliable task processor
14. BusyBee - Always working

### Technical
15. DTaskQ - Distributed Task Queue (abbreviated)

### Quick Picks
**Most Professional:** Orchestrate
**Most Creative:** Conductor
**Most Memorable:** WorkHorse
**Most Descriptive:** TaskFlow
**Best for Branding:** Catalyst
```

### Example 2: Blog Name Brainstorm

```bash
/name-brainstorm "startup founder lessons" --type=blog --tone=friendly --count=12
```

**Output (condensed):**
```markdown
## Name Brainstorm: "startup founder lessons"
**Type:** blog | **Tone:** friendly | **Generated:** 12 ideas

### Metaphorical
1. The Founder's Journey - Personal narrative angle
2. Startup Atlas - Navigation metaphor

### Question
3. So You're Building a Startup? - Direct address
4. What I Learned Building... - Reflective

### Alliterative
5. Founder Fieldnotes - Professional yet approachable
6. Startup Stories & Strategies

### Action-Oriented
7. Building in Public - Transparency focus
8. Learning to Launch

### Playful
9. From Zero to... Something - Humble humor
10. The Hot Mess Chronicles - Self-deprecating

### Friendly
11. Coffee & Cap Tables - Relatable combo
12. Your Startup Companion - Supportive tone

### Quick Picks
**Most Friendly:** Coffee & Cap Tables
**Most Creative:** The Founder's Journey
**Most Memorable:** From Zero to... Something
**Best for SEO:** Startup Founder Lessons (direct match)
```

### Example 3: Paper Title Brainstorm

```bash
/name-brainstorm "transformer attention mechanisms" --type=paper --tone=academic --count=10
```

**Output (condensed):**
```markdown
## Name Brainstorm: "transformer attention mechanisms"
**Type:** paper | **Tone:** academic | **Generated:** 10 ideas

### Descriptive
1. A Comprehensive Survey of Attention Mechanisms in Transformer Models
2. Attention Mechanisms in Modern Transformer Architectures: A Review

### Question
3. How Do Attention Mechanisms Scale in Large Language Models?
4. What Makes Attention Effective? An Empirical Study

### Numbered
5. Three Paradigms of Attention in Transformer Networks
6. Toward Unified Understanding: Five Properties of Attention Layers

### Action-Oriented
7. Analyzing Attention: Insights from Large-Scale Transformer Models
8. Understanding Multi-Head Attention Through Visualization

### Technical
9. Efficient Attention: Reducing Complexity in Transformer-Based Models
10. Cross-Attention Dynamics in Encoder-Decoder Transformers

### Quick Picks
**Most Academic:** A Comprehensive Survey... (standard format)
**Most Engaging:** What Makes Attention Effective?
**Most Specific:** Cross-Attention Dynamics...
**Best for Discovery:** How Do Attention Mechanisms Scale...
```

### Example 4: Presentation Title Brainstorm

```bash
/name-brainstorm "kubernetes cost optimization" --type=presentation --count=15
```

**Output (condensed):**
```markdown
## Name Brainstorm: "kubernetes cost optimization"
**Type:** presentation | **Tone:** professional | **Generated:** 15 ideas

### Numbered
1. 7 Ways to Cut Your Kubernetes Bill in Half
2. The 3 Most Expensive Kubernetes Mistakes

### Question
3. Is Your Kubernetes Cluster Burning Money?
4. What's Really Costing You in K8s?

### Metaphorical
5. Kubernetes on a Budget
6. Taming the Cloud Beast

### Action-Oriented
7. Optimize, Reduce, Repeat
8. Slash Your Kubernetes Costs

### Playful
9. K8s Cost Cutting Without the Tears
10. From Kubernetes Chaos to Cost Control

### Descriptive
11. Kubernetes Cost Optimization Strategies
12. Right-Sizing Your Kubernetes Workloads

### Technical
13. Pod Autoscaling for Cost Efficiency
14. Resource Requests, Limits, and Your Budget

### Creative
15. The Art of Frugal Kubernetes

### Quick Picks
**Most Attention-Grabbing:** Is Your Kubernetes Cluster Burning Money?
**Most Actionable:** 7 Ways to Cut Your Kubernetes Bill in Half
**Most Professional:** Kubernetes Cost Optimization Strategies
**Most Memorable:** From Kubernetes Chaos to Cost Control
```

## Edge Cases

### Missing Topic
If no topic provided:
```markdown
❌ **Error:** Topic required

Usage: /name-brainstorm "your topic" [options]

Example: /name-brainstorm "API design patterns" --type=blog
```

### Invalid Count
If count < 10 or > 30:
```markdown
⚠️ **Warning:** Count adjusted to valid range (10-30)

Generating 15 names (default)...
```

### Unclear Type
If type cannot be auto-detected:
```markdown
What type of name are you looking for?

[1] Project (software/tool/library)
[2] Blog (publication/series/newsletter)
[3] Paper (research/article/whitepaper)
[4] Presentation (talk/deck/workshop)
[5] Other (general brainstorm)

> _
```

## Related Commands

- `/name-project` - Structured project naming with collision checking and refinement
- For detailed project naming with web searches and availability checks, use `/name-project` instead

## Remember

### Genetic Mode (`--genetic`)
**Goal:** Interactive evolutionary refinement toward perfect name through user selection.

**Philosophy:** Natural selection through user preferences. Evolve 10 names per generation, select favorites, breed next generation.

**Key features:**
- 10 names per generation (always)
- User drives evolution (fitness function)
- Mutations, crossover, random variants
- Track ancestry and lineage
- Converge on winner through selection

### Standard Mode (default)
**Goal:** Fast creative exploration of naming possibilities across diverse styles.

**Philosophy:** Quantity breeds quality. Generate many ideas quickly, let the best ones emerge naturally.

**Key features:**
- Show all names at once (10-30)
- Style-based organization
- Curated recommendations
- Quick exploration without interaction

### Both Modes
**Not included:** Collision checking, domain availability (use `/name-project` for that).

---

**Web-Compatible:**
- **Genetic mode:** Requires user interaction after each generation
- **Standard mode:** Accepts all parameters upfront with optional interactive menu for type selection only
