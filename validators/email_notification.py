from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmailNotificationCreate(BaseModel):
    user_id: Optional[int]
    recipient_email: EmailStr
    subject: str
    body: str
    status: str = "pending"
    sent_at: Optional[datetime]
    was_present: Optional[bool]

class EmailNotificationOut(BaseModel):
    id: int
    user_id: Optional[int]
    recipient_email: EmailStr
    subject: str
    body: str
    status: str
    sent_at: datetime
    was_present: Optional[bool]

    class Config:
        orm_mode = True
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmailNotificationCreate(BaseModel):
    user_id: Optional[int]
    recipient_email: EmailStr
    subject: str
    body: str
    status: str = "pending"
    sent_at: Optional[datetime]
    was_present: Optional[bool]

class EmailNotificationOut(BaseModel):
    id: int
    user_id: Optional[int]
    recipient_email: EmailStr
    subject: str
    body: str
    status: str
    sent_at: datetime
    was_present: Optional[bool]

    class Config:
        orm_mode = True