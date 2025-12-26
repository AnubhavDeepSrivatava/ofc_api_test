from pydantic import BaseModel

class AdvisorCreate(BaseModel):
    user_id: int
    advisor_name: str
    team: str

class AdvisorResponse(AdvisorCreate):
    advisor_id: int

    class Config:
        from_attributes = True

