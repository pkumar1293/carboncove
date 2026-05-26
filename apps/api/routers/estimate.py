"""Public free calculator endpoint — no auth required."""
import os
from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from engine.scope1 import calculate_scope1_total
from engine.scope2 import calculate_scope2_total
from engine.cbam_cost import calculate_cbam_financial_impact
from models.requests import QuickEstimateRequest, LeadCaptureRequest
from db.database import get_db
from services.config_service import get_eu_ets_price, get_eur_to_inr
from models.db import Lead

router = APIRouter(prefix="/estimate", tags=["estimate"])
limiter = Limiter(key_func=get_remote_address)


@router.post("")
@limiter.limit("10/minute")
async def quick_estimate(
    request: Request,
    body: QuickEstimateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Public CBAM quick estimate — powers the free calculator.
    Rate limited to 10 req/min per IP.
    """
    try:
        ets_price = await get_eu_ets_price(db)
        eur_inr = await get_eur_to_inr(db)
    except Exception:
        ets_price = float(os.environ.get("EU_ETS_PRICE_EUR", "80"))
        eur_inr = float(os.environ.get("EUR_TO_INR_RATE", "90"))

    export_tonnes = body.annual_production_tonnes * (body.export_to_eu_percent / 100)

    scope1 = calculate_scope1_total(
        fuel_inputs=[fi.model_dump() for fi in body.fuel_inputs],
        sector=body.sector,
        production_route=body.production_route,
        production_volume_tonnes=body.annual_production_tonnes,
    )
    scope2 = calculate_scope2_total(
        grid_mwh=body.electricity_mwh,
        grid_region=body.grid_region,
        has_captive_power=body.has_captive_power,
        captive_fuel_type=body.captive_fuel_type,
        captive_fuel_tonnes=body.captive_fuel_tonnes,
    )
    total_embedded = scope1["total_scope1_tco2"] + scope2["total_scope2_tco2"]

    cbam = calculate_cbam_financial_impact(
        total_embedded_tco2=total_embedded,
        production_tonnes=body.annual_production_tonnes,
        export_to_eu_tonnes=export_tonnes,
        cn_code=body.cn_code,
        eu_ets_price_eur=ets_price,
        eur_to_inr=eur_inr,
    )

    return {
        **cbam,
        "scope1_detail": scope1,
        "scope2_detail": scope2,
        "calculation_version": "1.0",
    }


@router.post("/lead")
async def capture_lead(body: LeadCaptureRequest, db: AsyncSession = Depends(get_db)):
    """Save lead after calculator completion."""
    try:
        from sqlalchemy.dialects.postgresql import insert
        lead_data = body.model_dump(exclude={"wants_consultation"})
        stmt = insert(Lead).values(**lead_data).on_conflict_do_nothing(index_elements=["email"])
        await db.execute(stmt)
        await db.commit()
    except Exception:
        pass
    return {"status": "captured"}
