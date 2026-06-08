from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.db.models import User
from app.schemas.api import ToolExecuteRequest, ToolExecuteResponse, ToolRead
from app.tools.base import ToolContext
from app.tools.registry import PermissionedToolExecutor, build_default_tool_registry

router = APIRouter()


@router.get("", response_model=list[ToolRead])
async def list_tools(user: User = Depends(get_current_user)):
    registry = build_default_tool_registry()
    return [
        ToolRead(
            tool_id=tool.tool_id,
            name=tool.name,
            description=tool.description,
            capabilities=tool.capabilities,
            risk_level=tool.risk_level,
            requires_approval=tool.requires_approval,
        )
        for tool in registry.list_tools()
    ]


@router.post("/{tool_id}/execute", response_model=ToolExecuteResponse)
async def execute_tool(
    tool_id: str,
    payload: ToolExecuteRequest,
    user: User = Depends(get_current_user),
):
    executor = PermissionedToolExecutor()
    try:
        result = await executor.execute(
            tool_id,
            ToolContext(user_id=user.id, role=user.role.value, input=payload.input),
        )
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found") from exc
    return ToolExecuteResponse(
        tool_id=result.tool_id,
        success=result.success,
        output=result.output,
        error=result.error,
    )

