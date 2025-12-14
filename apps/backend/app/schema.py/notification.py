
from datetime import date
from pydantic import BaseModel

class NotificationBase(BaseModel):
    reminder_date: date
    message: str

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: int
    is_sent: bool

    class Config:
        from_attributes = True
