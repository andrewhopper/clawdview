---
name: acceptance-criteria
description: Capture and verify task completion with pre-populated acceptance criteria
version: 1.1.0
aliases:
  - verify
  - check-complete
  - acceptance
integrates_with:
  - flightcontrol
  - pre-code-gate
---
<!-- File UUID: 7c9e2f4a-1b3d-4e8c-9a2f-5d6e7f8a9b0d -->

# Acceptance Criteria Skill

**Auto-generate verification steps, confirm with user, execute checks**

## Purpose

Ensures tasks are truly complete by:
1. Pre-populating acceptance criteria from context
2. Allowing user confirmation/modification
3. Executing verification steps
4. Reporting pass/fail status

## When to Use

**Automatically trigger after:**
- File generation (HTML, configs, code)
- Deployments (infrastructure, frontend, API)
- Feature implementations
- Bug fixes
- Refactoring

**Manually invoke:**
```bash
/acceptance-criteria
/verify
/check-complete
```

## Execution Flow

```
┌──────────────────────────────────────────────┐
│ 1. ANALYZE CONTEXT                           │
│    - What was just done?                     │
│    - What files were created/modified?       │
│    - What type of task was it?               │
└────────────────┬─────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────┐
│ 2. GENERATE CRITERIA                         │
│    - Context-aware acceptance criteria       │
│    - Verification steps                      │
│    - Success indicators                      │
└────────────────┬─────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────┐
│ 3. PRESENT TO USER                           │
│    - Show suggested criteria (checkboxes)    │
│    - Allow add/remove/modify                 │
│    - Get confirmation                        │
└────────────────┬─────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────┐
│ 4. EXECUTE VERIFICATION                      │
│    - Run automated checks                    │
│    - Prompt for manual verification          │
│    - Collect results                         │
└────────────────┬─────────────────────────────┘
                 ▼
┌──────────────────────────────────────────────┐
│ 5. REPORT RESULTS                            │
│    - Pass/fail per criterion                 │
│    - Overall status                          │
│    - Next steps if failures                  │
└──────────────────────────────────────────────┘
```

## Context-Aware Criteria Generation

### HTML/Frontend Files
**Generated Criteria:**
1. [ ] File renders without errors in browser
2. [ ] All interactive elements work
3. [ ] Design system tokens used (no raw hex)
4. [ ] Responsive on mobile/desktop
5. [ ] No console errors

**Verification Steps:**
- Open file in browser (auto-launch Chrome)
- Check browser console for errors
- Test interactive elements
- Inspect color usage (search for `#`)

### API Endpoints
**Generated Criteria:**
1. [ ] Endpoint returns expected status code
2. [ ] Response schema matches specification
3. [ ] Error handling works correctly
4. [ ] Authentication/authorization enforced
5. [ ] Performance within acceptable range

**Verification Steps:**
- `curl` with valid/invalid inputs
- Check response JSON structure
- Test auth flows
- Measure response time

### Infrastructure/Deployment
**Generated Criteria:**
1. [ ] CloudFormation/CDK stack deployed successfully
2. [ ] All resources created (verify in console)
3. [ ] DNS records resolve correctly
4. [ ] URLs return HTTP 200
5. [ ] Git hash matches deployed version

**Verification Steps:**
- Check stack status
- `aws cloudformation describe-stacks`
- `dig` domain names
- `curl -I` URLs
- Check buildinfo.json

### Code Changes
**Generated Criteria:**
1. [ ] All tests pass
2. [ ] No linting errors
3. [ ] Type checking passes
4. [ ] Function works as expected
5. [ ] No breaking changes to API

**Verification Steps:**
- Run test suite
- Run linter
- Run type checker
- Manual testing if needed

### Bug Fixes
**Generated Criteria:**
1. [ ] Original bug no longer reproduces
2. [ ] Fix doesn't introduce new issues
3. [ ] Related functionality still works
4. [ ] Tests added to prevent regression

**Verification Steps:**
- Reproduce original bug (should fail now)
- Run full test suite
- Check related features

## User Interaction Format

### Step 1: Present Criteria

```
Acceptance Criteria for: [Task Description]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on context, I suggest these verification steps:

AUTOMATED CHECKS (will run automatically):
  [1] ✓ File renders in browser without errors
  [2] ✓ No console errors
  [3] ✓ Design system tokens used (no raw hex)

MANUAL CHECKS (will prompt you):
  [4] ✓ Interactive elements work as expected
  [5] ✓ Design looks correct on mobile/desktop

OPTIONAL:
  [6] ○ Add to artifact library for reuse
  [7] ○ Share with team

Actions:
  [a] Accept all - run verification
  [r] Remove criteria (comma-separated IDs)
  [+] Add custom criterion
  [m] Mark some as manual (comma-separated IDs)
  [s] Skip verification for now

Your choice:
```

### Step 2: Execute Verification

```
Running verification...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/5] File renders in browser...
      ✅ PASS - Opened example.html in Chrome

[2/5] Console errors check...
      ✅ PASS - No errors found

[3/5] Design token check...
      ❌ FAIL - Found raw hex colors:
          Line 45: background-color: #1a1a2e
          Line 78: color: #ff6b6b
      Fix: Replace with hsl(var(--background))

[4/5] Interactive elements... (MANUAL)
      Does the button toggle the menu? [y/n]: y
      ✅ PASS - User confirmed

[5/5] Mobile responsive... (MANUAL)
      Resize browser to mobile width.
      Does layout adapt correctly? [y/n]: y
      ✅ PASS - User confirmed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results: 4/5 passed (80%)

❌ FAILED CRITERIA:
  [3] Design token check - Raw hex colors found

Next steps:
  [1] Fix failures and re-run verification
  [2] Accept anyway (document reasons)
  [3] Mark task as incomplete

Your choice:
```

## Criteria Templates by Task Type

### Template: HTML File Generation
```yaml
automated:
  - name: File renders without errors
    command: open -a "Google Chrome" {file_path}
    success: "Page loads successfully"
  - name: No console errors
    command: Check browser console
    success: "No errors in console"
  - name: Design system compliance
    command: grep -n '#[0-9a-fA-F]\{6\}' {file_path}
    success: "No matches found"

manual:
  - name: Interactive elements work
    prompt: "Test all buttons, forms, and interactions"
  - name: Responsive design
    prompt: "Resize browser - does layout adapt?"
```

### Template: API Deployment
```yaml
automated:
  - name: Endpoint is accessible
    command: curl -I {api_url}
    success: "HTTP/2 200"
  - name: Health check passes
    command: curl {api_url}/health
    success: "status: ok"
  - name: Auth required
    command: curl {api_url}/protected
    success: "HTTP/2 401"

manual:
  - name: Test key flows
    prompt: "Test primary user workflows end-to-end"
```

### Template: Infrastructure Deployment
```yaml
automated:
  - name: Stack deployed
    command: aws cloudformation describe-stacks --stack-name {stack_name}
    success: "StackStatus: CREATE_COMPLETE"
  - name: DNS resolves
    command: dig {domain_name} +short
    success: "Returns IP address"
  - name: URL accessible
    command: curl -I https://{domain_name}
    success: "HTTP/2 200"
  - name: Git hash matches
    command: curl https://{domain_name}/buildinfo.json
    success: "git_hash matches current commit"

manual:
  - name: Services functional
    prompt: "Test core functionality in deployed environment"
```

### Template: Code Feature
```yaml
automated:
  - name: Tests pass
    command: npm test
    success: "All tests passed"
  - name: Linting passes
    command: npm run lint
    success: "No issues found"
  - name: Type checking
    command: npm run typecheck
    success: "No errors"

manual:
  - name: Feature works
    prompt: "Test the new feature manually"
  - name: No breaking changes
    prompt: "Verify existing features still work"
```

## Integration with TodoWrite

When todo is marked `completed`, automatically trigger acceptance criteria:

```
Assistant: "Great! Before marking this complete, let me verify..."
           [Launches acceptance criteria flow]
           [Presents suggested checks]
           [Executes verification]
           [Only marks complete if all pass OR user accepts anyway]
```

**Configuration** (in `.project` file):
```yaml
acceptance_criteria:
  auto_verify: true  # Auto-trigger on todo completion
  strict_mode: false # Allow proceeding with failures
  templates:
    - html-mockup
    - api-deployment
```

## Integration with Flightcontrol

When user starts session with `/flightcontrol`:

**Step 1: Import Criteria from Flight Plan**
```
Reading flight plan: .system/flight-plans/{session-id}.md
Found acceptance criteria:
  - User-defined (3 criteria)
  - Auto-generated (5 criteria)

Loading criteria for verification...
```

**Step 2: Merge with Context-Aware Criteria**
```
Flight Plan Criteria:
  [1] ✓ Users can sign in and stay signed in
  [2] ✓ App deployed to dev.ppm.b.lfg.new

Additional Context-Aware Criteria:
  [3] ✓ DNS records resolve (dig dev.ppm.b.lfg.new)
  [4] ✓ Git hash matches deployed version
  [5] ✓ Auth flow works end-to-end

Proceed with verification? [Y/n]:
```

**Step 3: Execute & Report to Flightcontrol**
```
After verification completes:
  - Update flight plan with results
  - Write results to .system/flight-plans/{session-id}.md
  - Return summary to Flightcontrol for debrief
```

**Shared Data Format:**
```yaml
# .system/flight-plans/{session-id}.md
acceptance_criteria:
  user_defined:
    - id: uc-1
      criterion: "Users can sign in and stay signed in"
      type: manual
      verified: true
      verified_at: "2026-01-28T15:30:00Z"
      result: pass

  auto_generated:
    - id: ag-1
      criterion: "App deployed to dev.ppm.b.lfg.new"
      type: automated
      command: "curl -I https://dev.ppm.b.lfg.new"
      success_indicator: "HTTP/2 200"
      verified: true
      verified_at: "2026-01-28T15:28:00Z"
      result: pass
      output: "HTTP/2 200 OK"

    - id: ag-2
      criterion: "Git hash matches deployed version"
      type: automated
      command: "curl https://dev.ppm.b.lfg.new/buildinfo.json | jq -r .git_hash"
      success_indicator: "a7f3b2c"
      verified: true
      verified_at: "2026-01-28T15:29:00Z"
      result: pass
      output: "a7f3b2c"

verification_summary:
  total: 3
  passed: 3
  failed: 0
  pass_rate: 100%
  verified_at: "2026-01-28T15:30:00Z"
```

## Implementation Guidelines

### Step 1: Context Analysis
```python
def analyze_context(conversation_history, recent_actions):
    """
    Analyze what was just done to infer criteria.

    Signals:
    - Files created/modified (Read, Write, Edit tools used)
    - Deployment commands (make deploy, aws cloudformation)
    - Test runs (npm test, pytest)
    - Todo completions (TodoWrite with status: completed)
    """
    context = {
        'task_type': detect_task_type(recent_actions),
        'files_affected': extract_files(recent_actions),
        'commands_run': extract_commands(recent_actions),
        'tech_stack': infer_tech_stack(files_affected)
    }
    return context
```

### Step 2: Criteria Generation
```python
def generate_criteria(context):
    """
    Generate acceptance criteria based on context.

    Returns list of criteria with:
    - id: unique identifier
    - name: human-readable description
    - type: 'automated' | 'manual'
    - verification: command or prompt
    - success_indicator: what indicates pass
    """
    template = load_template(context['task_type'])
    criteria = []

    for criterion in template:
        # Populate placeholders
        populated = substitute_vars(criterion, context)
        criteria.append(populated)

    # Add context-specific criteria
    if context['tech_stack'] == 'html':
        criteria.append({
            'name': f"Open {context['files_affected'][0]} in browser",
            'type': 'automated',
            'verification': f"open -a 'Google Chrome' {file_path}",
            'success_indicator': 'Browser opens, page renders'
        })

    return criteria
```

### Step 3: User Confirmation
Use `ask_human.py` tool with `multi-choice` template:

```python
from shared.tools.ask_human import ask_human

result = ask_human("multi-choice", {
    "title": "Acceptance Criteria - Confirm verification steps",
    "description": "Select which criteria to verify (uncheck to skip)",
    "options": [
        {
            "id": str(i),
            "label": criterion['name'],
            "description": f"{criterion['type'].upper()}: {criterion['verification']}"
        }
        for i, criterion in enumerate(criteria)
    ]
})

selected_ids = result['selected']
```

### Step 4: Execute Verification
```python
async def execute_verification(criteria, selected_ids):
    """
    Run verification steps for selected criteria.
    """
    results = []

    for criterion in criteria:
        if criterion['id'] not in selected_ids:
            results.append({'id': criterion['id'], 'status': 'skipped'})
            continue

        if criterion['type'] == 'automated':
            result = await run_automated_check(criterion)
        else:
            result = await run_manual_check(criterion)

        results.append(result)

    return results

async def run_automated_check(criterion):
    """Execute command and check output."""
    try:
        output = subprocess.run(
            criterion['verification'],
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        passed = criterion['success_indicator'] in output.stdout

        return {
            'id': criterion['id'],
            'name': criterion['name'],
            'status': 'pass' if passed else 'fail',
            'output': output.stdout[:200],  # Truncate
            'details': output.stderr if not passed else None
        }
    except Exception as e:
        return {
            'id': criterion['id'],
            'name': criterion['name'],
            'status': 'error',
            'error': str(e)
        }

async def run_manual_check(criterion):
    """Prompt user for manual verification."""
    result = ask_human("approve-deny", {
        "title": criterion['name'],
        "description": criterion['verification']
    })

    return {
        'id': criterion['id'],
        'name': criterion['name'],
        'status': 'pass' if result == 'approved' else 'fail',
        'manual': True
    }
```

### Step 5: Report Results
```python
def format_results(results, criteria):
    """Format verification results for display."""
    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'pass')
    failed = sum(1 for r in results if r['status'] == 'fail')
    skipped = sum(1 for r in results if r['status'] == 'skipped')

    report = f"""
Verification Complete
{'='*50}

Results: {passed}/{total} passed ({passed/total*100:.0f}%)

✅ PASSED ({passed}):
"""

    for r in results:
        if r['status'] == 'pass':
            report += f"  [{r['id']}] {r['name']}\n"

    if failed > 0:
        report += f"\n❌ FAILED ({failed}):\n"
        for r in results:
            if r['status'] == 'fail':
                report += f"  [{r['id']}] {r['name']}\n"
                if 'details' in r:
                    report += f"      {r['details']}\n"

    if skipped > 0:
        report += f"\n⊘ SKIPPED ({skipped})\n"

    return report
```

## Examples

### Example 1: HTML File Verification

**Context:** Just created `landing-page.html`

**Generated Criteria:**
```
Acceptance Criteria for: landing-page.html
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTOMATED:
  [1] ✓ File renders in browser
  [2] ✓ No console errors
  [3] ✓ Design tokens used (no raw hex)
  [4] ✓ No accessibility errors

MANUAL:
  [5] ✓ Interactive elements work
  [6] ✓ Responsive on mobile

Your choice: a (accept all)

Running verification...

[1/6] Opening landing-page.html in Chrome...
      ✅ PASS

[2/6] Checking console for errors...
      ✅ PASS - No errors

[3/6] Checking for raw hex colors...
      ✅ PASS - All colors use design tokens

[4/6] Running accessibility check...
      ⚠️  WARNING - 2 contrast issues found
      Details: Button text contrast ratio 3.2:1 (should be 4.5:1)

[5/6] Do interactive elements work? [y/n]: y
      ✅ PASS

[6/6] Is layout responsive on mobile? [y/n]: y
      ✅ PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results: 5/6 passed, 1 warning (83%)

⚠️  WARNINGS:
  [4] Accessibility - Button contrast too low

Next steps:
  [1] Fix warning and re-verify
  [2] Accept with documented risk
  [3] Mark incomplete

Your choice: 2

Documented risk: "Contrast warning - will fix in next iteration"
✅ Task marked complete with 1 known issue
```

### Example 2: API Deployment

**Context:** Just deployed API to staging

**Generated Criteria:**
```
Acceptance Criteria for: API deployment to staging
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTOMATED:
  [1] ✓ CloudFormation stack deployed
  [2] ✓ API Gateway endpoint accessible
  [3] ✓ Health check returns 200
  [4] ✓ Auth required for protected routes
  [5] ✓ Git hash matches deployed version

MANUAL:
  [6] ✓ Test create user flow
  [7] ✓ Test authentication flow

Your choice: a

Running verification...

[1/7] Checking CloudFormation stack...
      ✅ PASS - Stack status: UPDATE_COMPLETE

[2/7] Testing API endpoint...
      ✅ PASS - https://api.staging.example.com returns 200

[3/7] Health check...
      ✅ PASS - /health returns {"status": "ok"}

[4/7] Auth protection...
      ✅ PASS - GET /protected returns 401 without token

[5/7] Git hash verification...
      ✅ PASS - Deployed: a7f3b2c, Current: a7f3b2c

[6/7] Test create user flow (manual)
      Open Postman and create a test user. Success? [y/n]: y
      ✅ PASS

[7/7] Test authentication flow (manual)
      Sign in with test user and get token. Success? [y/n]: y
      ✅ PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results: 7/7 passed (100%)

✅ All acceptance criteria passed!
✅ Task marked complete
```

### Example 3: Bug Fix

**Context:** Fixed bug in user registration

**Generated Criteria:**
```
Acceptance Criteria for: Fix user registration bug
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTOMATED:
  [1] ✓ Original bug no longer reproduces
  [2] ✓ All tests pass
  [3] ✓ No new console errors

MANUAL:
  [4] ✓ Related features still work
  [5] ✓ No unexpected side effects

Your choice: a

Running verification...

[1/5] Attempting to reproduce original bug...
      Test: Register with duplicate email
      ✅ PASS - Now returns proper error (was crashing before)

[2/5] Running test suite...
      ✅ PASS - 87 tests, 0 failures

[3/5] Checking for new errors...
      ✅ PASS - No new errors in logs

[4/5] Do related features still work? (manual)
      Test: Login, password reset, email verification
      Try these flows now. All working? [y/n]: y
      ✅ PASS

[5/5] Any unexpected side effects? (manual)
      Did you notice anything unusual? [y/n]: n
      ✅ PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results: 5/5 passed (100%)

✅ All acceptance criteria passed!
✅ Task marked complete
```

## Configuration Options

### Per-Project Settings (.project file)
```yaml
acceptance_criteria:
  enabled: true
  auto_trigger: true  # Auto-run on todo completion
  strict_mode: false  # Allow failures with documentation

  default_templates:
    - html-file
    - api-endpoint

  custom_criteria:
    - name: "Brand compliance"
      type: manual
      prompt: "Does this match brand guidelines?"
```

### Global Settings (~/.claude/settings.json)
```json
{
  "acceptance_criteria": {
    "browser_path": "/Applications/Google Chrome.app",
    "default_timeout": 30,
    "skip_on_spike": true,
    "require_for_phase_transition": true
  }
}
```

## Benefits

1. **Catches incomplete work** - No more "done" when it's not tested
2. **Consistent verification** - Same checks every time
3. **Documentation** - Acceptance criteria become part of record
4. **Learning** - Junior devs see what "done" means
5. **Quality gate** - Prevents moving forward with broken work

## Best Practices

1. **Always verify HTML files in browser** - Don't assume it works
2. **Test auth flows end-to-end** - Not just unit tests
3. **Check deployed version** - Git hash verification catches wrong deploys
4. **Manual checks for UX** - Some things need human judgment
5. **Document accepted risks** - If proceeding with failures, write why

## Edge Cases

**What if verification fails?**
- Offer to fix and re-verify
- Allow proceeding with documented risk
- Mark task incomplete

**What if user skips verification?**
- Warn that task may not be complete
- Offer to run later with `/acceptance-criteria`
- Log skipped verification

**What if automated check hangs?**
- 30-second timeout
- Mark as error, offer manual verification
- Continue with remaining checks

**What if no criteria can be inferred?**
- Ask user what success looks like
- Offer common templates to choose from
- Save custom criteria for future