## 🌟 REFERENCE EXAMPLES (Gold Standard Code)

**Location:** `hmode/shared/standards/code/`

**Purpose:** Gold standard code examples for each key language/framework. These demonstrate best practices, patterns, and standards for all prototypes.

### Available References

1. **TypeScript** - Type safety, error handling, async patterns
2. **React + TypeScript** - Modern React components with hooks
3. **Node.js + Express** - RESTful API, middleware, error handling
4. **Vite** - Build configuration, optimization, development workflow
5. **Python** - Type hints, dataclasses, async patterns
6. **FastAPI** - Modern Python API with auto docs
7. **Pydantic** - Data validation and serialization
8. **Pydantic AI** - Type-safe AI agents with structured outputs
9. **BAML** - Structured LLM outputs with multi-language support

### When to Use

**Phase 6 (Technical Design):**
- Review hmode/shared/standards/code/ for chosen tech stack
- Validate design decisions against patterns
- Identify libraries and approaches

**Phase 7 (Implementation):**
- **ALWAYS reference hmode/shared/standards/code/** before writing code
- Copy patterns that fit your use case
- Maintain consistency with demonstrated standards
- Follow naming conventions and structure

**Phase 8 (Refinement):**
- Compare implementation against hmode/shared/standards/code/
- Refactor to match standards
- Update examples if better patterns discovered

### Standards from Examples

**Code Quality:**
- Full type hints (Python) or type annotations (TypeScript)
- JSDoc/docstrings for all public APIs
- Custom error classes for domain errors
- Async/await patterns throughout
- Proper error handling (never silent failures)
- **Model timestamps required:** All domain models MUST include `created_at` and `updated_at` fields

**Structure:**
- Service layer pattern
- Dependency injection
- Clean separation of concerns
- Testable design

**Documentation:**
- README in every directory
- Inline comments for complex logic
- Type definitions as documentation
- Usage examples

**Assets and Media:**
- **Use Unsplash for placeholder images/art** (free, high-quality, no attribution required for prototypes)
- Include Unsplash URLs or download images to `assets/images/`
- Example: `https://source.unsplash.com/800x600/?technology` for random tech images
- For specific images: `https://images.unsplash.com/photo-[id]?w=800`
- Never use copyrighted images or stock photos requiring licenses

**Design & Visualization Resources:**
- **Flowcharts:** Use Figma's comprehensive flowchart standards as reference
  - **Local Reference:** `hmode/shared/standards/design/flowcharts/` (12 example images + comprehensive guide)
  - **External Resource:** https://www.figma.com/resource-library/types-of-flow-charts/
  - **Documentation:** `hmode/shared/standards/design/flowcharts/README.md`
  - **Covers:** 12 diagram types with aesthetic principles, color usage, typography, accessibility
  - **Includes:** Process flows, data flows, swimlanes, decision trees, value streams, BPMN workflows
  - **Application:** Apply these principles when creating Mermaid diagrams or architectural visualizations
  - **Reference before creating:** Review relevant example image (01-12) for visual standards

### Reference Before Coding

```
Before:
❌ "Let me quickly write this API endpoint..."

After:
✅ "Let me check hmode/shared/standards/code/fastapi/ for the pattern..."
✅ "Following the structure from hmode/shared/standards/code/nodejs/..."
✅ "Using error handling pattern from hmode/shared/standards/code/python/..."
```

**See:** `hmode/shared/standards/code/README.md` for complete guidelines.

### Model Timestamps Requirement

**Rule:** ALL domain models MUST include `created_at` and `updated_at` fields for audit tracking.

**Pydantic (Python):**
```python
from datetime import datetime
from pydantic import BaseModel, Field, model_validator

class MyModel(BaseModel):
    # ... other fields ...
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    @model_validator(mode='after')
    def update_timestamp(self) -> 'MyModel':
        self.updated_at = datetime.now()
        return self
```

**SQLAlchemy (Python):**
```python
from datetime import datetime
from sqlalchemy import Column, DateTime

class MyModel(Base):
    # ... other fields ...
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

**Dataclass (Python):**
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MyModel:
    # ... other fields ...
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

**TypeScript Interface:**
```typescript
interface MyModel {
    // ... other fields ...
    createdAt: Date;
    updatedAt: Date;
}
```

**Reference Implementation:** `hmode/shared/standards/code/pydantic/models.py` (User class)

