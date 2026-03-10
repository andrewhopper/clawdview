---
uuid: cmd-mdash-8b9c0d1e
version: 2.0.0
last_updated: 2025-11-10
description: Path to the document to de-AI (e.g., ./docs/report.md)
---

# Kill M-Dash: AI Writing Pattern Remover

Remove AI-generated writing patterns from `{file_path}` to make content sound more natural and human.

## AI Writing Patterns to Remove

### 1.0 Content Patterns

**1.1 Undue Emphasis on Symbolism and Importance**
- "stands/serves as" → state directly
- "is a testament/reminder" → remove or be specific
- "plays a vital/significant/crucial role" → "is important" or be specific
- "underscores/highlights its importance/significance" → remove or state directly
- "reflects broader" → remove or be specific
- "symbolizing its ongoing" → remove
- "enduring/lasting impact" → "impact" or be specific
- "key turning point" → "turning point"
- "indelible mark" → remove or be specific
- "deeply rooted" → "rooted"
- "profound heritage" → "heritage"
- "steadfast dedication" → "dedication"

**1.2 Undue Emphasis on Notability and Media Coverage**
- "independent coverage" → show, don't tell
- "local/regional/national/[country] media outlets" → name them without emphasizing
- "has been featured in several outlets" → just cite the sources
- Remove meta-commentary about coverage quality

**1.3 Superficial Analyses**
- "ensuring..." → remove filler
- "highlighting..." → state directly
- "emphasizing..." → state directly
- "reflecting..." → state directly
- "underscoring..." → state directly
- "showcasing..." → state directly
- "aligns with..." → remove or be specific
- "contributing to..." → remove or be specific
- Watch for "-ing" phrases attached to end of sentences that analyze rather than state

**1.4 Promotional and Positively Loaded Language**
- "continues to captivate" → neutral description
- "groundbreaking" → "new" or be specific
- "intricate" → "complex" or be specific
- "stunning natural beauty" → "natural beauty"
- "enduring/lasting legacy" → "legacy"
- "nestled" → "located"
- "in the heart of" → "in" or "near"
- "rich/vibrant/diverse" → be specific or remove
- "artistic/cultural/literary/media landscape" → "scene" or be specific
- "boasts a" → "has"

**1.5 Didactic, Editorializing Disclaimers**
- "it's important/critical/crucial to note/remember/consider" → remove entirely
- "may vary..." → remove unless specifically necessary

**1.6 Section Summaries and Conclusions**
- "In summary," → remove
- "In conclusion," → remove
- "Overall," → remove
- Watch for "Despite its... faces several challenges..." formulas
- Remove speculation about "future prospects" or "future outlook"

**1.7 False Ranges (from X to Y)**
- Only accept ranges with real scales (numerical, temporal, categorical)
- "from problem-solving to creativity" → NOT a real range (list separately)
- "from seed to tree" → VALID (lifecycle scale)
- Avoid meaningless "from X to Y" that's just listing examples

### 2.0 Language and Grammar Patterns

**2.1 Overused AI Vocabulary Words**

HIGH FREQUENCY AI WORDS:
- "align/aligns/aligning with" → "match" or be specific
- "crucial" → "important"
- "delve/delves/delving into" → "explore" or "examine"
- "emphasizing" → state directly
- "enduring" → lasting or remove
- "enhance/enhances/enhancing" → "improve" or be specific
- "fostering" → "encouraging" or "supporting"
- "garnered/garnering" → "received" or "gained"
- "highlight/highlighted/highlighting/highlights" (as verb) → state directly
- "interplay" → "interaction"
- "intricate/intricacies" → "complex" or be specific
- "pivotal" → "important"
- "showcase/showcased/showcases/showcasing" → "show" or "display"
- "tapestry" (as abstract noun) → remove or be specific
- "underscore/underscored/underscores/underscoring" → state directly

MEDIUM FREQUENCY AI WORDS:
- "landscape" (as in "technology landscape") → "ecosystem" or be specific
- "robust" → "reliable", "strong", or specific quality
- "leverage" → "use" or be specific
- "seamlessly" → remove or be specific
- "comprehensive" → "complete" or remove
- "innovative" → be specific about what's new
- "cutting-edge" → "modern" or be specific
- "game-changer" / "game-changing" → be specific about impact
- "revolutionize" / "revolutionary" → "improve" or be specific
- "powerful" → be specific about capability
- "unlock" (as in "unlock potential") → remove or rephrase
- "harness" (as in "harness the power") → "use" or be specific
- "empower" → "enable" or be specific
- "transform" / "transformation" → "change" or be specific
- "holistic" → "complete" or remove
- "paradigm" / "paradigm shift" → remove or be specific
- "synergy" → "collaboration" or be specific
- "optimize" → "improve" or be specific
- "streamline" → "simplify" or be specific
- "elevate" → "improve" or be specific
- "foster" → "encourage" or "support"
- "facilitate" → "enable" or "help"
- "navigate" (as in "navigate complexity") → "handle" or "manage"
- "drive" (as in "drive innovation") → "create" or "lead"
- "dynamic" → be specific
- "scalable" → use only if technical context requires
- "resilient" → "reliable" or be specific

**2.2 Negative Parallelisms**
- "Not only X, but Y" → rewrite more directly
- "It is not just about X, it's Y" → rewrite
- "Not X, not Y, just Z" → rewrite
- Watch for cross-sentence negative parallelisms

**2.3 Rule of Three**
- "adjective, adjective, adjective" → use one or none
- "short phrase, short phrase, and short phrase" → consider simpler structure
- Watch for formulaic triads used to appear comprehensive

**2.4 Vague Attributions (Weasel Words)**
- "Industry reports" → name the report or remove
- "Observers have cited" → name them or remove
- "Some critics argue" → name them or remove
- "Research shows" (without citation) → cite specific research

**2.5 Elegant Variation**
- Watch for synonyms used repetitively to avoid reusing same word
- "protagonist / key player / eponymous character" for same person → just use name or consistent term

### 3.0 Formulaic Structures

**3.1 Introductory Patterns**
- "In today's fast-paced world..." → remove entirely
- "In an era of..." → remove entirely
- "As we move into..." → remove entirely
- "It's worth noting that..." → remove phrase
- "It's important to understand..." → remove phrase
- "One key aspect is..." → remove phrase
- "It goes without saying..." → remove entirely

**3.2 Transition Patterns**
- "Furthermore," → "Also,"
- "Moreover," → "Also," or remove
- "Additionally," → "Also," or remove when obvious
- "In conclusion," → remove or just start concluding
- "To sum up," → remove

**3.3 Emphasis Patterns**
- Multiple adjectives before nouns ("powerful, innovative solution") → use one or none
- Superlatives without data ("best", "most advanced") → remove or add evidence
- Hedging phrases ("it seems that", "it appears") → state directly

### 4.0 Style Issues

**4.1 Punctuation**

**Em dashes (—):**
- ✅ Keep: Occasional use for natural emphasis (1-2 per page)
- ❌ Remove: Excessive formulaic usage (especially in "punched up" sales style)
- ❌ Remove: Using em dash where comma/parentheses/colon would be more natural

**4.2 Passive Voice (where inappropriate)**
- "It can be seen that..." → "We see that..." or state directly
- "It has been observed..." → "Research shows..." or be specific
- "Improvements were made..." → "We improved..." or be specific

**4.3 Vague Quantifiers**
- "numerous" → give number or "many"
- "various" → be specific or "several"
- "significant" → quantify the significance
- "substantial" → quantify

**4.4 Redundant Emphasis**
- "very unique" → "unique"
- "completely transform" → "transform"
- "fully optimize" → "optimize"
- "really powerful" → "powerful" or better: be specific

## Instructions

### Phase 1: Detect AI Patterns

1. **Read the document**: Use Read tool to load `{file_path}`

2. **Scan for AI patterns**:
   - **Content patterns**: Symbolism emphasis, superficial analyses, promotional language
   - **Language patterns**: Overused AI vocabulary, negative parallelisms, rule of three
   - **Formulaic structures**: Cliché introductions, transitions, emphasis patterns
   - **Style issues**: Em dash overuse, passive voice, vague quantifiers, redundant emphasis
   - **Structural patterns**: "In conclusion" sections, "challenges and future" formulas
   - **False ranges**: Meaningless "from X to Y" constructions

3. **Present numbered issues with proposed changes**:

```markdown
# AI Writing Patterns: {file_path}

Found {N} AI patterns:

## Issues

**#1** [HIGH] Line 12: Em dash overuse
- Current: "The platform—built with AI—delivers results—faster than ever"
- Proposed: "The platform delivers results faster than ever"
- Pattern: Formulaic em dash usage

**#2** [MEDIUM] Line 23: AI filler phrase
- Current: "delve into the complexities"
- Proposed: "examine the complexities"
- Pattern: "delve into"

**#3** [HIGH] Line 45: Vague superlative
- Current: "revolutionary solution"
- Proposed: "solution that reduces processing time by 80%"
- Pattern: Unsubstantiated superlative

**#4** [LOW] Line 67: Redundant emphasis
- Current: "very unique approach"
- Proposed: "unique approach"
- Pattern: Redundant modifier

---

## Summary
- 🔴 High priority: 2
- ⚠️ Medium priority: 1
- 💡 Low priority: 1
```

### Phase 2: User Decision

4. **Prompt user with DSL options**:

```
Review proposed changes. Choose action:

• accept all          - Apply all fixes as-is
• reject all          - Skip all fixes
• accept: 1,2,4       - Apply fixes #1, #2, #4
• reject: 3           - Skip fix #3 (apply rest)
• edit: 2,3           - Manually edit fixes #2, #3 before applying
• e: 1                - Shorthand for edit

Combine commands: "accept: 1,4  edit: 2,3"

What would you like to do?
```

5. **Wait for user response** - DO NOT proceed until user provides input

### Phase 3: Handle Edits (if requested)

6. **If user requests edits** (e.g., `edit: 2,3`):
   - Present each issue for manual editing
   - Show current and proposed side-by-side
   - Ask user to provide their custom fix
   - Update the fix list with user's version

Example interaction:
```
📝 Edit mode for issue #2:

Current:  "delve into the complexities"
Proposed: "examine the complexities"

Enter your preferred fix (or press Enter to keep proposed):
> explore these complexities

✅ Updated fix #2
```

7. **After edits complete**, re-prompt for final acceptance

### Phase 4: Apply Fixes

8. **Parse user DSL input**:
   - `accept all` → apply all fixes
   - `reject all` → done
   - `accept: 1,2,4` → apply only #1, #2, #4
   - `reject: 3` → apply all except #3
   - `edit: 2,3` → enter edit mode for #2, #3

9. **Apply accepted fixes**:
   - Use Edit tool to replace current text with fixed text (or user's custom version)
   - Track which issues were fixed
   - Report completion

10. **Show fix summary**:

```markdown
✅ Applied fixes: #1, #2, #4
⏭️  Skipped: #3

File updated: {file_path}
```

### Phase 5: Review Statistics

11. **Calculate de-AI metrics**:

```markdown
# De-AI Statistics

**Before:**
- Em dashes: 12
- AI filler phrases: 8
- Formulaic patterns: 5
- Total AI patterns: 25

**After:**
- Em dashes: 2
- AI filler phrases: 0
- Formulaic patterns: 0
- Total AI patterns: 2

**Improvement:** 92% reduction in AI patterns
```

## Example Flow

**Original document** (example.md):
```
In today's fast-paced world, our revolutionary platform—powered by
cutting-edge AI—seamlessly delivers robust solutions that empower
teams to unlock their full potential. This groundbreaking approach
serves as a testament to innovation, showcasing how technology can
foster collaboration and drive results. Let's delve into how this
game-changing system aligns with modern needs and underscores the
importance of digital transformation.
```

**Step 1: Issues presented**
```
# AI Writing Patterns: example.md

Found 15 AI patterns:

**#1** [HIGH] Line 1: Formulaic intro
- Current: "In today's fast-paced world,"
- Proposed: [Remove]
- Pattern: 3.1 Introductory pattern

**#2** [HIGH] Line 1: Promotional language
- Current: "revolutionary platform"
- Proposed: "platform"
- Pattern: 1.4 Positively loaded language

**#3** [HIGH] Line 1: Promotional language
- Current: "cutting-edge AI"
- Proposed: "AI"
- Pattern: 1.4 Promotional language

**#4** [MEDIUM] Line 1: Em dash overuse
- Current: "platform—powered by cutting-edge AI—seamlessly"
- Proposed: "platform powered by AI"
- Pattern: 4.1 Formulaic em dashes

**#5** [HIGH] Line 2: AI vocabulary
- Current: "seamlessly delivers"
- Proposed: "delivers"
- Pattern: 2.1 Overused AI word

**#6** [MEDIUM] Line 2: AI vocabulary
- Current: "robust solutions"
- Proposed: "reliable solutions" or "solutions"
- Pattern: 2.1 AI vocabulary

**#7** [HIGH] Line 2: AI vocabulary
- Current: "empower teams"
- Proposed: "enable teams"
- Pattern: 2.1 Overused AI word

**#8** [HIGH] Line 2: Cliché phrase
- Current: "unlock their full potential"
- Proposed: "work more effectively"
- Pattern: 1.4 Promotional language

**#9** [HIGH] Line 3: Promotional language
- Current: "groundbreaking approach"
- Proposed: "approach"
- Pattern: 1.4 Positively loaded language

**#10** [HIGH] Line 3: Undue symbolism
- Current: "serves as a testament to innovation"
- Proposed: "demonstrates innovation" or remove
- Pattern: 1.1 Emphasis on symbolism

**#11** [HIGH] Line 3: AI vocabulary
- Current: "showcasing how"
- Proposed: state directly
- Pattern: 2.1 Overused AI word + 1.3 Superficial analysis

**#12** [MEDIUM] Line 4: AI vocabulary
- Current: "foster collaboration"
- Proposed: "encourage collaboration"
- Pattern: 2.1 AI vocabulary

**#13** [MEDIUM] Line 4: AI vocabulary
- Current: "drive results"
- Proposed: "create results" or "produce results"
- Pattern: 2.1 AI vocabulary

**#14** [HIGH] Line 4: AI vocabulary
- Current: "Let's delve into"
- Proposed: "Let's examine"
- Pattern: 2.1 Overused AI word

**#15** [HIGH] Line 5: AI vocabulary + superficial analysis
- Current: "aligns with modern needs and underscores the importance"
- Proposed: "meets modern needs"
- Pattern: 2.1 AI vocabulary + 1.3 Superficial analysis

---
Review proposed changes...
```

**Step 2: User accepts all**
```
accept all
```

**Step 3: Result**
```markdown
✅ Applied all 15 fixes

File updated: example.md

# Updated Content

Our platform powered by AI delivers reliable solutions that enable
teams to work more effectively. This approach demonstrates innovation
by encouraging collaboration and producing results. Let's examine how
this system meets modern needs.

# De-AI Statistics

**Before:**
- Content patterns: 4 (symbolism, superficial analyses)
- AI vocabulary: 9
- Formulaic structures: 2
- Total AI patterns: 15

**After:**
- Content patterns: 0
- AI vocabulary: 0
- Formulaic structures: 0
- Total AI patterns: 0

**Improvement:** 100% reduction
**Readability:** More direct, specific, and human
```

## Key Points

1. **Context matters**: Not all em dashes or "AI words" are actually AI—patterns matter more than individual words
2. **Wait for user**: DO NOT auto-fix without user acceptance
3. **Be specific**: Replace vague AI phrases with concrete language
4. **Preserve meaning**: Don't remove important information
5. **Prioritize**: Focus on high-impact changes (content patterns, superficial analyses, formulaic structures)
6. **Natural voice**: Aim for conversational, direct writing that states facts rather than analyzing them

## Pattern Source

AI writing patterns based on extensive research from Wikipedia's "Wikipedia:Large language models/AI-generated content indicators" - a comprehensive field guide compiled from analysis of thousands of AI-generated text samples. Patterns include content tells (symbolism emphasis, superficial analyses), language tells (overused vocabulary, negative parallelisms), and structural tells (formulaic conclusions, false ranges).

## DSL Syntax Rules

**Supported commands:**
- `accept all` or `accept: all` → Apply all fixes as-is
- `reject all` or `reject: all` → Skip all
- `accept: 1,2,3` → Apply only #1, #2, #3
- `reject: 2,4` → Apply all EXCEPT #2, #4
- `accept: 1-5` → Apply range #1 through #5
- `accept: 1,3-5,7` → Combine ranges and individual
- `edit: 2,3` or `e: 2,3` → Manually edit proposed fixes for #2, #3
- `accept: 1,4  edit: 2,3` → Combine commands

**Case insensitive**: Accept, ACCEPT, accept all work

## Workflow Summary

1. Scan document → identify AI writing patterns
2. Present numbered issues with Current → Proposed
3. Prompt user with DSL options
4. **WAIT** for user input
5. If user requests edits → enter edit mode for specific issues
6. Parse DSL → determine which to fix
7. Apply fixes using Edit tool
8. Report results with before/after statistics
9. Show improved content metrics

Make writing sound human, direct, and authentic.
