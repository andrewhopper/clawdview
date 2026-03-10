# Acceptance Criteria Tool Guide

<!-- File UUID: 2b4c6d8e-0f1a-3b5c-7d9e-1a2b3c4d5e6f -->

## Overview

The Acceptance Criteria tool automatically generates and verifies task completion criteria to ensure work is truly complete before moving on.

## Quick Start

### Python API (Recommended for Claude Code)

```python
from shared.tools.acceptance_criteria import AcceptanceCriteria

# Define task context
context = {
    'task_type': 'html',
    'description': 'Generated landing page mockup',
    'files_affected': ['landing-page.html']
}

# Create and run verification
ac = AcceptanceCriteria(context)
ac.generate_criteria()
selected_ids = ac.present_criteria()
results = ac.execute_verification(selected_ids)

# Check results
if results['pass_rate'] == 100:
    print("✅ All acceptance criteria passed!")
else:
    print(f"⚠️ {results['failed']} criteria failed")
```

### CLI Usage

```bash
uv run --project /Users/andyhop/dev/lab python3 \
  /Users/andyhop/dev/lab/shared/tools/acceptance_criteria.py \
  --context '{
    "task_type": "html",
    "description": "Landing page mockup",
    "files_affected": ["landing-page.html"]
  }' \
  --output results.json
```

## Task Types

### HTML File (`task_type: 'html'`)

**Auto-generated criteria:**
1. File renders in browser (opens Chrome)
2. No console errors
3. Design tokens used (no raw hex colors)
4. Interactive elements work
5. Responsive on mobile/desktop

**Required context:**
- `files_affected`: List of HTML files

**Example:**
```json
{
  "task_type": "html",
  "description": "Product landing page",
  "files_affected": ["product-landing.html"]
}
```

### API Endpoint (`task_type: 'api'`)

**Auto-generated criteria:**
1. Endpoint is accessible
2. Health check passes
3. Auth required for protected routes
4. Test key user flows

**Required context:**
- `api_url`: API base URL

**Example:**
```json
{
  "task_type": "api",
  "description": "User registration API",
  "api_url": "https://api.staging.example.com"
}
```

### Deployment (`task_type: 'deployment'`)

**Auto-generated criteria:**
1. CloudFormation stack deployed
2. DNS resolves
3. URL accessible (HTTP 200)
4. Git hash matches deployed version
5. Core functionality works

**Required context:**
- `stack_name`: CloudFormation stack name (optional)
- `domain`: Domain name to verify (optional)

**Example:**
```json
{
  "task_type": "deployment",
  "description": "Deploy to staging",
  "stack_name": "my-app-staging",
  "domain": "staging.example.com"
}
```

### Code Feature (`task_type: 'code'`)

**Auto-generated criteria:**
1. All tests pass
2. Linting passes
3. Type checking passes
4. Feature works as expected

**Required context:**
- `description`: What was implemented

**Example:**
```json
{
  "task_type": "code",
  "description": "Add user profile editing"
}
```

### Bug Fix (`task_type: 'bugfix'`)

**Auto-generated criteria:**
1. Original bug no longer reproduces
2. All tests pass
3. Related features still work

**Required context:**
- `description`: What bug was fixed

**Example:**
```json
{
  "task_type": "bugfix",
  "description": "Fix registration form validation"
}
```

## Integration with Claude Code

### Automatic Triggering

When Claude Code completes a task, it should automatically:

1. Detect task type from context
2. Generate acceptance criteria
3. Present to user
4. Execute verification
5. Only mark complete if passes

### Example Flow

```python
# In Claude Code workflow after completing task

# 1. Analyze what was done
context = analyze_recent_actions()
# Returns: {
#   'task_type': 'html',
#   'files_affected': ['mockup.html'],
#   'description': 'Created landing page mockup'
# }

# 2. Run acceptance criteria
from shared.tools.acceptance_criteria import AcceptanceCriteria

ac = AcceptanceCriteria(context)
criteria = ac.generate_criteria()

# Show to user
print(f"Before marking complete, let's verify {len(criteria)} criteria...")

# Get user selection
selected = ac.present_criteria()

# Run verification
results = ac.execute_verification(selected)

# Report results
if results['pass_rate'] == 100:
    print("✅ All criteria passed - marking task complete")
    # Mark todo as completed
else:
    print(f"⚠️ {results['failed']} criteria failed")
    print("Options:")
    print("  [1] Fix issues and re-verify")
    print("  [2] Accept anyway (document reasons)")
    print("  [3] Mark incomplete")
```

## Verification Types

### Automated Checks

Run automatically without user interaction:
- Command execution (curl, grep, aws cli)
- File analysis
- Service health checks
- Git hash verification

### Manual Checks

Require user confirmation:
- Visual verification (does it look right?)
- Interactive testing (do buttons work?)
- UX testing (is it intuitive?)
- End-to-end workflows

## Results Format

```json
{
  "timestamp": "2026-01-28T10:30:00",
  "total": 5,
  "passed": 4,
  "failed": 1,
  "skipped": 0,
  "errors": 0,
  "pass_rate": 80.0,
  "results": [
    {
      "id": "1",
      "name": "File renders in browser",
      "status": "pass"
    },
    {
      "id": "2",
      "name": "No console errors",
      "status": "pass"
    },
    {
      "id": "3",
      "name": "Design tokens used",
      "status": "fail",
      "details": "Found raw hex colors on line 45"
    },
    {
      "id": "4",
      "name": "Interactive elements work",
      "status": "pass",
      "manual": true
    },
    {
      "id": "5",
      "name": "Responsive design",
      "status": "pass",
      "manual": true
    }
  ]
}
```

## Best Practices

1. **Always verify HTML files in browser** - Auto-opens Chrome for visual inspection
2. **Test deployed environments** - Use real URLs, not localhost
3. **Verify git hashes** - Ensure correct version is deployed
4. **Document accepted risks** - If proceeding with failures, note why
5. **Manual checks for UX** - Some things need human judgment

## Customization

### Adding Custom Criteria

```python
# After generating default criteria
ac = AcceptanceCriteria(context)
ac.generate_criteria()

# Add custom criterion
ac.criteria.append({
    'id': '99',
    'name': 'Brand colors match style guide',
    'type': 'manual',
    'prompt': 'Compare colors against brand guidelines'
})
```

### Custom Task Types

Create your own task type handlers:

```python
class CustomAcceptanceCriteria(AcceptanceCriteria):
    def _my_custom_type_criteria(self):
        return [
            {
                'id': '1',
                'name': 'Custom check',
                'type': 'automated',
                'command': 'my-custom-command',
                'success': 'Expected output'
            }
        ]
```

## Common Issues

### Issue: Browser doesn't open automatically

**Solution:** Check browser path in context:
```python
context = {
    'task_type': 'html',
    'browser_path': '/Applications/Google Chrome.app',
    'files_affected': ['file.html']
}
```

### Issue: Command timeouts

**Solution:** Commands timeout after 30 seconds by default. For longer operations, mark as manual check instead.

### Issue: AWS credentials expired

**Solution:** Refresh credentials before deployment verification:
```bash
eval $(isengardcli credentials andyhop+bedrock@amazon.com 2>/dev/null)
```

## See Also

- `/acceptance-criteria` skill documentation: `.claude/skills/acceptance-criteria.md`
- Ask Human tool: `shared/tools/ask_human.py`
- Design System guidelines: `shared/design-system/MANAGEMENT_GUIDELINES.md`
- Smoke Test Pattern: `shared/standards/testing/SMOKE_TEST_PATTERN.md`
