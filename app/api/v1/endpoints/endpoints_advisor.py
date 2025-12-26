from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.schemas_advisor import AdvisorCreate, AdvisorResponse
from app.services.services_advisor import (
    create_advisor_service,
    get_advisor_service,
    list_advisors_service,
    update_advisor_service,
    delete_advisor_service,
)
from app.core.security import get_token_user_name

router = APIRouter(prefix="/advisors", tags=["Advisors"])


@router.post("/", response_model=AdvisorResponse)
async def create_advisor(
    advisor: AdvisorCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name) # Requires token in Header
):
    try:
        return await create_advisor_service(db, actor_name=actor_name, **advisor.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{advisor_id}", response_model=AdvisorResponse)
async def get_advisor(
    advisor_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_advisor_service(db, advisor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[AdvisorResponse])
async def list_advisors(
    db: AsyncSession = Depends(get_db),
):
    return await list_advisors_service(db)


@router.put("/{advisor_id}", response_model=AdvisorResponse)
async def update_advisor(
    advisor_id: int,
    advisor: AdvisorCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name) # Requires token in Header
):
    try:
        return await update_advisor_service(
            db,
            advisor_id,
            actor_name=actor_name,
            **advisor.model_dump(),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{advisor_id}")
async def delete_advisor(
    advisor_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        await delete_advisor_service(db, advisor_id)
        return {"message": "Advisor deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

