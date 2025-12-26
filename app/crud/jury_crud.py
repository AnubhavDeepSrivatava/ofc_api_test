from sqlalchemy.ext.asyncio import AsyncSession
from app.models.jury import Jury
from sqlalchemy import select

async def create_jury(
    db: AsyncSession,
    user_id: int,
    jury_name: str,
    jury_email: str,
    actor_name: str
) -> Jury:
    jury = Jury(
        user_id=user_id,
        jury_name=jury_name,
        jury_email=jury_email,
        created_by=actor_name, # Requirement: store name of creator
        updated_by=None
    )
    db.add(jury)
    await db.commit()
    await db.refresh(jury)
    return jury

async def get_jury_by_user(
    db: AsyncSession,
    user_id: int
) -> Jury | None:
    result = await db.execute(select(Jury).where(Jury.user_id == user_id))
    return result.scalar_one_or_none()

async def get_jury_by_id(
    db: AsyncSession,
    jury_id: int
) -> Jury | None:
    result = await db.execute(select(Jury).where(Jury.jury_id == jury_id))
    return result.scalar_one_or_none()


async def get_juries(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> list[Jury]:
    result = await db.execute(
    select(Jury).offset(skip).limit(limit)
)
    return result.scalars().all()


async def update_jury(
    db: AsyncSession,
    jury: Jury,
    actor_name: str,
    jury_name: str | None = None,
    jury_email: str | None = None
) -> Jury:
    if jury_name is not None:
        jury.jury_name = jury_name

    if jury_email is not None:
        jury.jury_email = jury_email

    jury.updated_by = actor_name # Track who updated it
    
    await db.commit()
    await db.refresh(jury)
    return jury

async def delete_jury(
    db: AsyncSession,
    jury: Jury
) -> bool:
    await db.delete(jury)
    await db.commit()
    return True

