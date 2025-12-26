from pydantic import BaseModel
from typing import Optional


# Used when creating a course (POST)
class CourseCreate(BaseModel):
    course_name: str
    sequence_number: int
    program_id: int


# Used when updating a course (PUT/PATCH)
class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    sequence_number: Optional[int] = None
    program_id: Optional[int] = None


# Used when returning course data (GET response)
class CourseResponse(BaseModel):
    course_id: int
    course_name: str
    sequence_number: int
    program_id: int

    class Config:
        from_attributes = True
