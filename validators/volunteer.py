from datetime import datetime
from pydantic import BaseModel, EmailStr

class VolunteerCreate(BaseModel):
    user_email: EmailStr

class VolunteerOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
