<!-- File UUID: 5a7d9f3c-2e8b-4a1f-9c6d-8b4e7f2a5c3d -->

# License Auditor Agent

## Overview

The License Auditor Agent is a specialized tool that audits project dependencies for license compatibility issues. It detects potential licensing conflicts before they become legal problems.

## Use Cases

**Invoke this agent when:**
- Starting a new project (verify clean license slate)
- Adding new dependencies (check compatibility)
- Preparing for open source release (audit compliance)
- Before commercial distribution (identify GPL conflicts)
- Due diligence for acquisitions (license risk assessment)
- Regular compliance audits (quarterly reviews)

**Common Scenarios:**
- **Proprietary software** using GPL dependencies (incompatible)
- **MIT project** with AGPL dependencies (may trigger copyleft)
- **GPL-2.0 project** using GPL-3.0 libraries (version mismatch)
- **Commercial SaaS** with unclear dependency licenses (risk assessment)

## Supported Ecosystems

| Ecosystem | Detection File | API Source |
|-----------|----------------|------------|
| **npm** | package.json | npm registry |
| **Python** | requirements.txt, pyproject.toml | PyPI |
| **Rust** | Cargo.toml | crates.io (planned) |
| **Go** | go.mod | pkg.go.dev (planned) |

## License Categories

The agent classifies licenses into compatibility categories:

### 1. Permissive
**Examples:** MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**Characteristics:**
- Can be used in any project (open source or proprietary)
- Minimal restrictions (usually just attribution)
- Compatible with copyleft licenses

**Use freely in:** Any project type

### 2. Weak Copyleft
**Examples:** LGPL-2.1, LGPL-3.0, MPL-2.0, EPL-2.0

**Characteristics:**
- Requires attribution and source disclosure for modifications
- Allows proprietary use if dynamically linked
- Compatible with proprietary software (with conditions)

**Use in proprietary:** Yes, if properly isolated (dynamic linking, separate modules)

### 3. Strong Copyleft
**Examples:** GPL-2.0, GPL-3.0, AGPL-3.0

**Characteristics:**
- Requires entire project to be open source
- Requires source disclosure for all modifications
- AGPL extends to network use (SaaS)

**Use in proprietary:** No (requires relicensing entire project)

### 4. Unknown
**Characteristics:**
- License not recognized or missing
- Requires manual review
- May hide legal risks

**Action:** Contact maintainer or find alternative

## Compatibility Rules

### Permissive Project (MIT, Apache, BSD)
```
✅ Permissive dependencies (MIT, Apache, BSD)
✅ Weak copyleft dependencies (LGPL, MPL) with proper linking
⚠️  Strong copyleft dependencies (GPL, AGPL) - requires relicensing
❌ Unknown licenses - manual review required
```

### Weak Copyleft Project (LGPL, MPL)
```
✅ Permissive dependencies (MIT, Apache, BSD)
✅ Same weak copyleft (LGPL-3.0 with LGPL-3.0)
⚠️  Different weak copyleft (LGPL-3.0 with MPL-2.0) - check compatibility
⚠️  Strong copyleft (GPL, AGPL) - may require relicensing
❌ Unknown licenses - manual review required
```

### Strong Copyleft Project (GPL, AGPL)
```
✅ Permissive dependencies (MIT, Apache, BSD)
✅ Weak copyleft dependencies (LGPL, MPL)
✅ Same strong copyleft version (GPL-3.0 with GPL-3.0)
❌ Different GPL version (GPL-2.0 with GPL-3.0) - incompatible
❌ Unknown licenses - manual review required
```

## Usage

### Command Line

**Basic audit (current directory):**
```bash
hmode/agents/license-auditor.py
```

**Audit specific project:**
```bash
hmode/agents/license-auditor.py ~/projects/my-app
```

**Save report to file:**
```bash
hmode/agents/license-auditor.py --output audit-report.txt
```

**JSON output (for CI/CD):**
```bash
hmode/agents/license-auditor.py --json --output audit.json
```

### Claude Code Skill

**Audit current project:**
```
/audit-licenses
```

**Audit specific directory:**
```
/audit-licenses ./projects/my-app
```

**Generate JSON report:**
```
/audit-licenses --json
```

## Output Format

### Text Report

```
================================================================================
LICENSE AUDIT REPORT
================================================================================

Project Directory: /Users/andy/projects/my-app
Project License: MIT
  Category: permissive

SUMMARY
--------------------------------------------------------------------------------
Total Dependencies: 47
Errors: 2
Warnings: 3

ISSUES
--------------------------------------------------------------------------------
❌ Copyleft license incompatibility: strong-copyleft-lib (GPL-3.0) vs project (MIT)
   Dependency: strong-copyleft-lib@2.1.0 (npm)
   License: GPL-3.0
   Recommendation: Consider using a different dependency or relicensing

⚠️  Unknown license for mystery-package
   Dependency: mystery-package@1.0.0 (npm)
   License: Unknown
   Recommendation: Manually verify license compatibility

DEPENDENCIES BY LICENSE
--------------------------------------------------------------------------------
MIT (32 packages):
  - lodash@4.17.21 (npm)
  - express@4.18.2 (npm)
  ...

Apache-2.0 (10 packages):
  - aws-sdk@2.1234.0 (npm)
  ...

GPL-3.0 (2 packages):
  - strong-copyleft-lib@2.1.0 (npm)
  ...

Unknown (3 packages):
  - mystery-package@1.0.0 (npm)
  ...

================================================================================
```

### JSON Report

```json
{
  "project_dir": "/Users/andy/projects/my-app",
  "project_license": {
    "name": "MIT",
    "spdx_id": "MIT"
  },
  "dependencies": [
    {
      "name": "lodash",
      "version": "^4.17.21",
      "ecosystem": "npm",
      "license": {
        "name": "MIT",
        "spdx_id": "MIT"
      }
    }
  ],
  "issues": [
    {
      "dependency": "strong-copyleft-lib",
      "severity": "error",
      "message": "Copyleft license incompatibility: strong-copyleft-lib (GPL-3.0) vs project (MIT)",
      "recommendation": "Consider using a different dependency or relicensing"
    }
  ]
}
```

## Remediation Strategies

### Error: Strong Copyleft in Permissive Project

**Problem:** MIT project using GPL-3.0 dependency

**Options:**
1. **Replace dependency** with permissive alternative (best)
2. **Isolate dependency** via separate service/API (good)
3. **Relicense project** to GPL-3.0 (if open source acceptable)
4. **Remove feature** that requires GPL dependency (acceptable)

**Example:**
```
❌ Using: readline (GPL-3.0) in MIT project
✅ Replace with: cli-readline (MIT alternative)
```

### Warning: Unknown License

**Problem:** Dependency has unclear or missing license

**Actions:**
1. Check package repository (GitHub, GitLab) for LICENSE file
2. Contact package maintainer for clarification
3. Use license scanning tools (licensee, scancode)
4. Find alternative with clear license
5. Document risk if proceeding

### Error: GPL Version Mismatch

**Problem:** GPL-2.0 project using GPL-3.0 dependency

**Options:**
1. **Upgrade project license** to GPL-3.0 (if compatible)
2. **Replace dependency** with GPL-2.0 version
3. **Downgrade dependency** to GPL-2.0 compatible version
4. **Dual license project** as GPL-2.0-or-later

## CI/CD Integration

### GitHub Actions

```yaml
name: License Audit
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run License Audit
        run: |
          hmode/agents/license-auditor.py --json --output audit.json
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: license-audit
          path: audit.json
      - name: Fail on Errors
        run: |
          if [ $? -ne 0 ]; then
            echo "License compatibility errors found!"
            exit 1
          fi
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running license audit..."
hmode/agents/license-auditor.py

if [ $? -ne 0 ]; then
  echo "❌ License audit failed! Fix issues before committing."
  exit 1
fi

echo "✅ License audit passed"
```

## Limitations

**Current Version:**
- **No transitive dependencies** (only direct dependencies audited)
- **Limited ecosystem support** (npm, Python; Rust/Go planned)
- **No license file parsing** for dependencies (relies on registry metadata)
- **Simple compatibility rules** (may miss edge cases)

**Planned Enhancements:**
- Transitive dependency scanning (detect deep GPL usage)
- SPDX expression parsing (handle compound licenses)
- Custom compatibility rules (user-defined policies)
- License file scanning (read LICENSE files directly)
- More ecosystems (Go, Ruby, PHP, Java)

## Best Practices

1. **Audit early** - Check licenses when adding dependencies
2. **Audit regularly** - Run quarterly audits for compliance
3. **Document decisions** - Record why specific licenses are acceptable
4. **Automate checks** - Integrate into CI/CD pipeline
5. **Review unknowns** - Never ignore "Unknown" licenses
6. **Update dependencies** - Newer versions may have clearer licenses
7. **Maintain allowlist** - Track approved licenses for your project type
8. **Legal review** - Consult legal team for commercial projects

## FAQs

**Q: Can I use GPL libraries in my MIT project?**
A: Technically no. GPL requires entire project to be GPL. Options: (1) Relicense as GPL, (2) Replace library, (3) Isolate via separate service.

**Q: What about dual-licensed dependencies?**
A: Choose the license that's compatible with your project. If dependency is MIT OR GPL, use MIT license terms.

**Q: Are dev dependencies exempt from licensing rules?**
A: Development-only tools (testing, linting) generally don't affect distribution license. However, if dev tools generate code included in production, their licenses apply.

**Q: What is AGPL and why is it problematic?**
A: AGPL (Affero GPL) extends GPL to network use. If users access your software over network (SaaS), you must provide source. Very restrictive for commercial SaaS.

**Q: How do I handle "UNKNOWN" licenses?**
A: (1) Check package repository manually, (2) Contact maintainer, (3) Use alternative with clear license, (4) Document risk and proceed with caution.

## References

- [SPDX License List](https://spdx.org/licenses/)
- [Choose a License](https://choosealicense.com/)
- [tl;drLegal](https://tldrlegal.com/)
- [GNU License Compatibility](https://www.gnu.org/licenses/gpl-faq.html#AllCompatibility)
- [Apache License vs MIT](https://opensource.stackexchange.com/questions/6988/)

## Support

**Issues:** Report bugs or suggest improvements in the monorepo

**Questions:** Use `/ask-human` skill for legal advice

**Updates:** Check `hmode/agents/license-auditor.py` for version info
