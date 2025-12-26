from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

class Jury(Base):
    __tablename__ = "juries"

    jury_id = Column(Integer, primary_key=True)
    jury_name = Column(String(100))
    jury_email = Column(String(150))
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)

