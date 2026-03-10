---
description: Alias for /error - track negative AI behavior (RLHF punishment signal)
---

# Punish (Alias for /error)

This is a convenience alias for `/error`. Use `/punish` to log negative AI behaviors.

**Configuration:** Logs to `data/rlhf/signals/punishments/`

## Usage

```
/punish
```

Logs a negative behavior pattern to `data/rlhf/signals/punishments/ERR-YYYYMMDD-NNNN_uuid.yaml`

## Full Documentation

See `hmode/commands/track-errors.md` for complete documentation.

---

**Auto-invoke:** Now loading `/track-errors` command...
