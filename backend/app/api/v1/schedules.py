from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.api import ScheduleCreate, ScheduleRead, ScheduleUpdate
from app.services.schedule_service import ScheduleService

router = APIRouter()


@router.post("", response_model=ScheduleRead, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    payload: ScheduleCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await ScheduleService().create(session, user.id, payload)


@router.get("", response_model=list[ScheduleRead])
async def list_schedules(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await ScheduleService().list(session, user.id)


@router.patch("/{schedule_id}", response_model=ScheduleRead)
async def update_schedule(
    schedule_id: str,
    payload: ScheduleUpdate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    schedule = await ScheduleService().update(session, user.id, schedule_id, payload)
    if schedule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return schedule

