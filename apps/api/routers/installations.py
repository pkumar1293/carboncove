from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from models.db import User, Installation
from services.auth import verify_supabase_token

router = APIRouter(prefix="/installations", tags=["installations"])


class InstallationCreate(BaseModel):
    name: str
    sector: str
    production_route: str
    state: str
    grid_region: str = "default"
    has_captive_power: bool = False
    annual_capacity_tonnes: float | None = None


@router.get("")
async def list_installations(
    user_info: dict = Depends(verify_supabase_token),
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_info["id"])
    if not user:
        return {"installations": []}
    result = await db.execute(
        select(Installation).where(Installation.company_id == user.company_id)
    )
    rows = result.scalars().all()
    return {
        "installations": [
            {
                "id": i.id,
                "company_id": i.company_id,
                "name": i.name,
                "sector": i.sector,
                "production_route": i.production_route,
                "state": i.state,
                "grid_region": i.grid_region,
                "has_captive_power": i.has_captive_power,
                "annual_capacity_tonnes": float(i.annual_capacity_tonnes)
                if i.annual_capacity_tonnes
                else None,
                "created_at": i.created_at.isoformat() if i.created_at else None,
            }
            for i in rows
        ]
    }


@router.post("")
async def create_installation(
    body: InstallationCreate,
    user_info: dict = Depends(verify_supabase_token),
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_info["id"])
    if not user:
        raise HTTPException(status_code=404, detail="Complete company onboarding first")

    inst = Installation(
        company_id=user.company_id,
        name=body.name,
        sector=body.sector,
        production_route=body.production_route,
        state=body.state,
        grid_region=body.grid_region,
        has_captive_power=body.has_captive_power,
        annual_capacity_tonnes=body.annual_capacity_tonnes,
    )
    db.add(inst)
    await db.commit()
    await db.refresh(inst)
    return {"id": inst.id, "status": "created"}
