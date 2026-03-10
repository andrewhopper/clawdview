---
version: 1.0.0
last_updated: 2025-11-23
description: Pull latest changes from remote main branch
---

# Pull

Pull the latest changes from remote origin/main.

## Instructions

1. **Fetch and pull from remote**:
   ```bash
   git pull origin main
   ```

2. **Report result**:
   ```
   ✅ Pulled from origin/main

   📥 [summary of changes or "Already up to date"]
   ```

3. **If conflicts occur**, report them and stop:
   ```
   ⚠️ Merge conflict detected in:
   - file1.txt
   - file2.txt

   Resolve conflicts manually before continuing.
   ```

## Usage

```bash
/pull
```
