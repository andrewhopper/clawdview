# Architecture Diagram SOP

## Overview
Standard Operating Procedure for creating AWS architecture diagrams using Draw.io.

## File Format
- **Tool:** Draw.io (https://app.diagrams.net)
- **Format:** `.drawio` XML format
- **Location:** `{prototype}/docs/{diagram-name}.drawio`

## Diagram Standards

### 1.0 Required Metadata
Every architecture diagram MUST include:
- **Project ID:** Based on folder name (e.g., `proto-s3-publish-vayfd-023`)
- **Author:** Andy Hopper
- **Date:** Current date in `YYYY-MM-DD` format

**Placement:**
- Below main title
- Format: `Project: {id} | Author: {name} | Date: {date}`
- Font: 10pt, color `#545B64` (AWS gray)

**Example:**
```xml
<mxCell id="metadata" value="Project: proto-s3-publish-vayfd-023 | Author: Andy Hopper | Date: 2025-11-19"
  style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontColor=#545B64;"
  vertex="1" parent="1">
  <mxGeometry x="300" y="60" width="600" height="20" as="geometry" />
</mxCell>
```

### 2.0 AWS Visual Standards

#### 2.1 Official AWS Icons
**ALWAYS use official AWS service icons:**
- CloudFront: `mxgraph.aws4.cloudfront`
- Lambda: `mxgraph.aws4.lambda`
- S3: `mxgraph.aws4.s3`
- IAM: `mxgraph.aws4.iam`
- SSM: `mxgraph.aws4.systems_manager`
- CloudTrail: `mxgraph.aws4.cloudtrail`
- CloudWatch: `mxgraph.aws4.cloudwatch_2`
- Route53: `mxgraph.aws4.route_53`
- ACM: `mxgraph.aws4.certificate_manager_3`
- User: `mxgraph.aws4.user`

**Icon Properties:**
- Size: 70x70 pixels (standard)
- Size: 60x60 pixels (optional components)
- Include gradient and official colors
- `strokeColor=#ffffff` for border

#### 2.2 AWS Color Scheme
**Service Categories:**
- **Compute** (Lambda): `#D05C17` (orange)
- **Storage** (S3): `#277116` (green)
- **Security** (IAM, SSM): `#C7131F` (red)
- **Networking** (CloudFront, Route53): `#5A30B5` (purple)
- **Management** (CloudTrail, CloudWatch): `#C7131F` (red)

**Infrastructure:**
- **AWS Cloud Border:** `#FF9900` (AWS orange), 3px, dashed
- **Region Border:** `#545B64` (gray), 2px, dashed
- **Region Background:** `#F7F8F9` (light gray)

### 3.0 Layout Structure

#### 3.1 Canvas Size
- **Standard:** 1200x900 pixels
- **Large/Complex:** 1400x1000 pixels
- **Grid:** 10px grid enabled
- **Guides:** Enabled for alignment

#### 3.2 Component Organization
**Horizontal Layout (Left to Right):**
1. **User/Client** (far left)
2. **CloudFront** (entry point)
3. **Lambda@Edge** (processing)
4. **S3/Backend** (storage/data)
5. **Info Boxes** (far right)

**Vertical Layout (Top to Bottom):**
1. **Title & Metadata** (top)
2. **Configuration** (SSM, secrets)
3. **Main Services** (request flow)
4. **Logging/Monitoring** (bottom)
5. **Optional Components** (bottom)

#### 3.3 Spacing
- **Component spacing:** 180-220px horizontal
- **Vertical spacing:** 140-190px between rows
- **Margins:** 40-80px from canvas edge
- **Info boxes:** 20px padding

### 4.0 Flow Lines & Arrows

#### 4.1 Line Types
**Solid Lines (Request/Data Flow):**
- Main request flow: 3px width
- Secondary flows: 2px width
- Color matches flow type

**Dashed Lines (Configuration/Logging):**
- Configuration: 2px width, dashed
- Logging: 2px width, dashed
- Use for non-request flows

#### 4.2 Color Coding
**Flow Colors:**
- **Orange** (`#FF9900`): HTTPS traffic, main entry
- **Green** (`#277116`): Valid authentication, success path
- **Red** (`#C7131F`): Invalid authentication, failure path
- **Purple** (`#5A30B5`): DNS, networking
- **Gray** (`#545B64`): Metadata, configuration

#### 4.3 Labels
**Flow Labels:**
- **Numbered:** Use sequential numbering (1, 2, 3...)
- **Descriptive:** Brief description (max 3-4 words)
- **Background:** White `#FFFFFF` for readability
- **Font:** 9-10pt for flow labels
- **Bold:** Use for primary flows

**Example Flow Labels:**
- `1. HTTPS + JWT`
- `2. Auth Check`
- `3. Read Secret`
- `4a. Valid ✓`
- `4b. Invalid ✗`

### 5.0 Information Boxes

#### 5.1 Box Types
Create 4 standard info boxes:
1. **JWT Flow** (blue): Authentication sequence
2. **Security** (red): Security features
3. **Performance** (yellow): Performance metrics
4. **Key Details** (purple): Architecture notes

#### 5.2 Box Styling
```
Border: 2px solid
Padding: 8px left, 3px top
Font: 10pt title (bold), 9pt content
Alignment: Left-aligned text
Size: 240x115-145px
```

#### 5.3 Color Palette
- **Blue Box:** `#E1F5FE` background, `#01579B` border
- **Red Box:** `#FFEBEE` background, `#C7131F` border
- **Yellow Box:** `#FFF9C4` background, `#F57F17` border
- **Purple Box:** `#F3E5F5` background, `#4A148C` border

### 6.0 Detail Boxes

#### 6.1 Component Details
Add small detail boxes next to major components:
- **Size:** 120x70px
- **Border:** 1.5px solid (matching component color)
- **Font:** 9pt
- **Content:** 3-5 bullet points

**Example (Lambda@Edge):**
```
• Verify JWT
• Check expiration
• Login/logout
• Generate tokens
```

### 7.0 Labels & Typography

#### 7.1 Component Labels
- **Font:** 11pt, bold
- **Color:** `#232F3E` (AWS dark gray)
- **Position:** Below icon
- **Max Width:** 110px
- **Multi-line:** OK for long names

#### 7.2 Title
- **Font:** 22pt, bold
- **Color:** `#232F3E`
- **Position:** Top center
- **Width:** 600px

#### 7.3 Metadata
- **Font:** 10pt, regular
- **Color:** `#545B64`
- **Position:** Below title
- **Format:** `Project: X | Author: Y | Date: Z`

### 8.0 AWS Region Boundaries

#### 8.1 Region Box
```xml
<mxCell id="region" value=""
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F7F8F9;strokeColor=#545B64;strokeWidth=2;dashed=1;">
  <mxGeometry x="80" y="130" width="1040" height="690" />
</mxCell>
```

#### 8.2 Region Label
- **Text:** `Region: us-east-1 (Required for Lambda@Edge)`
- **Font:** 12pt, bold
- **Color:** `#545B64`
- **Position:** Top-left inside region

### 9.0 Workflow for Creating Diagrams

#### 9.1 Step-by-Step Process
1. **Extract Metadata:**
   ```bash
   PROJECT_ID=$(basename $(pwd))
   AUTHOR="Andy Hopper"
   DATE=$(date +"%Y-%m-%d")
   ```

2. **Create Base Structure:**
   - Title + metadata
   - AWS Cloud border
   - Region boundary
   - Grid: 10px, guides enabled

3. **Add AWS Services:**
   - Use official icons (70x70px)
   - Follow left-to-right flow
   - Group by function (compute, storage, etc.)

4. **Connect Flows:**
   - Number primary flows (1, 2, 3...)
   - Color-code by type
   - Add descriptive labels

5. **Add Detail Boxes:**
   - Component details (small boxes)
   - Info boxes (right side)

6. **Add Optional Components:**
   - Bottom of diagram
   - Smaller icons (60x60px)
   - Dashed connections

7. **Final Review:**
   - Check metadata present
   - Verify all flows labeled
   - Ensure consistent spacing
   - Validate color scheme

#### 9.2 File Naming
**Pattern:** `{component}-{purpose}-architecture.drawio`

**Examples:**
- `cloudfront-jwt-architecture.drawio`
- `api-gateway-auth-architecture.drawio`
- `lambda-processing-architecture.drawio`

### 10.0 Common Patterns

#### 10.1 Two S3 Buckets Pattern
When showing asset + log buckets:
- **Label clearly:** "S3 Bucket (Assets)" and "S3 Bucket (Logs)"
- **Add detail boxes** explaining each bucket's purpose
- **Show logging flow** from assets to logs (dashed line)
- **Include CloudTrail** flow to logs bucket

#### 10.2 Lambda@Edge Pattern
- **Position:** Between CloudFront and S3
- **Show:** Both success (green) and failure (red) paths
- **Detail box:** List key functions (verify, generate, etc.)
- **Connection to SSM:** Dashed line for secret retrieval

#### 10.3 Optional Components
- **Smaller icons:** 60x60px
- **Position:** Bottom of diagram
- **Label:** Include "(Optional)" suffix
- **Flows:** Dashed lines to main components

### 11.0 Quality Checklist

Before finalizing diagram:
- ✅ Metadata present (Project ID, Author, Date)
- ✅ AWS official icons used
- ✅ AWS color scheme followed
- ✅ All flows numbered and labeled
- ✅ Info boxes complete (4 boxes)
- ✅ Detail boxes for major components
- ✅ Region boundaries shown
- ✅ Consistent spacing (grid-aligned)
- ✅ No overlapping components
- ✅ All text readable (min 9pt)

### 12.0 Export & Sharing

#### 12.1 File Formats
**Source:**
- Keep `.drawio` file in `docs/` folder
- Never delete source file

**Export Options:**
- **PNG:** For embedding in docs (300 DPI)
- **SVG:** For web/presentations (vector)
- **PDF:** For printing (vector)

#### 12.2 Version Control
- Commit `.drawio` file to git
- Include in prototype documentation
- Reference in README.md if applicable

---

## Example: Complete Diagram Creation

### Scenario
Create architecture diagram for CloudFront JWT auth prototype.

### Commands
```bash
# Extract metadata
cd /Users/andyhop/dev/protoflow/prototypes/proto-s3-publish-vayfd-023
PROJECT_ID=$(basename $(pwd))
AUTHOR="Andy Hopper"
DATE=$(date +"%Y-%m-%d")

# Output: proto-s3-publish-vayfd-023 | Andy Hopper | 2025-11-19
```

### Diagram Elements
1. **Title:** "CloudFront JWT Authentication Architecture"
2. **Metadata:** "Project: proto-s3-publish-vayfd-023 | Author: Andy Hopper | Date: 2025-11-19"
3. **Region:** us-east-1 boundary
4. **Services:** User, CloudFront, Lambda@Edge, S3 (2), SSM, CloudTrail, CloudWatch
5. **Flows:** 6 numbered request flows + logging flows
6. **Info Boxes:** JWT Flow, Security, Performance, Key Details

### Result
- **File:** `docs/cloudfront-jwt-architecture.drawio`
- **Size:** 1200x900px
- **Components:** 10 AWS services + 4 info boxes
- **Flows:** 13 connections (6 primary + 7 secondary)

---

## Quick Reference

**Metadata Format:**
```
Project: {folder-name} | Author: Andy Hopper | Date: {YYYY-MM-DD}
```

**Standard Icon Size:**
- Main: 70x70px
- Optional: 60x60px

**Standard Colors:**
- Compute: Orange `#D05C17`
- Storage: Green `#277116`
- Security: Red `#C7131F`
- Networking: Purple `#5A30B5`

**Standard Flow Widths:**
- Primary: 3px
- Secondary: 2px
- Dashed: 2px

**Standard Info Box Size:**
- 240px wide
- 115-145px tall

---

**Last Updated:** 2025-11-19
**Version:** 1.0.0
