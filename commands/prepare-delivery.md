---
uuid: cmd-prep-del-9m0n1o2p
version: 1.0.0
last_updated: 2025-11-11
description: Prepare prototype or idea for customer delivery
---

# Prepare Delivery Package

Package `{proto_name}` for customer delivery with documentation, diagrams, presentation, and email draft.

## Usage

```bash
/prepare-delivery proto-027-semantic-schema-mapper [--ideas] [--diagrams=essential|all|mermaid|drawio]
```

**Arguments:**
- `{proto_name}`: Prototype name (e.g., proto-027-semantic-schema-mapper)
- `--ideas`: Look in ideas/ directory instead of prototypes/ (optional)
- `--diagrams=essential`: Diagram detail level (optional, default: essential)
  - `essential`: DrawIO + one Mermaid diagram based on project type
  - `all`: DrawIO + Mermaid sequence + UML + architecture
  - `mermaid`: Only Mermaid diagrams
  - `drawio`: Only DrawIO diagrams

**Interactive Prompt:**
After validating the prototype, the skill will ask:
```
Customer/Initiative name for delivery package? (e.g., "acme-corp", "q4-migration", "poc")
```

This name will be included in the delivery folder path.

## Output Structure

Creates `artifacts/delivery/YYYY-MM-DD-{customer-name}-{proto-name}/` with:

```
artifacts/delivery/2025-11-11-acme-corp-semantic-schema-mapper/
├── PRE-DELIVERY-VALIDATION.md # Validation checklist with scan results
├── DISCLAIMER.md              # AWS SA disclaimer
├── AUTHOR.md                  # Author info + customer context
├── README.md                  # Project overview
├── NARRATIVE.md               # Project documentation
├── PRESENTATION.slides.md     # Slidev presentation
├── diagrams/
│   ├── architecture.drawio    # DrawIO architecture diagram
│   ├── architecture.md        # Mermaid architecture (if --diagrams=all)
│   ├── sequence.md            # Mermaid sequence (if --diagrams=all)
│   └── uml.md                 # Mermaid UML (if --diagrams=all)
├── src/                       # Source code (copied from prototype)
├── docs/                      # Documentation (copied from prototype)
└── delivery-email.txt         # Draft email for customer
```

Plus: `artifacts/delivery/2025-11-11-acme-corp-semantic-schema-mapper.zip`

## Workflow

### Step 1: Validate Input

1. **Parse arguments**:
   - Extract `{proto_name}` from first argument
   - Check for `--ideas` flag → search in ideas/ directory
   - Check for `--diagrams=` flag → default to `essential`

2. **Validate prototype exists**:
   - Default: Check `prototypes/{proto_name}/`
   - With `--ideas`: Check `ideas/{proto_name}/`
   - If not found: Error and list available prototypes

3. **Read `.project` file**:
   - Load `{proto_dir}/.project` to get metadata
   - Extract: name, current_phase, description, tech_stack, tags

### Step 2: Prompt for Customer/Initiative Name

4. **Ask user for customer/initiative name**:
   - Use AskUserQuestion tool
   - Prompt: "Customer/Initiative name for delivery package?"
   - Examples: "acme-corp", "q4-migration", "fintech-poc", "maxex"
   - Validation: Lowercase, alphanumeric + hyphens only
   - If user provides invalid format: Convert to valid (lowercase, replace spaces/special chars with hyphens)

**Example interaction:**
```
Customer/Initiative name for delivery package? (e.g., "acme-corp", "q4-migration", "poc")
> MaxEx Lending Platform

Normalized to: maxex-lending-platform
```

### Step 3: Create Delivery Directory

5. **Generate directory name**:
   - Format: `YYYY-MM-DD-{customer-name}-{proto-name}` (strip "proto-XXX-" prefix)
   - Example: `2025-11-11-acme-corp-semantic-schema-mapper`
   - Full path: `/Users/andyhop/dev/protoflow/artifacts/delivery/{date-customer-name}/`

6. **Create directory structure**:
   ```bash
   mkdir -p artifacts/delivery/{date-name}/diagrams
   mkdir -p artifacts/delivery/{date-name}/src
   mkdir -p artifacts/delivery/{date-name}/docs
   ```

### Step 4: Copy Project Files

7. **Copy source code**:
   - If prototype (Phase 7-8): Copy `src/`, `package.json`, `requirements.txt`, etc.
   - If idea (Phase 1-6): Copy all `.md` files from idea directory

8. **Copy documentation**:
   - Copy `README.md`, `docs/`, design docs
   - Preserve directory structure

### Step 5: Generate Disclaimer & Author Info

9. **Create DISCLAIMER.md**:
   - Use AWS SA disclaimer template
   - Include customer engagement context
   - Add IP notices (XIP tag if applicable)
   - Include license info

10. **Create AUTHOR.md**:
   - Author name: "Andy Hopper"
   - Role: "Startup AI/ML Solutions Architect, AWS"
   - Date: {current_date}
   - Customer context: Use provided customer/initiative name
   - Replace placeholders in template with actual customer name
   - Contact info: (optional, can be generic)

11. **Create PRE-DELIVERY-VALIDATION.md**:
   - Use checklist template from `hmode/templates/pre-delivery-validation.md`
   - Fill in automated scan results (security, AWS style, writing quality)
   - Populate customer name, prototype name, date
   - Include validation status for each category
   - Leave manual checkboxes for final review

### Step 6: Generate Project Narrative

12. **Invoke /generate-project-narrative**:
    - Input: prototype directory path
    - Output: `NARRATIVE.md` in delivery directory
    - Content: Problem statement, solution approach, architecture, tech stack, usage

### Step 7: Generate Diagrams

13. **Invoke /generate-project-diagram**:
    - Input: prototype directory, diagram level (--diagrams flag)
    - Output: Diagrams in `diagrams/` subdirectory
    - Types based on diagram level:
      - `essential`: architecture.drawio + best Mermaid diagram for project type
      - `all`: architecture.drawio + sequence.md + uml.md + architecture.md
      - `mermaid`: Only Mermaid diagrams
      - `drawio`: Only DrawIO diagram

### Step 8: Generate Presentation

14. **Invoke /generate-project-presentation**:
    - Input: prototype directory, NARRATIVE.md
    - Output: `PRESENTATION.slides.md` (Slidev format)
    - Content: Title, problem, solution, architecture, demo, next steps

### Step 9: Run Security & Quality Scans

15. **Run automated scans**:
   - `/remove-employee-configs {proto_dir} --report={delivery_dir}/EMPLOYEE_CONFIG_SCAN.md` → remove AWS employee tool references
   - `/scan-security {proto_dir} --report={delivery_dir}/SECURITY_SCAN.md` → scan for credentials, keys, secrets
   - `/amazon-style-checker NARRATIVE.md` → validate AWS style
   - `/amazon-style-checker PRESENTATION.slides.md` → validate presentation style
   - `/writing-quality NARRATIVE.md` → check documentation quality
   - Capture results for PRE-DELIVERY-VALIDATION.md

16. **Update validation checklist**:
   - Populate automated scan results in PRE-DELIVERY-VALIDATION.md
   - Mark checkboxes based on scan outcomes:
     - ✅ Employee configs: 0 references found
     - ⚠️ Employee configs: References removed (review auto-fixes)
     - ❌ Employee configs: Complex integrations require manual review
     - ✅ Security: 0 critical issues
     - ⚠️ Security: Medium issues only
     - ❌ Security: Critical issues found (blocks delivery)
   - Include metrics: issue counts, quality scores, compliance status
   - `/amazon-style-checker NARRATIVE.md` → fix AWS style issues
   - `/amazon-style-checker PRESENTATION.slides.md` → fix AWS style issues
   - `/writing-quality NARRATIVE.md` → check writing quality
   - Apply fixes automatically for delivery content

### Step 10: Generate Delivery Email

17. **Invoke /generate-delivery-email**:
    - Input: prototype metadata, NARRATIVE.md, delivery directory path
    - Output: `delivery-email.txt` in delivery directory
    - Format: 3-5 paragraph dense Amazon style email
    - Content: Context, what's included, key highlights, next steps

### Step 11: Create ZIP Archive

18. **Create ZIP file**:
    ```bash
    cd artifacts/delivery/
    zip -r {date-name}.zip {date-name}/
    ```
    - Output: `artifacts/delivery/{date-name}.zip`
    - Exclude: `.DS_Store`, `node_modules/`, `__pycache__/`, `.git/`

### Step 12: Final Report

19. **Display delivery summary**:

```markdown
# Delivery Package Created

**Prototype**: {proto_name}
**Customer/Initiative**: {customer_name}
**Date**: {current_date}
**Location**: `artifacts/delivery/{date-customer-name}/`

---

## Package Contents

✅ DISCLAIMER.md - AWS SA disclaimer + IP notices
✅ AUTHOR.md - Author info + customer context
✅ README.md - Project overview
✅ NARRATIVE.md - Complete project documentation
✅ PRESENTATION.slides.md - Slidev presentation
✅ diagrams/ - Architecture diagrams (DrawIO + Mermaid)
✅ src/ - Source code
✅ docs/ - Additional documentation
✅ delivery-email.txt - Draft email for customer
✅ PRE-DELIVERY-VALIDATION.md - Validation checklist with automated scan results
✅ EMPLOYEE_CONFIG_SCAN.md - AWS employee tool reference scan
✅ SECURITY_SCAN.md - Security scan report

---

## ZIP Archive

📦 `artifacts/delivery/{date-customer-name}.zip` ({size} MB)

---

## Draft Email

{Display contents of delivery-email.txt}

---

## Validation Results

**Employee Config Scan**:
- Tool references: {reference_count}
- Files cleaned: {files_modified}
- Status: {CLEAN/AUTO_FIXED/MANUAL_REVIEW}

**Security Scan**:
- Critical: {critical_count} ✅/❌
- High: {high_count}
- Status: {PASS/BLOCKED}

**AWS Style**: {issue_count} issues found, {fixed_count} auto-fixed
**Writing Quality**: Grade {grade}, {active_voice}% active voice

**Delivery Status**: {READY/BLOCKED/REVIEW_REQUIRED}

---

## Next Steps

1. **Review validation**: `open artifacts/delivery/{date-customer-name}/PRE-DELIVERY-VALIDATION.md`
2. **Complete manual checks**: Validate items in checklist
3. Review delivery package: `cd artifacts/delivery/{date-customer-name}`
4. Test presentation: `npx slidev PRESENTATION.slides.md`
5. Customize email: `open artifacts/delivery/{date-customer-name}/delivery-email.txt`
6. **Sign off checklist**: Mark "Approved for Delivery"
7. Send to customer: Copy email + attach ZIP file

---

✅ Delivery package ready for customer
```

## Sub-Skills Used

This command orchestrates multiple sub-skills:

1. **/remove-employee-configs** - Removes AWS employee tool references
2. **/scan-security** - Scans for credentials, keys, secrets
3. **/generate-project-narrative** - Creates comprehensive project documentation
4. **/generate-project-diagram** - Generates DrawIO and Mermaid diagrams
5. **/generate-project-presentation** - Creates Slidev presentation
6. **/generate-delivery-email** - Drafts AWS-style email
7. **/amazon-style-checker** - Validates AWS writing standards
8. **/writing-quality** - Checks documentation quality

## AWS SA Disclaimer Template

**DISCLAIMER.md** content:

```markdown
# Disclaimer

## Customer Engagement

This prototype was developed by Andy Hopper, Startup AI/ML Solutions Architect at AWS, as part of customer engagement activities.

## Intellectual Property

**Copyright © 2025 Andy Hopper. All rights reserved.**

This code and documentation are provided "as-is" without warranty of any kind, express or implied. This is prototype/demonstration code intended for evaluation purposes only.

## AWS Relationship

This prototype was created during my role at AWS but does not represent official AWS services, features, or recommendations. Any opinions expressed are my own and not those of Amazon Web Services, Inc.

## Usage Terms

- **Evaluation**: Free to evaluate and test in non-production environments
- **Modification**: You may modify this code for your internal use
- **Distribution**: Redistribution requires prior written permission
- **Support**: No official support provided; use at your own risk
- **Liability**: Author and AWS assume no liability for any damages

## Open Source Dependencies

This project may include open-source libraries. See `package.json` or `requirements.txt` for dependency licenses.

## XIP Notice

{If project has XIP tag:}
⚠️ **AWS Intellectual Property**: This prototype includes AWS-internal frameworks, templates, or methodologies. Contact your AWS account team before external distribution.

{Otherwise: omit this section}

---

**Contact**: For questions about this prototype, contact your AWS Solutions Architect or account team.

**Date**: {current_date}
```

## AUTHOR.md Template

```markdown
# Author Information

## Author

**Name**: Andy Hopper
**Role**: Startup AI/ML Solutions Architect, Amazon Web Services (AWS)
**Background**: Ex-startup founder & CTO, specializing in rapid prototyping and AI/ML solutions

## Customer Context

{If available from .project metadata or user input:}
This prototype was developed for **{customer_name}** to address **{problem_statement}**.

{Otherwise:}
This prototype demonstrates **{technology/approach}** for **{use_case}**.

## Engagement Type

Prototype development and technical consultation as part of AWS customer engagement.

## Date

**Created**: {date_from_project_file}
**Delivered**: {current_date}

---

*For questions or follow-up, contact your AWS account team.*
```

## Error Handling

**Prototype not found:**
```
Error: Prototype 'proto-027-semantic-schema-mapper' not found

Searched:
- prototypes/proto-027-semantic-schema-mapper/ ❌

Available prototypes:
- proto-001-loan-document-validator
- proto-015-claude-power-tools
- proto-026-meme-generator

Use: /list-prototypes to see all available prototypes
Use: /prepare-delivery {proto-name} --ideas to search in ideas/
```

**Missing required files:**
```
Warning: README.md not found in prototype directory
Creating README.md from .project metadata...
```

**Validation failures:**
```
Warning: NARRATIVE.md has 3 AWS style issues
Auto-fixing issues before adding to delivery package...
✅ Fixed 3 issues
```

## Best Practices

1. **Always validate content** before packaging
2. **Apply AWS style** automatically to all generated docs
3. **Include all dependencies** in package (package.json, requirements.txt)
4. **Test diagrams render** before adding to package
5. **Customize email** for specific customer context
6. **Review XIP tags** and add appropriate notices

## Integration

Works with existing slash commands:
- Uses `/visualize` logic for diagram generation
- Uses `/amazon-style-checker` for validation
- Uses `/writing-quality` for doc quality checks
- Leverages existing style guide and templates

---

Be thorough, professional, and AWS-standards focused.
