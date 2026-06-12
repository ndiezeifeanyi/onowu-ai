from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
import json

from typing import Any

from app.agents.base import AgentContext
from app.agents.registry import build_default_agent_registry
from app.api.deps import get_current_user
from app.db.models import User
from app.schemas.api import AgentRead, AgentRunRequest, AgentRunResponse
from app.agents.enterprise import EnterpriseReActAgent
from app.ai.providers import ModelRouter
from app.memory.vector import build_vector_provider
from app.mcp.server.executor import execute_mcp_syscall

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


@router.post("/run_stream")
async def run_agent_stream(payload: AgentRunRequest, user: User = Depends(get_current_user)):
    async def event_generator():
        class MCPClient:
            async def call(self, tool_name: str, args: dict[str, Any]):
                return await execute_mcp_syscall(tool_name, args, user)

        agent = EnterpriseReActAgent(ModelRouter(), build_vector_provider(), MCPClient())

        async for event in agent.execute_stream(payload.goal, user_id=user.id):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

