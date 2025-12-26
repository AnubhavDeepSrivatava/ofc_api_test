from pydantic import BaseModel
from typing import Optional


# Used when creating an activity (POST)
class ActivityCreate(BaseModel):
    activity_name: str
    collaboration_link_template: Optional[str] = None
    course_id: int


# Used when updating an activity (PUT/PATCH)
class ActivityUpdate(BaseModel):
    activity_name: Optional[str] = None
    collaboration_link_template: Optional[str] = None
    course_id: Optional[int] = None


# Used when returning activity data (GET response)
class ActivityResponse(BaseModel):
    activity_id: int
    activity_name: str
    collaboration_link_template: Optional[str]
    course_id: int

    class Config:
        from_attributes = True   # for SQLAlchemy ORM
