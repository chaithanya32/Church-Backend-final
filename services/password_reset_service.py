import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.user import User
from models.password_reset import PasswordResetOTP
from utilities.email import send_email
from passlib.hash import bcrypt


def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


def request_otp(db: Session, email: str):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise ValueError("User not found")

    # Check for recent OTP (within 1 minute)
    recent = (
        db.query(PasswordResetOTP)
        .filter(PasswordResetOTP.user_id == user.id)
        .order_by(PasswordResetOTP.expires_at.desc())
        .first()
    )
    if recent and (datetime.utcnow() - (recent.expires_at - timedelta(minutes=10))).total_seconds() < 60:
        raise ValueError("OTP already sent recently. Try again after a minute.")

    # Generate and store new OTP
    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Delete old OTPs and add new one
    db.query(PasswordResetOTP).filter_by(user_id=user.id).delete()
    db.add(PasswordResetOTP(user_id=user.id, otp=otp, expires_at=expires_at))
    db.commit()

    # ✅ Send OTP using updated email function
    send_email(
        to=email,
        subject="Password Reset OTP",
        otp=otp
    )


def verify_otp(db: Session, email: str, otp: str):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        return False

    record = (
        db.query(PasswordResetOTP)
        .filter_by(user_id=user.id, otp=otp)
        .first()
    )

    return record and record.expires_at >= datetime.utcnow()


def reset_password(db: Session, email: str, otp: str, new_password: str):
    if not verify_otp(db, email, otp):
        raise ValueError("Invalid or expired OTP")

    user = db.query(User).filter_by(email=email).first()
    user.password_hash = bcrypt.hash(new_password)

    # Delete the OTP after successful reset
    db.query(PasswordResetOTP).filter_by(user_id=user.id).delete()
    db.commit()

def cleanup_expired_otps(db: Session):
    db.query(PasswordResetOTP).filter(
        PasswordResetOTP.expires_at < datetime.utcnow()
    ).delete()
    db.commit()
