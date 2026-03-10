# Pydantic Reference Example

## Overview
Comprehensive Pydantic v2 examples demonstrating data validation, serialization, and best practices.

**Official Docs:** https://docs.pydantic.dev/latest/

## Key Features

### BaseModel Foundation
- Define data models with Python type hints
- Automatic validation on instantiation
- Type coercion and parsing

### Field Validation
- Built-in validators (EmailStr, HttpUrl, PositiveInt)
- String constraints (min/max length, regex patterns)
- Numeric constraints (ge, le, gt, lt)
- Custom field validators

### Advanced Validation
- `@field_validator` for single field validation
- `@model_validator` for cross-field validation
- Validation on assignment
- Custom error messages

### Nested Models
- Compose models with other models
- Lists and dictionaries of models
- Recursive models support

### Configuration
- `model_config` for model-wide settings
- Strip whitespace
- Extra fields handling (forbid, allow, ignore)
- Validate defaults and assignments

### Serialization
- `model_dump()` → dictionary
- `model_dump_json()` → JSON string
- `model_validate()` → from dictionary
- `model_validate_json()` → from JSON string

## Files
- `models.py` - Complete Pydantic models with all features

## Installation
```bash
pip install pydantic[email]
```

## Usage Examples

### Basic Model
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=3)
    email: str
    is_active: bool = True
```

### Type Coercion
```python
user = User(
    id="123",          # Coerced to int
    username="john",
    email="john@example.com",
    is_active="yes"    # Coerced to True
)
```

### Validation
```python
from pydantic import field_validator

class User(BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Must be alphanumeric')
        return v
```

### Nested Models
```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address
```

## Standards Demonstrated

### Model Design
- One model per logical entity
- Use nested models for composition
- Keep validators simple and focused
- Use Enums for constrained string values

### Field Definitions
- Required fields: `field: type`
- Optional fields: `field: Optional[type] = None`
- With defaults: `field: type = default_value`
- With validation: `field: type = Field(..., constraints)`

### Validators
- Use `@field_validator` for single fields
- Use `@model_validator` for cross-field logic
- Return the value (modified if needed)
- Raise `ValueError` for validation failures

### Configuration
- Set `str_strip_whitespace=True` for string cleaning
- Set `validate_assignment=True` for runtime validation
- Set `extra='forbid'` to catch typos
- Set `validate_default=True` for default validation

### Serialization
- Use `model_dump()` for dictionaries
- Use `model_dump_json()` for JSON
- Use `exclude` to omit fields
- Use `by_alias` for JSON field names

## Best Practices

1. **Type Hints First:** Let types guide validation
2. **Field Constraints:** Use built-in constraints before custom validators
3. **Keep Models Simple:** Avoid complex logic in models
4. **Document Fields:** Use `description` parameter
5. **Use Enums:** For constrained string values
6. **Validate Early:** Catch errors at model boundaries
7. **Test Validators:** Unit test custom validators
8. **Version Models:** Consider versioning for API changes

## Common Patterns

### Optional Fields
```python
age: Optional[int] = None
```

### Fields with Constraints
```python
username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-z]+$')
```

### Lists and Dicts
```python
tags: List[str] = Field(default_factory=list)
metadata: Dict[str, Any] = Field(default_factory=dict)
```

### Custom Validation
```python
@field_validator('email')
@classmethod
def email_lowercase(cls, v: str) -> str:
    return v.lower()
```

### Model Validation
```python
@model_validator(mode='after')
def check_passwords_match(self) -> 'User':
    if self.password != self.password_confirm:
        raise ValueError('Passwords do not match')
    return self
```
