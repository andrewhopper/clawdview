---
uuid: cmd-gen-asset-7q8r9s0t
version: 1.0.0
last_updated: 2025-11-14
description: Genetically generate and evolve assets (images, text, code) with clustering
---

# Genetic Asset Generator

Generate any type of asset (images, text, code, designs) using genetic algorithms with multi-generation evolution, auto-sampling, and intelligent clustering.

## Quick Start

```bash
# Basic: Generate 5 variants of an image
/gen-asset "professional headshot of a software engineer" --population=5

# Advanced: Evolve over 3 generations with clustering
/gen-asset "modern logo for tech startup" --population=5 --generations=3 --clusters=3

# Auto-sample best candidates
/gen-asset "python function to parse JSON" --population=10 --auto-sample=3 --criteria="correctness,readability,efficiency"

# Full genetic evolution with weighted criteria
/gen-asset "UI design for dashboard" --population=5 --generations=2 --clusters=2 --criteria="aesthetics,usability,innovation" --weights="aesthetics:0.4,usability:0.4,innovation:0.2"
```

## Parameters

### Required

**Asset Description** (first argument):
- What to generate (prompt, description, specification)
- Examples: "logo design", "python function", "marketing copy", "system architecture"

### Optional Flags

**Population Size** (`--population=N` or `-p N`):
- Number of variants per generation
- Default: `3`
- Range: `2-10` (higher = more diversity, more cost)
- Example: `--population=5` generates 5 variants

**Generations** (`--generations=N` or `-g N`):
- Number of evolutionary iterations
- Default: `1` (no evolution, just parallel generation)
- Range: `1-5` (exponential growth: gen2 = population × gen1)
- Example: `--generations=3` creates 3 → 9 → 27 candidates

**Clusters** (`--clusters=N` or `-c N`):
- Group similar candidates for easier review
- Default: `1` (no clustering)
- Range: `2-5`
- Example: `--clusters=3` groups into 3 style families

**Auto-Sample** (`--auto-sample=N`):
- Automatically select N best candidates
- Uses criteria-based scoring
- Default: disabled (show all candidates)
- Example: `--auto-sample=3` picks top 3

**Evaluation Criteria** (`--criteria=list`):
- Comma-separated criteria for scoring
- Used for auto-sampling and breeding selection
- Default: Asset-type specific defaults
- Examples:
  - Images: `"aesthetics,creativity,prompt_alignment"`
  - Code: `"correctness,readability,efficiency,maintainability"`
  - Text: `"clarity,persuasiveness,engagement,tone"`
  - Designs: `"aesthetics,usability,innovation,brand_alignment"`

**Criteria Weights** (`--weights=weighted_list`):
- Weight each criterion (must sum to 1.0)
- Default: Equal weights
- Format: `"criterion1:0.5,criterion2:0.3,criterion3:0.2"`
- Example: `--weights="correctness:0.5,readability:0.3,efficiency:0.2"`

**Asset Type** (`--type=type`):
- Override auto-detection
- Options: `image`, `text`, `code`, `design`, `architecture`, `data`, `audio`, `video`
- Default: Auto-inferred from description
- Example: `--type=code`

**Provider** (`--provider=name`):
- Generation provider/model
- Default: Auto-selected based on type
- Options:
  - Images: `dalle3`, `midjourney`, `stable-diffusion`, `ideogram`
  - Text: `claude`, `gpt4`, `gemini`
  - Code: `claude`, `gpt4`, `copilot`
  - Multi-modal: `gemini-pro`
- Example: `--provider=dalle3`

**Output Directory** (`--output=path`):
- Where to save generated assets
- Default: `./generated-assets/{timestamp}-{slug}/`
- Example: `--output=./designs/logo-variants/`

**Diversity Dimensions** (`--diversity=list`):
- Which dimensions to vary across population
- Default: Asset-type specific
- Examples:
  - Images: `"style,color_palette,composition,mood,lighting"`
  - Code: `"algorithm,pattern,paradigm,data_structure"`
  - Text: `"tone,structure,vocabulary,length"`
- Example: `--diversity="style,color_palette,mood"`

## Asset Types & Defaults

Each asset type has intelligent defaults for genetic parameters. You can run `/gen-asset "description"` and it auto-configures based on type.

### Quick Reference: Default Genetic Parameters by Asset Type

| Asset Type | Population | Generations | Clusters | Auto-Sample | Cost Est. |
|-----------|-----------|-------------|----------|-------------|-----------|
| Images | 5 | 1 | 2 | 3 | $0.55 |
| Code | 6 | 1 | 3 | 2 | $0.12 |
| Text | 8 | 1 | 4 | 3 | $0.16 |
| UI/UX | 6 | 1 | 3 | 2 | $0.66 |
| Presentations | 5 | 1 | 2 | 2 | $0.80 |
| Websites | 6 | 1 | 3 | 2 | $0.18 |
| Infographics | 6 | 1 | 2 | 3 | $0.66 |
| Documents | 4 | 1 | 2 | 2 | $0.08 |
| Marketing | 10 | 1 | 3 | 5 | $0.20 |
| Data Viz | 5 | 1 | 2 | 2 | $0.15 |
| Architecture | 5 | 1 | 2 | 2 | $0.10 |

**Key insights:**
- **Images/Infographics**: Higher cost due to DALL-E 3
- **Marketing**: High population (10) for A/B testing, more auto-samples (5)
- **Text/Code**: Lower cost, use Claude API
- **Documents**: Lowest population (4) for focused formal content
- All default to **1 generation** (no evolution) for speed

**Example simple usage (uses defaults):**
```bash
/gen-asset "picture of cow"           # Images: 5 pop, 2 clusters, top 3
/gen-asset "blog post about AI"       # Text: 8 pop, 4 clusters, top 3
/gen-asset "investor pitch deck"      # Presentations: 5 pop, 2 clusters, top 2
```

**Override any defaults:**
```bash
/gen-asset "picture of cow" --generations=2 --population=8
# Overrides: generations=2, population=8
# Keeps: clusters=2, auto-sample=3 (from image defaults)
```

### Images

**Auto-detected keywords:** "image", "photo", "picture", "illustration", "logo", "icon", "diagram"

**Default provider:** `dalle3`

**Default genetic params:**
- `--population=5` (good variety without excessive cost)
- `--generations=1` (single generation, no evolution unless specified)
- `--clusters=2` (group into 2 style families)
- `--auto-sample=3` (auto-pick top 3)

**Default criteria:** `"aesthetics,creativity,prompt_alignment,technical_quality"`

**Default criteria weights:** `"aesthetics:0.35,creativity:0.30,prompt_alignment:0.25,technical_quality:0.10"`

**Default diversity:** `"style,color_palette,composition,mood,lighting,perspective"`

**Simple usage:**
```bash
/gen-asset "picture of cow"
# Auto-runs: population=5, generations=1, clusters=2, auto-sample=3
# Output: 5 cow images, 2 style clusters, top 3 auto-selected
```

**Advanced usage:**
```bash
/gen-asset "minimalist logo for AI company" --generations=2 --clusters=3
# Overrides: generations=2, clusters=3
# Keeps defaults: population=5, auto-sample=3
```

### Code

**Auto-detected keywords:** "function", "class", "algorithm", "script", "program", "implementation"

**Default provider:** `claude`

**Default genetic params:**
- `--population=6` (more diversity for algorithmic approaches)
- `--generations=1` (single generation default)
- `--clusters=3` (group by algorithm/pattern/paradigm)
- `--auto-sample=2` (top 2 implementations)

**Default criteria:** `"correctness,readability,efficiency,maintainability"`

**Default criteria weights:** `"correctness:0.40,readability:0.30,efficiency:0.20,maintainability:0.10"`

**Default diversity:** `"algorithm,pattern,paradigm,data_structure,style"`

**Simple usage:**
```bash
/gen-asset "Python function to merge sorted lists"
# Output: 6 implementations, 3 algorithmic approaches, top 2 auto-selected
```

**Advanced usage:**
```bash
/gen-asset "sort algorithm" --population=10 --generations=2 --diversity="algorithm,complexity"
```

### Text (Copy, Content, Blog Posts)

**Auto-detected keywords:** "copy", "content", "article", "description", "paragraph", "headline", "blog post", "essay", "newsletter"

**Default provider:** `claude`

**Default genetic params:**
- `--population=8` (high diversity for writing styles)
- `--generations=1` (single generation default)
- `--clusters=4` (group by tone/length/audience/formality)
- `--auto-sample=3` (top 3 variants)

**Default criteria:** `"clarity,persuasiveness,engagement,tone"`

**Default criteria weights:** `"clarity:0.30,persuasiveness:0.25,engagement:0.30,tone:0.15"`

**Default diversity:** `"tone,structure,vocabulary,length,style,formality,audience"`

**Simple usage:**
```bash
/gen-asset "blog post about AI trends in 2025"
# Output: 8 variants, 4 style clusters, top 3 auto-selected
```

**Advanced usage:**
```bash
/gen-asset "product description" --clusters=2 --diversity="tone,length"
```

### Design (UI/UX)

**Auto-detected keywords:** "design", "interface", "UI", "UX", "mockup", "wireframe", "layout"

**Default provider:** `dalle3` or `figma` (if available)

**Default criteria:** `"aesthetics,usability,innovation,brand_alignment"`

**Default diversity:** `"layout,color_scheme,typography,component_style,density"`

**Example:**
```bash
/gen-asset "mobile app login screen" --population=4 --generations=2 --clusters=2
```

### Presentations (PowerPoint, Slides)

**Auto-detected keywords:** "presentation", "powerpoint", "slides", "deck", "keynote", "pitch deck"

**Default provider:** `claude` (generates outline + content) + `dalle3` (visuals)

**Default genetic params:**
- `--population=5` (5 distinct presentation approaches)
- `--generations=1` (single generation default)
- `--clusters=2` (group by narrative style: data-driven vs story-driven)
- `--auto-sample=2` (top 2 decks)

**Default criteria:** `"clarity,visual_appeal,persuasiveness,flow"`

**Default criteria weights:** `"clarity:0.25,visual_appeal:0.25,persuasiveness:0.30,flow:0.20"`

**Default diversity:** `"structure,visual_style,narrative_arc,density,formality"`

**Simple usage:**
```bash
/gen-asset "investor pitch deck"
# Output: 5 PPTX files, 2 narrative styles, top 2 auto-selected
```

**Advanced usage:**
```bash
/gen-asset "quarterly business review" --population=4 --diversity="formality,density"
```

### Websites (Landing Pages, Full Sites)

**Auto-detected keywords:** "website", "landing page", "web page", "site", "homepage"

**Default provider:** `claude` (HTML/CSS/JS) or `dalle3` (mockups)

**Default genetic params:**
- `--population=6` (diverse layout approaches)
- `--generations=1` (single generation default)
- `--clusters=3` (group by layout paradigm: hero-centric, feature-grid, storytelling)
- `--auto-sample=2` (top 2 designs)

**Default criteria:** `"aesthetics,usability,conversion_potential,responsiveness"`

**Default criteria weights:** `"aesthetics:0.25,usability:0.25,conversion_potential:0.35,responsiveness:0.15"`

**Default diversity:** `"layout,color_scheme,content_structure,cta_placement,navigation"`

**Simple usage:**
```bash
/gen-asset "landing page for productivity SaaS"
# Output: 6 landing pages, 3 layout families, top 2 auto-selected
```

**Advanced usage:**
```bash
/gen-asset "homepage" --generations=2 --clusters=2
```

### Infographics

**Auto-detected keywords:** "infographic", "data visualization", "visual summary", "info viz"

**Default provider:** `dalle3` or `claude` (SVG generation)

**Default genetic params:**
- `--population=6` (diverse visualization approaches)
- `--generations=1` (single generation default)
- `--clusters=2` (group by density: minimal vs detailed)
- `--auto-sample=3` (top 3 infographics)

**Default criteria:** `"clarity,visual_appeal,information_density,accuracy"`

**Default criteria weights:** `"clarity:0.35,visual_appeal:0.30,information_density:0.20,accuracy:0.15"`

**Default diversity:** `"layout,color_scheme,chart_types,information_hierarchy,style"`

**Simple usage:**
```bash
/gen-asset "infographic comparing cloud providers"
# Output: 6 infographics, 2 density styles, top 3 auto-selected
```

**Advanced usage:**
```bash
/gen-asset "data viz quarterly metrics" --population=8 --clusters=3
```

### Documents (Reports, Whitepapers, PDFs)

**Auto-detected keywords:** "document", "report", "whitepaper", "PDF", "research paper", "case study"

**Default provider:** `claude`

**Default genetic params:**
- `--population=4` (focused approaches for formal docs)
- `--generations=1` (single generation default)
- `--clusters=2` (group by depth: executive-summary vs technical-deep-dive)
- `--auto-sample=2` (top 2 documents)

**Default criteria:** `"clarity,depth,professionalism,structure"`

**Default criteria weights:** `"clarity:0.30,depth:0.30,professionalism:0.25,structure:0.15"`

**Default diversity:** `"format,tone,structure,depth,visual_density"`

**Simple usage:**
```bash
/gen-asset "technical whitepaper on edge computing"
# Output: 4 whitepapers, 2 depth levels, top 2 auto-selected
```

**Advanced usage:**
```bash
/gen-asset "quarterly report" --population=3 --diversity="tone,visual_density"
```

### Marketing Materials (Ads, Social Posts, Email)

**Auto-detected keywords:** "ad", "advertisement", "social post", "email", "campaign", "marketing"

**Default provider:** `claude` (copy) + `dalle3` (visuals)

**Default genetic params:**
- `--population=10` (high diversity for A/B testing)
- `--generations=1` (single generation default)
- `--clusters=3` (group by tone: professional, casual, urgent)
- `--auto-sample=5` (top 5 for A/B testing)

**Default criteria:** `"engagement,clarity,call_to_action,brand_alignment"`

**Default criteria weights:** `"engagement:0.40,clarity:0.20,call_to_action:0.25,brand_alignment:0.15"`

**Default diversity:** `"tone,format,visual_style,length,platform_optimization"`

**Simple usage:**
```bash
/gen-asset "LinkedIn post announcing product launch"
# Output: 10 posts, 3 tonal groups, top 5 for A/B testing
```

**Advanced usage:**
```bash
/gen-asset "email campaign" --population=12 --auto-sample=6
```

### Data Visualizations (Charts, Graphs, Dashboards)

**Auto-detected keywords:** "chart", "graph", "dashboard", "visualization", "metrics", "analytics"

**Default provider:** `claude` (D3.js, Chart.js) or `dalle3` (mockups)

**Default genetic params:**
- `--population=5` (diverse chart approaches)
- `--generations=1` (single generation default)
- `--clusters=2` (group by complexity: simple vs detailed)
- `--auto-sample=2` (top 2 visualizations)

**Default criteria:** `"clarity,accuracy,visual_appeal,insight_delivery"`

**Default criteria weights:** `"clarity:0.35,accuracy:0.30,visual_appeal:0.20,insight_delivery:0.15"`

**Default diversity:** `"chart_type,color_scheme,layout,interactivity,detail_level"`

**Simple usage:**
```bash
/gen-asset "sales dashboard showing KPIs"
# Output: 5 dashboard designs, 2 complexity levels, top 2 auto-selected
```

**Advanced usage:**
```bash
/gen-asset "analytics chart" --population=6 --diversity="chart_type,interactivity"
```

### Architecture (System Design)

**Auto-detected keywords:** "architecture", "system design", "diagram", "infrastructure"

**Default provider:** `claude` (generates Mermaid/PlantUML)

**Default genetic params:**
- `--population=5` (diverse architectural approaches)
- `--generations=1` (single generation default)
- `--clusters=2` (group by pattern: monolith vs microservices, sync vs async)
- `--auto-sample=2` (top 2 architectures)

**Default criteria:** `"scalability,clarity,best_practices,completeness"`

**Default criteria weights:** `"scalability:0.35,clarity:0.25,best_practices:0.25,completeness:0.15"`

**Default diversity:** `"architecture_pattern,tech_stack,deployment,data_flow"`

**Simple usage:**
```bash
/gen-asset "microservices architecture for e-commerce"
# Output: 5 architecture diagrams, 2 patterns, top 2 auto-selected
```

**Advanced usage:**
```bash
/gen-asset "system design" --population=6 --diversity="tech_stack,deployment"
```

### Generic/Fallback (Unknown Type)

**When auto-detection fails:**
If the command can't determine asset type from keywords, it uses generic defaults and asks for confirmation.

**Default genetic params:**
- `--population=5` (balanced default)
- `--generations=1` (single generation)
- `--clusters=2` (basic clustering)
- `--auto-sample=2` (top 2)

**Default provider:** `claude`

**Default criteria:** `"quality,creativity,usefulness,clarity"`

**Default criteria weights:** `"quality:0.35,creativity:0.25,usefulness:0.25,clarity:0.15"`

**Default diversity:** `"approach,style,complexity,format"`

**Behavior:**
```bash
/gen-asset "something unusual"
# AI detects: Cannot determine asset type
# Prompts: "Detected generic content. Suggested type: text. Override with --type=?"
# Uses fallback defaults unless --type specified
```

**Manual type override:**
```bash
/gen-asset "something unusual" --type=image
# Forces image defaults instead of fallback
```

## Workflow

### Step 1: Parse & Validate Arguments

1. **Extract asset description** (required first argument)
2. **Parse all flags** with defaults:
   - `population`: Default 3
   - `generations`: Default 1
   - `clusters`: Default 1 (disabled)
   - `auto-sample`: Default disabled
   - `criteria`: Auto-detect from type
   - `weights`: Equal weights if not specified
   - `type`: Auto-detect from description
   - `provider`: Auto-select based on type
   - `output`: Auto-generate path
   - `diversity`: Type-specific defaults

3. **Validate combinations**:
   - `auto-sample` requires `criteria`
   - `weights` requires `criteria`
   - `clusters` must be ≤ `population`
   - `generations > 1` requires sufficient population
   - Warn if exponential growth is large (pop=5, gen=3 → 125 final)

4. **Display plan** before execution:
   ```
   🧬 Genetic Asset Generation Plan

   Asset: "minimalist logo for AI company"
   Type: image (auto-detected)
   Provider: dalle3

   Population: 5 variants per generation
   Generations: 2 (5 → 25 total candidates)
   Clustering: 3 groups by similarity
   Auto-sampling: Top 3 candidates

   Evaluation Criteria (weighted):
   - aesthetics: 0.4
   - creativity: 0.3
   - prompt_alignment: 0.2
   - technical_quality: 0.1

   Diversity Dimensions:
   - style (minimalist vs geometric vs abstract)
   - color_palette (monochrome vs accent vs gradient)
   - composition (centered vs asymmetric vs layered)

   Estimated cost: ~$2.50 (25 DALL-E 3 generations)
   Estimated time: ~3-5 minutes

   Proceed? (y/n)
   ```

### Step 2: Generation 1 - Create Population

5. **Generate diversity matrix**:
   - Create `population` × `diversity_dimensions` matrix
   - Maximize Hamming distance between variants
   - Document diversity profile per variant

   **Example (population=5, type=image):**
   ```
   | Variant | Style        | Color Palette | Composition | Mood      | Lighting  |
   |---------|-------------|---------------|-------------|-----------|-----------|
   | A       | Minimalist  | Monochrome    | Centered    | Calm      | Soft      |
   | B       | Geometric   | Accent color  | Asymmetric  | Dynamic   | Dramatic  |
   | C       | Abstract    | Gradient      | Layered     | Mysterious| Ambient   |
   | D       | Line art    | Colorful      | Grid-based  | Playful   | Bright    |
   | E       | Organic     | Earth tones   | Flowing     | Natural   | Warm      |
   ```

6. **Generate all G1 variants in parallel**:
   - Create detailed prompts incorporating diversity dimensions
   - Use Task tool to parallelize generation
   - Save each variant with metadata

   **Variant A prompt:**
   ```
   minimalist logo for AI company
   Style: Clean minimalist design with simple shapes
   Color: Monochrome (black/white or single color)
   Composition: Centered, balanced symmetry
   Mood: Calm, professional, trustworthy
   Lighting: Soft, even lighting
   ```

7. **Save Generation 1 outputs with complete metadata**:
   ```
   generated-assets/2025-11-14-ai-logo/
   ├── generation-1/
   │   ├── variant-A.png
   │   ├── variant-A.metadata.json
   │   ├── variant-B.png
   │   ├── variant-B.metadata.json
   │   ├── variant-C.png
   │   ├── variant-C.metadata.json
   │   ├── variant-D.png
   │   ├── variant-D.metadata.json
   │   ├── variant-E.png
   │   └── variant-E.metadata.json
   ├── GENERATION_PLAN.md
   └── README.md
   ```

   **Metadata JSON format (CRITICAL - tracks full lineage):**
   ```json
   {
     "variant_id": "variant-A",
     "generation": 1,
     "timestamp": "2025-11-14T10:23:45Z",
     "asset_description": "minimalist logo for AI company",
     "asset_type": "image",
     "provider": "dalle3",

     "lineage": {
       "parent": null,
       "breeding_strategy": null,
       "mutations": [],
       "crossover_parents": []
     },

     "diversity_profile": {
       "style": "Minimalist",
       "color_palette": "Monochrome",
       "composition": "Centered",
       "mood": "Calm",
       "lighting": "Soft",
       "perspective": "Flat"
     },

     "prompt": {
       "user_input": "minimalist logo for AI company",
       "enhanced_prompt": "minimalist logo for AI company. Style: Clean minimalist design with simple shapes. Color: Monochrome (black/white or single color). Composition: Centered, balanced symmetry. Mood: Calm, professional, trustworthy. Lighting: Soft, even lighting.",
       "negative_prompt": null
     },

     "evaluation": {
       "criteria_scores": {
         "aesthetics": 8.0,
         "creativity": 6.0,
         "prompt_alignment": 9.0,
         "technical_quality": 7.0
       },
       "weighted_score": 7.5,
       "ranking": 2,
       "rationale": "Strong aesthetics and prompt alignment, professional feel. Lower creativity due to conventional approach."
     },

     "cluster": {
       "cluster_id": 1,
       "cluster_name": "Minimalist Clean",
       "similarity_score": 0.85,
       "cluster_representative": false
     },

     "generation_info": {
       "population_size": 5,
       "generation_number": 1,
       "total_generations_planned": 2,
       "breeding_enabled": true,
       "selected_for_breeding": true,
       "num_children_bred": 5
     },

     "technical_metadata": {
       "file_format": "PNG",
       "resolution": "1024x1024",
       "file_size_bytes": 245678,
       "color_mode": "RGBA",
       "generation_time_seconds": 13.2,
       "cost_usd": 0.11
     },

     "children": [
       "variant-A1-a",
       "variant-A1-b",
       "variant-A1-c",
       "variant-A2-a",
       "variant-A2-b"
     ]
   }
   ```

   **For Generation 2+ variants, lineage tracking:**
   ```json
   {
     "variant_id": "variant-C2-a",
     "generation": 2,
     "timestamp": "2025-11-14T10:28:12Z",

     "lineage": {
       "parent": "variant-C",
       "parent_score": 8.2,
       "breeding_strategy": "mutation",
       "mutation_dimensions": ["style"],
       "mutation_details": {
         "style": {
           "from": "Abstract fluid",
           "to": "Abstract geometric fractals",
           "rationale": "Explore more structured abstract approach"
         }
       },
       "crossover_parents": null,
       "inheritance": {
         "from_parent_c": ["color_palette", "composition", "mood"],
         "mutated": ["style"],
         "preserved_score_components": ["aesthetics", "prompt_alignment"]
       }
     },

     "diversity_profile": {
       "style": "Abstract geometric fractals",
       "color_palette": "Gradient (blue→purple)",
       "composition": "Layered",
       "mood": "Mysterious",
       "lighting": "Ambient",
       "perspective": "Isometric"
     },

     "evaluation": {
       "criteria_scores": {
         "aesthetics": 9.5,
         "creativity": 9.0,
         "prompt_alignment": 8.5,
         "technical_quality": 9.0
       },
       "weighted_score": 9.1,
       "improvement_from_parent": 0.9,
       "ranking": 1,
       "rationale": "Exceptional aesthetic appeal with fractal geometry. Breakthrough in combining minimalist principles with creative geometric patterns."
     },

     "breeding_comparison": {
       "siblings": ["variant-C1-a", "variant-C1-b", "variant-C1-c", "variant-C2-b"],
       "best_in_lineage": true,
       "parent_rank": 1,
       "self_rank": 1
     },

     "children": []
   }
   ```

   **For crossover variants:**
   ```json
   {
     "variant_id": "variant-AC-hybrid",
     "generation": 2,

     "lineage": {
       "parent": null,
       "breeding_strategy": "crossover",
       "mutation_dimensions": [],
       "crossover_parents": ["variant-A", "variant-C"],
       "inheritance": {
         "from_parent_a": ["composition", "mood", "lighting"],
         "from_parent_c": ["style", "color_palette"],
         "mutation": ["perspective"]
       },
       "crossover_details": {
         "rationale": "Combine A's professional centered composition with C's creative abstract style",
         "expected_strengths": ["aesthetics", "prompt_alignment"],
         "expected_risks": ["May dilute both parent strengths"]
       }
     }
   }
   ```

### Step 3: Evaluation (if generations > 1 or auto-sample)

8. **Score each variant** using criteria:

   **For images:** Use Claude vision to score
   ```
   Analyze this image and rate on:
   - Aesthetics (0-10): Visual appeal, composition quality
   - Creativity (0-10): Uniqueness, innovation
   - Prompt alignment (0-10): How well it matches description
   - Technical quality (0-10): Resolution, artifacts, clarity

   Return JSON: {"scores": {...}, "rationale": "..."}
   ```

   **For code:** Use execution + static analysis
   ```
   - Correctness: Run tests, check edge cases
   - Readability: Analyze complexity, naming, comments
   - Efficiency: Benchmark performance
   - Maintainability: Check modularity, coupling
   ```

   **For text:** Use LLM evaluation
   ```
   Rate this copy on:
   - Clarity: Easy to understand, well-structured
   - Persuasiveness: Compelling, convincing
   - Engagement: Interesting, captivating
   - Tone: Appropriate for audience
   ```

9. **Calculate weighted scores**:
   ```
   Weighted Score = Σ(criterion_score × criterion_weight)

   Example:
   Variant A:
   - aesthetics: 8 × 0.4 = 3.2
   - creativity: 6 × 0.3 = 1.8
   - prompt_alignment: 9 × 0.2 = 1.8
   - technical_quality: 7 × 0.1 = 0.7
   Total: 7.5/10
   ```

10. **Rank variants** by weighted score:
    ```
    Ranking (Generation 1):
    1. Variant C: 8.2/10
    2. Variant A: 7.5/10
    3. Variant E: 7.1/10
    4. Variant B: 6.8/10
    5. Variant D: 6.3/10
    ```

11. **Save evaluation**:
    ```
    generation-1/EVALUATION.md
    - Scoring table
    - Ranking
    - Rationales per variant
    - Criteria weights used
    ```

### Step 4: Clustering (if clusters > 1)

12. **Calculate similarity matrix**:
    - Extract features from each asset
    - Compute pairwise similarity scores
    - Use clustering algorithm (K-means, hierarchical)

    **For images:** Use CLIP embeddings or visual features
    **For text:** Use semantic embeddings (sentence transformers)
    **For code:** Use AST similarity + semantic embeddings

13. **Group into N clusters**:
    ```
    Cluster 1 (Minimalist Family):
    - Variant A: Monochrome minimalist
    - Variant D: Line art minimal
    Score range: 7.5-6.3, Avg: 6.9

    Cluster 2 (Geometric Bold):
    - Variant B: Geometric accent
    Score range: 6.8, Avg: 6.8

    Cluster 3 (Organic/Abstract):
    - Variant C: Abstract gradient
    - Variant E: Organic earth tones
    Score range: 8.2-7.1, Avg: 7.65
    ```

14. **Save cluster analysis**:
    ```
    generation-1/CLUSTERS.md
    - Cluster definitions
    - Members per cluster
    - Cluster characteristics
    - Representative (best) from each cluster
    ```

### Step 5: Auto-Sampling (if enabled)

15. **Select top N candidates**:
    - Sort by weighted score
    - Select top `auto-sample` count
    - Document selection rationale

    ```
    Auto-Sample Results (Top 3):

    🥇 Variant C (8.2/10) - Abstract gradient
    Rationale: Highest creativity and aesthetics, excellent prompt alignment

    🥈 Variant A (7.5/10) - Monochrome minimalist
    Rationale: Strong aesthetics and prompt alignment, professional feel

    🥉 Variant E (7.1/10) - Organic earth tones
    Rationale: Good balance across all criteria, approachable style
    ```

16. **Save auto-sample results**:
    ```
    generation-1/AUTO_SAMPLE.md
    generation-1/top-picks/
    ├── 1-variant-C.png
    ├── 2-variant-A.png
    └── 3-variant-E.png
    ```

### Step 6: Breeding (if generations > 1)

17. **Select parents for breeding**:
    - Default: Top 50% of population (by weighted score)
    - Minimum: Top 2 if population is small
    - Document parent selection

    ```
    Selected Parents (Generation 1):
    1. Variant C (8.2/10) → Will breed 5 children
    2. Variant A (7.5/10) → Will breed 5 children
    3. Variant E (7.1/10) → Will breed 5 children

    Total Generation 2 candidates: 15
    ```

18. **Generate breeding strategies** for each parent:
    - Each parent breeds `population` children
    - Strategies: Mutation (60%), Crossover (30%), Hybrid (10%)

    **Parent C children (Abstract gradient):**
    ```
    C1: Pure mutation - Color palette
       From: Gradient (blue→purple)
       To: Gradient (warm sunset colors)

    C2: Pure mutation - Style
       From: Abstract fluid
       To: Abstract geometric fractals

    C3: Crossover with A - Composition
       Take: C's abstract style + A's centered composition

    C4: Mutation - Mood
       From: Mysterious
       To: Energetic, vibrant

    C5: Hybrid (Crossover C×E + Mutate lighting)
       Take: C's abstract + E's organic elements + bright lighting
    ```

19. **Document breeding plan**:
    ```
    generation-1/BREEDING_PLAN.md
    - Parent selection rationale
    - Breeding strategies per parent
    - Expected diversity in G2
    - Mutation/crossover details
    ```

### Step 7: Generation 2+ (if generations > 1)

20. **Generate all G2 variants in parallel**:
    - Create prompts incorporating parent traits + mutations
    - Track lineage (parent → child)
    - Save with generation metadata

21. **Repeat evaluation** (Step 3):
    - Score all G2 variants
    - Rank within generation
    - Compare to G1 (track improvement)

22. **Repeat clustering** (Step 4 if enabled):
    - Cluster G2 variants
    - Identify emerging patterns
    - Track cluster evolution from G1

23. **Repeat breeding** (if generations > 2):
    - Select G2 parents
    - Generate G3
    - Continue until final generation

24. **Save generational data**:
    ```
    generated-assets/2025-11-14-ai-logo/
    ├── generation-1/ (5 variants)
    ├── generation-2/ (15 variants)
    ├── generation-3/ (45 variants if gen=3)
    ├── GENERATIONAL_ANALYSIS.md
    └── LINEAGE_TREE.md (parent-child relationships)
    ```

### Step 8: Final Selection & Report

25. **Identify overall winners**:
    - Rank ALL variants across ALL generations
    - Identify top candidates
    - Document generational improvements

    ```
    🏆 Overall Winners (Across All Generations)

    1. Variant C2-a (9.1/10) - Gen 2, Parent C
       Abstract geometric fractals with gradient
       Improvement from G1: +0.9 points

    2. Variant C1-c (8.8/10) - Gen 2, Parent C
       Sunset gradient abstract
       Improvement from G1: +0.6 points

    3. Variant C (8.2/10) - Gen 1
       Original abstract gradient (parent of winners)
    ```

26. **Create final cluster analysis** (if enabled):
    - Cluster across ALL generations
    - Show cluster evolution
    - Identify dominant styles

    ```
    Final Clusters (3 clusters, 65 total variants):

    Cluster 1: Minimalist Clean (18 variants)
    - Best: Variant A3-b (8.5/10)
    - Characteristics: Simple, monochrome, centered
    - Evolution: G1→G2→G3 showed refinement in balance

    Cluster 2: Abstract Bold (31 variants) ⭐ DOMINANT
    - Best: Variant C2-a (9.1/10)
    - Characteristics: Gradients, geometric, dynamic
    - Evolution: G1→G2 introduced fractals, major improvement

    Cluster 3: Organic Natural (16 variants)
    - Best: Variant E2-a (8.0/10)
    - Characteristics: Flowing, earth tones, warm
    - Evolution: Stable across generations
    ```

27. **Generate comprehensive report**:
    ```markdown
    # Genetic Asset Generation Report

    ## Summary

    **Asset:** Minimalist logo for AI company
    **Type:** Image
    **Provider:** DALL-E 3

    **Parameters:**
    - Population: 5 per generation
    - Generations: 2 (5 → 15 total)
    - Clusters: 3
    - Auto-sample: Top 3

    **Results:**
    - Total variants: 20
    - Best score: 9.1/10 (Variant C2-a)
    - Average improvement G1→G2: +0.7 points
    - Dominant cluster: Abstract Bold (55% of variants)

    ## Top Recommendations

    ### 🥇 Variant C2-a (9.1/10)
    ![C2-a](generation-2/variant-C2-a.png)

    **Lineage:** Gen 2, Parent C (Abstract gradient)
    **Strategy:** Pure mutation - Style dimension
    **Mutation:** Abstract fluid → Abstract geometric fractals

    **Scores:**
    - Aesthetics: 9.5/10 (Weight: 0.4) = 3.8
    - Creativity: 9.0/10 (Weight: 0.3) = 2.7
    - Prompt alignment: 8.5/10 (Weight: 0.2) = 1.7
    - Technical quality: 9.0/10 (Weight: 0.1) = 0.9
    **Weighted Total: 9.1/10**

    **Why it won:**
    - Exceptional aesthetic appeal with fractal geometry
    - Highly creative while maintaining minimalist principles
    - Strong brand potential for AI company
    - Professional and modern

    **Cluster:** Abstract Bold (representative)

    ---

    ### 🥈 Variant C1-c (8.8/10)
    ![C1-c](generation-2/variant-C1-c.png)

    **Lineage:** Gen 2, Parent C
    **Strategy:** Pure mutation - Color palette
    **Mutation:** Blue→purple gradient → Warm sunset gradient

    **Scores:**
    - Aesthetics: 9.0/10 = 3.6
    - Creativity: 8.5/10 = 2.55
    - Prompt alignment: 8.0/10 = 1.6
    - Technical quality: 9.5/10 = 0.95
    **Weighted Total: 8.8/10**

    **Why it's strong:**
    - Warm, approachable color palette
    - Excellent technical execution
    - Unique among tech logos

    **Cluster:** Abstract Bold

    ---

    ### 🥉 Variant C (8.2/10) - Original
    ![C](generation-1/variant-C.png)

    **Lineage:** Gen 1 (parent of winners)
    **Strategy:** Original high-diversity variant

    **Why it matters:**
    - Best of Generation 1
    - Parent of top 2 winners
    - Validates genetic breeding approach

    **Cluster:** Abstract Bold (founder)

    ---

    ## Cluster Analysis

    ### Abstract Bold (31 variants, 55%)
    **Representative:** Variant C2-a (9.1/10)
    **Score range:** 6.5-9.1, Average: 7.8

    **Characteristics:**
    - Gradient color schemes
    - Geometric or abstract shapes
    - Dynamic, modern feel
    - High creativity scores

    **Evolution:**
    - G1: 2 variants (C, B)
    - G2: 10 variants (C bred 5, B bred 5)
    - G3: 19 variants (top breeders from G2)
    - **Key insight:** Geometric mutation (C→C2) was breakthrough

    ---

    ### Minimalist Clean (18 variants, 32%)
    **Representative:** Variant A3-b (8.5/10)
    **Score range:** 6.3-8.5, Average: 7.2

    **Characteristics:**
    - Monochrome or limited color
    - Simple shapes, centered
    - Professional, trustworthy
    - High prompt alignment

    **Evolution:**
    - G1: 2 variants (A, D)
    - G2: 6 variants
    - G3: 10 variants
    - **Key insight:** Consistent performance, incremental improvements

    ---

    ### Organic Natural (16 variants, 28%)
    **Representative:** Variant E2-a (8.0/10)
    **Score range:** 6.8-8.0, Average: 7.3

    **Characteristics:**
    - Earth tones, warm colors
    - Flowing, organic shapes
    - Natural, approachable
    - Good balance across criteria

    **Evolution:**
    - G1: 1 variant (E)
    - G2: 5 variants
    - G3: 10 variants
    - **Key insight:** Stable performer, niche appeal

    ---

    ## Generational Insights

    ### Generation 1 (5 variants)
    - Highest: Variant C (8.2/10)
    - Average: 7.2/10
    - Diversity: Excellent (5 distinct styles)

    ### Generation 2 (15 variants)
    - Highest: Variant C2-a (9.1/10)
    - Average: 7.9/10 (+0.7 from G1)
    - Breakthrough: Geometric mutation from Abstract parent

    ### Key Findings

    1. **Geometric mutation was breakthrough**
       - C → C2-a: +0.9 points
       - Fractals added creativity without sacrificing aesthetics

    2. **Abstract Bold cluster dominated**
       - 55% of all variants
       - Highest scores on average
       - Most successful breeding lineage

    3. **Crossover showed mixed results**
       - Some successful (A×C hybrids)
       - Others diluted strengths
       - Pure mutations outperformed in this case

    4. **Color palette mutations were effective**
       - C1-c sunset variant scored 8.8/10
       - Warm colors differentiated from typical tech logos

    5. **Minimalist cluster was stable**
       - Consistent mid-high scores
       - Less variance than Abstract
       - Safe choice for conservative brands

    ---

    ## Cost & Performance

    **Total cost:** $2.20 (20 DALL-E 3 HD generations @ $0.11 each)
    **Total time:** 4 minutes 23 seconds
    **Variants generated:** 20
    **Cost per variant:** $0.11
    **Time per variant:** 13 seconds average

    **Evaluation:**
    - Claude vision API calls: 20 × $0.01 = $0.20
    - Clustering computation: <1 second (local)
    - Total cost: $2.40

    ---

    ## Recommendations

    ### For this project:

    **Best overall:** Variant C2-a (9.1/10)
    - Modern, creative, professional
    - Strong brand potential for AI company
    - Abstract geometric fractals convey intelligence

    **Best if conservative brand:** Variant A3-b (8.5/10)
    - Clean, trustworthy, professional
    - Monochrome works across mediums
    - Safe choice, widely appealing

    **Best for differentiation:** Variant C1-c (8.8/10)
    - Warm colors unusual for AI/tech
    - Approachable, human-centered feel
    - Stands out in crowded market

    ### For future genetic runs:

    1. **Abstract Bold cluster is promising**
       - Consider running dedicated evolution with this style
       - Explore more geometric variations
       - Try additional color palettes

    2. **Increase population in successful clusters**
       - G3 could focus on Abstract Bold only
       - Run population=10 within that cluster
       - Depth-first instead of breadth-first

    3. **Mutation > Crossover for this asset type**
       - Pure mutations had higher success rate
       - Consider 80% mutation, 20% crossover ratio
       - Crossover works better with closer parents

    4. **Color palette is high-impact dimension**
       - Small changes = big perception shifts
       - Worth dedicating mutations to color alone
       - Try palette-focused evolution

    ---

    ## Files Generated

    ```
    generated-assets/2025-11-14-ai-logo/
    ├── README.md (this file)
    ├── GENERATION_PLAN.md
    ├── GENERATIONAL_ANALYSIS.md
    ├── LINEAGE_TREE.md
    ├── generation-1/
    │   ├── variant-A.png + metadata.json
    │   ├── variant-B.png + metadata.json
    │   ├── variant-C.png + metadata.json ⭐
    │   ├── variant-D.png + metadata.json
    │   ├── variant-E.png + metadata.json
    │   ├── EVALUATION.md
    │   ├── CLUSTERS.md
    │   ├── BREEDING_PLAN.md
    │   └── AUTO_SAMPLE.md
    ├── generation-2/
    │   ├── variant-C1-a.png + metadata.json
    │   ├── variant-C1-b.png + metadata.json
    │   ├── variant-C1-c.png + metadata.json 🥈
    │   ├── variant-C2-a.png + metadata.json 🥇
    │   ├── variant-C2-b.png + metadata.json
    │   ├── [... 10 more variants]
    │   ├── EVALUATION.md
    │   └── CLUSTERS.md
    ├── top-picks/
    │   ├── 1-variant-C2-a.png 🥇
    │   ├── 2-variant-C1-c.png 🥈
    │   └── 3-variant-C.png 🥉
    └── clusters/
        ├── cluster-1-abstract-bold/ (31 variants)
        ├── cluster-2-minimalist-clean/ (18 variants)
        └── cluster-3-organic-natural/ (16 variants)
    ```

    ---

    ## Next Steps

    1. **Review top picks** in `top-picks/` directory
    2. **Explore clusters** to see style families
    3. **Check lineage** in LINEAGE_TREE.md to understand evolution
    4. **Refine winner** (optional):
       ```bash
       /gen-asset "geometric fractal logo based on C2-a" --population=5 --iterations=1
       ```
    5. **Export for design tools** (SVG conversion, sizing, etc.)

    ---

    🎉 **Genetic generation complete!**
    ```

28. **Create visual outputs**:
    - `top-picks/` directory with best N
    - `clusters/` directory with grouped variants
    - `lineage-tree.html` with interactive visualization
    - Comparison grids (side-by-side images)

### Step 9: Interactive Review (Web-Compatible)

29. **Generate review interface** (single HTML file):
    ```html
    <!DOCTYPE html>
    <html>
    <head>
      <title>Asset Generation Review</title>
      <style>
        /* Grid layout, filtering, sorting */
      </style>
    </head>
    <body>
      <h1>Review: Minimalist AI Logo (20 variants)</h1>

      <div class="controls">
        <button onclick="filterCluster(1)">Cluster 1: Abstract Bold</button>
        <button onclick="filterCluster(2)">Cluster 2: Minimalist</button>
        <button onclick="filterCluster(3)">Cluster 3: Organic</button>
        <button onclick="sortBy('score')">Sort by Score</button>
        <button onclick="sortBy('generation')">Sort by Generation</button>
      </div>

      <div class="grid">
        <!-- All variants in responsive grid -->
        <!-- Click to expand, view metadata -->
      </div>

      <script>
        // Filtering, sorting, comparison logic
      </script>
    </body>
    </html>
    ```

30. **Display summary** to user:
    ```
    ✅ Genetic Asset Generation Complete!

    Asset: "minimalist logo for AI company"
    Variants generated: 20 (5 per generation × 2 generations)

    🏆 Top Pick: Variant C2-a (9.1/10)
    📁 Output: generated-assets/2025-11-14-ai-logo/

    📊 Results:
    - Best score: 9.1/10 (Variant C2-a)
    - Average: 7.9/10
    - Clusters: 3 identified
    - Dominant cluster: Abstract Bold (55%)

    💰 Cost: $2.40 total
    ⏱️  Time: 4m 23s

    📂 Files:
    - top-picks/ → 3 best variants
    - clusters/ → 3 style families
    - generation-1/ → 5 G1 variants
    - generation-2/ → 15 G2 variants
    - README.md → Full report
    - review.html → Interactive viewer

    🔍 Next:
    - Open review.html to compare all variants
    - Check top-picks/ for winners
    - Read README.md for detailed analysis

    Want to evolve further?
    /gen-asset "refine variant C2-a" --population=5 --based-on=C2-a
    ```

## Advanced Features

### Diversity Optimization

**Hamming Distance Maximization:**
- Calculate diversity score between all variant pairs
- Ensure minimum distance threshold
- Reject variants too similar to existing

**Example diversity matrix (population=5):**
```
        A    B    C    D    E
    A   -   0.8  0.6  0.7  0.5
    B  0.8   -   0.9  0.6  0.7
    C  0.6  0.9   -   0.8  0.4
    D  0.7  0.6  0.8   -   0.6
    E  0.5  0.7  0.4  0.6   -

Min distance: 0.4 (C-E)
Avg distance: 0.67
Status: ✅ Good diversity (threshold: 0.5)
```

### Adaptive Criteria Weights

**Learn from user preferences:**
- Track which variants user selects
- Adjust criteria weights based on selections
- Personalize future generations

```
User selected: C2-a (creativity=9), C1-c (aesthetics=9)
User skipped: A3-b (creativity=6), D2-a (aesthetics=6)

Insight: User values creativity > prompt_alignment
Adjusted weights:
- creativity: 0.3 → 0.45 (+50%)
- prompt_alignment: 0.2 → 0.15 (-25%)
```

### Smart Mutations

**Context-aware mutations:**
- Analyze which mutations succeeded in previous generations
- Weight mutation strategies by historical success
- Avoid mutations that consistently fail

```
Mutation Success Analysis (After G2):

Color palette mutations: 80% success rate
- 4/5 improved scores
- Average gain: +0.6 points
- Recommendation: Increase mutation rate

Style mutations: 60% success rate
- 3/5 improved scores
- Average gain: +0.3 points
- Recommendation: Continue current rate

Composition mutations: 20% success rate
- 1/5 improved scores
- Average loss: -0.2 points
- Recommendation: Decrease or skip

Strategy for G3: Focus on color+style, skip composition
```

### Ensemble Voting

**Multi-model evaluation:**
- Use multiple LLMs to score variants
- Aggregate scores (average, weighted, etc.)
- Reduce single-model bias

```
Variant C2-a scores:

Claude (vision):
- Aesthetics: 9.5
- Creativity: 9.0
- Overall: 9.1

GPT-4V (vision):
- Aesthetics: 9.0
- Creativity: 9.5
- Overall: 9.2

Gemini (vision):
- Aesthetics: 9.5
- Creativity: 8.5
- Overall: 8.9

Ensemble (average): 9.1
Confidence: High (low variance)
```

### Batch Operations

**Generate multiple assets in one run:**
```bash
/gen-asset "logo,icon,banner" --population=3 --batch
# Generates 3 assets × 3 variants each = 9 total
```

### Constraint-Based Generation

**Apply hard constraints:**
```bash
/gen-asset "logo" --population=5 --constraints="monochrome,square,simple_shapes"
# All variants MUST satisfy constraints
# Reject any that violate
```

## Provider-Specific Features

### DALL-E 3
- Automatic prompt enhancement
- HD quality (1024×1024, 1792×1024)
- Style: natural, vivid

### Midjourney (via API)
- Aspect ratios (--ar 16:9)
- Stylize parameter (--s 0-1000)
- Chaos for variety (--c 0-100)
- Version selection (--v 6)

### Stable Diffusion
- Negative prompts
- CFG scale control
- Sampling methods
- LoRA models

### Claude (text/code)
- Streaming for long generations
- Artifacts for code
- Multi-turn refinement

## Error Handling

**Provider failures:**
```
⚠️  Warning: DALL-E 3 API error for variant C
Retrying with exponential backoff...
Retry 1/3... ✅ Success

If all retries fail:
- Skip variant, continue with others
- Document failure in metadata
- Suggest rerun for failed variants
```

**Insufficient budget:**
```
❌ Error: Estimated cost ($12.50) exceeds budget
Current parameters: population=10, generations=4 → 10,000 variants

Suggestions:
1. Reduce generations: --generations=2 → 100 variants ($1.10)
2. Reduce population: --population=5 → 625 variants ($6.88)
3. Enable auto-sample earlier: --auto-sample=3 --early-prune

Adjust parameters and retry.
```

**Clustering failure:**
```
⚠️  Warning: Unable to cluster (too few variants)
Need at least 2× cluster count variants
Current: 5 variants, requested: 3 clusters

Solution: Skipping clustering, showing all variants
Tip: Use --clusters=2 or increase --population
```

## Usage Examples

### Example 1: Simple Image Generation
```bash
/gen-asset "sunset over mountains" --population=5

# Output: 5 diverse image variants, no evolution
```

### Example 2: Code with Auto-Sampling
```bash
/gen-asset "Python function to validate email addresses" \
  --population=8 \
  --auto-sample=3 \
  --criteria="correctness,readability,robustness"

# Output: 8 variants generated, top 3 auto-selected by criteria
```

### Example 3: Multi-Generation Evolution
```bash
/gen-asset "modern UI design for login page" \
  --population=5 \
  --generations=3 \
  --clusters=3 \
  --criteria="aesthetics,usability,innovation"

# Output: 5→25→125 variants, clustered into 3 families
```

### Example 4: Text Copy with Clustering
```bash
/gen-asset "email subject line for product launch" \
  --population=10 \
  --clusters=3 \
  --diversity="tone,length,urgency"

# Output: 10 subject lines grouped into 3 tonal clusters
```

### Example 5: Architecture Diagrams
```bash
/gen-asset "microservices architecture for social media app" \
  --type=architecture \
  --population=5 \
  --auto-sample=2 \
  --criteria="scalability,clarity,best_practices"

# Output: 5 architecture diagrams (Mermaid), top 2 selected
```

### Example 6: Full Genetic Evolution
```bash
/gen-asset "brand identity system (logo, colors, typography)" \
  --population=5 \
  --generations=3 \
  --clusters=4 \
  --auto-sample=3 \
  --criteria="brand_coherence,aesthetics,versatility,uniqueness" \
  --weights="brand_coherence:0.35,aesthetics:0.30,versatility:0.20,uniqueness:0.15" \
  --diversity="style,color_palette,typography,mood,formality"

# Output: Comprehensive brand evolution with top 3 coherent systems
```

### Example 7: PowerPoint Presentation
```bash
/gen-asset "investor pitch deck for Series A fundraise" \
  --population=5 \
  --clusters=2 \
  --diversity="narrative_arc,visual_style,formality" \
  --auto-sample=2

# Output: 5 PPTX files, clustered by presentation style, top 2 auto-selected
# Each variant has different narrative structure and visual design
```

### Example 8: Website Landing Page
```bash
/gen-asset "landing page for AI meeting assistant SaaS" \
  --population=6 \
  --generations=2 \
  --clusters=3 \
  --criteria="aesthetics,conversion_potential,clarity,mobile_responsiveness" \
  --diversity="layout,cta_placement,color_scheme,content_hierarchy"

# Output: 6 initial + evolved variants, 3 layout families
# HTML/CSS/JS files ready to deploy
```

### Example 9: Infographic
```bash
/gen-asset "infographic comparing AI development frameworks" \
  --population=8 \
  --clusters=2 \
  --diversity="layout,chart_types,information_hierarchy,color_scheme" \
  --auto-sample=3

# Output: 8 infographic variants, 2 style clusters, top 3 selected
# PNG/SVG files with full metadata
```

### Example 10: Blog Post Content
```bash
/gen-asset "blog post: How to scale ML infrastructure for startups" \
  --population=10 \
  --clusters=4 \
  --diversity="tone,length,depth,audience,structure" \
  --criteria="engagement,clarity,technical_accuracy,actionability" \
  --auto-sample=3

# Output: 10 blog post variants in Markdown
# Clustered by: Technical Deep-Dive, Beginner-Friendly, Executive Summary, Tutorial
# Top 3 auto-selected by criteria
```

## Metadata Querying & Lineage Analysis

### Query Metadata
Every asset includes `.metadata.json` with complete lineage tracking. Use these to analyze evolution:

```bash
# Find all descendants of a winning variant
jq '.lineage.parent == "variant-C"' generation-2/*.metadata.json

# Find breakthrough mutations (score improvement > 0.5)
jq 'select(.evaluation.improvement_from_parent > 0.5)' generation-*/*.metadata.json

# Trace lineage tree from winner back to root
jq -r '.lineage | .parent, .crossover_parents[]?' variant-C2-a.metadata.json

# Find all variants in a cluster
jq 'select(.cluster.cluster_id == 2)' generation-*/*.metadata.json

# Calculate ROI: best score per dollar spent
jq '[.evaluation.weighted_score, .technical_metadata.cost_usd] | .[0]/.[1]' *.metadata.json
```

### Lineage Tree Visualization
Generate visual lineage tree from metadata:

```bash
# The command auto-generates lineage-tree.html
# Shows parent→child relationships, scores, mutations
# Interactive: click to view variant, filter by cluster
```

**Example lineage tree:**
```
Generation 1
├─ variant-A (7.5) ──┬─→ variant-A1-a (7.8) mutation:color
│                    ├─→ variant-A1-b (7.2) mutation:composition
│                    └─→ variant-A2-a (8.0) crossover:A×C
├─ variant-B (6.8) ──┴─→ [not selected for breeding]
├─ variant-C (8.2) ──┬─→ variant-C1-a (8.5) mutation:lighting
│                    ├─→ variant-C1-c (8.8) mutation:color_palette ⭐
│                    └─→ variant-C2-a (9.1) mutation:style 🏆
└─ variant-E (7.1) ──┴─→ variant-E1-a (7.4) mutation:mood

Legend:
🏆 Overall winner
⭐ Top 3
```

### Analyze Successful Mutations
Use metadata to identify which mutations work:

```bash
# Find most successful mutation dimension
jq -r '.lineage.mutation_dimensions[]' generation-2/*.metadata.json | sort | uniq -c | sort -rn

# Output:
# 12 color_palette
#  8 style
#  5 composition
#  3 lighting
# → Color palette mutations are most common

# Find mutation dimension with highest avg score improvement
for dim in style color_palette composition lighting; do
  echo "$dim: $(jq "select(.lineage.mutation_dimensions[] == \"$dim\") | .evaluation.improvement_from_parent" generation-2/*.metadata.json | jq -s 'add/length')"
done

# Output:
# style: 0.85
# color_palette: 0.55
# composition: -0.15
# lighting: 0.30
# → Style mutations yield biggest improvements
```

## Integration with Other Commands

### Refine Winners
```bash
# Generate initial variants
/gen-asset "hero image for landing page" --population=5 --auto-sample=1

# Refine the winner
/gen-asset "refine hero image with more contrast" \
  --based-on=generated-assets/2025-11-14-hero/top-picks/1-variant-C.png \
  --population=5
```

### Visualize Results
```bash
# Generate architecture
/gen-asset "system architecture" --type=architecture --population=5

# Visualize the winner
/visualize generated-assets/.../top-picks/1-variant-A.md --architecture
```

### Polish Code Outputs
```bash
# Generate code
/gen-asset "React component for data table" --population=5 --auto-sample=1

# Polish the result
/polish generated-assets/.../top-picks/1-variant-C/DataTable.tsx
```

### Generate Presentation from Winners
```bash
# Generate multiple assets
/gen-asset "logo for startup" --population=5 --auto-sample=1
/gen-asset "landing page hero" --population=5 --auto-sample=1
/gen-asset "product screenshot mockup" --population=5 --auto-sample=1

# Combine into pitch deck
/gen-asset "pitch deck using generated assets" \
  --type=presentation \
  --assets-dir=generated-assets/
```

## Best Practices

### Start Small, Scale Up
```bash
# Start: Test concept
/gen-asset "logo concept" --population=3 --generations=1

# Refine: Evolve promising direction
/gen-asset "logo based on abstract style" --population=5 --generations=2

# Polish: Final refinements
/gen-asset "final logo with tweaks" --population=3 --based-on=winner
```

### Use Clustering for Exploration
- High population + clustering reveals style families
- Helps identify unexpected winners
- Shows diversity of solution space

### Use Auto-Sampling for Efficiency
- When you trust the criteria
- For large populations (>10)
- To save review time

### Weighted Criteria for Specific Needs
```bash
# Conservative brand: Value alignment > creativity
--criteria="brand_alignment,professionalism,clarity,creativity" \
--weights="brand_alignment:0.4,professionalism:0.3,clarity:0.2,creativity:0.1"

# Innovative brand: Value creativity > alignment
--weights="creativity:0.4,innovation:0.3,aesthetics:0.2,brand_alignment:0.1"
```

### Multi-Generation for Quality
- Generation 1: Explore diversity
- Generation 2: Refine successful directions
- Generation 3: Polish winners

## Performance Tips

### Parallel Generation
- All variants within a generation run in parallel
- Use Task tool with multiple agents
- Maximize throughput

### Early Pruning
```bash
--auto-sample=5 --early-prune
# After G1, only top 5 breed for G2
# Reduces G2 from population×5 to 5×population
```

### Provider Selection
- DALL-E 3: Best quality, slower, $0.11/image
- Stable Diffusion: Faster, cheaper, local option
- Claude: Best for text/code, fast, cheap

### Caching
- Cache prompts across generations
- Reuse embeddings for clustering
- Save evaluation scores

## Troubleshooting

**Low diversity in variants:**
```
Problem: All variants look similar
Solution:
- Increase diversity dimensions
- Use more specific diversity constraints
- Check provider prompt enhancement (may homogenize)
```

**Poor scoring accuracy:**
```
Problem: Scores don't match human preference
Solution:
- Adjust criteria weights
- Use ensemble voting
- Add custom criteria
- Human-in-loop scoring
```

**Exponential cost explosion:**
```
Problem: population=5, generations=4 → 625 variants
Solution:
- Use early pruning: --early-prune --auto-sample=3
- Reduce population per generation
- Use tiered strategy: G1=5, G2=3 (top 3 breed)
```

---

**Remember:**
- Genetic generation excels at exploration
- More generations = refinement, not diversity
- Clustering reveals solution space structure
- Auto-sampling requires good criteria
- Start small, iterate based on results

🧬 **Happy evolving!**
