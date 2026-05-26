"""Read dynamic config from app_config table (EUR/INR rate, EU ETS price)."""
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.db import AppConfig


async def get_config(db: AsyncSession, key: str, default: str) -> str:
    """Fetch a config value from DB, fall back to default."""
    result = await db.execute(select(AppConfig).where(AppConfig.key == key))
    row = result.scalar_one_or_none()
    return row.value if row else os.environ.get(key, default)


async def get_eu_ets_price(db: AsyncSession) -> float:
    return float(await get_config(db, "EU_ETS_PRICE_EUR", "80.0"))


async def get_eur_to_inr(db: AsyncSession) -> float:
    return float(await get_config(db, "EUR_TO_INR_RATE", "90.0"))
