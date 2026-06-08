from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import httpx

from app.api.deps import get_current_user, get_db
from app.core.security import SecurityError, decode_token
from app.schemas.api import LoginRequest, RefreshRequest, RegisterRequest, TokenPair, UserRead
from app.services.auth_service import (
    authenticate_user,
    get_user_by_email,
    get_user_by_id,
    issue_tokens,
    register_user,
    create_login_code,
    verify_login_code,
)
from app.schemas.api import RequestCodeRequest, VerifyCodeRequest
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(session, payload.email)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return await register_user(session, payload)


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_db)):
    user = await authenticate_user(session, payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return issue_tokens(user)


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest, session: AsyncSession = Depends(get_db)):
    try:
        decoded = decode_token(payload.refresh_token, "refresh")
    except SecurityError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    user = await get_user_by_id(session, decoded["sub"])
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or missing user")
    return issue_tokens(user)


@router.get("/me", response_model=UserRead)
async def me(user=Depends(get_current_user)):
    return user


@router.post("/request-code")
async def request_code(payload: RequestCodeRequest, session: AsyncSession = Depends(get_db)):
    await create_login_code(session, payload.email)
    return {"ok": True}


@router.post("/verify-code", response_model=TokenPair)
async def verify_code(payload: VerifyCodeRequest, session: AsyncSession = Depends(get_db)):
    user = await verify_login_code(session, payload.email, payload.code)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid code")
    return issue_tokens(user)


# Google OAuth2 endpoints
@router.get("/google/login")
async def google_login():
    if not settings.google_client_id or not settings.google_redirect_uri:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Google OAuth not configured")
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url)


@router.get("/google/callback", response_model=TokenPair)
async def google_callback(code: str | None = None, session: AsyncSession = Depends(get_db)):
    if code is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing code")
    if not settings.google_client_id or not settings.google_client_secret or not settings.google_redirect_uri:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Google OAuth not configured")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        tok_resp = await client.post(token_url, data=data, timeout=10.0)
        if tok_resp.status_code != 200:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to exchange code")
        token_data = tok_resp.json()
        id_token = token_data.get("id_token")
        access_token = token_data.get("access_token")

        # fetch userinfo
        userinfo = None
        if access_token:
            ui_resp = await client.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {access_token}"}, timeout=10.0)
            if ui_resp.status_code == 200:
                userinfo = ui_resp.json()

    if not userinfo:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to fetch userinfo")

    email = userinfo.get("email")
    email_verified = userinfo.get("email_verified")
    if not email or not email_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google account email not verified")

    # create or get user
    user = await get_user_by_email(session, email)
    if user is None:
        # create user with a random password placeholder
        from app.schemas.api import RegisterRequest

        reg = RegisterRequest(email=email, password="")
        user = await register_user(session, reg)

    return issue_tokens(user)

