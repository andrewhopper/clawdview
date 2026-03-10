<!-- File UUID: 6b8e9f4d-3c7a-5e2f-8d9b-4f6a7e3b5c2d -->

# License Auditor Quick Reference

## Quick Start

**Audit current project:**
```bash
hmode/agents/license-auditor.py
```

**Audit specific directory:**
```bash
hmode/agents/license-auditor.py ~/projects/my-app
```

**Save report:**
```bash
hmode/agents/license-auditor.py --output report.txt
```

**JSON output (for CI/CD):**
```bash
hmode/agents/license-auditor.py --json --output audit.json
```

## Via Claude Code Skill

```
/audit-licenses
/audit-licenses ./projects/my-app
/audit-licenses --json
```

## Common Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| GPL in MIT project | ❌ Error | Replace dependency or relicense |
| Unknown license | ⚠️  Warning | Contact maintainer or find alternative |
| GPL version mismatch | ❌ Error | Upgrade license or downgrade dependency |
| AGPL in SaaS | ❌ Error | Replace or open source entire project |

## License Compatibility Chart

```
Project License → Can Use:
─────────────────────────────
MIT/Apache/BSD  → MIT, Apache, BSD, ISC ✅
                → LGPL, MPL (with conditions) ⚠️
                → GPL, AGPL (NO) ❌

LGPL/MPL        → MIT, Apache, BSD ✅
                → Same LGPL/MPL ✅
                → GPL (maybe) ⚠️

GPL             → MIT, Apache, BSD ✅
                → LGPL, MPL ✅
                → Same GPL version ✅
                → Different GPL version ❌
```

## Ecosystem Support

- ✅ **npm** (Node.js) - package.json
- ✅ **pip** (Python) - requirements.txt
- ⚠️  **cargo** (Rust) - Cargo.toml (partial)
- 🚧 **go** (Go) - go.mod (planned)

## Exit Codes

- `0` - No errors found
- `1` - Compatibility errors detected

## Full Documentation

See `hmode/docs/processes/LICENSE_AUDITOR_AGENT.md` for comprehensive guide.
