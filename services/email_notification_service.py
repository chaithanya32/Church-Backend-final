from models.email_notification import EmailNotification
from sqlalchemy.orm import Session
from datetime import datetime
from validators.email_notification import EmailNotificationCreate
from utilities.email import send_email

def create_and_send_notification(db: Session, user_id: int, recipient_email: str, was_present: bool):
    subject = "Thank you for attending Church" if was_present else "We missed you at Church"
    body = "We're glad you joined us!" if was_present else "Please try to attend next Sunday."
    status = "sent" if was_present else "pending"
    sent_at = datetime.utcnow() if was_present else None

    notification = EmailNotification(
        user_id=user_id,
        recipient_email=recipient_email,
        subject=subject,
        body=body,
        status=status,
        sent_at=sent_at,
        was_present=was_present,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    if was_present:
        send_email(to=recipient_email, subject=subject, body=body)

    return notification


def create_and_send_exit_notification(db: Session, user_id: int, recipient_email: str):
    subject = "Hope you had a blessed time at Church"
    body = "Thank you for being with us today. Have a wonderful week ahead!"
    status = "sent"
    sent_at = datetime.utcnow()

    notification = EmailNotification(
        user_id=user_id,
        recipient_email=recipient_email,
        subject=subject,
        body=body,
        status=status,
        sent_at=sent_at,
        was_present=True  # still mark as present, since they attended
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    # Immediately send exit email
    send_email(to=recipient_email, subject=subject, body=body)

    return notification
