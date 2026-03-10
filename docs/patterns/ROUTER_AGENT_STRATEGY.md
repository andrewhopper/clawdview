# Router Agent Strategy
<!-- File UUID: 7c4e8a9f-2d3b-4e7c-9a1f-3b5c6d8e9f2a -->

## 1.0 OVERVIEW

**Problem:** Main Claude loads full CLAUDE.md (~6K tokens) + conversation context on every interaction, causing slowness.

**Solution:** Transform main Claude into lightweight router that delegates complex tasks to specialized agents with narrow context.

**Expected Performance Gain:**
- Current: 6K tokens baseline (CLAUDE.md) + 4-10K context = 10-16K tokens
- With router: 2K tokens baseline (router only) + 3-6K context = 5-8K tokens
- **Estimated speedup: 40-60% faster responses**

## 2.0 ARCHITECTURE

### 2.1 Router Claude (Main)
**Role:** Traffic controller & orchestrator
**Context Load:** Minimal (~2K tokens)
**Responsibilities:**
1. Classify incoming request (intent detection)
2. Determine which specialist agent to spawn
3. Hand off full context to specialist
4. Receive result and relay to user
5. Track conversation continuity

**Does NOT:**
- Write code directly
- Execute complex workflows
- Load full SDLC documentation
- Perform deep research

### 2.2 Specialist Agents
Each agent loads **only its domain-specific context**.

```
┌─────────────────────────────────────────────────────┐
│                   ROUTER CLAUDE                      │
│            (Lightweight Orchestrator)                │
└──────────┬────────────────────────────────┬─────────┘
           │                                │
           ▼                                ▼
    ┌─────────────┐                 ┌─────────────┐
    │  Planning   │                 │    Code     │
    │   Agent     │                 │Implementer  │
    │             │                 │   Agent     │
    │ Phase 1-7   │                 │  Phase 8    │
    └─────────────┘                 └─────────────┘
           │                                │
           ▼                                ▼
    ┌─────────────┐                 ┌─────────────┐
    │  Research   │                 │    Docs     │
    │   Agent     │                 │   Agent     │
    │             │                 │             │
    │ Phase 2     │                 │ Reports     │
    └─────────────┘                 └─────────────┘
```

## 3.0 AGENT SPECIFICATIONS

### 3.1 Planning Agent
**Trigger:** SDLC Phase 1-7 work (SEED → Design)
**Context Load:** ~4K tokens
- CLAUDE.md sections: 1.0, 2.0, 3.0, 6.0 (SDLC only)
- Current phase docs: `@processes/PHASE_{N}_{NAME}`
- Relevant gate docs
- Project `.project` file

**Responsibilities:**
- Execute Phase 1 (SEED) - capture idea
- Execute Phase 2 (Research) - competitive analysis
- Execute Phase 3 (Expansion) - feature breakdown
- Execute Phase 4-6 - analysis, selection, design
- Execute Phase 7 (Test Scenarios) - scenario writing
- Update `.project` file with phase transitions
- Hand off to Code Implementer at Phase 8

**Output:** Phase completion artifacts + updated `.project`

### 3.2 Code Implementation Agent
**Trigger:** Phase 8 implementation work
**Context Load:** ~5K tokens
- CLAUDE.md sections: 1.0, 7.0 (Technical Standards)
- Code standards: `hmode/shared/standards/code/{tech}/`
- Domain models: relevant from `hmode/hmode/shared/semantic/domains/`
- Project context: `.project`, tech stack, architecture

**Responsibilities:**
- Write production code following standards
- Run tests immediately after creation
- Follow BDD workflow if tests exist
- Apply domain models and design patterns
- Update buildinfo.json for frontend apps
- Execute post-deployment smoke tests

**Does NOT:**
- Plan architecture (already done in Phase 6)
- Research alternatives (already done in Phase 2)
- Design UI/UX (delegates to ux-component-agent)

**Output:** Implemented code + test results

### 3.3 Research Agent
**Trigger:** Research requests, Phase 2 work, competitive analysis
**Context Load:** ~3K tokens
- CLAUDE.md sections: 1.0, 3.0 (Writing Standards), 4.2 (Research Workflow)
- Artifact library templates
- Web search tools
- Citation standards

**Responsibilities:**
- Execute competitive analysis
- Research technical solutions
- Generate research reports with citations
- Apply effort calibration (brief/standard/comprehensive)
- Format using densified writing style

**Output:** Research reports, comparison tables, recommendations

### 3.4 Documentation Agent
**Trigger:** Documentation requests, README updates, technical writing
**Context Load:** ~3K tokens
- CLAUDE.md sections: 1.0, 3.0 (Writing Standards)
- Writing style guide: `hmode/guardrails/WRITING_STYLE_GUIDE.md`
- Documentation templates
- Artifact library

**Responsibilities:**
- Generate READMEs, API docs, runbooks
- Create phase reports and project summaries
- Write user guides and tutorials
- Apply brand voice and writing standards
- Format using decimal outline structure

**Output:** Documentation files (Markdown, HTML)

## 4.0 ROUTING LOGIC

### 4.1 Intent Classification Matrix

| User Request Pattern | Route To | Context Loaded |
|---------------------|----------|----------------|
| "Start new project/idea" | Planning Agent | Phase 1 docs |
| "Research alternatives for X" | Research Agent | Research templates |
| "Implement feature X" | Code Implementation Agent | Code standards |
| "Write README for X" | Documentation Agent | Writing standards |
| "Continue working on X" | Detect phase → route accordingly | Project `.project` file |
| "Deploy X to Y" | infra-sre-agent OR amplify-deploy-specialist | Deployment docs |
| "Create mockup for X" | ux-component-agent | Design system |
| "Design navigation for X" | information-architecture-agent | IA patterns |
| "What domains apply to X?" | domain-modeling-specialist | Domain registry |

### 4.2 Router Decision Tree

```
User Request
     ↓
[Read .project file if exists]
     ↓
┌────────────────────────┐
│  Intent Classification │
│  (5 categories)        │
└────────┬───────────────┘
         │
    ┌────┴────┐
    │ Phase?  │
    └────┬────┘
         │
    ┌────┴────────────────────────────┐
    │                                 │
  Phase 1-7                       Phase 8+
    │                                 │
    ▼                                 ▼
Planning Agent              Code Implementation Agent
    │                                 │
    └─────────┬───────────────────────┘
              │
              ▼
      [Specialized agents]
      - Research Agent
      - Documentation Agent
      - Domain Specialist
      - IA Agent
      - UX Agent
      - Infra/SRE Agent
```

### 4.3 Agent Hand-Off Protocol

**When router spawns agent:**
```json
{
  "intent": "implementation",
  "phase": 8,
  "project_path": "/path/to/project",
  "project_context": {
    "uuid": "abc123",
    "name": "project-name",
    "tech_stack": ["Next.js", "FastAPI"],
    "current_phase": 8,
    "phase_status": "in_progress"
  },
  "user_request": "Implement user authentication",
  "relevant_docs": [
    "@processes/PHASE_8_IMPLEMENTATION",
    "hmode/shared/standards/code/typescript/",
    "hmode/hmode/shared/semantic/domains/auth/"
  ]
}
```

**When agent returns:**
```json
{
  "status": "success|partial|failed",
  "output": "Implementation complete. Created 3 files...",
  "artifacts": [
    "src/auth/login.ts",
    "src/auth/register.ts",
    "tests/auth.test.ts"
  ],
  "next_action": "Run tests" | "Deploy" | "Continue to Phase 9",
  "context_for_followup": {
    "phase": 8,
    "work_completed": ["auth implementation"],
    "work_remaining": ["email verification", "password reset"]
  }
}
```

## 5.0 IMPLEMENTATION PLAN

### 5.1 Phase 1: Router Claude (Main)
**File:** `CLAUDE.md` (further reduce to ~400 lines)
**Keep:**
- Section 1.0 (Overview)
- Section 2.0 (Intent Detection) - simplified
- Agent routing table
- Hand-off protocol

**Remove:**
- Section 4.0 (Workflows) → move to agents
- Section 6.0 (SDLC) → move to Planning Agent
- Section 7.0 (Technical Standards) → move to Code Implementation Agent
- Section 8.0 (Capabilities) → distribute to agents

### 5.2 Phase 2: Create Agent Specs
**Location:** `hmode/agents/`
**Files to create:**
- `planning-agent.md` (Phase 1-7 specialist)
- `code-implementation-agent.md` (Phase 8 specialist)
- `research-agent.md` (Phase 2 + ad-hoc research)
- `documentation-agent.md` (Technical writing)

**Existing agents (keep):**
- `domain-modeling-specialist.md`
- `information-architecture-agent.md`
- `ux-component-agent.md`
- `infra-sre-agent.md`
- `amplify-deploy-specialist.md`

### 5.3 Phase 3: Update Routing Commands
**File:** `hmode/commands/workon.md`
**Enhancement:** Auto-detect phase and route to correct agent

**New command:** `hmode/commands/route.md`
**Purpose:** Manual agent selection for edge cases

### 5.4 Phase 4: Proof of Concept
**Test with:**
1. New project request → Planning Agent (Phase 1)
2. Implementation request → Code Implementation Agent (Phase 8)
3. Research request → Research Agent
4. Documentation request → Documentation Agent

**Success criteria:**
- 40-60% token reduction vs current
- No loss of functionality
- Faster response times

## 6.0 MIGRATION STRATEGY

### 6.1 Gradual Rollout
**Week 1:** Create agent specs, test Planning Agent
**Week 2:** Test Code Implementation Agent
**Week 3:** Test Research + Documentation Agents
**Week 4:** Full cutover, monitor performance

### 6.2 Fallback Plan
Keep `CLAUDE.md.backup-*` files for 30 days.
If issues arise, revert with: `cp CLAUDE.md.backup-YYYYMMDD CLAUDE.md`

### 6.3 Performance Monitoring
**Metrics to track:**
- Average token count per interaction
- Response latency (user perception)
- Task completion success rate
- Number of agent hand-offs per task

**Target KPIs:**
- Token reduction: 40-60%
- Latency improvement: 30-50%
- Success rate: maintain 95%+

## 7.0 BENEFITS & TRADEOFFS

### 7.1 Benefits
1. **Performance:** 40-60% faster responses
2. **Cost:** Lower token costs per interaction
3. **Scalability:** Easy to add new specialist agents
4. **Maintainability:** Each agent has focused, narrow docs
5. **Clarity:** Clearer separation of concerns

### 7.2 Tradeoffs
1. **Complexity:** More agents to maintain
2. **Context loss:** Agent hand-offs may lose subtle context
3. **Debugging:** Harder to trace issues across agents
4. **Initial effort:** Requires upfront investment to create agents

### 7.3 Risk Mitigation
- Keep backup of current CLAUDE.md (already done)
- Implement gradually with A/B testing
- Monitor performance metrics closely
- Maintain fallback option for 30 days

## 8.0 SUCCESS CRITERIA

**Must achieve:**
- [ ] 40% token reduction vs v5.0.0 baseline
- [ ] No loss of functionality
- [ ] Faster perceived response times

**Nice to have:**
- [ ] 60% token reduction
- [ ] Sub-agent performance metrics dashboard
- [ ] Automatic agent selection (no manual routing)

## 9.0 NEXT STEPS

1. **[DONE]** Optimize CLAUDE.md to 845 lines (v5.0.0)
2. **[DONE]** Create Planning Agent spec (proof of concept)
3. **[NEXT]** Test Planning Agent with new project request
4. **[DONE]** Create Code Implementation Agent spec
5. Test end-to-end workflow (Phase 1 → Phase 8)
6. Measure performance improvements
7. **[DONE]** Create remaining agents (Research, Documentation)
8. Full cutover

---

**Document Status:** Draft v1.0
**Author:** Router Agent Strategy Working Group
**Date:** 2026-02-04
**Next Review:** After proof-of-concept completion
