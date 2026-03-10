# User Research Artifact SOP

## Purpose
Standard operating procedure for generating customer personas and research artifacts for web development consulting projects.

## When to Use
- Initial client discovery meeting
- Before designing/building a client website
- When validating target audience assumptions
- When testing website accessibility/usability

## Artifact Catalog

| Artifact | Purpose | When to Use |
|----------|---------|-------------|
| **Proto-Persona** | Demographics, goals, behaviors, accessibility | Always - foundation for all others |
| **Customer Profile (VPC)** | Jobs, Pains, Gains (Strategyzer) | Understanding customer motivations |
| **Empathy Map** | Says/Thinks/Does/Feels | Deep empathy building |
| **Jobs-to-Be-Done** | Functional/emotional/social jobs | Product/service positioning |
| **Accessibility Profile** | Detailed a11y simulation params | UX testing, inclusive design |

## Standard Flow

```
1. CLIENT INPUT
   ├─ Business name
   ├─ Business URL (if exists)
   ├─ Industry/vertical
   └─ Geographic focus

2. AI RESEARCH
   ├─ Analyze business website
   ├─ Research industry demographics
   ├─ Identify likely customer segments
   └─ Infer accessibility considerations

3. GENERATE ARTIFACTS (per segment)
   ├─ Proto-Persona (required)
   ├─ Customer Profile VPC (required)
   ├─ Empathy Map (recommended)
   ├─ JTBD Analysis (recommended)
   └─ Accessibility Profile (for simulation)

4. CLIENT REVIEW
   ├─ Present findings
   ├─ Client confirms/adjusts
   └─ Finalize personas

5. DESIGN APPLICATION
   ├─ Use personas to inform design decisions
   ├─ Run accessibility simulations
   └─ Validate against persona needs
```

## Artifact Generation Order

1. **Proto-Persona** — Always first, provides foundation
2. **Customer Profile (VPC)** — Jobs, Pains, Gains structure
3. **Accessibility Profile** — Extract from persona demographics
4. **Empathy Map** — Specific to a scenario/touchpoint
5. **JTBD** — Deep dive on hiring/firing criteria

## Minimum Viable Set

For quick client meetings, generate at minimum:
- 1-3 Proto-Personas (one per key segment)
- Customer Profile (VPC) for primary segment

## Artifact Locations

```
shared/artifact-library/catalog/user-research/
├── proto-persona.yaml
├── customer-profile-vpc.yaml
├── empathy-map.yaml
├── jobs-to-be-done.yaml
└── accessibility-profile.yaml
```

## Usage Example

**Input:**
```yaml
business_name: Goodhue Hawkins Boars
business_url: null  # No existing website
industry: Heritage livestock / small-scale agriculture
location: Rural Midwest
```

**Output Segments:**
1. Hobby Farmer (5-20 acres, supplemental income)
2. Commercial Breeder (50+ head operation)
3. Restaurant/Chef (farm-to-table sourcing)

**Artifacts per Segment:**
- Proto-Persona with accessibility traits
- Customer Profile (Jobs/Pains/Gains)
- Accessibility Profile for UX simulation

## Accessibility Simulation Usage

After generating personas, use Accessibility Profiles to:
1. Test website mockups against persona capabilities
2. Flag issues: contrast, font size, touch targets
3. Prioritize fixes based on persona demographics

**Example simulation check:**
```
Persona: Hobby Farmer Frank (age 55-65)
Issue: Body text at 14px
Recommendation: Increase to 18px minimum
Reason: Corrected vision + reduced contrast sensitivity
```

## Future Integration

Phase 2 of user-research-tool will:
1. Auto-simulate personas on actual websites
2. Generate UX issue reports per persona
3. Prioritize fixes by persona importance × issue severity

## References

- Cooper, A. (2004). *The Inmates Are Running the Asylum*
- Osterwalder, A. et al. (2014). *Value Proposition Design*
- Christensen, C. (2016). *Competing Against Luck*
- WCAG 2.1 Accessibility Guidelines
- Microsoft Inclusive Design Toolkit
