from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    reminder_date = Column(Date, nullable=False)
    message = Column(String(255), nullable=False)
    is_sent = Column(Boolean, default=False)

    user = relationship("User", back_populates="notifications")
