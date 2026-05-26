"""Scope 1 (direct) emission calculations — EU Reg 2023/1773 calculation-based method."""
from .constants import EMISSION_FACTORS, OXIDATION_FACTOR, PROCESS_EMISSION_FACTORS


def calculate_fuel_combustion(fuel_inputs: list[dict]) -> dict:
    """
    E_combustion = Σ(FC_i × NCV_i × EF_i × OF)
    fuel_inputs: [{"fuel_type": str, "quantity_tonnes": float}, ...]
    Returns: {"total_tco2": float, "breakdown": [...]}
    """
    breakdown = []
    total = 0.0

    for fi in fuel_inputs:
        ft = fi["fuel_type"]
        qty = float(fi["quantity_tonnes"])
        if ft not in EMISSION_FACTORS:
            raise ValueError(f"Unknown fuel type: {ft}")
        ef = EMISSION_FACTORS[ft]
        energy_gj = qty * ef["ncv"]
        tco2 = energy_gj * ef["ef"] * OXIDATION_FACTOR
        total += tco2
        breakdown.append({
            "fuel_type": ft,
            "quantity_tonnes": qty,
            "energy_gj": round(energy_gj, 4),
            "tco2": round(tco2, 6),
            "ncv_used": ef["ncv"],
            "ef_used": ef["ef"],
        })

    return {"total_tco2": round(total, 6), "breakdown": breakdown}


def calculate_process_emissions(
    sector: str,
    production_route: str,
    production_volume_tonnes: float,
    additional_inputs: dict | None = None,
) -> dict:
    """
    Process emissions from industrial reactions (limestone decomp, clinker calcination, PFC).
    Returns: {"total_tco2": float, "breakdown": dict}
    """
    additional_inputs = additional_inputs or {}
    breakdown = {}
    total = 0.0

    sector_factors = PROCESS_EMISSION_FACTORS.get(sector, {})
    route_factors = sector_factors.get(production_route, {})

    if sector == "iron_steel":
        factor = route_factors.get("limestone_decomp_per_tonne", 0.0)
        pe = production_volume_tonnes * factor
        total += pe
        breakdown["limestone_decomposition_tco2"] = round(pe, 6)

    elif sector == "cement":
        clinker_ratio = float(additional_inputs.get("clinker_ratio", 0.75))
        clinker_tonnes = production_volume_tonnes * clinker_ratio
        factor = route_factors.get("clinker_calcination_tco2_per_tonne_clinker", 0.525)
        pe = clinker_tonnes * factor
        total += pe
        breakdown["clinker_tonnes"] = round(clinker_tonnes, 2)
        breakdown["calcination_tco2"] = round(pe, 6)

    elif sector == "aluminium":
        pfc_factor = route_factors.get("pfc_tco2_per_tonne_al", 0.0)
        pe = production_volume_tonnes * pfc_factor
        total += pe
        breakdown["pfc_tco2"] = round(pe, 6)

    return {"total_tco2": round(total, 6), "breakdown": breakdown}


def calculate_scope1_total(
    fuel_inputs: list[dict],
    sector: str,
    production_route: str,
    production_volume_tonnes: float,
    additional_inputs: dict | None = None,
) -> dict:
    """Aggregate Scope 1: combustion + process emissions."""
    combustion = calculate_fuel_combustion(fuel_inputs)
    process = calculate_process_emissions(sector, production_route, production_volume_tonnes, additional_inputs)
    total = combustion["total_tco2"] + process["total_tco2"]
    return {
        "combustion_tco2": combustion["total_tco2"],
        "process_tco2": process["total_tco2"],
        "total_scope1_tco2": round(total, 6),
        "combustion_breakdown": combustion["breakdown"],
        "process_breakdown": process["breakdown"],
    }
