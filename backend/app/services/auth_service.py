from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_token, hash_password, verify_password
from app.db.models import RoleName, User
from app.schemas.api import RegisterRequest, TokenPair
from app.services.audit_service import audit
from app.db.models import EmailOTP
from app.services.email_service import send_email
from datetime import datetime, timedelta, UTC
import secrets


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    return await session.scalar(select(User).where(User.email == email.lower()))


async def get_user_by_id(session: AsyncSession, user_id: str) -> User | None:
    return await session.get(User, user_id)


async def register_user(
    session: AsyncSession,
    payload: RegisterRequest,
    role: RoleName = RoleName.member,
) -> User:
    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role=role,
        timezone=payload.timezone,
    )
    session.add(user)
    await audit(session, user_id=None, action="auth.register", resource_type="user")
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(session, email)
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    await audit(session, user_id=user.id, action="auth.login", resource_type="user", resource_id=user.id)
    await session.commit()
    return user


def issue_tokens(user: User) -> TokenPair:
    return TokenPair(
        access_token=create_token(user.id, "access"),
        refresh_token=create_token(user.id, "refresh"),
    )


async def create_login_code(session: AsyncSession, email: str, minutes: int = 10) -> None:
    """Generate a numeric code, store its hash and send it to the user's email."""
    code = f"{secrets.randbelow(10**6):06d}"
    code_hash = hash_password(code)
    expires_at = datetime.now(UTC) + timedelta(minutes=minutes)

    otp = EmailOTP(email=email.lower(), code_hash=code_hash, expires_at=expires_at, consumed=False)
    session.add(otp)
    await session.commit()
    # send email (best-effort)
    subject = "Your login code"
    body = f"Your login code for Personal AI OS is: {code}. It expires in {minutes} minutes."
    await send_email(subject, email, body)


async def verify_login_code(session: AsyncSession, email: str, code: str):
    """Verify a code for an email. Returns User on success, else None."""
    now = datetime.now(UTC)
    result = await session.scalar(
        select(EmailOTP)
        .where(EmailOTP.email == email.lower(), EmailOTP.consumed == False, EmailOTP.expires_at > now)
        .order_by(EmailOTP.created_at.desc())
    )
    if result is None:
        return None
    otp: EmailOTP = result
    if not verify_password(code, otp.code_hash):
        return None
    # mark consumed
    otp.consumed = True
    await session.commit()

    # find or create user
    user = await get_user_by_email(session, email)
    if user is None:
        # create a user with a random password
        random_pw = secrets.token_urlsafe(24)
        user = User(email=email.lower(), full_name=None, hashed_password=hash_password(random_pw), role=RoleName.member)
        session.add(user)
        await audit(session, user_id=None, action="auth.register_via_otp", resource_type="user")
        await session.commit()
        await session.refresh(user)
    await audit(session, user_id=user.id, action="auth.login_otp", resource_type="user", resource_id=user.id)
    await session.commit()
    return user

