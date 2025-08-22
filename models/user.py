from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from utilities.database import Base
from sqlalchemy.orm import relationship
from .admin import Admin

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # maps to user_name in frontend
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)

    # New fields
    id_number = Column(String, nullable=True)
    batch = Column(String, nullable=True)
    branch = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    gender = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    attendance_logs = relationship("AttendanceLog", back_populates="user")
    otp_resets = relationship("PasswordResetOTP", back_populates="user")
    temporary_attendance_logs = relationship("AttendanceTemporary", back_populates="user")
    admin = relationship("Admin", uselist=False, back_populates="user")

