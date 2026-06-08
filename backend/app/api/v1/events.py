from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.services.event_service import WorkflowEventService
from app.services.workflow_service import WorkflowService

router = APIRouter()


@router.get("/workflows/{workflow_id}")
async def stream_workflow_events(
    workflow_id: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    workflow = await WorkflowService().get(session, user.id, workflow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return StreamingResponse(
        WorkflowEventService().stream(workflow_id),
        media_type="text/event-stream",
    )
