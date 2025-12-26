from sqlalchemy.ext.asyncio import AsyncSession     
from app.crud.user_crud import create_user, get_user_by_id, get_user_by_email, get_all_users, update_user, delete_user

async def create_user_service(db:AsyncSession,user_name:str,user_email:str,actor_name: str):
    if await get_user_by_email(db,user_email):
        raise ValueError("User Already Exists")
    return await create_user(db,user_name,user_email,actor_name)

async def get_user_service(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    return user

async def list_users_service(db:AsyncSession):
    return await get_all_users(db)

async def update_user_service(db: AsyncSession, user_id: int, actor_name: str, user_name=None, user_email=None):
    # Pass the actor_name (from the token) into the CRUD function
    user = await update_user(db, user_id, actor_name, user_name, user_email)
    if not user:
        raise ValueError("User not found")
    return user

async def delete_user_service(db: AsyncSession, user_id: int):
    if not await    delete_user(db, user_id):
        raise ValueError("User not found")
    return True

