from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.schemas_student import StudentCreate, StudentResponse
from app.services import services
from app.core.security import get_token_user_name

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse)
async def create(student: StudentCreate, db: AsyncSession = Depends(get_db), actor_name: str = Depends(get_token_user_name)):
    return await services.create_entity(db, "student", student.model_dump(), actor_name)

@router.get("/{student_id}", response_model=StudentResponse)
async def get(student_id: int, db: AsyncSession = Depends(get_db)):
    return await services.get_entity(db, "student", student_id)

@router.put("/{student_id}", response_model=StudentResponse)
async def update(
    student_id: int,
    student_update: StudentCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
):
    return await services.update_entity(db, "student", student_id, student_update.model_dump(), actor_name)

