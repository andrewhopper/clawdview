---
description: Summarize a directory using local Ollama model
---

Summarize the directory using the local Ollama model. Run:

```bash
python3 /home/user/protoflow/hmode/shared/tools/dir_summarizer.py "$ARGUMENTS"
```

If no directory specified, use the current working directory.

The tool:
1. Prioritizes READMEs and manifest files (package.json, pyproject.toml, etc.)
2. Excludes node_modules, __pycache__, .git, etc.
3. Extracts code skeletons (imports, class/function defs) for large files
4. Stays within context limits (~15k chars)

Options:
- `-m MODEL` - Use different Ollama model (default: llama3.2)
- `-o FILE` - Save summary to file
- `--context-only` - Print gathered context without calling Ollama
