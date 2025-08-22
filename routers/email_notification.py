from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utilities.database import get_db
from models.email_notification import EmailNotification
from validators.email_notification import EmailNotificationCreate, EmailNotificationOut
from typing import List
from utilities.auth import get_current_user

router = APIRouter(prefix="/email-notifications", tags=["Email Notifications"])

# Create a notification
@router.post("/", response_model=EmailNotificationOut)
def create_notification(payload: EmailNotificationCreate, db: Session = Depends(get_db)):
    notification = EmailNotification(
        recipient_email=payload.recipient_email,
        subject=payload.subject,
        body=payload.message,
        status=payload.status  
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

# Get all notifications
@router.get("/", response_model=List[EmailNotificationOut])
def list_notifications(db: Session = Depends(get_db)):
    return db.query(EmailNotification).order_by(EmailNotification.sent_at.desc()).all()

# Update notification status
@router.patch("/{notification_id}", response_model=EmailNotificationOut)
def update_status(notification_id: int, status: str, db: Session = Depends(get_db)):
    notification = db.query(EmailNotification).get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.status = status
    db.commit()
    db.refresh(notification)
    return notification

@router.get("/my", response_model=list[EmailNotificationOut])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notifications = db.query(EmailNotification).filter(
        EmailNotification.user_id == current_user.id
    ).order_by(EmailNotification.sent_at.desc()).all()
    return notifications
