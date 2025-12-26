from pydantic import BaseModel
from enum import Enum

class GenderEnum(str,Enum):
    M="M"
    F="F"
    OTHER="OTHER"

class StudentCreate(BaseModel):
    user_id :int
    school_id :int
    gender: GenderEnum
    idea: str | None = None

class StudentResponse(StudentCreate):
    student_id:int
    onboarding_process_done:bool

    class Config:
        from_attributes = True

