from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(
    prefix="/cycle",
    tags=["cycles"]
)

# Helper: calculate phase
def calculate_cycle_phase(last_period: date, cycle_length: int, period_length: int):
    today = date.today()
    days_since_start = (today - last_period).days % cycle_length + 1

    if days_since_start <= period_length:
        phase = "Menstrual"
        tips = "Rest, stay hydrated, and take care of your mood"
    elif days_since_start <= 11:
        phase = "Follicular"
        tips = "Energy is up! Great time to start new projects"
    elif days_since_start <= 16:
        phase = "Ovulation"
        tips = "You may feel more social and confident"
    else:
        phase = "Luteal"
        tips = "Mood swings possible, try relaxation techniques"

    days_until_next_period = cycle_length - days_since_start + 1

    return days_since_start, phase, days_until_next_period, tips


@router.post("/add", response_model=schemas.CycleCreate)
def add_cycle(cycle: schemas.CycleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_cycle = models.Cycle(
        user_id=user.id,
        last_period_start=cycle.last_period_start,
        period_length=cycle.period_length,
        cycle_length=cycle.cycle_length,
        notes=cycle.notes
    )
    db.add(new_cycle)
    db.commit()
    db.refresh(new_cycle)
    return cycle


@router.get("/current", response_model=schemas.CycleResponse)
def current_cycle(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cycle = db.query(models.Cycle).filter(models.Cycle.user_id == user.id).order_by(models.Cycle.last_period_start.desc()).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="No cycle data found")
    
    current_day, phase, days_until_next_period, tips = calculate_cycle_phase(
        cycle.last_period_start,
        cycle.cycle_length,
        cycle.period_length
    )
    return {
        "current_day": current_day,
        "phase": phase,
        "days_until_next_period": days_until_next_period,
        "tips": tips
    }


@router.get("/history")
def cycle_history(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cycles = db.query(models.Cycle).filter(models.Cycle.user_id == user.id).order_by(models.Cycle.last_period_start.desc()).all()
    return cycles
