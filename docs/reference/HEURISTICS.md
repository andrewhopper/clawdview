# Development Heuristics

**Purpose:** Evidence-based best practices extracted from successful prototype development sessions.

**Last Updated:** 2025-11-20

---

## 🚨 CRITICAL HEURISTICS (Always Apply)

### 1. Strong Typing in Scripts
**Rule:** ALWAYS use strong typing in all scripts and code.

**Application:**
- TypeScript: Use explicit types, avoid `any`
- Python: Use type hints (e.g., `def process(data: dict[str, str]) -> list[int]:`)
- JavaScript: Prefer TypeScript
- BAML/Pydantic: Always use structured schemas

**Rationale:** Strong typing catches errors at development time, improves IDE support, and serves as documentation.

**Examples:**
```python
# ❌ Bad
def validate_loan(bundle, requirements):
    return check_docs(bundle, requirements)

# ✅ Good
def validate_loan(
    bundle: LoanBundle,
    requirements: list[DocumentType]
) -> ValidationResult:
    return check_docs(bundle, requirements)
```

```typescript
// ❌ Bad
function mapSchema(input, target) {
    return input.map(field => match(field, target))
}

// ✅ Good
function mapSchema(
    input: SchemaField[],
    target: SemanticLayer
): MappingResult[] {
    return input.map(field => match(field, target))
}
```

---

### 2. Tool Selection Criteria
**Rule:** When selecting tools/libraries, ALWAYS evaluate:
1. **GitHub Stars** - Community adoption
2. **Date of Last Commit** - Active maintenance
3. **Number of Committers** - Bus factor / sustainability
4. **Download/Usage Stats** - Production readiness
5. **License** - Compatibility with project

**Decision Matrix:**
```
HIGH CONFIDENCE:
✅ 1000+ stars
✅ Last commit < 3 months ago
✅ 5+ active committers
✅ 10k+ weekly downloads

MEDIUM CONFIDENCE:
⚠️  500+ stars
⚠️  Last commit < 6 months ago
⚠️  3+ active committers
⚠️  5k+ weekly downloads

LOW CONFIDENCE (Require approval):
❌ < 500 stars
❌ Last commit > 6 months ago
❌ < 3 committers
❌ < 1k weekly downloads
```

**Where to Check:**
- **GitHub:** Stars, commits, contributors
- **npm:** `npm info <package>` - weekly downloads
- **PyPI:** Download stats on package page
- **GitHub Pulse:** Activity over last month

**Example Analysis:**
```
Evaluating: pydantic-ai vs langchain

pydantic-ai:
- Stars: 2.5k
- Last commit: 2 days ago
- Contributors: 12
- Weekly downloads: 15k
- Status: ✅ HIGH CONFIDENCE

langchain:
- Stars: 85k
- Last commit: 1 day ago
- Contributors: 1000+
- Weekly downloads: 500k
- Status: ✅ HIGH CONFIDENCE (but heavier)

Decision: pydantic-ai (lightweight, focused, sufficient)
```

---

## 💻 CODING HEURISTICS

### 3. Research-First Approach
**Rule:** ALWAYS research best practices and real-world examples BEFORE generating requirements or building.

**Process:**
1. **Web Search**: Find best practices, design patterns, industry standards
2. **Example Analysis**: Examine 3-5 best-in-class examples in the domain
3. **Document Findings**: Save insights in artifact generation guidance or notes
4. **Apply Learnings**: Use insights to inform requirements and design

**Application:**
- Building a website → Look at 5-10 best-in-class sites in that domain
- Creating an API → Research API design best practices (REST, GraphQL patterns)
- Implementing authentication → Study OAuth 2.0, JWT, industry standards
- Designing a form → Analyze UX patterns from leading companies
- Building payment flows → Examine Stripe, Square, PayPal integration patterns

**Example:**
```
User: "Build a landscaping website with a payment portal"

AI Process:
1. WebSearch: "best landscaping company websites 2025"
2. Analyze: 5 top sites (design, navigation, booking flows)
3. WebSearch: "payment portal best practices SaaS"
4. Analyze: Stripe, Square integration patterns
5. Document: Key findings (mobile-first, photo galleries, online booking, trust signals)
6. Generate: Requirements informed by real-world examples
7. Build: Implementation based on proven patterns
```

**Rationale:** Real-world examples reveal proven patterns, UX conventions, and technical approaches that theoretical knowledge might miss. Studying implementations that users already trust reduces risk and improves quality.

**Tools:**
- `WebSearch` - Find best practices and examples
- `WebFetch` - Analyze specific sites and documentation
- Artifact notes - Document key findings

---

### 4. Test-Driven Development
**Pattern:** Write tests BEFORE implementation (Phase 7 → Phase 8).

**Playwright Testing:**
- Run Playwright validation after EVERY major change
- Test visual appearance AND functionality
- Create E2E tests for critical workflows

**Quality Gate:** "Make sure it looks and works well"

**Frequency:** Every 3-4 changes requires testing checkpoint.

---

### 5. Progressive Enhancement
**Pattern:** Build incrementally in one of two strategies:

**Strategy A: Small → Large**
1. Core API/functionality
2. File handling/input validation
3. Web interface
4. AI integration
5. Sample data
6. Production fixes

**Strategy B: Large → Details**
1. Full system scaffold
2. Test infrastructure
3. Backend implementation
4. Sample data
5. Feature completion
6. UI polish

**Choose based on:**
- **Strategy A:** Unclear requirements, exploratory
- **Strategy B:** Clear vision, comprehensive initial spec

---

### 6. Real-World Focus
**Rule:** ALWAYS use production-ready configurations from the start.

**Requirements:**
- ✅ Real AWS credentials (when applicable)
- ✅ Production model IDs (exact versions)
- ✅ Realistic sample data
- ✅ Industry-standard file formats
- ❌ No mock data or placeholder IDs in prototypes

**Example:**
```python
# ❌ Bad - Placeholder
MODEL_ID = "claude-sonnet"

# ✅ Good - Production
MODEL_ID = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"
```

---

### 7. Sample Data Requirements
**Rule:** ALWAYS include both good AND bad examples.

**Structure:**
```
samples/
├── good/
│   ├── example-1-complete.pdf
│   ├── example-2-valid.json
│   └── example-3-correct.csv
└── bad/
    ├── example-1-missing-fields.pdf
    ├── example-2-invalid-format.json
    └── example-3-corrupt.csv
```

**Rationale:** Tests both happy path and error handling.

---

### 8. Visual Verification
**Rule:** ALWAYS verify outputs visually, not just programmatically.

**Methods:**
- "Open this" after deployment
- Playwright screenshot comparisons
- Manual inspection in browser
- IDE opening for code review

**Pattern:** Don't trust, verify visually.

---

### 9. Build → Test → Fix Cycle
**Iterative Pattern:**
```
1. Implementation
   ↓
2. Playwright validation ← Quality gate
   ↓
3. Issues discovered?
   ├─ Yes → Quick fix → Return to step 2
   └─ No → Enhancement request → Return to step 1
```

**Average Fix Time:** 5-10 minutes per issue
**Iteration Count:** 1-2 per issue

---

## 🏗️ ARCHITECTURE HEURISTICS

### 10. Technology Preferences (From Production Use)

**Testing:**
- **Prefer:** Playwright (E2E browser testing)
- **Avoid:** Pure unit tests without integration

**Frontend:**
- **Prefer:** React + Vite (modern, fast)
- **Consider:** Next.js (if SSR needed)
- **Avoid:** Angular, older frameworks

**Backend:**
- **Prefer:** FastAPI (Python, modern, fast)
- **Avoid:** Django (heavy), Flask (old patterns)

**AI Libraries:**
- **Prefer:** Pydantic AI, BAML (focused, structured)
- **Avoid:** LangChain (heavy), LlamaIndex (complex)

**Rationale:** Based on successful prototype delivery in <2 hours with comprehensive test coverage.

---

### 11. Three-Tier Inference Pattern
**Pattern:** For AI systems, implement fallback chain:

```
Tier 1: LLM Inference (AWS Bedrock)
   ↓ (if unavailable or low confidence)
Tier 2: Rule-Based Matching (deterministic)
   ↓ (if no exact match)
Tier 3: Fuzzy Matching (similarity scoring)
```

**Performance Metrics:**
- Rule-based: 54% high confidence, 12% medium, 34% low
- Coverage: 90+ pre-configured mappings

**Use Case:** Any system requiring high availability without constant LLM access.

---

### 12. Human-in-the-Loop (HITL)
**Pattern:** For mapping/classification tasks, ALWAYS include:
1. AI-generated suggestions
2. Confidence scores (0-100%)
3. UI for review/approval
4. Ability to reject and provide feedback
5. Learning from corrections

**UI Requirements:**
- Visual diff/comparison
- Clear confidence indicators
- One-click approve/reject
- Batch operations
- Export approved results

---

## 📝 COMMUNICATION HEURISTICS

### 13. Brevity and Density
**Rule:** Use 50% fewer words. High information density.

**Target:** 10-15 words per instruction (average)

**Structure:**
- Imperative mood: "Create", "Test", "Fix"
- No pleasantries: Skip "please", "thank you"
- Direct objects: "the backend", "the AI page"
- Context-dependent: Rely on shared understanding

**Example:**
```
❌ "Could you please test this with playwright and make sure everything is working well? Thank you!"
✅ "Test with playwright"
```

---

### 14. Problem-First Communication
**Pattern:** Only mention issues, silence = approval.

**Feedback Style:**
- Factual: "There's an issue using the model ID"
- Specific: Exact error messages
- Actionable: Clear what needs fixing
- No emotion: Pure technical feedback

**Implicit Approval:** Next instruction = previous task accepted.

---

### 15. Trust but Verify
**Delegation Pattern:**
- User provides: Goals, options, constraints
- AI chooses: Technologies, architecture, implementation
- User verifies: Outcomes, not methods

**What Gets Verified:**
✅ Visual appearance
✅ Functionality
✅ AI integration
✅ E2E workflows

**What Doesn't:**
❌ Code quality (trusted)
❌ Architecture decisions (delegated)
❌ File structure (assumed good)

---

## 🚀 PERFORMANCE HEURISTICS

### 16. Parallel Execution
**Rule:** When operations are independent, execute in parallel.

**Examples:**
```python
# ✅ Good - Parallel tool calls
await asyncio.gather(
    read_file("schema1.json"),
    read_file("schema2.json"),
    read_file("schema3.json")
)

# ❌ Bad - Sequential
result1 = await read_file("schema1.json")
result2 = await read_file("schema2.json")
result3 = await read_file("schema3.json")
```

**Application:** Read multiple files, run multiple tests, fetch multiple APIs simultaneously.

---

### 17. Rapid Recovery
**Pattern:** Issues should be resolved in 5-10 minutes.

**Process:**
1. Identify issue (Playwright test, visual inspection)
2. Report issue (factual, specific, actionable)
3. Fix within 5-10 minutes
4. Verify fix (re-run tests)
5. Move forward

**Success Rate Target:** 100% issues resolved within session.

---

## 🎯 QUALITY HEURISTICS

### 18. Quality Gates
**Checkpoints:**
- "Make sure it **looks** well" → Visual quality
- "Make sure it **works** well" → Functional quality
- Every 3-4 changes → Testing checkpoint
- Before deployment → Comprehensive validation

**Playwright Policy:** "Test with playwright every time you change"

---

### 19. Context Management
**Pattern:** Build shared context, use implicit references.

**Communication Style:**
- "this" → Current artifact
- "the backend" → Previously mentioned backend
- "the AI page" → Page discussed earlier
- "test this" → Current implementation

**Context Boundaries:** Provide summaries at context switches.

---

### 20. Multimodal AI Integration
**Pattern:** For document analysis, use multimodal capabilities.

**Implementation:**
- Read PDFs visually (not just text extraction)
- Analyze images, charts, tables
- Understand layout and structure
- Confidence scoring per element

**Use Cases:**
- Loan document validation
- Form processing
- Visual quality inspection
- Layout analysis

---

### 21. Iterative Refinement
**Pattern:** Build → Test → Fix → Enhance → Repeat

**Cycle Time:**
- Build: 10-20 minutes
- Test: 2-5 minutes
- Fix: 5-10 minutes
- Enhance: 5-15 minutes

**Total Prototype Time:** 55-75 minutes for production-ready prototype.

---

## 📊 METRICS AND TARGETS

### Development Velocity
- **Words per instruction:** 10-15 average
- **Messages per feature:** 30-45 messages
- **Test frequency:** Every 3-4 instructions
- **Fix time:** 5-10 minutes per issue
- **Prototype completion:** 1-2 hours

### Quality Metrics
- **Test coverage:** E2E + integration + unit
- **Sample data:** Good AND bad examples
- **Visual verification:** Always
- **Documentation:** Complete at delivery
- **Production readiness:** From first deployment

### Communication Efficiency
- **Information density:** High (50% fewer words)
- **Context references:** Heavy use of implicit context
- **Social padding:** None
- **Verification focus:** Outcomes, not methods

---

## 🔄 APPLICATION WORKFLOW

**Before Starting:**
1. Read CRITICAL_RULES.md
2. Read this HEURISTICS.md
3. Load phase-specific process file
4. Check hmode/guardrails/ for tech preferences

**During Development:**
1. Apply strong typing (#1)
2. Evaluate tools using criteria (#2)
3. Research best practices first (#3)
4. Write tests first (#4)
5. Use progressive enhancement (#5)
6. Include real data (#6)
7. Verify visually (#8)
8. Follow build-test-fix cycle (#9)

**At Quality Gates:**
1. Run Playwright tests (#4)
2. Visual verification (#8)
3. Check both good/bad examples (#7)
4. Review error handling
5. Validate production configs (#6)

**Before Delivery:**
1. Comprehensive testing
2. Sample data included
3. Documentation complete
4. Production model IDs
5. Visual polish

---

## 📚 EVIDENCE BASE

**Source:** Claude Code session analysis, November 10, 2025
- 2 production prototypes in 2 hours
- 88 total tests (all passing)
- 35 user instructions (432 total words)
- 100% issue resolution rate
- Production-ready on first deployment

**Key Observations:**
- Extreme brevity (12 words/instruction)
- Test-driven (Playwright 23% of instructions)
- Trust-based (outcomes verified, implementations delegated)
- Real-world focus (production IDs, AWS credentials)
- Rapid recovery (5-10 min/issue)

---

## 🎓 LESSONS LEARNED

**What Works:**
✅ Concise instructions with clear goals
✅ Progressive enhancement approach
✅ Frequent testing checkpoints
✅ Visual verification ("open this")
✅ Technology options vs. hard requirements
✅ Trust in implementation details

**What Doesn't:**
❌ Long explanatory instructions
❌ Micromanagement of implementation
❌ Mock data / placeholder configs
❌ Batch testing at the end
❌ Trusting without verifying

---

## 🔍 QUICK REFERENCE

**Before starting:**
→ Research best practices and examples (#3)
→ Analyze best-in-class implementations (#3)

**When selecting a tool:**
→ Check stars, last commit, committers (#2)

**When writing code:**
→ Use strong typing (#1)
→ Write tests first (#4)
→ Use real data (#6)

**When testing:**
→ Run Playwright after each change (#4)
→ Verify visually (#8)
→ Include good/bad examples (#7)

**When communicating:**
→ Use 50% fewer words (#13)
→ Only report issues (#14)
→ Next instruction = previous approved (#14)

**When architecting:**
→ Three-tier inference for reliability (#11)
→ HITL for mapping/classification (#12)
→ Prefer FastAPI, React, Playwright (#10)

**When creating domain models:**
→ Check schema.org first (#22)
→ Research top GitHub projects in that domain (#22)
→ Analyze provider APIs (Stripe, Twilio, etc.) (#22)

---

### 22. Domain Model Research Pattern
**Rule:** When creating a new domain model, ALWAYS research external sources for inspiration and industry standards.

**Research Sources (in order):**

1. **Schema.org** - Check for standard schemas
   - Visit schema.org/docs/schemas.html
   - Search for relevant types (e.g., Product, Order, Person)
   - Note standard properties and relationships

2. **Top GitHub Projects** - Analyze battle-tested domain models
   - Search: "[domain] open source" (e.g., "ecommerce open source")
   - Target: Projects with 10k+ stars, active maintenance
   - Examples by domain:
     | Domain | Reference Projects |
     |--------|-------------------|
     | E-commerce | Magento, Shopify themes, Medusa, Saleor |
     | CRM | SuiteCRM, EspoCRM, Monica |
     | Healthcare | OpenMRS, HAPI FHIR |
     | Finance | Firefly III, Akaunting |
     | Project Mgmt | Taiga, Plane, Focalboard |

3. **Industry Provider APIs** - Learn from market leaders
   - Examine their API schemas and entity relationships
   - Examples by domain:
     | Domain | Reference APIs |
     |--------|---------------|
     | Payments | Stripe, Square, PayPal |
     | Communications | Twilio, SendGrid, Mailgun |
     | E-commerce | Shopify Admin API, BigCommerce |
     | Auth | Auth0, Okta, Firebase Auth |
     | CRM | Salesforce, HubSpot |
     | Shipping | ShipStation, EasyPost |

**Process:**
```
1. Identify domain (e.g., "e-commerce")
2. WebSearch: "schema.org [domain] types"
3. WebSearch: "[domain] open source github stars:>10000"
4. WebSearch: "[top provider] API reference entities"
5. Document findings: key entities, relationships, enums
6. Synthesize: Create domain model informed by research
7. Present: Show research sources with proposed model
```

**Example Research Output:**
```markdown
## Domain Model Research: E-commerce

### Schema.org Findings
- Product: sku, name, description, price, availability
- Order: orderNumber, orderStatus, customer, orderedItem
- Offer: price, priceCurrency, availability, validFrom

### GitHub Project Analysis
- Magento (48k stars): Product → Category (many-to-many), Configurable Products
- Medusa (28k stars): Region-based pricing, Cart → LineItem pattern
- Saleor (21k stars): Variant model for product options

### Provider API Analysis
- Stripe: PaymentIntent → Charge → Refund lifecycle
- Shopify: Product → Variant → InventoryItem hierarchy

### Synthesized Entities
- Product (informed by schema.org + Magento)
- Variant (informed by Saleor + Shopify)
- Order (informed by schema.org + Stripe lifecycle)
```

**Rationale:** Industry-proven domain models have evolved through real-world usage. Leveraging existing schemas reduces design errors, improves interoperability, and follows established conventions developers expect.

---

**Version:** 1.1.0
**Status:** Active
**Evidence-Based:** Yes (November 2025 session logs)
