"""Pydantic v2 response models."""
from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    status: str
    version: str
    service: str


class EstimateResponse(BaseModel):
    specific_embedded_tco2_per_tonne: float
    eu_default_tco2_per_tonne: float
    total_embedded_tco2: float
    export_to_eu_tonnes: float
    cbam_cost_actual_eur: float
    cbam_cost_actual_inr: float
    cbam_cost_default_eur: float
    cbam_cost_default_inr: float
    savings_eur: float
    savings_inr: float
    eu_ets_price_eur: float
    eur_to_inr_rate: float
    cn_code: str
    eu_default_product_name: str
    scope1_detail: dict
    scope2_detail: dict
    calculation_version: str


class LeadCaptureResponse(BaseModel):
    status: str


class CalculationResponse(BaseModel):
    result_id: str
    specific_embedded_tco2_per_tonne: float
    eu_default_tco2_per_tonne: float
    cbam_cost_actual_eur: float
    cbam_cost_actual_inr: float
    cbam_cost_default_eur: float
    cbam_cost_default_inr: float
    savings_eur: float
    savings_inr: float
    scope1_detail: dict
    scope2_detail: dict
