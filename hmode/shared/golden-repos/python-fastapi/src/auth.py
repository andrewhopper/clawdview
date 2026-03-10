"""Authentication utilities and middleware."""

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from .config import get_settings
from .logging_config import get_logger

log = get_logger("auth")
security = HTTPBearer(auto_error=False)


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str  # Subject (user ID)
    exp: datetime  # Expiration time
    iat: datetime  # Issued at


class User(BaseModel):
    """Authenticated user."""

    id: str
    email: str
    roles: list[str] = []


def create_token(user_id: str, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token.

    NOTE: This is a placeholder. In production, use a proper JWT library:
    - python-jose
    - PyJWT

    Example with python-jose:
        from jose import jwt
        to_encode = {"sub": user_id, "exp": expire}
        return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    """
    settings = get_settings()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))

    # Placeholder - replace with actual JWT encoding
    return f"placeholder-token-{user_id}-{expire.isoformat()}"


def decode_token(token: str) -> TokenPayload | None:
    """
    Decode and validate a JWT token.

    NOTE: This is a placeholder. In production, use a proper JWT library.

    Example with python-jose:
        from jose import jwt, JWTError
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            return TokenPayload(**payload)
        except JWTError:
            return None
    """
    # Placeholder - replace with actual JWT decoding
    if token.startswith("placeholder-token-"):
        parts = token.split("-")
        if len(parts) >= 4:
            return TokenPayload(
                sub=parts[2],
                exp=datetime.utcnow() + timedelta(hours=1),
                iat=datetime.utcnow(),
            )
    return None


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> User:
    """
    Dependency to get the current authenticated user.

    Usage:
        @router.get("/me")
        async def get_me(user: Annotated[User, Depends(get_current_user)]):
            return user
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # In production, fetch user from database
    user = User(
        id=payload.sub,
        email=f"{payload.sub}@example.com",  # Placeholder
        roles=["user"],
    )

    log.debug("User authenticated", user_id=user.id)
    return user


async def get_optional_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> User | None:
    """
    Dependency to optionally get the current user.
    Returns None if not authenticated (doesn't raise exception).
    """
    if not credentials:
        return None

    payload = decode_token(credentials.credentials)
    if not payload:
        return None

    return User(
        id=payload.sub,
        email=f"{payload.sub}@example.com",
        roles=["user"],
    )


def require_roles(*roles: str):
    """
    Dependency factory to require specific roles.

    Usage:
        @router.get("/admin")
        async def admin_only(user: Annotated[User, Depends(require_roles("admin"))]):
            return {"message": "Welcome admin"}
    """

    async def check_roles(
        user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if not any(role in user.roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return check_roles
