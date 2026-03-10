## 🔀 SPAWNING CHILD PROCESSES

**Pattern:** Spawn isolated Claude CLI child processes for parallel agent execution

**Reference Implementation:** `prototypes/proto-company-researcher-uiwid-005/orchestrator.py`

### When to Use

**✅ USE when:**
- Running multiple AI agents in parallel
- Need process isolation (prevent settings.local.json conflicts)
- Orchestrating complex multi-agent workflows
- Automating research, data gathering, or synthesis tasks
- Running autonomous agents with different prompts/contexts

**❌ DON'T USE when:**
- Single agent execution (use direct Claude CLI)
- Interactive workflows requiring human input
- Simple sequential tasks (use Task tool instead)

### Core Pattern: Isolated Child Processes

**Critical: Each child process MUST run in isolated temp directory**

```python
import asyncio
import tempfile
from pathlib import Path
import shutil

# 1. Create isolated working directory per agent
agent_work_dir = Path(tempfile.mkdtemp(prefix=f"agent_{agent_name}_"))

# 2. Copy existing context files to agent's work directory
# (e.g., previous research outputs for synthesis agents)
for file in existing_files:
    shutil.copy2(file, agent_work_dir / file.name)

# 3. Spawn Claude CLI process with isolation
process = await asyncio.create_subprocess_exec(
    claude_path,
    '--permission-mode', 'bypassPermissions',  # Autonomous execution
    '--model', 'haiku',                         # or 'sonnet', 'opus'
    '--print',                                  # Print to stdout
    '--output-format', 'stream-json',          # Real-time streaming
    '--verbose',                                # Required for stream-json
    '--include-partial-messages',              # Get updates as they arrive
    stdin=asyncio.subprocess.PIPE,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    cwd=str(agent_work_dir),  # 🚨 CRITICAL: Isolated settings.local.json
)

# 4. Send prompt via STDIN
prompt = load_agent_prompt(agent_name, company_name, domain)
process.stdin.write(prompt.encode('utf-8'))
await process.stdin.drain()
process.stdin.close()

# 5. Stream output in real-time
async for line in process.stdout:
    data = json.loads(line.decode('utf-8').strip())

    if data['type'] == 'assistant':
        # Process assistant messages
        for block in data.get('message', {}).get('content', []):
            if block['type'] == 'text':
                print(f"[{agent_name}] {block['text'][:100]}...")
            elif block['type'] == 'tool_use':
                print(f"[{agent_name}] Using tool: {block['name']}")

    elif data['type'] == 'result':
        # Final result with cost and duration
        cost = data.get('total_cost_usd', 0)
        duration = data.get('duration_api_ms', 0) / 1000
        print(f"[{agent_name}] Completed: {duration:.2f}s, ${cost:.4f}")

# 6. Wait for completion
await process.wait()

# 7. Collect outputs from agent's work directory
for file in agent_work_dir.glob("*.md"):
    if file.name.endswith("_research_raw.md"):
        # Detailed research → raw_research/
        shutil.copy2(file, output_folder / "raw_research" / file.name)
    else:
        # Summaries → root folder
        shutil.copy2(file, output_folder / file.name)

# 8. Cleanup isolated directory
shutil.rmtree(agent_work_dir, ignore_errors=True)
```

### Parallel Execution Pattern

**Run multiple agents concurrently using asyncio.gather**

```python
# Define agent orchestrator
async def run_agent(agent_name, company_name, domain):
    # ... (isolated child process pattern from above)
    return {"agent_name": agent_name, "status": "completed"}

# Phase 1: Data-gathering agents (parallel)
data_agents = ["company", "team", "tech", "products"]
tasks = [run_agent(agent, company_name, domain) for agent in data_agents]
results = await asyncio.gather(*tasks)  # 🔥 All run in parallel

# Phase 2: Synthesis agents (parallel, after data gathering)
synthesis_agents = ["summary", "slidev", "complete_brief"]
tasks = [run_agent(agent, company_name, domain) for agent in synthesis_agents]
synthesis_results = await asyncio.gather(*tasks)
```

**Performance:** 18 agents in 5 minutes (parallel) vs. 9+ minutes (sequential)

### Key Flags and Configuration

| Flag | Purpose | Required? |
|------|---------|-----------|
| `--permission-mode bypassPermissions` | Skip ALL permission prompts (autonomous execution) | ✅ Yes |
| `--output-format stream-json` | Real-time streaming output with metadata | ✅ Yes |
| `--print` | Print assistant responses to stdout | ✅ Yes |
| `--verbose` | Required for stream-json to work | ✅ Yes (with stream-json) |
| `--include-partial-messages` | Get updates as they arrive (not just final) | Recommended |
| `--model haiku/sonnet/opus` | Model selection (aliases, CLI resolves version) | Optional (default: haiku) |
| `cwd=agent_work_dir` | Isolated working directory | 🚨 **CRITICAL** |

### Streaming JSON Output Events

**Event types in stream-json:**

```python
# System initialization
{"type": "system", "subtype": "init", "session_id": "abc123", "model": "claude-haiku-4"}

# Assistant message (text, tool_use)
{"type": "assistant", "message": {"content": [
    {"type": "text", "text": "Analyzing company..."},
    {"type": "tool_use", "name": "WebSearch", "input": {...}}
]}}

# Final result
{"type": "result", "result": "...", "duration_api_ms": 5000, "total_cost_usd": 0.023}
```

### File Organization Strategy

**Organize agent outputs by type:**

```python
# Collect files from agent's work directory
for file in agent_work_dir.glob("*.md"):
    if file.name.endswith("_research_raw.md"):
        dest = output_folder / "raw_research" / file.name
    elif file.suffix == ".md":
        dest = output_folder / file.name  # Summaries at root

    shutil.copy2(file, dest)

# Artifacts
for file in agent_work_dir.glob("*.{drawio,svg,png,pptx}"):
    dest = output_folder / "artifacts" / file.name
    shutil.copy2(file, dest)

# Logs
for file in agent_work_dir.glob("*.log"):
    dest = output_folder / "logs" / file.name
    shutil.copy2(file, dest)
```

**Example structure:**
```
intelligence/company-name_2025-11-15/
├── company.md                   # Summary reports
├── team.md
├── tech.md
├── raw_research/                # Detailed research
│   ├── company_research_raw.md
│   ├── team_research_raw.md
│   └── tech_research_raw.md
├── artifacts/                   # Diagrams, presentations
│   ├── org_chart.drawio
│   ├── product_comparison.svg
│   └── company_presentation.pptx
└── logs/                        # Process logs
    ├── progress.log             # Orchestrator log
    ├── company_full_output.log  # Agent conversation
    └── company_stderr.log       # Error output
```

### Logging Strategy

**Multi-level logging for debugging and monitoring:**

```python
# 1. Orchestrator log (coordination, timing)
self.logger.info(f"[{agent_name}] Starting agent")
self.logger.debug(f"[{agent_name}] Working directory: {agent_work_dir}")
self.logger.info(f"[{agent_name}] Completed in {duration:.2f}s")

# 2. Full agent output (all streaming events)
full_output_log = logs_folder / f"{agent_name}_full_output.log"
full_output_log.write_text('\n'.join(all_output_lines))

# 3. Stderr (error output from Claude CLI process)
if error_output:
    stderr_log = logs_folder / f"{agent_name}_stderr.log"
    stderr_log.write_text(error_output)
```

### Agent Prompt Management

**Use slash command files as canonical source:**

```python
# Agent prompts stored in hmode/commands/
self.agents = {
    "company": "hmode/commands/company-agent.md",
    "team": "hmode/commands/team-agent.md",
    "summary": "hmode/commands/summary-agent.md",
}

def load_agent_prompt(agent_name, company_name, domain):
    """Load and format agent prompt from slash command file"""
    prompt_file = Path(self.agents[agent_name])
    content = prompt_file.read_text()

    # Parse YAML frontmatter (---\nargs:\n...\n---\nPrompt)
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    prompt = frontmatter_match.group(2) if frontmatter_match else content

    # Replace template variables
    prompt = prompt.replace("{company_name}", company_name)
    prompt = prompt.replace("{domain}", domain)

    return prompt
```

**Benefits:**
- Single source of truth for agent prompts
- Same prompts available interactively via slash commands (e.g., `/company-agent "Stripe" "stripe.com"`)
- Easy to version and update

### Context Sharing Between Agents

**Synthesis agents need previous outputs:**

```python
# Before spawning synthesis agent, copy existing reports
if output_folder.exists():
    existing_files = list(output_folder.glob("*.md"))  # Summaries
    existing_files.extend((output_folder / "raw_research").glob("*.md"))  # Details

    for file in existing_files:
        shutil.copy2(file, agent_work_dir / file.name)

# Now synthesis agent can read previous research
# e.g., summary agent reads company.md, team.md, tech.md to create summary
```

### Error Handling

```python
try:
    # Spawn and run agent
    process = await asyncio.create_subprocess_exec(...)
    await process.wait()

    # Check return code
    if process.returncode != 0:
        stderr = (await process.stderr.read()).decode('utf-8')
        raise Exception(f"Agent failed with code {process.returncode}: {stderr}")

    # Verify expected outputs
    if not (agent_work_dir / f"{agent_name}.md").exists():
        print(f"⚠️  Warning: {agent_name}.md not created")

except Exception as e:
    print(f"❌ {agent_name} failed: {e}")
    return {"agent_name": agent_name, "status": "failed", "error": str(e)}
finally:
    # Always cleanup temp directory
    shutil.rmtree(agent_work_dir, ignore_errors=True)
```

### Two-Phase Execution Pattern

**Data gathering → Synthesis**

```python
# Phase 1: Gather data in parallel
data_agents = ["company", "team", "tech", "products", "press"]
tasks = [run_agent(a, company, domain) for a in data_agents]
data_results = await asyncio.gather(*tasks)

print(f"✅ Phase 1: {len(data_results)} data agents completed")

# Phase 2: Synthesize in parallel (after data available)
synthesis_agents = ["summary", "pest", "complete_brief", "slidev"]
tasks = [run_agent(a, company, domain) for a in synthesis_agents]
synthesis_results = await asyncio.gather(*tasks)

print(f"✅ Phase 2: {len(synthesis_results)} synthesis agents completed")
```

**Why two phases:**
- Data agents can run fully in parallel (no dependencies)
- Synthesis agents need data agent outputs (but can still run in parallel with each other)
- Maximize parallelization while respecting dependencies

### Local Tooling Pattern

**Guideline:** When building local analysis/automation tools, **prefer Claude CLI subprocess over direct API calls**

**Why:**
- No credentials management (uses existing Claude Code session)
- No API keys or Bedrock setup required
- Simpler implementation (subprocess vs. boto3/SDK)
- Same environment as interactive Claude Code
- Reuses established patterns from company researcher

**Use cases:**
- Feedback analysis tools
- Code quality analyzers
- Documentation generators
- Report synthesis
- Data processing and analysis
- Any local automation that needs LLM intelligence

**Pattern:**
```python
import asyncio
import subprocess
import shutil

# Find claude CLI
claude_path = shutil.which('claude')
if not claude_path:
    raise RuntimeError("Claude CLI not found")

# Build prompt
prompt = "Analyze this data and provide insights..."

# Spawn subprocess
process = await asyncio.create_subprocess_exec(
    claude_path,
    '--permission-mode', 'bypassPermissions',
    '--model', 'sonnet',  # or 'haiku', 'opus'
    '--print',
    '--output-format', 'stream-json',
    stdin=asyncio.subprocess.PIPE,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
)

# Send prompt
process.stdin.write(prompt.encode('utf-8'))
await process.stdin.drain()
process.stdin.close()

# Capture output
output_text = []
async for line in process.stdout:
    data = json.loads(line.decode('utf-8').strip())
    if data.get('type') == 'assistant':
        for block in data['message']['content']:
            if block['type'] == 'text':
                output_text.append(block['text'])

# Wait for completion
await process.wait()

# Use the output
result = '\\n'.join(output_text)
```

**Examples:**
- **Feedback Analysis**: `shared/scripts/analyze-feedback.py` - Analyzes interaction feedback to suggest CLAUDE.md improvements
- **Company Research**: `prototypes/proto-company-researcher-uiwid-005/orchestrator.py` - Multi-agent research orchestrator

**Benefits over direct API:**
- ✅ No credential management
- ✅ Simpler setup (just need `claude` CLI installed)
- ✅ Same patterns as company researcher
- ✅ Automatic settings inheritance
- ✅ Less code (no SDK initialization)

**When to use direct API instead:**
- Server-side production deployments (need IAM roles, not local CLI)
- Services without Claude CLI available
- Need fine-grained API control (like prompt caching configuration)

### Best Practices

**✅ DO:**
- Use isolated temp directories per agent (prevents conflicts)
- Stream output for real-time monitoring
- Log everything (orchestrator, agent output, stderr)
- Organize outputs by type (summaries, raw research, artifacts, logs)
- Cleanup temp directories after completion
- Use `--permission-mode bypassPermissions` for autonomous execution
- Run independent agents in parallel with `asyncio.gather`
- Copy existing context to agent work dirs for synthesis agents

**❌ DON'T:**
- Share working directories between parallel agents (causes `settings.local.json` conflicts)
- Use blocking subprocess calls (kills parallelization)
- Skip error handling and logging
- Mix different execution patterns (e.g., some sync, some async)
- Forget to cleanup temp directories
- Run dependent agents in parallel (data gathering must complete before synthesis)

### Performance Considerations

**Parallelization gains:**
- Sequential: N agents × avg_time (e.g., 18 agents × 30s = 9 min)
- Parallel: max(agent_times) (e.g., longest agent = 5 min)
- **Speedup:** ~3x for typical multi-agent workflows

**Model selection:**
- `haiku`: Fast, cheap ($0.25/M input, $1.25/M output), ideal for data gathering
- `sonnet`: Balanced quality/speed, good for synthesis
- `opus`: Best quality, expensive, use sparingly for complex reasoning

**Cost optimization:**
- Use `haiku` for data gathering (18 agents × $0.02 = $0.36)
- Use `sonnet` for synthesis (4 agents × $0.15 = $0.60)
- Total: ~$1 for comprehensive research

### Example: Company Research Orchestrator

**See:** `prototypes/proto-company-researcher-uiwid-005/orchestrator.py`

**Usage:**
```bash
# Python orchestrator (parallel child processes)
python orchestrator.py "Stripe" --preset standard --model haiku

# Interactive slash commands (same prompts, single execution)
/company-agent "Stripe" "stripe.com"
/team-agent "Stripe" "stripe.com"
/summary-agent "Stripe" "stripe.com"
```

**18 agents, 5 minutes, $1 total cost, comprehensive company intelligence**

