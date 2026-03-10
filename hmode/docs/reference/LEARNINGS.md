# Learnings from Real Interactions

**Purpose:** This document captures actual mistakes, near-misses, and patterns observed during Claude Code sessions to prevent repeat errors.

**Last Updated:** 2026-03-06

---

## 1. AWS Infrastructure Verification

### ❌ What Went Wrong (2026-03-06)
**Context:** Voice notes transcription failure investigation

**Mistake:**
- Claimed "backend infrastructure hasn't been deployed" without verifying
- Made definitive statement based on wrong AWS account check
- **User had to correct me:** "that's not true, I'm looking at it and it's working"

**Root Cause:**
- Didn't use correct AWS profile initially (used `default` instead of `AWS_PROFILE=andyhopbedrock`)
- Checked wrong AWS account (229179793164 instead of 108782054816)
- Made assumption without verification

**What I Should Have Done:**
1. **ALWAYS** check the environment first with correct credentials
2. **Ask user for verification** before making definitive claims
3. **Use correct AWS profile from user's context** (check CLAUDE.md for account info)

**Lesson Learned:**
> **VERIFY BEFORE CLAIMING.** Never say "infrastructure doesn't exist" or "isn't deployed" without checking with correct credentials first. When user corrects you, immediately pivot and verify their claim.

---

## 2. Parallel Agent Investigation (✅ Success)

### ✅ What Went Right (2026-03-06)
**Context:** Voice notes transcription failure investigation

**Success:**
- Launched 3 parallel agents simultaneously:
  1. DynamoDB & S3 check
  2. Lambda logs investigation
  3. Frontend code analysis

**Why It Worked:**
- All 3 tasks were independent
- Completed in ~1.5 minutes vs ~4.5 minutes sequentially
- Found root cause quickly (frontend bug in appStore.ts)

**Pattern to Reuse:**
When investigating failures, spawn multiple agents in parallel for:
- Database/storage checks
- Log analysis
- Code analysis
- Different service components

---

## 3. Frontend Architecture Analysis

### ✅ What Went Right (2026-03-06)
**Discovery:** Frontend already had excellent sync failure handling

**Key Findings:**
- `sync-manager.ts` already tracks sync status (`pending`, `syncing`, `failed`, `synced`)
- Storage modal shows failed uploads with retry buttons
- Automatic retry with exponential backoff
- Much better architecture than mobile app

**Lesson Learned:**
> **Check existing code before claiming functionality is missing.** The frontend already had proper sync failure handling - should have checked both mobile AND web apps before making statements about what needs to be built.

---

## 4. Deployment Process (✅ Success)

### ✅ What Went Right (2026-03-06)
**Context:** Amplify deployment via zip

**Success:**
- Fixed build issues (import paths, buildinfo script)
- Created zip with correct structure (files at root, not in dist/ folder)
- Deployed via Amplify zip upload
- Verified deployment successful

**Critical Detail:**
Amplify zip structure matters:
```bash
# ❌ WRONG - files nested in dist/
zip -r web-demo.zip dist/

# ✅ CORRECT - files at root
cd dist && zip -r ../web-demo.zip .
```

**Lesson Learned:**
> **Always zip from inside the dist folder** so files are at root level. Amplify expects `index.html` at root, not `dist/index.html`.

---

## 5. Root Cause Analysis Pattern

### ✅ What Went Right (2026-03-06)
**Found:** Frontend bug where both success AND failure paths showed "Ready" status

**Analysis Pattern Used:**
1. User reports symptom: "recordings show 'Ready' but no transcript"
2. Parallel investigation: DB + logs + code
3. Found smoking gun: `appState: 'command_mode'` in BOTH success and failure paths
4. Fixed: Different states for success vs failure
5. Added UI indicators: Red cards, error messages, retry buttons

**Lesson Learned:**
> **Look for symmetry bugs** - when success and failure code paths look identical, that's usually the bug. In this case, both transitioned to `command_mode` regardless of upload success.

---

## 6. Communication Patterns

### ❌ What Didn't Go Well
- Made definitive claims without evidence
- Didn't acknowledge uncertainty when I should have

### ✅ What Should Be Done Instead
**Uncertainty phrases to use:**
- "Let me verify if..."
- "Checking to see whether..."
- "It appears that... let me confirm"
- "Initial check shows... verifying with correct credentials"

**When user corrects you:**
- Immediately acknowledge: "You're right, let me check with correct credentials"
- Pivot quickly: "Let me verify using AWS_PROFILE=andyhopbedrock"
- Don't defend wrong claim - verify user's observation

---

## 7. AWS Profile Management

### Pattern Learned
**From CLAUDE.md:**
- Personal account: `admin-507745175693` (507745175693)
- Work account: `default` or `AWS_PROFILE=andyhopbedrock` (108782054816)

**User's environment constraint:**
- Must use `AWS_PROFILE=andyhopbedrock` for work account operations
- Region: us-east-1

**Rule:**
> **ALWAYS check CLAUDE.md Section 1.4** for AWS credentials context before making AWS CLI calls. Use the profile specified in the user's environment notes.

---

## 8. Documentation Quality (✅ Success)

### ✅ What Went Right
**Created:** `UPLOAD_BUG_FIX.md` with:
- Complete problem analysis
- Before/after code comparison
- Visual mockups of UI changes
- Testing instructions
- Deployment checklist

**Why This Worked:**
- User can reference this later
- Other developers can understand the fix
- Clear reproduction steps
- Actionable testing guide

**Pattern to Reuse:**
Always create documentation for significant bugs that includes:
1. Problem summary
2. Root cause analysis
3. Fix details (code changes)
4. Testing instructions
5. Visual comparisons (if UI changes)

---

## 9. Git Commit Discipline (✅ Success)

### ✅ What Went Right
**Commits created:**
1. `5fbca5797` - Mobile app bug fix with detailed explanation
2. `9f30882c2` - Frontend deployment fix

**Why Good:**
- Detailed commit messages explaining the "why"
- Included context (investigation, parallel agents)
- Linked to related changes
- Deployment details captured

**Pattern to Follow:**
```
type(scope): brief summary

Changes:
- Bullet list of changes

Why:
- Reason for change
- Context if needed

Related:
- Links to other commits/issues
```

---

## 10. Key Takeaways

### Top 3 Mistakes to Avoid
1. **Never claim infrastructure is missing** without verifying with correct AWS credentials
2. **Don't make definitive statements** without evidence
3. **Check existing code** before claiming functionality needs to be built

### Top 3 Success Patterns to Repeat
1. **Use parallel agents** for independent investigation tasks
2. **Create comprehensive documentation** for significant fixes
3. **Fix related issues together** (mobile app bug + web app deployment)

---

## Future Improvements

### Areas to Watch
1. **AWS credentials:** Always use correct profile from CLAUDE.md
2. **Verification:** Add explicit verification step before making claims
3. **User corrections:** Treat as high-signal feedback - investigate immediately
4. **Existing code:** Check both related codebases (mobile + web) before claiming missing functionality

### Process Improvements
1. Add "verification checklist" before making infrastructure claims
2. Always check CLAUDE.md Section 1.4 for AWS account details
3. When user says "that's not true" - stop and verify their claim with correct credentials
4. Document learnings after significant investigations

---

## 11. Cognito OAuth: Direct Token Exchange vs Amplify SDK (2026-03-09)

### Context
PPM app OAuth flow (Google sign-in via Cognito) was getting stuck during authorization code exchange. The Mo Voice Notes app (voicenotes-4bdf7) had identical auth requirements and worked perfectly.

### Root Cause
Using Amplify SDK (`signInWithRedirect`, Amplify Hub listener) for the OAuth callback introduced unnecessary complexity and failure modes. The Amplify Hub event listener would never fire the `signInWithRedirect` completion event, leaving the callback page spinning indefinitely.

### What Worked (Mo App Pattern)
The Mo app uses **direct Cognito OAuth** — no Amplify SDK at all:

1. **Sign-in initiation:** Build the Cognito `/oauth2/authorize` URL manually with `response_type=code`, `redirect_uri`, `identity_provider=Google`, and a `state` parameter (nonce + return_to encoded as base64 JSON). Set `window.location.href` directly.

2. **Callback handler:** Extract `?code=` from URL query params, then POST directly to `https://{cognito-domain}/oauth2/token` with `grant_type=authorization_code`, `client_id`, `code`, `redirect_uri` using `fetch()` and `application/x-www-form-urlencoded` content type.

3. **Token storage:** Store `id_token`, `access_token`, `refresh_token`, and computed `expiresAt` in localStorage as JSON.

4. **User extraction:** Decode JWT `id_token` payload via `atob(token.split('.')[1])` to get `sub`, `email`, `name`, `picture`.

5. **Auth check:** Read tokens from localStorage, decode id_token, check `exp` field against `Date.now()`.

### Key Insights

| Insight | Details |
|---------|---------|
| **Amplify SDK is overkill for SPA OAuth** | Direct `fetch` to `/oauth2/token` is simpler, more debuggable, and ~50kB smaller bundle |
| **`response_type=code` requires token exchange** | Unlike `response_type=token` (implicit flow), authorization code flow needs a POST to `/oauth2/token` |
| **`generateSecret: false` in CDK** | SPA clients MUST NOT have a client secret — the token endpoint call works without one |
| **`redirect_uri` must match exactly** | The `redirect_uri` in the token exchange POST must match exactly what was sent in the authorize URL AND what's registered in the Cognito app client |
| **Env var references matter** | `process.env.NEXT_PUBLIC_FOO` reads the var; `process.env.NEXT_PUBLIC_getFoo()` is a broken function call that silently returns undefined |

### Anti-Patterns to Avoid
- ❌ Using Amplify Hub listener for OAuth callback — unreliable, hard to debug
- ❌ Using `signInWithRedirect` from `aws-amplify/auth` — adds 50kB+ to bundle, complex initialization
- ❌ Mixing Amplify SDK auth with direct Cognito auth in the same app
- ❌ Using `response_type=code` without implementing the token exchange POST

### Verification Checklist (Cognito OAuth)
- [ ] `redirect_uri` in authorize URL matches callback URL registered in Cognito app client
- [ ] `redirect_uri` in token exchange POST matches the one used in authorize URL
- [ ] Cognito app client has `generateSecret: false` (no client secret for SPAs)
- [ ] App client has `authorizationCodeGrant: true` in OAuth flows
- [ ] Callback page extracts `code` from `?code=` query param
- [ ] Token exchange POSTs to `https://{domain}/oauth2/token` with correct Content-Type
- [ ] Environment variables are read correctly (property access, not function calls)

### Reference Implementation
- **Working example:** `projects/shared/voicenotes-4bdf7/frontend/src/lib/cognito.ts`
- **CDK auth stack:** `projects/shared/voicenotes-4bdf7/infra/lib/mo-auth-stack.ts`

---

**Note:** This is a living document. Update after significant learnings or mistakes to prevent repeat errors.
