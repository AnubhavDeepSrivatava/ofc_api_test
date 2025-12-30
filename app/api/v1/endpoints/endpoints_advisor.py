from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.schemas_advisor import AdvisorCreate, AdvisorResponse
from app.services import services
from app.core.security import get_token_user_name

router = APIRouter(prefix="/advisors", tags=["Advisors"])


@router.post("/", response_model=AdvisorResponse)
async def create_advisor(
    advisor: AdvisorCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
):
    return await services.create_entity(db, "advisor", advisor.model_dump(), actor_name)


@router.get("/{advisor_id}", response_model=AdvisorResponse)
async def get_advisor(
    advisor_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.get_entity(db, "advisor", advisor_id)


@router.get("/", response_model=list[AdvisorResponse])
async def list_advisors(
    db: AsyncSession = Depends(get_db),
):
    return await services.list_entity(db, "advisor")


@router.put("/{advisor_id}", response_model=AdvisorResponse)
async def update_advisor(
    advisor_id: int,
    advisor: AdvisorCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
):
    return await services.update_entity(db, "advisor", advisor_id, advisor.model_dump(), actor_name)


@router.delete("/{advisor_id}")
async def delete_advisor(
    advisor_id: int,
    db: AsyncSession = Depends(get_db),
):
    await services.delete_entity(db, "advisor", advisor_id)
    return {"message": "Advisor deleted successfully"}

