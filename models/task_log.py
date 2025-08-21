# models/task_log.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from utilities.database import Base

class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"))
    task_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # success / failed
    run_at = Column(DateTime, default=datetime.utcnow)

    # relationship to volunteer (if you want)
    volunteer = relationship("Volunteer", back_populates="task_logs")
