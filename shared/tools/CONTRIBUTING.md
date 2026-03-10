<!-- File UUID: 9a4f2b5c-7e3d-4a1f-8c6b-2d9e5f1a3c8d -->

# Contributing to Protoflow Tools

Thank you for considering contributing to our tools! This document provides guidelines for contributing to the utilities in this repository.

## Getting Started

1. **Fork the repository** and clone your fork locally
2. **Create a branch** for your changes: `git checkout -b feature/your-feature-name`
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit your changes** with clear, descriptive messages
6. **Push to your fork** and submit a pull request

## Development Guidelines

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use descriptive variable names

**Example:**
```python
def process_file(file_path: str, options: dict[str, any]) -> bool:
    """Process a file with given options.

    Args:
        file_path: Path to the file to process
        options: Configuration options

    Returns:
        True if successful, False otherwise
    """
    pass
```

### Documentation

- **Docstrings:** All functions must have docstrings explaining purpose, arguments, and return values
- **README updates:** Update relevant README files when adding features or changing behavior
- **Comments:** Use inline comments for complex logic only

### Testing

Before submitting a pull request:

1. **Manual testing:** Test your changes with various inputs
2. **Edge cases:** Test error conditions and boundary cases
3. **Environment:** Test with required environment variables set and unset

### Commit Messages

Use clear, descriptive commit messages:

```
Good:
- "Add support for custom content-type override"
- "Fix error handling for missing credentials"
- "Update README with batch upload examples"

Bad:
- "fix bug"
- "updates"
- "wip"
```

## Pull Request Process

1. **Describe your changes** clearly in the PR description
2. **Link related issues** if applicable
3. **Update documentation** if you've changed functionality
4. **Ensure all checks pass** (if CI/CD is configured)
5. **Respond to review feedback** promptly

## Reporting Issues

When reporting bugs, include:

1. **Description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment details** (Python version, OS, etc.)
5. **Error messages** or stack traces

## Feature Requests

For feature requests, provide:

1. **Use case** - What problem does this solve?
2. **Proposed solution** - How should it work?
3. **Alternatives considered** - What other approaches did you consider?

## Code of Conduct

- Be respectful and constructive
- Focus on the code, not the person
- Accept constructive criticism gracefully
- Help newcomers and less experienced contributors

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the `question` label
- Reach out to the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
