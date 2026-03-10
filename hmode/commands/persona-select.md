---
version: 1.0.0
last_updated: 2025-11-19
description: Interactive persona selection through filtering questions
---

# Persona Selection Assistant

Select an AI interaction persona through guided filtering questions. Choose from 48 flowey SDLC personas (16 roles × 3 AI attitudes).

## Purpose

Match your current task to the most appropriate persona perspective:
- **Code review** → Skeptical, security-focused detractor
- **Architecture decisions** → Balanced, pragmatic neutral
- **Rapid prototyping** → Enthusiastic, innovative supporter
- **Stakeholder prep** → Role-specific perspective (CTO, PM, etc.)

## Persona Dimensions

**AI Attitude:**
- **Supporter/Protractor** (pro-AI): Enthusiastic, innovation-focused, AI-optimistic
- **Neutral/Pragmatist**: Balanced, evidence-driven, measured approach
- **Detractor/Skeptic** (anti-AI): Cautious, risk-aware, proven-tech focused

**Leadership Level:**
- **Executive** (CTO, CIO, VP Engineering): Strategic, governance, business impact
- **Director/Manager** (Director Engineering, Engineering Manager, Team Lead): Team coordination, process, delivery
- **Architect** (Enterprise Architect, Software Architect): System design, patterns, tech strategy
- **Individual Contributor** (Staff/Senior Engineer, Tech Lead): Hands-on, implementation, tactical

**Role Focus:**
- **Engineering**: Code quality, architecture, implementation
- **Product**: Features, user value, roadmap, priorities
- **QA**: Testing, quality, reliability, risk
- **Security**: Threat models, compliance, vulnerabilities
- **DevOps**: Infrastructure, deployment, operations, reliability

## Interactive Filtering Flow

### Step 1: AI Attitude Filter
```
What perspective do you need for this task?

A. Supporter/Protractor (pro-AI)
   → Enthusiastic about AI, explores possibilities, innovation-focused
   → Best for: Brainstorming, rapid prototyping, exploring new approaches

B. Pragmatist/Neutral
   → Balanced view, evidence-driven, weighs trade-offs
   → Best for: Architecture decisions, team discussions, balanced reviews

C. Detractor/Skeptic (anti-AI)
   → Cautious, risk-aware, proven technologies preferred
   → Best for: Security review, compliance checks, critical systems

Your choice (A/B/C):
```

### Step 2: Leadership Level Filter
```
What leadership perspective do you need?

A. Executive (CTO, CIO, VP)
   → Strategic vision, governance, business alignment, risk management
   → Best for: High-level decisions, stakeholder communication, strategy

B. Director/Manager
   → Team coordination, process design, delivery management
   → Best for: Project planning, team workflows, cross-team collaboration

C. Architect
   → System design, patterns, technical strategy, long-term maintainability
   → Best for: Architecture decisions, design patterns, tech stack choices

D. Individual Contributor (Staff/Senior Engineer, Tech Lead)
   → Hands-on implementation, code quality, tactical decisions
   → Best for: Code review, implementation details, debugging, refactoring

Your choice (A/B/C/D):
```

### Step 3: Role Focus Filter (if applicable)
```
What role perspective do you need?

A. Engineering (General)
   → Code quality, architecture, implementation best practices

B. Product
   → Feature prioritization, user value, roadmap, requirements

C. QA/Testing
   → Test coverage, quality assurance, reliability, edge cases

D. Security
   → Threat modeling, compliance, vulnerability assessment

E. DevOps/Infrastructure
   → Deployment, operations, reliability, infrastructure

F. Any (show all matching)
   → Display all personas matching previous filters

Your choice (A/B/C/D/E/F):
```

## Instructions

1. **Start filtering conversation**:
   - Present Step 1 (AI Attitude Filter)
   - Wait for user response (A/B/C)
   - Store selection

2. **Continue to Step 2**:
   - Present Step 2 (Leadership Level Filter)
   - Wait for user response (A/B/C/D)
   - Store selection

3. **Present Step 3 if needed**:
   - If leadership level has multiple role focuses → ask Step 3
   - If leadership level maps to single role (e.g., CTO → exec) → skip to results
   - Wait for user response (A/B/C/D/E/F)

4. **Filter personas**:
   - Load persona list from `projects/shared/active/protocol-flowey-sdlc-a6gsd/research/personas/`
   - Apply filters based on user selections
   - Match persona filename patterns:
     - AI attitude: `-pro-ai.md` | `-neutral.md` | `-anti-ai.md`
     - Role: `cto-`, `senior-engineer-`, `product-manager-`, etc.

5. **Present filtered results**:
   ```
   📋 Matching Personas (X found):

   1. CTO (Anti-AI) - Michael Kenwood
      → Cautious skeptic, proven tech, compliance-focused
      → Best for: Security reviews, critical systems, governance
      → File: cto-anti-ai.md

   2. Director Engineering (Anti-AI) - [Name]
      → [Brief description from persona file]
      → Best for: [Use cases]
      → File: director-engineering-anti-ai.md

   Select persona number (1-X) or 'r' to restart filtering:
   ```

6. **Load selected persona**:
   - Read full persona file: `projects/shared/active/protocol-flowey-sdlc-a6gsd/research/personas/{filename}`
   - Extract key sections:
     - Professional Profile
     - AI Attitude
     - Core Beliefs
     - Key Concerns
     - Decision Criteria
   - Apply persona as system context for remainder of conversation

7. **Confirm activation**:
   ```
   ✅ Persona activated: {Role} ({Attitude})

   🎭 I'll now respond as {Name} would:
   - Background: {Experience summary}
   - Perspective: {AI attitude + key concerns}
   - Focus: {Decision criteria}

   Ask your question or describe the task you need help with.
   ```

## Persona Mapping Reference

### AI Attitudes
- **A (Supporter/Protractor)**: `-pro-ai.md` files
- **B (Pragmatist/Neutral)**: `-neutral.md` files
- **C (Detractor/Skeptic)**: `-anti-ai.md` files

### Leadership Levels
- **A (Executive)**: `cto-`, `cio-`, `vp-engineering-`
- **B (Director/Manager)**: `director-engineering-`, `engineering-manager-`, `team-lead-`
- **C (Architect)**: `enterprise-architect-`, `software-architect-`
- **D (Individual Contributor)**: `staff-engineer-`, `senior-engineer-`, `tech-lead-`

### Role Focus (for IC level)
- **A (Engineering)**: `senior-engineer-`, `staff-engineer-`, `tech-lead-`
- **B (Product)**: `product-manager-`, `head-of-product-`
- **C (QA)**: `qa-manager-`
- **D (Security)**: `security-engineer-`
- **E (DevOps)**: `head-devops-`

## Example Usage

### Scenario 1: Security Code Review
```
User: /persona-select
AI: What perspective do you need? A/B/C
User: C (detractor - I want critical review)
AI: What leadership level? A/B/C/D
User: A (executive - strategic security thinking)
AI: [Presents] CTO (Anti-AI) - Michael Kenwood
User: 1
AI: ✅ Activated. Now reviewing as security-focused skeptical CTO...
```

### Scenario 2: Rapid Prototyping Support
```
User: /persona-select
AI: What perspective? A/B/C
User: A (supporter - want encouragement)
AI: What level? A/B/C/D
User: D (IC - hands-on coding help)
AI: What role? A/B/C/D/E/F
User: A (engineering)
AI: [Presents] Senior Engineer (Pro-AI), Staff Engineer (Pro-AI)
User: 2 (Staff Engineer)
AI: ✅ Activated. Ready to build something amazing...
```

### Scenario 3: Balanced Architecture Decision
```
User: /persona-select
AI: What perspective? A/B/C
User: B (pragmatist - need trade-off analysis)
AI: What level? A/B/C/D
User: C (architect - system design focus)
AI: [Presents] Software Architect (Neutral), Enterprise Architect (Neutral)
User: 1 (Software Architect)
AI: ✅ Activated. Let's analyze the architectural trade-offs...
```

## Implementation Notes

1. **Persona file location**: `projects/shared/active/protocol-flowey-sdlc-a6gsd/research/personas/`
2. **Total personas**: 48 (16 roles × 3 attitudes)
3. **Session scope**: Persona active for current conversation only
4. **Restart**: User can type 'r' at any point to restart filtering
5. **Skip filtering**: Advanced users can use `/persona-set {filename}` to directly activate

## State Management

**During filtering**:
- Track user selections in temporary state
- Allow 'back' to previous question
- Allow 'r' to restart from beginning

**After activation**:
- Prepend persona context to all subsequent responses
- Maintain persona consistency until user explicitly changes
- Show subtle reminder: `[Speaking as: {Role} ({Attitude})]`

## Deactivation

To return to default Claude mode:
```
User: /persona-clear
AI: ✅ Persona cleared. Back to default Claude mode.
```

---

**Goal**: Match interaction style to task needs through guided persona selection
