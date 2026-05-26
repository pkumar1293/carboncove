"""CBAM financial impact calculation."""
from .constants import EU_DEFAULT_VALUES


def calculate_cbam_financial_impact(
    total_embedded_tco2: float,
    production_tonnes: float,
    export_to_eu_tonnes: float,
    cn_code: str,
    eu_ets_price_eur: float = 80.0,
    eur_to_inr: float = 90.0,
    ccts_carbon_price_inr: float = 0.0,
) -> dict:
    """
    Calculate actual vs EU-default CBAM cost and savings.

    specific_embedded = total_embedded / production_tonnes   (tCO2/tonne product)
    cbam_actual = specific_embedded × export_tonnes × ets_price
    cbam_default = eu_default[cn_code] × export_tonnes × ets_price
    savings = cbam_default - cbam_actual
    """
    if production_tonnes <= 0:
        raise ValueError("production_tonnes must be > 0")

    specific_embedded = total_embedded_tco2 / production_tonnes

    eu_default = EU_DEFAULT_VALUES.get(cn_code)
    if eu_default is None:
        raise ValueError(f"No EU default value for CN code: {cn_code}")
    eu_default_tco2 = eu_default["value"]

    cbam_actual_eur = specific_embedded * export_to_eu_tonnes * eu_ets_price_eur
    cbam_default_eur = eu_default_tco2 * export_to_eu_tonnes * eu_ets_price_eur
    savings_eur = cbam_default_eur - cbam_actual_eur

    cbam_actual_inr = cbam_actual_eur * eur_to_inr
    cbam_default_inr = cbam_default_eur * eur_to_inr
    savings_inr = savings_eur * eur_to_inr

    # Carbon credit offset (Indian CCTS if applicable)
    ccts_offset_inr = ccts_carbon_price_inr * export_to_eu_tonnes * specific_embedded
    net_cbam_inr = max(0, cbam_actual_inr - ccts_offset_inr)

    return {
        "specific_embedded_tco2_per_tonne": round(specific_embedded, 6),
        "eu_default_tco2_per_tonne": eu_default_tco2,
        "total_embedded_tco2": round(total_embedded_tco2, 6),
        "export_to_eu_tonnes": export_to_eu_tonnes,
        "cbam_cost_actual_eur": round(cbam_actual_eur, 2),
        "cbam_cost_actual_inr": round(cbam_actual_inr, 2),
        "cbam_cost_default_eur": round(cbam_default_eur, 2),
        "cbam_cost_default_inr": round(cbam_default_inr, 2),
        "savings_eur": round(savings_eur, 2),
        "savings_inr": round(savings_inr, 2),
        "ccts_offset_inr": round(ccts_offset_inr, 2),
        "net_cbam_inr": round(net_cbam_inr, 2),
        "eu_ets_price_eur": eu_ets_price_eur,
        "eur_to_inr_rate": eur_to_inr,
        "cn_code": cn_code,
        "eu_default_product_name": eu_default["name"],
    }
