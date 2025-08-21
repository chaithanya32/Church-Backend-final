from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from validators.password_reset import (
    ForgotPasswordRequest, VerifyOTPRequest, ResetPasswordRequest
)
from services.password_reset_service import (
    request_otp, verify_otp, reset_password
)
from utilities.database import get_db

router = APIRouter(prefix="/auth", tags=["Password Reset"])

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        request_otp(db, data.email)
        return {"msg": "OTP sent to email"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/verify-otp")
def check_otp(data: VerifyOTPRequest, db: Session = Depends(get_db)):
    if verify_otp(db, data.email, data.otp):
        return {"msg": "OTP verified"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

@router.post("/reset-password")
def reset_user_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        reset_password(db, data.email, data.otp, data.new_password)
        return {"msg": "Password reset successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
