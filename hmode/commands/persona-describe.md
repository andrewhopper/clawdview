---
version: 1.0.0
last_updated: 2025-11-19
description: View detailed information about a specific persona
args:
  - name: persona_name
    description: Persona filename (e.g., cto-anti-ai, senior-engineer-neutral)
    required: true
---

# Describe Persona

Display full details of a specific persona including background, beliefs, concerns, and decision criteria.

## Purpose

Preview a persona's complete profile before activation. Understand their perspective, experience, and evaluation criteria.

## Usage

```bash
/persona-describe cto-anti-ai
/persona-describe senior-engineer-neutral
/persona-describe product-manager-pro-ai
```

## Instructions

1. **Parse persona name argument**:
   - Accept with or without `.md` extension
   - Normalize to lowercase with dashes
   - If invalid format → suggest using `/persona-list` to find correct name

2. **Load persona file**:
   - Path: `projects/shared/active/protocol-flowey-sdlc-a6gsd/research/personas/{persona_name}.md`
   - If file not found → suggest similar names or list all

3. **Extract and format key sections**:
   - Professional Profile (name, age, experience, tech stack, location)
   - Current Role (company, team size, responsibilities)
   - AI Attitude (overall stance and philosophy)
   - Core Beliefs (key principles)
   - Key Concerns (what they worry about)
   - Decision Criteria (how they evaluate)
   - Memorable Quote (if present)

4. **Present formatted profile**:
   ```
   🎭 Persona Profile: {Role} ({Attitude})

   👤 PROFESSIONAL PROFILE
   Name: {Name}
   Experience: {Years} years
   Tech Stack: {Stack}
   Current Role: {Title} at {Company} ({Team Size})

   🎯 AI ATTITUDE: {Attitude Type}
   {Attitude description paragraph}

   💭 CORE BELIEFS
   • {Belief 1}
   • {Belief 2}
   • {Belief 3}
   [...]

   ⚠️  KEY CONCERNS
   • {Concern 1}
   • {Concern 2}
   • {Concern 3}
   [...]

   ✅ DECISION CRITERIA
   1. {Criterion 1}
   2. {Criterion 2}
   3. {Criterion 3}
   [...]

   💬 MEMORABLE QUOTE
   "{Quote}"

   ---
   File: {filename}
   Use /persona-select to activate this persona
   ```

## Example Output

### CTO Anti-AI Persona
```
User: /persona-describe cto-anti-ai

🎭 Persona Profile: CTO (Anti-AI)

👤 PROFESSIONAL PROFILE
Name: Michael Kenwood
Experience: 30 years
Tech Stack: Java, COBOL, C++, Oracle, IBM Mainframe, Fortinet, CyberArk
Current Role: CTO at SecureBank Financial Technologies (85 engineers)

🎯 AI ATTITUDE: The Cautious Skeptic
Michael views AI technologies with deep skepticism, rooted in decades of
experience managing mission-critical systems where predictability trumps
innovation. Proven technologies are more reliable than emerging trends.

💭 CORE BELIEFS
• Proven technologies are more reliable than emerging trends
• Human expertise cannot be algorithmically replaced
• Regulatory compliance requires human oversight
• Technology should solve specific problems, not create new ones

⚠️  KEY CONCERNS
• Security Vulnerabilities: Potential AI-introduced attack surfaces
• Regulatory Compliance: Challenges in auditing AI-generated code
• Unpredictability: Non-deterministic behavior in critical systems
• Skill Erosion: Risk of developers becoming over-reliant on AI tools
• Long-Term Maintenance: Sustainability of AI-generated codebases

✅ DECISION CRITERIA
1. Absolute Reliability: Zero tolerance for unexpected behaviors
2. Comprehensive Audit Trails: Full traceability of all AI interventions
3. Strict Governance: Clear human checkpoints in all processes
4. Performance Predictability: Consistent, measurable outcomes
5. Minimal Disruption: Seamless integration with existing workflows

💬 MEMORABLE QUOTE
"Technology is a tool, not a magic wand. I've seen trends come and go,
but reliable software is built on solid engineering principles, not hype."

---
File: cto-anti-ai.md
Use /persona-select to activate this persona
```

### Senior Engineer Neutral Persona
```
User: /persona-describe senior-engineer-neutral

🎭 Persona Profile: Senior Engineer (Neutral)

👤 PROFESSIONAL PROFILE
Name: Aisha Patel
Experience: 18 years
Tech Stack: TypeScript, Node.js, React, GCP, DevOps
Current Role: Engineering Director at Mid-sized SaaS Product Company (40 engineers)

🎯 AI ATTITUDE: Balanced and Analytical
Aisha approaches AI-native software development with a measured, data-driven
perspective. She sees AI as a potential tool that must be carefully evaluated,
integrated, and managed. Primary focus is on tangible business value, team
productivity, and maintaining high-quality engineering standards.

💭 CORE BELIEFS
• Technology should solve real business problems
• Tools are means to an end, not ends themselves
• Continuous evaluation and adaptation are key
• Human creativity and strategic thinking remain paramount
• Effective integration requires nuanced understanding

⚠️  KEY CONCERNS
• Maintaining team skill development
• Ensuring consistent code quality
• Managing the learning curve of new technologies
• Balancing innovation with practical constraints
• Protecting team morale during technological transitions

✅ DECISION CRITERIA
1. Measurable business impact
2. Minimal disruption to existing workflows
3. Clear, manageable learning curve
4. Robust governance and control mechanisms
5. Alignment with long-term technology strategy

💬 MEMORABLE QUOTE
"Technology is a tool, not a religion. We adopt what works, challenge what
doesn't, and always keep our teams' growth and potential at the center of
our decisions."

---
File: senior-engineer-neutral.md
Use /persona-select to activate this persona
```

## Error Handling

### Persona not found
```
User: /persona-describe invalid-name

❌ Persona not found: invalid-name

Did you mean one of these?
• cto-anti-ai
• senior-engineer-neutral
• product-manager-pro-ai

Use /persona-list to see all available personas.
```

### Missing argument
```
User: /persona-describe

⚠️  Missing persona name

Usage: /persona-describe {persona-name}

Examples:
• /persona-describe cto-anti-ai
• /persona-describe senior-engineer-neutral
• /persona-describe product-manager-pro-ai

Use /persona-list to browse all available personas.
```

## Implementation Notes

1. **Fuzzy matching**: If exact match fails, suggest similar names (Levenshtein distance)
2. **Formatting**: Use emoji sparingly for section headers, maintain readability
3. **Truncation**: Display full content, don't truncate (personas are ~80 lines each)
4. **Linking**: Mention related commands at bottom for easy navigation

## Related Commands

- `/persona-select` - Interactive guided selection
- `/persona-list` - Browse all available personas
- `/persona-clear` - Deactivate current persona

---

**Goal**: Preview persona details before activation
