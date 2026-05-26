"""Seed reference data into local PostgreSQL."""
import asyncio
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from db.database import AsyncSessionLocal
from models.db import EmissionFactor, CeaGridFactor, EuDefaultValue, AppConfig


EMISSION_FACTORS = [
    {"fuel_type": "coal",         "ncv_gj_per_tonne": 26.7,  "ef_tco2_per_gj": 0.0946, "source": "IPCC_2006"},
    {"fuel_type": "coke",         "ncv_gj_per_tonne": 28.2,  "ef_tco2_per_gj": 0.1075, "source": "IPCC_2006"},
    {"fuel_type": "natural_gas",  "ncv_gj_per_tonne": 44.4,  "ef_tco2_per_gj": 0.0561, "source": "IPCC_2006"},
    {"fuel_type": "diesel",       "ncv_gj_per_tonne": 43.0,  "ef_tco2_per_gj": 0.0741, "source": "IPCC_2006"},
    {"fuel_type": "furnace_oil",  "ncv_gj_per_tonne": 40.4,  "ef_tco2_per_gj": 0.0774, "source": "IPCC_2006"},
    {"fuel_type": "petcoke",      "ncv_gj_per_tonne": 32.5,  "ef_tco2_per_gj": 0.0971, "source": "IPCC_2006"},
    {"fuel_type": "LPG",          "ncv_gj_per_tonne": 47.3,  "ef_tco2_per_gj": 0.0632, "source": "IPCC_2006"},
]

CEA_GRID_FACTORS = [
    {"grid_region": "Northern",      "year": 2024, "ef_tco2_per_mwh": 0.7078},
    {"grid_region": "Southern",      "year": 2024, "ef_tco2_per_mwh": 0.6987},
    {"grid_region": "Eastern",       "year": 2024, "ef_tco2_per_mwh": 0.9196},
    {"grid_region": "Western",       "year": 2024, "ef_tco2_per_mwh": 0.8038},
    {"grid_region": "North-Eastern", "year": 2024, "ef_tco2_per_mwh": 0.6023},
    {"grid_region": "Andaman",       "year": 2024, "ef_tco2_per_mwh": 0.9100},
    {"grid_region": "default",       "year": 2024, "ef_tco2_per_mwh": 0.7828},
]

EU_DEFAULTS = [
    {"cn_code": "7206.10", "product_name": "Crude steel (BF-BOF)",              "default_value_tco2_per_tonne": 2.559},
    {"cn_code": "7214.20", "product_name": "TMT bars / rebar",                  "default_value_tco2_per_tonne": 2.171},
    {"cn_code": "7208.10", "product_name": "Hot rolled coil",                   "default_value_tco2_per_tonne": 2.275},
    {"cn_code": "7601.10", "product_name": "Unwrought aluminium (primary)",      "default_value_tco2_per_tonne": 6.070},
    {"cn_code": "7601.20", "product_name": "Secondary aluminium (unwrought)",    "default_value_tco2_per_tonne": 0.937},
    {"cn_code": "7604.10", "product_name": "Aluminium bars and rods",            "default_value_tco2_per_tonne": 6.256},
    {"cn_code": "2523.10", "product_name": "Cement clinker",                     "default_value_tco2_per_tonne": 0.812},
    {"cn_code": "2523.29", "product_name": "OPC cement",                         "default_value_tco2_per_tonne": 0.791},
    {"cn_code": "3102.10", "product_name": "Urea (fertiliser)",                  "default_value_tco2_per_tonne": 2.478},
    {"cn_code": "2804.10", "product_name": "Hydrogen",                           "default_value_tco2_per_tonne": 8.900},
]

APP_CONFIG = [
    {"key": "EU_ETS_PRICE_EUR",  "value": "80.0",  "description": "Current EU ETS carbon price in EUR per tonne CO2"},
    {"key": "EUR_TO_INR_RATE",   "value": "90.0",  "description": "EUR to INR conversion rate"},
    {"key": "CBAM_REG_VERSION",  "value": "2023/1773", "description": "EU CBAM regulation version in use"},
]


async def seed():
    async with AsyncSessionLocal() as db:
        for ef in EMISSION_FACTORS:
            db.add(EmissionFactor(**ef, valid_from=date(2024, 1, 1)))
        for gf in CEA_GRID_FACTORS:
            db.add(CeaGridFactor(**gf))
        for eu in EU_DEFAULTS:
            db.add(EuDefaultValue(**eu, valid_from=date(2024, 1, 1)))
        for cfg in APP_CONFIG:
            db.add(AppConfig(**cfg))
        await db.commit()
        print("✅ Seed data inserted successfully")


if __name__ == "__main__":
    asyncio.run(seed())
