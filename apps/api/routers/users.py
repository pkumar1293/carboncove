from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from models.db import User, Company
from services.auth import verify_supabase_token

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_me(
    user_info: dict = Depends(verify_supabase_token),
    db: AsyncSession = Depends(get_db),
):
    user_id = user_info["id"]
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not provisioned. Complete onboarding.")
    company = await db.get(Company, user.company_id)
    return {
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "role": user.role,
            "company_id": user.company_id,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        },
        "company": {
            "id": company.id,
            "name": company.name,
            "contact_email": company.contact_email,
            "subscription_tier": company.subscription_tier,
        }
        if company
        else None,
    }
