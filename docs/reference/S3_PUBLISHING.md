# S3 Publishing Protocol

**Script:** `/projects/unspecified/active/tool-s3-publish-cli-vayfd/s3_publish.py`

**Status:** ✅ Fixed and Environment-Aware

## Environment Support

The tool supports three environments: `work`, `personal`, and `claude-code`. Each environment uses its own credentials and bucket.

## Environment Variables

**Environment-Specific (Recommended):**
```bash
# Work environment
WORK_AWS_ACCESS_KEY_ID
WORK_AWS_SECRET_ACCESS_KEY
WORK_AWS_BUCKET
WORK_AWS_REGION

# Personal environment
PERSONAL_AWS_ACCESS_KEY_ID
PERSONAL_AWS_SECRET_ACCESS_KEY
PERSONAL_AWS_BUCKET
PERSONAL_AWS_REGION

# Claude Code environment
CLAUDE_CODE_AWS_ACCESS_KEY_ID
CLAUDE_CODE_AWS_SECRET_ACCESS_KEY
CLAUDE_CODE_AWS_BUCKET
CLAUDE_CODE_AWS_REGION
```

**Legacy (Fallback):**
- `ASSET_DIST_AWS_ACCESS_KEY_ID` - AWS access key
- `ASSET_DIST_AWS_SECRET_ACCESS_KEY` - AWS secret key
- `ASSET_DIST_AWS_BUCKET` - S3 bucket name
- `ASSET_DIST_AWS_REGION` - AWS region (default: us-east-1)

## Usage

```bash
# Environment-aware publishing
python3 projects/unspecified/active/tool-s3-publish-cli-vayfd/s3_publish.py \
  path/to/file.md \
  --env work \
  --prefix folder \
  --verbose \
  --yes

# Legacy (no environment specified)
python3 projects/unspecified/active/tool-s3-publish-cli-vayfd/s3_publish.py \
  path/to/file.md \
  --prefix folder \
  --verbose \
  --yes
```

## Priority

1. Environment-specific env vars (when `--env` flag is used)
2. Legacy `ASSET_DIST_*` env vars
3. Command flags: `--access-key`, `--secret-key`, `--bucket`, `--region`
4. AWS profile: `--profile`

## Features

1. Environment-aware credential and bucket management
2. Replaced `upload_file()` with `put_object()` for reliability
3. Supports public, private, and temporary presigned URLs
4. Verbose mode shows environment, bucket, and region info
