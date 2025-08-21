from pydantic import BaseModel
from datetime import datetime

class AttendanceTemporaryCreate(BaseModel):
    user_id: int
    status: str = "present"

class AttendanceTemporaryOut(BaseModel):
    id: int
    user_id: int
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True
