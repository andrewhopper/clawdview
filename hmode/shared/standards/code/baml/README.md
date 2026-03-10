# BAML Reference Example

## Overview
Comprehensive BAML (Boundary Markup Language) examples for structured LLM outputs with type safety across Python, TypeScript, and other languages.

**Official Docs:** https://docs.boundaryml.com/
**GitHub:** https://github.com/BoundaryML/baml
**Examples:** https://github.com/BoundaryML/baml-examples/

## What is BAML?

BAML is a domain-specific language for:
- Defining structured types for LLM outputs
- Writing prompts with guaranteed output schemas
- Generating type-safe client code (Python, TS, Ruby, Go, etc.)
- Automatic JSON parsing, validation, and retry

### Key Benefits
- **Type Safety:** Generated code is fully typed
- **Automatic Retry:** Fixes broken JSON automatically
- **Multi-Language:** Works with Python, TypeScript, Ruby, Go, Java, Rust
- **IDE Support:** VSCode extension with syntax highlighting
- **Testable:** Built-in playground for testing

## Files

- `example.baml` - Complete BAML definitions (types, functions, tests)
- `python_usage.py` - Python client usage examples
- `typescript_usage.ts` - TypeScript client usage (see below)

## Installation

### 1. Install BAML CLI
```bash
npm install -g @boundaryml/baml
```

### 2. Install VSCode Extension
Search for "BAML" in VSCode extensions marketplace

### 3. Install Language Client
```bash
# Python
pip install baml-py

# TypeScript/Node
npm install @boundaryml/baml
```

## Quick Start

### 1. Create BAML File
```baml
// user.baml

class User {
  name string @description("User's full name")
  email string
  age int
}

client<llm> GPT4 {
  provider openai
  options {
    model gpt-4o
  }
}

function ExtractUser(text: string) -> User {
  client GPT4

  prompt #"
    Extract user info from: {{ text }}
  "#
}
```

### 2. Generate Client Code
```bash
baml generate
```

This creates `baml_client/` with generated code.

### 3. Use in Python
```python
from baml_client import b

user = await b.ExtractUser("John Doe, john@example.com, age 30")
print(user.name)  # Type-safe!
```

### 4. Use in TypeScript
```typescript
import { b } from './baml_client'

const user = await b.ExtractUser("John Doe, john@example.com, age 30")
console.log(user.name)  // Type-safe!
```

## BAML Syntax

### Type Definitions
```baml
// Basic class
class Person {
  name string
  age int
  email string
}

// Optional fields
class User {
  username string
  bio string?  // Optional
  verified bool
}

// Lists
class Post {
  title string
  tags string[]
  comments Comment[]
}

// Enums
enum Status {
  ACTIVE
  INACTIVE
  SUSPENDED
}

// Nested types
class BlogPost {
  title string
  author Person
  status Status
  tags string[]
}

// Validation constraints
class Product {
  name string @assert(this.length > 0)
  price float @assert(this > 0)
  rating float @assert(this >= 1.0 and this <= 5.0)
}
```

### Client Configuration
```baml
client<llm> OpenAI {
  provider openai
  options {
    model gpt-4o
    temperature 0.7
    max_tokens 1000
  }
}

client<llm> Anthropic {
  provider anthropic
  options {
    model claude-3-5-sonnet-20241022
  }
}

// With retry policy
client<llm> Production {
  provider openai
  options {
    model gpt-4o
  }
  retry_policy {
    max_retries 3
    strategy exponential_backoff
  }
}
```

### Function Definitions
```baml
// Simple function
function ExtractInfo(text: string) -> Person {
  client OpenAI

  prompt #"
    Extract person info from: {{ text }}
  "#
}

// Multiple parameters
function Summarize(
  text: string,
  max_length: int,
  style: string
) -> string {
  client OpenAI

  prompt #"
    Summarize in {{ style }} style (max {{ max_length }} words):
    {{ text }}
  "#
}

// Template loops
function Classify(text: string, categories: string[]) -> string {
  client OpenAI

  prompt #"
    Classify into one of these categories:
    {% for cat in categories %}
    - {{ cat }}
    {% endfor %}

    Text: {{ text }}
  "#
}
```

### Tests
```baml
test TestExtract {
  functions [ExtractInfo]

  args {
    text "John Doe, 30 years old"
  }
}
```

## Usage Patterns

### Python Usage
```python
from baml_client import b
from baml_client.types import User, Sentiment

# Simple call
user = await b.ExtractUser(text)

# With error handling
try:
    review = await b.AnalyzeReview(review_text)
    print(f"Sentiment: {review.sentiment}")
except Exception as e:
    print(f"Error: {e}")

# Batch processing
tasks = [b.ExtractUser(text) for text in texts]
users = await asyncio.gather(*tasks)
```

### TypeScript Usage
```typescript
import { b } from './baml_client'
import type { User, ProductReview } from './baml_client/types'

// Simple call
const user: User = await b.ExtractUser(text)

// With error handling
try {
  const review: ProductReview = await b.AnalyzeReview(reviewText)
  console.log(`Sentiment: ${review.sentiment}`)
} catch (error) {
  console.error('Error:', error)
}

// Batch processing
const tasks = texts.map(text => b.ExtractUser(text))
const users = await Promise.all(tasks)
```

## Advanced Features

### Automatic Error Recovery

BAML automatically handles:

1. **Malformed JSON**
   - Detects parsing errors
   - Uses reflection to explain error to LLM
   - Retries with corrected output

2. **Type Validation**
   - Validates against defined schema
   - Sends validation errors to LLM
   - Retries with proper types

3. **Network Errors**
   - Exponential backoff retry
   - Configurable retry policies

### Testing in Playground

Use VSCode extension to test BAML functions:

1. Open `.baml` file
2. Click "Run Test" on any `test` block
3. See results in playground
4. Debug prompts and outputs

### Multi-Language Support

Same BAML definition generates clients for:
- Python
- TypeScript
- Ruby
- Go
- Java
- C#
- Rust

## Best Practices

### 1. Type Design
```baml
// Good: Clear, validated types
class User {
  email string @description("Valid email address")
  age int @assert(this >= 0 and this <= 150)
}

// Bad: Vague types
class User {
  contact string  // Email? Phone? Unclear
  info string     // What info?
}
```

### 2. Prompt Engineering
```baml
// Good: Clear instructions
function Extract(text: string) -> User {
  prompt #"
    Extract user information from the text below.

    Requirements:
    - Name: Full name (first and last)
    - Email: Valid email format
    - Age: Integer between 0-150

    Text: {{ text }}
  "#
}

// Bad: Vague prompt
function Extract(text: string) -> User {
  prompt #"Get user from {{ text }}"#
}
```

### 3. Error Handling
```python
# Good: Handle specific errors
try:
    user = await b.ExtractUser(text)
except ValueError as e:
    # Validation failed
    logger.error(f"Validation: {e}")
except Exception as e:
    # Other errors
    logger.error(f"Extraction failed: {e}")

# Bad: Catch all, no logging
try:
    user = await b.ExtractUser(text)
except:
    pass
```

### 4. Testing
```baml
// Add tests for edge cases
test TestEmptyInput {
  functions [ExtractUser]
  args { text "" }
}

test TestInvalidFormat {
  functions [ExtractUser]
  args { text "random noise without user info" }
}
```

## Project Structure

```
my-project/
├── baml_src/              # BAML source files
│   ├── main.baml          # Main definitions
│   ├── types.baml         # Type definitions
│   └── functions.baml     # Function definitions
├── baml_client/           # Generated code (gitignore)
│   ├── __init__.py
│   ├── types.py
│   └── client.py
├── src/                   # Your application code
│   └── main.py
└── baml.config            # BAML configuration
```

## Environment Setup

```bash
# Required
export OPENAI_API_KEY="your-key"

# Optional (for other providers)
export ANTHROPIC_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
```

## Common Issues

### Issue: "baml_client not found"
**Solution:** Run `baml generate` to generate client code

### Issue: "Import error in generated code"
**Solution:** Ensure `baml-py` is installed: `pip install baml-py`

### Issue: "VSCode syntax highlighting not working"
**Solution:** Install BAML VSCode extension

### Issue: "Validation always fails"
**Solution:** Check constraints in type definition, simplify if too strict

## Resources

- **Documentation:** https://docs.boundaryml.com/
- **Examples Repo:** https://github.com/BoundaryML/baml-examples/
- **Discord Community:** (check GitHub for invite link)
- **GitHub Issues:** https://github.com/BoundaryML/baml/issues
