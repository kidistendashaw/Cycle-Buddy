from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# 👉 Create reminder
@router.post("/add", response_model=schemas.NotificationResponse)
def add_notification(
    data: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_note = models.Notification(
        user_id=user.id,
        reminder_date=data.reminder_date,
        message=data.message
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


# 👉 Get upcoming reminders (today or future)
@router.get("/upcoming", response_model=list[schemas.NotificationResponse])
def get_upcoming_notifications(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    today = date.today()
    notes = (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user.id)
        .filter(models.Notification.reminder_date >= today)
        .order_by(models.Notification.reminder_date)
        .all()
    )
    return notes


# 👉 Mark as sent (optional for later automation)
@router.patch("/{id}/sent", response_model=schemas.NotificationResponse)
def mark_notification_sent(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    note = (
        db.query(models.Notification)
        .filter(models.Notification.id == id)
        .filter(models.Notification.user_id == user.id)
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail="Notification not found")

    note.is_sent = True
    db.commit()
    db.refresh(note)
    return note
