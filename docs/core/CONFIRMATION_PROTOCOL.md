## 📡 CONFIRMATION PROTOCOL (Air Traffic Control)

**Purpose:** Prevent AI from executing wrong interpretation. Like ATC readback: confirm before action.

**Adapt to engineer level:**
- **Staff/Principal:** Assume deep arch knowledge. Concise options, minimal explanation.
- **Mid-level:** Balance detail and brevity. Include key rationale.
- **Junior:** More explanation. Clarify trade-offs, provide context.
- **Default:** Assume mid-level unless specified.

**When to confirm:**
- ✅ Complex multi-step tasks
- ✅ Ambiguous requests
- ✅ Multiple valid interpretations
- ✅ High-impact operations (delete, refactor, architecture changes)
- ✅ Phase transitions
- ❌ Small obvious tasks (read file, simple edits, status checks)

**Protocol flow:**

**1. Paraphrase request** (concise, densified)
```
User: "Add confirmation protocol to Claude.md and SDLC"
AI: "Request understood: Add ATC-style confirmation protocol to CLAUDE.md"
```

**2. Present 2-6 options** (fit on screen)
```
Option A: New section after CRITICAL RULES
  - Standalone protocol section
  - Referenced in enforcement rules
  - Trade-off: More visible, adds length

Option B: Add to existing "AI Partnership by Phase"
  - Integrates with phase descriptions
  - Less structural change
  - Trade-off: Less prominent, harder to find

Option C: Add to ENFORCEMENT section
  - Protocol as enforcement rule
  - Single location for rules
  - Trade-off: Buried with other rules
```

**3. AI recommendation** (brief rationale)
```
Recommend: Option A
Rationale: Protocol affects all phases. Visibility critical. Minimal length impact.
```

**4. User action + feedback prompt**
```
Look good? y/n/f                    f for feedback on the process
```

**Available actions:**
- `y` or `accept` - proceed with recommendation
- `n` or `reject` - cancel/regenerate
- `f` or `feedback` - provide feedback to improve CLAUDE.md (then proceed with task)
- `A` or `B` or `C` - select specific option
- `revise: <feedback>` - regenerate with guidance
- `skip` - skip confirmation for this task

**Format:** Always end confirmations with feedback reminder on same line, right-aligned feel using spaces

**Format rules:**
- **Order options best→worst** (AI rating, best first)
- **Include ASCII diagrams** (10-second visual scan)
- Max 6 options (screen limit)
- Each option: approach + key trade-off
- Use densified language (bullets, arrows, no filler)
- Options must be meaningfully different
- Trade-offs required (no option is perfect)
- Adapt detail level to engineer experience

**Examples:**

**Complex task (Staff/Principal level):**
```
User: "Refactor divergent mode to support 5 generations"
AI: "Refactor request: Extend genetic AI depth from 3→5 generations"

Option A: Generalize depth parameter (BEST)
  G1 → G2 → G3 → G4 → G5 (single run)
   3    9    27   81   243 variants
  - Update validation (max depth=5)
  - Extend naming (A1a1a, A1a1b...)
  - Trade-off: 3^5 = 243 variants, exponential complexity

Option B: Chain convergence→divergence
  [Run 1: G1→G2→G3] → converge → [Run 2: G1→G2] = 5 total
  - Keep depth=3 cap
  - Document multi-run pattern
  - Trade-off: Manual, no single execution

Recommend: A

Look good? y/n/f                    f for feedback on the process
```

**Same task (Junior level):**
```
User: "Refactor divergent mode to support 5 generations"
AI: "Refactor request: Extend genetic AI depth from 3→5 generations"

Option A: Generalize depth parameter (BEST)
  ┌─────────────────────────────────────────────┐
  │ G1 → G2 → G3 → G4 → G5  (single automated run) │
  │  3    9    27   81   243 final variants    │
  └─────────────────────────────────────────────┘
  - Update validation to allow max depth=5 instead of 3
  - Extend naming convention for deeper nesting (A1a1a, A1a1b...)
  - Why best: Directly addresses your need for 5 generations
  - Trade-off: Exponential growth warning needed (3^5 = 243 final variants)
  - Context: Each generation breeds WIDTH children. Depth 5 creates 5 generations.

Option B: Keep depth=3, document workaround pattern
  ┌───────────────┐    ┌─────────┐
  │ G1→G2→G3 (27) │ → │ G1→G2(9)│ = 5 total generations
  │   Run 1       │    │  Run 2  │   (manual process)
  └───────────────┘    └─────────┘
  - No code changes to existing divergent logic
  - Show users how to chain: run divergent depth=3 → converge → new divergent depth=2
  - Why considered: Safer, avoids exponential complexity
  - Trade-off: Manual multi-step process, no single automated run
  - Context: Workaround achieves 5 total gens but requires manual intervention

Recommend: A
Rationale: You explicitly asked for 5 gen support. Option A delivers that directly.
Complexity is manageable with proper warnings in docs and .project validation.

Look good? y/n/f                    f for feedback on the process
```

**Small obvious task (skip confirmation):**
```
User: "Read the .project file"
AI: [Directly reads file without confirmation]
```

**Ambiguous request:**
```
User: "Make the docs better"
AI: "Request: Improve documentation quality"

Option A: Audit against CLAUDE.md standards (BEST)
  Docs → [Audit] → Gap Report → Prioritized Fixes
         ┌──────────────────────────┐
         │ ✓ Decimal outline?       │
         │ ✓ Stage titles?          │
         │ ✓ ASCII diagrams?        │
         │ ✓ Trade-offs documented? │
         └──────────────────────────┘
  - Check decimal outline, stage titles, completeness
  - Generate gap report with prioritized fixes
  - Trade-off: Analysis only, requires follow-up action

Option B: Add ASCII diagrams to design docs
  Docs → [Add Visuals] → Scannable in 10sec
         ┌─────────┐      ┌─────────┐
         │ Before  │  →   │  After  │
         │ [Text]  │      │ [Diagram]│
         │ [Text]  │      │ [Text]  │
         └─────────┘      └─────────┘
  - Visual comprehension improvements
  - Meets markdown visual requirements
  - Trade-off: Manual effort, design time

Option C: Run /densify on all .md files
  Docs → [Densify] → 50% fewer words
  "The system provides capability..." → "System: LLM → quality"
  - Apply concise writing standards
  - Remove filler, tighten language
  - Trade-off: Automated but may lose important context

Recommend: A → then B or C based on gaps
Rationale: Assess before acting. Targeted improvements more effective than blanket changes.

Look good? y/n/f                    f for feedback on the process
```

**Enforcement:**
- AI MUST confirm before executing complex/ambiguous tasks
- AI MUST skip confirmation for small obvious tasks
- Options MUST include trade-offs (honest assessment)
- Recommendation MUST have brief rationale
- User can override with option letter or `skip`

---

## 🎯 RESPONSE VALIDATION (Auto-Proceed vs Confirm)

**Purpose:** Judge user response clarity to prevent errors from typos/ambiguity while maintaining flow.

**Rule:** Evaluate EVERY user response for confidence level:
- **High confidence (≥90%)** → Proceed automatically
- **Low confidence (<90%)** → Echo interpretation + request confirmation

**Confidence factors:**
1. **Standard shorthand:** Recognize y/yes/yeah/ye/yep/yup/n/no/nope/nah/ok/okay as high confidence (≥96%)
2. **Common commands:** Recognize test/open/fix/start/run/check as high confidence (≥95%)
3. **Phonetic similarity:** Soundex/Metaphone for "sounds like" matching (gith→git, nop→nope)
4. **Semantic similarity:** BERT/embeddings for intent matching (test≈check≈verify)
5. **Contextual validation:** Domain-specific validation and auto-correction (ports, URLs, technical terms)
6. **Implicit references:** "this", "it", "the X" with clear antecedent → High confidence
7. **Continuation markers:** "too", "also", "and" at start → High confidence (continuing previous context)
8. **Length:** Very short non-standard responses (<5 chars) → Lower confidence
9. **Context match:** Response addresses the question → Higher confidence
10. **Completeness:** Provides expected information → Higher confidence
11. **Edit distance:** Levenshtein distance ≤2 for typo detection
12. **Ambiguity:** Multiple interpretations possible → Lower confidence

**Examples:**

**Example 1: File naming**
```
AI: "Would you like to name the file cats.txt?"
User: "no cat.dat"
Analysis:
  ✓ Clear negation ("no")
  ✓ Provides alternative ("cat.dat")
  ✓ Context match (filename provided)
  ✓ Complete response
  → Confidence: 95% → PROCEED with cat.dat
```

```
AI: "Would you like to name the file cats.txt?"
User: "ca.dat"
Analysis:
  ✗ No negation (ambiguous intent)
  ✗ Very short (possible typo)
  ✗ Similar to "cat.dat" (1 char diff)
  ? Might be typo, might be intended abbreviation
  → Confidence: 40% → CONFIRM

AI response: "Name it 'ca.dat'? (or did you mean 'cat.dat'?) y/n"
```

**Example 2: Technical decision**
```
AI: "Use AWS Lambda for this function?"
User: "yes serverless makes sense here"
Analysis:
  ✓ Clear affirmation
  ✓ Provides reasoning
  ✓ Context match
  → Confidence: 98% → PROCEED
```

```
AI: "Use AWS Lambda for this function?"
User: "ye"
Analysis:
  ✗ Very short (2 chars)
  ✗ Possible typo of "yes"
  ✗ Could be incomplete
  → Confidence: 60% → CONFIRM

AI response: "Confirm: Use AWS Lambda? y/n"
```

**Example 3: Directory path**
```
AI: "Install in /opt/myapp?"
User: "no use /home/user/myapp instead"
Analysis:
  ✓ Clear negation
  ✓ Full alternative path
  ✓ Complete response
  → Confidence: 95% → PROCEED
```

```
AI: "Install in /opt/myapp?"
User: "/hom/user/myapp"
Analysis:
  ✗ Missing negation (did user see the question?)
  ✗ Potential typo ("/hom" vs "/home")
  → Confidence: 50% → CONFIRM

AI response: "Install in '/hom/user/myapp'? (noted: /hom might be typo for /home) y/n"
```

**Example 4: Standard Shorthand**
```
AI: "Deploy to production environment?"
User: "y"

Analysis:
  ✓ Standard shorthand (y = yes)
  ✓ Clear affirmation
  ✓ Context match
  → Confidence: 96%
  → PROCEED with production deployment
```

**Example 5: Informal Shorthand**
```
AI: "Enable feature flag?"
User: "ye"

Analysis:
  ✓ Standard informal shorthand (ye = yes)
  ✓ Clear affirmation
  ✓ Context match
  → Confidence: 96%
  → PROCEED with feature flag enabled
```

**Example 6: Port Configuration**
```
AI: "Run on port 3000?"
User: "nope use 8080"

Analysis:
  ✓ Standard shorthand negation ("nope")
  ✓ Provides alternative (8080)
  ✓ Complete response
  → Confidence: 96%
  → PROCEED with port 8080
```

**Example 7: Database Selection**
```
AI: "Use PostgreSQL for database?"
User: "yup postgres is better for this"

Analysis:
  ✓ Standard shorthand affirmation ("yup")
  ✓ Provides reasoning
  ✓ Context match
  → Confidence: 98%
  → PROCEED with PostgreSQL
```

**Example 8: Ambiguous Abbreviation**
```
AI: "Install React Testing Library?"
User: "rtl"

Analysis:
  ✗ Not standard shorthand
  ✗ Ambiguous (RTL = library name or affirmation?)
  ✗ Could mean "yes, RTL" or just confirming name
  → Confidence: 35%
  → CONFIRM

AI response: "Install React Testing Library? (did you mean 'yes'?) y/n"
```

**Example 9: Incomplete Path**
```
AI: "Save config to ~/.config/myapp/settings.json?"
User: "yeah that works"

Analysis:
  ✓ Standard shorthand ("yeah")
  ✓ Explicit confirmation ("that works")
  ✓ Complete response
  → Confidence: 98%
  → PROCEED with ~/.config/myapp/settings.json
```

**Example 10: Typo + Non-Destructive Action**
```
AI: "Install ESLint package?"
User: "yex"

Analysis:
  ✓ Non-destructive action (install)
  ✓ Likely typo "yex" → "yes" (distance 1)
  → Confidence: 92% (base 70% + 20% non-destructive boost)
  → PROCEED

AI response: "Installing ESLint package"
```

**Example 11: Typo + Destructive Action**
```
AI: "Delete production database?"
User: "yex"

Analysis:
  ✗ Destructive action (delete)
  ✗ Likely typo "yex" → "yes" (distance 1)
  → Confidence: 45% (no boost for destructive)
  → CONFIRM

AI response: "Delete production database? (did you mean 'yes'?) y/n"
```

**Example 12: Common Command**
```
AI: "I've updated the API. What would you like to do next?"
User: "test this"

Analysis:
  ✓ Common command pattern ("test")
  ✓ Implicit reference ("this" = the API)
  ✓ Clear antecedent (API just updated)
  → Confidence: 95%
  → PROCEED with testing the API
```

**Example 13: Common Command (Ultra-Short)**
```
AI: "The feature is ready. Next steps?"
User: "open"

Analysis:
  ✓ Common command ("open")
  ✓ Implicit object (the feature)
  ✓ Context clear
  → Confidence: 95%
  → PROCEED with opening/starting the feature
```

**Example 14: Implicit Reference with Context**
```
AI: "I've created the web interface. Would you like me to proceed?"
User: "start it"

Analysis:
  ✓ Common command ("start")
  ✓ Implicit reference ("it" = the web interface)
  ✓ Clear antecedent
  → Confidence: 95%
  → PROCEED with starting the web interface
```

**Example 15: Continuation Marker**
```
AI: "Added unit tests. What else?"
User: "also create sample data"

Analysis:
  ✓ Continuation marker ("also")
  ✓ Clear addition to previous work
  ✓ Complete instruction
  → Confidence: 96%
  → PROCEED with creating sample data
```

**Confirmation format:**
```
Confirm: [INTERPRETATION]? y/n
```

**With typo suggestion:**
```
[INTERPRETATION]? (or did you mean [ALTERNATIVE]?) y/n
```

**Standard Shorthand (Always High Confidence):**
- **Affirmative:** `y`, `yes`, `yeah`, `ye`, `yep`, `yup`, `ok`, `okay` (≥96% confidence)
- **Negative:** `n`, `no`, `nope`, `nah` (≥96% confidence)

**Common Commands (High Confidence ≥95%):**
- **Testing:** `test`, `test this`, `test it`, `check`, `check this`, `verify`
- **Viewing:** `open`, `open this`, `open it`, `start`, `start it`, `show`, `show me`
- **Actions:** `fix`, `fix this`, `fix it`, `run`, `run it`, `go`, `do it`
- **Continuation:** `also`, `too`, `and`, `plus` (at start of response)

---

## 🎯 CONTEXTUAL VALIDATION (Semantic Speed)

**Purpose:** Auto-correct common patterns and validate domain-specific inputs for maximum speed.

**Rule:** Apply domain-specific validation based on question context. High confidence → auto-correct and proceed.

**Domain-Specific Rules:**

**1. Port Numbers (Context: "port", "listen", "server")**
- **Valid range:** 1-65535
- **Common ports:** 80, 443, 3000, 8080, 8000, 5000, 5432, 27017
- **Auto-correct:**
  - `8` → `8000` (add trailing zeros)
  - `80` → `8080` (if 80 unavailable, suggest 8080)
  - `300` → `3000` (likely missing zero)
  - `808` → `8080` (likely missing zero)
- **Invalid:** `99999`, `0`, `-1` → CONFIRM with suggestion
- **Example:**
  ```
  AI: "Which port?"
  User: "808"
  → Auto-correct to 8080, confidence: 92% → PROCEED
  AI: "Starting server on port 8080"
  ```

**2. URLs (Context: "url", "link", "website", "endpoint")**
- **Auto-complete:**
  - `http` → `http://` (add protocol)
  - `https` → `https://` (add protocol)
  - `example.com` → `https://example.com` (add default protocol)
- **Validation:**
  - Check for protocol (http://, https://)
  - Check for domain structure
- **Example:**
  ```
  AI: "API endpoint URL?"
  User: "http api.example.com/v1"
  → Auto-correct to "http://api.example.com/v1", confidence: 95% → PROCEED
  AI: "Using endpoint: http://api.example.com/v1"
  ```

**3. Technical Terms (Context: technology decisions)**
- **Common typos → corrections:**
  - `gith` → `GitHub`
  - `postgre` → `PostgreSQL`
  - `mongo` → `MongoDB`
  - `redis` → `Redis`
  - `elastics` → `Elasticsearch`
  - `kubernet` → `Kubernetes`
  - `docker` → `Docker` (capitalize)
  - `aws` → `AWS` (uppercase)
  - `reactjs` → `React`
  - `nodejs` → `Node.js`
  - `typescript` → `TypeScript`
- **Example:**
  ```
  AI: "Use which version control?"
  User: "gith"
  → Auto-correct to "GitHub", confidence: 94% → PROCEED
  AI: "Using GitHub for version control"
  ```

**4. File Extensions (Context: "file", "save", "export")**
- **Auto-correct:**
  - `.js` → `.js` (valid)
  - `.t` → `.txt` (likely incomplete)
  - `.md` → `.md` (valid)
  - `.jso` → `.json` (likely typo)
  - `.yam` → `.yaml` (likely incomplete)
- **Example:**
  ```
  AI: "Save as what filename?"
  User: "config.jso"
  → Auto-correct to "config.json", confidence: 93% → PROCEED
  AI: "Saving as config.json"
  ```

**5. Paths (Context: "directory", "folder", "path")**
- **Validation:**
  - `~` → expand to home directory
  - `./` → relative path (valid)
  - `/` → absolute path (valid)
  - Missing leading `/` or `./` → suggest correction
- **Example:**
  ```
  AI: "Install directory?"
  User: "home/user/app"
  → Low confidence (missing leading /) → CONFIRM
  AI: "Install in 'home/user/app'? (did you mean '/home/user/app' or '~/app'?) y/n"
  ```

**6. Boolean Values (Context: "enable", "disable", "flag")**
- **Map to yes/no:**
  - `true`, `1`, `on`, `enabled` → yes (≥95%)
  - `false`, `0`, `off`, `disabled` → no (≥95%)
- **Example:**
  ```
  AI: "Enable feature flag?"
  User: "true"
  → Map to "yes", confidence: 96% → PROCEED
  AI: "Feature flag enabled"
  ```

**7. Numbers with Units (Context: "size", "memory", "timeout")**
- **Auto-complete units:**
  - `500` → `500ms` (if context is timeout)
  - `2` → `2GB` (if context is memory)
  - `10` → `10MB` (if context is file size)
- **Example:**
  ```
  AI: "Request timeout in milliseconds?"
  User: "5000"
  → Context: timeout → confidence: 96% → PROCEED with 5000ms
  AI: "Setting timeout to 5000ms"
  ```

**8. Destructive vs Non-Destructive Actions**

**Non-Destructive Actions (Auto-approve typos ≥90%):**
- Creating files, directories
- Reading/viewing files
- Installing packages
- Enabling features/flags
- Starting/restarting services
- Configuring settings
- Running tests
- Building projects
- Committing code (not force push)

**Destructive Actions (Confirm typos <90%):**
- Deleting files, directories, databases
- Dropping tables, collections
- Force pushing to git
- Overwriting existing data
- Terminating critical processes
- Revoking permissions
- Purging caches
- Resetting configurations

**Rule:** For non-destructive actions, auto-approve likely typos (yex→yes, nop→nope) with confidence ≥90%

**Examples:**

```
AI: "Install React package?"
User: "yex"
Analysis:
  ✓ Non-destructive action (install)
  ✓ Likely typo "yex" → "yes" (Levenshtein distance 1)
  → Confidence: 92% → PROCEED
AI: "Installing React package"
```

```
AI: "Delete production database?"
User: "yex"
Analysis:
  ✗ Destructive action (delete)
  ✗ Likely typo "yex" → "yes" (Levenshtein distance 1)
  → Confidence: 45% → CONFIRM (destructive)
AI: "Delete production database? (did you mean 'yes'?) y/n"
```

```
AI: "Enable debug logging?"
User: "ys"
Analysis:
  ✓ Non-destructive action (enable)
  ✓ Likely typo "ys" → "yes" (Levenshtein distance 2)
  → Confidence: 91% → PROCEED
AI: "Debug logging enabled"
```

**Enforcement:**
- Apply contextual validation BEFORE confidence calculation
- Auto-correct obvious issues (port ranges, URL protocols, tech term typos)
- For non-destructive actions: typos with distance ≤2 → auto-approve (≥90%)
- For destructive actions: typos always require confirmation (<90%)
- High confidence (≥90%) after correction → PROCEED with corrected value
- Low confidence (<90%) after correction → CONFIRM with suggestion
- Always show corrected value when proceeding: "Using [CORRECTED_VALUE]"
- Keep correction transparent (user sees what was interpreted)

**Confidence Boost:**
- Valid domain-specific pattern + auto-correction → +5-10% confidence
- Non-destructive action + typo correction → +15-20% confidence boost
- Example: "yex" (install package) → "yes" → 70% base + 20% boost = 90% → PROCEED
- Example: "yex" (delete database) → "yes" → 70% base + 0% boost = 70% → CONFIRM

**Standard Shorthand (Always High Confidence):**
- **Affirmative:** `y`, `yes`, `yeah`, `ye`, `yep`, `yup`, `ok`, `okay` (≥96% confidence)
- **Negative:** `n`, `no`, `nope`, `nah` (≥96% confidence)

**Common Commands (High Confidence ≥95%):**
- **Testing:** `test`, `test this`, `test it`, `check`, `check this`, `verify`
- **Viewing:** `open`, `open this`, `open it`, `start`, `start it`, `show`, `show me`
- **Actions:** `fix`, `fix this`, `fix it`, `run`, `run it`, `go`, `do it`
- **Continuation:** `also`, `too`, `and`, `plus` (at start of response)

**Implicit References (High Confidence ≥92%):**
- `this`, `it`, `that` when there's clear antecedent from previous message
- `the X` when X was mentioned in recent context
- Example: "Test this" after discussing a feature → 95% confidence

**Enforcement:**
- Apply contextual validation for domain-specific responses
- Recognize standard shorthand as high confidence (≥96%)
- Recognize common commands as high confidence (≥95%)
- Handle implicit references with clear context (≥92%)
- Calculate confidence for ALL other user responses
- Proceed automatically only if confidence ≥90%
- Always echo interpretation when confirming
- Suggest alternatives if obvious typo detected (Levenshtein distance ≤2)
- Keep confirmation concise (single line when possible)

