from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone
from utilities.database import Base

IST = timezone('Asia/Kolkata')

def current_ist_time():
    return datetime.now(IST)

class EmailNotification(Base):
    __tablename__ = 'email_notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    recipient_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending or sent
    sent_at = Column(DateTime, default=current_ist_time)
    was_present = Column(Boolean, nullable=True)

    user = relationship("User")
