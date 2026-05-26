"""Scope 2 (indirect) emission calculations."""
from .constants import CEA_GRID_FACTORS, EMISSION_FACTORS


def calculate_grid_electricity_emissions(electricity_mwh: float, grid_region: str) -> dict:
    """E = electricity_MWh × CEA_grid_factor (tCO2/MWh)"""
    factor = CEA_GRID_FACTORS.get(grid_region, CEA_GRID_FACTORS["default"])
    tco2 = electricity_mwh * factor
    return {
        "electricity_mwh": electricity_mwh,
        "grid_region": grid_region,
        "cea_factor_tco2_per_mwh": factor,
        "grid_tco2": round(tco2, 6),
    }


def calculate_captive_power_emissions(
    fuel_type: str,
    fuel_tonnes: float,
    electricity_generated_mwh: float,
) -> dict:
    """Emissions from captive power plant fuel combustion."""
    if fuel_type not in EMISSION_FACTORS:
        raise ValueError(f"Unknown captive fuel type: {fuel_type}")
    ef = EMISSION_FACTORS[fuel_type]
    energy_gj = fuel_tonnes * ef["ncv"]
    tco2 = energy_gj * ef["ef"]
    implied_ef = tco2 / electricity_generated_mwh if electricity_generated_mwh > 0 else 0
    return {
        "fuel_type": fuel_type,
        "fuel_tonnes": fuel_tonnes,
        "electricity_generated_mwh": electricity_generated_mwh,
        "captive_tco2": round(tco2, 6),
        "implied_ef_tco2_per_mwh": round(implied_ef, 6),
    }


def calculate_scope2_total(
    grid_mwh: float,
    grid_region: str,
    has_captive_power: bool = False,
    captive_fuel_type: str | None = None,
    captive_fuel_tonnes: float = 0.0,
    captive_elec_mwh: float = 0.0,
) -> dict:
    """Aggregate Scope 2: grid + captive power emissions."""
    grid = calculate_grid_electricity_emissions(grid_mwh, grid_region)
    captive_tco2 = 0.0
    captive_detail = None

    if has_captive_power and captive_fuel_type and captive_fuel_tonnes > 0:
        captive = calculate_captive_power_emissions(captive_fuel_type, captive_fuel_tonnes, captive_elec_mwh)
        captive_tco2 = captive["captive_tco2"]
        captive_detail = captive

    total = grid["grid_tco2"] + captive_tco2
    return {
        "grid_tco2": grid["grid_tco2"],
        "captive_tco2": captive_tco2,
        "total_scope2_tco2": round(total, 6),
        "grid_detail": grid,
        "captive_detail": captive_detail,
    }
