from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.advisor_crud import create_advisor, get_advisor_by_user, get_advisor_by_id, get_all_advisors, update_advisor, delete_advisor      


async def create_advisor_service(db: AsyncSession, actor_name: str, **data):
    if await get_advisor_by_user(db, data["user_id"]):
        raise ValueError("Advisor already exists ")
    # Pass actor_name explicitly
    return await create_advisor(db, actor_name=actor_name, **data)

async def get_advisor_service(db: AsyncSession, advisor_id: int):
    advisor = await get_advisor_by_id(db, advisor_id)
    if not advisor:
        raise ValueError("Advisor not found ")
    return advisor

async def list_advisors_service(db: AsyncSession):
    return await get_all_advisors(db)

async def update_advisor_service(db: AsyncSession, advisor_id: int, actor_name: str, **data):
    advisor = await get_advisor_by_id(db, advisor_id)
    if not advisor:
        raise ValueError("Advisor not found ")
    # Pass actor_name explicitly
    return await update_advisor(db, advisor, actor_name=actor_name, **data)

async def delete_advisor_service(db: AsyncSession, advisor_id: int):
    if not await delete_advisor(db, advisor_id):
        raise ValueError("Advisor not found ")
    return True

