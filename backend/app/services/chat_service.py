from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base import AgentContext
from app.agents.orchestrator import MasterAgent
from app.db.models import Conversation, MemoryType, Message
from app.schemas.api import ChatMessageCreate, ChatSessionCreate, MemoryCreate
from app.services.memory_service import MemoryService


class ChatService:
    def __init__(self, master_agent: MasterAgent | None = None) -> None:
        self.master_agent = master_agent or MasterAgent()

    async def create_session(
        self, session: AsyncSession, user_id: str, payload: ChatSessionCreate
    ) -> Conversation:
        conversation = Conversation(user_id=user_id, title=payload.title or "New conversation")
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return conversation

    async def list_sessions(self, session: AsyncSession, user_id: str) -> list[Conversation]:
        result = await session.scalars(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(50)
        )
        return list(result)

    async def post_message(
        self,
        session: AsyncSession,
        user_id: str,
        conversation_id: str,
        payload: ChatMessageCreate,
    ) -> tuple[Message, Message]:
        conversation = await session.scalar(
            select(Conversation).where(Conversation.user_id == user_id, Conversation.id == conversation_id)
        )
        if conversation is None:
            raise ValueError("Conversation not found")
        user_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=payload.content,
        )
        session.add(user_message)
        result = await self.master_agent.run(
            AgentContext(user_id=user_id, goal=payload.content, conversation_id=conversation_id)
        )
        assistant_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=result.output,
            metadata_json={
                "confidence": result.confidence,
                "tool_calls": result.tool_calls,
                "artifacts": result.artifacts,
            },
        )
        session.add(assistant_message)
        await MemoryService().create(
            session,
            user_id,
            MemoryCreate(
                memory_type=MemoryType.conversation,
                content=payload.content,
                source=f"conversation:{conversation_id}",
            ),
        )
        await session.commit()
        await session.refresh(user_message)
        await session.refresh(assistant_message)
        return user_message, assistant_message

