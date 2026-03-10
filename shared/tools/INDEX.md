<!-- File UUID: c4e2a1b8-7d3f-4e9c-8a5b-2f6d9c1e3b7a -->
# shared/tools — Tool Index

Quick reference for all tools. Grouped by purpose.

## AWS & S3

| Tool | Description |
|------|-------------|
| `s3publish.py` | Upload files to S3 with public URLs |
| `s3backup.py` | Backup monorepo to S3 with semantic indexing |
| `s3backup_subscriber.py` | Subscribe to S3 backup events |
| `s3backup-config.yaml` | S3 backup configuration |
| `s3backup-notifications/` | CDK stack for backup notifications |
| `s3backup-semantic-search/` | Semantic search over S3 backups (frontend + infra) |
| `generate_bedrock_longterm_key.py` | Generate long-term Bedrock API key |
| `generate_bedrock_shortterm_key.py` | Generate short-term Bedrock API key |
| `bedrock_key_export.sh` | Export Bedrock keys to environment |
| `sync-amplify-to-ssm.py` | Sync Amplify configs to SSM Parameter Store |
| `sync-infra-to-ssm.py` | Sync infrastructure outputs to SSM |
| `migrate-ssm-params.sh` | Migrate SSM parameters between accounts |

## Infrastructure & Auditing

| Tool | Description |
|------|-------------|
| `infra-import.py` | Import CloudFormation stacks into Capistrano structure |
| `infra-audit.py` | AWS infrastructure drift detection |
| `audit-hardcoded-infra.py` | Find hardcoded AWS resource IDs in codebase |
| `infra-grid-generator.py` | Generate infrastructure visualization grids |
| `project-audit/` | Infrastructure and project auditing tools |

## Deployment & Validation

| Tool | Description |
|------|-------------|
| `generate-buildinfo.py` | Generate buildinfo.json (git metadata + stack outputs) |
| `post-deploy-validate.py` | Post-deployment smoke tests and validation |
| `validate-cdk-deployment.ts` | CDK stack validation |
| `validate-deployment-config.py` | Deployment config validation |
| `check_url.py` | URL health check utility |

## Code Analysis

| Tool | Description |
|------|-------------|
| `ast_extractor.py` | Extract public API signatures via tree-sitter |
| `dir_summarizer.py` | Smart directory analysis using local LLM |
| `file_analyzer.py` | Analyze files/images/PDFs using Claude API |
| `diagram-generator/` | Architecture diagram generation CLI |
| `relationship-graph/` | Project dependency relationship mapping |

## AI/ML & LLM

| Tool | Description |
|------|-------------|
| `rlhf_tracker.py` | Log RLHF reward/punishment signals |
| `ollama-bridge/` | Local Ollama LLM integration with MCP tools |
| `claude-exporter/` | Claude session analytics and export |
| `mcp-direct-client/` | Direct Model Context Protocol client |
| `mcp-cli-wrappers/` | CLI wrappers for MCP tools |

## Project Management

| Tool | Description |
|------|-------------|
| `brownfield-audit/` | Legacy/brownfield project analysis (1,500+ lines) |
| `project-classifier/` | Auto-classify projects by type/maturity |
| `proposal-scorer/` | Score and rank proposals |
| `pre_code_gate.py` | SDLC gate: enforce phase requirements before code |
| `acceptance_criteria.py` | Generate acceptance criteria from requirements |

## Generation & Grids

| Tool | Description |
|------|-------------|
| `generate-complete-grid.py` | Generate complete project infrastructure grid |
| `generate-enhanced-grid.py` | Generate enhanced grid with resource details |
| `generate-manifest.js` | Generate asset manifests |
| `domain-generator/` | Generate domain model types from schemas |

## File Integrity

| Tool | Description |
|------|-------------|
| `add-file-uuids.py` | Add UUID headers to files for tracking |
| `integrity-check.js` | Check asset integrity |
| `fix-integrity-issues.js` | Fix asset integrity issues |

## Testing

| Tool | Description |
|------|-------------|
| `auth-e2e-tester/` | End-to-end authentication testing (Playwright) |
| `app-screenshot-pdf/` | Screenshot to PDF conversion |
| `screenshot/` | Screenshot utilities (Node.js) |
| `tests/` | Test suite for shared tools |

## Setup & Installation

| Tool | Description |
|------|-------------|
| `install-global-tools.sh` | Install global Python tools |
| `install-node-tools.sh` | Install global Node.js tools |
| `install-tmux-picker.sh` | Install tmux session picker |
| `auto-setup.sh` | Automated environment setup |
| `sparse-checkout/` | Sparse git checkout utilities |
| `create-prototype.sh` | Quick prototype scaffolding |

## Utilities

| Tool | Description |
|------|-------------|
| `_logger.py` | Shared structured logger (JSON + console) |
| `ask_human.py` | Prompt human for interactive decisions |
| `tmux-claude-picker` | Tmux session picker for Claude Code |

## Mobile

| Tool | Description |
|------|-------------|
| `android-kiosk-setup/` | Android kiosk configuration |

## Other

| Tool | Description |
|------|-------------|
| `sdlc-infographic/` | SDLC visualization infographic |
| `semantic-run/` | Semantic search runner and indexer |
| `proto-launcher` | Prototype launcher utility |
