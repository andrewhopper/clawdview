# Writing Style Guide
**Amazonian Narrative Prose for Sales Intelligence**

**Purpose**: This guide defines the writing standards for all sales intelligence outputs, from agent research to executive summaries. We follow Amazon's narrative prose principles adapted for factual intelligence reporting.

**Last Updated**: November 2, 2025

---

## Core Philosophy: The Amazonian Narrative Approach

Amazon famously banned PowerPoint presentations in favor of narrative memos. Instead of bullet points, Amazon executives write complete sentences that tell a coherent story. This approach forces clearer thinking and better communication.

**Why Narrative Prose for Sales Intelligence?**

1. **Clarity**: Complete sentences reveal gaps in logic that bullets hide
2. **Context**: Narratives explain *why* facts matter, not just *what* they are
3. **Memorability**: Stories stick in readers' minds better than bullet lists
4. **Credibility**: Well-written prose builds trust and professionalism
5. **Action**: Narratives naturally lead to decisions and next steps

**Our Adaptation**:
- Amazon writes forward-looking memos (planning, proposals)
- We write backward-looking intelligence (research, findings)
- Amazon emphasizes persuasion; we emphasize **objective reporting**
- We keep Amazon's clarity, structure, and data-driven approach

---

## The Six Core Principles

### 1. Complete Sentences and Paragraphs

**Amazon's Rule**: Ban bullets in narrative sections. Use complete sentences that form coherent paragraphs.

**Our Application**:
- **Use bullets for**: Lists of facts (technologies, team members, funding rounds)
- **Use prose for**: Context, analysis, implications, recommendations
- **Hybrid approach**: Lead with prose context, follow with bulleted facts

**Example - Bad** (bullet dump without context):
```markdown
## Company Overview
- Founded 2019
- Boston, MA
- $200M raised
- 800 employees
- Healthcare tech
```

**Example - Good** (narrative with context):
```markdown
## Company Overview

Cohere Health, founded in 2019 in Boston, MA, has emerged as a leader in healthcare technology with a specific focus on prior authorization automation. The company has raised $200M across three funding rounds, most recently a $90M Series C in May 2025 led by Temasek. This substantial funding has enabled rapid growth to approximately 800 employees across 48 US states.

The company's focus on AI-powered prior authorization addresses a critical pain point in healthcare: the administrative burden of approval processes. With 93% provider satisfaction rates and the ability to auto-approve 90% of prior authorization requests, Cohere Health has positioned itself as a solution to one of healthcare's most manual and frustrating processes.

**Key Facts**:
- Founded: 2019 in Boston, MA
- Total Funding: $200M (Series C: $90M, May 2025)
- Employees: ~800 across 48 US states
- Valuation: $5.5B
- Industry: Healthcare Technology / Clinical Intelligence SaaS
```

**Why This Works**:
- Opening paragraph provides context and positioning
- Second paragraph explains *why* this matters (the problem they solve)
- Bullets provide quick reference facts
- Reader understands the story, not just the data points

---

### 2. Start with the Customer (or in our case, the Reader)

**Amazon's Rule**: Always begin with the customer's needs and work backwards.

**Our Application**: Begin intelligence reports by answering "Why does the reader need to know this?"

**For Different Report Types**:

**Executive Brief** (reader: busy executive, 5-10 min prep):
- Start: "This brief prepares you for a call with Cohere Health in 10 minutes or less."
- Focus: Conversation hooks, key decision-makers, immediate action items

**Standard Summary** (reader: AE preparing for discovery, 20-30 min):
- Start: "This report provides comprehensive intelligence for your discovery call with Cohere Health."
- Focus: Business model, team structure, engagement strategy

**Deep Dive** (reader: SA for enterprise deal, 45-60 min):
- Start: "This strategic account analysis qualifies the Cohere Health opportunity and provides a complete engagement playbook."
- Focus: Deal qualification, risk assessment, technical integration, stakeholder mapping

**Example Opening - Bad**:
```markdown
# Company Intelligence: Cohere Health

Cohere Health is a healthcare technology company.
```

**Example Opening - Good**:
```markdown
# Company Intelligence: Cohere Health

**For Sales Context**: Cohere Health is a high-value prospect in the healthcare AI space. As a $5.5B company with $200M in funding and 800 employees, they represent a strategic account opportunity. This profile provides the business context, growth indicators, and competitive positioning you need to understand their market position and identify how your solution fits their current trajectory.

**Quick Qualification**: Strong fit for enterprise solutions given their growth stage (Series C), technical sophistication (Python/PyTorch ML stack), and expansion priorities (Microsoft partnership, payment integrity suite launch).
```

---

### 3. Data-Driven Assertions

**Amazon's Rule**: Every claim must be backed by data. No opinions without evidence.

**Our Application**: Cite sources for every fact. Distinguish between confirmed facts and reasonable inferences.

**Citation Standards**:

**High Confidence** (primary source, recent):
```markdown
Cohere Health raised $90M in Series C funding in May 2025, led by Temasek. [1]

[1] https://www.prnewswire.com/news-releases/cohere-health-secures-90m-series-c... (May 14, 2025)
```

**Medium Confidence** (inferred from job postings):
```markdown
The engineering team is estimated at 50-60 engineers based on LinkedIn profiles and job posting references to "15-person backend team" and "12-person frontend team." [2][3]

[2] https://linkedin.com/company/coherehealth/people
[3] https://coherehealth.com/careers/senior-backend-engineer (mentions team size)
```

**Low Confidence** (speculative, mark as such):
```markdown
The company likely uses a multi-tenant SaaS architecture given their healthcare focus and compliance requirements, though this is not publicly confirmed. Architecture details are not disclosed in public documentation.
```

**Confidence Indicators**:
- **Confirmed**: Multiple primary sources or official company statement
- **Inferred**: Logical deduction from available evidence (state your reasoning)
- **Speculative**: Educated guess (clearly mark as such, explain limitations)

**Example - Bad** (unsupported claims):
```markdown
Cohere Health is struggling with scalability challenges and desperately needs infrastructure improvements. Their engineering team is overwhelmed and likely looking for solutions like ours.
```

**Example - Good** (data-driven with evidence):
```markdown
Cohere Health shows signals of infrastructure investment priority:
- Actively recruiting for 5 DevOps/Infrastructure roles [1]
- Recent hire of VP Engineering from Fidelity with infrastructure scaling experience [2]
- Job postings mention "scaling to process 12M+ requests annually" as a key challenge [1]
- Engineering blog post discusses Kubernetes cost optimization [3]

These hiring patterns and public communications suggest infrastructure scaling is a current priority, making this a potentially receptive time for infrastructure solutions.

[Sources listed]
```

---

### 4. Specificity and Concreteness

**Amazon's Rule**: Avoid vague language. Be specific with numbers, names, dates.

**Our Application**: Replace generic statements with specific facts.

**Vague vs. Specific**:

| Vague ❌ | Specific ✅ |
|---------|------------|
| "Recently funded" | "Raised $90M Series C on May 14, 2025" |
| "Large company" | "800 employees across 48 US states" |
| "Growing fast" | "60% year-over-year ARR growth (2024)" |
| "Well-known customers" | "Customers include Geisinger Health Plan, Humana (50 states), and 2 major BCBS plans" |
| "Senior leadership" | "Gus Weber, Chief Digital and Technology Officer (joined 2024, previously SVP Engineering at Fidelity)" |
| "Strong tech stack" | "Backend: Python and Java Spring Boot; ML: PyTorch with MLFlow; Infrastructure: AWS ECS and Kubernetes" |

**Example - Bad** (vague):
```markdown
Cohere Health has received positive recognition from industry analysts and is considered a leader in their space. They have several notable customers and are growing quickly.
```

**Example - Good** (concrete):
```markdown
Cohere Health has achieved significant analyst recognition in 2025:
- Gartner: Included in Hype Cycle for U.S. Healthcare Payers for 4th consecutive year (August 2025), "Transformational" benefit rating
- TIME: Named to World's Top HealthTech Companies 2025 with "Outstanding" ranking in AI & Data Analytics category (September 2025)
- Inc. 5000: Ranked in top 25% of fastest-growing private companies (August 2025)

Customer base includes three publicly disclosed healthcare organizations:
- Geisinger Health Plan: 47% admin cost reduction reported
- Humana: Deployed across all 50 states
- Two major Blue Cross Blue Shield plans (names not disclosed)

Growth metrics demonstrate rapid expansion: 60% year-over-year ARR growth in 2024, processing 12M+ prior authorization requests annually for 660,000+ providers.
```

---

### 5. Active Voice and Clear Attribution

**Amazon's Rule**: Use active voice. Make it clear who did what.

**Our Application**: Attribute actions to specific actors (company, CEO, team, competitors).

**Passive vs. Active**:

| Passive ❌ | Active ✅ |
|-----------|----------|
| "A partnership was announced" | "Cohere Health announced a partnership with Microsoft on October 17, 2025" |
| "The product was launched" | "The company launched Review Assist in June 2025" |
| "Investment is being made in AI" | "CEO Siva Namasivayam stated the company is investing heavily in AI" |
| "Growth has been achieved" | "The company grew employee headcount by 18% year-over-year" |

**Attribution Specificity**:

**Generic ❌**:
```markdown
The company believes AI is the future of healthcare and is investing accordingly.
```

**Specific ✅**:
```markdown
CEO Siva Namasivayam stated in an October 2025 interview that "AI will transform utilization management from a manual process into intelligent, real-time clinical decision support." [1] The company is backing this vision with concrete investments: hiring for 8 ML engineering roles [2], acquiring ZignaAI in September 2025 [3], and launching Review Assist with 99% precision AI in June 2025 [4].
```

---

### 6. Structured Narrative Flow

**Amazon's Rule**: Organize information logically. Use headers to guide readers through the story.

**Our Application**: Each section should follow a consistent structure.

**The Standard Intelligence Narrative Structure**:

```
1. Opening Context (Why this matters)
   ↓
2. Current State (What is true today)
   ↓
3. Historical Context (How we got here)
   ↓
4. Implications (What this means for sales)
   ↓
5. Actionable Insights (What to do about it)
```

**Example - Company Intelligence Section**:

```markdown
## Business Model & Market Position

**Context**: Understanding Cohere Health's business model is critical for positioning solutions, as their revenue model (PMPM admin fees) and customer base (health plans) determine their buying priorities and budget cycles.

**Current State**: Cohere Health operates a B2B SaaS platform targeting health plans and payers with AI-powered prior authorization automation. The company uses a per-member-per-month (PMPM) admin fee pricing model, generating revenue from subscription fees, implementation services, and quality improvement program fees. Revenue has grown 60% year-over-year, reaching an estimated $20-30M ARR in 2024 based on the company's growth trajectory from $11M in 2021.

**Market Evolution**: The company was founded in 2019 to address prior authorization pain points. Initially focused on utilization management, the company has expanded into adjacent markets: acquiring ZignaAI for payment integrity in September 2025 and launching Cohere Validate for claims validation. This expansion reflects a strategic shift from point solution (prior auth) to platform play (end-to-end clinical intelligence).

**Competitive Context**: Cohere Health ranks 3rd out of 41 competitors in the prior authorization technology market according to CB Insights. Primary competitors include Itiliti Health, Waystar, and EviCore. Cohere differentiates on AI automation (90% auto-approval rate vs. industry average of 30-40%), provider satisfaction (93% vs. industry average of 60-70%), and API-first architecture (Cohere Connect™ for EHR integration).

**Sales Implications**:
- **Budget Authority**: CFO (Robert Shepardson, joined Oct 2024) controls spending. Recently raised $90M, indicating capital availability.
- **Buying Cycle**: Healthcare SaaS typically has 6-12 month sales cycles due to security reviews (HIPAA, SOC 2) and compliance requirements.
- **Pain Points**: Recent Microsoft partnership announcement suggests point-of-care automation is a priority. Platform expansion into payment integrity indicates desire for unified clinical intelligence infrastructure.
- **Decision Criteria**: Likely evaluating solutions based on: (1) API integration ease, (2) HIPAA compliance documentation, (3) prior authorization workflow familiarity, (4) proven healthcare industry experience.
```

**Why This Structure Works**:
1. **Context** tells the reader why they should care
2. **Current State** provides the facts
3. **Historical Context** shows trajectory and momentum
4. **Competitive Context** positions the company in the market
5. **Sales Implications** translates intelligence into action

---

## Writing Guidelines by Output Type

### Agent Research Reports (company.md, team.md, tech.md, press.md)

**Purpose**: Factual intelligence gathering with minimal interpretation
**Audience**: Other agents, summary generators, sales professionals
**Tone**: Objective, factual, cited
**Structure**: Hybrid (prose context + bulleted facts)

**Guidelines**:
1. **Lead each section with 1-2 paragraphs of prose context**
2. **Follow with bulleted facts for scannability**
3. **Cite every fact with numbered references**
4. **Distinguish confirmed facts from inferences**
5. **No sales advice or recommendations** (save for summaries)
6. **Use present tense for current state, past tense for historical events**

**Example Structure**:
```markdown
## Growth Indicators

Cohere Health demonstrates strong growth momentum across multiple dimensions: funding, headcount, customer acquisition, and product expansion. The company raised $90M in Series C funding on May 14, 2025, bringing total funding to $200M and valuation to $5.5B. This funding round, led by Temasek with participation from all existing investors, signals strong investor confidence and provides runway for continued expansion.

**Funding History**:
- Series C: $90M (May 14, 2025) - Led by Temasek [1]
- Series B: $50M (February 2024) - Led by Deerfield Management [2]
- Series A: July 2020 - Led by Flare Capital Partners [3]
- Total Raised: $200M from 7 institutional investors

**Revenue Growth**:
- 2021 Revenue: $11M [4]
- 2024 Growth: >60% YoY ARR growth [5]
- Estimated 2024 ARR: $20-30M (calculated from 2021 baseline and growth rate)

**Employee Growth**:
- Current: ~800 employees [6]
- Growth Rate: 18% YoY [6]
- Distribution: 48 US states (remote-first model) [7]

[Sources listed with full URLs]
```

---

### Executive Brief (1-2 pages)

**Purpose**: Quick pre-call prep for time-constrained executives
**Audience**: Busy executives, VPs, directors with 5-10 minutes
**Tone**: Crisp, actionable, confidence-building
**Structure**: Highly scannable (tables, short paragraphs, numbered lists)

**Guidelines**:
1. **Every paragraph must earn its place** - ruthlessly cut fluff
2. **Lead with impact** - most important information first
3. **Use tables for quick reference** - stats, decision-makers, tech stack
4. **Number your hooks** - "Top 5 Conversation Hooks" not "Conversation Hooks"
5. **End with 3 specific next actions** - "Contact John Smith on LinkedIn" not "Reach out to leadership"
6. **Maximum 3 sentences per paragraph** - if longer, split it

**Opening Paragraph Formula**:
```
[Company Name], a [valuation] [industry] company, [key differentiator].
Founded in [year], they've raised [funding] and employ [count] people.
[One sentence explaining why they're a good prospect].
```

**Example Opening**:
```markdown
## 60-Second Overview

Cohere Health, a $5.5B healthcare AI company, automates prior authorization for health plans with 90% auto-approval rates and 93% provider satisfaction. Founded in 2019, they've raised $200M (most recent: $90M Series C in May 2025) and employ 800 people across 48 states. They're an ideal strategic account given their growth stage, technical sophistication (Python/PyTorch ML stack), and recent Microsoft partnership announcement.
```

---

### Standard Summary (4-6 pages)

**Purpose**: Comprehensive sales intelligence for discovery calls
**Audience**: Account executives, solutions architects with 20-30 minutes
**Tone**: Professional, thorough, strategically focused
**Structure**: Narrative sections with supporting data

**Guidelines**:
1. **Each section tells a mini-story** - beginning, middle, end
2. **Connect dots between sections** - "Given X funding, they're likely hiring for Y"
3. **Balance depth and readability** - 2-3 paragraphs per subsection maximum
4. **Include "So What?" statements** - translate facts into sales implications
5. **Provide engagement specifics** - not "contact CTO" but "contact Gus Weber (CTO, joined 2024, focus on infrastructure, LinkedIn: [URL])"
6. **End each major section with implications** - "What This Means for Your Approach"

**Section Transition Example**:
```markdown
...With this understanding of Cohere Health's business model and competitive position, we can now examine the leadership team responsible for executing this strategy.

## Team & Organizational Intelligence

Cohere Health's leadership team combines healthcare domain expertise with technology scaling experience. This blend is evident in the backgrounds of key executives: CEO Siva Namasivayam co-founded SCIO Health Analytics (healthcare analytics), CTO Gus Weber came from Fidelity's engineering organization (scaling expertise), and CFO Robert Shepardson joined from Amwell (healthcare tech + public company experience). Understanding each executive's background and priorities is essential for tailoring your engagement approach.
```

---

### Deep Dive Report (8-12 pages)

**Purpose**: Strategic account qualification and engagement planning
**Audience**: Sales teams, executive sponsors, deal strategists with 45-60 minutes
**Tone**: Analytical, comprehensive, decision-oriented
**Structure**: Research report format with strategic recommendations

**Guidelines**:
1. **Write like a strategy consultant** - comprehensive, analytical, data-driven
2. **Include framework thinking** - MEDDIC, BANT, competitive matrix
3. **Provide explicit recommendations** - "Pursue/Monitor/Disqualify" with rationale
4. **Show your work** - explain how you reached conclusions
5. **Address counterarguments** - "While X suggests opportunity, Y indicates risk..."
6. **Quantify when possible** - deal scores, confidence levels, time estimates
7. **Include executive summary** - 1 page that stands alone

**Analytical Narrative Example**:
```markdown
## Deal Qualification Analysis

Based on comprehensive intelligence gathering across 12 domains, this section assesses Cohere Health as a sales opportunity using the MEDDIC qualification framework. Overall qualification score: 62/80 (Strong Opportunity).

**Metrics** (10/10): Pain is well-quantified. Cohere Health processes 12M+ prior authorizations annually and recently hired 5 DevOps engineers specifically for "scaling infrastructure to handle increased request volume" per job postings. The Microsoft partnership announcement (October 2025) indicates point-of-care integration is a strategic priority. These facts suggest infrastructure scaling pain that can be quantified in terms of request volume, latency requirements, and cost.

**Economic Buyer** (8/10): CFO Robert Shepardson (joined October 2024) holds budget authority for technology purchases based on his role and prior CFO experience at Amwell. His background in healthcare tech M&A suggests familiarity with solution evaluation. Risk: He's new (4 months tenure), so procurement processes may still be establishing. Mitigation: Engage CTO Gus Weber simultaneously as technical buyer.

**Decision Criteria** (6/10): Not yet known. Must discover in discovery call. Likely criteria based on healthcare SaaS patterns: HIPAA compliance documentation, SOC 2 Type II certification, healthcare industry references, API integration ease, pricing model (PMPM compatible). Gap: Need to confirm actual evaluation criteria.

[Continue through all MEDDIC criteria...]

**Conclusion**: Score of 62/80 indicates Strong Opportunity warranting full resource allocation. Primary risks are (1) unknown decision criteria and (2) new CFO may cause longer sales cycle. Recommended next action: Discovery call with VP Engineering to validate pain points and uncover decision process.
```

---

## Language and Style Mechanics

### Sentence Construction

**Keep Sentences Crisp**:
- **Target**: 15-25 words per sentence average
- **Maximum**: 35 words (split if longer)
- **Vary length**: Mix short (5-10 words) and medium (15-25 words) for rhythm

**Example - Too Long** (48 words):
```markdown
Cohere Health, which was founded in 2019 in Boston, Massachusetts, has raised a total of $200M in funding across three rounds, including a recent $90M Series C led by Temasek in May 2025, and now employs approximately 800 people across 48 US states in a remote-first model.
```

**Example - Better** (Split into 3 sentences, average 16 words):
```markdown
Cohere Health was founded in 2019 in Boston, Massachusetts. The company has raised $200M across three funding rounds, most recently a $90M Series C led by Temasek in May 2025. Today, approximately 800 employees work remotely across 48 US states.
```

### Paragraph Construction

**The 1-3-1 Rule**:
- **1**: Topic sentence (what is this paragraph about?)
- **3**: Supporting sentences (evidence, context, details)
- **1**: Concluding sentence (so what? / transition)

**Example Paragraph**:
```markdown
Cohere Health's hiring patterns signal infrastructure scaling as a strategic priority [1 - Topic]. The company is actively recruiting for 5 DevOps/Infrastructure engineers, 3 backend engineers with Kubernetes experience, and 2 platform architects [2 - Evidence]. Job postings explicitly mention "scaling to process 15M+ requests by 2026" as a key challenge, up from 12M today [3 - Context]. Additionally, the recent hire of VP Engineering from Fidelity, where he led infrastructure scaling for millions of daily transactions, suggests leadership is investing in this capability [4 - Detail]. These hiring signals, combined with the Microsoft partnership for point-of-care integration, indicate this is an opportune time to engage with infrastructure solutions [5 - Conclusion].
```

### Word Choice

**Precision Over Jargon**:
| Avoid ❌ | Use ✅ |
|---------|--------|
| "Leverage" | "Use" |
| "Utilize" | "Use" |
| "Synergy" | "Collaboration" or "combined benefit" |
| "Impactful" | "Significant" or "meaningful" |
| "Solutions" (generic) | "API platform" or "monitoring tool" (specific) |
| "Best-in-class" | Name specific metric: "93% satisfaction vs industry average 70%" |
| "Leading" (generic) | "Ranks 3rd out of 41 competitors per CB Insights" |

**Confidence Modifiers** (use sparingly):

| Confidence Level | Appropriate Modifiers |
|------------------|----------------------|
| **High** (confirmed facts) | No modifier needed: "Cohere raised $90M" |
| **Medium** (strong inference) | "Likely", "Indicates", "Suggests" |
| **Low** (speculation) | "May", "Could", "Possibly" + "though not confirmed" |

**Example Confidence Calibration**:
```markdown
High Confidence: "Cohere Health employs approximately 800 people across 48 US states." [Source: LinkedIn, company announcements]

Medium Confidence: "The engineering team likely numbers 50-60 engineers, based on LinkedIn profile counts and job posting references to team sizes." [Source: LinkedIn headcount + job descriptions]

Low Confidence: "The company may be considering international expansion, given the recent hire of a VP of Global Operations, though no official announcement has been made." [Source: LinkedIn profile, no press release]
```

---

## Common Writing Pitfalls to Avoid

### 1. The "Bullet Point Dump"

**Problem**: Lists without context provide data but no understanding.

**Bad**:
```markdown
## Key Facts
- $200M funding
- 800 employees
- Healthcare tech
- Boston, MA
- Founded 2019
```

**Good**:
```markdown
## Company Overview

Cohere Health operates at significant scale in the healthcare technology sector. Founded in 2019 and headquartered in Boston, MA, the company has grown to 800 employees distributed across 48 US states in a remote-first model. This growth has been fueled by $200M in venture funding, most recently a $90M Series C in May 2025, positioning the company as a well-capitalized player in the prior authorization automation market.
```

### 2. The "Passive Voice Maze"

**Problem**: Unclear who did what, when, and why.

**Bad**:
```markdown
A partnership was announced that will enable ambient listening to be used for prior authorization. Integration is expected to occur throughout 2026.
```

**Good**:
```markdown
On October 17, 2025, Cohere Health announced a partnership with Microsoft's Dragon Copilot team. This partnership will enable providers using Dragon Copilot's ambient listening technology to automatically initiate prior authorization requests during patient visits. Cohere plans to complete the integration throughout 2026, with beta testing beginning in Q1 2026.
```

### 3. The "Generic Fluff"

**Problem**: Meaningless adjectives and empty praise.

**Bad**:
```markdown
Cohere Health is an innovative and cutting-edge leader in the rapidly evolving healthcare technology space, delivering world-class solutions that empower customers to achieve transformational outcomes.
```

**Good**:
```markdown
Cohere Health ranks 3rd out of 41 competitors in prior authorization technology according to CB Insights. The company differentiates on three metrics: 90% auto-approval rate (vs industry average 30-40%), 93% provider satisfaction (vs. 60-70%), and 47% reduction in administrative costs for customers like Geisinger Health Plan.
```

### 4. The "Buried Lede"

**Problem**: Most important information appears too late.

**Bad**:
```markdown
Cohere Health was founded in 2019 in Boston by Siva Namasivayam and Matt Manger. The company initially focused on utilization management. Over time, they expanded into prior authorization. They use artificial intelligence and machine learning. Recently, they announced a partnership.
```

**Good**:
```markdown
Cohere Health announced a major partnership with Microsoft on October 17, 2025, integrating AI-powered prior authorization into Dragon Copilot's ambient listening platform. This partnership represents a significant strategic move for the Boston-based company, which was founded in 2019 and has raised $200M to automate healthcare's prior authorization processes.
```

### 5. The "Unsupported Claim"

**Problem**: Assertions without evidence.

**Bad**:
```markdown
Cohere Health is desperately seeking infrastructure solutions and would be highly receptive to our outreach. Their engineering team is overwhelmed and needs help immediately.
```

**Good**:
```markdown
Several signals suggest infrastructure is a current priority for Cohere Health:
1. Five active DevOps/Infrastructure job postings mention "scaling to 15M+ requests" [1]
2. Recent hire of VP Engineering from Fidelity with infrastructure scaling background [2]
3. Engineering blog post discusses Kubernetes cost optimization challenges [3]
4. Microsoft partnership requires real-time API integration at point-of-care [4]

These facts indicate infrastructure investment, making this a potentially receptive time for related solutions. Receptivity should be validated in discovery call.
```

---

## Templates and Examples

### Template: Company Intelligence Opening

```markdown
## [Company Name] Overview

**Context for Sales**: [Why this company matters as a prospect - 1 sentence]

[Company Name], a [valuation/size] [industry] company, [key differentiator and market position - 2-3 sentences]. Founded in [year] in [location], the company has [funding amount] and employs [count] people [distribution details]. [One sentence on recent momentum - funding, partnership, product launch].

**Quick Qualification**: [2-3 sentences on fit - stage, technical profile, buying signals]

**Business Model**: [2-3 sentences on how they make money and who they serve]

[Then proceed to bulleted facts...]
```

### Template: Executive Profile

```markdown
### [Name] - [Full Title]

[Name] serves as [title] at [Company], where [his/her/their] focus areas include [3-4 key responsibilities]. [Name] joined [Company] in [month year] from [previous company], bringing [X years] of experience in [domain/industry].

**Background**: Prior to [Company], [Name] spent [duration] at [Previous Company] as [role], where [key achievement]. [Name] holds a [degree] from [institution] and has [additional credentials/achievements].

**Current Priorities** (based on public statements): [Name]'s recent [LinkedIn posts/interviews/blog articles] emphasize [priority 1], [priority 2], and [priority 3]. In an [month year] interview, [he/she/they] stated "[direct quote showing priorities or pain points]."

**Engagement Strategy**: Best reached via [LinkedIn/email/warm intro], ideally with an opening that references [recent achievement/post/shared interest]. [Name]'s communication style is [formal/casual/technical/business-focused] based on [LinkedIn posts/blog writing/conference talks].

**Key Facts**:
- **LinkedIn**: [URL]
- **Twitter/X**: [@handle] ([follower count])
- **Tenure**: [Duration] at [Company]
- **Location**: [City, State]
- **Recent Activity**: [Last significant post/announcement]
```

### Template: Section Transitions

**Pattern**: Summarize previous section + preview next section

```markdown
...[End of previous section]

Having established [Company]'s [topic from previous section], we can now examine [topic of next section], which [why it matters / how it connects].

## [Next Section Title]

[Opening paragraph of next section...]
```

### Template: "So What?" Implications

**Pattern**: State facts, then translate to sales implications

```markdown
**Sales Implications**:
- **[Implication Category]**: [Specific takeaway for sales]
- **[Implication Category]**: [Specific takeaway for sales]
- **[Implication Category]**: [Specific takeaway for sales]
```

**Example**:
```markdown
**Sales Implications**:
- **Timing**: Recent $90M funding (May 2025) means capital is available; buying window is open
- **Decision-Maker**: New CFO (Robert Shepardson, joined Oct 2024) may be establishing vendor relationships
- **Pain Point**: 5 open DevOps roles and Microsoft integration project suggest infrastructure scaling priority
- **Approach**: Lead with healthcare compliance credentials (HIPAA, SOC 2) given their industry focus
```

---

## Editing Checklist

Before submitting any intelligence report or summary, verify:

### Content Quality
- [ ] Every fact has a citation with full URL
- [ ] Confidence levels are appropriate (confirmed vs inferred vs speculative)
- [ ] No unsupported opinions or speculation presented as fact
- [ ] Specific numbers, names, and dates used (not vague language)
- [ ] Each section answers "So what?" for the reader

### Narrative Structure
- [ ] Opening paragraph answers "Why does the reader need this?"
- [ ] Each section has a clear topic sentence
- [ ] Transitions connect sections logically
- [ ] Conclusion or implications section provides actionable insights
- [ ] Sections follow Context → Current State → Implications pattern

### Writing Mechanics
- [ ] Active voice used (except where passive is clearly better)
- [ ] Complete sentences (not fragments or run-ons)
- [ ] Average sentence length 15-25 words
- [ ] Paragraphs are 3-5 sentences (not walls of text)
- [ ] No jargon without definition
- [ ] No clichés or empty modifiers ("world-class", "cutting-edge")

### Formatting
- [ ] Headers create clear hierarchy (H2 for main sections, H3 for subsections)
- [ ] Bullets used for lists of facts (not for narrative content)
- [ ] Tables used for comparative data or quick reference
- [ ] Bold used sparingly for emphasis (names, key metrics)
- [ ] Whitespace provides breathing room (paragraph breaks, section breaks)

### Sales Context
- [ ] Decision-makers identified by name and title
- [ ] Pain points connected to evidence (hiring, press releases, posts)
- [ ] Timing signals noted (funding, launches, leadership changes)
- [ ] Engagement approach specified (who to contact, how, with what message)
- [ ] Competitive context provided (who else they might be evaluating)

---

## Examples of Amazon-Style Narratives in Our Context

### Example 1: Funding Round Analysis

**Instead of**:
```markdown
## Funding
- Series C: $90M
- Led by Temasek
- May 2025
```

**Write**:
```markdown
## Funding & Financial Health

On May 14, 2025, Cohere Health closed a $90M Series C funding round led by Temasek, with participation from all existing investors including Deerfield Management, Define Ventures, Flare Capital Partners, Longitude Capital, and Polaris Partners. This round brings total funding to $200M and values the company at $5.5B.

The significance of this funding extends beyond the dollar amount. First, the participation of all existing investors signals confidence from those with the deepest company knowledge. Second, Temasek's lead position brings strategic value: Temasek, a Singapore-based global investment firm, has deep healthcare and technology portfolios and can facilitate international expansion. Third, the timing—coming just 15 months after the $50M Series B—suggests accelerated growth requiring capital ahead of schedule.

Company statements indicate the funding will support three priorities: scaling the Cohere Unify™ platform, expanding into new clinical use cases beyond prior authorization, and deepening investment in AI-powered products. These priorities align with recent actions: the September 2025 acquisition of ZignaAI (payment integrity), the October 2025 Microsoft partnership (point-of-care automation), and active hiring for 25+ positions including 8 ML engineers.

**Sales Implications**: With $90M recently raised, capital constraints are not a barrier to purchases. CFO Robert Shepardson (joined October 2024) will likely be establishing vendor relationships and may be receptive to new solutions. However, with clear stated priorities (platform scaling, new use cases, AI investment), positioning your solution as aligned with these areas will be critical for mindshare and budget allocation.
```

### Example 2: Leadership Change Analysis

**Instead of**:
```markdown
## CFO
- Robert Shepardson
- Joined Oct 2024
- Previously Amwell CFO
```

**Write**:
```markdown
## CFO Transition: Robert Shepardson's Arrival

In October 2024, Cohere Health brought on Robert Shepardson as CFO, a strategic hire that signals preparation for increased scale and potential public market readiness. Shepardson brings 30+ years of experience from Morgan Stanley, where he led healthcare IPOs for Amwell, One Medical, Accolade, Oak Street Health, Certara, Alignment Healthcare, and Lifestance Health. Most recently, he served as CFO of Amwell from 2021-2024, overseeing the public company's financial operations, M&A activities, and investor relations.

Shepardson's hire at this stage (post-Series C, $200M raised, $5.5B valuation) suggests two possibilities: preparing for eventual IPO or M&A exit, or positioning for operational maturity and financial discipline as the company scales. His background in healthcare specifically—not just tech—indicates the company values deep domain expertise in healthcare economics, reimbursement models, and regulatory considerations.

For vendor relationships, Shepardson's relative newness (4 months tenure as of February 2025) presents both opportunity and challenge. As CFO, he controls technology spending budgets, but he's still establishing processes, vendor relationships, and priorities. His previous role at Amwell means he's familiar with healthcare SaaS economics, technology evaluations, and likely has established relationships with certain vendors.

**Engagement Strategy**: When engaging, acknowledge his healthcare background ("Given your experience at Amwell with [specific initiative]...") and frame solutions in terms of financial impact (cost reduction, efficiency gains, revenue enablement) rather than purely technical benefits. His Morgan Stanley background suggests comfort with detailed financial modeling; come prepared with ROI calculators and reference customer economics.
```

### Example 3: Competitive Positioning

**Instead of**:
```markdown
## Competitors
- Itiliti Health
- Waystar
- EviCore
- Ranks #3 out of 41
```

**Write**:
```markdown
## Competitive Position & Differentiation Strategy

Cohere Health operates in a crowded market of 41 prior authorization technology vendors but has established itself as a top-three player according to CB Insights. Understanding how Cohere positions itself relative to competitors reveals both their strengths and the decision criteria they prioritize with their customers—insights valuable for your own positioning.

**Primary Competitors**: The closest competitive set includes Itiliti Health (utilization management platform), Waystar (revenue cycle management with prior auth module), and EviCore (prior authorization outsourcing service). While all address prior authorization, their approaches differ fundamentally: Itiliti and Waystar are software platforms like Cohere, while EviCore is a BPO (business process outsourcing) service that takes over prior auth operations entirely.

**Cohere's Differentiation Narrative** (in their own words): The company emphasizes three key differentiators:

1. **AI Automation Rate**: Cohere claims 90% auto-approval rates versus industry average of 30-40%. They back this with customer data: Geisinger Health Plan reports 47% reduction in administrative costs.

2. **Provider Satisfaction**: 93% provider satisfaction score versus industry average of 60-70%. This metric matters because prior authorization is notoriously frustrating for providers; Cohere positions itself as "fixing" the provider experience, not just automating plan processes.

3. **API-First Architecture**: Cohere Connect™ provides comprehensive APIs for EHR integration, CMS-0057-F compliance, and third-party workflows. Competitors often offer proprietary portals requiring manual data entry; Cohere positions its open API approach as more scalable and less disruptive.

**What This Means for Your Positioning**: When Cohere evaluates your solution, expect them to apply similar criteria: (1) measurable automation/efficiency metrics, (2) user experience quality for their end users (clinicians), and (3) API/integration architecture. They will likely be skeptical of solutions requiring manual processes or proprietary portals, given their own product philosophy.
```

---

## Final Principles

1. **Write for a Skeptical Reader**: Assume the reader will question unsupported claims. Provide evidence preemptively.

2. **Edit Ruthlessly**: First draft is always too long. Cut 20-30% on second pass. If it doesn't add value, delete it.

3. **Respect the Reader's Time**: Every sentence should either inform, provide context, or drive action. No filler.

4. **Show, Don't Tell**: Instead of "Cohere is growing fast," write "Cohere grew from 400 to 800 employees in 18 months (100% headcount growth)."

5. **Link Intelligence to Action**: Every fact should connect to "So what does this mean for how I sell?"

6. **Maintain Objectivity**: You're an intelligence reporter, not an advocate. Present facts and let readers draw conclusions.

---

**Last Updated**: November 2, 2025
**Next Review**: Quarterly or when Amazon updates their narrative memo guidance
**Feedback**: Submit writing samples and questions to improve this guide

**Reference**: Amazon's "Working Backwards" approach, "Writing Narrative Memos" by Jeff Bezos, Amazon Leadership Principles (especially "Earn Trust" and "Have Backbone; Disagree and Commit")
