"""
Pydantic Models - Reference Example

Demonstrates:
- BaseModel usage and inheritance
- Field validation with constraints
- Custom validators
- Nested models
- Serialization/deserialization
- Configuration options
- Type coercion

Reference: https://docs.pydantic.dev/latest/
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ConfigDict,
    EmailStr,
    HttpUrl,
    PositiveInt,
    constr,
)


# Enums for constrained values
class UserRole(str, Enum):
    """User roles enumeration."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class AccountStatus(str, Enum):
    """Account status enumeration."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"


# Simple nested model
class Address(BaseModel):
    """Address model with validation.

    Demonstrates:
    - Field constraints
    - Optional fields
    - Default values
    """
    street: str = Field(..., min_length=1, max_length=200, description="Street address")
    city: str = Field(..., min_length=1, max_length=100)
    state: constr(min_length=2, max_length=2) = Field(..., description="Two-letter state code")
    zip_code: constr(pattern=r'^\d{5}(-\d{4})?$') = Field(..., description="US ZIP code")
    country: str = Field(default="USA", description="Country code")

    @field_validator('state')
    @classmethod
    def state_must_be_uppercase(cls, v: str) -> str:
        """Ensure state code is uppercase."""
        return v.upper()

    @field_validator('city')
    @classmethod
    def city_must_be_capitalized(cls, v: str) -> str:
        """Capitalize city name."""
        return v.title()


# Complex model with nested structures
class BankAccount(BaseModel):
    """Bank account model.

    Demonstrates:
    - Nested models
    - Custom types (Decimal for money)
    - Computed fields
    """
    account_number: constr(pattern=r'^\d{10}$') = Field(..., description="10-digit account number")
    balance: Decimal = Field(default=Decimal('0.00'), ge=0, description="Account balance")
    currency: str = Field(default="USD", max_length=3)
    status: AccountStatus = Field(default=AccountStatus.ACTIVE)
    opened_at: datetime = Field(default_factory=datetime.now)

    @field_validator('balance')
    @classmethod
    def validate_balance_precision(cls, v: Decimal) -> Decimal:
        """Ensure balance has at most 2 decimal places."""
        if v.as_tuple().exponent < -2:
            raise ValueError('Balance must have at most 2 decimal places')
        return v


# Main model with all features
class User(BaseModel):
    """Complete user model demonstrating all Pydantic features.

    Demonstrates:
    - All field types
    - Validation
    - Nested models
    - Custom validators
    - Model validators
    - Serialization
    """

    # Configuration
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Strip whitespace from strings
        validate_default=True,       # Validate default values
        validate_assignment=True,    # Validate on attribute assignment
        extra='forbid',              # Forbid extra fields
    )

    # Basic fields with validation
    id: PositiveInt = Field(..., description="Unique user identifier")
    username: constr(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$') = Field(
        ...,
        description="Username (alphanumeric, underscore, hyphen only)"
    )
    email: EmailStr = Field(..., description="Valid email address")

    # Optional fields
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[constr(pattern=r'^\+?1?\d{10,15}$')] = Field(None, description="Phone number")
    website: Optional[HttpUrl] = None

    # Fields with defaults
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    # Nested models
    address: Optional[Address] = None
    accounts: List[BankAccount] = Field(default_factory=list)

    # Complex types
    preferences: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list, max_length=10)

    # Metadata
    metadata: Dict[str, str] = Field(default_factory=dict)

    # Field validators
    @field_validator('username')
    @classmethod
    def username_no_spaces(cls, v: str) -> str:
        """Ensure username has no spaces."""
        if ' ' in v:
            raise ValueError('Username cannot contain spaces')
        return v.lower()

    @field_validator('tags')
    @classmethod
    def tags_must_be_unique(cls, v: List[str]) -> List[str]:
        """Ensure tags are unique."""
        return list(set(v))

    @field_validator('full_name')
    @classmethod
    def full_name_must_have_space(cls, v: Optional[str]) -> Optional[str]:
        """Ensure full name has at least one space (first and last name)."""
        if v and ' ' not in v.strip():
            raise ValueError('Full name must include first and last name')
        return v

    # Model validator (validates entire model)
    @model_validator(mode='after')
    def check_email_username_match(self) -> 'User':
        """Ensure email and username are consistent."""
        if self.email and self.username:
            email_prefix = self.email.split('@')[0]
            if email_prefix.lower() != self.username.lower():
                # Just log warning, don't fail validation
                print(f"Warning: Username '{self.username}' doesn't match email prefix '{email_prefix}'")
        return self

    @model_validator(mode='after')
    def update_timestamp(self) -> 'User':
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()
        return self

    # Serialization methods
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump()

    def to_json(self) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'User':
        """Create from JSON string."""
        return cls.model_validate_json(json_str)


# Example usage with type coercion
class UserRegistration(BaseModel):
    """User registration form with automatic type coercion.

    Demonstrates:
    - Automatic type coercion
    - Parsing from various formats
    """
    username: str
    email: EmailStr
    age: PositiveInt
    signup_timestamp: datetime
    agreed_to_terms: bool

    @field_validator('agreed_to_terms')
    @classmethod
    def terms_must_be_accepted(cls, v: bool) -> bool:
        """Ensure user accepted terms."""
        if not v:
            raise ValueError('Must accept terms to register')
        return v


# Inheritance example
class AdminUser(User):
    """Admin user with additional fields.

    Demonstrates:
    - Model inheritance
    - Field overriding
    """
    role: UserRole = Field(default=UserRole.ADMIN, frozen=True)  # Cannot be changed
    admin_level: PositiveInt = Field(default=1, ge=1, le=5)
    permissions: List[str] = Field(default_factory=list)

    @field_validator('permissions')
    @classmethod
    def permissions_must_be_uppercase(cls, v: List[str]) -> List[str]:
        """Ensure permissions are uppercase."""
        return [p.upper() for p in v]


# Example usage and demonstrations
if __name__ == "__main__":
    # Example 1: Basic model creation
    print("=== Example 1: Basic User ===")
    user = User(
        id=1,
        username="john_doe",
        email="john@example.com",
        full_name="John Doe",
    )
    print(user.to_json())

    # Example 2: Nested models
    print("\n=== Example 2: User with Address ===")
    user_with_address = User(
        id=2,
        username="jane_smith",
        email="jane@example.com",
        full_name="Jane Smith",
        address=Address(
            street="123 Main St",
            city="san francisco",
            state="ca",
            zip_code="94102",
        )
    )
    print(user_with_address.to_json())

    # Example 3: Type coercion
    print("\n=== Example 3: Type Coercion ===")
    registration = UserRegistration(
        username="new_user",
        email="user@example.com",
        age="25",  # String will be coerced to int
        signup_timestamp="2024-01-01T10:00:00",  # String will be coerced to datetime
        agreed_to_terms="true",  # String will be coerced to bool
    )
    print(f"Age type: {type(registration.age)} = {registration.age}")
    print(f"Timestamp type: {type(registration.signup_timestamp)} = {registration.signup_timestamp}")

    # Example 4: Validation errors
    print("\n=== Example 4: Validation Errors ===")
    try:
        invalid_user = User(
            id=-1,  # Must be positive
            username="ab",  # Too short
            email="invalid-email",  # Invalid email
        )
    except Exception as e:
        print(f"Validation error: {e}")

    # Example 5: Admin user inheritance
    print("\n=== Example 5: Admin User ===")
    admin = AdminUser(
        id=100,
        username="admin",
        email="admin@example.com",
        full_name="Admin User",
        admin_level=3,
        permissions=["read", "write", "delete"],
    )
    print(admin.to_json())

    # Example 6: Serialization/deserialization
    print("\n=== Example 6: JSON Round Trip ===")
    json_str = user.to_json()
    restored_user = User.from_json(json_str)
    print(f"Original ID: {user.id}, Restored ID: {restored_user.id}")
