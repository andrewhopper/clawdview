<!-- File UUID: 24cc7557-cfe4-4333-a366-5fe45ac2bc12 -->
# Cancel Ralph Loop

Stop an active Ralph loop.

## Usage

```
/cancel-ralph
```

## Execution

When this command is invoked, Claude should:

```bash
RALPH_DIR="${HOPPERLABS_ROOT:-$HOME/hopperlabs}/.claude/ralph"
STATE_FILE="$RALPH_DIR/active.json"

if [ -f "$STATE_FILE" ]; then
    STATE=$(cat "$STATE_FILE")
    ITERATIONS=$(echo "$STATE" | jq -r '.current_iteration // 0')
    START_TIME=$(echo "$STATE" | jq -r '.start_time // empty')
    
    rm -f "$STATE_FILE"
    echo "$(date -Iseconds) | Ralph loop cancelled after $ITERATIONS iterations" >> "$RALPH_DIR/history.log"
    
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  RALPH LOOP CANCELLED"
    echo "  Iterations completed: $ITERATIONS"
    echo "  Started: $START_TIME"
    echo "  Cancelled: $(date -Iseconds)"
    echo "═══════════════════════════════════════════════════════════════"
else
    echo "No active Ralph loop to cancel."
fi
```

## Output

Shows loop statistics when cancelled:
- Number of iterations completed
- Start time
- Cancellation time
