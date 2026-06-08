from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Notification, NotificationStatus


class NotificationService:
    async def create(
        self,
        session: AsyncSession,
        *,
        user_id: str,
        title: str,
        body: str,
        channel: str = "dashboard",
        metadata: dict | None = None,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            title=title,
            body=body,
            channel=channel,
            status=NotificationStatus.pending,
            metadata_json=metadata or {},
        )
        session.add(notification)
        await session.commit()
        await session.refresh(notification)
        return notification

    async def list(self, session: AsyncSession, user_id: str) -> list[Notification]:
        result = await session.scalars(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(50)
        )
        return list(result)

