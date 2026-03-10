---
uuid: cmd-meme-0t1u2v3w
---

# Generate Meme

Generate SVG memes with various template formats.

## Usage

```bash
/generate-meme "topic" [--template=<type>] [--output-dir=<path>] [--variants=<n>] [--skip-qc]
```

## Arguments

- `topic` (required): The subject/topic for the meme
- `--template=<type>` (optional): Meme template type. Options:
  - `all` - Generate all templates (default)
  - `expanding-brain` - Brain expansion meme (4 panels)
  - `drake` - Drake approval/disapproval meme
  - `two-buttons` - Sweating person choosing between two buttons
  - `distracted-boyfriend` - Person looking at alternative while with partner
  - `is-this-a-pigeon` - Person misidentifying something
- `--output-dir=<path>` (optional): Output directory (default: current directory)
- `--variants=<n>` (optional): Number of variants to generate per template (default: 5)
- `--skip-qc` (optional): Skip QC loop and generate directly (single-pass mode)

## Examples

```bash
# Generate all meme templates about mortgage tech
/generate-meme "mortgage tech software"

# Generate only Drake meme about DevOps
/generate-meme "DevOps practices" --template=drake

# Generate all templates in specific directory
/generate-meme "cloud migration" --output-dir=./memes
```

## Instructions

You are a meme generation assistant with self-reflective QC capabilities. Generate SVG memes based on the user's topic using an iterative refinement process.

### Process Overview

**Default Mode (with QC loop):**
1. Generate N variants (default: 5) per template
2. Self-evaluate each variant using scoring rubric
3. Present top 3 variants with scores
4. User selects favorite or requests refinement
5. Iterate based on feedback

**Single-Pass Mode (--skip-qc):**
1. Generate 1 high-quality variant per template
2. Save immediately without evaluation

### Detailed Process (QC Loop Enabled)

#### Phase 1: Topic Analysis
1. **Understand the topic**: Analyze the subject matter to identify:
   - Industry pain points
   - Ironies and contradictions
   - Common frustrations
   - Technical jargon and terminology
   - Relatable scenarios

#### Phase 2: Variant Generation
2. **Select templates**: Use specified template or generate all
3. **Generate variants**: For each template, create N variants (default: 5) with different approaches:
   - Variant 1: Obvious/direct pain point
   - Variant 2: Ironic contradiction
   - Variant 3: Technical/insider joke
   - Variant 4: Absurdist escalation
   - Variant 5: Meta-commentary on the industry
4. **Create content**: Each variant should:
   - Highlight different aspects of the topic
   - Use industry-specific jargon appropriately
   - Create humorous contrast between panels
   - Be concise (max 60 chars per line)

#### Phase 3: Self-Evaluation
5. **Score each variant**: Use evaluation rubric (see below)
6. **Rank variants**: Sort by total score
7. **Select top 3**: Present highest-scoring variants

#### Phase 4: User Selection
8. **Present variants**: Show scores and brief description of each
9. **Get user input**:
   - User selects variant number (1-3) to save
   - User types "refine" to regenerate with feedback
   - User types "all" to save all top 3
   - User types "regenerate" to create 5 new variants

#### Phase 5: Refinement (if requested)
10. **Analyze feedback**: Understand what worked/didn't work
11. **Generate new variants**: Create 5 new variants incorporating feedback
12. **Repeat QC loop**: Return to Phase 3

#### Phase 6: Finalization
13. **Generate SVG**: Create final SVG file(s) with:
    - Proper dimensions and viewBox
    - Clear text rendering
    - Appropriate colors and styling
    - Visual elements (faces, gestures, objects)
14. **Save files**: Name as `{template-name}-{topic-slug}-v{variant}.svg`
15. **Confirm**: Display saved file paths

### Template Specifications

#### Expanding Brain (4 panels, vertical)
- **Dimensions**: 800x1000
- **Structure**: 4 stacked panels, each 220px high
- **Brain progression**: Small → Normal → Glowing → Exploding galaxy
- **Text**: Left side brain visual, right side escalating statements
- **Purpose**: Show progression from simple to absurdly complex/ironic

#### Drake (2 panels, vertical)
- **Dimensions**: 800x600
- **Structure**: 2 panels (270px each), split left (Drake) / right (text)
- **Gestures**: Top = disapproving (🙅‍♂️), Bottom = approving (👉😏)
- **Text**: Top = logical/good option, Bottom = illogical/bad option (ironic preference)
- **Purpose**: Show preference for worse option

#### Two Buttons (single panel)
- **Dimensions**: 800x700
- **Structure**: Two buttons top, sweating person center, caption bottom
- **Buttons**: Red (left) and Blue (right) with clear labels
- **Person**: Sweating, worried expression, hands reaching toward buttons
- **Purpose**: Show difficult choice or avoidance of obvious solution

#### Distracted Boyfriend (single scene)
- **Dimensions**: 1000x700
- **Structure**: 3 characters (girlfriend left, boyfriend center, other woman right)
- **Characters**:
  - Left: Angry girlfriend (represents current/legacy solution)
  - Center: Boyfriend looking back (represents decision maker)
  - Right: Attractive woman (represents new/shiny solution)
- **Labels**: Name each character, add speech bubbles
- **Purpose**: Show attraction to new solution despite commitment to current one

#### Is This A Pigeon (single scene)
- **Dimensions**: 1000x800
- **Structure**: Person (left/bottom), butterfly/object (top/right), speech bubble
- **Person**: Pointing up at object, confused expression
- **Object**: Flying thing representing misidentified concept
- **Speech bubble**: "Is this {wrong label}?"
- **Purpose**: Show misunderstanding or mislabeling of concepts

### SVG Best Practices

1. **Clean structure**: Use groups (`<g>`) for logical components
2. **Readable text**: Arial/sans-serif, 18-32px sizes, bold for emphasis
3. **Color palette**:
   - Backgrounds: Light (#f0f0f0, #f8f8f8)
   - Skin tones: #ffdbac
   - Primary colors: Industry-appropriate
4. **Stroke consistency**: 2-3px for borders, 3px for emphasis
5. **Proper labels**: Text labels in white boxes with slight transparency
6. **Speech bubbles**: Ellipse with triangle pointer

### Evaluation Rubric

Score each variant on a 1-10 scale across these criteria:

#### 1. Humor Quality (Weight: 3x)
- **10**: Laugh-out-loud funny, perfect comedic timing
- **8**: Very funny, solid joke execution
- **6**: Amusing, gets a chuckle
- **4**: Mildly funny, weak punchline
- **2**: Not funny, joke falls flat

#### 2. Relatability (Weight: 2x)
- **10**: Universal pain point, everyone in industry will relate
- **8**: Very relatable to most practitioners
- **6**: Somewhat relatable, niche audience
- **4**: Limited relatability, obscure reference
- **2**: Not relatable, misses the mark

#### 3. Technical Accuracy (Weight: 2x)
- **10**: Perfectly accurate industry knowledge, insider credibility
- **8**: Accurate with minor creative license
- **6**: Mostly accurate, some simplification
- **4**: Questionable accuracy, potential errors
- **2**: Inaccurate, shows lack of understanding

#### 4. Visual Clarity (Weight: 1x)
- **10**: Crystal clear, text is concise and readable
- **8**: Clear with minor verbosity
- **6**: Understandable but somewhat cluttered
- **4**: Unclear, too much text or confusing layout
- **2**: Difficult to read or understand

#### 5. Originality (Weight: 2x)
- **10**: Fresh take, never seen this angle before
- **8**: Creative variation on common theme
- **6**: Standard approach, competent execution
- **4**: Predictable, seen many times
- **2**: Cliché, overused joke

**Total Score Calculation:**
```
Total = (Humor × 3) + (Relatability × 2) + (Technical × 2) + (Visual × 1) + (Originality × 2)
Maximum = 100 points
```

**Quality Thresholds:**
- 90-100: Excellent, viral potential
- 75-89: Very good, highly shareable
- 60-74: Good, solid meme
- 45-59: Acceptable, needs refinement
- Below 45: Poor, regenerate

### Content Guidelines

1. **Industry-specific**: Use appropriate jargon and references
2. **Ironic humor**: Highlight contradictions in practices
3. **Relatable**: Focus on common pain points
4. **Concise text**: 1-2 lines per text block, max 60 characters per line
5. **Escalation**: Build from reasonable to absurd (expanding brain) or contrast good/bad (Drake)

### QC Loop Presentation Format

When presenting variants to user, use this format:

```markdown
## Generated Variants for [{template}] - "{topic}"

### Variant 1 (Score: 87/100) 🥇
**Concept:** [Brief description of the joke/angle]
**Content:**
- Panel 1: "[text]"
- Panel 2: "[text]"
- ...

**Scores:**
- Humor: 9/10 (Weight: 3x) = 27
- Relatability: 8/10 (Weight: 2x) = 16
- Technical: 9/10 (Weight: 2x) = 18
- Visual: 8/10 (Weight: 1x) = 8
- Originality: 9/10 (Weight: 2x) = 18
**Total: 87/100** - Very good, highly shareable

---

### Variant 2 (Score: 82/100) 🥈
[Same format]

---

### Variant 3 (Score: 78/100) 🥉
[Same format]

---

**What would you like to do?**
- Type `1`, `2`, or `3` to select a variant to save
- Type `all` to save all 3 variants
- Type `refine [feedback]` to regenerate with specific feedback
- Type `regenerate` to create 5 completely new variants
```

### Output

**QC Loop Mode:**
1. Present top 3 variants with scores
2. Wait for user selection
3. Generate and save selected SVG(s)
4. List created file paths
5. Provide viewing suggestions

**Single-Pass Mode (--skip-qc):**
1. Generate single high-quality variant per template
2. Save immediately
3. List all created files with paths
4. Provide brief description of each meme's joke
5. Suggest viewing method (browser, file viewer)

## Examples of Generated Content

### Mortgage Tech Software (Expanding Brain)
1. "Manual underwriting in Excel spreadsheets"
2. "Using mortgage origination software"
3. "AI-powered automated underwriting"
4. "Still manually re-keying data between 7 different legacy systems that don't talk to each other"

### DevOps (Drake)
- Top (disapprove): "Implementing proper CI/CD pipeline"
- Bottom (approve): "Manually SSHing into production to fix bugs at 2am"

### Cloud Migration (Two Buttons)
- Left button: "Properly architect for cloud-native"
- Right button: "Lift-and-shift everything and call it 'cloud'"
- Caption: "Every enterprise CTO"
