---
description: Quick asset delivery tool for partners and customers
---

Generate AWS-branded download page for selected assets with manifest and private S3 upload.

**Usage:**
```bash
/deliver-assets [--from DIR] [--email] [--temp DURATION]
```

**Examples:**
```bash
# Interactive asset selection from current directory
/deliver-assets

# Select from specific directory with email generation
/deliver-assets --from ./prototype-demo --email

# Create delivery with custom expiration
/deliver-assets --from ./deliverables --temp 24h

# Full featured delivery
/deliver-assets --from ./assets --customer acme-corp --email --temp 7d
```

**Arguments:**
- `--from DIR` - Source directory for asset selection (default: current directory)
- `--email` - Generate delivery email (NEW!)
- `--temp DURATION` - Presigned URL expiration (e.g., 1h, 24h, 7d) (default: 7d)
- `--customer NAME` - Customer/initiative name (prompted if not provided)
- `--yes` - Skip confirmations
- `--bucket NAME` - Custom S3 bucket (default: ASSET_DIST_AWS_BUCKET env)
- `--region REGION` - AWS region (default: ASSET_DIST_AWS_REGION env)
- `--profile NAME` - AWS profile name

**Interactive Workflow:**

1. **Customer name prompt:**
   ```
   Customer/Initiative name? (e.g., "acme-corp", "q4-migration")
   >
   ```

2. **File selection** (checkbox UI):
   ```
   Select assets to deliver:
   [ ] architecture-diagram.png (2.3 MB)
   [ ] technical-spec.pdf (450 KB)
   [ ] demo-video.mp4 (15 MB)
   [ ] source-code.zip (5 MB)
   ```

3. **Optional descriptions** (AI-generated or user input):
   ```
   Add description for architecture-diagram.png?
   [AI suggestion: "System architecture diagram showing microservices"]
   >
   ```

4. **Generate deliverables:**
   - `START.md` - Asset manifest with descriptions
   - `index.html` - AWS-branded download page
   - `delivery-email.txt` - Professional delivery email (if --email)
   - Upload to S3: `delivery/{customer-name}/{YYYY-MM-DD}/`
   - Output presigned URL (valid 7 days)

**Output Structure:**

S3: `delivery/{customer-name}/{date}/`
```
delivery/acme-corp/2025-11-20/
├── index.html                 # AWS-branded landing page
├── START.md                   # Asset manifest
├── architecture-diagram.png
├── technical-spec.pdf
├── demo-video.mp4
└── source-code.zip
```

Local (if --email):
```
delivery-email-acme-corp-2025-11-20.txt   # Ready-to-send email
```

**index.html Features:**
- AWS branding (colors, professional styling)
- Author info: Andy Hopper (andyhop@amazon.com)
- File list with download buttons
- File metadata (size, description)
- Access expiration notice
- Mobile-responsive design

**delivery-email.txt Features** (with --email):
- Amazon-style professional email
- Asset summary (file count, total size)
- Complete file list
- Download instructions with presigned URL
- Important notes and next steps
- Author signature (Andy Hopper, andyhop@amazon.com)
- Expiration date reminder

**START.md Template:**
```markdown
# Asset Delivery Package

**Customer/Initiative:** {customer-name}
**Delivered by:** Andy Hopper, AWS Startup SA
**Contact:** andyhop@amazon.com
**Date:** {YYYY-MM-DD}
**Access expires:** {expiration-date}

## Assets Included

### architecture-diagram.png (2.3 MB)
System architecture diagram showing microservices and data flow.

### technical-spec.pdf (450 KB)
Detailed technical specification and implementation guide.

### demo-video.mp4 (15 MB)
Video walkthrough of the prototype functionality.

---

For questions or follow-up, contact: andyhop@amazon.com
```

**Credentials:**
Uses same AWS credentials as `/s3-publish`:
1. `ASSET_DIST_AWS_ACCESS_KEY_ID` / `ASSET_DIST_AWS_SECRET_ACCESS_KEY`
2. `--profile` AWS profile
3. `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (fallback)

**Setup:**
```bash
# Set default credentials
export ASSET_DIST_AWS_ACCESS_KEY_ID="your-key"
export ASSET_DIST_AWS_SECRET_ACCESS_KEY="your-secret"
export ASSET_DIST_AWS_BUCKET="your-bucket"
export ASSET_DIST_AWS_REGION="us-east-1"
```

Script location: `shared/scripts/deliver_assets.py`

---

Now executing deliver-assets command...

```bash
#!/bin/bash

# Get the repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT_PATH="$REPO_ROOT/shared/scripts/deliver_assets.py"

# Check if Python script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: deliver_assets.py not found at $SCRIPT_PATH"
    exit 1
fi

# Check if required packages are installed
python3 -c "import boto3" 2>/dev/null || {
    echo "📦 Installing boto3..."
    pip3 install boto3>=1.28.0
}

# Execute the Python script with all arguments
python3 "$SCRIPT_PATH" "$@"
```
