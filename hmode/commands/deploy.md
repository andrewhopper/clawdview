---
description: Upload/publish/deploy files to S3 with presigned URLs (default private)
tags: [project, publish, upload, deploy, s3]
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
   - Check for `./docs` directory (common for documentation)
   - Check current directory
   - Ask user if ambiguous

2. **Determine bucket:**
   - Check AWS_BUCKET environment variable
   - Check s3_config.json
   - Ask user if not found

3. **Run upload:**
   ```bash
   cd shared/semantic-model
   python3 s3_uploader.py <source_dir> -b <bucket_name> --private
   ```

4. **For public access:**
   ```bash
   python3 s3_uploader.py <source_dir> -b <bucket_name> --public
   ```

5. **With custom prefix:**
   ```bash
   python3 s3_uploader.py <source_dir> -b <bucket_name> -p path/prefix
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

Check before running:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (default: us-east-1)
- `AWS_BUCKET` (or ask user)

## Output

Display:
- Upload progress with file count
- Success/failure statistics
- Presigned URLs for key files (index.html, README.md, etc.)
- Instructions for accessing other files

## Error Handling

1. **Missing credentials:** Provide clear setup instructions
2. **Missing source directory:** Ask user to specify path
3. **Bucket access denied:** Check permissions and suggest fixes
4. **Upload failures:** Show which files failed and why

## Examples

**Example 1: Simple publish**
```
User: "publish the docs"
Assistant:
  - Detected: ./docs directory
  - Bucket: asset-distribution-bucket-1762910336 (from env)
  - Mode: Private with presigned URLs
  - [Runs upload]
  - [Shows presigned URLs]
```

**Example 2: Public website**
```
User: "deploy website to s3"
Assistant:
  - Detected: ./website directory
  - Presents options
  - User selects: [2] Public with website hosting
  - [Runs upload with --public]
  - [Shows public URL]
```

## Follow-up Actions

After successful upload, ask:
- "Would you like to save these URLs?"
- "Generate a sharing email with these links?"
- "Upload to a different bucket?"

## Notes

- Always use the enhanced `s3_uploader.py` script
- Never expose credentials in logs
- Validate source directory exists before upload
- Handle large directories with progress indication
- Support cancellation with Ctrl+C
