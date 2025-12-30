from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.schemas_user import UserCreate, UserResponse
from app.services import services
from app.core.security import get_token_user_name
from app.core.responses import JSendRoute

router = APIRouter(prefix="/users", tags=["Users"], route_class=JSendRoute)

@router.post("/", response_model=UserResponse)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db), actor_name: str = Depends(get_token_user_name)):
    return await services.create_entity(db, "user", user.model_dump(), actor_name)

@router.get("/{user_id}", response_model=UserResponse)
async def get(user_id: int, db: AsyncSession = Depends(get_db)):
    return await services.get_entity(db, "user", user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update(
    user_id: int, 
    user: UserCreate, 
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
):
    return await services.update_entity(db, "user", user_id, user.model_dump(), actor_name)

