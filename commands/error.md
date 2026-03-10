---
description: Quick alias for error tracking (invokes /track-errors)
---

# Error Tracking (Alias)

This is a convenience alias for `/track-errors`. Use `/error` when you want to quickly log an error or issue.

**Configuration:** File paths are defined in `shared/config.yaml` under `error_tracking`.

## Usage

**Track current conversation error:**
```
/error
```

**Update existing error status:**
```
/error <UUID|ID> status=fixed
```

**Add note to existing error:**
```
/error <UUID|ID> note="Fixed by implementing validation"
```

## Full Documentation

For complete error tracking documentation, see `hmode/commands/track-errors.md`.

---

**Auto-invoke:** Now loading `/track-errors` command...
