# Artifacts Rules

**Version:** 1.0.0  
**Last Updated:** 2025-11-19  
**Rule Count:** 11

## Table of Contents

1. [✅ decimal-outline-format](#decimal-outline-format)
2. [✅ stage-titles-format](#stage-titles-format)
3. [💡 ascii-diagrams-required](#ascii-diagrams-required)
4. [💡 numbered-lists-not-bullets](#numbered-lists-not-bullets)
5. [💡 densified-writing-50-percent](#densified-writing-50-percent)
6. [⚠️ progressive-content-complex-artifacts](#progressive-content-complex-artifacts)
7. [⚠️ progressive-content-thresholds](#progressive-content-thresholds)
8. [⚠️ trade-offs-in-options](#trade-offs-in-options)
9. [🚫 no-proactive-readme-creation](#no-proactive-readme-creation)
10. [💡 diagrams-fit-on-screen](#diagrams-fit-on-screen)
11. [👍 slide-deck-format-slidev](#slide-deck-format-slidev)

---

## Rules

### ✅ decimal-outline-format

**Level:** ALWAYS
**Category:** artifacts

Use decimal outline format (1.0, 1.1, 1.2, 2.0) for all documents

**Rationale:** Consistent formatting, easy navigation, clear hierarchy

**Context:**
- **When:** creating markdown documents, writing documentation

**Action:**
- **Directive:** use
- **Target:** Decimal outline numbering system

**Examples:**

1. **Scenario:** Creating technical design document
   - ✅ **Correct:** ## 1.0 Overview
## 2.0 Architecture
### 2.1 Components
### 2.2 Data Flow
   - ❌ **Incorrect:** ## Overview
## Architecture
### Components
### Data Flow

*Approved by: Andrew Hopper on 2025-11-19*

---
### ✅ stage-titles-format

**Level:** ALWAYS
**Category:** artifacts

Phase documents use format: # Stage N - Phase Name

**Rationale:** Clear phase identification, consistent formatting across prototypes

**Context:**
- **When:** creating SDLC phase documents
- **File Pattern:** `**/seed.md`

**Action:**
- **Directive:** use
- **Target:** Stage title format: # Stage N - Phase Name
- **Message:** "Example: # Stage 1 - Concept Seed"

**Examples:**

1. **Scenario:** Creating seed.md for new prototype
   - ✅ **Correct:** # Stage 1 - Concept Seed
   - ❌ **Incorrect:** '# Seed Document' or '# Phase 1'

*Approved by: Andrew Hopper on 2025-11-19*

---
### 💡 ascii-diagrams-required

**Level:** SHOULD
**Category:** artifacts

Include ASCII diagrams for 10-second visual comprehension

**Rationale:** Visual scan enables quick understanding, reduces reading time

**Context:**
- **When:** creating technical documents, explaining architecture

**Action:**
- **Directive:** use
- **Target:** ASCII diagrams at start of documents
- **Alternative:** Skip for very simple concepts

**Examples:**

1. **Scenario:** Documenting data flow
   - ✅ **Correct:** ```
Input → Process → Transform → Output
  │        │          │         │
  ▼        ▼          ▼         ▼
 File    Parse     Validate   Store
```
   - ❌ **Incorrect:** Text-only description without visual diagram

*Approved by: Andrew Hopper on 2025-11-19*

---
### 💡 numbered-lists-not-bullets

**Level:** SHOULD
**Category:** artifacts

Use numbered lists instead of bullets (except ✅/❌ checkboxes)

**Rationale:** Numbered lists enable referencing ('see item 3'), clearer sequence

**Context:**
- **When:** writing lists in documents

**Action:**
- **Directive:** prefer
- **Target:** Numbered lists (1. 2. 3.)
- **Alternative:** Use bullets only for ✅/❌ status indicators

**Examples:**

1. **Scenario:** Listing requirements
   - ✅ **Correct:** 1. User authentication
2. Role-based permissions
3. Audit logging
   - ❌ **Incorrect:** - User authentication
- Role-based permissions
- Audit logging

*Approved by: Andrew Hopper on 2025-11-19*

---
### 💡 densified-writing-50-percent

**Level:** SHOULD
**Category:** artifacts

Use 50% fewer words, densified technical writing

**Rationale:** Respect reader time, increase information density, reduce noise

**Context:**
- **When:** creating documentation, writing technical content

**Action:**
- **Directive:** use
- **Target:** Concise densified language
- **Message:** "Remove filler, use arrows/bullets, state directly"

**Examples:**

1. **Scenario:** Explaining a system
   - ✅ **Correct:** FastAPI backend → AWS Lambda → DynamoDB. 100ms p95 latency.
   - ❌ **Incorrect:** The system utilizes a FastAPI backend that is deployed on AWS Lambda, which then connects to DynamoDB for data storage. The 95th percentile latency is approximately 100 milliseconds.

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ progressive-content-complex-artifacts

**Level:** MUST
**Category:** artifacts

Use /progressive-content for complex artifacts (detailed presentations, comprehensive docs)

**Rationale:** Stage-gated creation ensures quality, enables feedback, prevents wasted effort

**Context:**
- **When:** creating detailed presentation, comprehensive documentation, strategic documents
- **Task Types:** New Artifact

**Action:**
- **Directive:** use
- **Target:** /progressive-content 6-stage workflow
- **Message:** "Complex artifact: Using /progressive-content (Stages 0-5)"

**Examples:**

1. **Scenario:** User: 'Create detailed architecture presentation'
   - ✅ **Correct:** Invoke /progressive-content, start Stage 0: 'What's the 2-3 sentence concept?'
   - ❌ **Incorrect:** Immediately generate full 20-slide presentation

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ progressive-content-thresholds

**Level:** MUST
**Category:** artifacts

Progressive content required for: >10 slides, >5 pages, >10 diagram nodes, strategic docs

**Rationale:** Thresholds prevent wasted effort on complex artifacts

**Context:**
- **When:** artifact exceeds complexity threshold

**Action:**
- **Directive:** require
- **Target:** /progressive-content workflow
- **Message:** "Complexity threshold: {threshold}. Using progressive workflow."

**Examples:**

1. **Scenario:** User: 'Create 15-slide presentation'
   - ✅ **Correct:** 15 slides > 10 threshold. Use /progressive-content.
   - ❌ **Incorrect:** Generate all 15 slides immediately

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ trade-offs-in-options

**Level:** MUST
**Category:** artifacts

When presenting options, always include trade-offs (no option is perfect)

**Rationale:** Honest assessment, helps user make informed decision, no option is perfect

**Context:**
- **When:** presenting multiple approaches, confirmation protocol

**Action:**
- **Directive:** require
- **Target:** Explicit trade-offs for each option
- **Message:** "Each option must have: approach + key trade-off"

**Examples:**

1. **Scenario:** Presenting architecture options
   - ✅ **Correct:** Option A: Serverless - Trade-off: Cold start latency
Option B: Containers - Trade-off: Higher operational overhead
   - ❌ **Incorrect:** Option A: Serverless (fast, cheap, scalable)
Option B: Containers (full control)

*Approved by: Andrew Hopper on 2025-11-19*

---
### 🚫 no-proactive-readme-creation

**Level:** NEVER
**Category:** artifacts

Never proactively create README.md or documentation files

**Rationale:** Avoid clutter, user knows when docs needed, focus on code quality first

**Context:**
- **When:** completed implementation
- **Unless:** user explicitly requests documentation

**Action:**
- **Directive:** prohibit
- **Target:** Proactive README/doc creation
- **Alternative:** Only create when user requests

**Examples:**

1. **Scenario:** Just implemented new utility function
   - ✅ **Correct:** Do not create README.md for the utility
   - ❌ **Incorrect:** Proactively create README.md documenting the utility

*Approved by: Andrew Hopper on 2025-11-19*

---
### 💡 diagrams-fit-on-screen

**Level:** SHOULD
**Category:** artifacts

ASCII diagrams should fit on one screen (no scrolling)

**Rationale:** 10-second visual scan impossible if scrolling required

**Context:**
- **When:** creating ASCII diagrams

**Action:**
- **Directive:** prefer
- **Target:** Diagrams fit in 80x40 character space
- **Alternative:** Break into multiple diagrams if too complex

**Examples:**

1. **Scenario:** Complex architecture with 20 components
   - ✅ **Correct:** Create 2-3 focused diagrams (high-level, then details)
   - ❌ **Incorrect:** Single massive diagram requiring vertical scrolling

*Approved by: Andrew Hopper on 2025-11-19*

---
### 👍 slide-deck-format-slidev

**Level:** PREFER
**Category:** artifacts

Use Slidev for presentations (markdown-based, version control friendly)

**Rationale:** Markdown-based, git-friendly, code syntax highlighting, developer-focused

**Context:**
- **When:** creating presentation
- **Unless:** user requests PowerPoint/Google Slides

**Action:**
- **Directive:** prefer
- **Target:** Slidev markdown format
- **Alternative:** PowerPoint/PDF if user requests

**Examples:**

1. **Scenario:** User: 'Create architecture presentation'
   - ✅ **Correct:** Generate Slidev markdown slides.md
   - ❌ **Incorrect:** Ask if they want PowerPoint (default to Slidev)

*Approved by: Andrew Hopper on 2025-11-19*

---
