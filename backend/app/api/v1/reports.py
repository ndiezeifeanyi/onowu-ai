from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.api import ReportGenerateRequest, ReportRead
from app.services.report_service import ReportService

router = APIRouter()


@router.get("", response_model=list[ReportRead])
async def list_reports(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await ReportService().list(session, user.id)


@router.post("/generate", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
async def generate_report(
    payload: ReportGenerateRequest,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await ReportService().generate(session, user.id, payload)

