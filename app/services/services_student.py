from sqlalchemy.ext.asyncio import AsyncSession 
from app.crud.student_crud import create_student, get_student_by_user, get_student_by_id, get_all_students, update_student, delete_student

async def create_student_service(db: AsyncSession,actor_name: str, **data):
    if await get_student_by_user(db, data["user_id"]):
        raise ValueError("Student already exists for this user  ")
    return await create_student(db,actor_name=actor_name, **data)

async def get_student_service(db: AsyncSession, student_id: int):
    student = await get_student_by_id(db, student_id)
    if not student:
        raise ValueError("Student not found ")
    return student

async def list_students_service(db: AsyncSession, skip: int, limit: int):
    return await get_all_students(db)[skip: skip + limit]

async def update_student_service(db: AsyncSession, student_id: int, actor_name: str, **data):
    student = await get_student_by_id(db, student_id)
    if not student:
        raise ValueError("Student not found")
    return await update_student(db, student, actor_name=actor_name, **data)

async def delete_student_service(db: AsyncSession, student_id: int):
    if not await delete_student(db, student_id):
        raise ValueError("Student not found ")
    return True

