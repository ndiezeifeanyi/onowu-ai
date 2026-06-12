from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import MemoryItem
from app.memory.vector import VectorProvider, build_vector_provider
from app.schemas.api import MemoryCreate, MemorySearchRequest


class MemoryService:
    def __init__(self, vector_provider: VectorProvider | None = None) -> None:
        self.vector_provider = vector_provider or build_vector_provider()

    async def create(self, session: AsyncSession, user_id: str, payload: MemoryCreate) -> MemoryItem:
        item = MemoryItem(
            user_id=user_id,
            memory_type=payload.memory_type,
            content=payload.content,
            source=payload.source,
            importance=payload.importance,
            metadata_json=payload.metadata,
        )
        session.add(item)
        await session.flush()
        try:
            item.embedding_id = await self.vector_provider.upsert(
                user_id=user_id,
                item_id=item.id,
                text=item.content,
                metadata={"memory_type": item.memory_type.value, "source": item.source},
            )
        except Exception:
            item.embedding_id = None
        await session.commit()
        await session.refresh(item)
        return item

    async def list(self, session: AsyncSession, user_id: str, limit: int = 50) -> list[MemoryItem]:
        result = await session.scalars(
            select(MemoryItem)
            .where(MemoryItem.user_id == user_id)
            .order_by(MemoryItem.created_at.desc())
            .limit(limit)
        )
        return list(result)

    async def search(
        self, session: AsyncSession, user_id: str, payload: MemorySearchRequest
    ) -> list[MemoryItem]:
        conditions = [MemoryItem.user_id == user_id]
        if payload.memory_type:
            conditions.append(MemoryItem.memory_type == payload.memory_type)
        terms = [term for term in payload.query.split() if term]
        if terms:
            conditions.append(or_(*[MemoryItem.content.ilike(f"%{term}%") for term in terms]))
        result = await session.scalars(
            select(MemoryItem)
            .where(*conditions)
            .order_by(MemoryItem.importance.desc(), MemoryItem.created_at.desc())
            .limit(payload.limit)
        )
        return list(result)

