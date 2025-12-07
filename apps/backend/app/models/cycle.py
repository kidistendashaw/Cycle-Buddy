from sqlalchemy import Column, Integer, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Cycle(Base):
    __tablename__ = "cycles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    last_period_start = Column(Date, nullable=False)
    period_length = Column(Integer, default=5)
    cycle_length = Column(Integer, default=28)

    user = relationship("User", back_populates="cycles")
