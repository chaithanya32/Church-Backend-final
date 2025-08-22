from pydantic import BaseModel, EmailStr
from datetime import datetime

class AdminCreate(BaseModel):
    email: EmailStr  # admin assigns using user email

class AdminOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
