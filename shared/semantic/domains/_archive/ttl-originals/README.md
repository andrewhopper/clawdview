# Archived TTL Files

These Turtle/RDF ontology files have been converted to YAML format.

## Conversion Date
2025-11-22

## Reason for Conversion
- YAML is more developer-friendly and easier to read/write
- Better suited for code generation workflows
- Simpler tooling requirements (no RDF libraries needed)
- Easier integration with domain model generators

## Original Files

| Domain | Original File | Converted To |
|--------|---------------|--------------|
| core | core-ontology.ttl | core/schema.yaml |
| auth | auth-ontology.ttl | auth/schema.yaml |
| action | action-ontology.ttl | action/schema.yaml |
| email | email-ontology.ttl | email/schema.yaml |
| health | health-ontology.ttl | health/schema.yaml |
| intent | intent-ontology.ttl | intent/schema.yaml |
| sdlc | sdlc-ontology.ttl | sdlc/schema.yaml |
| story | story-ontology.ttl, story-rules.shacl.ttl | story/schema.yaml |
| tech-advisory | tech-advisory-ontology.ttl | tech-advisory/schema.yaml |
| tts | tts-ontology.ttl | tts/schema.yaml |

## Notes
- SHACL constraints have been converted to inline validation rules in YAML
- OWL inheritance (rdfs:subClassOf) converted to `extends` property
- RDF properties converted to entity properties with type annotations
- Enum instances converted to YAML enum values
