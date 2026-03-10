# Guardrail Enforcement System - Testing Guide

## System Overview

The guardrail enforcement system consists of three integrated components:

1. **Hook-Based Validation** - `.claude/hooks/tool-result.sh` runs after each file operation
2. **Grace Period Validator** - `grace_period_validator.py` checks for evidence after 30s timeout
3. **Batch Detector** - `batch_detector.py` handles bulk file generation intelligently

## Test Scenarios

### Scenario 1: Single File Creation (Grace Period)

**What to test:** Grace period works, evidence checking prevents false positives

**Steps:**

```bash
# 1. Create a single HTML file
echo "<html><body>Test Site</body></html>" > test-single.html

# 2. Wait and observe
# Expected: Grace period validator starts watching (30s timeout)

# 3. Check pending validations
python3 .guardrails/ai-steering/grace_period_validator.py check

# Expected output (after 30s):
# 🤖 GRACE PERIOD EXPIRED - REMINDERS:
# ⚠️ REMINDER: File 'test-single.html' was created 30 seconds ago but not published to S3.
# Prompt user: 'Publish test-single.html to S3? [1] Public [2] Temp [3] Private [4] Skip'
```

**Verify grace period state:**
```bash
cat .guardrails/.pending_validations.json
# Should show test-single.html with check_after timestamp
```

---

### Scenario 2: Single File with Evidence (No Reminder)

**What to test:** Evidence checking prevents false positives

**Steps:**

```bash
# 1. Create HTML file
echo "<html><body>Test Site 2</body></html>" > test-evidence.html

# 2. Create skip marker BEFORE grace period expires
touch .s3-skip

# 3. Wait 30+ seconds, then check
python3 .guardrails/ai-steering/grace_period_validator.py check

# Expected output:
# ✅ No reminders needed
```

**Alternative evidence sources:**
```bash
# Option A: Create bookmark file
mkdir -p bookmarks
cat > bookmarks/test-evidence.url <<EOF
[InternetShortcut]
URL=https://bucket.s3.region.amazonaws.com/test-evidence.html
EOF

# Option B: Create skip marker in file directory
touch test-evidence.html.s3-published

# Option C: Commit with S3 mention in commit message
git add test-evidence.html
git commit -m "Add test-evidence.html and publish to S3"
```

---

### Scenario 3: Auto-Detected Batch Mode

**What to test:** Rapid file creation triggers batch mode automatically

**Steps:**

```bash
# 1. Clear any existing batch state
rm -f .guardrails/.batch_operation.json .guardrails/.file_history.json

# 2. Create 3+ files rapidly (within 10 seconds)
for i in {1..5}; do
  echo "<html><body>Page $i</body></html>" > test-batch-$i.html
  python3 .guardrails/ai-steering/batch_detector.py track test-batch-$i.html
done

# Expected output (after 3rd file):
# 📦 Auto-detected batch: 3 files

# 3. Check batch status
python3 .guardrails/ai-steering/batch_detector.py check

# Expected output:
# 📦 Batch active: 5 files
#    Idle: 0s
```

**Verify batch state:**
```bash
cat .guardrails/.batch_operation.json
# Should show:
# {
#   "active": true,
#   "declared": false,
#   "auto_detected": true,
#   "file_type": "html",
#   "expected_count": null,
#   "actual_count": 5,
#   "files": ["test-batch-1.html", ...]
# }
```

**Wait for batch completion:**
```bash
# Wait 30+ seconds without creating more files

# Check status
python3 .guardrails/ai-steering/batch_detector.py check

# Expected output:
# ✅ Batch generation complete: 5 html files created.
# Would you like to publish all files to S3?
#   [1] Publish all (bulk operation)
#   [2] Skip all
#   [3] Select individually
```

---

### Scenario 4: Pre-Declared Batch Mode

**What to test:** AI declares batch upfront (Rule 27 compliance)

**Steps:**

```bash
# 1. Clear batch state
rm -f .guardrails/.batch_operation.json .guardrails/.file_history.json

# 2. Declare batch BEFORE creating files
python3 .guardrails/ai-steering/batch_detector.py declare --count 10 --type html

# Expected output:
# ✅ Batch mode active: Expecting 10 html files. Grace periods paused.

# 3. Create files (grace periods will be skipped)
for i in {1..10}; do
  echo "<html><body>Declared Page $i</body></html>" > test-declared-$i.html
  python3 .guardrails/ai-steering/batch_detector.py track test-declared-$i.html
done

# Expected output (after each file):
# 📦 Batch mode active: 3/10 files
# 📦 Batch mode active: 4/10 files
# ...

# 4. Complete batch manually
python3 .guardrails/ai-steering/batch_detector.py complete

# Expected output:
# ✅ Batch generation complete: 10 html files created.
# Would you like to publish all files to S3?
#   [1] Publish all (bulk operation)
#   [2] Skip all
#   [3] Select individually
```

---

### Scenario 5: Hook Integration Test

**What to test:** `.claude/hooks/tool-result.sh` integrates batch detection + grace period

**Prerequisites:**
```bash
# Ensure hook is executable
chmod +x .claude/hooks/tool-result.sh
```

**Steps:**

```bash
# 1. Simulate Write tool execution (single file)
.claude/hooks/tool-result.sh Write "" "File created successfully at: test-hook.html"

# Expected: Grace period starts (30s timeout)

# 2. Check logs
tail -n 20 .guardrails/.supervisor.log

# Expected output:
# [2025-11-24 10:30:00] [GracePeriod] Added pending validation: test-hook.html (check after 30s)
# [2025-11-24 10:30:00] [GracePeriod] Watching test-hook.html for 30 seconds...

# 3. Simulate non-file tool execution (triggers validation check)
.claude/hooks/tool-result.sh Bash "" "Command executed successfully"

# After 30s, expected output:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🤖 GRACE PERIOD EXPIRED - REMINDERS:
# ⚠️ REMINDER: File 'test-hook.html' was created 30 seconds ago but not published to S3.
# Prompt user: 'Publish test-hook.html to S3? [1] Public [2] Temp [3] Private [4] Skip'
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Scenario 6: Batch Detection via Hook

**What to test:** Hook auto-detects batches and shows completion message

**Steps:**

```bash
# 1. Clear batch state
rm -f .guardrails/.batch_operation.json .guardrails/.file_history.json

# 2. Simulate rapid file creation via hook
for i in {1..4}; do
  .claude/hooks/tool-result.sh Write "" "File created successfully at: test-hook-batch-$i.html"
done

# Expected: After 3rd file, batch mode activates

# 3. Simulate non-file operation after 30s idle (triggers batch completion check)
sleep 31
.claude/hooks/tool-result.sh Bash "" "Command executed"

# Expected output:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✅ Batch generation complete: 4 html files created.
# Would you like to publish all files to S3?
#   [1] Publish all (bulk operation)
#   [2] Skip all
#   [3] Select individually
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Verification Commands

### Check System Status

```bash
# 1. Check if hook is executable
ls -la .claude/hooks/tool-result.sh
# Expected: -rwxr-xr-x (executable flag set)

# 2. Check grace period state
cat .guardrails/.pending_validations.json
# Shows files waiting for validation

# 3. Check batch state
cat .guardrails/.batch_operation.json
# Shows current batch operation status

# 4. Check file creation history
cat .guardrails/.file_history.json
# Shows recent file creations for auto-detection

# 5. View logs
tail -f .guardrails/.supervisor.log
# Live stream of validation events
```

### Manual Validation Check

```bash
# Check specific file for violations
python3 .guardrails/ai-steering/validate_periodic.py check test.html

# Check all files in directory
python3 .guardrails/ai-steering/validate_periodic.py check prototypes/proto-test/

# View ESLint-style report
python3 .guardrails/ai-steering/validate_periodic.py report

# Auto-fix violations (if possible)
python3 .guardrails/ai-steering/validate_periodic.py fix prototypes/proto-test/
```

---

## Configuration Tuning

### Adjust Timeouts

Edit thresholds in `batch_detector.py`:

```python
# Auto-detection thresholds
RAPID_CREATION_THRESHOLD = 3  # 3+ files in 10 seconds = batch mode
RAPID_CREATION_WINDOW = 10  # seconds
BATCH_IDLE_TIMEOUT = 30  # No files for 30s = batch complete
```

Edit grace period in `grace_period_validator.py`:

```python
DEFAULT_TIMEOUT = 30  # seconds
```

### Configure Publishable Extensions

Edit extensions in `grace_period_validator.py`:

```python
PUBLISHABLE_EXTENSIONS = {".html", ".pdf", ".svg", ".zip", ".mp3", ".mp4"}
```

---

## Troubleshooting

### Issue: Grace periods not starting

**Check:**
```bash
# 1. Verify hook is executable
ls -la .claude/hooks/tool-result.sh

# 2. Run hook manually
.claude/hooks/tool-result.sh Write "" "File created successfully at: test.html"

# 3. Check logs for errors
tail -n 50 .guardrails/.supervisor.log
```

**Fix:**
```bash
chmod +x .claude/hooks/tool-result.sh
```

---

### Issue: Batch mode not activating

**Check:**
```bash
# 1. Verify file history is being tracked
cat .guardrails/.file_history.json

# 2. Check if files are created within RAPID_CREATION_WINDOW (10s)
python3 .guardrails/ai-steering/batch_detector.py check
```

**Fix:**
```bash
# Lower threshold for testing
# Edit batch_detector.py:
RAPID_CREATION_THRESHOLD = 2  # Was 3
```

---

### Issue: False positive reminders (evidence not detected)

**Check:**
```bash
# 1. Verify evidence exists
ls -la .s3-skip
ls -la bookmarks/test.url
git log -5 --oneline | grep -i s3

# 2. Test evidence checker manually
python3 -c "
from pathlib import Path
from grace_period_validator import S3PublishEvidenceChecker

checker = S3PublishEvidenceChecker(Path('test.html'))
print(f'Evidence found: {checker.has_evidence()}')
"
```

**Fix:**
```bash
# Add evidence markers
touch .s3-skip  # Skip all files in directory
# OR
touch test.html.s3-published  # Skip specific file
# OR
mkdir -p bookmarks && cat > bookmarks/test.url <<EOF
[InternetShortcut]
URL=https://bucket.s3.amazonaws.com/test.html
EOF
```

---

## End-to-End Test Script

**Full system test:**

```bash
#!/bin/bash
# test_guardrails.sh - Comprehensive guardrail system test

echo "=== Guardrail Enforcement System Test ==="
echo ""

# Clean state
echo "1. Cleaning previous state..."
rm -f .guardrails/.batch_operation.json \
      .guardrails/.file_history.json \
      .guardrails/.pending_validations.json
rm -f test-*.html

echo "2. Testing single file (grace period)..."
echo "<html>Single</html>" > test-single.html
.claude/hooks/tool-result.sh Write "" "File created successfully at: test-single.html"
sleep 2

echo "3. Testing auto-detected batch..."
for i in {1..4}; do
  echo "<html>Batch $i</html>" > test-batch-$i.html
  .claude/hooks/tool-result.sh Write "" "File created successfully at: test-batch-$i.html"
done
sleep 2

echo "4. Checking batch status..."
python3 .guardrails/ai-steering/batch_detector.py check

echo ""
echo "5. Waiting for batch idle timeout (30s)..."
sleep 31

echo "6. Triggering batch completion check..."
.claude/hooks/tool-result.sh Bash "" "Command executed"

echo ""
echo "7. Checking grace period for single file..."
python3 .guardrails/ai-steering/grace_period_validator.py check

echo ""
echo "=== Test Complete ==="
echo "Check .guardrails/.supervisor.log for detailed logs"
```

**Run test:**
```bash
chmod +x test_guardrails.sh
./test_guardrails.sh
```

---

## Expected Behavior Summary

| Scenario | Grace Period | Batch Mode | Reminder |
|----------|-------------|------------|----------|
| Single file, no evidence | ✅ 30s | ❌ | ✅ After timeout |
| Single file, with evidence | ✅ 30s | ❌ | ❌ Evidence found |
| 3+ files rapidly | ❌ Skipped | ✅ Auto-detect | ❌ Until batch complete |
| Declared batch | ❌ Skipped | ✅ Pre-declared | ❌ Until batch complete |
| Batch idle 30s | N/A | ✅ → Complete | ✅ Bulk publish prompt |

---

## Next Steps

1. **Run basic tests** - Verify single file and batch scenarios work
2. **Check evidence detection** - Test all evidence sources (skip markers, bookmarks, git)
3. **Tune timeouts** - Adjust grace period and batch idle timeouts if needed
4. **Monitor logs** - Watch `.guardrails/.supervisor.log` during AI sessions
5. **Validate Rule 27** - Ensure AI declares batch count upfront per CLAUDE.md

---

## Integration with Claude Code

**How it works in practice:**

1. **User asks:** "Create a cat lovers website"
2. **AI creates:** `index.html` using Write tool
3. **Hook runs:** `.claude/hooks/tool-result.sh` detects file creation
4. **Grace period starts:** 30-second timeout begins
5. **AI sees:** Tool result (file created successfully)
6. **After 30s (if no S3 publish):** Hook injects reminder into next tool result
7. **Claude sees:** "⚠️ REMINDER: File 'index.html' is publishable but not published to S3..."
8. **AI prompts:** "Publish index.html to S3? [1] Public [2] Temp [3] Private [4] Skip"

**For batch operations:**

1. **AI announces:** "Now generating 10 HTML mockups for dashboard screens" (Rule 27)
2. **Batch detector:** Activates batch mode (either declared or auto-detected)
3. **AI creates:** 10 HTML files rapidly
4. **Grace periods:** Skipped (batch mode active)
5. **Batch completes:** After 30s idle time
6. **Hook injects:** Batch completion message
7. **AI prompts:** "Publish all 10 files to S3? [1] Publish all [2] Skip [3] Select individually"

---

[END OF TESTING GUIDE]
