---
description: Add any shared tool to a project (error tracker, auth gateway, web fetch, etc.)
tags: [integration, shared-tools, reuse]
trigger: "add shared tool", "integrate shared tool", "add [tool-name] to"
---

# Add Shared Tool Skill

Generic integration skill for adding any shared tool to a project.

## Trigger Phrases

- "add [tool-name] to [project]"
- "integrate [tool-name] into [project]"
- "use [tool-name] in [project]"
- "add shared tool [tool-name]"

## Execution Steps

### Step 1: Identify Tool and Project

Use nav hints to resolve both references:

```python
import yaml

def find_project(query: str):
    """Find project or tool by alias."""
    with open('.claude/nav-hints/hints.yaml') as f:
        hints = yaml.safe_load(f)['hints']

    query_lower = query.lower()
    for hint in hints:
        for alias in hint['aliases']:
            if query_lower == alias.lower() or query_lower in alias.lower():
                return {
                    'path': hint['project_path'],
                    'description': hint.get('description', ''),
                    'type': 'shared' if 'shared' in hint['project_path'] else 'project'
                }
    return None

# Parse user request
tool = find_project("error tracker")  # Tool to add
target = find_project("gocoder")      # Project to add it to
```

### Step 2: Verify Tool is Shared

Check if tool is in `projects/shared/`:

```bash
if [[ {tool_path} == projects/shared/* ]]; then
  echo "✓ Shared tool found"
else
  echo "❌ Not a shared tool"
  exit 1
fi
```

### Step 3: Check Integration Documentation

Look for integration docs in the tool's directory:

```bash
cd {tool_path}

# Check for integration guides
if [ -f "INTEGRATION.md" ]; then
  cat INTEGRATION.md
elif [ -f "README.md" ]; then
  # Look for "Integration" or "Quick Start" section
  grep -A 20 -i "integration\|quick start\|usage" README.md
fi
```

### Step 4: Detect Project Type

Determine target project's tech stack:

```bash
cd {target_path}

# Check for package.json (Node.js)
if [ -f "package.json" ]; then
  TECH="node"
  grep "react\|next\|vite\|express" package.json
fi

# Check for requirements.txt (Python)
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
  TECH="python"
fi

# Check for go.mod (Go)
if [ -f "go.mod" ]; then
  TECH="go"
fi
```

### Step 5: Execute Integration

Based on tool and project type, execute appropriate integration:

**Common Integration Patterns:**

**1. npm Package**
```bash
cd {target_path}
npm install {package-name}
```

**2. Python Package**
```bash
cd {target_path}
pip install {package-name}
# or
poetry add {package-name}
```

**3. Script Tag (Static HTML)**
```html
<script src="{cdn-url}" data-config="{value}"></script>
```

**4. Import & Initialize**
```typescript
import { Tool } from '{package-name}';
Tool.init({ /* config */ });
```

### Step 6: Add Configuration

**Environment Variables:**

```bash
# Detect env file
if [ -f ".env" ]; then
  echo "{TOOL_CONFIG_KEY}={value}" >> .env
elif [ -f ".env.local" ]; then
  echo "{TOOL_CONFIG_KEY}={value}" >> .env.local
fi
```

**Config Files:**

```bash
# Create config file if tool requires it
cat > {target_path}/config/{tool-name}.json <<EOF
{
  "endpoint": "{value}",
  "apiKey": "{value}"
}
EOF
```

### Step 7: Update Documentation

Add integration note to project README:

```bash
cd {target_path}

# Add to README.md
cat >> README.md <<EOF

## Integrated Tools

- **{tool-name}** - {description}
  - Location: {tool_path}
  - Integration: {method}
  - Config: {config-location}
EOF
```

## Available Shared Tools

Common shared tools that can be integrated:

| Tool | Aliases | Type | Integration |
|------|---------|------|-------------|
| Error Tracker JS | error tracker, js error | Frontend | npm + init |
| Auth Gateway | auth, authentication | Service | API endpoint |
| Web Fetch Fallbacks | web fetch, fetch lib | Library | npm |
| Cookie Extractor | cookie, auth cookie | Library | npm |
| Audio Notetaker | mo, voice notes | Service | API + UI |

### Tool-Specific Instructions

**Error Tracker:**
- Use dedicated skill: `/skill add-error-tracker`
- npm: `@protoflow/error-tracker-js`
- Init in main entry point

**Auth Gateway:**
- API endpoint integration
- Add OAuth redirect URLs
- Configure Cognito user pool

**Web Fetch:**
- npm: `@protoflow/web-fetch-fallbacks`
- Progressive: curl → playwright → manual
- Config: timeout, retry logic

## Output Format

```
✓ Integrated {tool-name} into {project-name}

📦 Integration Method: {npm/pip/script/api}
📍 Location: {file-path}
🔧 Configuration: {config-location}

Changes made:
  • Added package: {package-name}
  • Initialized in: {entry-point}
  • Added config: {config-file}
  • Updated docs: README.md

Next steps:
  {tool-specific instructions}
```

## Error Handling

**Tool not found:**
```
❌ Could not find shared tool "{tool}".

Available shared tools:
  - error tracker (js error tracker)
  - auth (authentication gateway)
  - web fetch (fetch fallbacks)

Try: /workon {tool}
```

**No integration docs:**
```
⚠️ No integration documentation found for {tool}.

Checked:
  • {tool_path}/INTEGRATION.md
  • {tool_path}/README.md

Please check the tool's documentation manually:
  cd {tool_path}
  cat README.md
```

**Incompatible project type:**
```
⚠️ {tool} requires {required-type} but {project} is {actual-type}.

{tool} cannot be integrated into this project type.
Consider using an alternative or creating a compatibility layer.
```

## Examples

**Example 1: Add error tracker**
```
User: "add error tracker to gocoder"

1. Resolve "error tracker" → projects/shared/tool-error-tracker-js-et001
2. Resolve "gocoder" → projects/personal/active/tool-gocoder-web-...
3. Detect: React + Vite project
4. Install: npm install @protoflow/error-tracker-js
5. Initialize in: src/main.tsx
6. Add env vars: .env
7. Test integration
```

**Example 2: Add auth gateway**
```
User: "use shared auth in my avatar project"

1. Resolve "shared auth" → projects/shared/shared-auth-gateway
2. Resolve "avatar" → projects/personal/active/avatar-pipeline-53e47
3. Check auth gateway docs
4. Add API endpoint to .env
5. Configure OAuth callbacks
6. Add auth middleware
```

## Related Skills

- **Specific integrations:**
  - `/skill add-error-tracker` - Error tracker integration
  - `/skill add-auth` - Auth gateway integration (if exists)

- **Tool discovery:**
  - `/workon [tool-name]` - Navigate to shared tool
  - List shared tools: `ls projects/shared/`

---

**Version:** 1.0.0
**Created:** 2025-12-22
