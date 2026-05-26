"""Pydantic v2 request models."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class FuelInput(BaseModel):
    fuel_type: str
    quantity_tonnes: float = Field(gt=0)


class QuickEstimateRequest(BaseModel):
    sector: str
    production_route: str
    annual_production_tonnes: float = Field(gt=0)
    export_to_eu_percent: float = Field(ge=0, le=100)
    grid_region: str = "default"
    cn_code: str
    fuel_inputs: list[FuelInput] = Field(default_factory=list)
    electricity_mwh: float = Field(default=0.0, ge=0)
    has_captive_power: bool = False
    captive_fuel_type: Optional[str] = None
    captive_fuel_tonnes: float = 0.0
    eu_ets_price_eur: float = 80.0
    eur_to_inr: float = 90.0


class FullCalculationRequest(BaseModel):
    installation_id: str
    reporting_period_start: date
    reporting_period_end: date
    production_volume_tonnes: float = Field(gt=0)
    export_to_eu_tonnes: float = Field(ge=0)
    cn_code: str
    fuel_inputs: list[FuelInput]
    electricity_grid_mwh: float = Field(ge=0)
    has_captive_power: bool = False
    captive_fuel_type: Optional[str] = None
    captive_fuel_tonnes: float = 0.0
    captive_electricity_mwh: float = 0.0
    grid_region: str = "default"
    sector: str
    production_route: str
    additional_process_inputs: Optional[dict] = None


class LeadCaptureRequest(BaseModel):
    email: str
    company_name: Optional[str] = None
    sector: Optional[str] = None
    annual_export_tonnes: Optional[float] = None
    estimated_cbam_cost: Optional[float] = None
    utm_source: Optional[str] = None
    wants_consultation: bool = False
