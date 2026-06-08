from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.api import NotificationRead
from app.services.notification_service import NotificationService

router = APIRouter()


@router.get("", response_model=list[NotificationRead])
async def list_notifications(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await NotificationService().list(session, user.id)


@router.post("/test", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
async def send_test_notification(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await NotificationService().create(
        session,
        user_id=user.id,
        title="Personal AI OS notification test",
        body="Dashboard notifications are connected.",
    )

