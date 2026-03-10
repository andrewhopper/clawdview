---
uuid: cmd-del-email-9s0t1u2v
version: 1.0.0
last_updated: 2025-11-11
description: Generate AWS-style delivery email for prototype
---

# Generate Delivery Email

Generate dense, AWS-style email for `{proto_dir}` delivery package.

## Usage

```bash
/generate-delivery-email prototypes/proto-027-semantic-schema-mapper [--narrative=./NARRATIVE.md] [--output=./delivery-email.txt]
```

**Arguments:**
- `{proto_dir}`: Path to prototype or idea directory
- `--narrative=./NARRATIVE.md`: Path to narrative doc (optional, enhances content)
- `--output=./delivery-email.txt`: Output file path (default: delivery-email.txt)

## Output

**delivery-email.txt** - 3-5 paragraph dense email with:
- Context (why sending, customer engagement)
- What's included (package contents summary)
- Key highlights (3-5 main points)
- Next steps (actions for recipient)
- Closing (contact info, follow-up)

## Email Structure

**Dense Amazon Style:**
- 3-5 paragraphs max
- Every sentence adds value
- Quantify everything
- No filler words
- Active voice
- Specific dates/metrics

**Format:**
```
Subject: {Project Name} - Prototype Delivery

{Paragraph 1: Context}
{Paragraph 2: What's Included}
{Paragraph 3: Key Highlights}
{Paragraph 4: Next Steps}
{Paragraph 5: Closing (optional)}
```

## Workflow

### Step 1: Gather Context

1. **Read project files**:
   - `.project` → metadata, description, phase
   - `README.md` → overview
   - `NARRATIVE.md` (if provided) → comprehensive details
   - `artifacts/delivery/YYYY-MM-DD-{name}/` → package contents

2. **Extract key information**:
   - **Problem solved**: What pain point addressed?
   - **Solution approach**: How does it work?
   - **Key outcomes**: Results, metrics, impact
   - **Technologies**: Tech stack highlights
   - **Next actions**: What should recipient do?

### Step 2: Generate Email Content

3. **Subject line**:

```
Subject: {Project Name} - Prototype Delivery Package
```

**Format**: Short, descriptive, professional

4. **Paragraph 1: Context** (2-4 sentences)

```
As discussed during our {date} engagement, I've completed the {project name} prototype to {primary purpose}. This prototype {key innovation or approach} to address {problem statement}. Package includes complete source code, architecture diagrams, technical documentation, and Slidev presentation.
```

**Content sources:**
- `.project` description → Primary purpose
- `NARRATIVE.md` problem statement → Problem addressed
- Engagement date (inferred or current date) → Context

**Example:**
```
As discussed during our October 2024 engagement, I've completed the Semantic Schema Mapper prototype to automate data mapping between heterogeneous database schemas. This prototype leverages LLMs with semantic understanding to reduce manual mapping time from 2-3 days to <1 hour. Package includes complete source code, architecture diagrams, technical documentation, and Slidev presentation.
```

5. **Paragraph 2: What's Included** (2-4 sentences)

```
Delivery package (attached as {filename}.zip, {size} MB) contains: (1) production-ready {language/framework} implementation with {component count} core components, (2) DrawIO and Mermaid architecture diagrams, (3) comprehensive technical narrative covering problem statement through implementation, (4) Slidev presentation with 13 slides, and (5) usage guide with installation/configuration steps. All documentation follows AWS writing standards and includes {specific details like API references, code examples, etc.}.
```

**Content sources:**
- ZIP file size → Package details
- Tech stack from `.project` → Technologies
- Diagram count → Visual aids
- Documentation list → Contents

**Example:**
```
Delivery package (attached as 2025-11-11-semantic-schema-mapper.zip, 15MB) contains: (1) production-ready Python implementation with 8 core modules including LLM-based semantic analyzer, (2) DrawIO architecture diagram plus Mermaid sequence diagrams, (3) comprehensive technical narrative (12 pages) covering problem statement through implementation details, (4) Slidev presentation with 13 slides ready for stakeholder demos, and (5) usage guide with API reference and code examples. All documentation follows AWS writing standards.
```

6. **Paragraph 3: Key Highlights** (3-5 bullet points or sentences)

```
Key highlights: (1) {Highlight 1 with metric}, (2) {Highlight 2 with technical detail}, (3) {Highlight 3 with outcome}, (4) {Highlight 4 with innovation}, and (5) {Highlight 5 with next step or recommendation}.
```

**Content sources:**
- `NARRATIVE.md` outcomes → Metrics
- Success criteria from `.project` → Achievements
- Technical decisions → Innovations
- Results section → Impact

**Example:**
```
Key highlights: (1) Achieved 85% mapping accuracy on test schemas, reducing manual validation time by 70%, (2) Implemented semantic similarity algorithm using sentence transformers with custom domain vocabulary, (3) Supports PostgreSQL, MySQL, MongoDB with extensible adapter pattern for additional databases, (4) Includes FastAPI REST interface for integration with existing ETL pipelines, and (5) Designed for AWS deployment via Lambda + RDS with estimated $50/month operational cost at 1000 mappings/month.
```

7. **Paragraph 4: Next Steps** (2-3 sentences)

```
Recommended next steps: (1) review {specific document} for {purpose}, (2) run local demo using installation guide in README.md, and (3) {specific action like "schedule 30-min walkthrough" or "test with your production schemas"}. I'm available for technical Q&A and can provide additional context on {specific areas like architecture decisions, deployment options, or integration patterns}.
```

**Content sources:**
- README.md → Installation steps
- NARRATIVE.md next steps → Recommendations
- Customer context → Specific actions

**Example:**
```
Recommended next steps: (1) review NARRATIVE.md sections 4.0 (Architecture) and 6.0 (Usage Guide) for implementation details, (2) run local demo using `docker-compose up` command in README.md, and (3) test mapping accuracy with 2-3 representative schemas from your environment. I'm available for technical Q&A and can provide additional context on LLM prompt engineering, adapter pattern implementation, or AWS deployment architecture.
```

8. **Paragraph 5: Closing** (1-2 sentences, optional)

```
{Acknowledgment or forward-looking statement}. Please reach out to your AWS account team or reply directly with questions or feedback.
```

**Example:**
```
This prototype demonstrates feasibility of LLM-based schema mapping for your use case and provides foundation for production implementation. Please reach out to your AWS account team or reply directly with questions or feedback.
```

### Step 3: Apply AWS Style

9. **Validate and fix AWS style**:
   - Use CSAT, not NPS
   - Specific dates, not "recently"
   - Quantify everything
   - "As an AWS Partner" if applicable
   - No fear-based security terms
   - "in AWS Marketplace" not "on AWS Marketplace"

10. **Densify**:
    - Remove filler: "very", "really", "just", "actually"
    - Combine sentences: Use semicolons, em-dashes
    - Active voice: "Prototype reduces time" not "Time is reduced"
    - Eliminate redundancy: "included and provided" → "included"

### Step 4: Write Email File

11. **Generate complete email**:
    - Use Write tool to create `{output_file}`
    - Format: Plain text, ready to copy-paste
    - Include subject line

12. **Report results**:

```markdown
# Delivery Email Generated

**Project**: {proto_name}
**Output**: {output_file}
**Length**: {word_count} words, {char_count} chars
**Paragraphs**: {paragraph_count}

---

## Email Preview

\`\`\`
{First 200 characters of email}...
\`\`\`

---

## Density Metrics

- **Words**: {word_count} (target: 150-250)
- **Characters**: {char_count}
- **Sentences**: {sentence_count}
- **Avg words/sentence**: {avg} (target: 15-20)

---

## Quality Checks

✅ AWS style compliant
✅ Quantified outcomes
✅ Specific dates/metrics
✅ Active voice
✅ Dense writing

---

## Usage

Copy email from: `{output_file}`
Paste into Outlook/Gmail
Attach ZIP file: `artifacts/delivery/{date-name}.zip`
Update recipient, subject if needed

---

✅ Email ready for customer delivery
```

## Email Templates by Project Type

**API/Backend Service:**
```
Subject: {Project Name} - API Prototype Delivery

As discussed during our {date} engagement, I've completed the {project name} prototype to {solve problem}. This {language/framework} API implements {key feature} with {metric like "sub-200ms p95 latency"} for {use case}. Package includes complete source, OpenAPI spec, architecture diagrams, and deployment guide.

Delivery package (attached as {filename}.zip, {size}MB) contains: (1) production-ready {framework} REST API with {N} endpoints, (2) architecture diagrams showing service dependencies and data flow, (3) technical narrative with API reference and authentication details, (4) Slidev presentation for stakeholder demos, and (5) Docker Compose setup for local testing. Documentation includes performance benchmarks and AWS deployment options.

Key highlights: (1) {metric/outcome}, (2) {technical innovation}, (3) {integration capability}, (4) {scalability feature}, and (5) {cost estimate for AWS deployment}.

Recommended next steps: (1) review API_DESIGN.md for endpoint specifications, (2) run local instance via `docker-compose up` and test with provided Postman collection, and (3) {customer-specific action}. I'm available for technical Q&A on authentication patterns, scaling strategies, or AWS deployment architecture.

This prototype validates {hypothesis} and provides foundation for {next phase}. Please reach out to your AWS account team or reply directly with questions.
```

**Data Pipeline/ETL:**
```
Subject: {Project Name} - Data Pipeline Prototype Delivery

As discussed during our {date} engagement, I've completed the {project name} prototype to {transform/process} {data type} at {scale metric like "1M records/hour"}. This {Python/Spark} pipeline implements {approach} to address {data quality/performance/cost challenge}. Package includes complete implementation, data flow diagrams, sample datasets, and operational runbook.

Delivery package (attached as {filename}.zip, {size}MB) contains: (1) production-ready {Python/Spark} pipeline with {N} transformation stages, (2) Mermaid data flow diagrams, (3) technical narrative covering schema design through error handling, (4) Slidev presentation with performance benchmarks, and (5) sample input/output datasets. Documentation includes AWS Glue and EMR deployment patterns.

Key highlights: (1) {throughput metric}, (2) {data quality improvement}, (3) {cost reduction vs current approach}, (4) {error handling strategy}, and (5) {monitoring/alerting capabilities}.

Recommended next steps: (1) review ARCHITECTURE.md section 4.3 (Data Flow), (2) test with sample datasets using provided Docker environment, and (3) {validate with subset of production data}. I'm available for technical Q&A on schema evolution, partitioning strategies, or AWS deployment architecture.

This prototype demonstrates {capability} and provides foundation for {production rollout}. Please reach out to your AWS account team or reply directly with questions.
```

**Full-Stack Application:**
```
Subject: {Project Name} - Full-Stack Prototype Delivery

As discussed during our {date} engagement, I've completed the {project name} prototype to {user-facing capability}. This {React/Next.js} + {Node.js/Python} application implements {feature} with {UX metric like "3-click workflow"} for {target users}. Package includes frontend, backend, database schema, deployment guide, and interactive demo.

Delivery package (attached as {filename}.zip, {size}MB) contains: (1) production-ready {frontend framework} UI with {backend framework} API, (2) architecture diagrams showing component interactions, (3) technical narrative covering user flows through database design, (4) Slidev presentation with screenshots and demo flow, and (5) Docker Compose setup for full-stack local testing. Documentation includes AWS Amplify and ECS deployment options.

Key highlights: (1) {user outcome metric}, (2) {responsive design/accessibility feature}, (3) {API performance}, (4) {security implementation like OAuth}, and (5) {estimated AWS hosting cost}.

Recommended next steps: (1) review NARRATIVE.md section 6.0 (Usage Guide), (2) launch local environment via `docker-compose up` and access UI at localhost:3000, and (3) {test with specific user persona/workflow}. I'm available for technical Q&A on authentication flows, state management, or deployment architecture.

This prototype validates {user experience hypothesis} and provides foundation for {beta testing/production launch}. Please reach out to your AWS account team or reply directly with questions.
```

## Content Extraction Priorities

**Priority 1** - Quantified outcomes:
- Success criteria from `.project`
- Metrics from `NARRATIVE.md` section 7.2
- Performance benchmarks from tests

**Priority 2** - Technical highlights:
- Key innovations from `NARRATIVE.md` section 3.2
- Architecture decisions from `ARCHITECTURE.md`
- Tech stack from `.project`

**Priority 3** - Customer-specific context:
- Engagement details (infer from dates)
- Use case specifics from problem statement
- Integration points with customer systems

**Priority 4** - Practical next steps:
- README.md usage instructions
- NARRATIVE.md recommendations
- Test procedures from docs

## Writing Rules

**Dense Amazon style:**
- 15-20 words/sentence average
- No filler words
- Quantify everything
- Parallel structure in lists
- Semicolons to combine related thoughts

**Specificity:**
- "Q2 2024" not "recently"
- "85% accuracy" not "high accuracy"
- "$50/month" not "low cost"
- "Sub-200ms p95" not "fast"

**Active voice:**
- "System processes X" not "X is processed"
- "Prototype achieves Y" not "Y is achieved"
- "Implementation includes Z" not "Z is included"

## Error Handling

**Minimal documentation:**
```
Warning: Limited documentation available
Email generated from .project and README only
Recommend adding NARRATIVE.md for richer content
```

**No metrics available:**
```
Info: No quantified outcomes found
Email focuses on technical capabilities and approach
Consider adding metrics to .project success_criteria
```

## Best Practices

1. **Customer-first**: Frame in terms of customer problems/goals
2. **Action-oriented**: Clear next steps, not just info dump
3. **Quantify impact**: Use metrics from success criteria, tests
4. **Technical credibility**: Include specific technologies, decisions
5. **Attachment clarity**: Reference ZIP file size, contents
6. **Follow-up path**: Clear how to get help, ask questions

## Integration

Works with:
- `/prepare-delivery` - Final step in delivery workflow
- `/generate-project-narrative` - Primary content source
- `/amazon-style-checker` - Validates AWS compliance
- `/densify` - Ensures concise writing

---

Be dense, specific, and customer-focused.
