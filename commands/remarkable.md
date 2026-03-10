# reMarkable Cloud Operations

Interact with reMarkable Cloud to push, pull, list, and sync files.

## Usage

```
/remarkable <action> [args]
```

## Actions

### List files
```
/remarkable ls [path]
/remarkable list [path]
```
List files and folders at the specified path (default: root).

### Push (upload) file
```
/remarkable push <local-file> [--dest <remote-folder>]
/remarkable upload <local-file> [--dest <remote-folder>]
```
Upload a PDF or EPUB to reMarkable Cloud.

### Pull (download) file
```
/remarkable pull <remote-file> [--dest <local-folder>]
/remarkable download <remote-file> [--dest <local-folder>]
```
Download a file from reMarkable Cloud.

### Sync directory
```
/remarkable sync <local-dir> [--remote <remote-folder>]
```
Bidirectional sync between local directory and reMarkable Cloud.

### Show tree
```
/remarkable tree [path]
```
Display folder structure as a tree.

---

## Instructions for Claude

When the user invokes this command, use the `rm-cloud` CLI tool to perform the requested operation.

**Prerequisites:**
1. Check if `rm-cloud` is available: `which rm-cloud || pip show remarkable-cli`
2. If not installed, install it: `pip install -e /home/user/protoflow/projects/personal/remarkable-cli-py`
3. Check authentication: `rm-cloud ls /` - if it fails with auth error, guide user to authenticate

**Executing commands:**

For `ls` or `list`:
```bash
rm-cloud ls "$path" --long
```

For `push` or `upload`:
```bash
rm-cloud push "$local_file" --dest "$remote_folder"
```

For `pull` or `download`:
```bash
rm-cloud pull "$remote_file" --dest "$local_folder"
```

For `sync`:
```bash
rm-cloud sync "$local_dir" --remote "$remote_folder" --dry-run
# Show the user what will happen, then if they confirm:
rm-cloud sync "$local_dir" --remote "$remote_folder"
```

For `tree`:
```bash
rm-cloud tree "$path"
```

**Authentication flow:**
If the user needs to authenticate:
1. Tell them to visit: https://my.remarkable.com/device/desktop/connect
2. Run: `rm-cloud auth <code>` with the code they provide

**Error handling:**
- If rmcl is not installed: `pip install rmcl`
- If auth fails: Guide user through re-authentication
- If file not found: Show available files with `rm-cloud ls`

**Output formatting:**
- Present results in a clean, readable format
- For list operations, show folders first, then files
- For sync, always show dry-run first before applying
