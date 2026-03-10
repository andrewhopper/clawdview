---
uuid: cmd-arch-research-5e6f7g8h
version: 1.0.0
last_updated: 2025-11-10
description: Research and document architectural options for technical decisions
---

# Architecture Research Command

You are helping the user conduct thorough architectural research. Follow this structured approach:

## Research Process

1. **Define Scope**
   - Clarify the architectural question/decision
   - Identify key evaluation criteria (cost, performance, scalability, etc.)
   - Determine constraints (budget, timeline, team expertise)

2. **Research Options**
   - Use WebSearch to find current (2025) information
   - Search for official documentation
   - Find real-world case studies and benchmarks
   - Look for cost comparisons and pricing updates
   - Research limitations and gotchas

3. **Batch Web Searches**
   - Execute ALL searches in parallel (one message, multiple WebSearch calls)
   - Search patterns:
     - "[Technology] pricing costs 2025"
     - "[Tech A] vs [Tech B] comparison performance 2025"
     - "[Technology] limitations cold start latency 2025"
     - "[Technology] production case studies real-world 2025"
     - "[Technology] best practices optimization 2025"

4. **Create Comparison Report**
   - Store in: `artifacts/research/[YYYY-MM-DD]/[topic-name]/`
   - Format: Markdown with tables, bullets, clear sections
   - Include:
     - Executive summary table
     - Detailed pros/cons for each option
     - Cost comparison (with real numbers)
     - Performance metrics (latency, throughput, cold starts)
     - Limitations and constraints
     - Decision matrix (by use case, budget, team skills)
     - Recommendations with rationale
     - References and sources

5. **Structure Report Sections**
   - Executive Summary (comparison table)
   - Detailed Option Analysis (one section per option)
   - Decision Matrix (by scenario)
   - Cost Optimization Strategies
   - 2025 Updates & Trends
   - Recommendations (by scenario)
   - Key Takeaways
   - References

## Quality Standards

- **Brevity:** Follow 50% fewer words rule (bullets, tables, no prose)
- **Current:** Always include "2025" in searches for latest info
- **Concrete:** Real costs, real metrics, real examples
- **Actionable:** Clear recommendations with rationale
- **Comparative:** Side-by-side tables, not isolated descriptions

## Example Topics

- Cloud service comparisons (AWS, GCP, Azure)
- Database options (SQL vs NoSQL vs NewSQL)
- Deployment strategies (serverless vs containers vs VMs)
- Architecture patterns (microservices vs monolith)
- Observability tools (metrics, logs, traces)
- CI/CD pipelines
- API gateway options
- Message queue comparisons

## Output

At the end, confirm:
- ✅ Report created at: `artifacts/research/[date]/[topic]/REPORT_NAME.md`
- 📊 X options compared
- 💰 Cost analysis included
- 🎯 Recommendations provided
- 🔗 Sources referenced

Now, ask the user: **"What architectural decision do you need to research?"**
