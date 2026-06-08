from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_token, hash_password, verify_password
from app.db.models import RoleName, User
from app.schemas.api import RegisterRequest, TokenPair
from app.services.audit_service import audit


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

