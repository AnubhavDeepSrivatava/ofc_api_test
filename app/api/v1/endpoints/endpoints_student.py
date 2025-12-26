from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.schemas_student import StudentCreate, StudentResponse
from app.services.services_student import *
from app.core.security import get_token_user_name

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse)
async def create(student: StudentCreate, db: AsyncSession = Depends(get_db),actor_name: str = Depends(get_token_user_name)):
    try:
        return await create_student_service(db, **student.model_dump(),actor_name=actor_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{student_id}", response_model=StudentResponse)
async def get(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await get_student_service(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{student_id}", response_model=StudentResponse)
async def update(
    student_id: int,
    student_update: StudentCreate, # Or a separate Update schema
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name) # Requires 'token' header
):
    try:
        return await update_student_service(
            db, 
            student_id=student_id, 
            actor_name=actor_name, 
            **student_update.model_dump()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

