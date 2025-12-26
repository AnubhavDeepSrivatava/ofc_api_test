from sqlalchemy.ext.asyncio import AsyncSession
from app.models.advisor import Advisor
from sqlalchemy import select

async def create_advisor(
    db: AsyncSession, 
    user_id: int, 
    advisor_name: str, 
    team: str, 
    actor_name: str  # NEW: Name from token
) -> Advisor:
    advisor = Advisor(
        user_id=user_id,
        advisor_name=advisor_name,
        team=team,
        created_by=actor_name, # Storing the name from token
        updated_by=None        # Null on first entry
    )
    db.add(advisor)
    await db.commit()
    await db.refresh(advisor)
    return advisor

async def get_advisor_by_user(db:AsyncSession , user_id:int) ->Advisor |None:
    result = await db.execute(select(Advisor).where(Advisor.user_id == user_id))
    return result.scalar_one_or_none()

async def get_advisor_by_id(db:AsyncSession , advisor_id:int) ->Advisor | None:
    result = await db.execute(select(Advisor).where(Advisor.advisor_id == advisor_id))
    return result.scalar_one_or_none()


async def get_all_advisors(db:AsyncSession) -> list[Advisor]:
   result = await db.execute(select(Advisor))
   return result.scalars().all()


async def update_advisor(
    db: AsyncSession,
    advisor: Advisor,
    actor_name: str,       # NEW: Name from token
    advisor_name: str | None = None,
    team: str | None = None
) -> Advisor:
    if advisor_name is not None:
        advisor.advisor_name = advisor_name
    if team is not None:
        advisor.team = team
    
    # Track who updated the record
    advisor.updated_by = actor_name 
    
    await db.commit()
    await db.refresh(advisor)
    return advisor

    
async def delete_advisor(db:AsyncSession , advisor_id:int)-> bool:
    result = await db.execute(select(Advisor).where(Advisor.advisor_id == advisor_id))
    advisor = result.scalar_one_or_none()

    if not advisor:
        return False
    await db.delete(advisor)
    await db.commit()
    return True

