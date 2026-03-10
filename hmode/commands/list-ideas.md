---
uuid: cmd-list-ideas-0d1e2f3g
version: 1.0.0
last_updated: 2025-11-10
description: List and browse all captured ideas
---

# List Ideas

You are an idea browsing assistant. Help users explore their captured ideas.

## Instructions

1. **Read IDEAS.md**:
   - Extract all ideas from each section
   - Count ideas by status (active, backlog, prototyped, archived)
   - Count by category
   - Identify high-priority or complex ideas

2. **Display formatted list**:
   ```
   💡 Ideas Collection
   ==================

   Total: X ideas (X active, X backlog, X prototyped, X archived)

   ## 🔥 Active Ideas (X)

   [For each active idea, show:]

   ### 💡 001: [Idea Name]
   **Category**: [Category] | **Complexity**: [Level] | **Priority**: [Level]
   **Status**: Active - [specific status if noted]

   [Brief description]

   **Tech Stack**: Technology 1, Technology 2
   **Time Estimate**: X days
   **Detailed Planning**: [link if exists]

   **Next Action**: [Extracted from next steps]

   ---

   ## 📦 Backlog Ideas (X)

   [Shorter format for backlog items]

   ### 💡 [Idea Name]
   **Category**: [Category] | **Complexity**: [Level]
   [Brief description]

   ---

   ## ✅ Prototyped Ideas (X)

   ### ✅ [Idea Name] → Proto-XXX
   **Prototyped**: YYYY-MM-DD
   **Prototype**: [proto-XXX-name](link)
   **Status**: [Prototype status]
   **Key Learnings**: [Brief note]

   ---

   ## 🗄️ Archived Ideas (X)

   [Minimal info for archived]
   - [Idea Name] - Archived YYYY-MM-DD: [Reason]

   ---

   ## 📊 Ideas by Category

   📱 Frontend:        X ideas
   ⚙️ Backend:         X ideas
   🌐 Full-Stack:      X ideas
   🤖 AI-ML:           X ideas
   🛠️ DevOps:          X ideas
   🔬 Research:        X ideas

   ## 🎯 Ideas by Complexity

   🟢 Simple:          X ideas (avg X days)
   🟡 Medium:          X ideas (avg X days)
   🔴 Complex:         X ideas (avg X days)

   ## 📈 Ideas by Priority

   🔴 High:            X ideas
   🟡 Medium:          X ideas
   🟢 Low:             X ideas

   ---

   ## 🚀 Ready to Build (Suggestions)

   Based on priority, complexity, and status:
   1. [Idea Name] - High priority, simple, well-defined
   2. [Idea Name] - Medium complexity, research complete
   3. [Idea Name] - Interesting learning opportunity

   ## 💡 Quick Actions

   - Add new idea: /new-idea
   - View idea details: cat ideas/active/[name].md
   - Start prototype: /new-prototype
   - Update dashboard: /update-dashboard
   ```

3. **Provide insights**:
   - Which ideas are ready to prototype?
   - Which need more research?
   - Category/complexity trends
   - Stale ideas (created long ago, no progress)

## Filtering Options

User can filter the list:

```bash
# All ideas (default)
/list-ideas

# Filter by status
/list-ideas --active
/list-ideas --backlog
/list-ideas --prototyped
/list-ideas --archived

# Filter by category
/list-ideas --category frontend
/list-ideas --category ai-ml

# Filter by complexity
/list-ideas --simple
/list-ideas --medium
/list-ideas --complex

# Filter by priority
/list-ideas --high
/list-ideas --low

# Multiple filters
/list-ideas --active --category backend --high
```

## Sorting Options

```bash
# By date (newest first)
/list-ideas --recent

# By priority
/list-ideas --by-priority

# By complexity
/list-ideas --by-complexity

# Alphabetical
/list-ideas --alpha
```

## Output Formats

```bash
# Default (detailed)
/list-ideas

# Compact (one line per idea)
/list-ideas --compact

# Full details (including next steps, notes)
/list-ideas --full

# JSON output
/list-ideas --json
```

## Compact Format Example

```
💡 Ideas (15 total)

🔥 Active (8)
001 💡 Real-time Chat      [Backend, Medium]  - WebSocket chat with rooms
002 💡 Dark Mode Toggle    [Frontend, Simple] - CSS variable theming
003 💡 Task Queue          [Backend, Complex] - Distributed task processing
...

📦 Backlog (4)
...

✅ Prototyped (2)
...

🗄️ Archived (1)
...
```

## Full Format Example

Include all details from IDEAS.md plus:
- Complete next steps
- Full tech stack lists
- All notes and links
- Research status
- Decision points

## JSON Format Example

```json
{
  "total": 15,
  "active": 8,
  "backlog": 4,
  "prototyped": 2,
  "archived": 1,
  "ideas": [
    {
      "id": "001",
      "name": "Real-time Chat",
      "status": "active",
      "category": "backend",
      "complexity": "medium",
      "priority": "high",
      "description": "WebSocket chat with rooms",
      "tech_stack": ["Node.js", "Socket.io", "Redis"],
      "time_estimate": "2-3 days",
      "detailed_planning": "ideas/active/realtime-chat.md",
      "created": "2025-11-01",
      "next_steps": [
        "Research Socket.io scaling",
        "Design room architecture",
        "Prototype basic chat"
      ]
    }
  ]
}
```

## Smart Suggestions

Based on the ideas, suggest:

**Ready to Build**:
- High priority + simple/medium complexity
- Research complete
- Clear next steps

**Need Attention**:
- High priority but blocked
- Complex ideas with no research progress
- Stale (created >30 days ago, no updates)

**Learning Opportunities**:
- Ideas with interesting tech stacks
- Good complexity for skill building
- Aligned with stated learning goals

## Statistics & Insights

```
📊 Idea Portfolio Analysis
==========================

Conversion Rate:     40% (2/5 active → prototyped)
Avg Time to Proto:   12 days (idea → prototype started)
Archive Rate:        10% (not building most ideas - good!)

Popular Categories:
1. Backend:      5 ideas (33%)
2. Frontend:     4 ideas (27%)
3. Full-Stack:   3 ideas (20%)

Complexity Distribution:
Simple:  ████░░░░░░ 40%
Medium:  ██████░░░░ 60%
Complex: ░░░░░░░░░░ 0% (might need more ambitious ideas!)

Priority Distribution:
High:    ████░░░░░░ 40%
Medium:  ████░░░░░░ 40%
Low:     ██░░░░░░░░ 20%

Recommendations:
✅ Good mix of complexities
⚠️ Consider adding some complex/research ideas
✅ Healthy archive rate (not holding onto everything)
💡 High conversion rate - great execution!
```

## Related Ideas

Identify potential connections:
```
🔗 Related Ideas
================

Ideas that could be combined:
- "Real-time Chat" + "User Presence" → Full messaging system
- "Task Queue" + "Monitoring Dashboard" → Complete job system

Ideas with overlapping tech:
- "Chat App" and "Notification Service" both use WebSockets
- "API Gateway" and "Auth Service" both use JWT

Learning path suggestions:
1. Start with "Dark Mode Toggle" (simple)
2. Then "Component Library" (builds on styling)
3. Finally "Design System" (combines both)
```

## Implementation Notes

1. **Parse IDEAS.md carefully** - Extract structured data from markdown
2. **Handle missing fields** - Not all ideas have all info
3. **Read detailed files if needed** - For --full format, read ideas/active/*.md
4. **Calculate statistics** - Counts, percentages, trends
5. **Be helpful** - Suggest next actions based on state

## Search Ideas

```bash
# Search by keyword
/list-ideas --search "websocket"
/list-ideas --search "auth"

# Search in descriptions and tech stacks
/list-ideas --search "react"
```

## Example Outputs

### For empty ideas list:
```
💡 Ideas Collection
==================

No ideas captured yet!

Get started:
1. /new-idea to capture your first idea
2. Check out ideas/TEMPLATE.md for inspiration
3. Review prototypes for ideas already built

💭 Idea generation prompts:
- What frustrates you in daily work?
- What would you like to learn?
- What tool are you missing?
```

### For healthy ideas list:
```
💡 Ideas Collection
==================

Total: 12 ideas (5 active, 3 backlog, 3 prototyped, 1 archived)

Great pipeline! You have:
✅ 5 active ideas ready for development
📦 3 ideas brewing in backlog
🎉 3 ideas already prototyped (27% conversion)

Next suggested action:
→ Build "Dark Mode Toggle" (high priority, simple, clear path)
```

---

**Remember**: Ideas are cheap, execution is valuable. This command helps you see what's worth building next!
