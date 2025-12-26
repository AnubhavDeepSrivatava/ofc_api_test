from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student  import Student , GenderEnum
from sqlalchemy import select


async def create_student(
    db: AsyncSession,
    user_id: int,
    school_id: int,
    gender: GenderEnum,
    actor_name: str,
    idea: str | None = None
) -> Student:
    student = Student(
        user_id=user_id,
        school_id=school_id,
        gender=gender,
        idea=idea,
        created_by=actor_name, # Storing the name
        updated_by=None
    )
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student

async def get_student_by_user(db: AsyncSession, user_id: int) -> Student | None:
    result = await db.execute(select(Student).where(Student.user_id == user_id))
    return result.scalar_one_or_none()


async def get_student_by_id(db:AsyncSession , student_id:int) -> Student | None:
    result = await db.execute(select(Student).where(Student.student_id == student_id))
    return result.scalar_one_or_none()


async def get_all_students(db:AsyncSession) -> list[Student]:
    result = await db.execute(select(Student))
    return result.scalars().all()

async def update_student(
    db: AsyncSession,
    student: Student,
    actor_name: str, # Name from token
    gender: GenderEnum | None = None,
    idea: str | None = None,
    onboarding_process_done: bool | None = None
) -> Student:
    if gender is not None:
        student.gender = gender
    if idea is not None:
        student.idea = idea
    if onboarding_process_done is not None:
        student.onboarding_process_done = onboarding_process_done

    student.updated_by = actor_name # Track who updated it
    
    await db.commit()
    await db.refresh(student)
    return student

async def delete_student(db:AsyncSession , student_id:int) -> bool:
    result = await db.execute(select(Student).where(Student.student_id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        return False
    await db.delete(student)
    await db.commit()
    return True

