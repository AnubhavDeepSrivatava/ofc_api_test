from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.schemas_user  import UserCreate, UserResponse
from app.services.services_user import *
from app.core.security import get_token_user_name

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db) , actor_name: str = Depends(get_token_user_name)):
    try:
        return await create_user_service(db, user.user_name, user.user_email , actor_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await get_user_service(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{user_id}", response_model=UserResponse)
async def update(
    user_id: int, 
    user: UserCreate, 
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
):
    return await update_user_service(db, user_id, actor_name, user.user_name, user.user_email)

