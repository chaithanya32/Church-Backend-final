from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from utilities.database import Base
import enum

class CodeTypeEnum(str, enum.Enum):
    IN = "in"
    OUT = "out"

class AttendanceCode(Base):
    __tablename__ = "attendance_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6), unique=True, nullable=False)
    code_type = Column(Enum(CodeTypeEnum), nullable=False)  # in or out

    created_by_id = Column(Integer, ForeignKey("volunteers.id"))
    created_by = relationship("Volunteer")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
