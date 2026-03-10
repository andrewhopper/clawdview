# Python Logging Standards

**Last Updated:** 2026-01-16
**Guardrail:** `.guardrails/ai-steering/rules/logging.json`

---

## 1.0 OVERVIEW

All Python scripts and tools MUST implement logging for debugging, audit trails, and operational visibility.

---

## 2.0 WHEN LOGGING IS REQUIRED

### Required For:
- ✅ Scripts in `shared/tools/`
- ✅ Utilities in `bin/`
- ✅ Standalone Python tools
- ✅ Long-running services
- ✅ Background processes
- ✅ Deployment scripts
- ✅ Data processing scripts

### Exceptions:
- ❌ Simple one-liners (<10 lines)
- ❌ Test files (use test output instead)
- ❌ Interactive notebooks (Jupyter)

---

## 3.0 LOG LOCATIONS

### Monorepo Tools
```
logs/tools/<script_name>.log
```

**Example:**
```python
# shared/tools/rlhf_tracker.py
LOG_FILE = REPO_ROOT / "logs" / "tools" / "rlhf_tracker.log"
```

### Project Scripts
```
<project_root>/logs/<script_name>.log
```

**Example:**
```python
# projects/my-app/scripts/deploy.py
LOG_FILE = Path.cwd() / "logs" / "deployment.log"
```

### Background Services
```
logs/<service_name>/<date>.log
```

**Example:**
```python
# bin/overwatch/file_watcher.py
LOG_FILE = REPO_ROOT / "logs" / "overwatch" / f"file_watcher_{datetime.now():%Y%m%d}.log"
```

---

## 4.0 STANDARD IMPLEMENTATION

### Minimal Template
```python
import logging
from pathlib import Path

# Setup logging
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs" / "tools"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "my_script.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Also output to console
    ]
)
logger = logging.getLogger(__name__)
```

### With Rotation (Long-Running Services)
```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "service.log"

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
```

---

## 5.0 LOG LEVELS

### DEBUG
**Use for:** Detailed diagnostic information
**Examples:**
- Function entry/exit
- Variable values
- Loop iterations

```python
logger.debug("Processing item %d: %s", idx, item)
```

### INFO
**Use for:** General informational messages
**Examples:**
- Script started/completed
- File processed
- Operation succeeded

```python
logger.info("Processing file: %s", filepath)
logger.info("Uploaded to S3: %s", s3_url)
```

### WARNING
**Use for:** Something unexpected but handled
**Examples:**
- Deprecated usage
- Fallback applied
- Missing optional config

```python
logger.warning("Config not found, using defaults")
logger.warning("Deprecated API used: %s", old_api)
```

### ERROR
**Use for:** Error occurred but script continues
**Examples:**
- File not found (with fallback)
- API call failed (with retry)
- Validation error (skipped)

```python
logger.error("Failed to upload %s: %s", filename, error)
logger.error("Validation failed for record %d", record_id)
```

### CRITICAL
**Use for:** Severe error, script cannot continue
**Examples:**
- Config missing (required)
- Auth failed
- Database connection lost

```python
logger.critical("Database connection failed: %s", error)
logger.critical("Required config missing: %s", config_key)
```

---

## 6.0 LOG FORMAT STANDARDS

### Standard Format (Recommended)
```python
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

**Output:**
```
2026-01-16 10:25:25,851 - __main__ - INFO - Command invoked: reward
```

### Minimal Format (Simple Scripts)
```python
format='%(asctime)s - %(levelname)s - %(message)s'
```

**Output:**
```
2026-01-16 10:25:25,851 - INFO - Command invoked: reward
```

### Extended Format (Complex Services)
```python
format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
```

**Output:**
```
2026-01-16 10:25:25,851 - __main__ - INFO - [rlhf_tracker.py:220] - Command invoked: reward
```

---

## 7.0 BEST PRACTICES

### DO:
- ✅ Create logs directory if it doesn't exist
- ✅ Use script/service name as log filename
- ✅ Include `.log` extension
- ✅ Log to both file and console (for debugging)
- ✅ Use structured log messages (with variables)
- ✅ Log at appropriate levels
- ✅ Include context in log messages

### DON'T:
- ❌ Log to current directory
- ❌ Hardcode log paths
- ❌ Use `print()` instead of logging
- ❌ Log sensitive data (passwords, keys, tokens)
- ❌ Over-log (DEBUG in production)
- ❌ Under-log (missing error context)

### Structured Logging Example
```python
# ✅ Good - Structured with variables
logger.info("User %s uploaded file %s (%d bytes)", user_id, filename, size)

# ❌ Bad - String concatenation
logger.info(f"User {user_id} uploaded file {filename} ({size} bytes)")
```

**Why?** Variable substitution is more efficient and enables log parsing.

---

## 8.0 REAL-WORLD EXAMPLES

### Example 1: RLHF Tracker
**File:** `shared/tools/rlhf_tracker.py`

```python
# Setup logging (LOG-001, LOG-002, LOG-003)
LOG_DIR = REPO_ROOT / "logs" / "tools"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "rlhf_tracker.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Usage throughout the script
logger.info("Command invoked: %s", args.command)
logger.info("Logging punishment signal")
logger.debug("Categories: %s", category)
logger.info("Punishment logged: %s", filepath.name)
logger.warning("Signal directory does not exist: %s", target_dir)
```

**Log Output:**
```
2026-01-16 10:25:25,851 - __main__ - INFO - Command invoked: reward
2026-01-16 10:25:25,881 - __main__ - INFO - Logging reward signal
2026-01-16 10:25:25,914 - __main__ - INFO - Reward logged: NICE-20260116-0002_5a35863f.yaml
```

### Example 2: Deployment Script
**File:** `projects/my-app/scripts/deploy.py`

```python
import logging
from pathlib import Path

# Project-level logging
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "deployment.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE)]
)
logger = logging.getLogger(__name__)

# Deployment steps
logger.info("Starting deployment to %s", environment)
logger.info("Building Docker image: %s", image_tag)
logger.info("Pushing to ECR: %s", ecr_url)
logger.info("Deploying to ECS cluster: %s", cluster_name)
logger.info("Deployment complete: %s", service_url)
```

### Example 3: Background Service
**File:** `bin/overwatch/file_watcher.py`

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs" / "overwatch"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "file_watcher.log"

# Rotating handler for long-running service
handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Service operations
logger.info("File watcher started, watching: %s", watch_dir)
logger.info("Detected change: %s", filepath)
logger.warning("File already being processed: %s", filepath)
logger.error("Failed to process file %s: %s", filepath, error)
```

---

## 9.0 CHECKLIST

Before committing a Python script:

- [ ] Logging configured (imports, basicConfig)
- [ ] Log file in `logs/` directory
- [ ] Log directory created if not exists
- [ ] Log file named after script
- [ ] Standard format used (asctime, levelname, message)
- [ ] Appropriate log levels used
- [ ] Structured log messages (with variables)
- [ ] No sensitive data logged
- [ ] Both file and console handlers (for tools)
- [ ] Rotation configured (for services)

---

## 10.0 GUARDRAIL ENFORCEMENT

**Rule ID:** LOG-001, LOG-002, LOG-003, LOG-004, LOG-005
**Severity:** Error (LOG-001, LOG-002), Warning (LOG-003, LOG-004), Info (LOG-005)
**Location:** `.guardrails/ai-steering/rules/logging.json`

**Validation:**
```bash
# Check if script has logging
grep -l "import logging" shared/tools/*.py

# Verify log files are in logs/
find logs/ -name "*.log"
```

---

## 11.0 RELATED DOCUMENTATION

- **Guardrail Definition:** `.guardrails/ai-steering/rules/logging.json`
- **Example Implementation:** `shared/tools/rlhf_tracker.py`
- **Python Logging Docs:** https://docs.python.org/3/library/logging.html
