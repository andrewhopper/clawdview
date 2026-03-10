---
description: Run agentic Ollama with MCP tools (filesystem, git, fetch)
---

Run a task using Ollama with MCP tool access. The local model can read/write files, run git commands, and fetch URLs.

**Task:** $ARGUMENTS

Execute using the ollama-bridge wrapper:

```bash
cd /home/user/protoflow/hmode/shared/tools/ollama-bridge
python3 ollama_bridge.py run "$ARGUMENTS"
```

If the bridge isn't running, start it first:
```bash
python3 ollama_bridge.py serve -b  # background
```

Common tasks:
- "List files in src/ and explain what each does"
- "Check git status and summarize recent changes"
- "Find all TODO comments in Python files"
- "Read package.json and list dependencies"
