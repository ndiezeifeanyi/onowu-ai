import json
from typing import Callable, Awaitable

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

from app.security.auth import verify_jwt
from app.security.rbac import check_access
from app.security.sanitizer import sanitize_payload
from app.security.audit import audit_log


class ProductionSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]):
        try:
            # 1. Ingress Authentication
            auth_header = request.headers.get("Authorization")
            user = verify_jwt(auth_header)

            # 2. Safe Body Stream Handling (Prevents Downstream Hanging)
            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.body()

                async def receive() -> Message:
                    return {"type": "http.request", "body": body, "more_body": False}

                request._receive = receive

                payload = json.loads(body.decode("utf-8")) if body else {}
                sanitize_payload(payload)

            # 3. Dynamic RBAC Enforcement
            check_access(user.role, request.url.path)

            # 4. Request Forwarding & Continuous Audit Logging
            response = await call_next(request)
            audit_log(user.id, request.url.path, response.status_code)
            return response

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Security validation breach identified.",
            )
