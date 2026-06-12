from typing import Any


def sanitize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Recursively sanitize payload strings to reduce injection vectors."""
    def _sanitize(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: _sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_sanitize(v) for v in obj]
        if isinstance(obj, str):
            s = obj
            if len(s) > 10000:
                s = s[:10000]
            # basic pattern stripping
            for pat in ("<script", "{{", "}}", "import os", "open(", "subprocess"):
                if pat in s:
                    s = s.replace(pat, "")
            return s
        return obj

    return _sanitize(payload)  # type: ignore[return-value]
