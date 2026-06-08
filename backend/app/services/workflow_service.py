from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base import AgentContext
from app.agents.orchestrator import WorkflowOrchestrator
from app.db.models import MemoryType, TaskRun, TaskStatus, WorkflowRun, WorkflowStatus
from app.schemas.api import MemoryCreate, WorkflowCreate
from app.services.memory_service import MemoryService


class WorkflowService:
    def __init__(self, orchestrator: WorkflowOrchestrator | None = None) -> None:
        self.orchestrator = orchestrator or WorkflowOrchestrator()

    async def create(self, session: AsyncSession, user_id: str, payload: WorkflowCreate) -> WorkflowRun:
        workflow = WorkflowRun(
            user_id=user_id,
            goal=payload.goal,
            priority=payload.priority,
            metadata_json=payload.metadata,
        )
        session.add(workflow)
        await session.commit()
        await session.refresh(workflow)
        return workflow

    async def list(self, session: AsyncSession, user_id: str, limit: int = 50) -> list[WorkflowRun]:
        result = await session.scalars(
            select(WorkflowRun)
            .where(WorkflowRun.user_id == user_id)
            .order_by(WorkflowRun.created_at.desc())
            .limit(limit)
        )
        return list(result)

    async def get(self, session: AsyncSession, user_id: str, workflow_id: str) -> WorkflowRun | None:
        return await session.scalar(
            select(WorkflowRun).where(WorkflowRun.user_id == user_id, WorkflowRun.id == workflow_id)
        )

    async def cancel(self, session: AsyncSession, user_id: str, workflow_id: str) -> WorkflowRun | None:
        workflow = await self.get(session, user_id, workflow_id)
        if workflow is None:
            return None
        workflow.status = WorkflowStatus.cancelled
        await session.commit()
        await session.refresh(workflow)
        return workflow

    async def create_task(
        self,
        session: AsyncSession,
        *,
        user_id: str,
        workflow_id: str | None,
        name: str,
        queue: str = "default",
        payload: dict | None = None,
    ) -> TaskRun:
        task = TaskRun(
            user_id=user_id,
            workflow_id=workflow_id,
            name=name,
            queue=queue,
            status=TaskStatus.queued,
            payload=payload or {},
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    async def run_inline(self, session: AsyncSession, user_id: str, workflow_id: str) -> WorkflowRun:
        workflow = await self.get(session, user_id, workflow_id)
        if workflow is None:
            raise ValueError("Workflow not found")
        workflow.status = WorkflowStatus.running
        await session.commit()

        context = AgentContext(
            user_id=user_id,
            goal=workflow.goal,
            workflow_id=workflow.id,
            metadata=workflow.metadata_json,
        )
        try:
            execution = await self.orchestrator.execute(context)
            workflow.plan = execution["plan"]
            workflow.result = execution["result"]
            workflow.status = WorkflowStatus.completed
            for memory_text in execution["result"].get("memory_writes", []):
                await MemoryService().create(
                    session,
                    user_id,
                    MemoryCreate(
                        memory_type=MemoryType.workflow,
                        content=memory_text,
                        source=f"workflow:{workflow.id}",
                    ),
                )
        except Exception as exc:
            workflow.status = WorkflowStatus.failed
            workflow.error = str(exc)
        await session.commit()
        await session.refresh(workflow)
        return workflow

