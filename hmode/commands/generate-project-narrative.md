---
uuid: cmd-proj-narr-2v3w4x5y
version: 1.0.0
last_updated: 2025-11-11
description: Generate comprehensive narrative documentation for prototype
---

# Generate Project Narrative

Generate comprehensive narrative documentation for `{proto_dir}`.

## Usage

```bash
/generate-project-narrative prototypes/proto-027-semantic-schema-mapper [--output=./NARRATIVE.md]
```

**Arguments:**
- `{proto_dir}`: Path to prototype or idea directory
- `--output=./NARRATIVE.md`: Output file path (default: NARRATIVE.md in proto_dir)

## Output

**NARRATIVE.md** - Comprehensive project documentation with:
- Executive summary
- Problem statement
- Solution approach
- Architecture
- Implementation details
- Tech stack
- Usage guide
- Results/impact
- Next steps

## Workflow

### Step 1: Gather Content

1. **Read all project files**:
   - `.project` → metadata, phase, description, success_criteria
   - `README.md` → overview, purpose, quick start
   - `ARCHITECTURE.md` or `design/ARCHITECTURE.md` → architecture details
   - `design/SPECIFICATION.md` → requirements, scope
   - `design/TECH_STACK.md` → technology choices
   - `design/IMPLEMENTATION_PLAN.md` → implementation approach
   - `LEARNINGS.md` or `RETROSPECTIVE.md` → lessons learned
   - Source files (if Phase 7-8) → code structure insights

2. **Extract key information**:
   - **Context**: Why was this built? What problem?
   - **Solution**: How does it solve the problem?
   - **Architecture**: System design, components, data flow
   - **Implementation**: Key technical decisions, patterns used
   - **Usage**: How to install, configure, use
   - **Results**: Outcomes, metrics, impact
   - **Learnings**: What worked, what didn't, future improvements

### Step 2: Structure Document

3. **Document outline** (decimal numbering per CLAUDE.md):

```markdown
# Project Narrative: {Project Name}

**Author**: Andy Hopper, AWS Solutions Architect
**Date**: {current_date}
**Phase**: {current_phase}
**Status**: {status}

---

## 1.0 Executive Summary
  1.1 Overview
  1.2 Key Outcomes
  1.3 Impact

## 2.0 Problem Statement
  2.1 Context
  2.2 Challenge
  2.3 Current State
  2.4 Goals

## 3.0 Solution Approach
  3.1 Strategy
  3.2 Key Innovations
  3.3 Design Principles
  3.4 Scope
    3.4.1 In Scope
    3.4.2 Out of Scope

## 4.0 Architecture
  4.1 System Overview
  4.2 Components
    4.2.1 {Component 1}
    4.2.2 {Component 2}
  4.3 Data Flow
  4.4 Technology Stack
    4.4.1 Frontend
    4.4.2 Backend
    4.4.3 Data Layer
    4.4.4 Infrastructure

## 5.0 Implementation
  5.1 Key Technical Decisions
  5.2 Design Patterns
  5.3 Code Organization
  5.4 Dependencies

## 6.0 Usage Guide
  6.1 Installation
  6.2 Configuration
  6.3 Basic Usage
  6.4 Advanced Features
  6.5 API Reference

## 7.0 Results & Impact
  7.1 Outcomes Achieved
  7.2 Metrics
  7.3 Lessons Learned
  7.4 Success Criteria Assessment

## 8.0 Next Steps
  8.1 Future Enhancements
  8.2 Known Limitations
  8.3 Recommendations

## 9.0 Appendix
  9.1 References
  9.2 Related Prototypes
  9.3 Technical Resources
```

### Step 3: Generate Content Sections

4. **1.0 Executive Summary**:

```markdown
## 1.0 Executive Summary

### 1.1 Overview

{Project name} is a {type of solution} built to {primary purpose}. This prototype {what it demonstrates/validates}.

**Key characteristics:**
- {Characteristic 1}
- {Characteristic 2}
- {Characteristic 3}

### 1.2 Key Outcomes

- ✅ **{Outcome 1}**: {Description + metric if available}
- ✅ **{Outcome 2}**: {Description + metric if available}
- ✅ **{Outcome 3}**: {Description + metric if available}

### 1.3 Impact

{High-level impact statement - what changed, what's now possible, who benefits}
```

**Content sources:**
- `.project` description → Overview
- `README.md` → Key characteristics
- Success criteria from `.project` → Outcomes
- Learnings/retrospective → Impact

5. **2.0 Problem Statement**:

```markdown
## 2.0 Problem Statement

### 2.1 Context

{Why was this needed? What's the business/technical context?}

### 2.2 Challenge

{What specific problem does this address?}

**Pain points:**
- {Pain point 1}
- {Pain point 2}
- {Pain point 3}

### 2.3 Current State

{How are people solving this today? What are the limitations?}

### 2.4 Goals

1. **Primary goal**: {Main objective}
2. **Secondary goals**:
   - {Goal 1}
   - {Goal 2}
   - {Goal 3}
```

**Content sources:**
- `design/SPECIFICATION.md` → Context, challenge, goals
- `seed.md` (if Phase 1-6) → Problem statement
- `README.md` introduction → Context

6. **3.0 Solution Approach**:

```markdown
## 3.0 Solution Approach

### 3.1 Strategy

{High-level approach to solving the problem}

### 3.2 Key Innovations

- **{Innovation 1}**: {What makes this unique/better}
- **{Innovation 2}**: {What makes this unique/better}

### 3.3 Design Principles

1. **{Principle 1}**: {Rationale}
2. **{Principle 2}**: {Rationale}
3. **{Principle 3}**: {Rationale}

### 3.4 Scope

#### 3.4.1 In Scope

- {Feature/capability 1}
- {Feature/capability 2}
- {Feature/capability 3}

#### 3.4.2 Out of Scope

- {Excluded feature 1}
- {Excluded feature 2}
```

**Content sources:**
- `design/SPECIFICATION.md` → Scope
- `analysis.md` or `selection.md` → Strategy, innovations
- `ARCHITECTURE.md` → Design principles

7. **4.0 Architecture**:

```markdown
## 4.0 Architecture

### 4.1 System Overview

{High-level architecture description}

### 4.2 Components

#### 4.2.1 {Component 1 Name}

**Purpose**: {What does this component do?}
**Technology**: {Framework/language used}
**Responsibilities**:
- {Responsibility 1}
- {Responsibility 2}

#### 4.2.2 {Component 2 Name}

**Purpose**: {What does this component do?}
**Technology**: {Framework/language used}
**Responsibilities**:
- {Responsibility 1}
- {Responsibility 2}

{Repeat for all major components}

### 4.3 Data Flow

{Describe how data flows through the system}

1. {Step 1 in data flow}
2. {Step 2 in data flow}
3. {Step 3 in data flow}

### 4.4 Technology Stack

#### 4.4.1 Frontend

- **Framework**: {React/Vue/Next.js/etc.}
- **UI Library**: {Tailwind/Material/etc.}
- **State Management**: {Redux/Zustand/etc.}

#### 4.4.2 Backend

- **Runtime**: {Node.js/Python/Go/etc.}
- **Framework**: {Express/FastAPI/etc.}
- **API Type**: {REST/GraphQL/gRPC}

#### 4.4.3 Data Layer

- **Primary Database**: {PostgreSQL/MongoDB/etc.}
- **Cache**: {Redis/etc.}
- **Storage**: {S3/etc.}

#### 4.4.4 Infrastructure

- **Cloud Provider**: {AWS/GCP/Azure}
- **Compute**: {Lambda/ECS/K8s}
- **CI/CD**: {GitHub Actions/etc.}
```

**Content sources:**
- `ARCHITECTURE.md` → All architecture content
- `design/TECH_STACK.md` → Technology choices
- `.project` tech_stack → Stack details
- Source code structure → Component details

8. **5.0 Implementation**:

```markdown
## 5.0 Implementation

### 5.1 Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| {Decision 1} | {What was chosen} | {Why} |
| {Decision 2} | {What was chosen} | {Why} |
| {Decision 3} | {What was chosen} | {Why} |

### 5.2 Design Patterns

- **{Pattern 1}**: {Where used and why}
- **{Pattern 2}**: {Where used and why}

### 5.3 Code Organization

\`\`\`
{project-root}/
├── src/
│   ├── {module1}/     # {Purpose}
│   ├── {module2}/     # {Purpose}
│   └── {module3}/     # {Purpose}
├── tests/
├── docs/
└── package.json
\`\`\`

### 5.4 Dependencies

**Core dependencies:**
- `{package1}` ({version}) - {Purpose}
- `{package2}` ({version}) - {Purpose}

**Total dependencies**: {count}
**License compliance**: {Status}
```

**Content sources:**
- `design/IMPLEMENTATION_PLAN.md` → Technical decisions, patterns
- `design/TECH_STACK.md` → Dependency rationale
- `package.json` or `requirements.txt` → Dependencies
- Source code → Code organization

9. **6.0 Usage Guide**:

```markdown
## 6.0 Usage Guide

### 6.1 Installation

\`\`\`bash
# Clone repository
git clone {repo-url}
cd {project-dir}

# Install dependencies
{npm install / pip install -r requirements.txt}

# Configure
cp .env.example .env
# Edit .env with your settings
\`\`\`

### 6.2 Configuration

**Required environment variables:**
- `{VAR1}`: {Description}
- `{VAR2}`: {Description}

**Optional settings:**
- `{VAR3}`: {Description} (default: {value})

### 6.3 Basic Usage

\`\`\`bash
# Start application
{npm start / python main.py}

# Example API call
curl -X POST http://localhost:3000/api/endpoint \\
  -H "Content-Type: application/json" \\
  -d '{"key": "value"}'
\`\`\`

### 6.4 Advanced Features

**{Feature 1}:**
{Description + example}

**{Feature 2}:**
{Description + example}

### 6.5 API Reference

**Endpoint**: `POST /api/{endpoint}`
**Description**: {What it does}
**Request body**:
\`\`\`json
{
  "param1": "value",
  "param2": 123
}
\`\`\`
**Response**:
\`\`\`json
{
  "result": "success",
  "data": {}
}
\`\`\`
```

**Content sources:**
- `README.md` → Installation, usage examples
- `design/API_DESIGN.md` → API reference
- `.env.example` → Configuration variables

10. **7.0 Results & Impact**:

```markdown
## 7.0 Results & Impact

### 7.1 Outcomes Achieved

{Summary of what was accomplished}

### 7.2 Metrics

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| {Metric 1} | {Target} | {Actual} | ✅/⚠️/❌ |
| {Metric 2} | {Target} | {Actual} | ✅/⚠️/❌ |

### 7.3 Lessons Learned

**What worked well:**
- {Learning 1}
- {Learning 2}

**Challenges encountered:**
- {Challenge 1} - {How resolved}
- {Challenge 2} - {How resolved}

**Would do differently:**
- {Change 1}
- {Change 2}

### 7.4 Success Criteria Assessment

| Criterion | Status | Notes |
|-----------|--------|-------|
| {Criterion 1} | ✅ Met | {Details} |
| {Criterion 2} | ⚠️ Partial | {Details} |
| {Criterion 3} | ✅ Met | {Details} |
```

**Content sources:**
- `.project` success_criteria → Success criteria
- `LEARNINGS.md` or `RETROSPECTIVE.md` → Lessons, challenges
- Test results, metrics files → Metrics data

11. **8.0 Next Steps**:

```markdown
## 8.0 Next Steps

### 8.1 Future Enhancements

**High priority:**
- {Enhancement 1}
- {Enhancement 2}

**Medium priority:**
- {Enhancement 3}
- {Enhancement 4}

**Low priority:**
- {Enhancement 5}

### 8.2 Known Limitations

- {Limitation 1} - {Impact}
- {Limitation 2} - {Impact}

### 8.3 Recommendations

**For production deployment:**
- {Recommendation 1}
- {Recommendation 2}

**For further development:**
- {Recommendation 3}
- {Recommendation 4}
```

**Content sources:**
- `LEARNINGS.md` → Limitations, recommendations
- `design/RISKS.md` → Known risks/limitations
- `.project` metadata → Future plans

12. **9.0 Appendix**:

```markdown
## 9.0 Appendix

### 9.1 References

1. {Reference 1 - documentation, paper, article}
2. {Reference 2}

### 9.2 Related Prototypes

- **{proto-name}**: {Brief description + link}

### 9.3 Technical Resources

- **Repository**: {GitHub URL}
- **Documentation**: {Docs URL}
- **Demo**: {Demo URL}
```

**Content sources:**
- Project references throughout docs
- Links to related prototypes in monorepo

### Step 4: Apply Dense Writing Style

13. **Densify content**:
    - Remove filler words ("very", "really", "just")
    - Use bullets over prose
    - Quantify everything
    - Active voice only
    - Specific terms over vague language

14. **AWS style compliance**:
    - CSAT over NPS
    - Specific dates/numbers
    - AWS-approved terminology
    - "As an AWS Partner" (if applicable)

### Step 5: Write Document

15. **Generate complete NARRATIVE.md**:
    - Use Write tool to create `{output_file}`
    - Format: Markdown with decimal outline numbering
    - Include all sections with actual content (no placeholders)

16. **Report results**:

```markdown
# Project Narrative Generated

**Project**: {proto_name}
**Output**: {output_file}
**Length**: {word_count} words, {char_count} chars
**Sections**: {section_count}

---

## Document Structure

✅ 1.0 Executive Summary
✅ 2.0 Problem Statement
✅ 3.0 Solution Approach
✅ 4.0 Architecture
✅ 5.0 Implementation
✅ 6.0 Usage Guide
✅ 7.0 Results & Impact
✅ 8.0 Next Steps
✅ 9.0 Appendix

---

## Content Sources Used

{List of files read and used for content}

---

## Quality Checks

Run quality checks:
\`\`\`bash
/writing-quality {output_file}
/amazon-style-checker {output_file}
\`\`\`

---

✅ Narrative ready for delivery package
```

## Content Extraction Strategies

**Prioritization:**
1. Design docs (Phase 6) → Most comprehensive
2. README.md → Quick overview
3. .project metadata → Basic info
4. Source code → Implementation details
5. Infer from context → Fill gaps

**Handling missing content:**
- **No ARCHITECTURE.md**: Infer from source code structure, README
- **No SPECIFICATION.md**: Extract from README, seed.md, .project
- **No LEARNINGS.md**: Note "Pending Phase 8 completion"
- **Minimal README**: Use .project description, infer from code

**Phase-specific strategies:**
- **Phase 1-6 (ideas/)**: Focus on design docs, specifications, plans
- **Phase 7-8 (prototypes/)**: Include implementation details, code structure, results

## Writing Style

**Dense, Amazon-style:**
- Quantify: "50% faster" not "much faster"
- Specific: "Q2 2024" not "recently"
- Active: "System processes X" not "X is processed"
- Bullets: Prefer lists over paragraphs
- Tables: Use for comparisons, metrics

**Professional tone:**
- Technical but accessible
- Focus on outcomes, not just features
- Include rationale for decisions
- Be honest about limitations

**Decimal outline format:**
- Required per CLAUDE.md
- Hierarchical numbering: 1.0, 1.1, 1.1.1
- 2-space indentation per level

## Error Handling

**Minimal documentation:**
```
Warning: Limited documentation available
Generating narrative from .project and README only
Result: Basic narrative - recommend adding design docs
```

**Missing key files:**
```
Info: ARCHITECTURE.md not found
Inferring architecture from source code and README
```

**Phase 1-6 prototype:**
```
Info: Prototype in Phase {N} - Implementation pending
Narrative focuses on design and planning artifacts
```

## Best Practices

1. **Read comprehensively**: Load all available docs before writing
2. **Be accurate**: Only include info that exists, don't fabricate
3. **Quantify impact**: Use metrics from success criteria, test results
4. **Include code examples**: Show actual usage, not generic templates
5. **Link to sources**: Reference design docs, specs in narrative
6. **Dense style**: Every sentence adds value

## Integration

Works with:
- `/prepare-delivery` - Primary narrative for delivery package
- `/generate-project-presentation` - Source for presentation content
- `/generate-delivery-email` - Source for email content
- `/amazon-style-checker` - Validates AWS style compliance
- `/writing-quality` - Validates documentation quality

---

Be comprehensive, accurate, and impact-focused.
