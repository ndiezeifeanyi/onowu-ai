from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.api import ChatMessageCreate, ChatMessageRead, ChatSessionCreate, ChatSessionRead
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/sessions", response_model=ChatSessionRead, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: ChatSessionCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await ChatService().create_session(session, user.id, payload)


@router.get("/sessions", response_model=list[ChatSessionRead])
async def list_sessions(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await ChatService().list_sessions(session, user.id)


@router.post("/sessions/{conversation_id}/messages", response_model=list[ChatMessageRead])
async def post_message(
    conversation_id: str,
    payload: ChatMessageCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        user_message, assistant_message = await ChatService().post_message(
            session, user.id, conversation_id, payload
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return [user_message, assistant_message]

