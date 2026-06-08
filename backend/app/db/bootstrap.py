from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.registry import build_default_agent_registry
from app.core.config import get_settings
from app.core.security import hash_password
from app.db.base import Base
from app.db.models import AgentRecord, RoleName, ToolPermission, ToolRecord, User
from app.db.session import engine
from app.tools.registry import build_default_tool_registry


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_defaults(session: AsyncSession) -> None:
    settings = get_settings()
    owner = await session.scalar(select(User).where(User.email == settings.default_owner_email))
    if owner is None:
        owner = User(
            email=settings.default_owner_email,
            full_name="Personal AI OS Owner",
            hashed_password=hash_password(settings.default_owner_password),
            role=RoleName.owner,
            preferences={
                "fields": ["AI", "Data Science", "Bioinformatics", "Microbiology"],
                "deployment_region": settings.gcp_region,
            },
        )
        session.add(owner)

    agent_registry = build_default_agent_registry()
    for agent in agent_registry.list_agents():
        existing = await session.scalar(
            select(AgentRecord).where(AgentRecord.agent_id == agent.definition.agent_id)
        )
        if existing is None:
            session.add(
                AgentRecord(
                    agent_id=agent.definition.agent_id,
                    display_name=agent.definition.name,
                    description=agent.definition.description,
                    capabilities=agent.definition.capabilities,
                )
            )

    tool_registry = build_default_tool_registry()
    for tool in tool_registry.list_tools():
        existing = await session.scalar(select(ToolRecord).where(ToolRecord.tool_id == tool.tool_id))
        if existing is None:
            session.add(
                ToolRecord(
                    tool_id=tool.tool_id,
                    name=tool.name,
                    description=tool.description,
                    capabilities=tool.capabilities,
                    risk_level=tool.risk_level,
                    requires_approval=tool.requires_approval,
                )
            )
        for role in (RoleName.owner, RoleName.admin, RoleName.member):
            allowed = await session.scalar(
                select(ToolPermission).where(
                    ToolPermission.tool_id == tool.tool_id,
                    ToolPermission.role == role,
                )
            )
            if allowed is None:
                session.add(ToolPermission(tool_id=tool.tool_id, role=role, allowed=True))

    await session.commit()

