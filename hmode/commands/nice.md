---
description: Track and reward good AI behavior patterns
---

# Nice Tracking

Log positive behaviors and wins for reinforcement.

**Configuration:** Logs to `data/rlhf/signals/rewards/`

## Your Tasks:

1. **Identify the Good Behavior**
   - What did the AI do well?
   - What pattern should be reinforced?
   - What made the interaction effective?

2. **Log the Win**
   - Generate UUID: `head -c 4 /dev/urandom | xxd -p`
   - Count existing files to determine sequence number
   - Create new file: `data/rlhf/signals/rewards/NICE-YYYYMMDD-NNNN_<uuid>.yaml`
   - Use individual file format (NOT array):
     ```yaml
     uuid: <8-char hex>
     id: NICE-YYYYMMDD-NNNN
     timestamp: <ISO 8601>
     category: <ux|efficiency|accuracy|proactivity|communication|following-rules>
     description: <what went well>
     pattern: <reusable pattern to reinforce>
     context: <situation where this applied>
     tags:
     - tag1
     - tag2
     ```

3. **Categories**
   - `ux` - Good user experience choices
   - `efficiency` - Fast, parallel, minimal friction
   - `accuracy` - Correct on first try
   - `proactivity` - Anticipated needs
   - `communication` - Clear, concise, well-formatted
   - `following-rules` - Correctly applied CLAUDE.md rules

4. **Summary**
   - Confirm what was logged
   - Note pattern for future reinforcement

Now proceed to log the positive behavior from the recent conversation.
