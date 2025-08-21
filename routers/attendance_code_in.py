from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from utilities.auth import get_current_user
from utilities.database import get_db
from services.attendance_code_service import generate_in_code_service

router = APIRouter(prefix="/attendance_code_in", tags=["Attendance Code IN"])

@router.post("/generate")
def generate_attendance_code_in(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Generate a new IN attendance code for the volunteer.
    Expires any previous IN code immediately.
    """
    return generate_in_code_service(db=db, current_user=current_user)
