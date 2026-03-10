# VS Code Workspace Management SOP

**Version:** 1.0
**Date:** 2025-12-18
**Purpose:** Manage large monorepos in VS Code without performance issues

---

## 1.0 PROBLEM

Opening the full monorepo (`~/dev/lab`) in VS Code causes:
1. Slow file watching (thousands of files)
2. Overwhelming search results
3. Difficult navigation
4. High memory/CPU usage

---

## 2.0 SOLUTION

**Multi-root workspaces** with shared resources:
- Each project gets its own workspace file
- Shared resources symlinked to `~/dev/hl-shared`
- Aggressive exclusions for build artifacts

---

## 3.0 SETUP

### 3.1 Create Shared Resources Directory (One-time)

```bash
mkdir -p ~/dev/hl-shared
cd ~/dev/hl-shared
ln -s ~/dev/lab/shared shared
ln -s ~/dev/lab/.claude .claude
ln -s ~/dev/lab/docs docs
```

### 3.2 Workspace File Template

Save as `~/dev/{project-name}.code-workspace`:

```json
{
  "folders": [
    {
      "name": "Project Name",
      "path": "/Users/andyhop/dev/lab/projects/{category}/{status}/{project-folder}"
    },
    {
      "name": "Shared Resources",
      "path": "/Users/andyhop/dev/hl-shared"
    }
  ],
  "settings": {
    "files.exclude": {
      "**/__pycache__": true,
      "**/.DS_Store": true,
      "**/*.pyc": true,
      "**/node_modules": true,
      "**/.venv": true,
      "**/dist": true,
      "**/build": true,
      "**/.next": true
    },
    "search.exclude": {
      "**/node_modules": true,
      "**/.venv": true,
      "**/dist": true,
      "**/build": true,
      "**/.next": true,
      "**/package-lock.json": true,
      "**/yarn.lock": true
    },
    "files.watcherExclude": {
      "**/node_modules/**": true,
      "**/.venv/**": true,
      "**/dist/**": true,
      "**/build/**": true,
      "**/.next/**": true
    },
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.eslint": "explicit"
    },
    "typescript.preferences.importModuleSpecifier": "relative"
  },
  "extensions": {
    "recommendations": [
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode",
      "bradlc.vscode-tailwindcss",
      "ms-python.python",
      "ms-python.vscode-pylance"
    ]
  }
}
```

---

## 4.0 USAGE

### 4.1 Open Workspace

```bash
code ~/dev/{project-name}.code-workspace
```

### 4.2 Create New Workspace

1. Copy template above
2. Replace `{project-name}` with actual project name
3. Update path to project directory
4. Adjust extensions recommendations if needed
5. Save to `~/dev/{project-name}.code-workspace`
6. Open with `code ~/dev/{project-name}.code-workspace`

### 4.3 Workspace Generator Script (Optional)

Create `~/dev/lab/bin/make-workspace`:

```bash
#!/bin/bash
# Usage: make-workspace ~/dev/lab/projects/personal/active/my-project

PROJECT_PATH="$1"
PROJECT_NAME=$(basename "$PROJECT_PATH")
WORKSPACE_FILE="$HOME/dev/${PROJECT_NAME}.code-workspace"

cat > "$WORKSPACE_FILE" << 'EOF'
{
  "folders": [
    {
      "name": "PROJECT_NAME_PLACEHOLDER",
      "path": "PROJECT_PATH_PLACEHOLDER"
    },
    {
      "name": "Shared Resources",
      "path": "/Users/andyhop/dev/hl-shared"
    }
  ],
  "settings": {
    "files.exclude": {
      "**/__pycache__": true,
      "**/.DS_Store": true,
      "**/node_modules": true,
      "**/.venv": true,
      "**/dist": true,
      "**/build": true
    },
    "search.exclude": {
      "**/node_modules": true,
      "**/.venv": true,
      "**/dist": true,
      "**/build": true
    },
    "files.watcherExclude": {
      "**/node_modules/**": true,
      "**/.venv/**": true,
      "**/dist/**": true,
      "**/build/**": true
    }
  }
}
EOF

# Replace placeholders
sed -i '' "s|PROJECT_NAME_PLACEHOLDER|$PROJECT_NAME|g" "$WORKSPACE_FILE"
sed -i '' "s|PROJECT_PATH_PLACEHOLDER|$PROJECT_PATH|g" "$WORKSPACE_FILE"

echo "Created: $WORKSPACE_FILE"
code "$WORKSPACE_FILE"
```

Make executable:
```bash
chmod +x ~/dev/lab/bin/make-workspace
```

---

## 5.0 BEST PRACTICES

1. **Never open full monorepo** - Always use workspaces
2. **One workspace per active project** - Don't mix unrelated projects
3. **Include shared resources** - Always add `~/dev/hl-shared` folder
4. **Aggressive exclusions** - Add all build artifacts to exclude lists
5. **Extension recommendations** - Tailor to project tech stack
6. **Naming convention** - `{project-name}.code-workspace` in `~/dev/`

---

## 6.0 EXAMPLES

### 6.1 GoCoder Workspace

File: `~/dev/gocoder.code-workspace`

```json
{
  "folders": [
    {
      "name": "GoCoder",
      "path": "/Users/andyhop/dev/lab/projects/personal/active/tool-gocoder-web-agentic-coding-ui-like-claude-code-web-t9x2k"
    },
    {
      "name": "Shared Resources",
      "path": "/Users/andyhop/dev/hl-shared"
    }
  ]
}
```

Open: `code ~/dev/gocoder.code-workspace`

### 6.2 Python API Workspace

File: `~/dev/my-api.code-workspace`

```json
{
  "folders": [
    {
      "name": "My API",
      "path": "/Users/andyhop/dev/lab/projects/work/active/my-api"
    },
    {
      "name": "Shared Resources",
      "path": "/Users/andyhop/dev/hl-shared"
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": ".venv/bin/python"
  },
  "extensions": {
    "recommendations": [
      "ms-python.python",
      "ms-python.vscode-pylance",
      "ms-python.black-formatter"
    ]
  }
}
```

---

## 7.0 TROUBLESHOOTING

### 7.1 Symlinks Not Working

**Symptom:** VS Code can't find files in `~/dev/hl-shared`

**Solution:**
```bash
# Verify symlinks
ls -la ~/dev/hl-shared
# Recreate if needed
rm -rf ~/dev/hl-shared
mkdir ~/dev/hl-shared && cd ~/dev/hl-shared
ln -s ~/dev/lab/shared shared
ln -s ~/dev/lab/.claude .claude
ln -s ~/dev/lab/docs docs
```

### 7.2 Still Slow Performance

**Symptom:** VS Code still slow with workspace

**Solutions:**
1. Add more exclusions to `files.watcherExclude`
2. Disable unused extensions in workspace
3. Use VS Code Profiles for different workflows
4. Check disk I/O with Activity Monitor

### 7.3 Extensions Not Loading

**Symptom:** Recommended extensions not installing

**Solution:**
1. Open workspace
2. View → Command Palette → "Extensions: Show Recommended Extensions"
3. Install All Workspace Recommendations

---

## 8.0 MAINTENANCE

1. **Update exclusions** when adding new build tools
2. **Archive old workspaces** when projects complete
3. **Keep shared resources updated** - they're symlinks, auto-update
4. **Review extension recommendations** quarterly

---

[END SOP]
