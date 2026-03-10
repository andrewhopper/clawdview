---
description: Infer target audience/personas from context (price, industry, location, brands)
version: 1.0.0
---

# Infer Audience

Proactively infer target audience demographics and personas from contextual signals. **Everything we build is for a human with an intent** - this command ensures we identify WHO before proceeding.

## Arguments

```
$ARGUMENTS = Context to analyze (product description, price range, industry, etc.)
             OR path to .project / BUSINESS_CONTEXT.md file
```

## Philosophy

> "When someone says 'build a website for my boat dealer', the AI should say:
> 'Based on $75k-$200k boats and premium brands, your market is likely
> affluent buyers aged 45-65. Sound right?'"

**NEVER:**
- Mark demographics as "TBD" or "All audiences"
- Wait passively for user to define personas
- Proceed without validating WHO the end user is

**ALWAYS:**
- Infer from available signals
- Present hypothesis with evidence
- Ask for confirmation before proceeding

## Inference Signals

### Price Point Signals

| Price Range | Likely Demographics |
|-------------|---------------------|
| $0-50 | Mass market, price-sensitive, 18-35 |
| $50-500 | Middle market, value-conscious, 25-55 |
| $500-5k | Considered purchase, 30-60, research-heavy |
| $5k-50k | High-value, 35-65, spouse/family involved |
| $50k-500k | Affluent, 45-70, wealth advisors involved |
| $500k+ | Ultra-high-net-worth, 50+, trust/estate planning |

### Industry Signals

| Industry | Typical Buyer Profile |
|----------|----------------------|
| Boats/Marine | 45-70, $200k+ HHI, second home owners, relationship buyers |
| Luxury Auto | 35-65, status-conscious, brand loyal, lease vs buy split |
| Home Services | Homeowners 35-70, dual-income, time-poor |
| B2B SaaS | Decision-makers 30-55, ROI-focused, committee buying |
| E-commerce | Varies by product, impulse vs considered |
| Healthcare | 40-75 for self, 35-55 for family decisions |
| Financial Services | 35-65, life-event triggered, trust-dependent |
| Education | Parents 35-55, students 18-25, career-changers 30-50 |

### Location Signals

| Location Type | Demographic Indicators |
|---------------|------------------------|
| Newport Beach, Hamptons, Aspen | Ultra-affluent, 45+, second/third home |
| Lake communities | Upper-middle to affluent, 45-70, family-oriented |
| Urban cores | Younger, 25-45, convenience-focused |
| Suburban | Families, 30-55, space/school-focused |
| Rural | Older, 45+, value/durability-focused |

### Brand Signals

| Brand Tier | Audience Inference |
|------------|-------------------|
| Premium/Luxury (Boston Whaler, BMW, Rolex) | Affluent, brand-aware, quality > price |
| Aspirational (Coach, Lexus, Ray-Ban) | Upper-middle, status-seeking, stretch purchase |
| Value (Toyota, IKEA, Costco) | Middle market, practical, value-conscious |
| Budget (Walmart, Kia, Timex) | Price-sensitive, function > form |

## Instructions

### Step 1: Gather Context

If `$ARGUMENTS` is a file path:
```bash
# Read project context
cat "$ARGUMENTS"
```

If `$ARGUMENTS` is text, extract:
- Product/service type
- Price points mentioned
- Brands mentioned
- Locations mentioned
- Industry signals

### Step 2: Apply Inference Rules

Cross-reference signals to build hypothesis:

```python
signals = {
    "price_range": extract_price_range(context),
    "industry": detect_industry(context),
    "locations": extract_locations(context),
    "brands": extract_brands(context),
    "product_type": detect_product_type(context)
}

# Weight signals by confidence
primary_persona = infer_from_signals(signals)
secondary_persona = infer_secondary(signals)
```

### Step 3: Present Hypothesis

Format output as conversational confirmation:

```markdown
## Audience Inference

Based on your context:
- **Price range:** $75,000 - $200,000 (high-value considered purchase)
- **Industry:** Marine/recreational vehicles
- **Brands:** Boston Whaler, MasterCraft (premium positioning)
- **Locations:** Lake Winnipesaukee, Newport Beach (affluent areas)

### Primary Persona: "Lake House Larry"

| Attribute | Inference | Confidence |
|-----------|-----------|------------|
| **Age** | 45-65 | HIGH |
| **Household Income** | $250,000+ | HIGH |
| **Lifecycle** | Empty nester or near-empty | MEDIUM |
| **Decision Style** | Research-heavy, spouse-involved | HIGH |
| **Values** | Quality, heritage, service relationship | HIGH |
| **Purchase Trigger** | Life event (retirement, bonus, home sale) | MEDIUM |

**Behavioral traits:**
- Visits dealership 3-5 times before purchase
- Researches online extensively (6+ months)
- Values long-term service relationship
- Influenced by peer recommendations
- Willing to travel for right boat/dealer

### Secondary Persona: "Aspirational Alex"

| Attribute | Inference | Confidence |
|-----------|-----------|------------|
| **Age** | 35-45 | MEDIUM |
| **Household Income** | $150,000-250,000 | MEDIUM |
| **Lifecycle** | Young family, career ascending | MEDIUM |
| **Decision Style** | Financing-focused, feature comparison | HIGH |
| **Values** | Family experiences, status, value | MEDIUM |

---

**Does this match your understanding of your customers?**

Options:
1. **Yes, proceed** - Use these personas for design decisions
2. **Adjust primary** - Modify age, income, or traits
3. **Different audience** - Describe your actual customers
4. **Add persona** - Include another segment

Select: _
```

### Step 4: Wait for Confirmation

**STOP and wait for user response.**

Do NOT proceed with design, content, or UX decisions until personas are validated.

### Step 5: Document Validated Personas

After confirmation, update project files:

```markdown
# Update BUSINESS_CONTEXT.md or .project

### 3.1 Demographics (AI-Inferred, Human-Validated)
- **Primary Age:** 45-65
- **Income:** $250,000+ HHI
- **Lifecycle:** Empty nester / near-empty nester
- **Geography:** Lake communities, coastal affluent areas
- **Validation:** Confirmed by [user] on [date]

### 3.2 Buyer Personas

#### Primary: "Lake House Larry" (70% of sales)
[Full persona details...]

#### Secondary: "Aspirational Alex" (25% of sales)
[Full persona details...]

#### Tertiary: [If applicable] (5% of sales)
[...]
```

## Integration with SDLC

| Phase | /infer-audience Role |
|-------|---------------------|
| Phase 1 (Seed) | Optional - early hypothesis |
| Phase 2 (Research) | **REQUIRED** - validate before expansion |
| Phase 3 (Expansion) | Refine based on research |
| Phase 5.5 (PRD) | Embed in requirements |
| Phase 6 (Design) | Guide UX decisions |
| Phase 8.5 (QA) | Validate against persona needs |

## Examples

### Example 1: Boat Dealer

**Input:**
```
/infer-audience Boat dealer website, $75k-$200k inventory,
Boston Whaler and MasterCraft, Lake Winnipesaukee NH
```

**Output:**
```
Based on premium boat brands ($75k-$200k) in an affluent lake
community, your primary market is likely:

  Age: 45-65 (peak wealth, kids leaving home)
  Income: $250k+ household
  Lifestyle: Second home / lake house owners
  Values: Quality, heritage, dealer relationship

Sound right? [Y/n/adjust]
```

### Example 2: SaaS Product

**Input:**
```
/infer-audience B2B expense management software, $500/mo,
targeting finance teams at mid-market companies
```

**Output:**
```
Based on B2B SaaS pricing ($500/mo = $6k ARR) targeting
mid-market finance teams:

  Decision Maker: CFO or VP Finance, 40-55
  Company Size: 100-1000 employees
  Pain Points: Manual processes, audit prep, policy compliance
  Buying Cycle: 3-6 months, committee decision
  Triggers: Audit findings, growth/scaling, new CFO

Sound right? [Y/n/adjust]
```

### Example 3: Consumer App

**Input:**
```
/infer-audience Fitness app with AI coaching,
$20/month subscription, focus on busy professionals
```

**Output:**
```
Based on premium fitness subscription ($20/mo) for
busy professionals:

  Age: 28-45
  Income: $75k-150k
  Lifestyle: Time-poor, health-conscious, tech-comfortable
  Values: Efficiency, results, personalization
  Competitors they've tried: Peloton, Noom, MyFitnessPal

Sound right? [Y/n/adjust]
```

## Error Handling

**Insufficient context:**
```
I don't have enough signals to infer your audience.
Please provide:
- Price range or pricing model
- Industry or product type
- Target geography (if relevant)
- Competitor brands (if known)
```

**Conflicting signals:**
```
I'm seeing mixed signals:
- Price suggests affluent ($100k+)
- But location suggests mass market

Which is more accurate for your target?
1. Premium positioning (fewer, higher-value customers)
2. Mass market (volume-focused, lower prices)
3. Mixed (different tiers/products)
```

## Quality Checklist

Before marking personas complete:
- [ ] Price range analyzed
- [ ] Industry signals applied
- [ ] Location context considered
- [ ] Brand positioning factored
- [ ] Primary persona defined with confidence levels
- [ ] Secondary persona identified (if applicable)
- [ ] User confirmed/adjusted inference
- [ ] BUSINESS_CONTEXT.md updated with validated personas

## Notes

- Confidence levels (HIGH/MEDIUM/LOW) indicate inference strength
- Always present as hypothesis, not fact
- User validation is REQUIRED before proceeding
- Update personas as new information emerges
- Link personas to design decisions throughout SDLC
