# ADR-0023: Adopt PostgreSQL for Primary Data Store

**Domain:** Software Engineering
**Artifact Type:** Architecture Decision Record (ADR)
**Harvested:** 2025-11-25
**Source Pattern:** [Michael Nygard's ADR Format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), [GitHub ADR Organization](https://adr.github.io/)

---

## Metadata

| Field | Value |
|-------|-------|
| **ADR Number** | ADR-0023 |
| **Title** | Adopt PostgreSQL for Primary Data Store |
| **Status** | Accepted |
| **Date** | 2025-11-15 |
| **Decision Makers** | @sarah-chen (Architect), @mike-torres (Eng Director) |
| **Consulted** | Platform Team, Data Team, Security |
| **Informed** | All Engineering |

---

## 1.0 Context

We are building a new order management system that requires:

- **ACID transactions** for financial data integrity
- **Complex queries** across multiple related entities (orders, items, customers, inventory)
- **Scalability** to 10,000 transactions/second within 2 years
- **High availability** (99.99% uptime SLA)
- **Compliance** with SOC 2 and PCI-DSS requirements

Currently, the team has experience with:
- MySQL (legacy systems)
- MongoDB (analytics pipeline)
- DynamoDB (real-time features)

The decision must be made now because:
1. Database schema design starts next sprint
2. Infrastructure provisioning requires 4-week lead time
3. Team training must be scheduled

---

## 2.0 Decision

**We will use PostgreSQL as the primary data store for the order management system.**

Specifically:
- **Version:** PostgreSQL 16 (latest stable)
- **Deployment:** Amazon RDS Multi-AZ with read replicas
- **Extensions:** pg_stat_statements, pgcrypto, PostGIS (if geo features needed)

---

## 3.0 Rationale

### 3.1 Options Considered

| Option | Description |
|--------|-------------|
| **PostgreSQL** | Open-source relational database with strong ACID guarantees |
| **MySQL 8** | Open-source relational, team has existing experience |
| **Amazon Aurora** | MySQL/PostgreSQL-compatible, AWS-managed |
| **CockroachDB** | Distributed SQL, strong consistency |
| **MongoDB** | Document store, flexible schema |

### 3.2 Evaluation Criteria

| Criteria | Weight | PostgreSQL | MySQL 8 | Aurora | CockroachDB | MongoDB |
|----------|--------|------------|---------|--------|-------------|---------|
| ACID compliance | 25% | ✅ 5 | ✅ 5 | ✅ 5 | ✅ 5 | ⚠️ 3 |
| Query complexity | 20% | ✅ 5 | ⚠️ 3 | ⚠️ 4 | ✅ 5 | ⚠️ 3 |
| Scalability | 20% | ⚠️ 4 | ⚠️ 3 | ✅ 5 | ✅ 5 | ✅ 5 |
| Operational cost | 15% | ✅ 5 | ✅ 5 | ⚠️ 3 | ❌ 2 | ⚠️ 4 |
| Team expertise | 10% | ⚠️ 3 | ✅ 5 | ⚠️ 3 | ❌ 1 | ⚠️ 4 |
| Ecosystem/tooling | 10% | ✅ 5 | ✅ 5 | ⚠️ 4 | ⚠️ 3 | ✅ 5 |
| **Weighted Score** | | **4.45** | **4.05** | **4.15** | **3.80** | **3.85** |

### 3.3 Why PostgreSQL

**Strongest fit for requirements:**

1. **Superior query capabilities**
   - CTEs, window functions, lateral joins
   - JSON/JSONB for semi-structured data
   - Full-text search built-in
   - Materialized views for complex reporting

2. **Proven scalability path**
   - Read replicas for query scaling
   - Connection pooling (PgBouncer)
   - Table partitioning for large datasets
   - Citus extension for horizontal scaling if needed

3. **Enterprise-grade reliability**
   - 25+ years of production hardening
   - Point-in-time recovery
   - Logical replication for zero-downtime migrations
   - Extensive monitoring capabilities

4. **Cost-effective**
   - Open-source (no license fees)
   - RDS pricing competitive
   - Large talent pool reduces hiring costs

### 3.4 Why Not Others

**MySQL 8:**
- Weaker window function support
- Less sophisticated query planner
- Replication historically less reliable

**Aurora:**
- 2-3x cost premium over standard RDS
- Vendor lock-in concerns
- Overkill for initial scale requirements

**CockroachDB:**
- Team has zero experience
- Higher operational complexity
- Premium pricing for enterprise features
- Better suited for global distribution (not our requirement)

**MongoDB:**
- Transactions added recently, less battle-tested
- Joins require application-level handling
- Schema flexibility not needed for this use case

---

## 4.0 Consequences

### 4.1 Positive

| Consequence | Impact |
|-------------|--------|
| Strong data integrity | Financial transactions protected by proven ACID |
| Query flexibility | Complex reporting without data warehouse initially |
| Talent availability | Large PostgreSQL community, easier hiring |
| Future optionality | Can migrate to Aurora PostgreSQL or Citus if needed |
| Tooling ecosystem | PgAdmin, DataGrip, extensive ORMs support |

### 4.2 Negative

| Consequence | Mitigation |
|-------------|------------|
| Team learning curve | Schedule 2-day PostgreSQL training |
| Single-node write scaling | Design for read replica offloading; Citus as escape hatch |
| No native multi-region | Use application-level routing; revisit in Year 2 |
| Migration from MySQL | Document MySQL → PostgreSQL differences for team |

### 4.3 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Performance issues at scale | Medium | High | Load testing at 2x projected volume |
| Operational incidents | Low | High | Runbooks, RDS monitoring, on-call training |
| Team resistance (MySQL preference) | Low | Medium | Involve team in decision, highlight benefits |

---

## 5.0 Implementation

### 5.1 Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Training | Week 1-2 | PostgreSQL fundamentals, query optimization |
| Infrastructure | Week 2-3 | RDS provisioning, security config, monitoring |
| Schema design | Week 3-5 | Data modeling, migration scripts |
| Integration | Week 5-8 | ORM setup, connection pooling, testing |

### 5.2 Technical Details

**RDS Configuration:**
```
Instance: db.r6g.xlarge (4 vCPU, 32GB RAM)
Storage: 500GB gp3, 3000 IOPS
Multi-AZ: Enabled
Read Replicas: 2 (scaling)
Backup: 7-day retention, daily snapshots
Encryption: AES-256 at rest, TLS in transit
```

**Connection Management:**
```
PgBouncer: Transaction pooling mode
Max connections: 200 (RDS) + 1000 (pooler)
Statement timeout: 30 seconds
Idle timeout: 5 minutes
```

### 5.3 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Query latency (p99) | <50ms | APM monitoring |
| Transaction throughput | 1000 TPS | Load testing |
| Availability | 99.99% | CloudWatch |
| Team proficiency | 100% trained | Training completion |

---

## 6.0 Compliance Notes

| Requirement | How PostgreSQL Addresses |
|-------------|-------------------------|
| **PCI-DSS** | Encryption at rest/transit, audit logging, access controls |
| **SOC 2** | RDS compliance inheritance, backup/recovery, monitoring |
| **GDPR** | Row-level security, data masking extensions, deletion support |

---

## 7.0 Related Decisions

| ADR | Relationship |
|-----|--------------|
| ADR-0018 | Caching strategy (Redis) — complements PostgreSQL for hot data |
| ADR-0021 | Event sourcing — PostgreSQL stores projections |
| ADR-0025 | Search infrastructure — may need Elasticsearch for full-text (future) |

---

## 8.0 References

- [PostgreSQL 16 Release Notes](https://www.postgresql.org/docs/16/release-16.html)
- [Amazon RDS for PostgreSQL](https://aws.amazon.com/rds/postgresql/)
- [High Performance PostgreSQL (book)](https://www.oreilly.com/library/view/high-performance-postgresql/9781492077411/)
- Internal: Database Selection Spike Report (Confluence)

---

## 9.0 Changelog

| Date | Author | Change |
|------|--------|--------|
| 2025-11-15 | @sarah-chen | Initial decision |
| 2025-11-18 | @mike-torres | Added compliance section |
| 2025-11-20 | @sarah-chen | Updated RDS configuration after sizing review |

---

## 10.0 Decision Record

**Status:** Accepted ✅

**Approved by:**
- Sarah Chen (Principal Architect) — 2025-11-15
- Mike Torres (Engineering Director) — 2025-11-15

**Supersedes:** None

**Superseded by:** None (current)

---

## Why This Is Best-in-Class

1. **Complete context:** Clear problem statement and constraints
2. **Structured evaluation:** Weighted scoring of alternatives
3. **Honest trade-offs:** Both positive and negative consequences
4. **Actionable implementation:** Timeline, configuration, success criteria
5. **Living document:** Changelog tracks evolution
6. **Connected:** Links to related decisions for context
7. **Compliance-aware:** Addresses regulatory requirements upfront
