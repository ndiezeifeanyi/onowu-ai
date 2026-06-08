from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import TaskRun, TaskStatus


class TaskService:
    async def list(self, session: AsyncSession, user_id: str, limit: int = 50) -> list[TaskRun]:
        result = await session.scalars(
            select(TaskRun)
            .where(TaskRun.user_id == user_id)
            .order_by(TaskRun.created_at.desc())
            .limit(limit)
        )
        return list(result)

    async def get(self, session: AsyncSession, user_id: str, task_id: str) -> TaskRun | None:
        return await session.scalar(select(TaskRun).where(TaskRun.user_id == user_id, TaskRun.id == task_id))

    async def mark_retry(self, session: AsyncSession, user_id: str, task_id: str) -> TaskRun | None:
        task = await self.get(session, user_id, task_id)
        if task is None:
            return None
        task.status = TaskStatus.retrying
        task.attempts += 1
        await session.commit()
        await session.refresh(task)
        return task

