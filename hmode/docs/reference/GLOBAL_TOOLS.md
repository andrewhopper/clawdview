## 🌐 GLOBAL TOOLS

**Gitleaks:** Required for security - secret scanning and leak prevention
- Scans code for accidentally committed secrets (API keys, credentials, tokens)
- Pre-commit hook prevents secrets from entering git history
- CI/CD integration via GitHub Actions workflow
- Detects: AWS keys, API keys (OpenAI, Anthropic, GitHub), private keys, database credentials
- Configuration: `.gitleaks.toml` (custom rules and allowlist)
- Installation:
  - macOS: `brew install gitleaks`
  - Linux: Download from https://github.com/gitleaks/gitleaks/releases
  - Windows: Download binary or use WSL
- Pre-commit hook: `.git/hooks/pre-commit` (automatically blocks commits with secrets)
- Manual scan: `gitleaks detect --source . --verbose`
- **Critical security tool** - prevents credential leaks and security incidents

**Playwright:** Installed globally, available for testing and validating websites
- Test web applications (local or remote URLs)
- Validate website functionality, performance, accessibility
- Capture screenshots and perform visual regression testing
- Automate user workflows and interactions
- Browse sites that may be blocked by browser extensions (e.g., LinkedIn)
- Can be used outside SDLC for ad-hoc website testing/validation

