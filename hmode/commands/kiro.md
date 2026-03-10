---
version: 1.0.0
last_updated: 2025-12-09
description: Run Kiro CLI via kiro-pytool Python wrapper
---

# Kiro CLI Wrapper

Run Kiro CLI commands via the Python wrapper for non-interactive execution.

## Parameter Handling

**Provided arguments**:
- prompt: {prompt} (required) - The prompt to send to Kiro CLI
- format: {format} (default: json) - Output format (json or raw)
- timeout: {timeout} (default: 60) - Timeout in seconds
- isolated: {isolated} (default: false) - Run in isolated temp directory
- model: {model} (optional) - Model ID to use

## Overview

This command runs Kiro CLI through the kiro-pytool wrapper at `/Users/andyhop/dev/lab/bin/kiro-pytool`.

The wrapper provides:
- Async execution with streaming output
- JSON or raw output formats
- Autonomous execution mode (bypass permissions)
- Isolated directory support
- Model selection

## Instructions

### Basic Usage

Run a simple prompt:

```bash
echo "{prompt}" | /Users/andyhop/dev/lab/bin/kiro-pytool --async-mode --stdin-prompt --format {format} --timeout {timeout}
```

### With Isolation

Run in an isolated temp directory:

```bash
echo "{prompt}" | /Users/andyhop/dev/lab/bin/kiro-pytool --async-mode --stdin-prompt --format {format} --timeout {timeout} --isolated
```

### With Model Selection

Specify a model:

```bash
echo "{prompt}" | /Users/andyhop/dev/lab/bin/kiro-pytool --async-mode --stdin-prompt --format {format} --timeout {timeout} --model {model}
```

## Output Format

**JSON format** (default):
```json
{
  "agent_name": "main",
  "success": true,
  "exit_code": 0,
  "stdout": "...",
  "stderr": "...",
  "work_dir": "/path/to/work/dir",
  "cost": null,
  "event_count": 1,
  "error": null
}
```

**Raw format**:
Returns the raw stdout from Kiro CLI with stderr printed to stderr.

## Usage Examples

**Ask a question:**
```bash
/kiro prompt="What is 2+2?"
```

**Check available tools:**
```bash
/kiro prompt="what mcp tools do you have?"
```

**Run with custom timeout:**
```bash
/kiro prompt="analyze this codebase" timeout=300
```

**Run in isolated mode:**
```bash
/kiro prompt="create a test file" isolated=true
```

**Get raw output:**
```bash
/kiro prompt="show my calendar" format=raw
```

## Notes

- The wrapper runs in async mode with streaming output by default
- Bypass permissions are enabled for autonomous execution
- The wrapper uses the .venv Python if available, otherwise system Python
- Timeout defaults to 60 seconds but can be increased for longer operations
