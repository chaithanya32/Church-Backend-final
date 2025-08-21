from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from utilities.database import Base
from models.task_log import TaskLog

class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    task_logs = relationship("TaskLog", back_populates="volunteer")
    user = relationship("User")
