<!-- File UUID: 8f3e9a2c-5d7b-4e1f-9c3a-6b2d8f4e1a7c -->

# S3 Publish Utility

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A simple, robust Python utility for uploading files to Amazon S3 with automatic content-type detection and public URL generation.

## Features

- **Simple CLI Interface** - Upload files with a single command
- **Auto Content-Type Detection** - Automatically detects MIME types from file extensions
- **Public URL Generation** - Returns the public S3 URL after upload
- **Environment-Based Configuration** - Secure credential management via environment variables
- **Error Handling** - Clear error messages for missing files or credentials

## Installation

### Prerequisites

- Python 3.8 or higher
- An AWS S3 bucket with appropriate permissions
- AWS credentials with S3 write access

### Install Dependencies

```bash
pip install boto3
```

Or using a requirements file:

```bash
echo "boto3>=1.26.0" > requirements.txt
pip install -r requirements.txt
```

## Configuration

Set the following environment variables before using the tool:

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `ASSET_DIST_AWS_ACCESS_KEY_ID` | Yes | AWS Access Key ID | - |
| `ASSET_DIST_AWS_ACCESS_KEY_SECRET` | Yes | AWS Secret Access Key | - |
| `ASSET_DIST_AWS_BUCKET` | Yes | S3 bucket name | - |
| `ASSET_DIST_AWS_REGION` | No | AWS region | `us-east-1` |

### Example Configuration

```bash
export ASSET_DIST_AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export ASSET_DIST_AWS_ACCESS_KEY_SECRET="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export ASSET_DIST_AWS_BUCKET="my-public-assets"
export ASSET_DIST_AWS_REGION="us-east-1"
```

For persistent configuration, add these to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.).

## Usage

### Command Line

**Upload with automatic key (uses filename):**
```bash
python3 s3publish.py /path/to/file.pdf
# Output: https://my-bucket.s3.us-east-1.amazonaws.com/file.pdf
```

**Upload with custom S3 key:**
```bash
python3 s3publish.py /path/to/file.pdf documents/report-2025.pdf
# Output: https://my-bucket.s3.us-east-1.amazonaws.com/documents/report-2025.pdf
```

### Python API

```python
from s3publish import publish

# Upload with automatic key
url = publish('/path/to/image.png')
print(f'Uploaded to: {url}')

# Upload with custom key
url = publish('/path/to/data.json', 'api/v1/data.json')
print(f'Uploaded to: {url}')
```

### Supported File Types

The tool automatically detects content types for common formats:
- **Documents:** PDF, DOCX, TXT, MD
- **Images:** PNG, JPG, GIF, SVG, WEBP
- **Web:** HTML, CSS, JS, JSON
- **Archives:** ZIP, TAR, GZ
- **Media:** MP4, MP3, WAV

Unknown types default to `application/octet-stream`.

## Examples

### Upload a Static Website

```bash
# Upload HTML file
python3 s3publish.py index.html

# Upload with directory structure
python3 s3publish.py styles.css assets/styles.css
python3 s3publish.py app.js assets/app.js
```

### Upload Build Artifacts

```bash
# Upload build output
python3 s3publish.py dist/bundle.js releases/v1.2.3/bundle.js
python3 s3publish.py dist/styles.css releases/v1.2.3/styles.css
```

### Batch Upload with Shell Script

```bash
#!/bin/bash
# upload-assets.sh

for file in dist/*; do
  key="releases/$(date +%Y%m%d)/$(basename $file)"
  python3 s3publish.py "$file" "$key"
done
```

## Error Handling

The tool provides clear error messages for common issues:

**Missing environment variables:**
```
Error: Missing required environment variables: ASSET_DIST_AWS_ACCESS_KEY_ID, ASSET_DIST_AWS_BUCKET
```

**File not found:**
```
Error: File not found: /path/to/missing.pdf
```

**AWS permissions error:**
```
Error: An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
```

## Security Notes

1. **Never commit credentials** to version control
2. **Use IAM roles** when running on AWS infrastructure (EC2, Lambda, etc.)
3. **Restrict bucket permissions** to minimum required access
4. **Use environment variables** or AWS credential chain for authentication

### Recommended IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

## Troubleshooting

### Issue: "Bucket doesn't allow ACLs" error

The tool intentionally omits the `ACL` parameter. If you need to set object ACLs, modify line 64-69 to include:
```python
s3.put_object(
    Bucket=bucket,
    Key=s3_key,
    Body=f.read(),
    ContentType=content_type,
    ACL='public-read'  # Add if your bucket allows ACLs
)
```

### Issue: URLs not publicly accessible

Ensure your S3 bucket has a policy allowing public read access:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Changelog

### v1.0.0 (2025-01-15)
- Initial release
- Basic upload functionality
- Auto content-type detection
- Environment-based configuration
