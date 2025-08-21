from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utilities.database import get_db
from models.attendance_temporary import AttendanceTemporary
from models.user import User

router = APIRouter(prefix="/attendance_temp", tags=["Temporary Attendance"])

@router.get("/batch-wise")
def get_batch_wise_attendance(db: Session = Depends(get_db)):
    """
    Returns attendance grouped by batch with id_number and in_time
    """
    attendance_records = db.query(AttendanceTemporary).join(User).all()

    batch_dict = {}
    for idx, record in enumerate(attendance_records, start=1):
        batch_name = record.user.batch  # batch should exist in User model
        if batch_name not in batch_dict:
            batch_dict[batch_name] = []

        batch_dict[batch_name].append({
            "serial": len(batch_dict[batch_name]) + 1,
            "id": record.user.id,
            "id_number": record.user.id_number,
            "name": record.user.name,
            "in_time": record.timestamp.strftime("%H:%M:%S")
        })

    return batch_dict
