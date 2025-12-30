from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services import services
from app.schemas.schema_activity import (
    ActivityCreate,
    ActivityUpdate,
    ActivityResponse,
)

router = APIRouter(
    prefix="/activities",
    tags=["Activity"]
)


@router.post("/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    payload: ActivityCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = "system"
):
    return await services.create_entity(db, "activity", payload.model_dump(), actor_name)


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.get_entity(db, "activity", activity_id)


@router.get("/", response_model=list[ActivityResponse])
async def get_activities(
    db: AsyncSession = Depends(get_db),
):
    return await services.list_entity(db, "activity")


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
):
    await services.delete_entity(db, "activity", activity_id)
    return None
