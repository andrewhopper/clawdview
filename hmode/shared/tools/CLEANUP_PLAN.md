<!-- File UUID: 7c2e4a91-3f8b-4d7c-b5a2-9e1f0c3d6e8a -->
# Vibe Code Cleanup Plan — shared/tools

> Project: shared/tools (Hopper Labs monorepo shared utilities)
> Path: /Users/andyhop/dev/hopperlabs/shared/tools/
> Generated: 2026-03-01
> Findings: 48 total (6 critical, 16 high, 18 medium, 8 low)

---

## Summary

| # | Category | Critical | High | Medium | Low | Total |
|---|----------|----------|------|--------|-----|-------|
| 1 | Structure & Duplication | 1 | 2 | 2 | 0 | 5 |
| 2 | Deploy & Config Hygiene | 3 | 2 | 1 | 0 | 6 |
| 3 | CDK Patterns | 0 | 1 | 1 | 1 | 3 |
| 4 | Code Quality / IA | 0 | 3 | 4 | 2 | 9 |
| 5 | Models & Schema | 0 | 1 | 3 | 1 | 5 |
| 6 | Security & Auth | 0 | 1 | 1 | 0 | 2 |
| 7 | Cognito & OAuth | 0 | 0 | 1 | 0 | 1 |
| 8 | Documentation | 0 | 1 | 2 | 2 | 5 |
| 9 | Observability | 2 | 3 | 2 | 1 | 8 |
| 10 | Config & Deps | 0 | 2 | 2 | 1 | 5 |
| | **TOTAL** | **6** | **16** | **19** | **8** | **49** |

---

## Critical

### 2.0 Deploy & Config Hygiene

**2.1** `infra-import.py:22` — Personal AWS profile `admin-507745175693` hardcoded as default.
Also at lines `:290`, `:418-419`. Any collaborator or CI environment using this tool will
silently target the personal account.
- Fix: Replace default with `AWS_PROFILE` env var (`os.environ.get("AWS_PROFILE", "default")`)
- Delegate: code-cleanup-agent

**2.2** `sparse-checkout/init-env.sh:34` — Personal AWS account ID hardcoded: `export AWS_ACCOUNT_ID="108782054816"`
- Fix: Replace with `AWS_ACCOUNT_ID` from env or `aws sts get-caller-identity --query Account`
- Delegate: code-cleanup-agent

**2.3** `generate-enhanced-grid.py:205` — Personal boto3 session hardcoded:
`session = boto3.Session(profile_name='admin-507745175693', region_name='us-east-1')`
Also at lines `:133`, `:144`, `:157` — hardcoded `.b.lfg.new` domain string used as detection logic.
- Fix: Read profile from `AWS_PROFILE` env; replace domain detection with configurable env var
- Also at line `:207`: `monorepo = Path('/Users/andyhop/dev/hopperlabs')` — hardcoded absolute path
- Fix for path: `Path.cwd()` or env var `HOPPERLABS_ROOT`
- Delegate: code-cleanup-agent

### 9.0 Observability

**9.1** 69 Python files use `print()` as their only output mechanism with no logger configured.
Includes core shared tools: `s3publish.py`, `file_analyzer.py`, `brownfield-audit/brownfield_audit.py`,
`diagram-generator/` (5 files), `semantic-run/` (15+ files), `pre_code_gate.py`, `infra-import.py`.
This means all tool output is unstructured, unredirectable, and lost in automated contexts.
- Fix: Add `logging.getLogger(__name__)` to each module; replace `print()` with `logger.info/warning/error()`
- Delegate: code-cleanup-agent

**9.2** No error tracker integrated anywhere across 69 Python files and all TypeScript tools.
Zero observability for failures in shared infrastructure tools (s3backup, s3publish, auth-e2e-tester).
- Fix: Integrate `@hopperlabs/error-tracker` or at minimum add `logging.exception()` in all bare `except` blocks
- Delegate: manual (`/add-error-tracker`)

---

## High

### 1.0 Structure & Duplication

**1.1** `diagram_generator/` is a symlink pointing to `diagram-generator/`. The symlink exists at root
level alongside the real directory. This causes confusion and potential double-inclusion issues with tools
that traverse directories.
- Fix: Remove the symlink `diagram_generator` — the canonical name is `diagram-generator`
- Delegate: project-cleanup-specialist

**1.2** `rlhf_tracker.py` (267 lines) and `rlhf-reward-punishment-tracker.py` (272 lines) serve different
purposes (reward/punishment logging vs. error-only CLI) but share a YAML backend and are not cross-referenced.
Creates confusion for callers about which tool to use.
- Fix: Consolidate into `rlhf_tracker.py` by adding an `error` subcommand; remove the standalone tracker
- Delegate: code-cleanup-agent

**1.3** `auth-e2e-tester/dist/` is committed to git (compiled JS output). The git-tracked `.venv`
directories at `semantic-run/.venv/` and `android-kiosk-setup/.venv/` contain full virtual environments
(including torch model dump JS, urllib3 source) — potentially MBs of binary/generated content in git history.
- Fix: Add `dist/`, `.venv/`, `__pycache__/`, `node_modules/` to a `shared/tools/.gitignore`;
  run `git rm --cached` for tracked artifacts
- Delegate: manual (`.gitignore` creation + `git rm --cached`)

### 2.0 Deploy & Config Hygiene

**2.4** `s3backup-config.yaml:6` — Personal AWS account ID committed in plain config:
`account_id: "507745175693"` and `bucket: hopperlabs-backups-507745175693`.
Also `s3backup-notifications/infra/app.py:33` uses this as a hardcoded fallback:
`os.environ.get("CDK_DEFAULT_ACCOUNT", aws_config.get("account_id", "507745175693"))`.
- Fix: Remove account_id from YAML; rely solely on `CDK_DEFAULT_ACCOUNT` / `aws sts get-caller-identity`
- Delegate: code-cleanup-agent

**2.5** `audit-hardcoded-infra.py:138` — The tool designed to detect hardcoded IDs has the work
account ID hardcoded in its detection list as a comment: `'108782054816',  # Your AWS account ID (from CLAUDE.md)`
This will fail for any user running the tool who is not "andyhop".
- Fix: Load the account detection list from env or `~/.aws/config` dynamically
- Delegate: code-cleanup-agent

### 3.0 CDK Patterns

**3.1** `ollama-bridge/ollama_bridge.py:28-30` — Three env vars with hardcoded URL/value fallbacks:
```python
BRIDGE_PORT = int(os.environ.get("OLLAMA_BRIDGE_PORT", "11435"))
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_DEFAULT_MODEL", "gpt-oss:20b")
```
The `http://` fallback for `OLLAMA_HOST` is insecure and commits a specific model name as default.
- Fix: Remove fallback strings; raise `ValueError` if not set; document in `.env.example`
- Delegate: code-cleanup-agent

### 4.0 Code Quality

**4.1** 29 files exceed 300 lines (project standard). Worst offenders:
- `brownfield-audit/brownfield_audit.py` — 1,512 lines
- `diagram-generator/templates.py` — 1,271 lines
- `post-deploy-validate.py` — 1,017 lines
- `diagram-generator/generators.py` — 940 lines
- `semantic-run/index_prototypes.py` — 930 lines
- `sparse-checkout/sparse_checkout.py` — 929 lines
- `diagram-generator/run_generator.py` — 899 lines
- `s3backup.py` — 725 lines

All violate the 300-500 line standard and indicate missing decomposition.
- Fix: Extract logical sections into module files per tool (e.g., `brownfield_audit/checks/`, `diagram_generator/templates/`)
- Delegate: code-cleanup-agent

**4.2** 28+ loose Python/shell files at root level with no subdirectory grouping.
Natural groupings exist but are unstructured:
- Infra tools: `infra-audit.py`, `infra-import.py`, `infra-grid-generator.py`, `sync-amplify-to-ssm.py`, `sync-infra-to-ssm.py`, `post-deploy-validate.py`
- Bedrock/AWS tools: `generate_bedrock_longterm_key.py`, `generate_bedrock_shortterm_key.py`, `bedrock_key_export.sh`
- Grid/reporting: `generate-buildinfo.py`, `generate-complete-grid.py`, `generate-enhanced-grid.py`, `infra-grid-generator.py`
- Install/setup: `auto-setup.sh`, `install-global-tools.sh`, `install-node-tools.sh`
- S3 tools: `s3backup.py`, `s3backup_subscriber.py`, `s3publish.py`

These should be grouped into subdirectories (`infra/`, `bedrock/`, `reporting/`, `setup/`) matching the existing
pattern used by `diagram-generator/`, `project-audit/`, `semantic-run/`, etc.
- Fix: Migrate loose root files into named subdirectories; update `README.md` index
- Delegate: information-architecture-agent

**4.3** `claude-exporter/scripts/data-download/download_all_sessions.py:38,258` —
Hardcoded absolute local machine paths:
```python
'output_dir': '/Users/andyhop/Desktop/claude_sessions_full_archive'
har_file = '/Users/andyhop/Desktop/claude.ai.har'
```
Also in `analyze_api_structure.py:174-175` and `extract_claude_data.py:143-144`.
- Fix: Replace with CLI arguments with `argparse`; use `Path.home()` for defaults
- Delegate: code-cleanup-agent

### 9.0 Observability

**9.3** 4 files use `logging.basicConfig()` — the unstructured, non-configurable Python logging setup.
These produce plain-text output with no JSON structure, no routing, and cannot be aggregated:
- `semantic-run/search_api.py:27`
- `s3backup.py:44`
- `s3backup_subscriber.py:58`
- `rlhf_tracker.py:43`

- Fix: Replace `basicConfig()` with a structured logger config (JSON formatter + `RotatingFileHandler`);
  adopt the pattern already in `semantic-run/logging_config.py` across all tools
- Delegate: code-cleanup-agent

**9.4** `semantic-run/` has a well-structured `logging_config.py` with `RotatingFileHandler` but this
pattern is not shared or reused by any of the 69 other files that need it.
- Fix: Move `semantic-run/logging_config.py` to a shared location (`shared/tools/logging_config.py`);
  import from there across all tools
- Delegate: code-cleanup-agent

**9.5** `s3backup-semantic-search/frontend/src/lib/amplify-config.ts:last line` — `API_URL` set with
empty string fallback `process.env.NEXT_PUBLIC_API_URL || ''`, meaning silent failure if env var missing.
- Fix: Use `getRequiredEnv()` (already defined in this file) instead of `|| ''`
- Delegate: code-cleanup-agent

### 10.0 Config & Deps

**10.1** `mcp-cli-wrappers/mcp_cli_wrappers/config.py:29` — Personal email hardcoded as default:
`default="andyhop+bedrock@amazon.com"`. Also in `tests/test_config.py:15` where the test asserts
this personal value as expected.
- Fix: Remove default email; require explicit configuration; update test to use a placeholder
- Delegate: code-cleanup-agent

**10.2** `pyproject.toml` (root tools) declares only 4 dependencies (`anthropic`, `boto3`, `pillow`, `pyyaml`)
but the 28+ root-level scripts import many more packages used without declaration:
- `requests` (used by `check_url.py`, `ask_human.py`)
- `rich` (used by multiple CLI tools)
- `click` (used by several tools)
- `tree-sitter*` (used by `ast_extractor.py` — only declared in `requirements.txt`, not `pyproject.toml`)
- `pydantic`, `pydantic-settings` (used by tools outside `mcp-cli-wrappers`)

This means `uv run` or `uv sync` on the root `pyproject.toml` will fail for most tools.
- Fix: Audit all imports across root-level scripts; add missing deps to `pyproject.toml`
- Delegate: code-cleanup-agent

---

## Medium

### 1.0 Structure & Duplication

**1.4** `auth-e2e-tester/tests/uat.spec.ts` (445 lines) and `auth-e2e-tester/tests/auth.spec.ts`
have significant overlap — both test the same `auth.b.lfg.new` login flow with near-identical
selectors and assertions. Likely evolved from copy-paste.
- Fix: Extract shared auth flow helpers into `tests/helpers/auth-flow.ts`; deduplicate specs
- Delegate: code-cleanup-agent

**1.5** Two conflicting `mcp-cli-wrappers/scripts/fetch_january_emails.py` and
`fetch_all_january_emails.py` — both are one-off scripts committed with no apparent ongoing use.
- Fix: Delete both if no longer needed; otherwise archive in a `scripts/archive/` subdirectory
- Delegate: project-cleanup-specialist

### 2.0 Deploy & Config Hygiene

**2.6** No `.gitignore` file at `shared/tools/` level. The root `.gitignore` covers some patterns
but `.venv/`, `dist/`, `__pycache__/` inside subdirectories should be covered locally.
- Fix: Create `shared/tools/.gitignore` with: `.venv/`, `dist/`, `__pycache__/`, `node_modules/`,
  `*.pyc`, `test-results/`, `*.log`, `.DS_Store`
- Delegate: manual

### 3.0 CDK Patterns

**3.2** `s3backup-notifications/infra/app.py:33` — CDK app uses `os.environ.get("CDK_DEFAULT_ACCOUNT", "507745175693")`
as fallback. CDK's own account resolution should be used instead; the hardcoded fallback masks
missing-config errors.
- Fix: Remove fallback literal; let CDK raise if account not configured
- Delegate: code-cleanup-agent

### 4.0 Code Quality

**4.4** `project-audit/audit.py:73` — Hardcoded absolute path with personal home directory:
```python
for candidate in [Path("/Users/andyhop/dev/lab"), Path.home() / "dev/lab"]:
```
The first candidate will always fail for any other user.
- Fix: Remove `/Users/andyhop/dev/lab`; use env var `LAB_ROOT` with `Path.home() / "dev/lab"` as default
- Delegate: code-cleanup-agent

**4.5** `validate-deployment-config.py` (714 lines) and `post-deploy-validate.py` (1,017 lines) are
both top-level deployment validation scripts with overlapping concerns (config validation, deploy checks).
- Fix: Determine canonical owner; consolidate into `deployment/` subdirectory with clear separation
  of pre-deploy config check vs. post-deploy smoke test
- Delegate: code-cleanup-agent

**4.6** `mcp-cli-wrappers/test_mcp_integrations.py` and `tests/` directory at root —
two separate test locations exist with no clear organization rule.
- Fix: Consolidate tests into `shared/tools/tests/`; remove top-level loose test files
- Delegate: information-architecture-agent

**4.7** `proto-launcher`, `tmux-claude-picker` — present as top-level directories but contain only
shell scripts with no README or subdirectory structure. Inconsistent with tool packaging pattern.
- Fix: Add README to each; or migrate shell scripts into a `bin/` or `scripts/` subdirectory
- Delegate: information-architecture-agent

### 5.0 Models & Schema

**5.1** `validate-cdk-deployment.ts` uses `as any` in 6 places including `extractS3Buckets(template: any)`.
The CloudFormation template shape is well-known and should be typed.
- Fix: Define `CfnTemplate` interface; replace `any` with typed parameters
- Delegate: domain-modeling-specialist

**5.2** `acceptance_criteria.py` uses `List[Dict[str, Any]]` as return type for all criteria methods
(lines `:39`, `:59`, `:98`, `:132`, `:182`, `:214`, `:238`). The criteria dict structure is consistent
but untyped.
- Fix: Define `Criterion` TypedDict or Pydantic model; replace `Dict[str, Any]` returns
- Delegate: domain-modeling-specialist

**5.3** `proposal-scorer/proposal_scorer.py` uses bare `dict` in 8 function signatures
(`load_project`, `save_project`, `calculate_score`, `check_gate`, etc.) and has 3 `@dataclass`
models with manual `to_dict()` / `from_dict()` methods. Pydantic would eliminate this boilerplate.
- Fix: Migrate `RICEScore`, `WSJFScore`, `ProposalScore` dataclasses to Pydantic BaseModel
- Delegate: domain-modeling-specialist

### 6.0 Security & Auth

**6.1** `s3backup-semantic-search/frontend/src/lib/amplify-config.ts` — OAuth `redirectSignIn` and
`redirectSignOut` fallback to `http://localhost:3000` (insecure) when `window` is not available.
In SSR contexts this silently uses an insecure redirect.
- Fix: Use `process.env.NEXT_PUBLIC_REDIRECT_URL` with env validation; remove localhost fallback
- Delegate: cognito-expert-agent

### 8.0 Documentation

**8.1** Three separate README files exist at root in addition to `README.md`:
`README-INTEGRITY-CHECK.md`, `README-s3backup.md`, `README-s3publish.md`.
These belong in their respective tool subdirectories or as sections of the main README.
- Fix: Move content into tool-specific directories or consolidate into `README.md` as sections
- Delegate: manual

**8.2** `mcp-cli-wrappers/README.md` (586 lines) and `semantic-run/README.md` (434 lines) are
excessively verbose. `semantic-run/` alone has 15 separate markdown files totalling ~6,500 lines.
- Fix: Densify to essential quick-start + link to supporting docs; target < 150 lines for main READMEs
- Delegate: manual

### 9.0 Observability

**9.6** `semantic-run/search_api.py:27` uses `logging.basicConfig(level=logging.INFO)` with no
JSON format or file transport, while the same directory has `logging_config.py` that defines proper
`RotatingFileHandler`. Inconsistent within the same tool.
- Fix: Replace `basicConfig` in `search_api.py` with `setup_logging()` from `logging_config.py`
- Delegate: code-cleanup-agent

### 10.0 Config & Deps

**10.3** 24 files scatter `os.environ` / `process.env` reads with no centralized config module
(outside `semantic-run/` which has its own `config.py`). Key offenders:
`s3publish.py`, `s3backup.py`, `file_analyzer.py`, `infra-import.py`, `auth-e2e-tester/src/config.ts`.
- Fix: Create `shared/tools/config.py` as a centralized settings module for root-level scripts;
  `auth-e2e-tester` already has `src/config.ts` — ensure all env reads go through it
- Delegate: code-cleanup-agent

**10.4** `requirements.txt` is orphaned — it only declares `tree-sitter*` packages but does not
correspond to `pyproject.toml`. Having both creates confusion: which one should `uv sync` use?
- Fix: Migrate `tree-sitter*` deps into `pyproject.toml` as optional extras; delete `requirements.txt`
- Delegate: code-cleanup-agent

---

## Low

### 3.0 CDK Patterns

**3.3** `validate-cdk-deployment.ts` instantiates AWS SDK clients directly (`new CloudFormationClient()`,
`new S3Client()`) with no dependency injection. Region defaults to `us-east-1` if env var missing.
- Fix: Accept region as a CLI argument; document the requirement
- Delegate: code-cleanup-agent

### 4.0 Code Quality

**4.8** `validate-cdk-deployment-package.json` is a standalone `package.json` at root level for a single
TypeScript file (`validate-cdk-deployment.ts`). It creates a phantom npm package at root.
- Fix: Move into a `validate-cdk/` subdirectory or integrate into an existing package
- Delegate: information-architecture-agent

### 5.0 Models & Schema

**5.4** `sync-infra-to-ssm.py:51` uses `@dataclass` with `metadata: Dict[str, Any] = field(default_factory=dict)`.
No validation on the metadata dict.
- Fix: Add TypedDict for known metadata keys; validate on construction
- Delegate: domain-modeling-specialist

### 7.0 Cognito & OAuth

**7.1** `auth-e2e-tester/src/config.ts` defines `AUTH_TARGETS` with per-app `cognitoDomain: 'auth.b.lfg.new'`
hardcoded in three separate entries. Any domain change requires 3 edits.
- Fix: Extract `COGNITO_DOMAIN` as a top-level constant read from env var; reference it in all targets
- Delegate: code-cleanup-agent

### 8.0 Documentation

**8.3** `mcp-cli-wrappers/README.md:218` references an internal Amazon Quip URL
(`https://quip-amazon.com/xxxxx`) as an example. This leaks internal tooling details.
- Fix: Replace with a generic placeholder URL in the example
- Delegate: manual

**8.4** `VALIDATE_CDK_README.md:270` links to a 2025/11 CloudFormation announcement URL.
Docs referencing dated AWS announcements become stale and should reference stable doc pages.
- Fix: Replace with a link to stable CloudFormation developer guide page
- Delegate: manual

### 9.0 Observability

**9.7** `rlhf_tracker.py` configures both a `StreamHandler` and a `FileHandler` via `basicConfig()`.
The `basicConfig()` pattern means log level is global and cannot be configured per-module.
- Fix: Replace `basicConfig()` with `getLogger(__name__)` + handlers added explicitly
- Delegate: code-cleanup-agent

### 10.0 Config & Deps

**10.5** `global-requirements.txt` and `global-node-packages.json` exist at root with no documentation
on who reads them or when they are applied. They duplicate information in `pyproject.toml` and
individual `package.json` files in subdirectories.
- Fix: Document purpose clearly in `README.md` or delete if superseded by `install-global-tools.sh`
- Delegate: manual

---

## Execution Plan

| Phase | Scope | Items | Delegate |
|-------|-------|-------|----------|
| 1 | Committed secrets / personal config | 2.1, 2.2, 2.3, 2.4, 2.5, 10.1 | code-cleanup-agent |
| 2 | Git hygiene (.gitignore, rm --cached) | 2.6, 1.3 (dist/venv) | manual |
| 3 | Config / deps consolidation | 10.2, 10.3, 10.4, 3.1, 3.2 | code-cleanup-agent |
| 4 | Observability (logging, error tracking) | 9.1, 9.3, 9.4, 9.5, 9.6, 9.7 | code-cleanup-agent |
| 5 | Information architecture (root clutter) | 1.1, 1.2, 4.2, 4.7, 4.8 | information-architecture-agent |
| 6 | Code decomposition (long files) | 4.1, 4.3, 4.4, 4.5, 4.6 | code-cleanup-agent |
| 7 | Models & types | 5.1, 5.2, 5.3, 5.4 | domain-modeling-specialist |
| 8 | Security & auth | 6.1, 7.1, 9.2 | cognito-expert-agent + manual |
| 9 | Docs cleanup | 8.1, 8.2, 8.3, 8.4, 10.5 | manual |

**Approve?** [Y] Execute all phases in order  [P] Execute specific phase  [R] Revise plan  [S] Save plan only (already saved)
