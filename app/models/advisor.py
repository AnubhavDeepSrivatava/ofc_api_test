from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

class Advisor(Base):
    __tablename__ = "advisors"

    advisor_id = Column(Integer, primary_key=True)
    advisor_name = Column(String(100))
    team = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)

