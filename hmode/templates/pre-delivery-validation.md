# Pre-Delivery Validation Checklist

**Prototype**: {PROTOTYPE_NAME}
**Customer/Initiative**: {CUSTOMER_NAME}
**Date**: {DELIVERY_DATE}
**Validated By**: {VALIDATOR_NAME}

---

## Security & Credentials

- [ ] **No AWS credentials**: No AWS access keys, secret keys, or session tokens found
- [ ] **No API keys**: No OpenAI, Anthropic, GitHub, Stripe, or other API keys found
- [ ] **No private keys**: No RSA, SSH, or PEM private keys found
- [ ] **No database credentials**: No connection strings with embedded passwords
- [ ] **No hardcoded passwords**: No password variables or basic auth credentials
- [ ] **No OAuth tokens**: No bearer tokens, JWT tokens, or session tokens
- [ ] **`.gitignore` configured**: Sensitive files (`.env`, `*.pem`, `secrets.json`) in `.gitignore`
- [ ] **Git history clean**: No secrets committed to git history

**Security Scan Results:**
- Critical issues: {CRITICAL_COUNT}
- High issues: {HIGH_COUNT}
- Medium issues: {MEDIUM_COUNT}
- Low issues: {LOW_COUNT}

**Action taken**: {SECURITY_ACTION}

---

## Sensitive Information & PII

- [ ] **No PII in code**: No names, emails, phone numbers, addresses in source code
- [ ] **No PII in docs**: Documentation contains no customer PII
- [ ] **No real data**: Test data is synthetic, no production data samples
- [ ] **No internal URLs**: No internal AWS URLs, dashboards, or wiki links
- [ ] **No customer identifiers**: No customer account IDs, ARNs, or unique identifiers
- [ ] **No email addresses**: No real email addresses (except generic examples)
- [ ] **No phone numbers**: No real phone numbers in code or docs

**PII Scan Results**: {PII_SCAN_RESULTS}

---

## AWS Intellectual Property (XIP)

- [ ] **XIP tag verified**: `.project` file checked for XIP tag
- [ ] **Appropriate disclaimer**: Using correct disclaimer (XIP vs non-XIP)
- [ ] **No AWS internal frameworks**: Or properly disclosed if included (MIRA, CDAT, SRA, etc.)
- [ ] **No AWS templates**: No internal PR/FAQ, 6-pager, or assessment templates (unless disclosed)
- [ ] **No AWS methodologies**: No internal engagement patterns or frameworks (unless disclosed)
- [ ] **No AWS reporting formats**: No internal reporting or assessment formats (unless disclosed)
- [ ] **Partner messaging compliant**: AWS Partner guidelines followed if applicable

**XIP Status**: {XIP_STATUS}
**Disclaimer Used**: {DISCLAIMER_TYPE}

---

## Documentation Quality

- [ ] **README complete**: Installation, usage, tech stack documented
- [ ] **NARRATIVE generated**: Comprehensive technical narrative included
- [ ] **AUTHOR info populated**: Author information with customer context
- [ ] **DISCLAIMER included**: Appropriate AWS SA disclaimer present
- [ ] **Diagrams rendered**: All Mermaid and DrawIO diagrams render correctly
- [ ] **Presentation functional**: Slidev presentation runs without errors
- [ ] **AWS style compliant**: All docs follow Amazon writing standards
- [ ] **No m-dashes**: No AI-generated m-dash overuse ("—")
- [ ] **Citations present**: Claims have appropriate citations/references
- [ ] **Specific metrics**: Vague language replaced with quantified outcomes

**Writing Quality Score**: {QUALITY_SCORE}

---

## AWS Style Compliance

- [ ] **CSAT not NPS**: Customer satisfaction metric is CSAT, not NPS
- [ ] **Specific dates**: "Q2 2024" instead of "recently"
- [ ] **Quantified claims**: Numbers, percentages, thresholds included
- [ ] **Active voice**: >80% active voice usage
- [ ] **AWS terminology**: "As an AWS Partner", "in AWS Marketplace" (not "on")
- [ ] **No fear-based security**: "malicious actor" not "hacker", "security incident" not "breach"
- [ ] **Leadership principles**: AWS LP language where appropriate
- [ ] **Dense writing**: No filler words, concise phrasing

**AWS Style Issues**: {AWS_STYLE_ISSUE_COUNT}

---

## Code Quality

- [ ] **Builds successfully**: Code compiles/runs without errors
- [ ] **Tests pass**: All unit and integration tests pass
- [ ] **No debug code**: No console.log, print statements, or debug flags
- [ ] **No commented code**: Minimal commented-out code blocks
- [ ] **Dependencies documented**: `package.json`, `requirements.txt`, etc. complete
- [ ] **License compliance**: All dependencies have compatible licenses
- [ ] **No malware**: Code scanned, no malicious patterns found
- [ ] **Error handling**: Appropriate error handling and logging

**Build Status**: {BUILD_STATUS}
**Test Coverage**: {TEST_COVERAGE}%

---

## Technical Accuracy

- [ ] **Architecture diagrams accurate**: Diagrams match actual implementation
- [ ] **Tech stack correct**: Technologies listed match what's used
- [ ] **API docs current**: API documentation matches current endpoints
- [ ] **Installation tested**: Installation steps verified on clean environment
- [ ] **Examples work**: Code examples and demos function correctly
- [ ] **Links valid**: All URLs and links work (no 404s)
- [ ] **Version numbers accurate**: Software versions in docs match actual dependencies

**Technical Review**: {TECHNICAL_REVIEW_STATUS}

---

## Delivery Package Contents

- [ ] **DISCLAIMER.md**: Present and correct (XIP-aware)
- [ ] **AUTHOR.md**: Present with customer context
- [ ] **README.md**: Copied from prototype
- [ ] **NARRATIVE.md**: Comprehensive technical documentation
- [ ] **PRESENTATION.slides.md**: Slidev presentation (13 slides)
- [ ] **artifacts/diagrams/**: Architecture diagrams (DrawIO + Mermaid)
- [ ] **src/**: Source code copied
- [ ] **docs/**: Additional documentation
- [ ] **delivery-email.txt**: Draft email ready
- [ ] **ZIP archive**: Created and tested

**Package Size**: {PACKAGE_SIZE_MB} MB
**File Count**: {FILE_COUNT} files

---

## Customer Context

- [ ] **Customer name included**: Folder name includes customer/initiative identifier
- [ ] **Engagement context**: AUTHOR.md has relevant engagement details
- [ ] **Email personalized**: Delivery email references customer context
- [ ] **Presentation customized**: Slides include customer-specific use case
- [ ] **Problem statement relevant**: Docs address customer's actual problem

**Customer/Initiative**: {CUSTOMER_NAME}

---

## Legal & Compliance

- [ ] **License included**: Appropriate license or usage terms present
- [ ] **No copyrighted material**: No unauthorized use of copyrighted code/content
- [ ] **Attribution present**: Third-party code/content properly attributed
- [ ] **Export compliance**: No export-controlled technologies
- [ ] **GDPR/privacy**: No personal data violations
- [ ] **AWS branding compliant**: AWS marks/logos used per guidelines (if any)

**Legal Review Status**: {LEGAL_REVIEW_STATUS}

---

## Final Checks

- [ ] **ZIP file tested**: Archive extracts successfully, no corruption
- [ ] **File permissions**: No world-writable files, appropriate permissions
- [ ] **File paths relative**: No absolute paths to local machine
- [ ] **No temp files**: No `.DS_Store`, `Thumbs.db`, `.swp` files
- [ ] **No IDE configs**: No `.vscode/`, `.idea/` unless intentional
- [ ] **No build artifacts**: No `node_modules/`, `dist/`, `__pycache__/` in ZIP
- [ ] **Presentation tested**: `npx slidev PRESENTATION.slides.md` works
- [ ] **Email reviewed**: Delivery email copy-paste ready

---

## Automated Scan Summary

**Security Scan** (`/scan-security`):
- Status: {SECURITY_SCAN_STATUS}
- Critical issues: {CRITICAL_COUNT}
- Action: {SECURITY_ACTION_TAKEN}

**AWS Style Check** (`/amazon-style-checker`):
- Status: {AWS_STYLE_STATUS}
- Issues found: {AWS_STYLE_ISSUE_COUNT}
- Issues fixed: {AWS_STYLE_FIXED_COUNT}

**Writing Quality** (`/writing-quality`):
- Grade: {QUALITY_GRADE}
- Active voice: {ACTIVE_VOICE_PERCENT}%
- Citations: {CITATION_COUNT}/{REQUIRED_CITATIONS}

---

## Sign-Off

**Validated By**: {VALIDATOR_NAME}
**Date**: {VALIDATION_DATE}
**Status**: {PASS/FAIL/CONDITIONAL}

**Notes**:
{VALIDATION_NOTES}

**Approved for Delivery**: [ ] Yes [ ] No [ ] With conditions

**Conditions** (if any):
{CONDITIONS}

---

## Delivery Instructions

1. **Review email**: Open `delivery-email.txt`, customize if needed
2. **Test presentation**: Run `npx slidev PRESENTATION.slides.md` to preview
3. **Verify ZIP**: Extract ZIP to test directory, verify contents
4. **Send package**:
   - Attach: `{DELIVERY_ZIP_FILENAME}.zip`
   - Email body: Copy from `delivery-email.txt`
   - Recipients: {RECIPIENTS}
5. **Follow up**: Schedule technical walkthrough if requested

---

## Validation Checklist Legend

- ✅ **Passed**: Item validated, no issues
- ⚠️ **Warning**: Minor issue, acceptable for delivery
- ❌ **Failed**: Critical issue, blocks delivery
- ⏭️ **N/A**: Not applicable to this prototype

---

*This checklist was auto-generated by `/prepare-delivery` on {GENERATION_DATE}*
*Validate all items before customer delivery*
