from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services import services
from app.schemas.schema_course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
)

router = APIRouter(
    prefix="/courses",
    tags=["Course"]
)


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    payload: CourseCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = "system"
):
    return await services.create_entity(db, "course", payload.model_dump(), actor_name)


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.get_entity(db, "course", course_id)


@router.get("/", response_model=list[CourseResponse])
async def get_courses(
    db: AsyncSession = Depends(get_db),
):
    return await services.list_entity(db, "course")


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    await services.delete_entity(db, "course", course_id)
    return None
