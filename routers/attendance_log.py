from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from utilities.database import get_db
from utilities.auth import get_current_user
from services.email_notification_service import create_and_send_notification

from models.user import User
from models.attendance_log import AttendanceLog
from models.attendance_temporary import AttendanceTemporary
from models.attendance_code import AttendanceCode
from validators.attendance_log import AttendanceCodeInput
from validators.attendance_log import AttendanceLogOut

router = APIRouter(prefix="/attendance", tags=["Attendance"])

# -------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models.attendance_log import AttendanceLog
from models.attendance_code import AttendanceCode
from models.attendance_temporary import AttendanceTemporary
from models.user import User
from utilities.database import get_db
from utilities.auth import get_current_user
from validators.attendance_log import AttendanceCodeInput
from services.email_notification_service import create_and_send_notification
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/going-to-church")
def going_to_church(
    code_input: AttendanceCodeInput,  # ✅ Receive the 6-digit code
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if code is valid
    code_record = db.query(AttendanceCode).filter(
        AttendanceCode.code == code_input.code,
        AttendanceCode.code_type == "IN",
        AttendanceCode.expires_at > datetime.utcnow()
    ).first()
    if not code_record:
        raise HTTPException(status_code=400, detail="Invalid or expired IN code.")

    # Check if user already inside
    temp_attendance = db.query(AttendanceTemporary).filter(
        AttendanceTemporary.user_id == current_user.id
    ).first()
    if temp_attendance:
        raise HTTPException(status_code=400, detail="Already marked inside the church.")

    # Save attendance log in IST
    log_entry = AttendanceLog(
    user_id=current_user.id,
    status="present",
    timestamp=datetime.now(IST)  # ✅ IST
    )
    db.add(log_entry)

    # Save in temporary table in IST
    temp_entry = AttendanceTemporary(
    user_id=current_user.id,
    status="present",
    timestamp=datetime.now(IST)  # ✅ IST
    )
    db.add(temp_entry)
    db.commit()

    # Send email notification
    create_and_send_notification(
        db=db,
        user_id=current_user.id,
        recipient_email=current_user.email,
        was_present=True
    )

    return {"message": "Attendance recorded successfully."}


@router.post("/going-out-of-church")
def going_out_of_church(
    code_input: AttendanceCodeInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if code is valid
    code_record = db.query(AttendanceCode).filter(
        AttendanceCode.code == code_input.code,
        AttendanceCode.code_type == "OUT",
        AttendanceCode.expires_at > datetime.utcnow()
    ).first()
    if not code_record:
        raise HTTPException(status_code=400, detail="Invalid or expired OUT code.")

    # Check if user is inside
    temp_attendance = db.query(AttendanceTemporary).filter(
        AttendanceTemporary.user_id == current_user.id
    ).first()
    if not temp_attendance:
        raise HTTPException(status_code=400, detail="You are not inside the church.")

    # Remove from temporary table
    db.delete(temp_attendance)
    db.commit()

    return {"message": "Exit recorded successfully."}

@router.get("/my-logs", response_model=List[AttendanceLogOut])
def get_my_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logs = db.query(AttendanceLog).filter_by(user_id=current_user.id)\
        .order_by(AttendanceLog.timestamp.desc()).all()
    return logs

# -------------------------------
# 4. Admin: Get all logs
# -------------------------------
@router.get("/all", response_model=List[AttendanceLogOut])
def get_all_logs(db: Session = Depends(get_db)):
    return db.query(AttendanceLog)\
        .order_by(AttendanceLog.timestamp.desc())\
        .all()


# -------------------------------
# 5. Admin: Get logs by date
# -------------------------------
@router.get("/date/{date}", response_model=List[AttendanceLogOut])
def get_logs_by_date(
    date: str,
    db: Session = Depends(get_db)
):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    return db.query(AttendanceLog)\
        .filter(AttendanceLog.timestamp.cast("date") == target_date)\
        .order_by(AttendanceLog.timestamp.desc())\
        .all()
