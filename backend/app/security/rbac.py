from app.core.security import has_role, SecurityError


def check_access(user_role: str, path: str) -> None:
    # Lightweight path-based RBAC rules. Extend for production policies.
    if user_role in ("owner", "admin"):
        return
    # Disallow non-admins from mutating tools
    if path.startswith("/api/v1/tools") and user_role != "admin":
        raise SecurityError("Insufficient role for tools access")


def enforce_tool_access(user_role: str, allowed_roles: list[str]) -> None:
    if user_role in ("owner", "admin"):
        return
    if not has_role(user_role, set(allowed_roles)):
        raise SecurityError("Tool access denied for role")
