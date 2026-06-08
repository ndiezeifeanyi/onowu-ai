from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Report
from app.schemas.api import ReportGenerateRequest


class ReportService:
    async def generate(
        self, session: AsyncSession, user_id: str, payload: ReportGenerateRequest
    ) -> Report:
        title = payload.title or f"{payload.report_type.title()} Personal AI OS Briefing"
        content = (
            f"# {title}\n\n"
            f"Window: {payload.source_window}\n\n"
            "- Workflow activity will be summarized from recent runs.\n"
            "- Scholarship and research updates are pulled from agent outputs.\n"
            "- Notifications and reminders are included when configured.\n"
        )
        report = Report(
            user_id=user_id,
            report_type=payload.report_type,
            title=title,
            content=content,
            summary="Generated briefing from current Personal AI OS state.",
        )
        session.add(report)
        await session.commit()
        await session.refresh(report)
        return report

    async def list(self, session: AsyncSession, user_id: str) -> list[Report]:
        result = await session.scalars(
            select(Report).where(Report.user_id == user_id).order_by(Report.created_at.desc()).limit(50)
        )
        return list(result)

