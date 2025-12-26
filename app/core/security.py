# # from my_company_core.auth import get_current_user

# # Placeholder for local security logic
# def get_current_user_stub():
#     pass


from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from sqlalchemy import select
from app.models.user import User

def is_admin():
    return True  # placeholder for now


async def get_token_user_name(token: str = Header(...), db: AsyncSession = Depends(get_db)):
    # 1. 'token' arrives as "1" (the user_id)
    try:
        user_id_int = int(token)
    except ValueError:
        raise HTTPException(status_code=400, detail="Token must be a numeric User ID")
    
    # 2. Look up that user's name in the DB
    result = await db.execute(select(User).where(User.user_id == user_id_int))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User in token not found")
    
    # 3. Return the user_name (e.g., "Rahul") to be used in created_by/updated_by
    return user.user_name

