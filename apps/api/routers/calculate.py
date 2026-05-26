"""Authenticated full calculation endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from engine.scope1 import calculate_scope1_total
from engine.scope2 import calculate_scope2_total
from engine.cbam_cost import calculate_cbam_financial_impact
from models.requests import FullCalculationRequest
from models.db import EmissionResult
from db.database import get_db
from services.auth import verify_supabase_token
from services.config_service import get_eu_ets_price, get_eur_to_inr

router = APIRouter(prefix="/calculate", tags=["calculate"])


@router.post("")
async def full_calculation(
    body: FullCalculationRequest,
    user: dict = Depends(verify_supabase_token),
    db: AsyncSession = Depends(get_db),
):
    """Full CBAM calculation — authenticated, saves result to DB."""
    ets_price = await get_eu_ets_price(db)
    eur_inr = await get_eur_to_inr(db)

    scope1 = calculate_scope1_total(
        fuel_inputs=[fi.model_dump() for fi in body.fuel_inputs],
        sector=body.sector,
        production_route=body.production_route,
        production_volume_tonnes=body.production_volume_tonnes,
        additional_inputs=body.additional_process_inputs,
    )
    scope2 = calculate_scope2_total(
        grid_mwh=body.electricity_grid_mwh,
        grid_region=body.grid_region,
        has_captive_power=body.has_captive_power,
        captive_fuel_type=body.captive_fuel_type,
        captive_fuel_tonnes=body.captive_fuel_tonnes,
        captive_elec_mwh=body.captive_electricity_mwh,
    )
    total_embedded = scope1["total_scope1_tco2"] + scope2["total_scope2_tco2"]

    cbam = calculate_cbam_financial_impact(
        total_embedded_tco2=total_embedded,
        production_tonnes=body.production_volume_tonnes,
        export_to_eu_tonnes=body.export_to_eu_tonnes,
        cn_code=body.cn_code,
        eu_ets_price_eur=ets_price,
        eur_to_inr=eur_inr,
    )

    savings_tco2 = (cbam["eu_default_tco2_per_tonne"] - cbam["specific_embedded_tco2_per_tonne"]) * body.export_to_eu_tonnes

    result = EmissionResult(
        installation_id=body.installation_id,
        reporting_period_start=body.reporting_period_start,
        reporting_period_end=body.reporting_period_end,
        scope1_direct=scope1["total_scope1_tco2"],
        scope2_indirect=scope2["total_scope2_tco2"],
        total_embedded=total_embedded,
        production_volume=body.production_volume_tonnes,
        specific_embedded=cbam["specific_embedded_tco2_per_tonne"],
        eu_default_value=cbam["eu_default_tco2_per_tonne"],
        savings_vs_default=savings_tco2,
        eu_ets_price_used=ets_price,
        eur_to_inr_rate=eur_inr,
        cbam_cost_actual=cbam["cbam_cost_actual_inr"],
        cbam_cost_default=cbam["cbam_cost_default_inr"],
        input_data={"scope1": scope1, "scope2": scope2, "request": body.model_dump(mode="json")},
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)

    return {"result_id": str(result.id), **cbam, "scope1_detail": scope1, "scope2_detail": scope2}


@router.get("/sectors")
async def list_sectors():
    """List all CBAM sectors with routes and CN codes — no auth."""
    from engine.constants import EU_DEFAULT_VALUES, PROCESS_EMISSION_FACTORS
    return {"sectors": list(PROCESS_EMISSION_FACTORS.keys()), "cn_codes": EU_DEFAULT_VALUES}


@router.get("/emission-factors")
async def list_emission_factors():
    """List all fuel emission factors — no auth."""
    from engine.constants import EMISSION_FACTORS
    return {"emission_factors": EMISSION_FACTORS}
