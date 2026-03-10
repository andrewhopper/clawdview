---
uuid: cmd-upd-dash-5c6d7e8f
version: 1.0.0
last_updated: 2025-11-10
description: Update DASHBOARD.md with current prototype status and metrics
---

# Update Dashboard

You are a dashboard update assistant. Refresh the DASHBOARD.md file with current information from all prototypes.

## Instructions

1. **Scan all prototypes** (in parallel):
   - Read all prototype README.md files
   - Read all prototype TODO.md files
   - Extract status, progress, tech stack, last updated

2. **Calculate metrics**:
   - Total prototypes (active, completed, on hold, archived)
   - Total tasks across all prototypes
   - Completion rates
   - Recent activity (from git or file dates)
   - Tech stack distribution

3. **Update DASHBOARD.md** with fresh data:
   ```markdown
   # 🚀 Protoflow - Dashboard

   > **Last Updated**: [Current Date]

   ---

   ## 📊 Monorepo Health

   ```
   🎯 Active Prototypes    : [count]
   ⏸️ On Hold             : [count]
   ✅ Completed           : [count]
   🗄️ Archived            : [count]
   ──────────────────────────
   📦 Total Prototypes    : [total]
   ```

   ---

   ## 🔥 Current Focus

   **This Week**:
   - [Auto-generated from in-progress tasks]
   - [Most active prototypes]
   - [Critical tasks]

   **Next Week**:
   - [High priority pending tasks]
   - [Planned prototypes]

   ---

   ## 📋 Active Prototypes

   [For each active prototype:]

   ### 🟢 Proto-XXX: [Name]
   - **Started**: YYYY-MM-DD
   - **Progress**: XX%
   - **Status**: [Brief status note from TODO.md or README.md]
   - **Link**: [prototypes/proto-XXX-name](./prototypes/proto-XXX-name)

   ---

   ## 📈 Recent Activity

   ### This Week
   - [Date]: [Activity from git log or TODO updates]
   - [Date]: [Activity]

   ### Last Week
   - [Date]: [Activity]

   ---

   ## 🎯 Upcoming Work

   ### High Priority
   [Top 5-10 high priority tasks across all prototypes]

   ### Medium Priority
   [Top 3-5 medium priority tasks]

   ### Backlog
   [Low priority ideas and future work]

   ---

   ## 📊 Metrics (Optional)

   ### Prototype Velocity
   ```
   Prototypes Started  : [count]
   Prototypes Completed: [count]
   Average Duration    : [X days]
   ```

   ### Task Completion
   ```
   Open Tasks     : [count]
   Completed (Week): [count]
   Completed (Month): [count]
   Completion Rate: [percentage]
   ```

   ---

   ## 🧠 Key Learnings

   ### What's Working
   [Extract from completed prototypes' LEARNINGS sections]

   ### What's Not Working
   [Extract from notes, issues encountered]

   ### Patterns Emerging
   [Analyze common approaches, repeated tech choices]

   ---

   ## 🛠️ Technical Stack Overview

   ### Prototypes Built With
   - [Language/Framework]: X prototypes
   - [Language/Framework]: X prototypes

   ### Most Common Dependencies
   1. [Dependency] - [count] prototypes
   2. [Dependency] - [count] prototypes
   3. [Dependency] - [count] prototypes

   ---

   ## 📚 Resources

   - [Monorepo Todos](./TODO.md) - All monorepo-level tasks
   - [Project Management](./docs/PROJECT_MANAGEMENT.md) - Todo system guide
   - [Claude Code Config](./CLAUDE.md) - Development guidelines

   ---

   ## 🎉 Milestones

   - ✅ [Date]: [Milestone achieved]
   - ⭕ [Future milestone]
   - ⭕ [Future milestone]

   ---

   ## 💡 Quick Actions

   ```bash
   # Create new prototype
   /new-prototype

   # View todos
   cat TODO.md

   # List all prototypes
   /list-prototypes

   # Check prototype status
   /prototype-status [name]

   # Start development
   cd prototypes/proto-XXX-name && npm run dev
   ```
   ```

4. **Generate insights**:
   - Which prototypes need attention (stale, blocked)
   - Velocity trends (speeding up or slowing down)
   - Tech stack patterns (what's working well)
   - Completion rate trends

5. **Show diff** of what changed:
   ```
   📊 Dashboard Updated!

   Changes:
   - Added Proto-005: api-gateway (new)
   - Proto-001: auth-system progress 60% → 75%
   - Proto-002: chat-interface marked completed ✅
   - Total tasks: 67 → 87 (+20 new tasks)
   - Completion rate: 45% → 48%

   Insights:
   - 🎉 1 prototype completed this week
   - 📈 Velocity up 15% (tasks/week)
   - ⚠️ Proto-004 stale (no activity 7+ days)
   - 🔥 Most active: Proto-001 (5 tasks this week)
   ```

6. **Optional: Generate visualizations**:
   ```
   Prototype Timeline:
   Nov 05 ║ 🟢───────────────────────────
   Nov 04 ║ 🟢──────────────────────────
   Nov 03 ║ 🟢─────────────────────────
   Nov 02 ║ 🟢────────────────────────
   Nov 01 ║ 🟢───────────────────────
          ║
          ║ 001  002  003  004  005

   Progress Chart:
   100% ┤                    ✅
    75% ┤  ████
    50% ┤  ████  ████
    25% ┤  ████  ████  ██
     0% ┼──────────────────────
        │  001   002   003  004
   ```

## Auto-Update Triggers

Suggest updating dashboard after:
- Creating a new prototype
- Completing a prototype
- Significant progress on tasks
- Weekly reviews
- Monthly reports

## Implementation Notes

1. **Preserve manual edits**: Don't overwrite "Current Focus" or "Key Learnings" sections if user has customized
2. **Use git data**: Extract commit messages, dates for activity
3. **Calculate smart metrics**: Completion rates, velocity, trends
4. **Keep it actionable**: Focus on what needs attention
5. **Make it visual**: Use progress bars, emoji indicators

## Usage Examples

```bash
# Update dashboard with current data
/update-dashboard

# Update with verbose output
/update-dashboard --verbose

# Update and commit changes
/update-dashboard --commit

# Dry run (show what would change)
/update-dashboard --dry-run

# Generate report for specific date range
/update-dashboard --since 2025-11-01

# Include detailed metrics
/update-dashboard --detailed
```

## Options

- `--verbose` - Show detailed changes and insights
- `--commit` - Auto-commit updated dashboard
- `--dry-run` - Preview changes without writing
- `--since [date]` - Calculate metrics from specific date
- `--detailed` - Include all optional metrics and visualizations
- `--skip-insights` - Update data only, no analysis

## Output Format

```
📊 Updating Dashboard...

Scanning prototypes... [Done - 5 found]
Reading files... [Done - 25 files]
Calculating metrics... [Done]
Generating insights... [Done]
Writing DASHBOARD.md... [Done]

✅ Dashboard updated successfully!

Summary:
- 5 prototypes tracked
- 87 total tasks (42 complete, 45 remaining)
- 48% completion rate
- 1 prototype completed this week
- 2 prototypes need attention

View: cat DASHBOARD.md
```

---

**Remember**: Keep the dashboard current - it's the single source of truth for monorepo health!
