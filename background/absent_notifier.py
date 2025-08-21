from datetime import datetime, date, time
import pytz
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.user import User
from models.attendance_log import AttendanceLog
from models.email_notification import EmailNotification
from utilities.email import send_email


def get_utc_range_for_ist_day(ist_date: date):
    """Returns UTC start and end datetime for a given IST date"""
    ist = pytz.timezone("Asia/Kolkata")
    start_ist = datetime.combine(ist_date, time.min)
    end_ist = datetime.combine(ist_date, time.max)
    start_utc = ist.localize(start_ist).astimezone(pytz.utc)
    end_utc = ist.localize(end_ist).astimezone(pytz.utc)
    return start_utc, end_utc


def mark_absentees_and_queue_emails(db: Session):
    today = date.today()

    # Get UTC start and end for today in IST
    start_utc, end_utc = get_utc_range_for_ist_day(today)

    # Fetch all users
    all_users = db.query(User).all()

    # Fetch attended users (filtering by UTC but using IST day)
    attended_users = db.query(AttendanceLog.user_id).filter(
        and_(
            AttendanceLog.timestamp >= start_utc,
            AttendanceLog.timestamp <= end_utc
        )
    ).distinct()

    attended_user_ids = {user_id for (user_id,) in attended_users}

    # Queue emails for absent users
    for user in all_users:
        if user.id not in attended_user_ids:
            notification = EmailNotification(
                user_id=user.id,
                recipient_email=user.email,
                subject="You missed church today!",
                body="We noticed you weren't present at church today. We missed you!",
                status="pending"
            )
            db.add(notification)

    db.commit()
    print("Pending emails created for absent users.")
