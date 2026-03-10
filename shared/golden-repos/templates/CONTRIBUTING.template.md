# Contributing to {Project Name}

Thank you for your interest in contributing! This document provides guidelines and steps for contributing.

## Code of Conduct

Be respectful and constructive. We're all here to build great software together.

## Getting Started

### Development Setup

```bash
# Clone and install
git clone https://github.com/{org}/{repo}.git
cd {repo}
npm install  # or: uv pip install -e ".[dev]"

# Set up pre-commit hooks (if applicable)
npm run prepare  # or: pre-commit install

# Verify setup
npm test
```

### Project Structure

```
src/           # Source code
tests/         # Test files
docs/          # Documentation
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Changes

- Write code following our style guide
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
npm test

# Run specific test file
npm test -- path/to/test.ts

# Check types
npm run typecheck

# Lint code
npm run lint
```

### 4. Commit Changes

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: <type>(<scope>): <description>

git commit -m "feat(auth): add JWT refresh token support"
git commit -m "fix(api): handle null response correctly"
git commit -m "docs(readme): update installation steps"
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code style (formatting, semicolons)
- `refactor` - Code change that neither fixes nor adds
- `test` - Adding or updating tests
- `chore` - Maintenance tasks

### 5. Submit Pull Request

1. Push your branch: `git push origin feature/your-feature-name`
2. Open a PR against `main`
3. Fill out the PR template
4. Request review

## Code Style

### TypeScript

- Use TypeScript strict mode
- Prefer `const` over `let`
- Use explicit return types for functions
- Follow ESLint configuration

```typescript
// Good
export function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Avoid
export function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price;
  }
  return total;
}
```

### Python

- Follow PEP 8 and use type hints
- Use Google-style docstrings
- Run `ruff` for linting

```python
# Good
def calculate_total(items: list[Item]) -> float:
    """Calculate total price of items.

    Args:
        items: List of items with price attribute.

    Returns:
        Sum of all item prices.
    """
    return sum(item.price for item in items)
```

## Testing

### Writing Tests

- Place tests in `tests/` directory
- Name test files `*.test.ts` or `test_*.py`
- Use descriptive test names

```typescript
describe('calculateTotal', () => {
  it('returns 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('sums prices correctly', () => {
    const items = [{ price: 10 }, { price: 20 }];
    expect(calculateTotal(items)).toBe(30);
  });
});
```

### Test Coverage

- Aim for 80%+ coverage on new code
- Focus on critical paths and edge cases
- Don't test implementation details

## Documentation

- Update README.md for user-facing changes
- Add JSDoc/docstrings for public APIs
- Include code examples where helpful

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be specific and include reproduction steps for bugs
