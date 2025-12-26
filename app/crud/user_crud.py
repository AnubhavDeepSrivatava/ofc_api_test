from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select


async def create_user(db:AsyncSession, user_name:str , user_email:str , creator_name: str) -> User:
    user = User(user_name=user_name, user_email=user_email)
    # Value from token (the name found via the ID)
    user.created_by = creator_name
    # Explicitly null on start
    user.updated_by = None

    db.add(user)

    
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_id(db:AsyncSession , user_id:int) -> User | None:
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db:AsyncSession ,user_email:str) -> User | None:
    result = await db.execute(select(User).where(User.user_email == user_email))
    return result.scalar_one_or_none()


async def get_all_users(db:AsyncSession) -> list[User]:   #abhi isme issue ahin size define nahi hain
    result = await db.execute(select(User))
    return result.scalars().all()


async def update_user(
    db: AsyncSession,
    user_id: int,
    updater_name: str,
    user_name: str | None = None,
    user_email: str | None = None
) -> User | None:
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()


    if not user:
        return None

    if user_name is not None:
        user.user_name = user_name

    if user_email is not None:
        user.user_email = user_email

    user.updated_by = updater_name
    
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db:AsyncSession , user_id:int) -> bool:
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True

