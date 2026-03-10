---
uuid: cmd-cite-0j1k2l3m
version: 1.0.0
last_updated: 2025-11-10
description: Add citations to a markdown document with linked references
---

# Cite

Transform a markdown document by adding proper citations. Searches for credible sources, adds inline citation markers, and creates a References section.

## Purpose

For idea documents, technical specs, or research notes that need authoritative sources and proper citations.

## Process

1. **Read target document**
   - User provides path to markdown file (typically in `ideas/` folder)
   - If no path provided, ask user for document location

2. **Identify citation needs**
   - Look for markers: `[citation needed]`, `[source]`, `[ref]`
   - Identify factual claims that need backing
   - Note technical assertions requiring sources
   - Flag statistics, research findings, or quotes

3. **Search for sources**
   - Use WebSearch to find credible sources for each claim
   - Prioritize: official docs, research papers, reputable tech sites, industry reports
   - Avoid: low-quality sources, blogs without authority, outdated content
   - Gather: title, URL, author/org (if available), publication date

4. **Update document**
   - Replace citation markers with numbered references: `[1]`, `[2]`, etc.
   - Add inline citations after relevant statements
   - Maintain original content and meaning
   - Preserve formatting and structure

5. **Create References section**
   - Add `## References` section at document end (or update if exists)
   - Format each citation:
     ```
     [1] Title - Source Name
         URL
         Accessed: YYYY-MM-DD
     ```
   - Order citations by first appearance
   - Include all citation details

6. **Write updated document**
   - Save changes to original file
   - Preserve all other content
   - Maintain markdown formatting

## Citation Markers

**User can mark statements needing citations:**
- `[citation needed]` - General citation needed
- `[source]` - Source required
- `[ref]` - Reference needed
- `[cite: search query]` - Specific search query for citation

**Examples:**
```markdown
TypeScript adoption grew 50% in 2023 [citation needed]

PostgreSQL handles 15k writes/sec on m5.large [source]

React remains most popular frontend framework [ref]

WebAssembly enables near-native performance [cite: wasm performance benchmarks]
```

## Citation Format

**Inline:**
```markdown
TypeScript adoption grew 50% in 2023.[1]
```

**References Section:**
```markdown
## References

[1] State of JavaScript 2023 Survey - JavaScript Rising
    https://stateofjs.com/2023/typescript-adoption
    Accessed: 2025-11-07

[2] PostgreSQL Performance Benchmarks - PostgreSQL Wiki
    https://wiki.postgresql.org/wiki/Performance_Optimization
    Accessed: 2025-11-07
```

## Usage Examples

**Basic usage:**
```
/cite ideas/proto-001-ai-agents/seed.md
```

**With context:**
```
/cite ideas/proto-003-realtime-chat/analysis.md
Please focus on finding citations for the WebSocket performance claims
```

**Multiple documents:**
```
/cite ideas/proto-002-auth/expansion.md ideas/proto-002-auth/analysis.md
```

## Search Strategy

**For technical claims:**
- Official documentation (React docs, AWS docs, etc.)
- GitHub repositories (stars, activity, official status)
- Technical blogs from reputable sources (Vercel, Netlify, etc.)
- Stack Overflow insights for common patterns

**For statistics:**
- Industry reports (State of JS, Stack Overflow Survey, etc.)
- Research papers (IEEE, ACM, arXiv)
- Company reports (from relevant tech companies)
- Market analysis (Gartner, IDC, etc.)

**For best practices:**
- Official style guides
- Well-known developer resources (MDN, web.dev)
- Established engineering blogs (Airbnb, Netflix, etc.)
- Conference talks and presentations

## Quality Checks

Before finalizing:
- [ ] All citation markers replaced with numbered references
- [ ] Each citation has complete information (title, URL, date)
- [ ] URLs are valid and accessible
- [ ] Sources are credible and authoritative
- [ ] Citation numbers match references section
- [ ] References ordered by first appearance
- [ ] Document structure and content preserved
- [ ] Markdown formatting maintained

## Citation Coverage Metrics

**Calculate and report citation quality:**

1. **Count factual claims:**
   - Statistics or numbers (e.g., "50% growth", "15k writes/sec")
   - Technical assertions (e.g., "fastest framework", "most secure")
   - Comparative statements (e.g., "better than X", "outperforms Y")
   - Research findings or quotes
   - Best practice recommendations

2. **Count citations:**
   - Explicit markers found and resolved
   - Existing citations in document
   - New citations added

3. **Calculate coverage:**
   ```
   Coverage = (Claims with citations / Total claims) × 100%
   ```

4. **Quality rating:**
   - **Excellent (90-100%):** 🟢 Strong evidence base
   - **Good (70-89%):** 🟡 Well-supported, some gaps
   - **Fair (50-69%):** 🟠 Needs more citations
   - **Poor (<50%):** 🔴 Insufficient backing

## Output Format

Present changes as:
```
📚 Citation Report

**Document:** [path]

**Coverage Metrics:**
📊 Claims: 10 total
✅ Cited: 7 claims (70%)
❌ Uncited: 3 claims
🟡 Quality: Good - Well-supported, some gaps

**Citations Added:** 7
**Sources Found:**
- [1] State of JavaScript 2023 Survey - JavaScript Rising
- [2] PostgreSQL Performance Benchmarks - PostgreSQL Wiki
- [3] React Documentation - Official Docs
...

**Changes:**
- Line 23: Added citation [1] for TypeScript adoption claim
- Line 45: Added citation [2] for PostgreSQL performance data
- Line 67: Added citation [3] for React popularity claim
- Added References section at end

**Uncited Claims:**
- Line 12: "Most developers prefer TypeScript" - needs survey data
- Line 89: "WebSockets are faster than polling" - needs benchmark
- Line 102: "JWT is industry standard" - needs authoritative source

✅ Document updated with citations
```

**Example variations:**

**Excellent coverage (95%):**
```
**Coverage Metrics:**
📊 Claims: 20 total
✅ Cited: 19 claims (95%)
❌ Uncited: 1 claim
🟢 Quality: Excellent - Strong evidence base
```

**Poor coverage (40%):**
```
**Coverage Metrics:**
📊 Claims: 15 total
✅ Cited: 6 claims (40%)
❌ Uncited: 9 claims
🔴 Quality: Poor - Insufficient backing

**Recommendation:** Review uncited claims below and add sources
```

## Edge Cases

**No citation markers found:**
- Ask user to point out specific claims needing citations
- Or suggest adding markers for review

**Citation not found:**
- Note which claims couldn't be cited
- Suggest alternative search terms
- Flag for manual research

**Existing citations:**
- Preserve existing references
- Add new citations with next available numbers
- Update References section accordingly

**Multiple files:**
- Process each file independently
- Report on each file separately

## Implementation Notes

1. **Read original document** first
2. **Analyze content** for claims:
   - Scan for numbers, statistics, percentages
   - Identify technical assertions and comparisons
   - Note existing citations
3. **Parse for citation markers** using regex
4. **Count total claims** in document
5. **Search systematically** for each marker
6. **Collect all citations** before writing
7. **Calculate coverage metrics**:
   - Total claims identified
   - Claims with citations (marked + existing)
   - Claims without citations
   - Coverage percentage
   - Quality rating
8. **Update document once** with all changes
9. **Validate** all URLs work
10. **Report changes** with metrics to user

## Philosophy

Good citations:
- Support factual claims with authoritative sources
- Enable readers to verify information
- Add credibility to technical arguments
- Point to further reading and context
- Use current, relevant sources

---

**Remember:** Citations strengthen technical documents by providing verifiable sources and enabling deeper research. Always prioritize quality, authoritative sources over quick, questionable ones.
