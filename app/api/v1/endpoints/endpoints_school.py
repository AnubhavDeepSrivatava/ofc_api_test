from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services import services
from app.schemas.schema_school import (
    SchoolCreate,
    SchoolUpdate,
    SchoolResponse,
)

router = APIRouter(
    prefix="/schools",
    tags=["School"]
)


@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def create_school(
    payload: SchoolCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = "system"
):
    return await services.create_entity(db, "school", payload.model_dump(), actor_name)


@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.get_entity(db, "school", school_id)


@router.get("/", response_model=list[SchoolResponse])
async def get_schools(
    db: AsyncSession = Depends(get_db),
):
    return await services.list_entity(db, "school")


@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_school(
    school_id: int,
    db: AsyncSession = Depends(get_db),
):
    await services.delete_entity(db, "school", school_id)
    return None
