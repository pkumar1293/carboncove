"""Report generation and download endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.db import EmissionResult, Report
from db.database import get_db
from services.auth import verify_supabase_token

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate/{result_id}")
async def generate_report(
    result_id: str,
    user: dict = Depends(verify_supabase_token),
    db: AsyncSession = Depends(get_db),
):
    """Queue async PDF report generation for a calculation result."""
    result = await db.execute(select(EmissionResult).where(EmissionResult.id == result_id))
    emission_result = result.scalar_one_or_none()
    if not emission_result:
        raise HTTPException(status_code=404, detail="Calculation result not found")

    from tasks.pdf_tasks import generate_report_task
    task = generate_report_task.delay(
        result_id=result_id,
        company_info={"name": user.get("user_metadata", {}).get("company_name", "N/A")},
        installation_info={
            "name": "Installation",
            "scope1_direct": float(emission_result.scope1_direct or 0),
            "scope2_indirect": float(emission_result.scope2_indirect or 0),
            "total_embedded": float(emission_result.total_embedded or 0),
            "specific_embedded": float(emission_result.specific_embedded or 0),
            "eu_default_value": float(emission_result.eu_default_value or 0),
            "cbam_cost_actual": float(emission_result.cbam_cost_actual or 0),
            "cbam_cost_default": float(emission_result.cbam_cost_default or 0),
            "savings_vs_default": float(emission_result.savings_vs_default or 0),
        },
    )
    return {"task_id": task.id, "status": "queued"}


@router.get("/{result_id}")
async def get_report_status(
    result_id: str,
    user: dict = Depends(verify_supabase_token),
    db: AsyncSession = Depends(get_db),
):
    """Check report generation status."""
    result = await db.execute(
        select(Report).where(Report.installation_id == result_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        return {"status": "not_found"}
    return {"status": report.status, "file_url": report.file_url}
