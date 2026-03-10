---
uuid: cmd-s3-pub-9w0x1y2z
description: Publish assets to S3 with flexible access control (public, temp links, private)
---

Publish files/directories to S3. **Secure by default**: Files are uploaded privately with 7-day presigned URLs unless specified otherwise.

**Usage:**
- `/s3-publish <path> [--public] [--temp DURATION] [--private] [--yes]`

**Security Modes:**

1. **Default (Secure Sharing)**: Private upload with 7-day presigned URL
   ```bash
   /s3-publish ./document.pdf
   # ✅ Generates shareable link that expires in 7 days
   ```

2. **Public Access**: Make files permanently accessible (requires confirmation)
   ```bash
   /s3-publish ./build --public --yes
   # ⚠️ Files accessible to ANYONE on the internet
   ```

3. **Custom Expiry**: Private upload with custom duration presigned URL
   ```bash
   /s3-publish ./report.pdf --temp 12h
   # ✅ Generates link that expires in 12 hours
   ```

4. **Private Only**: No URL generation (S3 URI only, requires AWS credentials)
   ```bash
   /s3-publish ./internal-doc.pdf --private
   # 🔒 Returns S3 URI only, no shareable link
   ```

**Examples:**
```bash
# Default: Secure 7-day presigned URL
/s3-publish ./document.pdf

# Public static website (requires confirmation)
/s3-publish ./build --public --yes

# Temporary access (12 hours)
/s3-publish ./report.pdf --temp 12h

# Private only (no URL generation)
/s3-publish ./confidential.pdf --private

# Custom bucket and region
/s3-publish ./assets --bucket my-custom-bucket --region us-west-2
```

**Arguments:**
- `path` - File or directory to upload (required)
- `--public` - Make files publicly accessible (requires confirmation)
- `--temp DURATION` - Generate presigned URL with custom duration (e.g., 1h, 24h, 7d)
- `--private` - Private upload with no URL (S3 URI only, requires AWS credentials)
- `--bucket NAME` - Custom S3 bucket (default: ASSET_DIST_AWS_BUCKET env)
- `--region REGION` - AWS region (default: ASSET_DIST_AWS_REGION env or us-east-1)
- `--prefix PATH` - S3 key prefix (folder path)
- `--yes` - Skip confirmation prompts
- `--verbose` - Show detailed upload progress
- `--format FORMAT` - Output format: text, json, verbose
- `--dry-run` - List files without uploading

**Security Features:**
- **Secure by default**: 7-day presigned URLs for private sharing
- **Public access requires confirmation**: Prevents accidental public uploads
- **Flexible expiry**: Custom presigned URL durations (1h, 24h, 7d, etc.)
- **Truly private mode**: No URL generation for maximum security

**Credentials:**
Priority order:
1. `ASSET_DIST_AWS_ACCESS_KEY_ID` / `ASSET_DIST_AWS_SECRET_ACCESS_KEY` env vars
2. `--access-key` / `--secret-key` flags
3. `--profile` AWS profile name
4. `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (fallback)

**Setup:**
```bash
# Install dependencies (boto3 will auto-install if missing)
pip3 install boto3>=1.28.0

# Set default credentials (recommended)
export ASSET_DIST_AWS_ACCESS_KEY_ID="your-key"
export ASSET_DIST_AWS_SECRET_ACCESS_KEY="your-secret"
export ASSET_DIST_AWS_BUCKET="your-bucket"
export ASSET_DIST_AWS_REGION="us-east-1"
```

Script location: `prototypes/proto-015-claude-power-tools/scripts/s3_publish.py`

---

Now executing s3-publish command...

```bash
#!/bin/bash

# Get the repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT_PATH="$REPO_ROOT/shared/scripts/s3_publish.py"

# Check if Python script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: s3_publish.py not found at $SCRIPT_PATH"
    exit 1
fi

# Check if boto3 is installed, install if missing
python3 -c "import boto3" 2>/dev/null || {
    echo "📦 Installing boto3..."
    pip3 install boto3>=1.28.0
}

# Execute the Python script with all arguments
python3 "$SCRIPT_PATH" "$@"
```
