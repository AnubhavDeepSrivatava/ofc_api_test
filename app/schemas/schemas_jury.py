from pydantic import BaseModel, EmailStr

class JuryCreate(BaseModel):
    user_id: int
    jury_name: str
    jury_email: EmailStr

class JuryResponse(JuryCreate):
    jury_id: int

    class Config:
        from_attributes = True

