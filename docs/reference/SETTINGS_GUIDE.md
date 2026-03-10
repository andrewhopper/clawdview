# Claude Code Settings Guide

## 1.0 OVERVIEW

Auto-approval and security settings for Protoflow monorepo.

**Location:** `/Users/andyhop/dev/lab/.claude/settings.json`

### 1.1 Settings Hierarchy

```
Global (~/.claude/settings.json)
  ↓ overridden by
Monorepo (/dev/lab/.claude/settings.json) ← THIS FILE
  ↓ overridden by
Project (projects/*/.claude/settings.json) [OPTIONAL]
```

---

## 2.0 AUTO-APPROVAL

### 2.1 Tools

```
Read, Glob, Grep, Edit     → ✓ All operations
Write                      → ✓ Pattern-restricted
Bash                       → ✓ Pattern-restricted
WebFetch                   → ✓ Domain-restricted
WebSearch, Task, TodoWrite → ✓ All operations
```

### 2.2 Write Patterns

**Paths:** `prototypes/**, shared/**, docs/**, tools/**, .vscode/**, .claude/**`
**Extensions:** `*.{md,json,js,ts,jsx,tsx,css,scss,html,yml,yaml}`

### 2.3 Bash Patterns

**Read:** `cat, ls, tree, grep, find, head, tail, wc, sort, uniq, diff, stat, du, df, jq, awk, sed, cut, tr, paste`

**Write:** `mkdir, touch, cp, mv` | `rm:prototypes/**, chmod:prototypes/**`

**Git:** `status, log, diff, show, blame, pull, checkout, branch, add, commit, push`

**Dev:** `npm, npx, yarn, node, python, python3, curl, wget, which, type`

### 2.4 WebFetch Domains

**Docs:** github.com, githubusercontent.com, developer.mozilla.org, stackoverflow.com, docs.rs, pypi.org

**Frameworks:** nodejs.org, npmjs.com, typescriptlang.org, reactjs.org, vuejs.org, nextjs.org, vercel.com, tailwindcss.com

**AI/ML:** anthropic.com, openai.com, huggingface.co, arxiv.org, towardsdatascience.com

**Content:** google.com, youtube.com, medium.com, dev.to

---

## 3.0 GIT

**Allowed:** commit, push, pull, branch | **Blocked:** PRs | **Default:** main | **Auto-commit:** false

**Template:**
```
${summary}
🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## 4.0 SECURITY

### 4.1 Protected Files
`.env, *.{pem,key,crt}, credentials.json, secrets.json, node_modules/, .git/`

### 4.2 Require Approval
`sudo, su, rm -rf, chmod 777, git push --force, npm publish, docker, kubectl`

### 4.3 Hard Block
`rm -rf /, rm -rf /*, rm -rf ~, rm -rf ~/, dd if=/dev/zero, mkfs, fdisk, > /dev/sda`

---

## 5.0 DIRECTORY PROTOCOLS

### 5.1 Monorepo Root (`/Users/andyhop/dev/lab/`)

**Purpose:** Coordination only (docs, shared resources, project management, config)

**Allowed:** Read all, Glob/Grep all, Write docs/config/shared, Git ops, file inspection

**Restricted:** Root-level test/temp/prototype files, destructive ops outside allowed dirs

### 5.2 Shared Folder (`shared/`)

**Purpose:** Reusable components (templates, domain models, code standards, utils)

**Allowed:** Read all, Write/Edit new resources, all file ops

**Rules:**
1. Domain models require human approval
2. Test changes (affects multiple projects)
3. Semantic versioning for breaking changes
4. Document all components

### 5.3 Projects Folder (`projects/`)

**Purpose:** Individual project isolation

**Settings Precedence:** `projects/{type}/{status}/{project}/.claude/settings.json` → monorepo

**Structure:** `{personal|work|shared|oss}/{active|archived}/{project}/`

**Project-Level Settings (OPTIONAL):**

Create `.claude/settings.json` for:
- Production projects (stricter controls)
- Experimental projects (more freedom)
- Specific tool requirements
- Unique security needs

Skip for standard prototypes/workflows.

**Examples:**

Stricter (production):
```json
{
  "allowedTools": { "Bash": { "autoApprove": false } },
  "git": { "allowPush": false, "requireApprovalFor": ["commit", "push"] }
}
```

Permissive (prototype):
```json
{
  "allowedTools": {
    "Write": { "patterns": ["**/*"] },
    "Bash": { "patterns": ["rm:*"] }
  }
}
```

### 5.4 Protocol Summary

```
┌─────────────────────┬──────────────┬────────────┬─────────────────────┐
│ Location            │ Write Scope  │ Bash Scope │ Purpose             │
├─────────────────────┼──────────────┼────────────┼─────────────────────┤
│ Monorepo Root       │ Limited      │ Limited    │ Coordination        │
│ .claude/            │ Full         │ Limited    │ Documentation       │
│ hmode/guardrails/        │ Protected    │ Protected  │ Tech preferences    │
│ shared/             │ Full         │ Full       │ Reusable components │
│ projects/{project}/ │ Full         │ Full       │ Project work        │
│ project-management/ │ Full         │ Limited    │ Ideas & tracking    │
└─────────────────────┴──────────────┴────────────┴─────────────────────┘
```

---

## 6.0 WORKFLOW

**Enabled:** Hooks, Auto-Format | **Disabled:** Linting, Testing

**Active Hooks:** PostToolUse → ZMQ Event Publisher (`$PROTOFLOW_ROOT/.claude/hooks/zmq-event-publisher.sh`)

---

## 7.0 UI

```json
{
  "verboseLogging": false,
  "showPermissionPrompts": false,
  "autoApprovePatterns": true,
  "confirmDestructiveOperations": true
}
```

---

## 8.0 EMAIL (MCP)

```json
{
  "defaultBcc": "crm@yourcompany.com",
  "crmSystem": "salesforce",
  "defaultTone": "neutral",
  "solutionCount": 3,
  "autoArchive": true,
  "calendarLink": "https://calendly.com/yourname"
}
```

---

## 9.0 TROUBLESHOOTING

### 9.1 Command Not Auto-Approved
1. Check pattern match (use `*` wildcard)
2. Check no conflicting deny rules
3. Check not in `protectedFiles`

### 9.2 Git Ops Require Approval
1. Verify `git.<op>:*` in Bash patterns
2. Check `git.allow<Op>` is true
3. Check not using `--force` or restricted flags

### 9.3 WebFetch Blocked
1. Check domain in allowedDomains
2. Add if missing
3. Verify exact domain match

---

## 10.0 EXTENDING

### 10.1 Add Bash Pattern
```json
{ "allowedTools": { "Bash": { "patterns": ["new-cmd:*"] } } }
```

### 10.2 Add WebFetch Domain
```json
{ "allowedTools": { "WebFetch": { "allowedDomains": ["new-domain.com"] } } }
```

### 10.3 Add Protected File
```json
{ "prototyping": { "protectedFiles": ["*.secret", "private/**"] } }
```

---

## 11.0 SECURITY PHILOSOPHY

**Auto-approve:** Read-only, well-defined scope, reversible, minimal risk

**Require approval:** Destructive, system-level, publishing, outside boundaries

**Quarterly audit:** Remove unused approvals, verify boundaries, update domains/protected files

**Incident response:** Disable autoApprove, review commits, check mods, restore backup, update rules

---

## APPENDIX: FULL STRUCTURE

```json
{
  "allowedCommands": [...],
  "deniedCommands": [...],
  "allowedTools": {
    "Bash": { "autoApprove": true, "patterns": [...] },
    "Read": { "autoApprove": true },
    "Write": { "autoApprove": true, "patterns": [...] },
    "Edit": { "autoApprove": true },
    "Glob": { "autoApprove": true },
    "Grep": { "autoApprove": true },
    "WebFetch": { "autoApprove": true, "allowedDomains": [...] },
    "WebSearch": { "autoApprove": true },
    "Task": { "autoApprove": true },
    "TodoWrite": { "autoApprove": true }
  },
  "git": { ... },
  "prototyping": { ... },
  "security": { ... },
  "workflow": { ... },
  "ui": { ... },
  "emailConfig": { ... },
  "hooks": { ... }
}
```

---

**Updated:** 2025-12-02 | **Version:** 2.0.0 (Densified)

**Related:** [settings.json](.claude/settings.json) | [CLAUDE.md](../../CLAUDE.md) | [@core/CRITICAL_RULES](hmode/docs/core/CRITICAL_RULES.md)
