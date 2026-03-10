# Business Case: Electric Vehicle Battery Swapping Network

**Domain:** Automotive Industry
**Artifact Type:** Executive Business Case
**Harvested:** 2025-11-25
**Source Pattern:** [Center for Automotive Research Product Planning](https://www.cargroup.org/)

---

## Executive Summary

| Field | Value |
|-------|-------|
| **Project** | EV Battery Swapping Network (Project Volt-X) |
| **Sponsor** | VP, Electric Vehicle Strategy |
| **Investment** | $840M over 4 years |
| **Target Launch** | Q3 2027 (pilot), Q1 2028 (regional) |
| **NPV (10-year)** | $1.2B |
| **IRR** | 24% |
| **Payback** | 4.2 years |

---

## 1.0 Strategic Opportunity

### 1.1 Problem Statement

EV adoption is constrained by charging infrastructure limitations:

| Barrier | Impact | Current State |
|---------|--------|---------------|
| Charge time | 40% cite as adoption barrier | 30-60 min DC fast charge |
| Range anxiety | 33% cite as adoption barrier | 250-350 mi average range |
| Infrastructure gaps | 27% cite as adoption barrier | 48K public DC stations (US) |

Fleet operators face acute challenges:
- Lost revenue during charging (avg. $85/hour for delivery vehicles)
- Unpredictable charge times affecting scheduling
- Infrastructure investment competing with fleet expansion

### 1.2 Proposed Solution

Deploy a **standardized battery swapping network** enabling 3-5 minute battery exchanges for commercial EVs.

```
┌─────────────────────────────────────────────────────────────┐
│                     VOLT-X NETWORK                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐      ┌─────────────┐      ┌─────────────┐    │
│   │ Fleet   │      │   Swap      │      │  Battery    │    │
│   │ Vehicle │─────▶│   Station   │─────▶│  Cloud      │    │
│   │         │      │   (robotic) │      │  (SOC/SOH)  │    │
│   └─────────┘      └─────────────┘      └─────────────┘    │
│        │                  │                    │            │
│        │                  ▼                    │            │
│        │           ┌─────────────┐             │            │
│        │           │  Charging   │             │            │
│        └──────────▶│  Buffer     │◀────────────┘            │
│                    │  (off-peak) │                          │
│                    └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Value Proposition

| Stakeholder | Benefit |
|-------------|---------|
| **Fleet operators** | 90% reduction in charging downtime |
| **Our company** | New revenue stream ($45/swap), customer lock-in |
| **Grid operators** | Off-peak charging, load balancing capability |
| **Environment** | Extended battery life through optimal charging |

---

## 2.0 Market Analysis

### 2.1 Target Segments

| Segment | US Fleet Size | EV Penetration (2025) | Projected (2030) |
|---------|---------------|----------------------|------------------|
| Last-mile delivery | 420,000 | 8% | 45% |
| Ride-share | 180,000 | 12% | 55% |
| Taxi/Limo | 95,000 | 6% | 35% |
| **Total Addressable** | 695,000 | — | — |

### 2.2 Competitive Landscape

| Player | Model | Geography | Status |
|--------|-------|-----------|--------|
| NIO | Consumer swap | China | 2,400+ stations |
| Aulton | Commercial/consumer | China | 800+ stations |
| Gogoro | Scooter swap | Taiwan, global | 12,000+ stations |
| Ample | Modular swap | US (pilot) | 5 stations |

**Gap:** No scaled commercial vehicle swap network in North America.

### 2.3 Regulatory Tailwinds

- California Advanced Clean Fleets rule (2024): 100% ZEV by 2035
- EPA Phase 3 emissions standards (2024): 67% EV by 2032
- IRA commercial EV credit: Up to $40,000/vehicle

---

## 3.0 Technical Approach

### 3.1 Battery Standardization

| Specification | Value | Rationale |
|---------------|-------|-----------|
| Form factor | 800V modular | Compatibility with next-gen platforms |
| Capacity | 100 kWh (2 x 50 kWh modules) | Covers 200+ mi range classes |
| Connector | Proprietary + CCS adapter | Enable charging fallback |
| Weight | 450 kg per pack | Within swap robot capacity |

### 3.2 Station Design

| Component | Specification |
|-----------|---------------|
| Footprint | 2,500 sq ft (fits gas station lot) |
| Swap capacity | 120 swaps/day (24-hour operation) |
| Battery inventory | 20 packs per station |
| Swap time | 3-5 minutes |
| Automation | Fully robotic (no attendant) |

### 3.3 Development Timeline

| Phase | Duration | Milestone |
|-------|----------|-----------|
| Design & prototype | 12 months | Functional swap prototype |
| Pilot deployment | 12 months | 10 stations, 3 fleet partners |
| Regional scale | 18 months | 150 stations, Southwest US |
| National expansion | Ongoing | 500+ stations by 2030 |

---

## 4.0 Financial Analysis

### 4.1 Investment Requirements

| Category | Year 1 | Year 2 | Year 3 | Year 4 | Total |
|----------|--------|--------|--------|--------|-------|
| R&D | $120M | $60M | $20M | $10M | $210M |
| Station buildout | $40M | $180M | $220M | $80M | $520M |
| Battery inventory | $20M | $45M | $35M | $10M | $110M |
| **Total** | $180M | $285M | $275M | $100M | **$840M** |

### 4.2 Revenue Model

| Stream | Unit Economics | Year 5 Volume | Year 5 Revenue |
|--------|---------------|---------------|----------------|
| Swap fees | $45/swap | 8.2M swaps | $369M |
| Battery-as-a-Service | $400/mo | 12,000 vehicles | $58M |
| Grid services | $15/kWh arbitrage | 45 GWh | $675M* |
| **Total Year 5** | | | **$427M** |

*Grid services modeled conservatively at 10% of theoretical

### 4.3 Profitability Forecast

| Metric | Year 3 | Year 5 | Year 7 | Year 10 |
|--------|--------|--------|--------|---------|
| Revenue | $42M | $427M | $890M | $1.4B |
| Gross margin | 28% | 52% | 58% | 62% |
| EBITDA | -$85M | $142M | $380M | $620M |
| Cumulative FCF | -$580M | -$210M | $340M | $1.1B |

### 4.4 Return Metrics

| Metric | Value |
|--------|-------|
| NPV (10-year, 10% discount) | $1.2B |
| IRR | 24% |
| Payback period | 4.2 years |
| MOIC (10-year) | 3.8x |

---

## 5.0 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Battery standardization failure | Medium | High | Start with owned fleet, expand to partners |
| Competitor leapfrog | Medium | Medium | Patent portfolio, first-mover advantage |
| Regulatory headwinds | Low | High | Active policy engagement, state partnerships |
| Technology obsolescence | Medium | Medium | Modular design, upgrade paths |
| Fleet partner churn | Medium | Medium | Long-term contracts, captive economics |

### 5.1 Sensitivity Analysis

| Variable | Base Case | Downside | Upside |
|----------|-----------|----------|--------|
| Swap volume (Y5) | 8.2M | 5.5M | 11.0M |
| Swap price | $45 | $38 | $52 |
| Station cost | $2.8M | $3.4M | $2.2M |
| **NPV Impact** | $1.2B | $0.4B | $2.1B |

---

## 6.0 Strategic Alignment

### 6.1 Corporate Strategy Fit

| Strategic Priority | Project Contribution |
|--------------------|---------------------|
| EV leadership | Differentiated infrastructure offering |
| Fleet solutions | Comprehensive commercial EV ecosystem |
| Recurring revenue | $400/mo BaaS + swap fees |
| Sustainability | Battery life extension, grid integration |

### 6.2 Synergies

- **Vehicle design:** Influence next-gen commercial EV architecture
- **Energy division:** Grid services revenue opportunity
- **Dealer network:** Station co-location, service revenue

---

## 7.0 Recommendation

**Proceed with Phase 1 investment ($180M)** to complete R&D and deploy 10-station pilot network.

### 7.1 Go/No-Go Criteria for Phase 2

| Metric | Threshold |
|--------|-----------|
| Swap reliability | >99% success rate |
| Customer NPS | >50 |
| Unit economics | Positive station-level contribution |
| Partner commitments | 3+ fleets, 5,000+ vehicles |

### 7.2 Decision Timeline

| Milestone | Date |
|-----------|------|
| Board approval (Phase 1) | Q1 2026 |
| Pilot launch | Q3 2027 |
| Phase 2 decision | Q4 2027 |
| Regional rollout | Q1 2028 |

---

## 8.0 Appendices

- A: Detailed financial model
- B: Patent landscape analysis
- C: Fleet partner LOIs
- D: Regulatory analysis by state
- E: Competitive intelligence deck

---

## Why This Is Best-in-Class

1. **Automotive industry format:** Follows CAR product planning structure
2. **Clear strategic logic:** Problem → Solution → Value → Financials
3. **Quantified throughout:** Every claim supported by specific numbers
4. **Risk transparency:** Honest assessment with mitigations
5. **Stage-gated approach:** Clear decision points reduce commitment risk
6. **Visual architecture:** Diagrams clarify complex systems
