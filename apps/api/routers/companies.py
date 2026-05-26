from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from models.db import User, Company
from services.auth import verify_supabase_token

router = APIRouter(prefix="/companies", tags=["companies"])


class CompanyCreate(BaseModel):
    name: str
    contact_email: EmailStr
    contact_name: str | None = None
    gstin: str | None = None
    state: str | None = None
    city: str | None = None


@router.post("")
async def create_company(
    body: CompanyCreate,
    user_info: dict = Depends(verify_supabase_token),
    db: AsyncSession = Depends(get_db),
):
    user_id = user_info["id"]
    existing = await db.get(User, user_id)
    if existing:
        raise HTTPException(status_code=400, detail="User already has a company")

    company = Company(
        name=body.name,
        contact_email=body.contact_email,
        contact_name=body.contact_name,
        gstin=body.gstin,
        state=body.state,
        city=body.city,
        subscription_tier="free",
    )
    db.add(company)
    await db.flush()

    user = User(
        id=user_id,
        company_id=company.id,
        full_name=user_info.get("user_metadata", {}).get("full_name"),
        role="owner",
    )
    db.add(user)
    await db.commit()
    await db.refresh(company)
    return {"company_id": company.id, "status": "created"}
