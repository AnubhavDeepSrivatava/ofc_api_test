from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.schemas_jury import JuryCreate, JuryResponse
from app.services.services_jury import (
    create_jury_service,
    get_jury_service,
    list_juries_service,
    update_jury_service,
    delete_jury_service,
)
from app.core.security import get_token_user_name
router = APIRouter(prefix="/juries", tags=["Juries"])


@router.post("/", response_model=JuryResponse)
async def create_jury(
    jury: JuryCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
):
    try:
        return await create_jury_service(db, actor_name=actor_name, **jury.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{jury_id}", response_model=JuryResponse)
async def get_jury(
    jury_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_jury_service(db, jury_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[JuryResponse])
async def list_juries(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await list_juries_service(db, skip, limit)


@router.put("/{jury_id}", response_model=JuryResponse)
async def update_jury(
    jury_id: int,
    jury: JuryCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
):
    try:
        return await update_jury_service(
            db,
            jury_id,
            actor_name=actor_name,
            **jury.model_dump(),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{jury_id}")
async def delete_jury(
    jury_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        await delete_jury_service(db, jury_id)
        return {"message": "Jury deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

