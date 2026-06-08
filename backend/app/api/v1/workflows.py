from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.api import WorkflowCreate, WorkflowRead
from app.services.workflow_service import WorkflowService

router = APIRouter()


@router.post("", response_model=WorkflowRead, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    payload: WorkflowCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = WorkflowService()
    workflow = await service.create(session, user.id, payload)
    if payload.enqueue:
        await service.create_task(
            session,
            user_id=user.id,
            workflow_id=workflow.id,
            name="workflow.run",
            queue="agents",
            payload={"workflow_id": workflow.id},
        )
        try:
            from app.workers.tasks import run_workflow_task

            run_workflow_task.delay(workflow.id, user.id)
        except Exception:
            pass
    return workflow


@router.get("", response_model=list[WorkflowRead])
async def list_workflows(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await WorkflowService().list(session, user.id)


@router.get("/{workflow_id}", response_model=WorkflowRead)
async def get_workflow(
    workflow_id: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    workflow = await WorkflowService().get(session, user.id, workflow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return workflow


@router.post("/{workflow_id}/cancel", response_model=WorkflowRead)
async def cancel_workflow(
    workflow_id: str,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    workflow = await WorkflowService().cancel(session, user.id, workflow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return workflow

