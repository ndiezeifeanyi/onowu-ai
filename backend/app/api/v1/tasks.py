from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.api import TaskRead
from app.services.task_service import TaskService

router = APIRouter()


@router.get("", response_model=list[TaskRead])
async def list_tasks(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await TaskService().list(session, user.id)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = await TaskService().get(session, user.id, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("/{task_id}/retry", response_model=TaskRead)
async def retry_task(
    task_id: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = await TaskService().mark_retry(session, user.id, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

