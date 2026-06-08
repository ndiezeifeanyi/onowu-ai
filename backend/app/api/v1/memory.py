from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.api import MemoryCreate, MemoryRead, MemorySearchRequest
from app.services.memory_service import MemoryService

router = APIRouter()


@router.post("/items", response_model=MemoryRead, status_code=status.HTTP_201_CREATED)
async def create_memory(
    payload: MemoryCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await MemoryService().create(session, user.id, payload)


@router.get("/items", response_model=list[MemoryRead])
async def list_memory(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await MemoryService().list(session, user.id)


@router.post("/search", response_model=list[MemoryRead])
async def search_memory(
    payload: MemorySearchRequest,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await MemoryService().search(session, user.id, payload)

