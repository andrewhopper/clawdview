# DOMAIN_NAME Domain Model

## Overview
DOMAIN_DESCRIPTION

## Usage

1. Copy this template:
   ```bash
   cp -r /shared/semantic/domains/_template /shared/semantic/domains/your-domain
   ```

2. Replace placeholders:
   - `DOMAIN_NAME` → your domain name (lowercase, hyphenated)
   - `DOMAIN_DESCRIPTION` → one-line description
   - `Entity1` → your first entity name

3. Define your entities in `ontology.ttl`

4. Add validation rules in `rules.shacl.ttl`

5. Update `version.json` with your entities and changelog

6. Generate types:
   ```bash
   cd /shared/semantic/tools/generator
   npm run generate -- --domain your-domain --lang typescript,python
   ```

7. Register in `/shared/semantic/domains/registry.yaml`

## Files

| File | Purpose |
|------|---------|
| `ontology.ttl` | RDF/OWL entity and action definitions |
| `rules.shacl.ttl` | SHACL validation constraints |
| `version.json` | Metadata and changelog |
| `generated/` | Auto-generated TypeScript/Python/Rust types |

## Standards

- W3C RDF (Resource Description Framework)
- W3C OWL (Web Ontology Language)
- W3C SHACL (Shapes Constraint Language)
