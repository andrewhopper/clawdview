# Stage 1 - Domain Model SEED: observation

**Generated:** 2025-11-25
**Status:** PENDING APPROVAL
**SDLC Phase:** 1 - SEED

---

## 1.1 Domain Need Capture

**Domain Name:** observation

**Purpose:** Track probabilistic observations and inferences about entities with confidence levels, differentiating between confirmed facts and uncertain inferences.

**Trigger:** Need to capture inferred information from various sources (e.g., social media activity, indirect signals) with varying degrees of certainty. For example: observing someone posts about golf on social media → save medium confidence inference that they like golf.

**Project Type:** [x] production

**Use Cases:**
1. **Social Media Intelligence:** Infer interests/preferences from social activity with confidence scores
2. **Lead Scoring:** Track probabilistic signals about prospects (e.g., job change, budget availability)
3. **Customer Insights:** Build probabilistic profiles from behavioral data
4. **Knowledge Graph:** Represent uncertain facts with confidence levels
5. **Evidence-Based Reasoning:** Track observations with supporting evidence

**Initial Entities (best guess):**
1. **Observation** - A fact or inference about an entity with confidence level
2. **Evidence** - Supporting data that backs up an observation
3. **ConfidenceScore** - Quantitative measure of certainty (0.0-1.0)
4. **Source** - Where the observation originated (social media, manual input, API, etc.)
5. **ObservationRevision** - Historical changes to confidence/evidence over time
6. **EntityProfile** - Collection of observations about a specific entity

**Key Characteristics:**
- Probabilistic vs. Confirmed: Differentiate between inferred facts (medium confidence) and verified facts (high/confirmed)
- Evidence-Based: Track supporting evidence that increases/decreases confidence
- Temporal: Observations can strengthen or weaken over time
- Composable: Multiple observations can combine to form higher-level inferences
- Auditable: Track who made the observation, when, and based on what evidence

**Differentiators from Existing Domains:**
- **vs. core.AuditInfo:** Not just tracking changes, but tracking probabilistic knowledge with confidence
- **vs. observer:** Observer validates AI outputs; this tracks uncertain observations about real-world entities
- **vs. llm-evaluation:** Not evaluating AI quality; tracking real-world observations with uncertainty

**Dependencies (anticipated):**
- `core` - Entity, Person, AuditInfo, TimePoint
- `auth` - User (who made the observation)

---

## 1.2 Initial Data Model Sketch

```yaml
# Preliminary sketch - NOT final design

entities:
  Observation:
    description: "A fact or inference about an entity with confidence level"
    properties:
      id: uuid
      subject_entity_id: uuid  # What entity is being observed
      subject_entity_type: string  # Person, Organization, etc.
      property_name: string  # What property (e.g., "interests.golf")
      property_value: any  # The observed value
      observation_type: enum  # DIRECT, INFERRED, AGGREGATED
      confidence_score: float  # 0.0-1.0
      confidence_category: enum  # LOW, MEDIUM, HIGH, CONFIRMED
      observed_at: datetime
      observed_by_id: uuid  # User who made/recorded observation
      source_id: uuid  # Where this came from
      evidence: Evidence[]
      created_at: datetime
      updated_at: datetime

  Evidence:
    description: "Supporting data for an observation"
    properties:
      id: uuid
      observation_id: uuid
      evidence_type: enum  # SOCIAL_POST, DIRECT_STATEMENT, THIRD_PARTY, etc.
      source_url: string?
      content_snippet: string?
      reliability_score: float  # How reliable is this evidence
      collected_at: datetime
      created_at: datetime
      updated_at: datetime

  Source:
    description: "Origin of an observation"
    properties:
      id: uuid
      source_type: enum  # SOCIAL_MEDIA, DIRECT_INPUT, API, SCRAPER, etc.
      source_name: string  # "LinkedIn", "Twitter", "Manual Entry"
      reliability_rating: float  # How reliable is this source generally
      created_at: datetime
      updated_at: datetime

  ObservationRevision:
    description: "Historical changes to observations"
    properties:
      id: uuid
      observation_id: uuid
      previous_confidence_score: float
      new_confidence_score: float
      reason: string
      revised_at: datetime
      revised_by_id: uuid
      created_at: datetime
      updated_at: datetime

enums:
  ObservationType:
    values:
      - DIRECT  # Directly observed/stated
      - INFERRED  # Inferred from indirect signals
      - AGGREGATED  # Derived from multiple observations
      - COMPUTED  # Calculated from other data

  ConfidenceCategory:
    values:
      - VERY_LOW  # 0.0-0.2
      - LOW  # 0.2-0.4
      - MEDIUM  # 0.4-0.6
      - HIGH  # 0.6-0.8
      - VERY_HIGH  # 0.8-0.95
      - CONFIRMED  # 0.95-1.0 (verified fact)

  EvidenceType:
    values:
      - SOCIAL_POST  # Social media post
      - PROFILE_DATA  # Profile information
      - DIRECT_STATEMENT  # Person explicitly stated
      - BEHAVIORAL_SIGNAL  # Observed behavior
      - THIRD_PARTY_REPORT  # Report from another source
      - DOCUMENT  # Supporting document
      - IMAGE  # Image evidence
      - VIDEO  # Video evidence

  SourceType:
    values:
      - SOCIAL_MEDIA  # LinkedIn, Twitter, etc.
      - DIRECT_INPUT  # Manual entry by user
      - API_INTEGRATION  # External API
      - WEB_SCRAPER  # Automated scraper
      - THIRD_PARTY_DATA  # Data provider
      - INTERNAL_SYSTEM  # Internal data source
```

---

## 1.3 Example Usage

**Scenario:** LinkedIn post about golf tournament

```typescript
// Someone posts about a golf tournament on LinkedIn
const observation = {
  subject_entity_id: "person-123",
  subject_entity_type: "Person",
  property_name: "interests.golf",
  property_value: true,
  observation_type: "INFERRED",
  confidence_score: 0.6,  // Medium confidence
  confidence_category: "MEDIUM",
  observed_at: "2025-11-25T10:00:00Z",
  observed_by_id: "system-ai-001",
  source_id: "linkedin-monitor",
  evidence: [
    {
      evidence_type: "SOCIAL_POST",
      source_url: "https://linkedin.com/posts/...",
      content_snippet: "Had a great time at the charity golf tournament!",
      reliability_score: 0.8,
      collected_at: "2025-11-25T10:00:00Z"
    }
  ]
}

// Later, they mention golf again → update confidence
const revision = {
  observation_id: observation.id,
  previous_confidence_score: 0.6,
  new_confidence_score: 0.75,  // Increased confidence
  reason: "Multiple mentions of golf across 3 posts",
  revised_at: "2025-12-01T14:00:00Z"
}
```

---

## ✅ APPROVAL GATE: Phase 1 → 2

**Domain:** observation
**Purpose:** Track probabilistic observations and inferences about entities with confidence levels

**Proceed to Research?**
- [Y] Yes, research existing standards and patterns
- [N] No, needs more clarification
- [R] Revise scope (provide feedback)

**Human response:** ___
