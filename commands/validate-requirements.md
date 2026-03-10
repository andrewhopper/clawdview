---
version: 1.0.0
last_updated: 2026-02-19
description: Validate product requirements documents (PRDs) for completeness
args:
  document: Path to requirements file OR paste requirements text directly
---

# Validate Requirements

Validate product requirements documents (PRDs, SEED docs, user stories) and get comprehensive completeness feedback.

## Usage

**Option 1: Validate a file**
```
/validate-requirements path/to/PRD.md
```

**Option 2: Paste requirements directly**
```
/validate-requirements "
# Project Idea
Building a note-taking app with AI...
"
```

**Option 3: Validate current directory's SEED**
```
/validate-requirements .project
```

---

## What It Validates

### Document Types Auto-Detected

**SEED Document (Phase 1):**
- Idea statement
- Target user/persona
- User intent
- Problem statement
- Success criteria
- Constraints

**PRD Document (Phase 5.5):**
- Title + summary
- Problem statement
- Target audience
- Goals + metrics
- User stories
- Functional requirements
- Non-functional requirements
- Out of scope
- Constraints
- Dependencies
- Risks + mitigations
- Acceptance criteria
- Assumptions
- Open questions

**User Stories:**
- Proper format (As a X, I want Y, so that Z)
- Acceptance criteria
- Priority (MoSCoW)
- Story points
- Dependencies
- Persona alignment

---

## Output

You'll receive:

1. **Completeness Score:** X/Y (Z%)
2. **Status:** ✅ Complete | ⚠️ Nearly Complete | ⚠️ Incomplete | ❌ Insufficient
3. **Gap Analysis:** What's missing and why it matters
4. **Recommendations:** Actionable improvements
5. **Improved Version:** Example showing what complete looks like
6. **Next Steps:** What to do based on completeness level

---

## When to Use

- **Before Phase 2:** Validate SEED completeness
- **Before Phase 6:** Validate PRD for production projects
- **Before stakeholder review:** Ensure requirements are complete
- **After requirements draft:** Get feedback on what's missing
- **During requirements refinement:** Iterative validation

---

## Examples

### Example 1: Quick SEED Validation
```
/validate-requirements "
Idea: AI chatbot for customer support
Target: Small businesses with 10-100 tickets/day
Problem: Support teams overwhelmed with repetitive questions
"
```

**Result:** Completeness report with missing fields (user intent, success criteria, constraints)

### Example 2: Full PRD Validation
```
/validate-requirements docs/PRD.md
```

**Result:** Detailed report with 14-point checklist, gap analysis, recommendations

### Example 3: User Stories Validation
```
/validate-requirements "
As a customer, I want to track my order
As a support agent, I want to see ticket history
"
```

**Result:** Per-story validation with acceptance criteria gaps

---

## Behind the Scenes

This skill spawns the **requirements-validator** agent which:
1. Reads your requirements
2. Detects document type
3. Validates against appropriate checklist
4. Provides comprehensive feedback
5. Shows improved version

---

## Related

- `/audit-proposal` - Validate technical proposals (database, auth, infrastructure)
- Phase 1 (SEED) - Initial idea documentation
- Phase 5.5 (PRD) - Formal requirements for production projects
- `.project` file - Project metadata and phase tracking

---

## Instructions for Claude

When user invokes `/validate-requirements [arg]`:

1. **Parse argument:**
   - If file path → Read file
   - If ".project" → Read current directory's SEED or PRD
   - If text block → Use as-is
   - If empty → Ask user to provide requirements

2. **Spawn requirements-validator agent:**
   ```python
   Task(
       subagent_type="general-purpose",
       prompt=f"""
       You are a requirements validation specialist. Your task is to validate the following requirements document and provide comprehensive completeness feedback.

       Load and follow the agent definition: hmode/agents/requirements-validator.md

       REQUIREMENTS DOCUMENT:
       {document_content}

       Provide:
       1. Document type detection
       2. Completeness score
       3. Gap analysis
       4. Recommendations
       5. Improved version
       6. Next steps
       """,
       description="Validate requirements"
   )
   ```

3. **Present results to user:**
   - Show completeness score and status
   - Highlight critical gaps
   - Provide actionable recommendations
   - Offer improved version

4. **Follow-up:**
   - Ask if user wants to update requirements
   - Offer to save improved version
   - Suggest next SDLC phase if complete

---

**Skill Version:** 1.0.0
**Agent:** requirements-validator
