# Communication Style Selector

Switch between communication protocols for human-AI interaction.

---

## Current Session State

Check if HACP (Human-AI Command Protocol) is active for this session.

---

## Menu

Present the following options to the user:

```
┌─────────────────────────────────────────────────────────────┐
│              COMMUNICATION STYLE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [1] DEFAULT - Standard conversational mode                  │
│      Natural dialogue, AI uses judgment on format            │
│                                                              │
│  [2] HACP - Human-AI Command Protocol                        │
│      Military-inspired structured communication:             │
│      • BLUF (bottom line up front)                           │
│      • Explicit authority levels                             │
│      • Structured status reports                             │
│      • Phase-gate checkpoints for large tasks                │
│                                                              │
│  [3] HACP + STRICT - Protocol with enforcement               │
│      Same as HACP, plus:                                     │
│      • AI requests BLUF if not provided                      │
│      • AI confirms authority level before proceeding         │
│      • Formal escalation format required                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Actions

Based on user selection:

### If [1] DEFAULT selected:
- Confirm: "Communication style: **DEFAULT** — natural conversation mode."
- Do NOT load HACP protocol rules
- Use standard conversational format

### If [2] HACP selected:
- Load `@core/HACP` documentation
- Confirm: "Communication style: **HACP ACTIVE**"
- Display quick reference:
```
HACP Quick Reference:
─────────────────────
Task Order:   BLUF → INTENT → SCOPE → AUTHORITY → CONTEXT → OUTPUT
Authority:    FULL | STANDARD | LIMITED | CONSULT
Status:       BLUF → PROGRESS → BLOCKERS → DECISIONS → REQUEST
Escalate:     Ambiguity, scope creep, tradeoffs, security concerns
```
- Begin using HACP format for all responses

### If [3] HACP + STRICT selected:
- Load `@core/HACP` documentation
- Confirm: "Communication style: **HACP STRICT MODE**"
- Enable enforcement:
  - If user message lacks BLUF, ask: "BLUF? (What do you need in one sentence)"
  - Before starting M/L/XL tasks, confirm: "Authority level? [FULL/STANDARD/LIMITED/CONSULT]"
  - Use formal escalation format for all decision points

---

## Session Persistence

Note: Communication style persists for current session only.
To make permanent, user should add to `.claude/settings.json` or session hooks.

---

## Example Usage

**User:** `/comms`
**AI:** Shows menu, user selects [2]
**AI:** "HACP ACTIVE. Ready for structured task orders."

**User (in HACP mode):**
```
BLUF:   Add dark mode to settings page.
INTENT: Users requested it, improves accessibility.
SCOPE:  M
```

**AI (HACP response):**
```
BLUF: Dark mode implementation ready — 3 components modified.

PROGRESS:
✓ Added ThemeContext with system preference detection
✓ Updated Settings page with toggle
✓ Applied CSS variables for theme switching

DECISIONS MADE:
- Used CSS custom properties (not styled-components) — matches existing patterns
- System preference detection enabled by default

REQUEST: None — ready for review.
```
