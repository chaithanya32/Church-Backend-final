# services/email_scheduler_service.py

from sqlalchemy.orm import Session
from datetime import datetime
from models.user import User
from models.attendance_log import AttendanceLog
from models.email_notification import EmailNotification
from utilities.email import send_email


def mark_absentees_and_queue_emails(db: Session):
    """Find users who did NOT attend and create pending notifications."""
    today = datetime.now().date()

    # Get all active users
    users = db.query(User).filter(User.is_active == True).all()

    for user in users:
        attended = (
            db.query(AttendanceLog)
            .filter(
                AttendanceLog.user_id == user.id,
                AttendanceLog.timestamp >= datetime.combine(today, datetime.min.time()),
                AttendanceLog.timestamp <= datetime.combine(today, datetime.max.time()),
            )
            .first()
        )

        if not attended:
            # Queue a "We missed you" email (pending)
            notification = EmailNotification(
                user_id=user.id,
                recipient_email=user.email,
                subject="We missed you at Church",
                body="Please try to attend next Sunday.",
                status="pending",
                was_present=False,
            )
            db.add(notification)

    db.commit()


def send_pending_notifications(db: Session):
    """Send all pending notifications and mark them as sent."""
    pending_emails = (
        db.query(EmailNotification).filter(EmailNotification.status == "pending").all()
    )

    for notification in pending_emails:
        send_email(
            to=notification.recipient_email,
            subject=notification.subject,
            body=notification.body,
        )
        notification.status = "sent"
        notification.sent_at = datetime.utcnow()

    db.commit()
