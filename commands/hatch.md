---
uuid: cmd-hatch-5y6z7a8b
description: Extract idea or prototype into standalone repository
args:
  proto_name:
    description: Prototype name (e.g., proto-001-name or just 001)
    required: false
  output_dir:
    description: Output directory path (default ../hatch-output/)
    required: false
  init_git:
    description: Initialize git repository (true/false, default true)
    required: false
  clean_deps:
    description: Remove monorepo-specific dependencies (true/false, default true)
    required: false
---

# Hatch: Extract to Standalone Repository

Extract an idea or prototype from the monorepo into a standalone, deployable repository.

## Parameter Handling

**If arguments provided**: Use them directly
**If arguments missing**: Infer from context or use smart defaults
- `proto_name`: Required - ask if not provided or infer from current directory
- `output_dir`: Default to `../hatch-output/[proto-name]`
- `init_git`: Default to `true`
- `clean_deps`: Default to `true`

**Provided arguments**:
- Proto Name: {proto_name}
- Output Directory: {output_dir}
- Initialize Git: {init_git}
- Clean Dependencies: {clean_deps}

## Instructions

### 1. Locate Source Project

**Find prototype or idea**:
- If `proto_name` provided, search for it in `prototypes/` or `ideas/`
- Accept formats: `proto-001-name`, `001`, `proto-001`, `name`
- If not provided, check if currently in a proto directory (pwd)
- If still not found, list available prototypes and ask

**Validate source**:
- Verify directory exists
- Check if it's an idea (phases 1-6) or prototype (phases 7-8)
- Read `.project` file if exists to understand current phase
- Warn if extracting an incomplete idea (phases 1-5)

### 2. Prepare Output Directory

**Create output structure**:
```bash
output_dir="${output_dir:-../hatch-output/$proto_name}"
mkdir -p "$output_dir"
```

**If directory exists and not empty**:
- Show error: "Output directory already exists: $output_dir"
- Suggest: "Use a different --output-dir or remove existing directory"
- STOP - don't overwrite

### 3. Copy Files Selectively

**Include**:
- All `src/`, `tests/`, `docs/`, `public/` directories
- `README.md`, `package.json`, `tsconfig.json`, `vite.config.*`, etc.
- `.env.example` (NOT `.env`)
- `*.config.js`, `*.config.ts` config files
- License files if present
- Any framework-specific files (next.config.js, etc.)

**Exclude** (monorepo-specific):
- `.project` file (internal tracking)
- `node_modules/` (will be reinstalled)
- `.git/` (will reinitialize if requested)
- `TODO.md` (internal planning, not needed externally)
- References to `../../shared/` or `../../packages/`
- `LEARNINGS.md`, `RETROSPECTIVE.md` (internal)

**Copy command**:
```bash
# Use rsync or cp with exclusions
rsync -av \
  --exclude=node_modules \
  --exclude=.git \
  --exclude=.project \
  --exclude=TODO.md \
  --exclude=LEARNINGS.md \
  --exclude=RETROSPECTIVE.md \
  "$source_dir/" "$output_dir/"
```

### 4. Clean Monorepo Dependencies (if clean_deps=true)

**Scan for monorepo references**:
- Search all source files for imports from `../../shared/` or `../../packages/`
- List all found references
- Identify which shared utilities are used

**For each shared dependency**:

**Option A - Inline the code (simple utilities)**:
- Copy the shared utility into the new repo (`src/utils/` or similar)
- Update import paths
- Add attribution comment

**Option B - Replace with npm package (if equivalent exists)**:
- Identify equivalent npm package
- Add to package.json
- Update imports
- Example: `../../shared/logger` → `winston` or `pino`

**Option C - Document manual action needed**:
- If complex or no clear alternative
- Add comment in code with TODO
- Document in README under "Post-Hatch Setup"

**Update package.json**:
- Remove any workspace: references
- Remove monorepo-specific scripts (like `/update-manifest`)
- Update name to match new repo
- Ensure all dependencies are from npm (no local paths)

### 5. Create Standalone README

**Transform README.md**:
- Keep core purpose and description
- Remove monorepo-specific sections:
  - Phase tracking
  - Links to other prototypes
  - References to monorepo structure
- Add new sections:
  - **Getting Started** - Fresh install instructions
  - **Installation** - `npm install`, `npm run dev`, etc.
  - **Deployment** - Basic deployment instructions
  - **License** - Add if not present (suggest MIT or ISC)
  - **Origin** - Optional note: "Hatched from Protoflow monorepo"

**Example transformation**:
```markdown
# [Project Name]

> Standalone version - ready for deployment

## Overview
[Keep original purpose/description]

## Features
[Keep features list]

## Installation

```bash
# Clone the repository
git clone [repo-url]

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

## Tech Stack
[Keep tech stack]

## Configuration
[Document environment variables from .env.example]

## Deployment
[Add basic deployment instructions for common platforms]

## License
MIT

---
*Hatched from Protoflow - [date]*
```

### 6. Initialize Git (if init_git=true)

**Setup git**:
```bash
cd "$output_dir"
git init
git add .
git commit -m "Initial commit - hatched from protoflow monorepo

Original prototype: $proto_name
Hatched on: $(date -I)

This is now a standalone repository ready for independent development."
```

**Add .gitignore** (if not exists):
```
node_modules/
.env
.DS_Store
dist/
build/
*.log
.cache/
coverage/
```

### 7. Validation & Testing

**Validate standalone repo**:
- Run `npm install` (or equivalent for tech stack)
- Check for missing dependencies
- Try to build/start the project: `npm run build` or `npm run dev`
- Report any errors or warnings

**If validation fails**:
- Document issues in `HATCH_NOTES.md`
- List missing dependencies
- Note manual fixes needed
- Don't fail the hatch - complete it with warnings

### 8. Create Hatch Report

**Generate `HATCH_NOTES.md`** in output directory:
```markdown
# Hatch Report

**Hatched on**: [date]
**From**: protoflow monorepo
**Original path**: [original-path]
**Phase at hatch**: [phase-name]

## Changes Made

### Files Copied
- src/ (X files)
- tests/ (X files)
- Configuration files
- Documentation

### Files Excluded
- .project (internal tracking)
- TODO.md (internal planning)
- node_modules/
- Retrospective docs

### Dependencies Cleaned

#### Inlined
- [utility-name] from shared/ → src/utils/[utility-name].ts

#### Replaced with npm packages
- [shared-package] → [npm-package-name]

#### Manual Action Required
- [ ] Review TODO comments in [file-names]
- [ ] Configure [service-name] API keys in .env
- [ ] Update [placeholder] values

## Validation Results

✅ npm install: Success
✅ npm run build: Success
⚠️ Tests: [status/warnings]

## Next Steps

1. Review HATCH_NOTES.md (this file)
2. Update .env with your configuration
3. Test locally: `npm run dev`
4. Create remote repository on GitHub/GitLab
5. Push: `git remote add origin [url] && git push -u origin main`
6. Configure CI/CD if needed
7. Deploy!

## Original Monorepo Info

For reference, the original prototype remains in the monorepo at:
`[original-path]`

The monorepo may contain additional context in TODO.md, LEARNINGS.md, or design docs.
```

### 9. Display Summary

**Show completion message**:
```
🐣 Hatched successfully!

📦 Standalone repo created: $output_dir
🎯 Project: $proto_name
📁 Files: [count] files copied
🔧 Dependencies: [cleaned/inlined/replaced count]
🚀 Git: [Initialized / Not initialized]

✅ Validation:
   - npm install: [Success/Failed]
   - Build: [Success/Failed/Skipped]
   - Tests: [Pass/Fail/Skipped/None]

📋 See detailed report: $output_dir/HATCH_NOTES.md

Next steps:
1. cd $output_dir
2. Review HATCH_NOTES.md for any manual actions
3. Update .env with your configuration
4. Test: npm run dev
5. Create GitHub repo and push
6. Deploy!

Optional - Archive in monorepo:
If this prototype is complete and you want to archive it in the
monorepo (optional):
   Update .project status to "GRADUATED"
   Move to ideas/graduated/ or prototypes/graduated/
```

## Tech Stack Specific Handling

### Node.js / TypeScript
- Ensure package.json has proper "name" (not workspace name)
- Check tsconfig.json doesn't reference workspace tsconfig
- Verify all @types/* packages are in devDependencies

### React / Vue / Frontend
- Update vite.config or webpack config (remove workspace aliases)
- Check for hardcoded API URLs pointing to monorepo services
- Ensure all assets referenced are included

### Python
- Create requirements.txt from shared deps if needed
- Check for imports from parent directories (../../)
- Ensure virtual env setup instructions in README

### Full-Stack
- Verify frontend and backend are both included
- Check for environment variable coordination
- Document multi-service startup in README

## Common Shared Dependencies

**Logger** → Replace with `winston`, `pino`, or `bunyan`
**HTTP client** → Replace with `axios`, `got`, or `fetch`
**Date utils** → Replace with `date-fns` or `dayjs`
**Validation** → Replace with `zod`, `joi`, or `yup`
**Testing utils** → Usually can be removed or replaced with framework tools

## Error Handling

**If source not found**:
```
❌ Error: Prototype '$proto_name' not found

Available prototypes:
  - proto-001-example
  - proto-002-another

Usage: /hatch <proto-name> [options]
```

**If output exists**:
```
❌ Error: Output directory already exists: $output_dir

Options:
1. Use different output: /hatch $proto_name --output-dir=../other-path
2. Remove existing: rm -rf $output_dir
3. Choose different name
```

**If dependencies can't be resolved**:
```
⚠️ Warning: Some dependencies couldn't be automatically resolved

See HATCH_NOTES.md for manual actions required.
The repo has been created but may need fixes before it runs.
```

## Best Practices

1. **Always validate** - Run install and build to catch issues
2. **Document everything** - HATCH_NOTES.md should be comprehensive
3. **Be conservative** - Include files if unsure (better than missing)
4. **Test the output** - Actually try to run the hatched project
5. **Preserve history** - Git commit message should reference origin
6. **Clean thoroughly** - Remove all monorepo references
7. **Update README** - Make it deployment-ready

## Usage Examples

**Hatch a prototype with defaults**:
```bash
/hatch proto-015-api-gateway
# Creates in ../hatch-output/proto-015-api-gateway/
# Initializes git
# Cleans dependencies
```

**Hatch to specific location**:
```bash
/hatch proto-015-api-gateway --output-dir=/Users/andrew/projects/api-gateway
```

**Hatch without git initialization**:
```bash
/hatch proto-015-api-gateway --init-git=false
```

**Keep monorepo dependencies for manual review**:
```bash
/hatch proto-015-api-gateway --clean-deps=false
# Leaves all imports as-is for manual cleanup
```

**Hatch from current directory**:
```bash
cd prototypes/proto-015-api-gateway
/hatch
# Infers proto-015-api-gateway from pwd
```

## Important Notes

- **XIP Projects**: If prototype has `-xip` suffix (AWS IP), warn before hatching and document in output
- **Incomplete ideas**: Warn if hatching phases 1-5 (not yet implemented)
- **No git push**: Never push to remote automatically (user decision)
- **Monorepo unchanged**: Original prototype remains in monorepo
- **Independent development**: Hatched repo is completely independent

## Post-Hatch

**In the hatched repo**:
- Develop independently
- Deploy to production
- Create issues/PRs as normal standalone project
- No connection to monorepo

**In the monorepo** (optional):
- Mark prototype as "GRADUATED" in .project
- Move to graduated/ folder if desired
- Update DASHBOARD.md
- Document success in LEARNINGS.md

---

**Remember**: Hatching creates a clean, standalone, production-ready repository. The goal is zero monorepo references and immediate deployability!
