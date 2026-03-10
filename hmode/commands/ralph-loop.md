<!-- File UUID: aeeb97cc-5074-40e2-a845-54ad8ef82971 -->
# Ralph Loop - Iterative Self-Referential Development

Start an iterative loop that repeatedly feeds the same prompt until completion.

## Usage

```
/ralph-loop "<prompt>" --max-iterations <n> --completion-promise "<text>"
```

## Parameters

- `<prompt>` - The task to iterate on (required)
- `--max-iterations <n>` - Stop after N iterations (default: 10, safety limit)
- `--completion-promise <text>` - Text that signals task completion

## How It Works

1. You start the loop with a prompt
2. Claude works on the task
3. When Claude tries to exit, the Stop hook blocks it
4. The hook re-feeds the SAME prompt
5. Claude sees its previous work in files/git history
6. Loop continues until completion promise or max iterations

## Examples

### Basic Loop
```
/ralph-loop "Fix all TypeScript errors in src/. Run npm run typecheck after each fix. Output <promise>ALL_CLEAR</promise> when no errors remain." --completion-promise "ALL_CLEAR" --max-iterations 20
```

### Test-Driven Development
```
/ralph-loop "Implement the UserService class following TDD:
1. Run npm test to see failing tests
2. Implement just enough to pass one test
3. Run tests again
4. Repeat until all tests pass
5. Output <promise>TESTS_PASSING</promise> when done" --completion-promise "TESTS_PASSING" --max-iterations 30
```

### Refactoring Loop
```
/ralph-loop "Refactor large-file.ts into smaller modules:
1. Identify one cohesive piece to extract
2. Create new module file
3. Move code and update imports
4. Run tests to verify
5. Repeat until file is under 200 lines
6. Output <promise>REFACTORED</promise> when done" --completion-promise "REFACTORED"
```

## Execution

When this command is invoked, Claude should:

1. Parse the prompt and options from $ARGUMENTS
2. Create the loop state file:

```bash
RALPH_DIR="${HOPPERLABS_ROOT:-$HOME/hopperlabs}/.claude/ralph"
mkdir -p "$RALPH_DIR"

# Extract arguments (prompt is everything before --, options after)
PROMPT="$ARGUMENTS"
MAX_ITERATIONS=10
COMPLETION_PROMISE=""

# Parse --max-iterations and --completion-promise from ARGUMENTS
# ... (Claude should extract these from the command arguments)

# Create state file
cat > "$RALPH_DIR/active.json" << EOFSTATE
{
  "prompt": "$(echo "$PROMPT" | sed 's/"/\\"/g')",
  "max_iterations": $MAX_ITERATIONS,
  "completion_promise": "$COMPLETION_PROMISE",
  "current_iteration": 0,
  "start_time": "$(date -Iseconds)"
}
EOFSTATE

echo "$(date -Iseconds) | Ralph loop started: max=$MAX_ITERATIONS, promise=$COMPLETION_PROMISE" >> "$RALPH_DIR/history.log"
```

3. Immediately begin working on the prompt

## Cancel

Use `/cancel-ralph` to stop an active loop.

## Best Practices

1. **Always set max-iterations** - Prevents runaway loops
2. **Clear completion criteria** - Define exactly what "done" means
3. **Incremental goals** - Break complex tasks into phases
4. **Self-verification** - Include test/lint commands in the prompt
5. **Escape hatches** - Document what to do if stuck

## Good For

- Getting tests to pass
- Fixing type errors
- Iterative refactoring
- Greenfield projects
- Tasks with automatic verification

## Not Good For

- Tasks requiring human judgment
- Design decisions
- Production debugging
- Unclear success criteria
