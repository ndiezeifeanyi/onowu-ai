from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.base import AgentContext
from app.agents.registry import build_default_agent_registry
from app.api.deps import get_current_user
from app.db.models import User
from app.schemas.api import AgentRead, AgentRunRequest, AgentRunResponse

router = APIRouter()


@router.get("", response_model=list[AgentRead])
async def list_agents(user: User = Depends(get_current_user)):
    registry = build_default_agent_registry()
    return [
        AgentRead(
            agent_id=agent.definition.agent_id,
            name=agent.definition.name,
            description=agent.definition.description,
            capabilities=agent.definition.capabilities,
        )
        for agent in registry.list_agents()
    ]


@router.post("/{agent_id}/runs", response_model=AgentRunResponse)
async def run_agent(
    agent_id: str,
    payload: AgentRunRequest,
    user: User = Depends(get_current_user),
):
    registry = build_default_agent_registry()
    try:
        agent = registry.get(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found") from exc
    result = await agent.run(AgentContext(user_id=user.id, goal=payload.goal, metadata=payload.context))
    return AgentRunResponse(
        agent_id=result.agent_id,
        output=result.output,
        confidence=result.confidence,
        tool_calls=result.tool_calls,
        memory_writes=result.memory_writes,
    )

