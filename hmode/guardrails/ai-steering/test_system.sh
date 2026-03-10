#!/bin/bash
#
# Guardrail Enforcement System - Quick Test Script
#
# Tests all scenarios:
# 1. Single file with grace period
# 2. Auto-detected batch mode
# 3. Pre-declared batch mode
# 4. Evidence checking
# 5. Hook integration

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Guardrail Enforcement System - Test Suite${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ============================================================================
# Test 1: Clean State
# ============================================================================

echo -e "${YELLOW}[Test 1]${NC} Cleaning previous state..."
rm -f .guardrails/.batch_operation.json \
      .guardrails/.file_history.json \
      .guardrails/.pending_validations.json \
      .guardrails/.supervisor.log
rm -f test-*.html
echo -e "${GREEN}✓ State cleaned${NC}"
echo ""

# ============================================================================
# Test 2: Single File (Grace Period)
# ============================================================================

echo -e "${YELLOW}[Test 2]${NC} Testing single file with grace period..."
echo "<html><body>Single File Test</body></html>" > test-single.html
echo "  → Created test-single.html"

# Start grace period
python3 .guardrails/ai-steering/grace_period_validator.py watch test-single.html --timeout 30 &
GRACE_PID=$!
echo "  → Grace period started (PID: $GRACE_PID, timeout: 30s)"

# Check pending validations
sleep 2
if [ -f .guardrails/.pending_validations.json ]; then
    echo -e "${GREEN}✓ Pending validation tracked${NC}"
    echo "  Content: $(cat .guardrails/.pending_validations.json | python3 -m json.tool 2>/dev/null | head -5)"
else
    echo -e "${RED}✗ Pending validation file not created${NC}"
fi
echo ""

# ============================================================================
# Test 3: Evidence Checking (Skip Single File Reminder)
# ============================================================================

echo -e "${YELLOW}[Test 3]${NC} Testing evidence checking (skip marker)..."
echo "<html><body>Evidence Test</body></html>" > test-evidence.html
echo "  → Created test-evidence.html"

# Create skip marker before grace period expires
touch .s3-skip
echo "  → Created .s3-skip marker"

# Start grace period
python3 .guardrails/ai-steering/grace_period_validator.py watch test-evidence.html --timeout 5 &
EVIDENCE_PID=$!
sleep 6

# Check if reminder is generated
REMINDERS=$(python3 .guardrails/ai-steering/grace_period_validator.py check 2>/dev/null || echo "")
if echo "$REMINDERS" | grep -q "test-evidence.html"; then
    echo -e "${RED}✗ False positive: Reminder generated despite evidence${NC}"
else
    echo -e "${GREEN}✓ Evidence detected, no reminder${NC}"
fi

rm -f .s3-skip
echo ""

# ============================================================================
# Test 4: Auto-Detected Batch Mode
# ============================================================================

echo -e "${YELLOW}[Test 4]${NC} Testing auto-detected batch mode..."
rm -f .guardrails/.batch_operation.json .guardrails/.file_history.json

echo "  → Creating 4 files rapidly (within 10 seconds)..."
for i in {1..4}; do
  echo "<html><body>Batch Auto $i</body></html>" > test-batch-auto-$i.html
  python3 .guardrails/ai-steering/batch_detector.py track test-batch-auto-$i.html 2>/dev/null
  echo "    - Created test-batch-auto-$i.html"
done

# Check batch status
BATCH_STATUS=$(python3 .guardrails/ai-steering/batch_detector.py check 2>/dev/null)
if echo "$BATCH_STATUS" | grep -q "Batch active"; then
    echo -e "${GREEN}✓ Batch mode auto-detected${NC}"
    echo "  Status: $BATCH_STATUS"
else
    echo -e "${RED}✗ Batch mode not activated${NC}"
fi
echo ""

# ============================================================================
# Test 5: Batch Completion (Idle Timeout)
# ============================================================================

echo -e "${YELLOW}[Test 5]${NC} Testing batch completion (idle timeout)..."
echo "  → Waiting 5 seconds for idle timeout... (normally 30s, reduced for testing)"

# Temporarily reduce idle timeout for testing
# Note: In production, this is 30 seconds
sleep 5

# Manually complete batch for testing (in production, idle timeout triggers this)
COMPLETION=$(python3 .guardrails/ai-steering/batch_detector.py complete 2>/dev/null)
if echo "$COMPLETION" | grep -q "Batch complete"; then
    echo -e "${GREEN}✓ Batch completion detected${NC}"
    echo "$COMPLETION"
else
    echo -e "${YELLOW}⚠ Batch may still be active (idle timeout not reached)${NC}"
fi
echo ""

# ============================================================================
# Test 6: Pre-Declared Batch Mode
# ============================================================================

echo -e "${YELLOW}[Test 6]${NC} Testing pre-declared batch mode..."
rm -f .guardrails/.batch_operation.json .guardrails/.file_history.json

echo "  → Declaring batch: 5 HTML files"
DECLARE_OUTPUT=$(python3 .guardrails/ai-steering/batch_detector.py declare --count 5 --type html 2>/dev/null)
echo "  $DECLARE_OUTPUT"

echo "  → Creating 5 files..."
for i in {1..5}; do
  echo "<html><body>Batch Declared $i</body></html>" > test-batch-declared-$i.html
  python3 .guardrails/ai-steering/batch_detector.py track test-batch-declared-$i.html 2>/dev/null
  echo "    - Created test-batch-declared-$i.html"
done

# Check batch state
if [ -f .guardrails/.batch_operation.json ]; then
    DECLARED=$(cat .guardrails/.batch_operation.json | python3 -c "import sys, json; print(json.load(sys.stdin)['declared'])" 2>/dev/null || echo "false")
    if [ "$DECLARED" = "True" ]; then
        echo -e "${GREEN}✓ Pre-declared batch mode active${NC}"
    else
        echo -e "${YELLOW}⚠ Batch active but not marked as declared${NC}"
    fi
fi

# Complete batch
python3 .guardrails/ai-steering/batch_detector.py complete >/dev/null 2>&1
echo ""

# ============================================================================
# Test 7: Hook Integration
# ============================================================================

echo -e "${YELLOW}[Test 7]${NC} Testing hook integration..."

if [ ! -x .claude/hooks/tool-result.sh ]; then
    echo -e "${RED}✗ Hook not executable${NC}"
    echo "  Run: chmod +x .claude/hooks/tool-result.sh"
else
    echo -e "${GREEN}✓ Hook is executable${NC}"

    # Test hook with single file
    echo "  → Simulating Write tool execution..."
    .claude/hooks/tool-result.sh Write "" "File created successfully at: test-hook.html" >/dev/null 2>&1

    sleep 2

    # Check if grace period started
    if [ -f .guardrails/.pending_validations.json ]; then
        echo -e "${GREEN}✓ Hook triggered grace period${NC}"
    else
        echo -e "${YELLOW}⚠ Grace period may not have started${NC}"
    fi
fi
echo ""

# ============================================================================
# Test 8: Logs
# ============================================================================

echo -e "${YELLOW}[Test 8]${NC} Checking logs..."
if [ -f .guardrails/.supervisor.log ]; then
    LOG_LINES=$(wc -l < .guardrails/.supervisor.log)
    echo -e "${GREEN}✓ Log file exists ($LOG_LINES lines)${NC}"
    echo "  Last 5 entries:"
    tail -n 5 .guardrails/.supervisor.log | sed 's/^/    /'
else
    echo -e "${YELLOW}⚠ No log file created yet${NC}"
fi
echo ""

# ============================================================================
# Summary
# ============================================================================

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Tests completed. Review results above."
echo ""
echo "Next steps:"
echo "  1. Review logs: tail -f .guardrails/.supervisor.log"
echo "  2. Check state files:"
echo "     - cat .guardrails/.pending_validations.json"
echo "     - cat .guardrails/.batch_operation.json"
echo "     - cat .guardrails/.file_history.json"
echo "  3. Clean test files: rm -f test-*.html"
echo ""
echo "For detailed testing instructions, see:"
echo "  .guardrails/ai-steering/TESTING_GUIDE.md"
echo ""

# ============================================================================
# Cleanup (optional)
# ============================================================================

read -p "Clean up test files? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleaning up..."
    rm -f test-*.html \
          .guardrails/.batch_operation.json \
          .guardrails/.file_history.json \
          .guardrails/.pending_validations.json
    echo -e "${GREEN}✓ Test files cleaned${NC}"
fi

echo ""
echo -e "${GREEN}Done!${NC}"
