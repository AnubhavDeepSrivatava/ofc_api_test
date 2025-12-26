from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.jury_crud import create_jury, get_jury_by_user, get_jury_by_id, get_juries, update_jury, delete_jury


async def create_jury_service(db: AsyncSession,actor_name: str, **data):
    if await get_jury_by_user(db, data["user_id"]):
        raise ValueError("Jury already exists")
    return await create_jury(db,actor_name=actor_name, **data)

async def get_jury_service(db: AsyncSession, jury_id: int):
    jury = await get_jury_by_id(db, jury_id)
    if not jury:
        raise ValueError("Jury not found ")
    return jury

async def list_juries_service(db: AsyncSession, skip: int, limit: int):
    return await get_juries(db, skip, limit)

async def update_jury_service(db: AsyncSession, jury_id: int,actor_name: str, **data):
    jury = await get_jury_by_id(db, jury_id)
    if not jury:
        raise ValueError("Jury not found ")
    return await update_jury(db, jury, actor_name=actor_name, **data)

async def delete_jury_service(db: AsyncSession, jury_id: int):
    jury = await get_jury_by_id(db, jury_id)
    if not jury:
        raise ValueError("Jury not found ")
    return await delete_jury(db, jury)

