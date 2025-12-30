from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.schemas_jury import JuryCreate, JuryResponse
from app.services import services
from app.core.security import get_token_user_name

router = APIRouter(prefix="/juries", tags=["Juries"])


@router.post("/", response_model=JuryResponse)
async def create_jury(
    jury: JuryCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
):
    return await services.create_entity(db, "jury", jury.model_dump(), actor_name)


@router.get("/{jury_id}", response_model=JuryResponse)
async def get_jury(
    jury_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.get_entity(db, "jury", jury_id)


@router.get("/", response_model=list[JuryResponse])
async def list_juries(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await services.list_entity(db, "jury", skip=skip, limit=limit)


@router.put("/{jury_id}", response_model=JuryResponse)
async def update_jury(
    jury_id: int,
    jury: JuryCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
):
    return await services.update_entity(db, "jury", jury_id, jury.model_dump(), actor_name)


@router.delete("/{jury_id}")
async def delete_jury(
    jury_id: int,
    db: AsyncSession = Depends(get_db),
):
    await services.delete_entity(db, "jury", jury_id)
    return {"message": "Jury deleted successfully"}

