# S3 Backup Tool

Incremental backup to S3 with Merkle tree change detection. Designed for Claude Code Web environments where standard sync tools aren't available.

## Features

- **Merkle Tree Change Detection**: Uses content hashing (SHA-256) to detect actual file changes, not just mtime
- **Incremental Backups**: Only uploads files that have truly changed since last backup
- **Time-based Filtering**: Optional `--days N` to limit scan to recently modified files
- **Multi-credential Support**: AWS_*, ASSET_DIST_AWS_*, or default boto3 chain
- **Configurable Exclusions**: Skip .git, node_modules, binaries, etc.
- **S3 Versioning Compatible**: Works with versioned buckets for file history

## Quick Start

```bash
# From repo root (uses project's virtual environment)
source .venv/bin/activate

# Incremental backup (uses manifest for change detection)
python shared/tools/s3backup.py

# Backup files changed in last 7 days
python shared/tools/s3backup.py --days 7

# Preview what would be uploaded
python shared/tools/s3backup.py --dry-run

# Force full backup (ignore previous manifest)
python shared/tools/s3backup.py --full
```

## Configuration

Edit `shared/tools/s3backup-config.yaml`:

```yaml
aws:
  region: us-east-1
  account_id: "507745175693"

backup:
  bucket: protoflow-backups-507745175693
  prefix: backups/protoflow
  max_size_mb: 50

exclude_patterns:
  - .git
  - __pycache__
  - node_modules
  - .venv
  - .env

exclude_extensions:
  - .exe
  - .zip
  - .mp4
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--days N`, `-d N` | Only backup files modified in last N days |
| `--path PATH`, `-p PATH` | Root path to backup (default: current directory) |
| `--bucket NAME`, `-b NAME` | Override S3 bucket name |
| `--prefix PREFIX`, `-P PREFIX` | Override S3 key prefix |
| `--dry-run`, `-n` | Preview only, don't upload |
| `--full`, `-f` | Force full backup (ignore manifest) |
| `--config FILE`, `-c FILE` | Custom config file path |
| `--max-size MB` | Max file size in MB (default: 50) |
| `--show-tree` | Show directory tree with change status |
| `--verbose`, `-v` | Enable debug logging |
| `--log-file FILE` | Write logs to file |

## How It Works

### Merkle Tree Change Detection

1. **Build Tree**: Scans filesystem, computes SHA-256 hash of each file
2. **Compare**: Loads previous manifest and compares hashes
3. **Upload**: Only uploads files with changed hashes
4. **Save Manifest**: Stores `.s3backup-manifest.json` for next run

```
Root Hash = hash(sorted child hashes)
├── dir1/ hash = hash(file1.hash + file2.hash)
│   ├── file1.txt hash = sha256(content)[:16]
│   └── file2.txt hash = sha256(content)[:16]
└── dir2/ hash = hash(file3.hash)
    └── file3.txt hash = sha256(content)[:16]
```

### Credential Priority

1. `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` + optional `AWS_SESSION_TOKEN`
2. `ASSET_DIST_AWS_ACCESS_KEY_ID` + `ASSET_DIST_AWS_ACCESS_KEY_SECRET` (Claude Code Web)
3. Default boto3 credential chain (profiles, IAM roles, etc.)

## Dependencies

Uses dependencies from the project's root `pyproject.toml`:
- `boto3>=1.28.0` - AWS SDK
- `pyyaml>=6.0` - YAML config parsing

No separate installation needed when using the project's virtual environment.

## Examples

```bash
# Backup entire repo, time-filtered
python shared/tools/s3backup.py --days 1 --log-file /tmp/backup.log

# Backup specific project
python shared/tools/s3backup.py --path projects/my-project --prefix backups/my-project

# Use custom bucket and prefix
python shared/tools/s3backup.py --bucket my-bucket --prefix 2024/december

# Full backup with verbose logging
python shared/tools/s3backup.py --full --verbose
```

## S3 Bucket Setup

The backup bucket should have versioning enabled for file history:

```bash
aws s3api put-bucket-versioning \
  --bucket protoflow-backups-507745175693 \
  --versioning-configuration Status=Enabled \
  --profile admin-507745175693
```

## Files

- `s3backup.py` - Main backup script
- `s3backup-config.yaml` - Configuration file
- `.s3backup-manifest.json` - Auto-generated manifest (git-ignored)
