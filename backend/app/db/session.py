from collections.abc import AsyncGenerator

import orjson
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

engine_kwargs = {
    "pool_pre_ping": True,
    "json_serializer": lambda value: orjson.dumps(value).decode(),
    "json_deserializer": orjson.loads,
}

if settings.database_url.startswith("sqlite"):
    engine_kwargs.pop("pool_pre_ping", None)

engine = create_async_engine(settings.database_url, **engine_kwargs)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

