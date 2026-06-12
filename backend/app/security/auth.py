from dataclasses import dataclass
from typing import Optional

from app.core.security import decode_token, SecurityError


@dataclass
class UserContext:
    id: str
    role: str


def verify_jwt(auth_header: Optional[str]) -> UserContext:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise SecurityError("Authorization header missing or malformed")
    token = auth_header.split(" ", 1)[1]
    payload = decode_token(token, "access")
    return UserContext(id=payload["sub"], role=payload.get("role", "member"))
