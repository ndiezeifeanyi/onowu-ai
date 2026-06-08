import asyncio

from sqlalchemy import select

from app.db.models import TaskRun, TaskStatus
from app.db.session import AsyncSessionLocal
from app.services.event_service import WorkflowEventService
from app.services.workflow_service import WorkflowService
from app.workers.celery_app import celery_app


@celery_app.task(name="workflows.run", autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def run_workflow_task(workflow_id: str, user_id: str) -> dict:
    return asyncio.run(_run_workflow(workflow_id, user_id))


async def _run_workflow(workflow_id: str, user_id: str) -> dict:
    async with AsyncSessionLocal() as session:
        await WorkflowEventService().publish(
            workflow_id, {"status": "running", "message": "Workflow execution started"}
        )
        workflow = await WorkflowService().run_inline(session, user_id, workflow_id)
        task = await session.scalar(
            select(TaskRun).where(TaskRun.workflow_id == workflow_id, TaskRun.name == "workflow.run")
        )
        if task is not None:
            task.status = TaskStatus.completed if workflow.error is None else TaskStatus.failed
            task.result = workflow.result
            task.error = workflow.error
            await session.commit()
        await WorkflowEventService().publish(
            workflow_id,
            {
                "status": workflow.status.value,
                "message": "Workflow execution finished",
                "result": workflow.result,
            },
        )
        return {"workflow_id": workflow.id, "status": workflow.status.value}


@celery_app.task(name="reports.generate")
def generate_report_task() -> dict:
    return {"status": "scheduled", "task": "reports.generate"}


@celery_app.task(name="scholarships.scan")
def scholarship_scan_task() -> dict:
    return {"status": "scheduled", "task": "scholarships.scan"}


@celery_app.task(name="research.scan")
def research_scan_task() -> dict:
    return {"status": "scheduled", "task": "research.scan"}


@celery_app.task(name="notifications.dispatch")
def dispatch_notifications_task() -> dict:
    return {"status": "scheduled", "task": "notifications.dispatch"}


@celery_app.task(name="browser.run")
def browser_run_task() -> dict:
    return {"status": "scheduled", "task": "browser.run"}

