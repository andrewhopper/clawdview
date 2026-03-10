---
uuid: cmd-rm-emp-6t7u8v9w
version: 1.0.0
last_updated: 2025-11-11
description: Remove AWS employee-specific configuration references
---

# Remove Employee Configs

Scan `{directory}` for AWS employee-specific tools and configurations, then remove or redact them.

## Usage

```bash
/remove-employee-configs prototypes/proto-027-semantic-schema-mapper [--dry-run] [--report=./EMPLOYEE_CONFIG_SCAN.md]
```

**Arguments:**
- `{directory}`: Path to directory to scan
- `--dry-run`: Show what would be removed without making changes
- `--report=./EMPLOYEE_CONFIG_SCAN.md`: Output report path (default: EMPLOYEE_CONFIG_SCAN.md)

## What It Detects

### AWS Employee Tools

**Internal CLI Tools:**
- `isengard` - AWS internal identity/access management tool
- `isengardcli` - Command-line interface for Isengard
- `midway` - AWS internal deployment/build system
- `midwaycli` - Command-line interface for Midway
- `brazil` - AWS internal build system
- `brazilcli` - Command-line interface for Brazil

**Internal Systems:**
- `mwinit` - AWS credential initialization tool
- `ada` - AWS credentials broker
- `odin` - AWS internal tools
- `pipelines` - AWS internal CI/CD references
- `cr.amazon.com` - AWS internal code review system
- `sim.amazon.com` - AWS internal issue tracking

**Configuration References:**
- Environment variables referencing internal tools
- Configuration files with internal system settings
- Scripts calling internal CLIs
- Documentation mentioning internal workflows

### Detection Patterns

**Case-insensitive search for:**
```regex
# CLI Tools
\b(isengard|isengardcli|midway|midwaycli|brazil|brazilcli)\b

# Internal Systems
\b(mwinit|ada|odin)\b

# URLs
(cr|sim|issues)\.amazon\.com

# Configuration
(ISENGARD|MIDWAY|BRAZIL|MWINIT|ADA)_[A-Z_]+
```

**File types to scan:**
- Code files: `.js`, `.ts`, `.py`, `.go`, `.java`, `.rb`, `.php`
- Config files: `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.config`
- Scripts: `.sh`, `.bash`, `.zsh`, `.fish`
- Documentation: `.md`, `.txt`, `.rst`
- Environment: `.env`, `.env.example`, `.envrc`

**Exclude:**
- `node_modules/`, `venv/`, `.venv/`, `vendor/`
- `dist/`, `build/`, `out/`
- `.git/`
- Binary files

## Workflow

### Step 1: Scan Directory

1. **Find all relevant files:**
   ```bash
   # Use Glob to find files to scan
   **/*.{js,ts,py,go,java,rb,php,json,yaml,yml,toml,ini,config,sh,bash,md,txt,env}
   ```

2. **Search for employee tool references:**
   ```bash
   # Use Grep with case-insensitive search
   # Pattern: (isengard|midway|brazil|mwinit|ada|odin)
   ```

### Step 2: Classify Findings

3. **Categorize by type:**

**CRITICAL** (must remove before delivery):
- Hardcoded credentials/tokens for internal systems
- Internal URLs (cr.amazon.com, sim.amazon.com)
- Environment variables for internal tools
- Scripts that call internal CLIs

**HIGH** (should remove for external use):
- Configuration files referencing internal tools
- Documentation with internal workflows
- Comments mentioning internal systems
- Import statements for internal packages

**MEDIUM** (review and consider):
- Generic mentions in documentation
- Commented-out references
- Historical context in commit messages (read-only)

**LOW** (informational):
- Public AWS service names that happen to match (false positives)
- Acronyms in unrelated contexts

4. **Context analysis:**
   - Check surrounding lines for context
   - Determine if reference is active or legacy
   - Identify if it's critical to functionality

### Step 3: Generate Report

5. **Create scan report:**

```markdown
# Employee Configuration Scan Report

**Directory**: {directory}
**Scan Date**: {timestamp}
**Files Scanned**: {file_count}
**References Found**: {total_count}

---

## Summary

- 🔴 **Critical**: {critical_count} (must remove)
- 🟠 **High**: {high_count} (should remove)
- 🟡 **Medium**: {medium_count} (review)
- 🟢 **Low**: {low_count} (informational)

---

## Critical Issues

### 🔴 #1: Isengard CLI Reference in Script

**File**: `scripts/deploy.sh:23`
**Tool**: isengardcli
**Finding**:
\`\`\`bash
# Authenticate with Isengard
isengardcli auth --profile production
aws s3 sync ./build s3://my-bucket/
\`\`\`

**Impact**: Script will fail for external users (tool unavailable)
**Recommendation**:
- Remove isengardcli authentication
- Use standard AWS credential methods (IAM roles, env vars)
- Update documentation with external auth flow

**Suggested replacement:**
\`\`\`bash
# Authenticate with AWS (external)
# Ensure AWS credentials are configured:
# - Via IAM role (recommended for EC2/Lambda)
# - Via AWS CLI: aws configure
# - Via environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

aws s3 sync ./build s3://my-bucket/
\`\`\`

---

### 🔴 #2: Midway Configuration File

**File**: `config/build.yaml:5`
**Tool**: midway
**Finding**:
\`\`\`yaml
build:
  system: midway
  pipeline: my-service-pipeline
  target: prod
\`\`\`

**Impact**: Build configuration references internal system
**Recommendation**:
- Replace with standard build tool (npm, webpack, etc.)
- Document build process for external users
- Provide Dockerfile or standard build script

---

## High Priority Issues

### 🟠 #3: Documentation with Isengard Workflow

**File**: `docs/DEPLOYMENT.md:45`
**Tool**: isengard
**Finding**:
\`\`\`markdown
## Deployment Process

1. Run \`mwinit\` to refresh credentials
2. Use Isengard to assume production role
3. Run deployment script
\`\`\`

**Impact**: Documentation won't apply to external users
**Recommendation**:
- Rewrite deployment docs for standard AWS credentials
- Remove references to internal tools
- Add external-friendly setup instructions

**Suggested replacement:**
\`\`\`markdown
## Deployment Process

1. Configure AWS credentials:
   - For IAM users: \`aws configure\`
   - For IAM roles: Ensure EC2 instance has appropriate role
2. Verify credentials: \`aws sts get-caller-identity\`
3. Run deployment script: \`./deploy.sh\`
\`\`\`

---

### 🟠 #4: Environment Variable for Internal Tool

**File**: `.env.example:12`
**Tool**: ada
**Finding**:
\`\`\`bash
ADA_CREDENTIALS_PATH=/home/user/.ada/credentials
AWS_PROFILE=isengard-prod
\`\`\`

**Impact**: Invalid configuration for external users
**Recommendation**:
- Remove internal tool environment variables
- Use standard AWS credential configuration
- Update .env.example with external-friendly vars

**Suggested replacement:**
\`\`\`bash
# AWS Configuration
# Set these environment variables or use AWS CLI configuration
# AWS_ACCESS_KEY_ID=your_access_key
# AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
AWS_PROFILE=default
\`\`\`

---

{Continue for all findings...}

---

## Files by Reference Count

| File | References | Severity | Status |
|------|-----------|----------|--------|
| scripts/deploy.sh | 5 | CRITICAL | 🔴 Must fix |
| docs/DEPLOYMENT.md | 8 | HIGH | 🟠 Should fix |
| config/build.yaml | 3 | CRITICAL | 🔴 Must fix |
| .env.example | 2 | HIGH | 🟠 Should fix |
| README.md | 1 | MEDIUM | 🟡 Review |

---

## Recommended Actions

### Immediate (Critical)

1. ❌ **Remove isengardcli** from `scripts/deploy.sh`
2. ❌ **Replace midway config** in `config/build.yaml`
3. ❌ **Update authentication flow** to use standard AWS methods

### Before Delivery (High)

1. ⚠️ **Rewrite deployment docs** with external-friendly instructions
2. ⚠️ **Clean .env.example** of internal tool variables
3. ⚠️ **Test scripts** without internal tool dependencies

### Review (Medium)

1. 💡 Audit all documentation for internal references
2. 💡 Add "External Setup" section to README
3. 💡 Create FAQ for common AWS credential setup

---

## Tool Reference Summary

### Found References by Tool

| Tool | Count | Files | Severity |
|------|-------|-------|----------|
| isengard/isengardcli | 8 | 4 | CRITICAL |
| midway/midwaycli | 5 | 2 | CRITICAL |
| mwinit | 3 | 2 | HIGH |
| ada | 2 | 1 | HIGH |
| brazil | 1 | 1 | MEDIUM |

### Replacement Guidance

**Instead of isengard/mwinit/ada:**
- Use AWS IAM roles (preferred for EC2/ECS/Lambda)
- Use AWS CLI configuration: `aws configure`
- Use environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- Use AWS credential file: `~/.aws/credentials`

**Instead of midway/brazil:**
- Use standard build tools: npm, webpack, docker
- Use CI/CD: GitHub Actions, GitLab CI, CircleCI
- Provide Dockerfile for containerized builds
- Document manual build steps

**Instead of internal URLs:**
- Use GitHub issues (not sim.amazon.com)
- Use GitHub pull requests (not cr.amazon.com)
- Use public AWS documentation links

---

## Scan Statistics

- **Total files scanned**: {file_count}
- **Files with references**: {affected_file_count}
- **Total references found**: {reference_count}
- **Unique tools detected**: {unique_tool_count}
- **Scan duration**: {duration_ms}ms

---

*Generated by /remove-employee-configs*
*Run before: /prepare-delivery, /scan-security*
```

### Step 4: Remove References (Default Behavior)

6. **If NOT --dry-run, perform cleanup:**

   a. **Create backup:**
   ```bash
   cp -r {directory} {directory}.backup-{timestamp}
   ```

   b. **Remove/replace references:**

   **For scripts (.sh, .bash, .zsh):**
   - Remove lines calling internal CLIs
   - Add comments explaining standard AWS auth
   - Update with external-friendly commands

   **For config files (.json, .yaml, .yml):**
   - Remove internal tool configuration
   - Replace with standard AWS config
   - Add comments with setup instructions

   **For documentation (.md, .txt):**
   - Remove internal workflow sections
   - Replace with external-friendly instructions
   - Add standard AWS credential setup docs

   **For code files (.js, .ts, .py, etc.):**
   - Remove import statements for internal tools
   - Replace internal auth flows with standard AWS SDK
   - Add comments explaining changes

   **For environment files (.env, .env.example):**
   - Remove internal tool env vars
   - Add standard AWS env var examples
   - Include setup comments

   c. **Report changes:**
   ```markdown
   ## Auto-Cleanup Applied

   ✅ Backup created: `{directory}.backup-{timestamp}/`
   ✅ Removed {count} employee tool references
   ✅ Updated {count} files

   **Files modified:**
   - `scripts/deploy.sh` - Removed isengardcli, added standard AWS auth
   - `config/build.yaml` - Removed midway config, added npm scripts
   - `docs/DEPLOYMENT.md` - Rewrote with external-friendly instructions
   - `.env.example` - Removed internal tool vars, added AWS standard vars

   **Manual review needed:**
   - `src/auth.ts:45` - Complex isengard integration (review required)
   - `README.md:89` - Internal workflow mentioned in overview
   ```

### Step 5: Integration

7. **Integrate with delivery pipeline:**
   - `/prepare-delivery` calls `/remove-employee-configs` automatically
   - Warns if internal tool references found
   - Includes cleanup report in delivery package

8. **Delivery gate:**
   ```
   🟠 AWS EMPLOYEE TOOL REFERENCES FOUND

   Found 8 references to internal AWS tools:
   - isengardcli (4 references)
   - midway (3 references)
   - mwinit (1 reference)

   These will prevent external use. Recommend cleanup.

   Action options:
   1. Run: /remove-employee-configs {proto_dir} --dry-run (preview changes)
   2. Run: /remove-employee-configs {proto_dir} (auto-cleanup)
   3. Continue with warning (not recommended)
   ```

## Common Patterns

### Authentication Scripts

**Before:**
```bash
#!/bin/bash
mwinit -o
isengardcli auth --profile my-app-prod
aws s3 cp ./data s3://my-bucket/
```

**After:**
```bash
#!/bin/bash
# Authenticate with AWS
# Option 1: Use IAM role (recommended for EC2/ECS/Lambda)
# Option 2: Use AWS CLI: aws configure
# Option 3: Set environment variables:
#   export AWS_ACCESS_KEY_ID=your_key
#   export AWS_SECRET_ACCESS_KEY=your_secret

# Verify credentials
aws sts get-caller-identity

aws s3 cp ./data s3://my-bucket/
```

### Configuration Files

**Before:**
```yaml
deployment:
  system: midway
  pipeline: my-service-prod
  stage: gamma
```

**After:**
```yaml
deployment:
  # Use standard CI/CD or manual deployment
  # See docs/DEPLOYMENT.md for instructions
  environment: production
  region: us-east-1
```

### Documentation

**Before:**
```markdown
## Setup

1. Run `mwinit` to initialize credentials
2. Use Isengard to assume the AppRole
3. Clone the repository from cr.amazon.com
```

**After:**
```markdown
## Setup

1. Configure AWS credentials (choose one):
   - **IAM Role** (recommended for AWS services)
   - **AWS CLI**: Run `aws configure`
   - **Environment variables**: Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

2. Verify credentials:
   ```bash
   aws sts get-caller-identity
   ```

3. Clone the repository:
   ```bash
   git clone https://github.com/your-org/your-repo.git
   ```
```

### Environment Variables

**Before:**
```bash
# .env.example
ISENGARD_PROFILE=my-app-prod
ADA_CREDENTIALS=/home/user/.ada/creds
MIDWAY_BUILD_ID=12345
```

**After:**
```bash
# .env.example

# AWS Configuration
# Configure using one of these methods:
# 1. AWS CLI: aws configure
# 2. Environment variables (below)
# 3. IAM role (for EC2/ECS/Lambda)

# AWS_ACCESS_KEY_ID=your_access_key_here
# AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
```

## Best Practices

1. **Scan before delivery**: Always run before creating customer packages
2. **Review auto-fixes**: Check that replacements are appropriate
3. **Test after cleanup**: Ensure functionality works without internal tools
4. **Document changes**: Update README with external setup instructions
5. **Provide alternatives**: Show standard AWS credential methods

## Error Handling

**Complex integrations:**
```
Warning: Complex internal tool integration detected
File: src/auth.ts:45-67
Tool: isengard

This code has deep integration with internal tools.
Auto-cleanup may break functionality.

Recommend: Manual review and refactoring
```

**No references found:**
```
✅ No employee tool references found

Scanned {file_count} files
No internal AWS tool references detected
Repository is clean for external delivery
```

## Integration Points

Works with:
- `/prepare-delivery` - Automatic cleanup before packaging
- `/scan-security` - Complementary security scan
- `/quality-control` - Validate documentation after cleanup

---

Be thorough and ensure all internal tool references are removed or replaced with external-friendly alternatives.
