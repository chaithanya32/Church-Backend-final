# routers/email_tasks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.email_scheduler_service import mark_absentees_and_queue_emails, send_pending_notifications
from services.password_reset_service import cleanup_expired_otps
from utilities.database import get_db
from models.user import User
from models.volunteer import Volunteer
from utilities.auth import get_current_user
import logging

router = APIRouter(prefix="/email-tasks", tags=["Email Tasks"])

logger = logging.getLogger("email_tasks")
logging.basicConfig(level=logging.INFO)

@router.post("/run-daily")
def run_daily_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ Check if the current_user exists in volunteers table
    volunteer = db.query(Volunteer).filter(Volunteer.user_id == current_user.id).first()
    if not volunteer:
        raise HTTPException(status_code=403, detail="Only volunteers can run this task.")

    # Step 1: Mark absentees and queue emails
    mark_absentees_and_queue_emails(db)

    # Step 2: Send pending emails
    send_pending_notifications(db)

    # Step 3: Clean expired OTPs
    cleanup_expired_otps(db)

    # ✅ Log volunteer info
    logger.info(f"✅ Daily email tasks triggered by Volunteer: {current_user.name} "
                f"(ID: {current_user.id}, Email: {current_user.email})")

    return {"message": f"Daily email tasks completed successfully by {current_user.name}."}
