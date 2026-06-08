from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Schedule
from app.schemas.api import ScheduleCreate, ScheduleUpdate


class ScheduleService:
    async def create(self, session: AsyncSession, user_id: str, payload: ScheduleCreate) -> Schedule:
        schedule = Schedule(
            user_id=user_id,
            name=payload.name,
            cron=payload.cron,
            timezone=payload.timezone,
            workflow_goal=payload.workflow_goal,
            payload=payload.payload,
        )
        session.add(schedule)
        await session.commit()
        await session.refresh(schedule)
        return schedule

    async def list(self, session: AsyncSession, user_id: str) -> list[Schedule]:
        result = await session.scalars(
            select(Schedule).where(Schedule.user_id == user_id).order_by(Schedule.created_at.desc())
        )
        return list(result)

    async def update(
        self, session: AsyncSession, user_id: str, schedule_id: str, payload: ScheduleUpdate
    ) -> Schedule | None:
        schedule = await session.scalar(
            select(Schedule).where(Schedule.user_id == user_id, Schedule.id == schedule_id)
        )
        if schedule is None:
            return None
        if payload.status is not None:
            schedule.status = payload.status
        if payload.cron is not None:
            schedule.cron = payload.cron
        if payload.payload is not None:
            schedule.payload = payload.payload
        await session.commit()
        await session.refresh(schedule)
        return schedule

