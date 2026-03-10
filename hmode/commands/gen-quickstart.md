---
uuid: cmd-gen-quick-8r9s0t1u
version: 1.0.0
last_updated: 2025-11-10
description: Generate or update a quickstart guide for any project
---

# Generate Quickstart Guide

You are a quickstart documentation assistant. Help users create concise, actionable quickstart guides for their projects.

## Purpose

Create focused quickstart guides that get users productive in 5-10 minutes by clearly explaining:
- **Business goals** - Why this exists, what problem it solves
- **Core concepts** - Key ideas needed to understand the project
- **Installation** - How to get started (30 sec - 2 min)
- **First use** - Immediate hands-on experience (2-5 min)
- **Common workflows** - Typical usage patterns
- **Learning path** - Day 1 → Week 1 → Month 1 progression

## Instructions

### 1. Gather Context

Ask for project path if not provided:
```
Which project needs a quickstart guide?
1. Path to project directory
2. Or describe project if starting from scratch
```

If path provided, read:
- `README.md` (understand project)
- `package.json` or equivalent (understand tools)
- Key source files (understand features)
- Existing docs (avoid duplication)

### 2. Determine Scope

**For existing projects**: Analyze and ask:
```
I found these key features:
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

Which should be in the quickstart? (Choose 1-3 most important)
What's the #1 goal for new users?
```

**For new projects**: Ask:
```
Tell me about your project:
1. What problem does it solve?
2. Who is the target user?
3. What should they accomplish in first 5 minutes?
4. What are the 3 most important features?
```

### 3. Generate Quickstart

Use this structure (adapt as needed):

```markdown
# 🚀 [Project Name] - Quickstart Guide

**Get productive in [X] minutes**

---

## What is [Project Name]?

**[One sentence description]**

**Business Goal**: [Why this exists - the problem it solves]

**Key Benefit**: [Primary value proposition]

**Expected Result**: [What users achieve after following this guide]

---

## 🎯 Core Concepts

### [Concept 1]
**Brief explanation** - Why it matters, how it works

### [Concept 2]
**Brief explanation** - Key terminology or patterns

### [Concept 3]
**Brief explanation** - Important constraints or principles

---

## ⚡ Installation ([Time estimate])

\`\`\`bash
[Installation commands]
\`\`\`

**What this does**: [Explanation of what gets installed/configured]

**Requirements**: [Prerequisites if any]

---

## 🚀 First Use ([Time estimate])

### Try 1: [Simplest possible use case]

\`\`\`bash
[Command or code]
\`\`\`

**What to expect**: [Expected output or result]

### Try 2: [Next simplest use case]

\`\`\`bash
[Command or code]
\`\`\`

**What to expect**: [Expected output or result]

### Try 3: [Slightly more complex]

\`\`\`bash
[Command or code]
\`\`\`

**What to expect**: [Expected output or result]

---

## 📚 Which Tool/Feature When?

| I want to... | Use this | Time |
|-------------|----------|------|
| [Use case 1] | [Feature/command] | [Est. time] |
| [Use case 2] | [Feature/command] | [Est. time] |
| [Use case 3] | [Feature/command] | [Est. time] |

---

## 🎓 Learning Path

### Day 1: Basics ([Time estimate])
1. ✅ [First task]
2. ✅ [Second task]
3. ✅ [Third task]

### Week 1: [Intermediate level] ([Time estimate])
1. ✅ [More complex task]
2. ✅ [Integration task]
3. ✅ [Customization task]

### Month 1: Advanced ([Time estimate])
1. ✅ [Advanced feature]
2. ✅ [Optimization]
3. ✅ [Team/production use]

---

## 🔄 Typical Workflows

### Workflow 1: [Most common use case]

\`\`\`bash
# Step 1: [Action]
[command]

# Step 2: [Action]
[command]

# Step 3: [Action]
[command]
\`\`\`

### Workflow 2: [Second common use case]

\`\`\`bash
[Commands with explanations]
\`\`\`

### Workflow 3: [Third common use case]

\`\`\`bash
[Commands with explanations]
\`\`\`

---

## 🛠️ Essential Commands/Features

\`\`\`bash
[command]  # [What it does]
[command]  # [What it does]
[command]  # [What it does]
\`\`\`

---

## 💡 Pro Tips

- **Tip 1**: [Helpful insight]
- **Tip 2**: [Common gotcha to avoid]
- **Tip 3**: [Performance or quality tip]

---

## 🚨 Common Issues

### "[Error or problem]"
**Cause**: [Why this happens]
**Fix**: [How to resolve]

### "[Another common issue]"
**Cause**: [Why this happens]
**Fix**: [How to resolve]

---

## 🎯 Success Criteria

**You're productive when you can**:
- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

---

## 📚 Next Steps

- [Link to full documentation]
- [Link to advanced guides]
- [Link to examples]
- [Link to community/support]

---

## 🚀 Ready to Start?

\`\`\`bash
# [Final call to action with actual command]
\`\`\`

**Happy [verb]!** [emoji]
```

### 4. Customize for Project Type

**CLI Tool**:
- Focus on commands and flags
- Show common command combinations
- Include output examples

**Library/Framework**:
- Focus on API usage
- Show code examples
- Include integration patterns

**Web App**:
- Focus on user workflows
- Show screenshots if available
- Include configuration

**Slash Commands/Tools Suite**:
- Focus on use cases → tool mapping
- Show navigation and interactive features
- Include workflow combinations

### 5. Validate Quickstart

Check that it includes:
- ✅ Clear business goal (why this exists)
- ✅ 3-5 core concepts explained briefly
- ✅ Installation under 2 minutes
- ✅ First use examples (2-5 minutes)
- ✅ Learning path (Day 1, Week 1, Month 1)
- ✅ Common workflows (3-5 most frequent)
- ✅ Success criteria (measurable outcomes)
- ✅ Time estimates for all activities
- ✅ Next steps and full docs links

### 6. Placement

**If project has README.md**: Ask:
```
Where should I save this quickstart?
1. Replace README.md (if current README is too long)
2. Create QUICKSTART.md (keep README separate)
3. Add "Quickstart" section to existing README
4. Show output only (you decide where to save)
```

**If new project**: Create `QUICKSTART.md`

### 7. Update Related Docs

After creating quickstart:
```
✅ Quickstart guide created!

Saved to: [path]

Consider also:
- Update README.md to link to quickstart
- Add to documentation index
- Include in installation/onboarding flow
```

## Writing Guidelines

### Brevity
- Use 50% fewer words than typical documentation
- Bullets over prose
- Tables for comparisons
- Code examples over lengthy explanations

### Structure
- Use decimal outline format (1.0, 1.1, 1.1.1) for complex sections
- Consistent heading hierarchy
- Visual separators (`---`) between major sections
- Emojis for section headers (optional, project-dependent)

### Time Estimates
- Installation: 30 sec - 2 min
- First use: 2-5 min total
- Each example: 30 sec - 1 min
- Full quickstart completion: 5-10 min
- Learning path stages: Day 1 (15-30 min), Week 1 (1-2 hours), Month 1 (ongoing)

### Business Context
**Always include**:
- **Business goal** - Problem solved, value delivered
- **Expected benefits** - Quantified when possible (50% faster, 70% fewer errors)
- **Success criteria** - Measurable outcomes users achieve

### Accessibility
- Assume reader knows basics of domain (don't explain "what is Git")
- Define project-specific concepts only
- Show, don't tell (code examples > descriptions)
- Progressive complexity (simplest first, advanced later)

## Examples of Good vs Bad

### ❌ Bad: Too Generic
```
## Installation
Install the tool using your package manager.
```

### ✅ Good: Specific and Timed
```
## ⚡ Installation (30 seconds)

\`\`\`bash
npm install -g awesome-tool
\`\`\`

**What this does**: Installs CLI globally, adds `awesome` command to PATH
```

### ❌ Bad: No Context
```
Run this command to start.
```

### ✅ Good: Clear Purpose
```
### Try 1: Generate Your First Report (1 min)

\`\`\`bash
awesome generate report --type=weekly
\`\`\`

**What to expect**: Creates `report.md` with weekly summary
```

### ❌ Bad: Missing Business Context
```
This tool helps you write code faster.
```

### ✅ Good: Clear Value Proposition
```
## What is CodeGen?

**Code generation tool** for boilerplate reduction

**Business Goal**: Reduce repetitive coding from 2 hours → 5 minutes

**Key Benefit**: 95% less boilerplate, 100% type-safe

**Expected Result**: Generate complete CRUD APIs in under 5 minutes
```

## Interactive Usage

**If user provides path**:
```bash
/gen-quickstart prototypes/proto-015-claude-power-tools
```
→ Read project, analyze, generate quickstart

**If user provides inline details**:
```bash
/gen-quickstart "API rate limiting library, Express middleware, <100 req/min default"
```
→ Generate from description

**If user says just `/gen-quickstart`**:
→ Ask for project path or description

## Output

Show preview first:
```
📄 Generated Quickstart Guide

[Preview first 20 lines]

...

[Show last section]

---

Save to:
1. QUICKSTART.md (recommended)
2. README.md (replace existing)
3. Append to existing README
4. Show me full output (I'll save manually)

Choose option (1-4):
```

After saving:
```
✅ Quickstart guide saved to [path]

Summary:
- Business goal: [extracted goal]
- Installation: [time] min
- First use: [time] min
- Learning path: Day 1 → Week 1 → Month 1
- Workflows: [count] common patterns

Next steps:
- Link from README: [README.md](./README.md)
- Test with new user
- Update as project evolves
```

## Tips for Good Quickstarts

1. **Start with "why"** - Business context before technical details
2. **Show don't tell** - Code examples over descriptions
3. **Time everything** - Users want to know time investment
4. **Progressive learning** - Simple → Complex over time
5. **Measurable success** - Clear criteria for "productive"
6. **Common patterns** - Real workflows, not isolated features
7. **Brevity wins** - 50% fewer words than you think needed

## Maintenance

Suggest including in quickstart:
```
📌 **This guide was generated on [date]**

If project changes, regenerate with:
\`\`\`bash
/gen-quickstart [path]
\`\`\`
```

---

**Remember**: Best quickstarts get users productive in 5 minutes, not comprehensive - that's what full documentation is for!
