# run_daily_email_tasks.py

from services.email_scheduler_service import mark_absentees_and_queue_emails, send_pending_notifications
from services.password_reset_service import cleanup_expired_otps
from utilities.database import get_db

if __name__ == "__main__":
    db = next(get_db())

    # Step 1: Mark absentees and queue emails
    mark_absentees_and_queue_emails(db)
    print("Pending emails created for absent users.")

    # Step 2: Send pending emails
    send_pending_notifications(db)
    print("Pending emails sent and status updated.")

    # Step 3: Clean up expired OTPs
    cleanup_expired_otps(db)
    print("Expired OTPs cleaned up.")
