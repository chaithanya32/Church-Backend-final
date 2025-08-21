import random
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.attendance_code import AttendanceCode
from models.volunteer import Volunteer


CODE_EXPIRY_MINUTES = 5  # Validity window for codes


def generate_code() -> str:
    """Generate a unique 6-digit code"""
    return str(random.randint(100000, 999999))


def expire_existing_codes(db: Session, volunteer_id: int, code_type: str):
    """Expire existing active codes of the same type for this volunteer"""
    db.query(AttendanceCode).filter(
        AttendanceCode.created_by_id == volunteer_id,
        AttendanceCode.code_type == code_type,
        AttendanceCode.expires_at > datetime.utcnow()
    ).update({AttendanceCode.expires_at: datetime.utcnow()})
    db.commit()


def generate_in_code_service(db: Session, current_user):
    """Generate a new IN code, expire old one if exists"""
    volunteer = db.query(Volunteer).filter(Volunteer.user_id == current_user.id).first()
    if not volunteer:
        raise HTTPException(status_code=403, detail="Only volunteers can generate codes.")

    new_code = AttendanceCode(
    code=generate_code(),
    code_type="IN",   # or "EXIT"
    created_by_id=volunteer.id,  # use volunteer.id, NOT user.id
    expires_at=datetime.utcnow() + timedelta(minutes=5)
)


    db.add(new_code)
    db.commit()
    db.refresh(new_code)

    return {
        "message": "IN code generated successfully.",
        "code": new_code.code,
        "expires_at": new_code.expires_at
    }


def generate_exit_code_service(db: Session, current_user):
    """Generate a new EXIT code, expire old one if exists"""
    volunteer = db.query(Volunteer).filter(Volunteer.user_id == current_user.id).first()
    if not volunteer:
        raise HTTPException(status_code=403, detail="Only volunteers can generate codes.")

    new_code = AttendanceCode(
        code=generate_code(),
        code_type="OUT",
        created_by_id=volunteer.id,  # use volunteer table PK, not user.id
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(new_code)
    db.commit()
    db.refresh(new_code)

    return {
        "message": "EXIT code generated successfully.",
        "code": new_code.code,
        "expires_at": new_code.expires_at
    }
