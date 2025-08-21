from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from utilities.database import Base

IST = timezone('Asia/Kolkata')

def current_ist_time():
    return datetime.now(IST)

class AttendanceLog(Base):
    __tablename__ = "attendance_logs"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False, default="present")
    timestamp = Column(DateTime, default=current_ist_time)

    user = relationship("User", back_populates="attendance_logs")
