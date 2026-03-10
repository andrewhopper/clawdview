---
description: Upload/publish/deploy files to S3 with presigned URLs (default private)
tags: [project, publish, upload, deploy, s3]
uuid: 178eb2bb-0ea3-4a04-b620-5ba3bfb59cf5
---

# Publish to S3

Upload files to S3 with smart defaults for private access and presigned URLs.

## Intent Detection

Trigger this command when user says:
- "upload [files/directory] to s3"
- "publish [files/directory]"
- "deploy [files/directory]"
- "share [files/directory]"

## Configuration

**Default Behavior:**
- Private bucket (blocked public access)
- Presigned URLs (7-day expiry)
- Versioning enabled
- Enhanced logging and error handling

## Usage

1. **Detect source directory:**
   - If user specifies path, use it
   - Check for `./dist` directory (build output)
   - Check for `./docs` directory (common for documentation)
   - Check current directory
   - Ask user if ambiguous

2. **Determine bucket:**
   - Check ASSET_DIST_AWS_BUCKET environment variable
   - **FATAL ERROR if not set** - DO NOT proceed
   - Ask user to configure bucket

3. **Resolve credentials (REQUIRED):**
   ```bash
   # Use AWS credential helper
   eval $(cd $PROTOFLOW_ROOT && python3 shared/storage/aws_credentials.py 2>/dev/null | grep export)
   export ASSET_DIST_AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
   export ASSET_DIST_AWS_ACCESS_KEY_SECRET=$AWS_SECRET_ACCESS_KEY
   export ASSET_DIST_AWS_REGION=$AWS_REGION
   ```

4. **Run upload using s3publish.py:**
   ```bash
   # Single file upload
   python3 $PROTOFLOW_ROOT/hmode/shared/tools/s3publish.py <file_path> [s3_key]

   # Example with custom key
   python3 $PROTOFLOW_ROOT/hmode/shared/tools/s3publish.py dist/index.html marketing/index.html
   ```

5. **For directory uploads:**
   ```bash
   # Upload all files in dist/
   for file in dist/*; do
     python3 $PROTOFLOW_ROOT/hmode/shared/tools/s3publish.py "$file" "$(basename $file)"
   done
   ```

## Interactive Options

After detecting intent, present options:

```
Publishing options:
[1] Private with presigned URLs (default, 7-day links)
[2] Public with website hosting
[3] Custom configuration

Source: <detected_directory>
Bucket: <detected_bucket>
```

## Required Environment Variables

**CRITICAL: Always use AWS credential helper**

Before uploading, MUST resolve credentials using the credential helper:

```bash
# 1. Resolve credentials using credential helper
eval $(cd $PROTOFLOW_ROOT && python3 shared/storage/aws_credentials.py 2>/dev/null | grep export)

# 2. Map to ASSET_DIST_AWS_* variables for s3publish.py
export ASSET_DIST_AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export ASSET_DIST_AWS_ACCESS_KEY_SECRET=$AWS_SECRET_ACCESS_KEY
export ASSET_DIST_AWS_REGION=$AWS_REGION
```

**FATAL ERROR if bucket not set:**
- `ASSET_DIST_AWS_BUCKET` MUST be set or script will fail
- Script will exit with error: "Missing required environment variables: ASSET_DIST_AWS_BUCKET"
- DO NOT proceed without bucket configuration

**Credential Priority (handled by helper):**
1. isengardcli (work laptop)
2. aws CLI / aws sso login (personal laptop)
3. Environment variables (Claude Code web)

Check before running:
- `ASSET_DIST_AWS_BUCKET` (REQUIRED - fatal error if missing)
- `ASSET_DIST_AWS_REGION` (default: us-east-1)

## Output

Display:
- Upload progress with file count
- Success/failure statistics
- Presigned URLs for key files (index.html, README.md, etc.)
- Instructions for accessing other files

## Error Handling

1. **Missing bucket (FATAL):** Exit immediately with error message
   ```
   ❌ FATAL ERROR: S3 bucket not configured
   Error: Missing required environment variables: ASSET_DIST_AWS_BUCKET

   Required Action: Set ASSET_DIST_AWS_BUCKET environment variable
   ```

2. **Credential resolution failures:**
   - Check if isengardcli available (work laptop)
   - Check if aws CLI available (personal laptop)
   - Provide instructions for `aws sso login`
   - Show credential helper verbose output for debugging

3. **Missing source directory:** Ask user to specify path

4. **Bucket access denied:** Check permissions and suggest fixes

5. **Upload failures:** Show which files failed and why

## Examples

**Example 1: Successful publish with credential helper**
```
User: "publish the marketing site"
Assistant:
  - Detected: ./marketplace-site/dist/ directory
  - Resolving credentials via AWS credential helper...
  - ✅ isengardcli: ASIARSU7KN... (work laptop detected)
  - Checking ASSET_DIST_AWS_BUCKET...
  - Bucket: protoflow-marketing-site (from env)
  - Uploading files...
  - [Shows URLs]
```

**Example 2: Fatal error - bucket not configured**
```
User: "deploy this to s3"
Assistant:
  - Detected: ./dist/ directory
  - Resolving credentials via AWS credential helper...
  - ✅ Credentials resolved
  - Checking ASSET_DIST_AWS_BUCKET...
  - ❌ FATAL ERROR: S3 bucket not configured

  Required Action: Set ASSET_DIST_AWS_BUCKET environment variable

  Options:
  [1] Set bucket environment variable
  [2] Create new S3 bucket
  [3] Use existing bucket (provide name)
```

**Example 3: Credential helper verbose mode**
```
User: "publish with debug output"
Assistant:
  - Running credential helper in verbose mode...
  - 🔍 isengardcli found (account: user@amazon.com)...
  - ✅ isengardcli: ASIARSU7KN...
  - export AWS_ACCESS_KEY_ID="..."
  - export AWS_REGION="us-east-1"
  - # method: isengardcli
```

## Follow-up Actions

After successful upload, ask:
- "Would you like to save these URLs?"
- "Generate a sharing email with these links?"
- "Upload to a different bucket?"

## Notes

- **ALWAYS** use AWS credential helper before uploading
- **ALWAYS** use `$PROTOFLOW_ROOT/hmode/shared/tools/s3publish.py` for uploads
- **FATAL ERROR** if ASSET_DIST_AWS_BUCKET not set - do not proceed
- Never expose credentials in logs (credential helper handles this)
- Validate source directory exists before upload
- Handle large directories with progress indication
- Support cancellation with Ctrl+C
- Script automatically detects content-type from file extension
- URLs returned use format: `https://{bucket}.s3.{region}.amazonaws.com/{key}`
