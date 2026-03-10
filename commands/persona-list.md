---
version: 1.0.0
last_updated: 2025-11-19
description: Browse all available personas from flowey SDLC project
---

# List Available Personas

Display all 48 available personas from the flowey SDLC project with filtering options.

## Purpose

Browse and discover personas before selection. Understand the range of perspectives available.

## Usage

```bash
# List all personas
/persona-list

# Filter by AI attitude
/persona-list pro-ai
/persona-list neutral
/persona-list anti-ai

# Filter by role
/persona-list cto
/persona-list senior-engineer
/persona-list product-manager
```

## Instructions

1. **Parse optional filter argument**:
   - No argument → show all 48 personas
   - `pro-ai` | `neutral` | `anti-ai` → filter by attitude
   - `{role-name}` → filter by specific role

2. **Load persona files**:
   - Directory: `projects/shared/active/protocol-flowey-sdlc-a6gsd/research/personas/`
   - Read all `.md` files matching filter (or all if no filter)

3. **Extract metadata from each persona**:
   - Name (from "**Name**:" line)
   - Role (from filename and title)
   - AI Attitude (from filename: `-pro-ai`, `-neutral`, `-anti-ai`)
   - Years of Experience
   - Brief description (from "## AI Attitude" section)

4. **Present formatted list**:
   ```
   📋 Available Personas (X total)

   === EXECUTIVES ===
   1. CTO (Pro-AI) - [Name] | 30 years
      → Innovation advocate, strategic AI integration
      File: cto-pro-ai.md

   2. CTO (Neutral) - [Name] | 28 years
      → Balanced approach, evidence-driven decisions
      File: cto-neutral.md

   3. CTO (Anti-AI) - Michael Kenwood | 30 years
      → Cautious skeptic, proven tech, security-focused
      File: cto-anti-ai.md

   === DIRECTORS/MANAGERS ===
   4. Director Engineering (Pro-AI) - [Name] | 18 years
      → [Brief description]
      File: director-engineering-pro-ai.md

   [... continues ...]

   === INDIVIDUAL CONTRIBUTORS ===
   28. Senior Engineer (Neutral) - Aisha Patel | 18 years
      → Pragmatic integrator, balanced approach, metrics-driven
      File: senior-engineer-neutral.md

   [... continues ...]

   ---
   Use /persona-select for guided selection
   Or /persona-describe {filename} to view full details
   ```

5. **Group by leadership level**:
   - **Executives**: CTO, CIO, VP Engineering
   - **Directors/Managers**: Director Engineering, Engineering Manager, Team Lead
   - **Architects**: Enterprise Architect, Software Architect
   - **Individual Contributors**: Staff Engineer, Senior Engineer, Tech Lead
   - **Specialists**: QA Manager, Security Engineer, Head DevOps, Product Manager

## Example Output

### List all personas
```
User: /persona-list

📋 Available Personas (48 total)

=== EXECUTIVES (9 personas) ===
1. CTO (Pro-AI) - [Name] | 30y | Innovation advocate
2. CTO (Neutral) - [Name] | 28y | Balanced evidence-driven
3. CTO (Anti-AI) - Michael Kenwood | 30y | Security-focused skeptic
4. CIO (Pro-AI) - [Name] | 25y | Digital transformation leader
5. CIO (Neutral) - [Name] | 27y | Pragmatic IT strategist
6. CIO (Anti-AI) - [Name] | 29y | Risk-aware governance
7. VP Engineering (Pro-AI) - [Name] | 22y | Scale-focused innovator
8. VP Engineering (Neutral) - [Name] | 24y | Balanced delivery
9. VP Engineering (Anti-AI) - [Name] | 26y | Quality-first conservative

=== DIRECTORS/MANAGERS (9 personas) ===
[... continues with all 48 personas grouped ...]
```

### Filter by attitude
```
User: /persona-list anti-ai

📋 Personas with Anti-AI Attitude (16 total)

1. CTO (Anti-AI) - Michael Kenwood | 30y
   → Security skeptic, proven tech, compliance-focused
   File: cto-anti-ai.md

2. Senior Engineer (Anti-AI) - [Name] | 12y
   → Quality-focused, manual testing advocate
   File: senior-engineer-anti-ai.md

[... continues with all 16 anti-ai personas ...]

Use /persona-select to activate one
```

### Filter by role
```
User: /persona-list senior-engineer

📋 Senior Engineer Personas (3 attitudes)

1. Senior Engineer (Pro-AI) - [Name] | 10y
   → AI enthusiast, productivity-focused, explores new tools
   File: senior-engineer-pro-ai.md

2. Senior Engineer (Neutral) - Aisha Patel | 18y
   → Pragmatic integrator, balanced approach, metrics-driven
   File: senior-engineer-neutral.md

3. Senior Engineer (Anti-AI) - [Name] | 12y
   → Quality-focused, prefers manual control, skeptical of automation
   File: senior-engineer-anti-ai.md

Use /persona-select to activate one
```

## Persona Categories

### By AI Attitude
- **Pro-AI (16)**: Enthusiastic, innovation-focused, AI-optimistic
- **Neutral (16)**: Balanced, evidence-driven, pragmatic
- **Anti-AI (16)**: Cautious, risk-aware, proven-tech focused

### By Role (16 roles × 3 attitudes = 48 total)
1. CTO
2. CIO
3. VP Engineering
4. Director Engineering
5. Engineering Manager
6. Team Lead
7. Enterprise Architect
8. Software Architect
9. Staff Engineer
10. Senior Engineer
11. Tech Lead
12. Product Manager
13. Head of Product
14. QA Manager
15. Security Engineer
16. Head DevOps

## Related Commands

- `/persona-select` - Interactive guided selection
- `/persona-describe {filename}` - View full persona details
- `/persona-clear` - Deactivate current persona

---

**Goal**: Discover and browse available persona perspectives
