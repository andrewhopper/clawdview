<!-- File UUID: d8e4f2a1-3b7c-4d9e-8f5a-6c2b1e9d7a3f -->
# shared/tools Vibe Code Cleanup — Progress

**Started:** 2026-03-01
**Full plan:** `shared/tools/CLEANUP_PLAN.md`

## Completed Phases

### Phase 1: Strip personal configs (6 findings, ALL FIXED)
- `infra-import.py` — Removed hardcoded AWS profile `admin-507745175693` (3 locations: constructor, shell template, argparse default). Now uses `$AWS_PROFILE` env var.
- `sparse-checkout/init-env.sh` — Removed hardcoded account ID `108782054816`. Now requires `$AWS_ACCOUNT_ID` env var (fail-fast).
- `generate-enhanced-grid.py` — Removed hardcoded profile + absolute path `/Users/andyhop/dev/hopperlabs`. Now uses `$AWS_PROFILE` + `Path(__file__)`.
- `s3backup-config.yaml` — Replaced account ID and bucket name with `${AWS_ACCOUNT_ID}` / `${S3_BACKUP_BUCKET}` placeholders.
- `s3backup-notifications/infra/app.py` — Removed fallback account ID `507745175693` and bucket name from CDK env.
- `audit-hardcoded-infra.py` — Removed `108782054816` from ALLOWLIST + replaced hardcoded `/home/user/hopperlabs` default path with dynamic detection.
- `mcp-cli-wrappers/config.py` — Replaced hardcoded email `andyhop+bedrock@amazon.com` with empty default (set via `MCP_CLI_ISENGARD_EMAIL` env var). Updated test assertion.

### Phase 2: Git hygiene (VERIFIED CLEAN)
- Audit overstated: `dist/`, `.venv/`, `node_modules/` were NOT tracked in git (subdirs already have proper `.gitignore`).
- Created `shared/tools/.gitignore` for defense-in-depth (Python, Node, OS, IDE, logs).

### Phase 3: Config/deps consolidation (DONE)
- Audit overstated: Root scripts only import `anthropic`, `boto3`, `pillow`, `pyyaml` — all declared in `pyproject.toml`.
- Merged `requirements.txt` tree-sitter deps into `pyproject.toml` as `[ast]` optional group.
- Replaced `requirements.txt` with pointer to `pyproject.toml` install commands.
- Ollama `http://localhost` is standard for local-only service — not a real security issue.

### Phase 4: Observability (FOUNDATION LAID)
- Created `shared/tools/_logger.py` — shared structured logger (JSON file + console, 10MB rotation, env var config).
- Added `logs/` to `.gitignore`.
- NOT done: Migrating 25+ scripts from `print()` to logger (incremental future work — each script adopts as it's touched).

### Phase 5: Information Architecture (DONE)
- Created `shared/tools/INDEX.md` — categorized reference covering all 64 root files and 21 subdirectories across 12 groups.
- Physical file moves rejected (would break references across monorepo — CLAUDE.md, hooks, commands all reference current paths).

### Phase 6: Code decomposition (PARTIAL — large files deferred)
- Fixed hardcoded `/Users/andyhop/Desktop/` paths in 3 claude-exporter scripts (now use `$CLAUDE_HAR_FILE`/`$CLAUDE_EXPORT_DIR` + `Path.home()`).
- Fixed hardcoded `/Users/andyhop/dev/lab` in `project-audit/audit.py` (now uses `Path.home() / "dev/hopperlabs"`).
- Updated `track-errors.md` command to reference `rlhf_tracker.py` (primary) instead of duplicate `rlhf-reward-punishment-tracker.py`.
- Added missing `os` and `Path` imports to `analyze_api_structure.py`.
- NOT done: Decomposing 29 files >300 lines (too invasive — largest are `brownfield_audit.py` 1,512 lines, `templates.py` 1,271 lines, `post-deploy-validate.py` 1,017 lines).

### Phase 7: Type models (DONE)
- `validate-cdk-deployment.ts` — Replaced all 6 `any` types: added `CfnTemplate`, `CfnResource`, `CfnParameter` interfaces; added `isAwsError()` type guard; changed `catch (err: any)` → `catch (err: unknown)` with proper narrowing; removed `paramConfig as any` and `resource as any` casts.
- `acceptance_criteria.py` — Added `Criterion` TypedDict with `NotRequired` fields; updated all 8 method return types from `List[Dict[str, Any]]` to `List[Criterion]`.
- `proposal-scorer/proposal_scorer.py` — Skipped: dataclasses with `to_dict()`/`from_dict()` work correctly, converting to Pydantic would add unnecessary dependency.

### Phase 8: Security and auth (DONE)
- `s3backup-semantic-search/frontend/src/lib/amplify-config.ts` — SSR fallback now reads `NEXT_PUBLIC_APP_URL` env var instead of hardcoded `http://localhost:3000`.
- `auth-e2e-tester/src/config.ts` — Extracted `DEFAULT_COGNITO_DOMAIN = 'auth.b.lfg.new'` constant; replaced 3 duplicate string literals.

### Phase 9: Docs cleanup (DONE)
- `README-s3backup.md` — Replaced hardcoded account ID `507745175693` and bucket name with `${AWS_ACCOUNT_ID}`/`${S3_BACKUP_BUCKET}` env var placeholders (2 locations).
- `mcp-cli-wrappers/README.md` — Replaced stale `https://quip-amazon.com/xxxxx` internal URL with generic placeholder.
- `README-INTEGRITY-CHECK.md` — Reviewed, no issues (proper tool documentation at correct location).

## Remaining Work (Future Sessions)

- **Code decomposition**: 29 files >300 lines need splitting (brownfield_audit.py, templates.py, post-deploy-validate.py, etc.)
- **Logger migration**: 25+ scripts still use `print()` — adopt `_logger.py` incrementally as files are touched
- **Verbose docs**: Several READMEs could be condensed

## Files Modified (All Sessions)

```
# Phase 1 (personal configs)
shared/tools/infra-import.py
shared/tools/sparse-checkout/init-env.sh
shared/tools/generate-enhanced-grid.py
shared/tools/s3backup-config.yaml
shared/tools/s3backup-notifications/infra/app.py
shared/tools/audit-hardcoded-infra.py
shared/tools/mcp-cli-wrappers/mcp_cli_wrappers/config.py
shared/tools/mcp-cli-wrappers/tests/test_config.py

# Phase 3 (deps consolidation)
shared/tools/pyproject.toml
shared/tools/requirements.txt

# Phase 6 (code decomposition)
shared/tools/claude-exporter/scripts/data-download/extract_claude_data.py
shared/tools/claude-exporter/scripts/data-download/analyze_api_structure.py
shared/tools/claude-exporter/scripts/data-download/download_all_sessions.py
shared/tools/project-audit/audit.py
.claude/commands/track-errors.md

# Phase 7 (type models)
shared/tools/validate-cdk-deployment.ts
shared/tools/acceptance_criteria.py

# Phase 8 (security/auth)
shared/tools/s3backup-semantic-search/frontend/src/lib/amplify-config.ts
shared/tools/auth-e2e-tester/src/config.ts

# Phase 9 (docs)
shared/tools/README-s3backup.md
shared/tools/mcp-cli-wrappers/README.md
```

## Files Created (All Sessions)

```
shared/tools/.gitignore
shared/tools/_logger.py
shared/tools/INDEX.md
shared/tools/CLEANUP_PLAN.md
shared/tools/CLEANUP_PROGRESS.md
```
