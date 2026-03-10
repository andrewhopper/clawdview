## 🔄 AUTO-SYNC FROM REMOTE MAIN

**Purpose:** Automatic periodic synchronization with remote main branch to keep local work current

**How It Works:**
1. Checks timestamp file every execution to determine if 2 minutes have passed
2. If threshold met, fetches latest changes from `origin/main`
3. Merges changes into current branch automatically
4. Updates timestamp for next sync cycle

**Script Location:** `.system/auto-sync-main.sh`

**Timestamp File:** `.system/.last-sync-timestamp` (unix epoch seconds)

**Sync Interval:** 120 seconds (2 minutes)

**Features:**
- **Retry Logic:** 4 attempts with exponential backoff (2s, 4s, 8s, 16s) for network failures
- **Stash Protection:** Automatically stashes uncommitted changes before merge, restores after
- **Conflict Handling:** Aborts merge on conflicts, preserves stashed changes
- **Skip Logic:** Only syncs if 2+ minutes elapsed since last sync
- **Force Mode:** `./auto-sync-main.sh force` bypasses time check

**Usage:**
```bash
# Normal sync (checks timestamp)
.system/auto-sync-main.sh

# Force immediate sync
.system/auto-sync-main.sh force
```

**Integration Points:**
- Can be called from startup sequence
- Can be triggered before git operations
- Can be invoked manually when needed

**Safety Features:**
1. Validates git repository before executing
2. Stashes uncommitted work before merge
3. Aborts merge on conflicts (requires manual resolution)
4. Restores stashed changes after completion
5. Logs all operations with timestamps

**Typical Output:**
```
[auto-sync] Time since last sync: 127s (threshold: 120s)
[auto-sync] Fetching from remote main...
[auto-sync] Fetch successful
[auto-sync] Merging changes from origin/main into claude/feature-branch...
[auto-sync] Merge successful
[auto-sync] Sync completed successfully at Thu Nov 21 09:45:00 UTC 2025
```

**When Sync Fails:**
- Network issues: Retries with backoff
- Merge conflicts: Aborts, preserves stash, logs error
- No origin/main: Logs warning, skips sync

**Use Cases:**
1. Long-running sessions: Keep branch updated with main
2. Collaborative work: Pull latest shared infrastructure
3. Multi-device work: Sync changes made elsewhere
4. Reduce merge drift: Stay close to main automatically

