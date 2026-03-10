# Stage 5 - Candidate Selection

## 1.0 Selected Approach

**Full Stack: CLI + Validation + Codegen + MCP Server**

Combines human-facing CLI with AI-agent accessibility, directly supporting the persona's vision that "semantic layer enables AI."

---

## 2.0 Component Breakdown

| Component | Tool/Approach | Purpose |
|-----------|---------------|---------|
| **CLI Core** | Click + Rich | Human discovery: list, show, search, create |
| **Validation** | pykwalify integration | Schema validation against meta-schema |
| **Codegen** | datamodel-code-generator | Generate Pydantic models from domain YAML |
| **MCP Server** | Custom MCP implementation | AI agent discovery of domains |

---

## 3.0 MVP Scope (Revised)

| Phase | Features | Status |
|-------|----------|--------|
| **v0.1 (Done)** | `list`, `show`, `search`, `create`, `validate` | ✅ Implemented |
| **v0.2** | Enhanced validation with pykwalify | 🔜 Next |
| **v0.3** | `codegen` command via datamodel-code-generator | 🔜 Planned |
| **v0.4** | MCP Server for AI agent access | 🔜 Planned |

### v0.1 Features (Current)
- `domain list [--status]` - List all domains
- `domain show <name> [--schema]` - Display domain details
- `domain search <query>` - Search by name/description/entity
- `domain create <name>` - Create from template
- `domain validate <name> [--strict]` - Validate schema structure

### v0.2 Features (Enhanced Validation)
- Meta-schema definition for domain YAML format
- pykwalify-powered deep validation
- Better error messages with line numbers

### v0.3 Features (Code Generation)
- `domain codegen <name> [--output]` - Generate Pydantic models
- Integration with datamodel-code-generator
- Support for v1 and v2 Pydantic output

### v0.4 Features (MCP Server)
- `domain-search` tool for AI agents
- `domain-details` tool for schema inspection
- Natural language domain discovery

---

## 4.0 Output/Audience Validation

| Option | Format | Audience | Selected |
|--------|--------|----------|----------|
| CLI only | Terminal | Human developers | ✅ v0.1 |
| CLI + Codegen | Terminal + Python files | Human developers | ✅ v0.3 |
| CLI + MCP | Terminal + AI tools | Human + AI agents | ✅ v0.4 |

**Selected: Full stack** - All three capabilities

---

## 5.0 Rationale

1. **Persona alignment** - "Semantic layer enables AI" requires MCP
2. **DRY principle** - Codegen prevents redefining types in Python
3. **Incremental delivery** - CLI works now, enhance over time
4. **Tool reuse** - Leverage datamodel-code-generator (3.6k★) and pykwalify

---

## 6.0 Dependencies to Add

```toml
# v0.2
pykwalify = "^1.8"

# v0.3
datamodel-code-generator = "^0.25"

# v0.4
mcp = "^1.0"  # or appropriate MCP SDK
```

---

## 7.0 Decision Record

| Decision | Choice | Alternatives Rejected | Reason |
|----------|--------|----------------------|--------|
| CLI Framework | Click | Typer, argparse | Golden repo pattern |
| Output | Rich | Plain text | Better DX |
| Validation | pykwalify | jsonschema, manual | YAML-native |
| Codegen | datamodel-code-generator | Custom, none | 3.6k★, battle-tested |
| AI Access | MCP Server | VS Code ext, web UI | Supports vision |
