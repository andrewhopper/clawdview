---
uuid: cmd-densify-2l3m4n5o
version: 1.0.0
last_updated: 2025-11-10
description: Convert verbose text to high-density technical format
---

# Densify

Transform verbose documentation into compressed technical format while preserving semantic meaning and critical information.

## Compression Principles

**✅ Preserve:**
- Brand names (GitHub, AWS, Docker, PostgreSQL)
- Technical accuracy and specificity
- Domain-specific terminology
- Critical numbers, metrics, thresholds

**✅ Use tech forum conventions:**
- `postgres` not PostgreSQL
- `k8s` not Kubernetes
- `dynamo` not DynamoDB
- Lowercase for common tools

**✅ Compress:**
- Remove filler words (very, really, basically, essentially)
- Replace verbose phrases with arrows (→)
- Use bullets instead of prose
- Abbreviate predictable technical patterns
- Remove redundant explanations

**❌ Never:**
- Lose semantic meaning
- Remove critical constraints
- Abbreviate brand names
- Guess at unclear technical details

## Examples

**Architecture:**
- Input: "We need to implement a microservices architecture with an API gateway for routing, a service mesh for inter-service communication, and deploy everything to Kubernetes with Istio"
- Output: "Implement microservices with API gateway, service mesh, deploy to k8s+Istio"

**CI/CD:**
- Input: "Set up a continuous integration and continuous deployment pipeline using GitHub Actions that builds the Docker image, runs the test suite, and deploys to Amazon ECS"
- Output: "Setup CI/CD: GitHub Actions → build, test, deploy to AWS ECS"

**Database:**
- Input: "Create a PostgreSQL database with connection pooling, read replicas for scaling, and automated backup to S3 every 24 hours"
- Output: "Create postgres with pooling, read replicas, S3 backup (24h)"

## Instructions

1. **Read input text** provided by user
2. **Identify key information:**
   - Technical components
   - Brand names to preserve
   - Critical constraints/requirements
   - Numeric values and thresholds

3. **Apply compression:**
   - Convert prose → bullets
   - Replace verbose connectors with `→`
   - Use standard tech abbreviations
   - Remove predictable context

4. **Validate output:**
   - Semantic meaning preserved?
   - All critical details present?
   - Brand names intact?
   - Recoverability >95%?

5. **Present result:**
   ```
   **Original:** [length]
   **Compressed:** [length]
   **Reduction:** [percentage]%

   [Compressed output]
   ```

## Target Compression

Aim for 60-70% token reduction while maintaining >95% semantic recoverability.
