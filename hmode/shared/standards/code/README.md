# Reference Examples

## Overview
Gold standard code examples for each key language and framework used in Protoflow prototypes. These examples demonstrate best practices, patterns, and standards to follow across all projects.

## Purpose
- **Consistency:** Maintain consistent coding standards across prototypes
- **Quality:** Set the bar for production-ready code
- **Learning:** Quick reference for best practices
- **Onboarding:** Help new team members understand expected standards

## Languages & Frameworks

### 1. TypeScript
**Location:** `typescript/`
**Demonstrates:** Type safety, error handling, async patterns, documentation

**Key Features:**
- Explicit type definitions and interfaces
- Custom error classes
- JSDoc documentation
- Async/await best practices
- Generic types and type guards

**Use as reference for:**
- Type definitions in any TS project
- Error handling patterns
- Async processing with timeouts
- Function documentation

---

### 2. React + TypeScript
**Location:** `react/`
**Demonstrates:** Modern React patterns, hooks, component composition

**Key Features:**
- Functional components with TypeScript
- React hooks (useState, useEffect, useCallback)
- Props interfaces with proper types
- Accessibility (ARIA attributes)
- Event handling and state management

**Use as reference for:**
- React component structure
- TypeScript integration with React
- Hook patterns and memoization
- Accessible UI components

---

### 3. Node.js + Express
**Location:** `nodejs/`
**Demonstrates:** RESTful API design, middleware, error handling

**Key Features:**
- Express.js server architecture
- Router-based organization
- Middleware pipeline (security, logging)
- Service layer pattern
- Graceful shutdown

**Use as reference for:**
- API server structure
- Express middleware
- Error handling in Node.js
- Async route handlers

---

### 4. Vite Configuration
**Location:** `vite/`
**Demonstrates:** Build tooling, optimization, development workflow

**Key Features:**
- TypeScript configuration
- Path aliases for clean imports
- Build optimization (code splitting)
- Development server with HMR
- Environment variable management

**Use as reference for:**
- Vite project setup
- Build optimization strategies
- Path alias configuration
- Development server setup

---

### 5. Python
**Location:** `python/`
**Demonstrates:** Modern Python patterns, type hints, async processing

**Key Features:**
- Type hints (PEP 484)
- Dataclasses for structured data
- Async/await patterns
- Context managers
- Google-style docstrings

**Use as reference for:**
- Python type annotations
- Dataclass usage
- Async Python patterns
- Error handling and logging

---

### 6. FastAPI
**Location:** `fastapi/`
**Demonstrates:** Modern Python web API with automatic docs

**Key Features:**
- Pydantic models for validation
- Dependency injection
- Auto-generated API documentation
- Async endpoints
- Middleware and exception handlers

**Use as reference for:**
- FastAPI application structure
- Pydantic model design
- API endpoint patterns
- Dependency injection in Python

---

### 7. Pydantic
**Location:** `pydantic/`
**Demonstrates:** Data validation and serialization with Python type hints
**Official Docs:** https://docs.pydantic.dev/

**Key Features:**
- BaseModel for structured data
- Field validation with constraints
- Custom validators (@field_validator, @model_validator)
- Nested models and composition
- Type coercion and parsing
- Serialization (JSON, dict)

**Use as reference for:**
- Data model definition
- Input validation
- API request/response models
- Configuration management
- Type-safe data structures

---

### 8. Pydantic AI
**Location:** `pydantic-ai/`
**Demonstrates:** Type-safe AI agents with structured outputs
**Official Docs:** https://ai.pydantic.dev/

**Key Features:**
- Agent creation with LLM models
- Tool registration (@agent.tool)
- Dependency injection
- Guaranteed structured outputs
- Dynamic instructions
- Streaming responses

**Use as reference for:**
- Building AI agents
- LLM tool integration
- Structured LLM outputs
- Agent orchestration
- Context-aware AI assistants

---

### 9. BAML (BoundaryML)
**Location:** `baml/`
**Demonstrates:** Domain-specific language for structured LLM outputs
**Official Docs:** https://docs.boundaryml.com/

**Key Features:**
- Type definitions for LLM outputs
- Function definitions with prompts
- Multi-language client generation (Python, TS, Ruby, Go, etc.)
- Automatic JSON parsing and retry
- Built-in validation
- VSCode extension with playground

**Use as reference for:**
- Structured LLM outputs
- Type-safe AI integrations
- Cross-language LLM clients
- Prompt engineering
- LLM output validation

---

## Usage Guidelines

### When Starting a New Prototype

1. **Review relevant examples** before writing code
2. **Copy patterns** that fit your use case
3. **Maintain consistency** with demonstrated standards
4. **Adapt as needed** but keep core principles

### Standards to Follow

#### Naming Conventions
- **TypeScript/JavaScript:** camelCase (functions/variables), PascalCase (types/classes)
- **Python:** snake_case (functions/variables), PascalCase (classes)
- **Files:** kebab-case for files, match exports for modules

#### Documentation
- **All public APIs:** JSDoc (TS/JS) or docstrings (Python)
- **Complex logic:** Inline comments explaining "why"
- **Type hints:** Required for all Python functions
- **README:** Every example has comprehensive README

#### Error Handling
- **Custom error classes** for domain-specific errors
- **Try-catch/try-except** around risky operations
- **Logging** for errors and important events
- **Never silent failures:** Always handle or propagate errors

#### Async Patterns
- **Always async/await:** Never raw promises (JS) or callbacks
- **Timeout handling:** Set reasonable timeouts
- **Concurrency control:** Use semaphores or limits for batch operations
- **Error handling:** Proper error propagation in async code

#### Testing (Future)
- Unit tests for business logic
- Integration tests for APIs
- Mock external dependencies
- Aim for >80% coverage

---

## Integration with CLAUDE.md

These examples are referenced in `/home/user/protoflow/CLAUDE.md` as the gold standard for code quality. When Claude Code assists with prototypes, it follows these patterns.

### Phase 7: Implementation

During Phase 7 (Implementation), reference these examples for:
- **Code structure:** How to organize files and modules
- **Design patterns:** Which patterns to use
- **Error handling:** How to handle errors properly
- **Documentation:** What documentation is needed

---

## Maintenance

### Adding New Examples

When adding new language/framework examples:

1. Create new directory under `reference-examples/`
2. Include working code example
3. Add comprehensive README.md
4. Document key features and patterns
5. Update this main README
6. Reference in CLAUDE.md if applicable

### Updating Examples

Examples should evolve as standards improve:
- Keep up with language/framework updates
- Incorporate new best practices
- Add patterns discovered in prototypes
- Remove deprecated approaches

---

## Contributing

When building prototypes, if you discover better patterns:

1. Validate the pattern works well in practice
2. Document the improvement
3. Update relevant reference example
4. Ensure consistency across all examples

---

## Questions?

These examples are living documents. If something is unclear or missing:
- Check the individual README in each example directory
- Review the code - it's heavily commented
- Look at CLAUDE.md for project-wide standards
- Ask for clarification or suggest improvements
