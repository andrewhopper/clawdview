# Pydantic AI Reference Example

## Overview
Comprehensive Pydantic AI agent examples demonstrating AI agent patterns with type-safe tools and structured outputs.

**Official Docs:** https://ai.pydantic.dev/

## Key Features

### Agent Creation
- Initialize agents with model selection
- Type-safe dependencies
- Guaranteed structured outputs
- System prompts and instructions

### Tool Registration
- `@agent.tool` decorator for functions
- Automatic tool description from docstrings
- Type-safe parameters
- Async tool support

### Dependency Injection
- Pass context to agent and tools
- Type-safe dependencies
- Database connections, configs, etc.
- Testable with mock dependencies

### Structured Outputs
- Pydantic models for responses
- Automatic validation and retry
- Type-safe access to results
- JSON schema generation

### Dynamic Instructions
- Runtime instruction generation
- Context-aware prompts
- Personalized guidance

## Files
- `agent.py` - Complete agent with tools, dependencies, and examples

## Installation
```bash
pip install pydantic-ai pydantic
# Also need an LLM provider, e.g.:
pip install openai
```

## Usage Examples

### Basic Agent
```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result = await agent.run('What is the capital of France?')
print(result.data)  # "Paris"
```

### Agent with Structured Output
```python
from pydantic import BaseModel
from pydantic_ai import Agent

class CityInfo(BaseModel):
    name: str
    country: str
    population: int

agent = Agent(
    'openai:gpt-4o',
    output_type=CityInfo,
)

result = await agent.run('Tell me about Paris')
city = result.data  # Guaranteed to be CityInfo
print(f"{city.name}, {city.country} - {city.population:,}")
```

### Agent with Tools
```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4o')

@agent.tool
async def get_weather(city: str) -> dict:
    """Get current weather for a city."""
    # API call here
    return {"temp": 72, "conditions": "sunny"}

result = await agent.run("What's the weather in San Francisco?")
```

### Agent with Dependencies
```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class Dependencies:
    user_id: str
    api_key: str

agent = Agent(
    'openai:gpt-4o',
    deps_type=Dependencies,
)

@agent.tool
async def get_user_data(ctx: RunContext[Dependencies]) -> dict:
    """Get user data from database."""
    user_id = ctx.deps.user_id
    # Database query here
    return {"name": "John", "email": "john@example.com"}

deps = Dependencies(user_id="123", api_key="secret")
result = await agent.run("Get my profile", deps=deps)
```

### Dynamic Instructions
```python
@agent.system_prompt
def dynamic_prompt(ctx: RunContext[Dependencies]) -> str:
    return f"You are assisting user {ctx.deps.user_id}"
```

## Standards Demonstrated

### Agent Structure
- One agent per logical task/domain
- Clear system prompts
- Type-safe dependencies
- Structured outputs

### Tool Design
- Focused, single-purpose tools
- Clear docstrings (become tool descriptions)
- Type hints for all parameters
- Return structured data

### Dependencies
- Use dataclasses or Pydantic models
- Include only what tools need
- Easy to mock for testing
- Immutable when possible

### Output Models
- Pydantic BaseModel for validation
- Clear field descriptions
- Appropriate constraints
- Example schemas

### Error Handling
- Let Pydantic AI handle retries
- Provide clear error messages
- Log tool calls for debugging
- Validate inputs in tools

## Best Practices

### 1. Tool Documentation
```python
@agent.tool
async def search_products(
    query: str,
    max_results: int = 10,
) -> List[dict]:
    """Search products in the catalog.

    Args:
        query: Search query string
        max_results: Maximum number of results

    Returns:
        List of matching products
    """
    # Implementation
```

### 2. Dependency Injection
```python
@dataclass
class AppDependencies:
    db: Database
    api_client: APIClient
    user_context: UserContext

# Easy to test with mocks
mock_deps = AppDependencies(
    db=MockDatabase(),
    api_client=MockAPI(),
    user_context=test_user,
)
```

### 3. Structured Outputs
```python
class AnalysisOutput(BaseModel):
    summary: str = Field(..., description="Brief summary")
    confidence: float = Field(..., ge=0, le=1)
    recommendations: List[str]

    @validator('recommendations')
    def min_recommendations(cls, v):
        if len(v) < 1:
            raise ValueError('At least 1 recommendation required')
        return v
```

### 4. Streaming Responses
```python
async with agent.run_stream(message, deps=deps) as result:
    async for text in result.stream_text():
        print(text, end='', flush=True)

    final_output = await result.data()
```

### 5. Error Recovery
```python
try:
    result = await agent.run(message, deps=deps)
except Exception as e:
    logger.error(f"Agent failed: {e}")
    # Fallback logic
```

## Common Patterns

### Multi-Tool Agent
```python
agent = Agent('openai:gpt-4o')

@agent.tool
async def tool_a(): ...

@agent.tool
async def tool_b(): ...

@agent.tool
async def tool_c(): ...
```

### Context-Aware Tools
```python
@agent.tool
async def get_data(ctx: RunContext[Deps]) -> dict:
    # Access dependencies
    db = ctx.deps.database
    user = ctx.deps.user_id

    # Use context for queries
    return await db.fetch(user)
```

### Validation and Retry
Pydantic AI automatically retries if output validation fails:
```python
class Output(BaseModel):
    score: int = Field(..., ge=0, le=100)

# If LLM returns score=150, Pydantic AI will:
# 1. Detect validation failure
# 2. Send error back to LLM
# 3. Ask LLM to retry with correct format
```

## Testing

### Mock Dependencies
```python
@dataclass
class MockDeps:
    customer_id: str = "test_123"
    database_url: str = "mock://db"

deps = MockDeps()
result = await agent.run("test message", deps=deps)
```

### Mock Tools
```python
@agent.tool
async def get_data(ctx: RunContext[Deps]) -> dict:
    if ctx.deps.database_url.startswith("mock://"):
        return {"mock": "data"}
    # Real implementation
```

## Environment Setup

```bash
# Required
export OPENAI_API_KEY="your-key-here"

# Optional (for other providers)
export ANTHROPIC_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
```

## Supported Models

- OpenAI: `openai:gpt-4o`, `openai:gpt-4o-mini`
- Anthropic: `anthropic:claude-3-5-sonnet-20241022`
- Google: `google:gemini-1.5-pro`
- And more (see docs)
