from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

TokenType = Literal["access", "refresh"]

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class SecurityError(Exception):
    """Raised when authentication or authorization fails."""


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_token(subject: str, token_type: TokenType, expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    now = datetime.now(UTC)
    if expires_delta is None:
        minutes = (
            settings.access_token_expire_minutes
            if token_type == "access"
            else settings.refresh_token_expire_minutes
        )
        expires_delta = timedelta(minutes=minutes)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_token(token: str, expected_type: TokenType = "access") -> dict[str, Any]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise SecurityError("Invalid token") from exc
    if payload.get("type") != expected_type:
        raise SecurityError("Invalid token type")
    if not payload.get("sub"):
        raise SecurityError("Token subject is missing")
    return payload


def has_role(user_role: str, accepted_roles: set[str]) -> bool:
    if user_role == "owner":
        return True
    if user_role == "admin" and accepted_roles.intersection({"admin", "member", "viewer"}):
        return True
    if user_role == "member" and accepted_roles.intersection({"member", "viewer"}):
        return True
    if user_role == "viewer" and "viewer" in accepted_roles:
        return True
    return user_role in accepted_roles

