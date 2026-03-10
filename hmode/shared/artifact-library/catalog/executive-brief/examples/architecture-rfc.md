# RFC: Event-Driven Architecture Migration

**Domain:** Software Engineering
**Artifact Type:** Architecture Proposal / RFC
**Harvested:** 2025-11-25
**Source Pattern:** [HashiCorp RFC Template](https://works.hashicorp.com/articles/rfc-template), [Pragmatic Engineer RFC Guide](https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design)

---

## Document Metadata

| Field | Value |
|-------|-------|
| **RFC Number** | RFC-2025-047 |
| **Title** | Event-Driven Architecture Migration for Order Processing |
| **Author** | Maria Santos (Staff Engineer) |
| **Status** | Proposed |
| **Created** | 2025-11-25 |
| **Decision Deadline** | 2025-12-09 |
| **Reviewers** | @platform-team, @order-team, @architecture-council |

---

## 1.0 Summary

**TL;DR:** Migrate order processing from synchronous REST calls to event-driven architecture using Apache Kafka, reducing system coupling, improving resilience, and enabling 10x throughput scaling.

**If you read nothing else:**
- Current architecture cannot scale beyond 500 orders/second
- Black Friday 2024 caused 3 outages, $2.1M revenue impact
- Proposed: Event-driven with Kafka, 6-month migration
- Investment: $840K (infra + eng time)
- ROI: $4.2M annually (avoided outages + reduced infra)

---

## 2.0 Background

### 2.1 Current Architecture

```
┌─────────┐    REST    ┌─────────┐    REST    ┌─────────┐
│   Web   │───────────▶│  Order  │───────────▶│Inventory│
│   App   │            │ Service │            │ Service │
└─────────┘            └────┬────┘            └─────────┘
                            │ REST
                            ▼
                       ┌─────────┐    REST    ┌─────────┐
                       │ Payment │───────────▶│  Email  │
                       │ Service │            │ Service │
                       └─────────┘            └─────────┘
```

**Problems with current state:**

| Issue | Impact | Frequency |
|-------|--------|-----------|
| Cascade failures | Full outage when any downstream fails | 12x/year |
| Retry storms | 10x load amplification during recovery | Every outage |
| Tight coupling | 6-week lead time for new integrations | Ongoing |
| Sync bottleneck | Max 500 orders/sec throughput | Peak periods |
| No replay | Lost orders require manual recovery | 3x/year |

### 2.2 Incident History (2024)

| Date | Duration | Root Cause | Revenue Impact |
|------|----------|------------|----------------|
| Mar 15 | 47 min | Payment service timeout cascade | $180K |
| Jul 4 | 2.1 hrs | Inventory DB connection exhaustion | $420K |
| Nov 29 | 3.8 hrs | Black Friday retry storm | $1.5M |

### 2.3 Business Context

- **Traffic growth:** 40% YoY, current architecture won't survive 2025 peak
- **New markets:** APAC expansion requires regional processing (Q3 2026)
- **Compliance:** PCI audit flagged synchronous payment retry patterns

---

## 3.0 Proposal

### 3.1 Target Architecture

```
┌─────────┐         ┌─────────────────────────────────────┐
│   Web   │────────▶│           Apache Kafka              │
│   App   │ produce │  ┌─────────────────────────────┐    │
└─────────┘         │  │     order-events topic      │    │
                    │  └──────────────┬──────────────┘    │
                    │                 │                    │
                    │    ┌────────────┼────────────┐      │
                    │    ▼            ▼            ▼      │
                    │ ┌──────┐  ┌─────────┐  ┌────────┐   │
                    │ │Order │  │Inventory│  │Payment │   │
                    │ │Worker│  │ Worker  │  │ Worker │   │
                    │ └──────┘  └─────────┘  └────────┘   │
                    │    │            │            │      │
                    │    ▼            ▼            ▼      │
                    │ ┌─────────────────────────────┐     │
                    │ │   order-completed topic     │     │
                    │ └──────────────┬──────────────┘     │
                    │                ▼                    │
                    │           ┌─────────┐              │
                    │           │  Email  │              │
                    │           │ Worker  │              │
                    │           └─────────┘              │
                    └─────────────────────────────────────┘
```

### 3.2 Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Message broker | Apache Kafka | Proven at scale, team expertise, replay capability |
| Schema registry | Confluent Schema Registry | Avro schemas, backward compatibility |
| Consumer pattern | Consumer groups | Horizontal scaling, automatic rebalancing |
| Ordering guarantee | Per-customer partitioning | Preserve order semantics where needed |
| Dead letter queue | Yes, per topic | Isolate poison messages, manual review |

### 3.3 Event Schema (Simplified)

```json
{
  "event_id": "uuid",
  "event_type": "OrderCreated | OrderPaid | OrderFulfilled",
  "event_time": "ISO-8601",
  "aggregate_id": "order-uuid",
  "aggregate_version": 1,
  "payload": {
    "customer_id": "string",
    "items": [...],
    "total_amount": 0.00,
    "currency": "USD"
  },
  "metadata": {
    "correlation_id": "uuid",
    "source_service": "string",
    "trace_id": "string"
  }
}
```

### 3.4 Migration Strategy

**Strangler Fig Pattern:** Run both architectures in parallel, gradually shift traffic.

| Phase | Scope | Duration | Rollback |
|-------|-------|----------|----------|
| 1. Foundation | Kafka cluster, schema registry, observability | 4 weeks | N/A |
| 2. Shadow mode | Dual-write to Kafka, verify parity | 4 weeks | Disable writes |
| 3. Inventory | Migrate inventory consumer | 3 weeks | Feature flag |
| 4. Payment | Migrate payment consumer | 4 weeks | Feature flag |
| 5. Email | Migrate email consumer | 2 weeks | Feature flag |
| 6. Cutover | Disable REST path, Kafka primary | 2 weeks | Re-enable REST |
| 7. Cleanup | Remove legacy code, optimize | 4 weeks | N/A |

---

## 4.0 Alternatives Considered

### 4.1 Alternative: AWS SQS + SNS

| Aspect | Kafka | SQS + SNS |
|--------|-------|-----------|
| Replay capability | ✅ Native | ❌ Requires S3 archive |
| Ordering | ✅ Per-partition | ⚠️ FIFO queues (limited) |
| Throughput | ✅ Millions/sec | ⚠️ 3K/sec per queue |
| Multi-consumer | ✅ Consumer groups | ⚠️ Fan-out complexity |
| Ops complexity | ⚠️ Self-managed | ✅ Fully managed |
| Cost at scale | ✅ Lower | ⚠️ Higher |

**Decision:** Kafka. Replay capability critical for debugging and recovery. Team has Kafka expertise from analytics pipeline.

### 4.2 Alternative: Synchronous with Circuit Breakers

Add circuit breakers and bulkheads to existing REST architecture.

**Rejected because:**
- Doesn't solve throughput ceiling (still sync)
- Doesn't enable replay/recovery
- Doesn't reduce coupling (still point-to-point)
- Band-aid, not solution

### 4.3 Alternative: gRPC Streaming

Replace REST with gRPC bidirectional streaming.

**Rejected because:**
- Still synchronous mental model
- No persistence/replay
- Doesn't solve cascade failures
- Higher learning curve, lower ecosystem support

---

## 5.0 Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Data loss during migration** | Medium | Critical | Shadow mode with verification, replay capability |
| **Kafka operational issues** | Medium | High | Runbook creation, on-call training, managed option backup |
| **Consumer lag causing delays** | Medium | Medium | Alerting, auto-scaling consumers, lag SLOs |
| **Schema evolution breaks** | Low | High | Schema registry, compatibility checks in CI |
| **Team unfamiliarity** | Medium | Medium | Training sessions, pairing, gradual rollout |
| **Cost overrun** | Low | Medium | Phased approach, checkpoint reviews |

### 5.1 Rollback Plan

Each phase has independent rollback:
1. **Shadow mode:** Disable Kafka writes, continue REST-only
2. **Per-consumer:** Feature flag to route back to REST
3. **Full rollback:** Re-enable REST path, disable Kafka consumers

Rollback decision criteria:
- Error rate >1% for >5 minutes
- P99 latency >2x baseline for >10 minutes
- Any data loss detected

---

## 6.0 Security Considerations

| Concern | Approach |
|---------|----------|
| Data in transit | TLS 1.3 for all Kafka connections |
| Data at rest | Encrypted EBS volumes |
| Authentication | mTLS for service-to-Kafka |
| Authorization | Kafka ACLs per topic per service |
| PII handling | Tokenize PII before publishing |
| Audit logging | All producer/consumer actions logged |

---

## 7.0 Observability

### 7.1 Metrics

| Metric | Alert Threshold |
|--------|-----------------|
| Consumer lag (per group) | >10K messages |
| Producer error rate | >0.1% |
| End-to-end latency (P99) | >5 seconds |
| DLQ message count | >100/hour |
| Kafka broker disk usage | >75% |

### 7.2 Dashboards

- Kafka cluster health (brokers, partitions, ISR)
- Per-topic throughput and latency
- Consumer group lag and rebalancing
- End-to-end order flow tracing
- DLQ monitoring and triage

### 7.3 Tracing

Correlation IDs propagated through all events, integrated with existing Datadog APM.

---

## 8.0 Resource Requirements

### 8.1 Infrastructure

| Component | Specification | Monthly Cost |
|-----------|---------------|--------------|
| Kafka cluster | 6 brokers, m5.2xlarge | $4,200 |
| Schema Registry | 3 nodes, m5.large | $420 |
| Kafka Connect | 4 workers, m5.xlarge | $1,120 |
| Additional storage | 10TB EBS | $800 |
| **Total** | | **$6,540/mo** |

### 8.2 Engineering Investment

| Phase | Team | Duration | Cost |
|-------|------|----------|------|
| Foundation | Platform (3 eng) | 4 weeks | $120K |
| Migration | Order team (4 eng) | 16 weeks | $320K |
| Testing/QA | QA (2 eng) | 8 weeks | $80K |
| Training | All teams | 2 weeks | $40K |
| **Total** | | | **$560K** |

### 8.3 Total Investment

| Category | Amount |
|----------|--------|
| Infrastructure (Year 1) | $78K |
| Engineering | $560K |
| Training & tooling | $42K |
| Contingency (20%) | $136K |
| **Total** | **$816K** |

---

## 9.0 Success Criteria

### 9.1 Technical Metrics

| Metric | Current | Target | Deadline |
|--------|---------|--------|----------|
| Throughput capacity | 500/sec | 5,000/sec | M+6 |
| Cascade failure incidents | 12/year | 0 | M+6 |
| Integration lead time | 6 weeks | 1 week | M+9 |
| Order recovery time | 4 hours | 5 minutes | M+6 |
| System availability | 99.5% | 99.95% | M+6 |

### 9.2 Business Metrics

| Metric | Target |
|--------|--------|
| Revenue loss from outages | <$100K/year |
| Peak season availability | 100% |
| New integration velocity | 4x improvement |

---

## 10.0 Timeline

```
2026
Jan     Feb     Mar     Apr     May     Jun     Jul
│       │       │       │       │       │       │
▼───────▼───────▼───────▼───────▼───────▼───────▼
│ Foundation    │ Shadow │ Inventory │Payment│Email│Cleanup│
│ (4 weeks)     │(4 wks) │ (3 weeks) │(4 wks)│(2wk)│(4 wks)│
└───────────────┴────────┴───────────┴───────┴─────┴───────┘
        ▲                ▲                   ▲       ▲
        │                │                   │       │
   Go/No-Go         Traffic shift       Cutover   Complete
   Decision         begins              complete
```

---

## 11.0 Open Questions

| Question | Owner | Due Date |
|----------|-------|----------|
| Managed Kafka (Confluent Cloud) vs. self-hosted? | Platform | Dec 2 |
| Exactly-once semantics required for payment? | Order Team | Dec 5 |
| Multi-region replication for APAC? | Architecture | Dec 9 |
| Schema evolution policy (forward vs. full)? | Platform | Dec 2 |

---

## 12.0 Appendices

- A: Detailed event schema specifications
- B: Kafka cluster sizing calculations
- C: Consumer implementation patterns
- D: Incident post-mortems (2024)
- E: Training plan outline

---

## 13.0 Decision

**Requested decision by:** December 9, 2025

**Decision maker:** @vp-engineering

**Options:**
1. ✅ Approve as proposed
2. ⚠️ Approve with modifications (specify)
3. ❌ Reject (provide alternative direction)
4. 🔄 Request more information (specify)

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2025-11-25 | Maria Santos | Initial draft |

---

## Why This Is Best-in-Class

1. **Clear structure:** Follows proven RFC format (HashiCorp/Squarespace patterns)
2. **Executive summary first:** Decision-makers can stop after Section 1
3. **Alternatives explored:** Shows due diligence, not just advocacy
4. **Quantified impact:** Specific metrics, costs, and timelines
5. **Risk transparency:** Explicit risks with mitigations and rollback plans
6. **Actionable decision:** Clear options and deadline for decision-maker
