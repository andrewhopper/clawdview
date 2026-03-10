---
name: check-url
description: URL health check with content validation - verifies HTTP status and checks for error patterns
version: 1.0.0
---

# URL Health Check Skill

**Check if URLs are healthy and their content is error-free.**

## Quick Usage

```bash
# Basic check
/check-url http://localhost:3456/

# Strict mode (recommended) - catches errors, build failures, stack traces
/check-url http://localhost:3456/ --strict

# Check with custom forbidden patterns
/check-url http://localhost:5173/ --forbidden "error,failed,404"

# Check with required patterns
/check-url http://api.example.com/health --required "status,ok"

# JSON output
/check-url http://localhost:3456/ --json
```

## Tool Location

`hmode/shared/tools/check_url.py`

## Execution

When this skill is invoked:

1. **Parse arguments** - Extract URL and options from user input
2. **Run check_url.py** - Execute the health check script
3. **Report results** - Show pass/fail with details

### Basic Check

```bash
uv run hmode/shared/tools/check_url.py http://localhost:3456/
```

### With Forbidden Patterns

Check that response doesn't contain error indicators:

```bash
uv run hmode/shared/tools/check_url.py http://localhost:3456/ \
  --forbidden "error,failed,cannot find,404,500"
```

### With Required Patterns

Check that response contains expected content:

```bash
uv run hmode/shared/tools/check_url.py http://localhost:5173/ \
  --required "Portfolio,Projects"
```

### Combined Check

```bash
uv run hmode/shared/tools/check_url.py http://localhost:3456/ \
  --forbidden "error,failed" \
  --required "Dashboard,Status" \
  --timeout 10
```

## Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--strict` | `-S` | Use default forbidden patterns (recommended) | false |
| `--forbidden` | `-f` | Comma-separated patterns that should NOT appear | none |
| `--required` | `-r` | Comma-separated patterns that MUST appear | none |
| `--timeout` | `-t` | Request timeout in seconds | 5 |
| `--status` | `-s` | Expected HTTP status code | 200 |
| `--json` | `-j` | Output results as JSON | false |
| `--verbose` | `-v` | Show response details | false |

## Strict Mode Patterns

`--strict` checks for 30+ error patterns including:

**General errors:** error, failed, exception

**HTTP errors:** 404, 500, 502, 503

**Vite/Build errors:**
- `plugin:vite`, `Cannot find module`, `Module not found`
- `Require stack`, `fix the code to dismiss`, `hmr.overlay`
- `postcss`, `webpack`, `esbuild`, `rollup`

**JS errors:**
- `SyntaxError`, `TypeError`, `ReferenceError`
- `undefined is not`, `is not defined`, `is not a function`
- `Uncaught Error`, React errors

**Stack traces:** `at Function`, `at Module`, `at Object`, `node_modules`

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Health check passed |
| 1 | Health check failed (bad status, pattern match) |
| 2 | Connection error or timeout |

## Output Formats

### Standard Output

```
✅ http://localhost:3456/
   HTTP 200 OK

❌ http://localhost:5173/
   Found forbidden pattern: 'error'
```

### JSON Output

```json
{
  "url": "http://localhost:3456/",
  "healthy": true,
  "status_code": 200,
  "message": "HTTP 200 OK",
  "timestamp": "2025-02-23T10:30:00.000000",
  "details": {
    "content_type": "text/html",
    "forbidden_checked": 5
  }
}
```

## Common Use Cases

### Check Overwatch Dashboard

```bash
uv run hmode/shared/tools/check_url.py http://127.0.0.1:3456/ \
  --forbidden "error,failed,cannot find,404,500,undefined"
```

### Check Portfolio App

```bash
uv run hmode/shared/tools/check_url.py http://localhost:5173/ \
  --forbidden "error,failed" \
  --required "Portfolio"
```

### Check API Health Endpoint

```bash
uv run hmode/shared/tools/check_url.py http://localhost:5557/health \
  --required "status,healthy" \
  --timeout 3
```

### Batch Check Multiple URLs

```bash
for url in "http://localhost:3456/" "http://localhost:5173/" "http://localhost:5557/health"; do
  uv run hmode/shared/tools/check_url.py "$url" --forbidden "error,failed"
done
```

## Integration with Overwatch

The `overwatch-manager` uses the same health check logic. Configure in `config/overwatch-services.yaml`:

```yaml
ui_dashboard:
  health_check:
    type: "http"
    url: "http://127.0.0.1:3456/"
    timeout: 5
    expected: 200
    forbidden_patterns:
      - "error"
      - "failed"
      - "cannot find"
```

## Troubleshooting

### Connection Refused

```
❌ http://localhost:3456/
   Connection failed: Connection refused
```

**Fix**: Service not running. Start it with `bin/overwatch-manager start ui_dashboard`

### Timeout

```
❌ http://localhost:3456/
   Timeout after 5s
```

**Fix**: Increase timeout with `--timeout 15` or check if service is overloaded

### Found Forbidden Pattern

```
❌ http://localhost:5173/
   Found forbidden pattern: 'error'
```

**Fix**: Check browser console for JavaScript errors, review server logs

## Notes

- All pattern matching is case-insensitive
- Patterns are simple substring matches (not regex)
- Response body is fully loaded for pattern checks
- Works with any HTTP/HTTPS URL
