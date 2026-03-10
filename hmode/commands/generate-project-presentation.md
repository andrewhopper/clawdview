---
uuid: cmd-proj-pres-3w4x5y6z
version: 1.0.0
last_updated: 2025-11-11
description: Generate Slidev presentation for prototype
---

# Generate Project Presentation

Generate Slidev presentation for `{proto_dir}`.

## Usage

```bash
/generate-project-presentation prototypes/proto-027-semantic-schema-mapper [--output=artifacts/presentations/PRESENTATION.slides.md] [--narrative=./NARRATIVE.md]
```

**Arguments:**
- `{proto_dir}`: Path to prototype or idea directory
- `--output=artifacts/presentations/PRESENTATION.slides.md`: Output file path (default: artifacts/presentations/{proto-name}.slides.md)
- `--narrative=./NARRATIVE.md`: Path to narrative doc (optional, enhances content)

## Output

**PRESENTATION.slides.md** - Slidev presentation with:
- Title slide
- Problem statement
- Solution approach
- Architecture diagram
- Key features
- Tech stack
- Demo/Usage
- Results/Impact
- Next steps

## Workflow

### Step 1: Gather Content

1. **Read project files**:
   - `.project` → metadata, description, success_criteria
   - `README.md` → overview, purpose
   - `NARRATIVE.md` (if provided) → comprehensive project story
   - `ARCHITECTURE.md` or `design/ARCHITECTURE.md` → architecture details
   - `diagrams/architecture.md` → Mermaid architecture diagram (if exists)

2. **Extract key information**:
   - **Problem**: What problem does this solve?
   - **Solution**: How does it solve it?
   - **Architecture**: High-level system design
   - **Features**: Key capabilities
   - **Tech stack**: Technologies used
   - **Impact**: Results, metrics, outcomes
   - **Next steps**: Future work, improvements

### Step 2: Build Presentation Structure

3. **Slidev frontmatter** (YAML header):

```yaml
---
theme: default
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## {Project Name}

  {Brief description}
drawings:
  persist: false
transition: slide-left
title: {Project Name}
mdc: true
---
```

4. **Slide structure** (10-15 slides):

**Slide 1**: Title + Author
**Slide 2**: Problem Statement
**Slide 3**: Solution Approach
**Slide 4**: Architecture Overview
**Slide 5**: Architecture Diagram
**Slide 6**: Key Features
**Slide 7**: Tech Stack
**Slide 8**: Implementation Highlights
**Slide 9**: Demo/Usage
**Slide 10**: Results/Impact
**Slide 11**: Learnings
**Slide 12**: Next Steps
**Slide 13**: Q&A

### Step 3: Generate Slide Content

5. **Slide 1: Title**

```markdown
---
layout: cover
---

# {Project Name}

{Tagline or brief description}

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

<div class="abs-br m-6 flex gap-2">
  <span class="text-sm opacity-50">Andy Hopper | AWS Solutions Architect</span>
</div>
```

6. **Slide 2: Problem Statement**

```markdown
---
layout: default
---

# Problem

<v-clicks>

- **Challenge**: {What's the core problem?}
- **Impact**: {Who does it affect? How?}
- **Current state**: {What are people doing today?}
- **Pain points**: {What's wrong with current approach?}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 2
</div>
```

7. **Slide 3: Solution**

```markdown
---
layout: default
---

# Solution

<v-clicks>

- **Approach**: {High-level solution strategy}
- **Key innovation**: {What makes this different/better?}
- **Benefits**: {Top 3-5 benefits}
- **Target users**: {Who is this for?}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 3
</div>
```

8. **Slide 4: Architecture Overview**

```markdown
---
layout: two-cols
---

# Architecture

## Design Principles

<v-clicks>

- {Principle 1: e.g., "Event-driven"}
- {Principle 2: e.g., "Serverless"}
- {Principle 3: e.g., "Modular"}

</v-clicks>

::right::

## Components

<v-clicks>

- **{Component 1}**: {Purpose}
- **{Component 2}**: {Purpose}
- **{Component 3}**: {Purpose}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 4
</div>
```

9. **Slide 5: Architecture Diagram**

```markdown
---
layout: default
---

# Architecture Diagram

\`\`\`mermaid {scale: 0.8}
{Insert Mermaid diagram from diagrams/architecture.md OR generate simple graph}
\`\`\`

<div class="abs-br m-6 text-sm opacity-50">
  Slide 5
</div>
```

10. **Slide 6: Key Features**

```markdown
---
layout: default
---

# Key Features

<v-clicks>

- ✅ **{Feature 1}**: {Description}
- ✅ **{Feature 2}**: {Description}
- ✅ **{Feature 3}**: {Description}
- ✅ **{Feature 4}**: {Description}
- ✅ **{Feature 5}**: {Description}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 6
</div>
```

11. **Slide 7: Tech Stack**

```markdown
---
layout: two-cols
---

# Tech Stack

## Frontend
<v-clicks>

- {Frontend framework: React/Vue/Next.js}
- {UI library: Tailwind/Material/etc.}

</v-clicks>

## Backend
<v-clicks>

- {Backend framework: Node.js/Python/Go}
- {API type: REST/GraphQL/gRPC}

</v-clicks>

::right::

## Data & Infrastructure
<v-clicks>

- **Database**: {PostgreSQL/MongoDB/etc.}
- **Cache**: {Redis/etc.}
- **Cloud**: {AWS/GCP/Azure}
- **Deployment**: {Docker/K8s/Serverless}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 7
</div>
```

12. **Slide 8: Implementation Highlights**

```markdown
---
layout: default
---

# Implementation Highlights

<v-clicks>

- **{Highlight 1}**: {Technical detail or design decision}
- **{Highlight 2}**: {Technical detail or design decision}
- **{Highlight 3}**: {Technical detail or design decision}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 8
</div>
```

13. **Slide 9: Demo/Usage**

```markdown
---
layout: default
---

# Demo / Usage

## Example

\`\`\`bash
# Installation
npm install {package-name}

# Usage
{example command or code snippet}
\`\`\`

<v-clicks>

**Result**: {What happens when you run this}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 9
</div>
```

14. **Slide 10: Results/Impact**

```markdown
---
layout: default
---

# Results & Impact

<v-clicks>

- 📊 **{Metric 1}**: {Result - e.g., "50% faster processing"}
- 📊 **{Metric 2}**: {Result - e.g., "Reduced cost by $X"}
- 📊 **{Metric 3}**: {Result - e.g., "Improved UX by X%"}
- ✅ **{Qualitative result}**: {e.g., "Simplified workflow"}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 10
</div>
```

15. **Slide 11: Learnings**

```markdown
---
layout: default
---

# Key Learnings

<v-clicks>

- 💡 **{Learning 1}**: {What worked well}
- 💡 **{Learning 2}**: {What was challenging}
- 💡 **{Learning 3}**: {What would you do differently}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 11
</div>
```

16. **Slide 12: Next Steps**

```markdown
---
layout: default
---

# Next Steps

<v-clicks>

- 🚀 **{Next step 1}**: {Future enhancement}
- 🚀 **{Next step 2}**: {Future enhancement}
- 🚀 **{Next step 3}**: {Future enhancement}

</v-clicks>

<div class="abs-br m-6 text-sm opacity-50">
  Slide 12
</div>
```

17. **Slide 13: Q&A**

```markdown
---
layout: center
class: text-center
---

# Questions?

Contact: Your AWS Solutions Architect

<div class="pt-12">
  <a href="https://github.com/{repo}" target="_blank" class="px-2 py-1 rounded cursor-pointer hover:bg-white hover:bg-opacity-10">
    View on GitHub →
  </a>
</div>
```

### Step 4: Customize Content

18. **Replace placeholders** with actual content:
    - Extract from `.project`, README, NARRATIVE.md
    - Infer problem/solution from description
    - Use actual tech stack from metadata
    - Include real metrics if available

19. **Include diagrams**:
    - If `diagrams/architecture.md` exists → embed Mermaid diagram
    - Otherwise → generate simple architecture graph from README/docs

20. **Add code examples**:
    - Extract from README usage section
    - Include installation commands
    - Show simple API call or CLI usage

### Step 5: Write Presentation File

21. **Generate complete Slidev file**:
    - Use Write tool to create `{output_file}`
    - Format: Valid Slidev markdown with YAML frontmatter

22. **Validate structure**:
    - Check YAML frontmatter is valid
    - Ensure slide separators (`---`) are correct
    - Verify Mermaid diagrams are properly formatted

23. **Report results**:

```markdown
# Presentation Generated

**Project**: {proto_name}
**Output**: {output_file}
**Slides**: {slide_count}

---

## Content

✅ Title slide
✅ Problem statement
✅ Solution approach
✅ Architecture diagram
✅ Key features
✅ Tech stack
✅ Implementation highlights
✅ Demo/usage
✅ Results/impact
✅ Learnings
✅ Next steps
✅ Q&A

---

## Preview Presentation

Run locally:
\`\`\`bash
npx slidev {output_file}
\`\`\`

Opens at: http://localhost:3030

---

## Export Options

**PDF**:
\`\`\`bash
npx slidev export {output_file} --format pdf
\`\`\`

**PowerPoint** (via PDF):
\`\`\`bash
npx slidev export {output_file} --format pdf
# Open PDF in PowerPoint, save as .pptx
\`\`\`

---

✅ Presentation ready for delivery package
```

## Content Extraction Rules

**From .project:**
- `description` → Problem statement, solution approach
- `tech_stack` → Tech stack slide
- `success_criteria` → Results/impact metrics
- `metadata.priority` → Emphasize if high priority

**From README.md:**
- First paragraph → Tagline
- "Problem" or "Background" section → Problem slide
- "Solution" or "Features" section → Solution + features slides
- "Installation" or "Usage" → Demo slide
- "Tech Stack" or "Built With" → Tech stack slide

**From NARRATIVE.md (if provided):**
- Comprehensive project story → All content
- Problem/solution sections → Respective slides
- Architecture details → Architecture slides
- Results/learnings → Impact/learnings slides

**From ARCHITECTURE.md:**
- Architecture overview → Architecture slides
- Component descriptions → Architecture + implementation slides
- Design decisions → Implementation highlights

**From diagrams/:**
- `architecture.md` → Embed in architecture diagram slide
- Other diagrams → Optional additional slides

## Slidev Features Used

**Layouts:**
- `cover` - Title slide
- `default` - Standard content
- `two-cols` - Two-column layout
- `center` - Centered content (Q&A)

**Animations:**
- `<v-clicks>` - Click-to-reveal bullet points
- `transition: slide-left` - Smooth transitions

**Styling:**
- `class: text-center` - Centered text
- `highlighter: shiki` - Code syntax highlighting
- `mdc: true` - Enhanced markdown features

**Icons:**
- Carbon icons: `<carbon:arrow-right />`
- Emoji: ✅ 🚀 📊 💡

## Best Practices

1. **Keep slides concise**: 3-5 bullet points per slide
2. **Use visuals**: Include diagrams, code, screenshots
3. **Progressive disclosure**: Use `<v-clicks>` for reveals
4. **Consistent style**: Use same layout patterns
5. **Actionable content**: Focus on "why" and "how", not just "what"
6. **Tell a story**: Problem → Solution → Results → Next
7. **Quantify impact**: Include metrics where possible

## Error Handling

**No README found:**
```
Warning: README.md not found
Generating presentation from .project metadata only
Result: Basic presentation with limited detail
```

**No architecture info:**
```
Warning: No architecture documentation found
Skipping architecture diagram slide
Suggestion: Add ARCHITECTURE.md for better presentation
```

**Invalid Slidev format:**
```
Error: Invalid Slidev format generated
Fix: Review YAML frontmatter and slide separators
```

## Testing Presentation

**Local preview:**
```bash
npx slidev PRESENTATION.slides.md
```

**Export to PDF:**
```bash
npx slidev export PRESENTATION.slides.md --format pdf
```

**Export to PowerPoint:**
```bash
npx slidev export PRESENTATION.slides.md --format pptx
```

Note: pptx export may require additional setup

## Integration

Works with:
- `/prepare-delivery` - Called by main delivery workflow
- `/generate-project-diagram` - Uses generated diagrams
- `/generate-project-narrative` - Uses narrative content
- `/amazon-style-checker` - Validates AWS style

---

Be visual, concise, and story-focused.
