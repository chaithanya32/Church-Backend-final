from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from utilities.auth import get_current_user
from utilities.database import get_db
from services.attendance_code_service import generate_exit_code_service

router = APIRouter(prefix="/attendance_code_out", tags=["Attendance Code OUT"])

@router.post("/generate")
def generate_attendance_code_out(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Generate a new EXIT attendance code for the volunteer.
    Expires any previous EXIT code immediately.
    """
    return generate_exit_code_service(db=db, current_user=current_user)
