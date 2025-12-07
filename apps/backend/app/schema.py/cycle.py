from pydantic import BaseModel
from datetime import date
from typing import Optional

class CycleCreate(BaseModel):
    last_period_start: date
    period_length: Optional[int] = 5
    cycle_length: Optional[int] = 28
    notes: Optional[str] = None

class CycleResponse(BaseModel):
    current_day: int
    phase: str
    days_until_next_period: int
    tips: str

    class Config:
        orm_mode = True
