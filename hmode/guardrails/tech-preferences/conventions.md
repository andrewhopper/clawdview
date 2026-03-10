# Development Conventions

**Standard operating procedures for naming, identifiers, and project organization**

---

## UUID Generation

### OpenSSL Hex Format (Standard)

**Command:**
```bash
openssl rand -hex 4
```

**Output:** 8-character hexadecimal string (e.g., `f3f4f4fc`, `k7m3p-066`)

**Use Cases:**
- Topic/content identifiers: `notes/future-it-ai-{uuid}/`
- Project IDs: `{name}-{5char-id}`
- Unique folder names requiring collision resistance

**Examples:**
```
notes/future-it-ai-f3f4f4fc/
content/draft/architecture-redesign-a1b2c3d4/
bedrock-integration-k7m3p/
```

**Rationale:**
- Cryptographically random (collision resistant)
- Short enough for human readability (8 chars)
- Available in all environments (OpenSSL standard tool)
- Consistent with existing project naming conventions

**Approved:** 2025-11-20
**Approved by:** Andrew Hopper

---

## Folder Structure Conventions

### Content Workflow

**Structure:**
```
content/
├── seed/           # Raw ideas, initial concepts (no UUID subdirs)
├── draft/          # Work in progress (UUID subdirs per topic)
├── review/         # Ready for review (UUID subdirs per topic)
└── published/      # Final versions (UUID subdirs per topic)
```

**Naming Pattern:**
- Seed: `content/seed/{topic-name}.md` (shared space)
- Draft/Review/Published: `content/{stage}/{topic-name-uuid}/`

**Example:**
```
content/seed/future-it-ai-ideas.md
content/draft/future-it-ai-f3f4f4fc/
content/review/future-it-ai-f3f4f4fc/
content/published/future-it-ai-f3f4f4fc/
```

### Notes Organization

**Structure:**
```
notes/
└── {topic-name-uuid}/
    └── README.md
```

**Purpose:** Research notes, references, observations organized by topic UUID

**Example:**
```
notes/future-it-ai-f3f4f4fc/README.md
```

**Approved:** 2025-11-20
**Approved by:** Andrew Hopper

---

## Future Conventions

(Add additional conventions as they are established)
