---
description: Memorize learnings, patterns, or insights from conversation (goes back 10 turns)
---

# Memo - Capture Knowledge

Extract and save learnings, patterns, or insights from the recent conversation.

**Configuration:** Saves to `data/rlhf/memos/`

## Your Tasks:

1. **Review Last 10 Turns**
   - Look back at the last 10 user/assistant exchanges
   - Identify valuable knowledge worth preserving
   - Extract patterns, solutions, decisions, or insights

2. **Categorize the Memo**
   - `learning` - Something new learned
   - `pattern` - Reusable pattern or approach
   - `decision` - Important decision made
   - `insight` - Key realization
   - `solution` - Problem solution worth remembering
   - `preference` - User preference discovered
   - `gotcha` - Pitfall or edge case to remember

3. **Create Memo File**
   - Directory: `data/rlhf/memos/`
   - Filename: `MEMO-YYYYMMDD-NNNN_uuid8.yaml`
   - Schema:
     ```yaml
     uuid: <8-char-uuid>
     id: MEMO-YYYYMMDD-NNNN
     timestamp: <ISO 8601>
     category: <learning|pattern|decision|insight|solution|preference|gotcha>
     title: <short descriptive title>
     content: |
       Detailed memo content.
       Can be multi-line.
     context: <what prompted this memo>
     source_turns: <number of turns reviewed>
     tags: []
     ```

4. **Summary**
   - Confirm what was memorized
   - Note how it might be useful in the future

## Usage

```
/memo
```

Reviews last 10 turns and extracts knowledge worth remembering.

Now proceed to review the last 10 conversation turns and create a memo.
